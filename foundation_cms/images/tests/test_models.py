import io
import shutil
import tempfile
from unittest.mock import patch

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage, default_storage
from django.test import TestCase, override_settings
from PIL import Image as PILImage

from foundation_cms.images.models import FoundationCustomImage, PassthroughRendition
from foundation_cms.images.webp import utils as webp_utils


# These have to be images Pillow can actually decode, not the hand-built
# structures test_gif.py uses: Wagtail's file field declares width_field and
# height_field, so Django reads the dimensions off the file on assignment and
# writes NULL into two NOT NULL columns for anything it cannot open.
def gif_bytes(frames=3, size=(8, 6)):
    out = io.BytesIO()
    images = [PILImage.new("P", size, color=index % 2) for index in range(frames)]
    images[0].save(out, format="GIF", save_all=True, append_images=images[1:], loop=0)
    return out.getvalue()


def image_bytes(fmt="JPEG", size=(8, 6)):
    out = io.BytesIO()
    PILImage.new("RGB", size).save(out, format=fmt)
    return out.getvalue()


def content_for(name):
    """
    A named ContentFile, which the name is load-bearing for.

    FieldFile.save() hands the content object back to the field so the
    dimensions can be read off it. Django wraps an unnamed one in a FieldFile
    with no name, which is falsy -- so update_dimension_fields takes its
    "no file" branch and writes NULL into width and height.
    """
    data = gif_bytes() if name.lower().endswith(".gif") else image_bytes()
    return ContentFile(data, name=name)


# Conversion is asynchronous everywhere these tests care about; leaving the
# synchronous path on would shell out to ffmpeg on every save.
@override_settings(GIF_CONVERT_SYNCHRONOUSLY=False)
class ImageModelTestCase(TestCase):
    def setUp(self):
        media_root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, media_root, ignore_errors=True)
        media = override_settings(MEDIA_ROOT=media_root)
        media.enable()
        self.addCleanup(media.disable)

    def create_image(self, name="first.gif", with_webp=False):
        """An image whose file is committed to storage, as an upload would be."""
        image = FoundationCustomImage(title="An image")
        image.file.save(name, content_for(name), save=False)
        image.save()

        if with_webp:
            image.animated_webp.save("first.webp", ContentFile(b"fake webp"), save=True)

        return FoundationCustomImage.objects.get(pk=image.pk)

    def replace_file(self, image, name):
        image.file.save(name, content_for(name), save=False)
        image.save()
        return image


