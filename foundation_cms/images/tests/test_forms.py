from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, override_settings

from foundation_cms.images.forms import validate_gif_upload_size

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
