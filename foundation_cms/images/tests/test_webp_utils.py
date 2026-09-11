import subprocess
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase, override_settings

from foundation_cms.images.webp import utils as webp_utils


class RunFfmpegTests(SimpleTestCase):
    """
    _run_ffmpeg must never raise and never hang. Every failure mode is logged
    and reported as False so callers can fall back to the unconverted source.
    """

    @override_settings(GIF_CONVERSION_TIMEOUT=7)
    @patch("foundation_cms.images.webp.utils.subprocess.run")
    def test_passes_timeout_to_subprocess(self, mock_run):
        webp_utils._run_ffmpeg(["ffmpeg", "-y"], "test")

        self.assertEqual(mock_run.call_args.kwargs["timeout"], 7)
        self.assertTrue(mock_run.call_args.kwargs["check"])

    @patch("foundation_cms.images.webp.utils.subprocess.run")
    def test_returns_true_on_success(self, mock_run):
        self.assertIs(webp_utils._run_ffmpeg(["ffmpeg"], "test"), True)

    @override_settings(GIF_CONVERSION_TIMEOUT=3)
    @patch("foundation_cms.images.webp.utils.subprocess.run")
    def test_timeout_is_caught_and_logged(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="ffmpeg", timeout=3)

        with self.assertLogs("foundation_cms.images.webp.utils", level="WARNING") as logs:
            result = webp_utils._run_ffmpeg(["ffmpeg"], "test conversion")

        self.assertIs(result, False)
        self.assertIn("timed out after 3s", logs.output[0])

    @patch("foundation_cms.images.webp.utils.subprocess.run")
    def test_called_process_error_is_caught(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "ffmpeg", stderr=b"boom")

        with self.assertLogs("foundation_cms.images.webp.utils", level="WARNING") as logs:
            result = webp_utils._run_ffmpeg(["ffmpeg"], "test conversion")

        self.assertIs(result, False)
        self.assertIn("boom", logs.output[0])

    @patch("foundation_cms.images.webp.utils.subprocess.run")
    def test_called_process_error_with_no_stderr(self, mock_run):
        """e.stderr is None when stderr was not captured -- must not blow up."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "ffmpeg", stderr=None)

        with self.assertLogs("foundation_cms.images.webp.utils", level="WARNING"):
            self.assertIs(webp_utils._run_ffmpeg(["ffmpeg"], "test"), False)

    @patch("foundation_cms.images.webp.utils.subprocess.run")
    def test_missing_ffmpeg_binary_is_caught(self, mock_run):
        mock_run.side_effect = FileNotFoundError()

        with self.assertLogs("foundation_cms.images.webp.utils", level="WARNING") as logs:
            result = webp_utils._run_ffmpeg(["ffmpeg"], "test")

        self.assertIs(result, False)
        self.assertIn("not installed", logs.output[0])


def _source_file(payload=b"GIF89a-not-really"):
    """Minimal stand-in for a Django FieldFile opened as a context manager."""
    handle = MagicMock()
    handle.read.return_value = payload
    handle.__enter__ = MagicMock(return_value=handle)
    handle.__exit__ = MagicMock(return_value=False)

    source = MagicMock()
    source.open.return_value = handle
    return source


class GenerateWebpRenditionTests(SimpleTestCase):
    """
    The read path is the half of the ffmpeg work that survives the move to
    asynchronous conversion, so it carries the timeout and the None contract.
    """

    @patch("foundation_cms.images.webp.utils._run_ffmpeg", return_value=False)
    def test_returns_none_when_ffmpeg_fails(self, mock_run):
        """
        Callers fall back to an unconverted rendition on None. Previously this
        fell off the end of an except block -- the same value by accident
        rather than by contract.
        """
        image = MagicMock(pk=1)

        result = webp_utils.generate_webp_rendition(image, _source_file(), "fill-800x450-webp", 800, 450)

        self.assertIsNone(result)

    @patch("foundation_cms.images.webp.utils._run_ffmpeg", return_value=True)
    def test_passes_a_description_naming_the_spec(self, mock_run):
        """Log lines have to identify which rendition failed."""
        image = MagicMock(pk=1)

        with patch("builtins.open", side_effect=OSError):
            try:
                webp_utils.generate_webp_rendition(image, _source_file(), "fill-800x450-webp", 800, 450)
            except OSError:
                pass

        self.assertIn("fill-800x450-webp", mock_run.call_args.args[1])

    def test_open_failure_does_not_raise_nameerror(self):
        """
        Regression: the finally block referenced `temp_in`, which is unbound if
        source_file.open() raises -- masking the real error with a NameError.
        """
        image = MagicMock(pk=1)
        source = MagicMock()
        source.open.side_effect = OSError("S3 unavailable")

        with self.assertRaises(OSError):
            webp_utils.generate_webp_rendition(image, source, "fill-800x450-webp", 800, 450)


class DeriveWebpNameTests(SimpleTestCase):
    """
    Half of a contract with the conversion Lambda: both sides derive the same
    key from the source name, independently. Changing this breaks the pairing.
    """

    def test_swaps_extension_and_reparents(self):
        self.assertEqual(
            webp_utils.derive_webp_name("original_images/rotating_earth.gif"),
            "images/converted_webp/rotating_earth.webp",
        )

    def test_uses_basename_only(self):
        """Source lives under original_images/; output must not inherit that."""
        self.assertEqual(
            webp_utils.derive_webp_name("original_images/nested/deep/a.gif"),
            "images/converted_webp/a.webp",
        )

    def test_handles_storage_collision_suffix(self):
        """AWS_S3_FILE_OVERWRITE=False makes django-storages append a suffix."""
        self.assertEqual(
            webp_utils.derive_webp_name("original_images/loop_aB3xK9.gif"),
            "images/converted_webp/loop_aB3xK9.webp",
        )

    def test_preserves_dots_in_stem(self):
        self.assertEqual(
            webp_utils.derive_webp_name("original_images/v1.2.final.gif"),
            "images/converted_webp/v1.2.final.webp",
        )

    def test_uppercase_extension(self):
        self.assertEqual(
            webp_utils.derive_webp_name("original_images/SHOUTY.GIF"),
            "images/converted_webp/SHOUTY.webp",
        )


class ConvertedWebpExistsTests(SimpleTestCase):
    def setUp(self):
        from django.core.cache import cache

        cache.clear()
        self.addCleanup(cache.clear)

    @patch("foundation_cms.images.webp.utils.default_storage.exists", return_value=True)
    def test_true_when_present(self, mock_exists):
        self.assertIs(webp_utils.converted_webp_exists("images/converted_webp/a.webp"), True)

    @patch("foundation_cms.images.webp.utils.default_storage.exists", return_value=False)
    def test_false_when_absent(self, mock_exists):
        self.assertIs(webp_utils.converted_webp_exists("images/converted_webp/a.webp"), False)

    @patch("foundation_cms.images.webp.utils.default_storage.exists", return_value=True)
    def test_result_is_cached(self, mock_exists):
        webp_utils.converted_webp_exists("images/converted_webp/a.webp")
        webp_utils.converted_webp_exists("images/converted_webp/a.webp")

        self.assertEqual(mock_exists.call_count, 1)

    @patch("foundation_cms.images.webp.utils.default_storage.exists", return_value=False)
    def test_negative_result_is_cached_too(self, mock_exists):
        """A page of unconverted GIFs must not issue an S3 HEAD per render."""
        webp_utils.converted_webp_exists("images/converted_webp/a.webp")
        webp_utils.converted_webp_exists("images/converted_webp/a.webp")

        self.assertEqual(mock_exists.call_count, 1)

    @patch("foundation_cms.images.webp.utils.default_storage.exists", side_effect=OSError("S3 down"))
    def test_storage_failure_reads_as_not_ready(self, mock_exists):
        """Never raise into a template render; fall back to the GIF instead."""
        with self.assertLogs("foundation_cms.images.webp.utils", level="WARNING"):
            result = webp_utils.converted_webp_exists("images/converted_webp/a.webp")

        self.assertIs(result, False)

    @patch("foundation_cms.images.webp.utils.default_storage.exists", side_effect=OSError("S3 down"))
    def test_storage_failure_is_not_cached(self, mock_exists):
        """A transient outage must not pin 'missing' for the full miss TTL."""
        with self.assertLogs("foundation_cms.images.webp.utils", level="WARNING"):
            webp_utils.converted_webp_exists("images/converted_webp/a.webp")
            webp_utils.converted_webp_exists("images/converted_webp/a.webp")

        self.assertEqual(mock_exists.call_count, 2)
