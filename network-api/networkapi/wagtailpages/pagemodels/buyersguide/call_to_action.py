from wagtail.snippets.models import register_snippet
from django.db import models
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, MultiFieldPanel
from wagtail.core.models import Page, TranslatableMixin
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail_localize.fields import SynchronizedField, TranslatableField
from wagtail.search import index
from networkapi.wagtailpages.pagemodels.mixin.snippets import LocalizedSnippet
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from networkapi.wagtailpages.pagemodels.customblocks.base_rich_text_options import base_rich_text_options


@register_snippet
class BuyersGuideCallToAction(
    index.Indexed,
    TranslatableMixin,
    LocalizedSnippet,
    models.Model
):
    """
    Reusable call to action for the buyers guide,
    features a title and rich text body, with optional image and link.
    """
    sticker_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Sticker Image',
        help_text='Optional image on CTA.',
    )
    title = models.CharField(max_length=200)
    content = RichTextField(features=base_rich_text_options, blank=True)
    link_label = models.CharField(max_length=2048, blank=True)
    link_target_url = models.URLField(blank=True)
    link_target_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='cta_link_page'
    )

    panels = [
        ImageChooserPanel("sticker_image"),
        FieldPanel('title'),
        FieldPanel('content'),
        MultiFieldPanel([
            FieldPanel('link_label'),
            FieldPanel('link_target_url'),
            PageChooserPanel('link_target_page'),
        ], heading='Call To Action Link'),
    ]

    translatable_fields = [
        SynchronizedField('sticker_image'),
        TranslatableField('title'),
        TranslatableField('content'),
        TranslatableField('link_label'),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Buyers Guide Call To Action"
        verbose_name_plural = "Buyers Guide Call To Actions"

    def __str__(self):
        return str(self.title)

    def get_target_url(self):
        if self.link_target_url:
            return self.link_target_url
        else:
            return self.link_target_page.url

    def clean(self):
        errors = {}
        duplicate_link_target_error = ErrorList(['Please select a page OR enter a URL for the link (choose one)'])
        # If user enters both link URL and link page:
        if self.link_label and self.link_target_url and self.link_target_page:
            errors['link_target_url'] = duplicate_link_target_error
            errors['link_target_page'] = duplicate_link_target_error
        # If user enters link URL or page but no label:
        elif not self.link_label and self.link_target_page or self.link_target_url:
            errors['link_label'] = ErrorList(['Please enter a label for the link'])
        # If user enters link label but no page or URL to link to:
        elif not self.link_target_page and not self.link_target_url and self.link_label:
            errors['link_target_url'] = duplicate_link_target_error
            errors['link_target_page'] = duplicate_link_target_error

        if errors:
            raise ValidationError(errors)
