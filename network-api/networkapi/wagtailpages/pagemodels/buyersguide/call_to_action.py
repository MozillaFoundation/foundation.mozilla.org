from wagtail.snippets.models import register_snippet
from django.db import models
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.models import Page, TranslatableMixin
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail_localize.fields import SynchronizedField, TranslatableField
from wagtail.search import index
from networkapi.wagtailpages.pagemodels.mixin.snippets import LocalizedSnippet


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
    content = RichTextField()
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
        FieldPanel('link_label'),
        FieldPanel('link_target_url'),
        PageChooserPanel('link_target_page'),
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
