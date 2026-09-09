from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _
from wagtail.images.forms import BaseImageForm


def validate_gif_upload_size(file):
    """
    Reject GIFs larger than GIF_MAX_UPLOAD_SIZE.

    Wagtail already enforces WAGTAILIMAGES_MAX_UPLOAD_SIZE across every image
    type. GIFs need a stricter ceiling of their own: they are converted to
    animated WebP with ffmpeg, and a GIF costs far more memory and CPU to
    process than a still image of the same byte size.

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


class FoundationImageForm(BaseImageForm):
    """
    Wagtail's image form plus a GIF-specific upload size limit.

    Wired up via the WAGTAILIMAGES_IMAGE_FORM_BASE setting.
    """

    def clean_file(self):
        return validate_gif_upload_size(super().clean_file())
