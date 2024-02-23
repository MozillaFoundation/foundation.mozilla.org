from django.core import validators

from wagtail.blocks import CharBlock


class MailToValidator(validators.EmailValidator):
    def __call__(self, value):
        if value.startswith("mailto:"):
            value = value[7:]
        super().__call__(value)


class RelativeURLValidator(validators.URLValidator):
    def __call__(self, value):
        if value.startswith("/"):
            value = "http://example.com" + value
        super().__call__(value)


mailto_validator = MailToValidator()
relative_url_validator = RelativeURLValidator()
url_validator = validators.URLValidator()


def extended_url_validator(value, message=validators.URLValidator.message):
    # Try a mailto URL first
    try:
        mailto_validator(value)
        return
    except validators.ValidationError:
        pass

    # If that fails, try a relative URL
    try:
        relative_url_validator(value)
        return
    except validators.ValidationError:
        pass

    # Finally, let's try a regular URL
    try:
        url_validator(value)
        return
    except validators.ValidationError:
        pass

    # If it was neither of those, raise a validation error
    raise validators.ValidationError(
        message,
        params={"value": value},
        code="invalid",
    )


class ExtendedURLBlock(CharBlock):
    def __init__(self, required=True, help_text=None, **kwargs):
        super().__init__(
            required=required,
            help_text=help_text,
            validators=[extended_url_validator],
            **kwargs,
        )
