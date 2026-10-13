from unittest import mock

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import FileField
from django.forms.renderers import get_default_renderer
from django.forms.utils import ErrorList
from django.test import SimpleTestCase, override_settings
from wagtail.images.forms import BaseImageForm

from foundation_cms.images.forms import (
    FoundationImageForm,
    normalise_extension,
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


@override_settings(GIF_MAX_UPLOAD_SIZE=5 * ONE_MB, GIF_MAX_FRAME_VOLUME=10 * ONE_MB)
class ScreensBeforeFieldValidationTests(SimpleTestCase):
    """
    The check has to run before Django validates the file field.

    _clean_fields calls field.clean() -- which for Wagtail's image field opens
    the file -- and only then the clean_<name> hook. A validator that lives
    only in clean_file is correct and useless: the decode that exhausts the
    dyno has already happened by the time it runs.
    """

    def _bind(self, upload):
        """
        A FoundationImageForm without BaseImageForm.__init__, which wants a
        collection and a database.

        Mirrors what BaseForm.__init__ assigns, because full_clean and
        add_error reach for several of these -- add_error builds a BoundField
        to read its auto_id, which needs _bound_fields_cache and auto_id.
        """
        form = FoundationImageForm.__new__(FoundationImageForm)
        form.is_bound = True
        form.data = {}
        form.files = {"file": upload}
        form.auto_id = "id_%s"
        form.prefix = None
        form.initial = {}
        form.error_class = ErrorList
        form.label_suffix = ":"
        form.empty_permitted = False
        form._errors = None
        form.fields = {"file": FileField()}
        form.renderer = get_default_renderer()
        form._bound_fields_cache = {}
        return form

    def test_finds_the_upload_the_way_django_does(self):
        upload = _gif_upload(width=8, height=8, frames=2)
        self.assertIs(self._bind(upload)._uploaded_file(), upload)

    def test_oversized_gif_never_reaches_field_validation(self):
        """
        The regression: reaching super().full_clean() at all means the file
        gets handed to Wagtail's image field and opened.
        """
        form = self._bind(_gif_upload(width=950, height=950, frames=109))

        with mock.patch.object(BaseImageForm, "full_clean", create=True) as parent:
            form.full_clean()

        parent.assert_not_called()
        self.assertEqual(form.errors.as_data()["file"][0].code, "gif_frame_volume_too_large")
        self.assertEqual(form.cleaned_data, {})

    def test_acceptable_gif_falls_through_to_normal_validation(self):
        """
        The screen must not swallow ordinary uploads -- every image of every
        type passes through full_clean, not just GIFs.
        """
        form = self._bind(_gif_upload(width=220, height=154, frames=21))

        with mock.patch.object(BaseImageForm, "full_clean", create=True) as parent:
            form.full_clean()

        parent.assert_called_once()
        self.assertIsNone(form._errors)

    def test_non_gif_falls_through_to_normal_validation(self):
        upload = SimpleUploadedFile("photo.jpg", b"not a gif", content_type="image/jpeg")
        form = self._bind(upload)

        with mock.patch.object(BaseImageForm, "full_clean", create=True) as parent:
            form.full_clean()

        parent.assert_called_once()


class NormaliseExtensionTests(SimpleTestCase):
    """
    S3 notification suffix filters are case-sensitive while this app lowercases
    before comparing, so a `.GIF` reads as a GIF here but never triggers the
    conversion Lambda.
    """

    def test_lowercases_a_shouty_extension(self):
        upload = SimpleUploadedFile("Party.GIF", b"x", content_type="image/gif")

        normalise_extension(upload)

        self.assertEqual(upload.name, "Party.gif")

    def test_leaves_the_stem_alone(self):
        """Only the extension is matched against; the rest is the editor's."""
        upload = SimpleUploadedFile("MoFo Party 2026.GIF", b"x")

        normalise_extension(upload)

        self.assertEqual(upload.name, "MoFo Party 2026.gif")

    def test_leaves_a_lowercase_name_untouched(self):
        upload = SimpleUploadedFile("party.gif", b"x")

        normalise_extension(upload)

        self.assertEqual(upload.name, "party.gif")

    def test_tolerates_a_name_with_no_extension(self):
        upload = SimpleUploadedFile("party", b"x")

        normalise_extension(upload)

        self.assertEqual(upload.name, "party")

    def test_tolerates_none(self):
        self.assertIsNone(normalise_extension(None))


@override_settings(GIF_MAX_UPLOAD_SIZE=5 * ONE_MB, GIF_MAX_FRAME_VOLUME=10 * ONE_MB)
class FormNormalisesExtensionTests(SimpleTestCase):
    """
    The rename has to happen before the field stores the file, which is the
    only point at which the storage key -- and so the S3 event -- is decided.
    """

    def _bind(self, upload):
        # Same shortcut as ScreensBeforeFieldValidationTests: BaseImageForm's
        # __init__ wants a collection and a database, and neither matters here.
        form = FoundationImageForm.__new__(FoundationImageForm)
        form.is_bound = True
        form.data = {}
        form.files = {"file": upload}
        form.auto_id = "id_%s"
        form.prefix = None
        form.initial = {}
        form.error_class = ErrorList
        form.label_suffix = ":"
        form.empty_permitted = False
        form._errors = None
        form.fields = {"file": FileField()}
        form.renderer = get_default_renderer()
        form._bound_fields_cache = {}
        return form

    def test_uppercase_upload_is_normalised_before_field_validation(self):
        upload = _gif_upload("Party.GIF", width=8, height=8, frames=2)
        form = self._bind(upload)

        with mock.patch.object(BaseImageForm, "full_clean", create=True):
            form.full_clean()

        self.assertEqual(upload.name, "Party.gif")
