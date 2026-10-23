from foundation_cms.blocks.factories import (
    ActivationCardBlockFactory,
    ImageTextPanelBlockFactory,
    ImpactNumberBlockFactory,
    LinkBlockFactory,
    LinkButtonBlockFactory,
    MeetMozillaBlockFactory,
    NewsletterSignupBlockFactory,
    PillarCardBlockFactory,
    PillarCardSetBlockFactory,
    SpotlightCardBlockFactory,
    SpotlightCardSetBlockFactory,
    TimelyActivationsCardsBlockFactory,
    TitleBlockFactory,
    VideoPanelBlockFactory,
)


def _external_link(label, url, new_window=False):
    return dict(
        LinkBlockFactory(
            label=label,
            link_to="external_url",
            external_url=url,
            relative_url="",
            page=None,
            anchor="",
            email="",
            file=None,
            phone="",
            new_window=new_window,
        )
    )


def _primary_button(label, url):
    return dict(
        LinkButtonBlockFactory(
            label=label,
            link_to="external_url",
            external_url=url,
            relative_url="",
            page=None,
            anchor="",
            email="",
            file=None,
            phone="",
            new_window=False,
            style="btn-primary",
            alignment="link-button-block--left",
        )
    )


def _pillar_card(headline, image, cta_label, cta_url):
    return dict(
        PillarCardBlockFactory(
            headline=headline,
            image=image,
            cta_link=[_external_link(cta_label, cta_url)],
        )
    )


def _activation_card(category, title, image, cta_label, cta_url):
    return {
        "type": "card",
        "value": dict(
            ActivationCardBlockFactory(
                category=category,
                title=title,
                text="",
                image=image,
                link=_external_link(cta_label, cta_url),
            )
        ),
    }


def build_homepage_hero_accordion(images):
    return [
        {
            "type": "video_panel",
            "value": dict(
                VideoPanelBlockFactory(
                    label="Stand up for a better internet",
                    heading=(
                        "Hear from Mozilla Foundation’s CEO Nabiha Syed on why "
                        "making good is about building ethical technology."
                    ),
                    thumbnail=images["hero_accordion__1"],
                    video_url="https://vimeo.com/1073235226",
                )
            ),
        },
        {
            "type": "image_text_panel",
            "value": dict(
                ImageTextPanelBlockFactory(
                    label="Mozilla Festival 2025",
                    heading="Bold ideas shaping the future of technology",
                    image=images["hero_accordion__2"],
                    cta_text="",
                    cta_link="",
                    description=(
                        "Join us in Barcelona this November for three days to "
                        "unlearn and reimagine the role of technology in our lives."
                    ),
                )
            ),
        },
        {
            "type": "image_text_panel",
            "value": dict(
                ImageTextPanelBlockFactory(
                    label="Community",
                    heading="How we make it matters",
                    image=images["hero_accordion__3"],
                    cta_text="",
                    cta_link="",
                    description=(
                        "The internet is for everyone. Let’s make it good together " "with our community and yours."
                    ),
                )
            ),
        },
    ]


def build_homepage_meet_mozilla():
    return [
        {
            "type": "meet_mozilla",
            "value": dict(
                MeetMozillaBlockFactory(
                    eyebrow="Meet Mozilla",
                    heading="Mozilla Foundation supports...",
                    intro="Advancing technology that reflects human values.",
                    intro_link=[_external_link("Learn more", "https://example.com")],
                    steps=[
                        {
                            "label": "Imagine",
                            "statement": (
                                "We search in unlikely places for people imagining tech that works for more of us."
                            ),
                        },
                        {
                            "label": "Co-create",
                            "statement": (
                                "We offer capital and expertise to builders developing tech for their own communities."
                            ),
                        },
                        {
                            "label": "Mobilize",
                            "statement": "We connect builders and dreamers so that good ideas can travel.",
                        },
                    ],
                )
            ),
        },
    ]


