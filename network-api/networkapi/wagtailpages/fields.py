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
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('U', 'Unknown'),
    ]

    default_choice = 'U'

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = self.choice_list
        kwargs['default'] = self.default_choice
        kwargs['max_length'] = 3
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['choices']
        del kwargs['default']
        del kwargs['max_length']
        return name, path, args, kwargs


class ExtendedYesNoField(models.CharField):
    description = "Yes, No, Not Applicable, or Can’t Determine"

    choice_list = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('NA', 'Not Applicable'),
        ('CD', 'Can’t Determine'),
    ]

    default_choice = 'CD'

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = self.choice_list
        kwargs['default'] = self.default_choice
        kwargs['max_length'] = 3
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['choices']
        del kwargs['default']
        del kwargs['max_length']
        return name, path, args, kwargs
