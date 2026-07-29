import factory
import wagtail_factories

from foundation_cms.base.factories import ImageFactory
from foundation_cms.blocks.featured_card_block import FeaturedCardBlock
from foundation_cms.blocks.hero_accordion import ImageTextPanelBlock, VideoPanelBlock
from foundation_cms.blocks.impact_number_block import ImpactNumberBlock, ImpactStatBlock
from foundation_cms.blocks.link_block import LinkBlock
from foundation_cms.blocks.link_button_block import LinkButtonBlock
from foundation_cms.blocks.newsletter_signup_block import NewsletterSignupBlock
from foundation_cms.blocks.pillar_card_block import PillarCardBlock
from foundation_cms.blocks.pillar_card_set_block import PillarCardSetBlock
from foundation_cms.blocks.spotlight_card_block import SpotlightCardBlock
from foundation_cms.blocks.spotlight_card_set_block import SpotlightCardSetBlock
from foundation_cms.blocks.timely_activations_cards_block import (
    ActivationCardBlock,
    TimelyActivationsCardsBlock,
)
from foundation_cms.blocks.title_block import TitleBlock
from foundation_cms.snippets.factories import NewsletterSignupFactory


class LinkBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = LinkBlock

    label = factory.Faker("sentence", nb_words=3)
    link_to = "external_url"
    page = None
    external_url = factory.Faker("url")
    relative_url = ""
    anchor = ""
    email = ""
    file = None
    phone = ""
    new_window = False


class LinkButtonBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = LinkButtonBlock

    label = factory.Faker("sentence", nb_words=3)
    link_to = "external_url"
    page = None
    external_url = factory.Faker("url")
    relative_url = ""
    anchor = ""
    email = ""
    file = None
    phone = ""
    new_window = False
    style = factory.Faker("random_element", elements=["btn-primary", "btn-secondary"])
    alignment = factory.Faker(
        "random_element",
        elements=["link-button-block--left", "link-button-block--center"],
    )


class VideoPanelBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = VideoPanelBlock

    label = factory.Faker("sentence", nb_words=4)
    heading = factory.Faker("sentence", nb_words=12)
    thumbnail = factory.LazyFunction(lambda: ImageFactory().id)
    video_url = "https://vimeo.com/1073235226"


class ImageTextPanelBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = ImageTextPanelBlock

    label = factory.Faker("sentence", nb_words=3)
    heading = factory.Faker("sentence", nb_words=8)
    image = factory.LazyFunction(lambda: ImageFactory().id)
    cta_text = ""
    cta_link = ""
    description = factory.Faker("paragraph", nb_sentences=2)


class NewsletterSignupBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = NewsletterSignupBlock

    newsletter_signup = factory.LazyFunction(lambda: NewsletterSignupFactory().id)


class PillarCardBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = PillarCardBlock

    headline = factory.Faker("sentence", nb_words=6)
    cta_link = wagtail_factories.ListBlockFactory(
        LinkBlockFactory,
        **{"0__link_to": "external_url"},
    )


class PillarCardSetBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = PillarCardSetBlock

    cards = wagtail_factories.ListBlockFactory(
        PillarCardBlockFactory,
        **{"0": "", "1": "", "2": ""},
    )


class TitleBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = TitleBlock

    title = factory.Faker("sentence", nb_words=4)
    style = "shape"


class ImpactStatBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = ImpactStatBlock

    stat_number = factory.Iterator(["$25M", "31K", "33M"])
    stat_heading = factory.Faker("sentence", nb_words=5)
    stat_description = factory.Faker("sentence", nb_words=8)


class ImpactNumberBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = ImpactNumberBlock

    stats = wagtail_factories.ListBlockFactory(
        ImpactStatBlockFactory,
        **{"0": "", "1": "", "2": ""},
    )


class ActivationCardBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = ActivationCardBlock

    category = factory.Faker("word")
    title = factory.Faker("sentence", nb_words=6)
    text = ""
    image = factory.LazyFunction(lambda: ImageFactory().id)
    link = factory.SubFactory(LinkBlockFactory)


class TimelyActivationsCardsBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = TimelyActivationsCardsBlock

    cards = wagtail_factories.StreamFieldFactory(
        {"card": factory.SubFactory(ActivationCardBlockFactory)},
        **{"0": "card", "1": "card", "2": "card"},
    )


class SpotlightCardBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = SpotlightCardBlock

    title = factory.Faker("sentence", nb_words=2)
    name = factory.Faker("name")
    description = factory.Faker("paragraph", nb_sentences=3)
    image = factory.LazyFunction(lambda: ImageFactory().id)


class SpotlightCardSetBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = SpotlightCardSetBlock

    cards = wagtail_factories.ListBlockFactory(
        SpotlightCardBlockFactory,
        **{"0": "", "1": "", "2": ""},
    )


class FeaturedCardBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = FeaturedCardBlock

    heading = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph", nb_sentences=2)
    image = factory.LazyFunction(lambda: ImageFactory().id)
    button = factory.SubFactory(
        LinkButtonBlockFactory,
        link_to="external_url",
        style="btn-primary",
        alignment="link-button-block--left",
    )
