from foundation_cms.legacy_apps.wagtailpages.factory.libraries import rcc, research_hub

from . import (
    app_install_page,
    bannered_campaign_page,
    blog,
    buyersguide,
    campaign_page,
    dear_internet_page,
    homepage,
    homepage_cause_statement_link,
    homepage_features,
    homepage_highlights,
    homepage_partner_logos,
    homepage_take_action,
    initiatives_page,
    locale,
    opportunity,
    participate_page,
    participate_page_featured_highlights,
    profiles,
    publication,
    styleguide,
    youtube_regrets_page,
)


def generate(seed):
    # these are not, and should not be, alphabetically ordered.
    locale.generate(seed)
    homepage.generate(seed)
    participate_page.generate(seed)
    profiles.generate(seed)
    blog.generate(seed)
    buyersguide.generate(seed)
    bannered_campaign_page.generate(seed)
    campaign_page.generate(seed)
    dear_internet_page.generate(seed)
    # homepage_features requires blog pages to exist
    homepage_features.generate(seed)
    homepage_partner_logos.generate(seed)
    homepage_take_action.generate(seed)
    homepage_highlights.generate(seed)
    initiatives_page.generate(seed)
    opportunity.generate(seed)
    participate_page_featured_highlights.generate(seed)
    publication.generate(seed)
    styleguide.generate(seed)
    youtube_regrets_page.generate(seed)
    research_hub.generate(seed)
    rcc.generate(seed)
    # homepage_cause_statement_link requires child pages of homepage to exist
    homepage_cause_statement_link.generate(seed)
    app_install_page.generate(seed)


def generate_barebones(seed):
    """
    Minimal wagtailpages content: just enough for a browsable legacy site.

    homepage.html includes its highlights, ideas, take-action and partner
    fragments unconditionally, and those fragments walk into the first item of
    each orderable without checking that one exists, so the homepage 500s unless
    the sections behind them are populated. That fixes the floor for "barebones":
    the locales, the Homepage and its Site record, the blog (highlights indexes
    four BlogPages and ideas_posts picks from the same set), profiles to author
    them, and the homepage section orderables.

    Everything reachable only from a deeper listing is still skipped: the
    buyersguide/PNI, publications, campaigns, MozFest, donate, the RCC and
    research hub libraries, the styleguide and youtube-regrets pages.

    Ordering follows generate() above, which is deliberate and not alphabetical.
    """
    locale.generate(seed)
    homepage.generate(seed)
    profiles.generate(seed)
    blog.generate(seed)
    # homepage_features requires blog pages to exist
    homepage_features.generate(seed)
    homepage_partner_logos.generate(seed)
    homepage_take_action.generate(seed)
    homepage_highlights.generate(seed)
    # homepage_cause_statement_link requires child pages of homepage to exist
    homepage_cause_statement_link.generate(seed)


__all__ = [
    "generate",
    "generate_barebones",
]
