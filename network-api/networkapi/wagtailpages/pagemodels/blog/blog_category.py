from django.db import models
from django.template.defaultfilters import slugify
from wagtail.core.fields import RichTextField
from wagtail.snippets.models import register_snippet


@register_snippet
class BlogPageCategory(models.Model):
    name = models.CharField(
        max_length=50
    )

    intro = RichTextField(
        features=[
            'bold', 'italic', 'link',
        ],
        blank=True,
    )

    @property
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Page Category"
        verbose_name_plural = "Blog Page Categories"
