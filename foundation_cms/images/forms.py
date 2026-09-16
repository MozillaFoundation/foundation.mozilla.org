import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorDict
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _
from wagtail.images.forms import BaseImageForm

from . import gif

logger = logging.getLogger(__name__)


def validate_gif_upload_size(file):
    """
    Reject GIFs larger than GIF_MAX_UPLOAD_SIZE.

    A no-op for non-GIFs, for files with no name or size, and when the limit is
    unset or zero.
    """
    max_size = getattr(settings, "GIF_MAX_UPLOAD_SIZE", 0)
    if not max_size or file is None:
        return file

    name = getattr(file, "name", "") or ""
    size = getattr(file, "size", None)

    if not name.lower().endswith(".gif") or size is None or size <= max_size:
        return file

    raise ValidationError(
        _(
            "This animated GIF is %(size)s, which is over the %(limit)s limit for GIFs. "
            "Large GIFs take too long to convert and can take the site down. "
            "Please reduce its dimensions, frame count, or colour depth and try again."
        )
        % {
            "size": filesizeformat(size),
            "limit": filesizeformat(max_size),
        },
        code="gif_too_large",
    )


def validate_gif_frame_volume(file):
    """
    Reject GIFs whose decoded frame data would not fit in a web dyno.

    Lenient about files it cannot parse: Wagtail's own format validation
    rejects those, with a better message than this check could produce.
    """
    max_volume = getattr(settings, "GIF_MAX_FRAME_VOLUME", 0)
    if not max_volume or file is None:
        return file

    name = getattr(file, "name", "") or ""
    if not name.lower().endswith(".gif"):
        return file

    try:
        file.seek(0)
        info = gif.probe(file)
    except (gif.GifParseError, OSError) as e:
        logger.warning(f"Could not read GIF structure of {name}: {e}")
        return file
    finally:
        # Everything downstream -- Wagtail's validation, the upload to storage
        try:
            file.seek(0)
        except Exception:
            pass

    if info.decoded_size <= max_volume:
        return file

    raise ValidationError(
        _(
            "This animated GIF is %(width)sx%(height)s with %(frames)s frames, which needs "
            "about %(decoded)s of memory to process, which is over the %(limit)s limit. Its file "
            "size is not the problem; the frame count and dimensions are. Please reduce "
            "either one and try again."
        )
        % {
            "width": info.width,
            "height": info.height,
            "frames": info.frames,
            "decoded": filesizeformat(info.decoded_size),
            "limit": filesizeformat(max_volume),
        },
        code="gif_frame_volume_too_large",
    )


class FoundationImageForm(BaseImageForm):
    """
    Wagtail's image form plus GIF-specific upload limits.

    Wired up via the WAGTAILIMAGES_IMAGE_FORM_BASE setting.
    """

    def _uploaded_file(self):
        """The raw upload, fetched exactly the way Django's own field does."""
        field = self.fields.get("file")
        if field is None or not self.is_bound:
            return None
        name = self.add_prefix("file")
        return field.widget.value_from_datadict(self.data, self.files, name)

    def full_clean(self):
        """
        Screen the upload before Django validates any field.

        Django's _clean_fields calls field.clean() first and the clean_<name>
        hook several lines later. Wagtail's image field opens the file inside
        clean(), so a GIF heavy enough to exhaust the dyno does so before any
        hook of ours runs -- checking in clean_file alone is too late to
        prevent anything.

        Bailing out here means the file is never handed to the image field.
        """
        upload = self._uploaded_file()
        if upload is not None:
            try:
                validate_gif_upload_size(upload)
                validate_gif_frame_volume(upload)
            except ValidationError as error:
                self._errors = ErrorDict(renderer=self.renderer)
                self.cleaned_data = {}
                self.add_error("file", error)
                return

        super().full_clean()

    def clean_file(self):
        # Belt and braces. full_clean above is what protects the dyno, but it
        # can only see uploads that arrive through self.files; this covers a
        # form driven programmatically. Both validators are idempotent and
        # rewind the file, so running them twice is safe.
        file = validate_gif_upload_size(self.cleaned_data.get("file"))
        return validate_gif_frame_volume(file)
