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


def _pillar_card():
    return dict(
        PillarCardBlockFactory(
            cta_link=[dict(LinkBlockFactory(link_to="external_url"))],
        )
    )


def _activation_card():
    return {"type": "card", "value": dict(ActivationCardBlockFactory())}


def build_general_page_body():
    """One instance of each GeneralPage body block type that already has a factory."""
    return [
        {"type": "title_block", "value": dict(TitleBlockFactory(title="General page block coverage"))},
        {"type": "quote", "value": dict(QuoteBlockFactory())},
        {"type": "custom_media", "value": dict(CustomMediaBlockFactory(image=ImageFactory().id))},
        {"type": "video_block", "value": dict(VideoBlockFactory())},
        {"type": "newsletter_signup", "value": dict(NewsletterSignupBlockFactory())},
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
                TimelyActivationsCardsBlockFactory(cards=[_activation_card(), _activation_card(), _activation_card()])
            ),
        },
        {
            "type": "spotlight_card_set_block",
            "value": dict(
                SpotlightCardSetBlockFactory(
                    cards=[
                        dict(SpotlightCardBlockFactory()),
                        dict(SpotlightCardBlockFactory()),
                        dict(SpotlightCardBlockFactory()),
                    ]
                )
            ),
        },
        {"type": "featured_card_block", "value": dict(FeaturedCardBlockFactory())},
        {"type": "link_button_block", "value": dict(LinkButtonBlockFactory())},
    ]
