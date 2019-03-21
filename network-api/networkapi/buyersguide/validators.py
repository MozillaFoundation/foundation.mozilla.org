from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValueListValidator:
    def __init__(self, valid_values=None):
        self.valid_values = valid_values

    def __call__(self, value):
        if value not in self.valid_values:
            raise ValidationError(f'{value} is not a permitted attribute')

    def __eq__(self, other):
        return self.valid_values == other.valid_values
