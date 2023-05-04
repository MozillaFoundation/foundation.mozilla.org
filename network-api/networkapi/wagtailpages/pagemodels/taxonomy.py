from django.db import models
from wagtail.admin import FieldPanel


class BaseTaxonomy(models.Model):
    """
    Defines BaseTaxonomy which serves as an abstract base class
    for creating taxonomy models.

    Attributes:
        abstract (bool): A boolean attribute set to True indicating that the model is abstract.
        name (CharField): A required CharField that represents the name of the taxonomy.
        panels (list): A list of panel objects that can be used in the Wagtail admin interface for
            editing instances of this model.

    Methods:
        str(): Returns a string representation of the name of the taxonomy.

    Note:
        This model should be subclassed to create specific taxonomy models with additional fields.
    """

    abstract = True
    name = models.CharField(max_length=70, blank=False)

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name
