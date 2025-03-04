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


__all__ = [
    "generate",
]
