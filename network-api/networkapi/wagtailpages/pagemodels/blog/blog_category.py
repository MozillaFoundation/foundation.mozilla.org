from django.db import models
from django.template.defaultfilters import slugify
from wagtail.core.fields import RichTextField
from wagtail.core.models import TranslatableMixin
from wagtail.snippets.models import register_snippet


@register_snippet
class BlogPageCategory(TranslatableMixin, models.Model):
    name = models.CharField(
        max_length=50
    )

    intro = RichTextField(
        features=[
            'bold', 'italic', 'link',
        ],
        blank=True,
    )

    def get_categories():
        """
        WARNING: this function is referenced by two migrations:

        - mozfest/0014_auto_20200406_2109.py
        - wagtailpages/0095_auto_20200406_2109.py

        This means that renaming/(re)moving this function will require
        back-updating those two migrations, as "from scratch" migrations
        (compared to update-only migrations) will throw errors when trying
        to apply this function from its original location.
        """
        choices = [(cat.name, cat.name) for cat in BlogPageCategory.objects.all()]
        choices.sort(key=lambda c: c[1])
        choices.insert(0, ('All', 'All'))
        return choices

    @property
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Blog Page Category"
        verbose_name_plural = "Blog Page Categories"
