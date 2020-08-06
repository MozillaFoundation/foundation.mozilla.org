from . import (
    areas_of_focus,
    blog,
    campaign_page,
    bannered_campaign_page,
    homepage_areas_of_focus,
    homepage_take_action,
    homepage_features,
    homepage,
    initiatives_page,
    news_page,
    opportunity,
    participate_page_featured_highlights,
    participate_page,
    styleguide,
    youtube_regrets_page
)


def generate(seed):
    areas_of_focus.generate(seed)
    homepage.generate(seed)
    blog.generate(seed)
    bannered_campaign_page.generate(seed)
    campaign_page.generate(seed)
    # areas_of_focus.generate is required before the homepage_areas_of_focus can exist
    homepage_areas_of_focus.generate(seed)
    # homepage_features.generate requires blog pages to exist first
    homepage_features.generate(seed)
    homepage_take_action.generate(seed)
    initiatives_page.generate(seed)
    news_page.generate(seed)
    opportunity.generate(seed)
    participate_page.generate(seed)
    participate_page_featured_highlights.generate(seed)
    styleguide.generate(seed)
    youtube_regrets_page.generate(seed)

__all__ = [
    'generate'
]
