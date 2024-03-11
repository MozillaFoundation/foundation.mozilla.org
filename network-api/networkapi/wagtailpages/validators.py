from django.core import validators
from django.core.exceptions import ValidationError


class RelativeURLValidator(validators.URLValidator):
    def __call__(self, value):
        if not value:
            raise ValidationError("This field cannot be empty.")

        if not value.startswith("/"):
            raise ValidationError('This field must start with "/"')

        value = "http://example.com" + value
        super().__call__(value)


class AnchorLinkValidator(validators.URLValidator):
    def __call__(self, value):
        if not value:
            raise ValidationError("This field cannot be empty.")

        if not value.startswith("#"):
            raise ValidationError('This field must start with "#"')

        value = "http://example.com" + value
        super().__call__(value)
