from django.db import models


class ExtendedYesNoField(models.CharField):
    # This has been replaced with networkapi.wagtailpages.fields.ExtendedYesNoField
    # TODO: Remove this class when migrations are squashed next.
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
