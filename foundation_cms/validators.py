import re
from urllib.parse import urlparse

from django.core import validators
from django.core.exceptions import ValidationError


class RelativeURLValidator(validators.URLValidator):
    def __call__(self, value):
        if not value:
            raise ValidationError("This field cannot be empty.")

        parsed_url = urlparse(value)
        if parsed_url.scheme or parsed_url.netloc:
            raise ValidationError('Please use "external URL" for absolute urls.')

        if not (value.startswith("/") or value.startswith("?")):
            raise ValidationError('Relative URLs must start with "/" or "?"')

        value = "http://example.com" + value
        super().__call__(value)


class AnchorLinkValidator(validators.URLValidator):
    def __call__(self, value):
        if not value:
            raise ValidationError("This field cannot be empty.")

        parsed_url = urlparse(value)
        if parsed_url.scheme or parsed_url.netloc:
            raise ValidationError('Please use "external URL" for absolute urls.')

        if not value.startswith("#"):
            raise ValidationError('This field must start with "#"')

        value = "http://example.com" + value
        super().__call__(value)


VIMEO_HELP_TEXT = (
    "Please enter a valid Vimeo URL (e.g. https://vimeo.com/123456789 or " "https://player.vimeo.com/video/123456789)."
)


def validate_vimeo_url(url):
    pattern = r"^https?://(www\.)?(vimeo\.com|player\.vimeo\.com/video)/\d+"
    if not re.match(pattern, url):
        raise ValidationError(VIMEO_HELP_TEXT)


VIMEO_MP4_URL_HELP_TEXT = (
    "Please enter a valid Vimeo mp4 URL (e.g. "
    "https://player.vimeo.com/progressive_redirect/playback/123456789/"
    "rendition/1080p/file.mp4...)."
)


def validate_vimeo_mp4_url(url):
    pattern = r"^https?://player\.vimeo\.com/progressive_redirect/playback/\d+/rendition/\d+p/file\.mp4"
    if not re.match(pattern, url):
        raise ValidationError(VIMEO_MP4_URL_HELP_TEXT)
