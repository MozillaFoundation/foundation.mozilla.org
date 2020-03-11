from .index import IndexPage


class CampaignIndexPage(IndexPage):
    """
    The campaign index is specifically for campaign pages
    """

    subpage_types = [
        'BlogPage',  # FIXME:This one really shouldn't be here.
        'BanneredCampaignPage',
        'CampaignPage',
        'OpportunityPage',
        'YoutubeRegretsPage',
    ]

    template = 'wagtailpages/index_page.html'
