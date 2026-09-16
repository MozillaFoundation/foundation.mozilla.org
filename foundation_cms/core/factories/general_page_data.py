from wagtail.images import get_image_model

from foundation_cms.base.factories import ImageFactory
from foundation_cms.blocks.factories import (
    AccordionBlockFactory,
    AccordionBlockItemFactory,
    ActivationCardBlockFactory,
    CustomImageBlockFactory,
    CustomMediaBlockFactory,
    DividerBlockFactory,
    DonorHelpContactUsFormBlockFactory,
    FeaturedCardBlockFactory,
    FruElementBlockFactory,
    IconInfoGridBlockFactory,
    IconInfoGridItemBlockFactory,
    IllustratedNewsletterSignupBlockFactory,
    ImageCarouselBlockFactory,
    ImageCarouselItemBlockFactory,
    ImageGridBlockFactory,
    ImageGridItemBlockFactory,
    ImageGridSectionBlockFactory,
    ImpactNumberBlockFactory,
    ImpactStatBlockFactory,
    LinkBlockFactory,
    LinkButtonBlockFactory,
    ListBlockFactory,
    NewsletterSignupBlockFactory,
    NewsletterUnsubscribeBlockFactory,
    PillarCardBlockFactory,
    PillarCardSetBlockFactory,
    PodcastBlockFactory,
    PortraitCardBlockFactory,
    PortraitCardSetBlockFactory,
    QuoteBlockFactory,
    SpacerBlockFactory,
    SpotlightCardBlockFactory,
    SpotlightCardSetBlockFactory,
    ThreeColumnContainerBlockFactory,
    TimelyActivationsCardsBlockFactory,
    TitleBlockFactory,
    TwoColumnContainerBlockFactory,
    VideoBlockFactory,
    iFrameBlockFactory,
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


def _portrait_card(image_id):
    return dict(
        PortraitCardBlockFactory(
            image=image_id,
            cta_link=dict(LinkBlockFactory(link_to="external_url")),
        )
    )


def _icon_info_grid_item():
    return dict(IconInfoGridItemBlockFactory())


def _accordion_item():
    return dict(AccordionBlockItemFactory())


def _carousel_item(image_id):
    return {"type": "carousel_item", "value": dict(ImageCarouselItemBlockFactory(image=image_id))}


def _column_content(image_id):
    return [
        {"type": "rich_text", "value": "<p>Sample column content.</p>"},
        {"type": "image", "value": dict(CustomImageBlockFactory(image=image_id))},
        {"type": "quote", "value": dict(QuoteBlockFactory())},
    ]


def _image_grid_item(image_id):
    return dict(ImageGridItemBlockFactory(image=image_id))


def _image_grid_section(image_1, image_2):
    return dict(
        ImageGridSectionBlockFactory(
            items=[
                _image_grid_item(image_1),
                _image_grid_item(image_2),
                _image_grid_item(image_1),
                _image_grid_item(image_2),
            ]
        )
    )


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
        {"type": "divider", "value": dict(DividerBlockFactory())},
        {"type": "spacer_block", "value": dict(SpacerBlockFactory())},
        {"type": "podcast_block", "value": dict(PodcastBlockFactory())},
        {"type": "iframe_block", "value": dict(iFrameBlockFactory())},
        {"type": "fru_element_block", "value": dict(FruElementBlockFactory())},
        {"type": "image", "value": dict(CustomImageBlockFactory(image=image_2))},
        {
            "type": "donor_help_contact_us_form",
            "value": dict(DonorHelpContactUsFormBlockFactory(image=image_1)),
        },
        {"type": "newsletter_unsubscribe", "value": dict(NewsletterUnsubscribeBlockFactory())},
        {"type": "illustrated_newsletter_signup", "value": dict(IllustratedNewsletterSignupBlockFactory())},
        {
            "type": "portrait_card_set_block",
            "value": dict(
                PortraitCardSetBlockFactory(
                    cards=[_portrait_card(image_1), _portrait_card(image_2), _portrait_card(image_1)]
                )
            ),
        },
        {
            "type": "icon_info_grid",
            "value": dict(
                IconInfoGridBlockFactory(
                    items=[_icon_info_grid_item(), _icon_info_grid_item(), _icon_info_grid_item()]
                )
            ),
        },
        {
            "type": "list_block",
            "value": dict(
                ListBlockFactory(
                    items=[
                        dict(LinkBlockFactory(link_to="external_url")),
                        dict(LinkBlockFactory(link_to="external_url")),
                    ]
                )
            ),
        },
        {
            "type": "image_grid",
            "value": dict(ImageGridBlockFactory(sections=[_image_grid_section(image_1, image_2)])),
        },
        {
            "type": "accordion_block",
            "value": dict(AccordionBlockFactory(accordion_items=[_accordion_item(), _accordion_item()])),
        },
        {
            "type": "image_carousel_block",
            "value": dict(
                ImageCarouselBlockFactory(
                    items=[
                        _carousel_item(image_1),
                        _carousel_item(image_2),
                        _carousel_item(image_1),
                    ]
                )
            ),
        },
        {
            "type": "two_column_container_block",
            "value": dict(
                TwoColumnContainerBlockFactory(
                    left_column=_column_content(image_1),
                    right_column=_column_content(image_2),
                )
            ),
        },
        {
            "type": "three_column_container_block",
            "value": dict(
                ThreeColumnContainerBlockFactory(
                    left_column=_column_content(image_1),
                    center_column=_column_content(image_2),
                    right_column=_column_content(image_1),
                )
            ),
        },
        {"type": "rich_text", "value": "<p>Sample rich text content.</p>"},
    ]
