from django.db import models
from django.template.defaultfilters import slugify
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import TranslatableMixin
from wagtail.snippets.models import register_snippet

from networkapi.wagtailpages.pagemodels.customblocks.base_rich_text_options import base_rich_text_options


@register_snippet
class BlogPageTopic(TranslatableMixin, models.Model):
    name = models.CharField(
        max_length=50
    )

    title = models.TextField(
        blank=True,
        help_text='Optional title that will apear on the page and when topic page is shared. '
                  'If not set, will default to "name" text.'
    )

    intro = RichTextField(
        features=base_rich_text_options,
        blank=True,
    )
    share_description = models.TextField(
        blank=True,
        help_text='Optional description that will apear when topic page is shared. '
                  'If not set, will default to "intro" text.'
    )
    share_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Share Image',
        help_text='Optional image that will apear when topic page is shared.',
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("title"),
        FieldPanel("intro"),
        FieldPanel("share_description"),
        ImageChooserPanel("share_image"),
    ]

    @staticmethod
    def get_topics():
        """
        WARNING: this function is referenced by two migrations:

        - mozfest/0001_10_0015.py
        - wagtailpages/0001_initial.py

        This means that renaming/(re)moving this function will require
        back-updating those two migrations, as "from scratch" migrations
        (compared to update-only migrations) will throw errors when trying
        to apply this function from its original location.
        """
        return [
            ('All', 'All'),
            ('Advocacy', 'Advocacy'),
            ('Common Voice', 'Common Voice'),
            ('Fellowships & Awards', 'Fellowships & Awards'),
            ('Insights', 'Insights'),
            ('Moz News Beat', 'Moz News Beat'),
            ('Mozilla Explains', 'Mozilla Explains'),
            ('Mozilla Festival', 'Mozilla Festival'),
            ('Open Leadership & Events', 'Open Leadership & Events')
        ]

    @property
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Blog Page Topic"
        verbose_name_plural = "Blog Page Topics"
