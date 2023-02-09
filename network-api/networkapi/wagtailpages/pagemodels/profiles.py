from django.db import models
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.models import TranslatableMixin
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField, TranslatableField


class ProfileQuerySet(models.QuerySet):
    def filter_research_authors(self):
        return self.filter(authored_research__isnull=False).distinct()

    def filter_blog_authors(self):
        return self.filter(blogauthors__isnull=False).distinct()


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
        index.SearchField("name", partial_match=True),
        # Needed for locale filtering in the Wagtail admin. A helpful error message pointed this out.
        index.FilterField("locale_id"),
    ]

    objects = ProfileQuerySet.as_manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}-{str(self.id)}")
        super(Profile, self).save(*args, **kwargs)

    class Meta(TranslatableMixin.Meta):
        ordering = ["name"]
