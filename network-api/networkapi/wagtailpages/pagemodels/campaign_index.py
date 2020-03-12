from .index import IndexPage


class CampaignIndexPage(IndexPage):
    """
    The campaign index is specifically for campaign pages
    """

    # Commented off for now, as we'll do the refactor first,
    # then explicitly set up the permitted page types in
    # immediate follow-up.
    #
    # See issue https://github.com/mozilla/foundation.mozilla.org/issues/4221
    #
    # subpage_types = [
    #     'BlogPage',
    #     'BanneredCampaignPage',
    #     'CampaignPage',
    #     'OpportunityPage',
    #     'YoutubeRegretsPage',
    # ]

    template = 'wagtailpages/index_page.html'
