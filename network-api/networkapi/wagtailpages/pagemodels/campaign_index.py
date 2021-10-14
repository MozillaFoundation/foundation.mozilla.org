from .index import IndexPage

from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages.pagemodels.publications.publication import PublicationPage
from networkapi.wagtailpages.utils import get_locale_from_request


class CampaignIndexPage(IndexPage):
    """
    The campaign index is specifically for campaign-related pages
    """

    subpage_types = [
        'BanneredCampaignPage',
        'CampaignPage',
        'DearInternetPage',
        'OpportunityPage',
        'YoutubeRegretsPage',
        'YoutubeRegretsReporterPage',
        'PublicationPage',
        'ArticlePage'
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField('slug'),
        TranslatableField('seo_title'),
        SynchronizedField('show_in_menus'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
        # Content tab fields from IndexPage
        TranslatableField('title'),
        TranslatableField('intro'),
        TranslatableField('header'),
        SynchronizedField('page_size'),
    ]

    template = 'wagtailpages/index_page.html'

    def get_context(self, request):
        # bootstrap the render context
        context = super().get_context(request)
        locale = get_locale_from_request(request)
        entries = self.get_all_entries(locale).not_type(PublicationPage)
        context['entries'] = entries[0:self.page_size]
        # Which pagetype to exclude during the "load more" ajax request: PublicationPage
        context['exclude_pagetype'] = 'publicationpage'
        return context
