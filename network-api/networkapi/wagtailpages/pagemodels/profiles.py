from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import TranslatableMixin
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Profile(TranslatableMixin, models.Model):
    name = models.CharField(max_length=70, blank=False)

    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    panels = [
        FieldPanel("name"),
        ImageChooserPanel("image"),
    ]

    def __str__(self):
        return self.name
