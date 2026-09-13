from wagtail.images import get_image_model

from foundation_cms.base.factories import ImageFactory
from foundation_cms.blocks.factories import (
    ActivationCardBlockFactory,
    CustomMediaBlockFactory,
    FeaturedCardBlockFactory,
    ImpactNumberBlockFactory,
    ImpactStatBlockFactory,
    LinkBlockFactory,
    LinkButtonBlockFactory,
    NewsletterSignupBlockFactory,
    PillarCardBlockFactory,
    PillarCardSetBlockFactory,
    QuoteBlockFactory,
    SpotlightCardBlockFactory,
    SpotlightCardSetBlockFactory,
    TimelyActivationsCardsBlockFactory,
    TitleBlockFactory,
    VideoBlockFactory,
)

Image = get_image_model()

# A small, reused image pool rather than a fresh ImageFactory() per card:
# this page is rendered for the first time in CI right alongside the rest of
# load_redesign_data, so every distinct image means fresh renditions have to
# be generated cold. Reusing a couple of titles keeps that cost bounded and
# matches the pattern homepage_data.py already uses for its own images.
_SHARED_IMAGE_TITLES = ["General Page placeholder 1", "General Page placeholder 2"]


def _get_or_create_shared_images():
    ids = []
    for title in _SHARED_IMAGE_TITLES:
        existing = Image.objects.filter(title=title).first()
        ids.append(existing.id if existing else ImageFactory(title=title).id)
    return ids


def _pillar_card():
    return dict(
        PillarCardBlockFactory(
            cta_link=[dict(LinkBlockFactory(link_to="external_url"))],
        )
    )


def _activation_card(image_id):
    return {"type": "card", "value": dict(ActivationCardBlockFactory(image=image_id))}


def build_general_page_body():
    """One instance of each GeneralPage body block type that already has a factory."""
    image_1, image_2 = _get_or_create_shared_images()

    return [
        # Text & headings
        {"type": "title_block", "value": dict(TitleBlockFactory(title="General page block coverage"))},
        {"type": "quote", "value": dict(QuoteBlockFactory())},
        # Media
        {"type": "custom_media", "value": dict(CustomMediaBlockFactory(image=image_1))},
        {"type": "video_block", "value": dict(VideoBlockFactory())},
        # Cards & grids
        {
            "type": "pillar_card_set",
            "value": dict(PillarCardSetBlockFactory(cards=[_pillar_card(), _pillar_card(), _pillar_card()])),
        },
        {
            "type": "impact_numbers",
            "value": dict(
                ImpactNumberBlockFactory(
                    stats=[
                        dict(ImpactStatBlockFactory()),
                        dict(ImpactStatBlockFactory()),
                        dict(ImpactStatBlockFactory()),
                    ]
                )
            ),
        },
        {
            "type": "timely_activations_cards",
            "value": dict(
                TimelyActivationsCardsBlockFactory(
                    cards=[
                        _activation_card(image_1),
                        _activation_card(image_2),
                        _activation_card(image_1),
                    ]
                )
            ),
        },
        {
            "type": "spotlight_card_set_block",
            "value": dict(
                SpotlightCardSetBlockFactory(
                    cards=[
                        dict(SpotlightCardBlockFactory(image=image_2)),
                        dict(SpotlightCardBlockFactory(image=image_1)),
                        dict(SpotlightCardBlockFactory(image=image_2)),
                    ]
                )
            ),
        },
        {"type": "featured_card_block", "value": dict(FeaturedCardBlockFactory(image=image_1))},
        # Forms & signups
        {"type": "newsletter_signup", "value": dict(NewsletterSignupBlockFactory())},
        # CTAs & embeds
        {"type": "link_button_block", "value": dict(LinkButtonBlockFactory())},
    ]
