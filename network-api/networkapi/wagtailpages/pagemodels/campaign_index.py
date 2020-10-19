from .index import IndexPage


class CampaignIndexPage(IndexPage):
    """
    The campaign index is specifically for campaign-related pages
    """

    subpage_types = [
        'BanneredCampaignPage',
        'CampaignPage',
        'OpportunityPage',
        'YoutubeRegretsPage',
        'YoutubeRegretsReporterPage',
        'PublicationPage',
    ]

    template = 'wagtailpages/index_page.html'
