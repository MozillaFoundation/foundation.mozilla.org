from django.db import models


class ExtendedYesNoField(models.CharField):
    description = "Yes, No, Not Applicable, or Unknown"

    choice_list = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('NA', 'Not Applicable'),
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
