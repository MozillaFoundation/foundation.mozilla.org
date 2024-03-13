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

        if not value.startswith("/"):
            raise ValidationError('Relative URLs must start with "/"')

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
