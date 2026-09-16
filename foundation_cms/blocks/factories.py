import factory
import wagtail_factories

from foundation_cms.base.factories import ImageFactory
from foundation_cms.blocks.accordion_block import AccordionBlock, AccordionBlockItem
from foundation_cms.blocks.divider_block import DividerBlock
from foundation_cms.blocks.donor_help_contact_us_form_block import (
    DonorHelpContactUsFormBlock,
)
from foundation_cms.blocks.featured_card_block import FeaturedCardBlock
from foundation_cms.blocks.fru_element_block import FruElementBlock
from foundation_cms.blocks.hero_accordion import ImageTextPanelBlock, VideoPanelBlock
from foundation_cms.blocks.icon_info_grid_block import (
    IconInfoGridBlock,
    IconInfoGridItemBlock,
)
from foundation_cms.blocks.iframe_block import iFrameBlock
from foundation_cms.blocks.illustrated_newsletter_signup_block import (
    IllustratedNewsletterSignupBlock,
)
from foundation_cms.blocks.image_block import CustomImageBlock
from foundation_cms.blocks.image_carousel_block import (
    ImageCarouselBlock,
    ImageCarouselItemBlock,
)
from foundation_cms.blocks.image_grid_block import (
    ImageGridBlock,
    ImageGridItemBlock,
    ImageGridSectionBlock,
)
from foundation_cms.blocks.impact_number_block import ImpactNumberBlock, ImpactStatBlock
from foundation_cms.blocks.link_block import LinkBlock
from foundation_cms.blocks.link_button_block import LinkButtonBlock
from foundation_cms.blocks.list_block import ListBlock
from foundation_cms.blocks.media_block import CustomMediaBlock
from foundation_cms.blocks.newsletter_signup_block import NewsletterSignupBlock
from foundation_cms.blocks.newsletter_unsubscribe_block import (
    NewsletterUnsubscribeBlock,
)
from foundation_cms.blocks.pillar_card_block import PillarCardBlock
from foundation_cms.blocks.pillar_card_set_block import PillarCardSetBlock
from foundation_cms.blocks.podcast_block import PodcastBlock
from foundation_cms.blocks.portrait_card_block import PortraitCardBlock
from foundation_cms.blocks.portrait_card_set_block import PortraitCardSetBlock
from foundation_cms.blocks.quote_block import QuoteBlock
from foundation_cms.blocks.spacer_block import SpacerBlock
from foundation_cms.blocks.spotlight_card_block import SpotlightCardBlock
from foundation_cms.blocks.spotlight_card_set_block import SpotlightCardSetBlock
from foundation_cms.blocks.timely_activations_cards_block import (
    ActivationCardBlock,
    TimelyActivationsCardsBlock,
)
from foundation_cms.blocks.title_block import TitleBlock
from foundation_cms.blocks.video_block import VideoBlock
from foundation_cms.snippets.factories import (
    IllustratedNewsletterSignupFactory,
    NewsletterSignupFactory,
    NewsletterUnsubscribeFactory,
)


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


class QuoteBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = QuoteBlock

    quote = factory.Faker("sentence", nb_words=12)
    attribution = factory.Faker("name")


class CustomMediaBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = CustomMediaBlock

    title = factory.Faker("sentence", nb_words=3)
    content = "image"
    image = None
    video_url = ""
    orientation = "landscape"


class VideoBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = VideoBlock

    video_url = "https://vimeo.com/1073235226"
    caption = ""
    caption_url: list = []


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


class DividerBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = DividerBlock


class SpacerBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = SpacerBlock

    size = "medium"


class PodcastBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = PodcastBlock

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph", nb_sentences=2)
    simplecast_embed_code = "<iframe src='https://player.simplecast.com/example'></iframe>"


class iFrameBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = iFrameBlock

    url = "https://example.org/embed"
    height = 600
    iframe_width = "normal"
    disable_scroll = False


class FruElementBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = FruElementBlock

    fru_element_type = "donate-button"
    fru_element_embed_code = "<div id='fru-donate-button'></div>"


class CustomImageBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = CustomImageBlock

    title = factory.Faker("sentence", nb_words=3)
    image = factory.LazyFunction(lambda: ImageFactory().id)
    orientation = "landscape"


class DonorHelpContactUsFormBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = DonorHelpContactUsFormBlock

    heading = "Contact Us"
    subheading = "Questions about your donation? Get in touch with our team by using the form below."
    image = factory.LazyFunction(lambda: ImageFactory().id)


class NewsletterUnsubscribeBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = NewsletterUnsubscribeBlock

    newsletter_unsubscribe = factory.LazyFunction(lambda: NewsletterUnsubscribeFactory().id)


class IllustratedNewsletterSignupBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = IllustratedNewsletterSignupBlock

    newsletter_signup = factory.LazyFunction(lambda: IllustratedNewsletterSignupFactory().id)


class PortraitCardBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = PortraitCardBlock

    label = factory.Faker("word")
    headline = factory.Faker("sentence", nb_words=4)
    image = factory.LazyFunction(lambda: ImageFactory().id)
    cta_link = factory.SubFactory(LinkBlockFactory, link_to="external_url")


class PortraitCardSetBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = PortraitCardSetBlock

    cards = wagtail_factories.ListBlockFactory(
        PortraitCardBlockFactory,
        **{"0": "", "1": "", "2": ""},
    )


class IconInfoGridItemBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = IconInfoGridItemBlock

    icon = "star"
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("sentence", nb_words=10)


class IconInfoGridBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = IconInfoGridBlock

    heading = factory.Faker("sentence", nb_words=4)
    icon_color = "orange"
    columns = "3"
    layout_style = "detailed"
    items = wagtail_factories.ListBlockFactory(
        IconInfoGridItemBlockFactory,
        **{"0": "", "1": "", "2": ""},
    )


class ListBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = ListBlock

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph", nb_sentences=2)
    items = wagtail_factories.ListBlockFactory(
        LinkBlockFactory,
        **{"0__link_to": "external_url", "1__link_to": "external_url"},
    )


class ImageGridItemBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = ImageGridItemBlock

    image = factory.LazyFunction(lambda: ImageFactory().id)
    caption = "<p>Sample caption</p>"
    link: list = []


class ImageGridSectionBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = ImageGridSectionBlock

    heading = factory.Faker("sentence", nb_words=3)
    section_orientation = "landscape"
    items_per_row = "4"
    items = wagtail_factories.ListBlockFactory(
        ImageGridItemBlockFactory,
        **{"0": "", "1": "", "2": "", "3": ""},
    )


class ImageGridBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = ImageGridBlock

    sections = wagtail_factories.ListBlockFactory(
        ImageGridSectionBlockFactory,
        **{"0": ""},
    )


class AccordionBlockItemFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = AccordionBlockItem

    title = factory.Faker("sentence", nb_words=4)
    content = [{"type": "rich_text", "value": "<p>Sample accordion content.</p>"}]


class AccordionBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = AccordionBlock

    accordion_items = wagtail_factories.ListBlockFactory(
        AccordionBlockItemFactory,
        **{"0": "", "1": ""},
    )


class ImageCarouselItemBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = ImageCarouselItemBlock

    image = factory.LazyFunction(lambda: ImageFactory().id)
    header = factory.Faker("sentence", nb_words=3)
    title = factory.Faker("sentence", nb_words=4)
    description = "<p>Sample carousel item description.</p>"
    link: list = []


class ImageCarouselBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = ImageCarouselBlock

    title = factory.Faker("sentence", nb_words=3)
    orientation = "portrait"
    items = wagtail_factories.StreamFieldFactory(
        {"carousel_item": factory.SubFactory(ImageCarouselItemBlockFactory)},
        **{"0": "carousel_item", "1": "carousel_item", "2": "carousel_item"},
    )
