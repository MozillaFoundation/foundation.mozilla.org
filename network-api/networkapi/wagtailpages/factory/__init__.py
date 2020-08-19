from . import (
    blog,
    campaign_page,
    bannered_campaign_page,
    homepage_features,
    homepage,
    initiatives_page,
    news_page,
    opportunity,
    participate_page_featured_highlights,
    participate_page,
    publication,
    styleguide,
    youtube_regrets_page,
)


def generate(seed):
    homepage.generate(seed)
    blog.generate(seed)
    # homepage_features.generate requires blog pages to exist first
    homepage_features.generate(seed)
    campaign_page.generate(seed)
    bannered_campaign_page.generate(seed)
    initiatives_page.generate(seed)
    news_page.generate(seed)
    opportunity.generate(seed)
    participate_page.generate(seed)
    participate_page_featured_highlights.generate(seed)
    publication.generate(seed)
    styleguide.generate(seed)
    youtube_regrets_page.generate(seed)


__all__ = [
    'generate'
]
