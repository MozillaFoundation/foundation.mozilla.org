from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import TranslatableMixin
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from django.utils.text import slugify


class ProfileQuerySet(models.QuerySet):
    def filter_research_authors(self):
        return self.filter(authored_research__isnull=False).distinct()

    def filter_blog_authors(self):
        return self.filter(blogauthors__isnull=False).distinct()


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
    slug = models.SlugField(blank=True)

    panels = [
        FieldPanel("name"),
        ImageChooserPanel("image"),
        FieldPanel("tagline"),
        FieldPanel("introduction"),
    ]

    objects = ProfileQuerySet.as_manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.name}-{str(self.id)}')
        super(Profile, self).save(*args, **kwargs)
