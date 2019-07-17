from . import (
    blog,
    campaign_page,
    homepage_features,
    homepage,
    initiatives_page,
    news_page,
    opportunity,
    participate_page_featured_highlights,
    participate_page,
    styleguide
)


def generate(seed):
    homepage.generate(seed)
    homepage_features.generate(seed)
    blog.generate(seed)
    campaign_page.generate(seed)
    initiatives_page.generate(seed)
    news_page.generate(seed)
    opportunity.generate(seed)
    participate_page.generate(seed)
    participate_page_featured_highlights.generate(seed)
    styleguide.generate(seed)


__all__ = [
    'generate'
]
