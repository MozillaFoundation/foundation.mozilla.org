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

# Each entry is (factory_module, required_for_barebones). generate() runs every
# step below in order; generate_barebones() runs only the ones flagged True,
# in that same order
#
# These are not, and should not be, alphabetically ordered.
STEPS = [
    (locale, True),
    (homepage, True),
    (participate_page, False),
    (profiles, True),
    (blog, True),
    (buyersguide, False),
    (bannered_campaign_page, False),
    (campaign_page, False),
    (dear_internet_page, False),
    # homepage_features requires blog pages to exist
    (homepage_features, True),
    (homepage_partner_logos, True),
    (homepage_take_action, True),
    (homepage_highlights, True),
    (initiatives_page, False),
    (opportunity, False),
    (participate_page_featured_highlights, False),
    (publication, False),
    (styleguide, False),
    (youtube_regrets_page, False),
    (research_hub, False),
    (rcc, False),
    # homepage_cause_statement_link requires child pages of homepage to exist
    (homepage_cause_statement_link, True),
    (app_install_page, False),
]


def generate(seed):
    for step, _ in STEPS:
        step.generate(seed)


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

    Runs the STEPS list above filtered to required_for_barebones
    """
    for step, required in STEPS:
        if required:
            step.generate(seed)


__all__ = [
    "generate",
    "generate_barebones",
]
