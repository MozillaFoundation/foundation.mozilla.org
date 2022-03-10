from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import TranslatableMixin
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from wagtail_localize.fields import TranslatableField, SynchronizedField


@register_snippet
class Profile(TranslatableMixin, models.Model):
    name = models.CharField(max_length=70, blank=False)

    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    tagline = models.CharField(
        max_length=50,
        blank=True,
        help_text="Use this field for things like a person's job title."
    )

    introduction = models.TextField(max_length=500, blank=True)

    panels = [
        FieldPanel("name"),
        ImageChooserPanel("image"),
        FieldPanel("tagline"),
        FieldPanel("introduction"),
    ]

    translatable_fields = [
        SynchronizedField('name'),
        SynchronizedField('image'),
        TranslatableField('tagline'),
        TranslatableField('introduction'),
    ]

    def __str__(self):
        return self.name
