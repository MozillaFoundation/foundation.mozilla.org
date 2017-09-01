from django.db import models


# Create your models here.
class Homepage(models.Model):
    # All the fields are created as Foreign Keys in the related models so
    # that we have a 1:Many relationship between the homepage and related model
    # i.e., one (the only) Homepage model has many instances of the related
    # model(s).
    pass
