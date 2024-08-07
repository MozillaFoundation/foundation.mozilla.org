import os
from datetime import datetime, timezone

from django.core.validators import FileExtensionValidator
from slugify import slugify


def get_image_upload_path(app_name, prop_name, instance, current_filename, suffix=""):
    timestamp = int((datetime.now(tz=timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds())

    filename = "{name}{suffix}_{timestamp}{ext}".format(
        name=slugify(getattr(instance, prop_name), max_length=300),
        suffix=suffix,
        timestamp=str(timestamp),
        ext=os.path.splitext(current_filename)[1],
    )

    return "images/{app_name}/{filename}".format(
        app_name=app_name,
        filename=filename,
    )


def SVGImageFormatValidator(value):
    validator = FileExtensionValidator(allowed_extensions=["svg"])
    return validator(value.file)