class FileReplacementTests(ImageModelTestCase):
    """
    Replacing an image's file must not leave it described by the previous one.

    The GIF -> GIF case is the one that shows: without the reset the stale
    animated_webp is still populated, so animated_webp_ready returns it and the
    old animation is served under the new image.
    """

    def test_replacing_a_gif_clears_the_stale_webp(self):
        image = self.create_image(with_webp=True)
        old_webp = image.animated_webp.name

        self.replace_file(image, "second.gif")

        self.assertFalse(image.animated_webp)
        self.assertFalse(default_storage.exists(old_webp))

    def test_replacing_a_gif_recaptures_the_original(self):
        image = self.create_image(with_webp=True)
        old_original = image.original_gif.name

        self.replace_file(image, "second.gif")

        self.assertIn("second", image.original_gif.name)
        self.assertFalse(default_storage.exists(old_original))

    def test_replacing_a_gif_deletes_the_previous_upload(self):
        """
        A divergence from stock Wagtail, which abandons the old object in
        storage. Nothing points at it once the row moves on.
        """
        image = self.create_image()
        previous = image.file.name

        self.replace_file(image, "second.gif")

        self.assertFalse(default_storage.exists(previous))

    def test_replacing_a_gif_keeps_the_new_upload(self):
        image = self.create_image()

        self.replace_file(image, "second.gif")

        self.assertTrue(default_storage.exists(image.file.name))

    def test_a_storage_failure_does_not_break_the_replacement(self):
        """
        Cleaning up after a replace must never cost the editor the replace
        itself, which has already been committed to storage by this point.
        """
        image = self.create_image()

        with patch.object(FileSystemStorage, "delete", side_effect=OSError("bucket on fire")):
            with self.assertLogs("foundation_cms.images.models", level="WARNING"):
                self.replace_file(image, "second.gif")

        self.assertIn("second", image.file.name)
        self.assertFalse(FoundationCustomImage.objects.get(pk=image.pk).animated_webp)

    def test_replacing_a_gif_with_a_jpg_clears_both_fields(self):
        image = self.create_image(with_webp=True)

        self.replace_file(image, "second.jpg")

        self.assertFalse(image.animated_webp)
        self.assertFalse(image.original_gif)

    def test_replacement_is_persisted(self):
        image = self.create_image(with_webp=True)

        self.replace_file(image, "second.jpg")

        self.assertFalse(FoundationCustomImage.objects.get(pk=image.pk).animated_webp)

    def test_replacing_a_gif_asks_for_the_lambdas_output(self):
        """The field may be empty while the Lambda's WebP exists in storage."""
        image = self.create_image()
        previous = image.file.name

        with patch.object(webp_utils, "delete_converted_webp") as delete:
            self.replace_file(image, "second.gif")

        delete.assert_called_once_with(previous)

    def test_replacing_a_gif_purges_renditions(self):
        image = self.create_image()
        image.renditions.create(
            filter_spec="fill-10x10",
            focal_point_key="",
            file=ContentFile(image_bytes(fmt="WEBP", size=(10, 10)), name="r.webp"),
        )

        self.replace_file(image, "second.gif")

        self.assertEqual(image.renditions.count(), 0)

    def test_saving_without_replacing_keeps_the_webp(self):
        image = self.create_image(with_webp=True)
        webp = image.animated_webp.name

        image.title = "Renamed"
        image.save()

        self.assertEqual(image.animated_webp.name, webp)
        self.assertTrue(default_storage.exists(webp))

    def test_a_new_image_is_not_treated_as_a_replacement(self):
        """Nothing is derived yet, so there is nothing to reset."""
        with patch.object(webp_utils, "delete_converted_webp") as delete:
            image = self.create_image()

        delete.assert_not_called()
        self.assertTrue(image.original_gif)


class UnconvertedGifRenditionTests(ImageModelTestCase):
    """
    A GIF with no WebP must never reach Wagtail's resizer: that decodes every
    frame inside the request, which is the allocation behind the 503 -- here
    reachable by any visitor rather than by an editor on upload.
    """

    def test_gif_without_a_webp_is_served_unresized(self):
        image = self.create_image()

        with patch.object(webp_utils, "converted_webp_exists", return_value=False):
            with patch("wagtail.images.models.AbstractImage.get_rendition") as wagtail_resize:
                rendition = image.get_rendition("fill-10x10")

        self.assertIsInstance(rendition, PassthroughRendition)
        wagtail_resize.assert_not_called()

    def test_passthrough_points_at_the_source_file(self):
        image = self.create_image()

        with patch.object(webp_utils, "converted_webp_exists", return_value=False):
            rendition = image.get_rendition("fill-10x10")

        self.assertEqual(rendition.url, image.file.url)
        self.assertEqual((rendition.width, rendition.height), (image.width, image.height))

    def test_non_gif_still_goes_through_wagtail(self):
        image = self.create_image(name="photo.jpg")

        with patch("wagtail.images.models.AbstractImage.get_rendition") as wagtail_resize:
            image.get_rendition("fill-10x10")

        wagtail_resize.assert_called_once()


class ImageDeletionTests(ImageModelTestCase):
    def test_deleting_an_unrendered_gif_removes_the_lambdas_output(self):
        """
        animated_webp is only populated by a render, so an image uploaded and
        deleted straight away has an empty field and a real object in storage.
        """
        image = self.create_image()
        source_name = image.file.name

        with patch.object(webp_utils, "delete_converted_webp") as delete:
            image.delete()

        delete.assert_called_once_with(source_name)

    def test_deleting_a_non_gif_asks_for_nothing(self):
        image = self.create_image(name="photo.jpg")

        with patch.object(webp_utils, "delete_converted_webp") as delete:
            image.delete()

        delete.assert_not_called()

    def test_recorded_webp_is_still_deleted(self):
        image = self.create_image(with_webp=True)
        webp = image.animated_webp.name

        image.delete()

        self.assertFalse(default_storage.exists(webp))
