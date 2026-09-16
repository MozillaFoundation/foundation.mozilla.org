import logging

from django.conf import settings
from django.core.exceptions import ValidationError
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

    def clean_file(self):
        # Django has already run the field's own validation and stashed the
        # result in cleaned_data by the time this hook is called
        file = validate_gif_upload_size(self.cleaned_data.get("file"))
        return validate_gif_frame_volume(file)
