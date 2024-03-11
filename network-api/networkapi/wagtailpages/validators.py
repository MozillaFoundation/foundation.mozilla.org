from urllib.parse import urlparse

from django.core import validators
from django.core.exceptions import ValidationError


class RelativeURLValidator(validators.URLValidator):
    def __call__(self, value):
        if not value:
            raise ValidationError("This field cannot be empty.")

        # No anchor links
        if value.startswith("#"):
            raise ValidationError("This field must be a relative URL.")

        parsed_url = urlparse(value)
        if parsed_url.scheme or parsed_url.netloc:
            raise ValidationError("This field must be a relative URL.")

        value = "http://example.com/" + value
        super().__call__(value)
