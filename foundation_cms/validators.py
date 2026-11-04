import re
from urllib.parse import urlparse, urlsplit, urlunsplit

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


VIMEO_VIDEO_OR_EVENT_HELP_TEXT = (
    "Please enter a valid Vimeo video or event URL (e.g. https://vimeo.com/123456789, "
    "https://player.vimeo.com/video/123456789, or https://vimeo.com/event/123456)."
)

# Group 2 is the privacy hash that "Copy Link" puts in the path of unlisted videos.
_VIMEO_VIDEO_URL_RE = re.compile(
    r"^https?://(?:www\.)?(?:vimeo\.com|player\.vimeo\.com/video)/(\d+)(?:/([0-9a-f]{10})(?=[/?#]|$))?"
)
_VIMEO_EVENT_URL_RE = re.compile(r"^https?://(?:www\.)?vimeo\.com/event/(\d+)")


def get_vimeo_embed_url(url):
    # Keep the query and fragment: they carry the ?h= privacy hash and playback options.
    parts = urlsplit(url)
    query = parts.query
    if match := _VIMEO_EVENT_URL_RE.match(url):
        host, path = "vimeo.com", f"/event/{match[1]}/embed"
    elif match := _VIMEO_VIDEO_URL_RE.match(url):
        host, path = "player.vimeo.com", f"/video/{match[1]}"
        if match[2]:
            query = f"h={match[2]}&{query}" if query else f"h={match[2]}"
    else:
        return ""
    return urlunsplit(("https", host, path, query, parts.fragment))


def validate_vimeo_video_or_event_url(url):
    if not get_vimeo_embed_url(url):
        raise ValidationError(VIMEO_VIDEO_OR_EVENT_HELP_TEXT)


VIMEO_MP4_URL_HELP_TEXT = (
    "Please enter a valid Vimeo mp4 URL (e.g. "
    "https://player.vimeo.com/progressive_redirect/playback/123456789/"
    "rendition/1080p/file.mp4...)."
)


def validate_vimeo_mp4_url(url):
    pattern = r"^https?://player\.vimeo\.com/progressive_redirect/playback/\d+/rendition/\d+p/file\.mp4"
    if not re.match(pattern, url):
        raise ValidationError(VIMEO_MP4_URL_HELP_TEXT)
