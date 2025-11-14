import json

from wagtail.fields import StreamField as WagtailStreamfield

from django.db import models


class ExtendedBoolean(models.CharField):
    """
    TODO: unify this with the ExtendedYesNoField below. Because this would
          introduce a superclass hierarchy change, and Django is notoriously
          bad at those, this is a separate task.

          See https://github.com/mozilla/foundation.mozilla.org/issues/6929
    """

    description = "Yes, No, Unknown"

    choice_list = [
        ("Yes", "Yes"),
        ("No", "No"),
        ("U", "Unknown"),
    ]

    default_choice = "U"

    def __init__(self, *args, **kwargs):
        kwargs["choices"] = self.choice_list
        kwargs["default"] = self.default_choice
        kwargs["max_length"] = 3
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["choices"]
        del kwargs["default"]
        del kwargs["max_length"]
        return name, path, args, kwargs


class ExtendedYesNoField(models.CharField):
    description = "Yes, No, Not Applicable, or Can’t Determine"

    choice_list = [
        ("Yes", "Yes"),
        ("No", "No"),
        ("NA", "Not Applicable"),
        ("CD", "Can’t Determine"),
    ]

    default_choice = "CD"

    def __init__(self, *args, **kwargs):
        kwargs["choices"] = self.choice_list
        kwargs["default"] = self.default_choice
        kwargs["max_length"] = 3
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["choices"]
        del kwargs["default"]
        del kwargs["max_length"]
        return name, path, args, kwargs

# Source: https://gist.github.com/zerolab/cbd19becd21a5ab12a711674d5979157
# In order to cut down on massive streamfield migrations pre-wagtail 6.2
# that are causing memory issues spinning up review apps.
class StreamField(WagtailStreamfield):
    def __init__(self, *args, **kwargs):
        """
        Overrides StreamField.__init__() to account for `block_types` no longer
        being received as an arg when migrating (because there is no longer a
        `block_types` value in the migration to provide).
        Usage: 
        import this StreamField instead of `from wagtail.fields import StreamField` for usage in your models
        """
        if args:
            block_types = args[0] or []
            args = args[1:]
        else:
            block_types = kwargs.pop("block_types", [])
        super().__init__(block_types, *args, **kwargs)

    def deconstruct(self):
        """
        Overrides StreamField.deconstruct() to remove `block_types` and
        `verbose_name` values so that migrations remain smaller in size,
        and changes to those attributes do not require a new migration.
        """
        name, path, args, kwargs = super().deconstruct()
        if args:
            args = args[1:]
        else:
            kwargs.pop("block_types", None)
        kwargs.pop("verbose_name", None)
        return name, path, args, kwargs

    def to_python(self, value):
        """
        Overrides StreamField.to_python() to make the return value
        (a `StreamValue`) more useful when migrating. When migrating, block
        definitions are unavailable to the field's underlying StreamBlock,
        causing self.stream_block.to_python() to not recognise any of the
        blocks in the stored value.
        """
        stream_value = super().to_python(value)

        # There is no way to be absolutely sure this is a migration,
        # but the combination of factors below is a pretty decent indicator
        if not self.stream_block.child_blocks and value and not stream_value._raw_data:
            stream_data = None
            if isinstance(value, list):
                stream_data = value
            elif isinstance(value, str):
                try:
                    stream_data = json.loads(value)
                except ValueError:
                    stream_value.raw_text = value

            if stream_data:
                return type(stream_value)(self, stream_data, is_lazy=True)

        return stream_value