def build_homepage_body(main_newsletter_id, images):
    return [
        {
            "type": "newsletter_signup",
            "value": dict(
                NewsletterSignupBlockFactory(
                    newsletter_signup=main_newsletter_id,
                )
            ),
        },
        {
            "type": "pillar_card_set",
            "value": dict(
                PillarCardSetBlockFactory(
                    cards=[
                        _pillar_card(
                            headline="We invest in alternative tech futures",
                            image=images["pillar_card__1"],
                            cta_label="Calling all builders",
                            cta_url="https://example.com",
                        ),
                        _pillar_card(
                            headline="Better tech education for everyone, everywhere",
                            image=images["pillar_card__2"],
                            cta_label="Learn with us",
                            cta_url="https://example.com",
                        ),
                        _pillar_card(
                            headline="Powered by our people and purpose",
                            image=images["pillar_card__3"],
                            cta_label="Let's mobilize",
                            cta_url="https://example.com",
                        ),
                    ]
                )
            ),
        },
        {
            "type": "title_block",
            "value": dict(
                TitleBlockFactory(
                    title="Impact numbers",
                    style="shape",
                )
            ),
        },
        {
            "type": "impact_numbers",
            "value": dict(
                ImpactNumberBlockFactory(
                    stats=[
                        {
                            "stat_number": "$25M",
                            "stat_heading": "Common Voice Audio Clips",
                            "stat_description": "The world’s largest crowdsourced datasets powered by people.",
                        },
                        {
                            "stat_number": "31K",
                            "stat_heading": "Nurturing the next generation of responsible technologists",
                            "stat_description": "Monthly page views.",
                        },
                        {
                            "stat_number": "33M",
                            "stat_heading": "Awarded in grants",
                            "stat_description": "Fueling over 800 worldwide tech for good projects.",
                        },
                    ]
                )
            ),
        },
        {
            "type": "title_block",
            "value": dict(
                TitleBlockFactory(
                    title="Timely activations",
                    style="loop-line",
                )
            ),
        },
        {
            "type": "timely_activations_cards",
            "value": dict(
                TimelyActivationsCardsBlockFactory(
                    cards=[
                        _activation_card(
                            category="Campaign",
                            title="See No Evil: Shining a light surveillance tech",
                            image=images["timely_activations__1"],
                            cta_label="Our ShadowDragon campaign",
                            cta_url="https://example.com",
                        ),
                        _activation_card(
                            category="Mozilla Festival 2025",
                            title="Early Bird badges are on sale",
                            image=images["timely_activations__2"],
                            cta_label="Get yours today!",
                            cta_url="https://example.com",
                        ),
                        _activation_card(
                            category="Data",
                            title="The most diverse open voice dataset in the world",
                            image=images["timely_activations__3"],
                            cta_label="Be part of Common Voice",
                            cta_url="https://example.com",
                        ),
                    ]
                )
            ),
        },
        {
            "type": "title_block",
            "value": dict(
                TitleBlockFactory(
                    title="Community spotlight",
                    style="shape",
                )
            ),
        },
        {
            "type": "spotlight_card_set_block",
            "value": dict(
                SpotlightCardSetBlockFactory(
                    cards=[
                        dict(
                            SpotlightCardBlockFactory(
                                title="Faculty",
                                name="Dr. Mary Mwadulo",
                                description="Dr. Mary is reimagining tech education in Kenya...",
                                image=images["spotlight_card_set__1"],
                            )
                        ),
                        dict(
                            SpotlightCardBlockFactory(
                                title="Common Voice",
                                name="Irvin Chen",
                                description="Irvin is inspiring more people to build a better digital future...",
                                image=images["spotlight_card_set__2"],
                            )
                        ),
                        dict(
                            SpotlightCardBlockFactory(
                                title="Festival Wrangler",
                                name="Surabhi Srivastava",
                                description="Surabhi explores how media can be a lever to drive social impact...",
                                image=images["spotlight_card_set__3"],
                            )
                        ),
                    ]
                )
            ),
        },
    ]
