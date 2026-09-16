from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, override_settings

from foundation_cms.images.forms import (
    FoundationImageForm,
    validate_gif_frame_volume,
    validate_gif_upload_size,
)
from foundation_cms.images.tests.test_gif import build_gif

ONE_MB = 1024 * 1024


def _upload(name, size):
    upload = SimpleUploadedFile(name, b"x", content_type="image/gif")
    upload.size = size
    return upload


@override_settings(GIF_MAX_UPLOAD_SIZE=5 * ONE_MB)
class ValidateGifUploadSizeTests(SimpleTestCase):
    def test_rejects_oversized_gif(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_gif_upload_size(_upload("big.gif", 6 * ONE_MB))

        self.assertEqual(ctx.exception.code, "gif_too_large")

    def test_error_message_names_both_sizes(self):
        """Editors need to know what they uploaded and what the ceiling is."""
        with self.assertRaises(ValidationError) as ctx:
            validate_gif_upload_size(_upload("big.gif", 6 * ONE_MB))

        message = str(ctx.exception.messages[0])
        self.assertIn("6.0", message)
        self.assertIn("5.0", message)

    def test_allows_gif_at_the_limit(self):
        upload = _upload("exact.gif", 5 * ONE_MB)
        self.assertIs(validate_gif_upload_size(upload), upload)

    def test_allows_small_gif(self):
        upload = _upload("small.gif", 100)
        self.assertIs(validate_gif_upload_size(upload), upload)

    def test_ignores_case_of_extension(self):
        with self.assertRaises(ValidationError):
            validate_gif_upload_size(_upload("SHOUTY.GIF", 6 * ONE_MB))

    def test_does_not_limit_other_formats(self):
        """The stricter cap is GIF-only; Wagtail's global limit covers the rest."""
        upload = _upload("huge.jpg", 50 * ONE_MB)
        self.assertIs(validate_gif_upload_size(upload), upload)

    def test_tolerates_none(self):
        self.assertIsNone(validate_gif_upload_size(None))

    def test_tolerates_missing_size(self):
        upload = SimpleUploadedFile("x.gif", b"x")
        del upload.size
        self.assertIs(validate_gif_upload_size(upload), upload)


class DisabledLimitTests(SimpleTestCase):
    @override_settings(GIF_MAX_UPLOAD_SIZE=0)
    def test_zero_disables_the_check(self):
        upload = _upload("enormous.gif", 500 * ONE_MB)
        self.assertIs(validate_gif_upload_size(upload), upload)


class FoundationImageFormCleanFileTests(SimpleTestCase):
    """
    Exercise the form hook itself, not just the validator underneath it.

    """

    def _form_with(self, upload):
        # __new__ skips BaseImageForm.__init__, which wants a collection and a
        # database. clean_file only reads cleaned_data, so this is enough.
        form = FoundationImageForm.__new__(FoundationImageForm)
        form.cleaned_data = {"file": upload}
        return form

    @override_settings(GIF_MAX_UPLOAD_SIZE=5 * ONE_MB)
    def test_passes_an_acceptable_gif_through(self):
        upload = _upload("small.gif", 100)
        self.assertIs(self._form_with(upload).clean_file(), upload)

    @override_settings(GIF_MAX_UPLOAD_SIZE=5 * ONE_MB)
    def test_passes_a_non_gif_through(self):
        """The regression: this raised AttributeError, breaking all uploads."""
        upload = _upload("photo.jpg", 50 * ONE_MB)
        self.assertIs(self._form_with(upload).clean_file(), upload)

    @override_settings(GIF_MAX_UPLOAD_SIZE=5 * ONE_MB)
    def test_still_rejects_an_oversized_gif(self):
        form = self._form_with(_upload("big.gif", 6 * ONE_MB))
        with self.assertRaises(ValidationError) as ctx:
            form.clean_file()

        self.assertEqual(ctx.exception.code, "gif_too_large")


def _gif_upload(name="anim.gif", **kwargs):
    """A real, structurally valid GIF wrapped as an upload."""
    return SimpleUploadedFile(name, build_gif(**kwargs).getvalue(), content_type="image/gif")


@override_settings(GIF_MAX_FRAME_VOLUME=10 * ONE_MB)
class ValidateGifFrameVolumeTests(SimpleTestCase):
    def test_rejects_a_gif_whose_frames_would_not_fit(self):
        """950x950x109 -- the asset that killed a Standard-2X worker."""
        upload = _gif_upload(width=950, height=950, frames=109)

        with self.assertRaises(ValidationError) as ctx:
            validate_gif_frame_volume(upload)

        self.assertEqual(ctx.exception.code, "gif_frame_volume_too_large")

    def test_error_message_names_the_dimensions_and_frames(self):
        """
        The editor has to know what to change, and it is not the file size --
        which is the one thing the old message talked about.
        """
        upload = _gif_upload(width=950, height=950, frames=109)

        with self.assertRaises(ValidationError) as ctx:
            validate_gif_frame_volume(upload)

        message = str(ctx.exception.messages[0])
        self.assertIn("950x950", message)
        self.assertIn("109", message)

    def test_allows_a_modest_animation(self):
        """220x154x21 -- the asset that uploaded without trouble."""
        upload = _gif_upload(width=220, height=154, frames=21)
        self.assertIs(validate_gif_frame_volume(upload), upload)

    def test_rewinds_the_file(self):
        """
        Wagtail's validation and the upload to storage both read this file from
        the start afterwards. Leaving it consumed breaks every GIF upload.
        """
        upload = _gif_upload(width=8, height=8, frames=3)
        validate_gif_frame_volume(upload)
        self.assertEqual(upload.tell(), 0)

    def test_rewinds_the_file_even_when_rejecting(self):
        upload = _gif_upload(width=950, height=950, frames=109)
        with self.assertRaises(ValidationError):
            validate_gif_frame_volume(upload)
        self.assertEqual(upload.tell(), 0)

    def test_ignores_non_gifs(self):
        upload = SimpleUploadedFile("photo.jpg", b"not a gif at all", content_type="image/jpeg")
        self.assertIs(validate_gif_frame_volume(upload), upload)

    def test_tolerates_none(self):
        self.assertIsNone(validate_gif_frame_volume(None))

    def test_passes_unparseable_gifs_through(self):
        """Wagtail's format validation rejects these with a better message."""
        upload = SimpleUploadedFile("broken.gif", b"GIF89a truncated", content_type="image/gif")
        self.assertIs(validate_gif_frame_volume(upload), upload)

    def test_passes_through_a_file_that_is_not_a_gif_despite_its_name(self):
        """Exercises the GifParseError branch: wrong magic, .gif extension."""
        upload = SimpleUploadedFile("liar.gif", b"\x89PNG\r\n\x1a\n" + b"\x00" * 64)
        self.assertIs(validate_gif_frame_volume(upload), upload)

    @override_settings(GIF_MAX_FRAME_VOLUME=0)
    def test_zero_disables_the_check(self):
        upload = _gif_upload(width=950, height=950, frames=109)
        self.assertIs(validate_gif_frame_volume(upload), upload)


@override_settings(GIF_MAX_UPLOAD_SIZE=5 * ONE_MB, GIF_MAX_FRAME_VOLUME=10 * ONE_MB)
class FormAppliesBothLimitsTests(SimpleTestCase):
    def _clean(self, upload):
        form = FoundationImageForm.__new__(FoundationImageForm)
        form.cleaned_data = {"file": upload}
        return form.clean_file()

    def test_rejects_on_frame_volume_even_when_bytes_are_fine(self):
        """
        The gap the byte limit cannot close: this GIF is 5.2 MB on disk, under
        the size cap, and still far too heavy to process.
        """
        upload = _gif_upload(width=950, height=950, frames=109)
        self.assertLess(upload.size, 5 * ONE_MB)

        with self.assertRaises(ValidationError) as ctx:
            self._clean(upload)

        self.assertEqual(ctx.exception.code, "gif_frame_volume_too_large")

    def test_accepts_a_reasonable_gif(self):
        upload = _gif_upload(width=220, height=154, frames=21)
        self.assertIs(self._clean(upload), upload)
