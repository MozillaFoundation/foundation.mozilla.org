from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.models import TranslatableMixin
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField, TranslatableField


@register_snippet
class Profile(index.Indexed, TranslatableMixin, models.Model):
    name = models.CharField(max_length=70, blank=False)

    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    tagline = models.CharField(
        max_length=50,
        blank=True,
        help_text="Use this field for things like a person's job title.",
    )

    introduction = models.TextField(max_length=500, blank=True)

    # The slug field is set during save and should not be managed manually.
    slug = models.SlugField(blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("image"),
        FieldPanel("tagline"),
        FieldPanel("introduction"),
    ]

    translatable_fields = [
        SynchronizedField("name"),
        SynchronizedField("image"),
        TranslatableField("tagline"),
        TranslatableField("introduction"),
    ]

    search_fields = [
        index.AutocompleteField("name"),
        # Needed for locale filtering in the Wagtail admin. A helpful error message pointed this out.
        index.FilterField("locale_id"),
    ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Profile, self).save(*args, **kwargs)
        self._meta.model.objects.filter(id=self.id).update(slug=Concat(F("slug"), Value("-"), F("id")))

    class Meta(TranslatableMixin.Meta):
        ordering = ["name"]
