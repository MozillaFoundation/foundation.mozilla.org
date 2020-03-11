from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from .base_fields import base_fields
from .mixin.foundation_metadata import FoundationMetadataPageMixin
from ..utils import (
    set_main_site_nav_information,
    get_page_tree_information
)


class ModularPage(FoundationMetadataPageMixin, Page):
    """
    The base class offers universal component picking
    """

    header = models.CharField(
        max_length=250,
        blank=True
    )

    narrowed_page_content = models.BooleanField(
        default=False,
        help_text='For text-heavy pages, turn this on to reduce the overall width of the content on the page.'
    )

    zen_nav = models.BooleanField(
        default=True,
        help_text='For secondary nav pages, use this to collapse the primary nav under a toggle hamburger.'
    )

    body = StreamField(base_fields)

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
          [
            FieldPanel('narrowed_page_content'),
          ],
          classname="collapsible"
        ),
        MultiFieldPanel(
          [
            FieldPanel('zen_nav'),
          ],
          classname="collapsible"
        )
    ]

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        StreamFieldPanel('body'),
    ]

    show_in_menus_default = True

    def get_context(self, request):
        context = super().get_context(request)
        return set_main_site_nav_information(self, context, 'Homepage')


class MiniSiteNameSpace(ModularPage):
    subpage_types = [
        'BlogPage',
        'CampaignPage',
        'BanneredCampaignPage',
        'OpportunityPage',
        'YoutubeRegretsPage',
    ]

    """
    This is basically an abstract page type for setting up
    minisite namespaces such as "campaign", "opportunity", etc.
    """

    def get_context(self, request):
        """
        Extend the context so that mini-site pages know what kind of tree
        they live in, and what some of their local aspects are:
        """
        context = super().get_context(request)
        updated = get_page_tree_information(self, context)
        updated['mini_site_title'] = updated['root'].title
        return updated
