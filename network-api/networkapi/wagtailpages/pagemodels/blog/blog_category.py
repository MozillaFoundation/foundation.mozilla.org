from django.db import models
from django.template.defaultfilters import slugify
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel
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
    share_description = models.TextField(
        blank=True,
        help_text='Optional description that will apear when category page is shared. '
                  'If not set, will default to "intro" text.'
    )
    share_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Share Image',
        help_text='Optional image that will apear when category page is shared.',
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("intro"),
        FieldPanel("share_description"),
        ImageChooserPanel("share_image"),
    ]

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
