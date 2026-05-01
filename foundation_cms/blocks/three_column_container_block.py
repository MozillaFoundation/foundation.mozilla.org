from wagtail.blocks import ChoiceBlock, StreamBlock

from foundation_cms.base.models.base_block import BaseBlock

from .common.background_color_block import BackgroundColorChoiceBlock
from .custom_rich_text_block import CustomRichTextBlock
from .fru_element_block import FruElementBlock
from .gallery_card_block import GalleryCardBlock
from .image_block import CustomImageBlock
from .link_button_block import LinkButtonBlock
from .list_block import ListBlock
from .newsletter_signup_block import NewsletterSignupBlock
from .podcast_block import PodcastBlock
from .quote_block import QuoteBlock
from .spacer_block import SpacerBlock
from .video_block import VideoBlock


class ThreeColumnStreamBlock(StreamBlock):
    rich_text = CustomRichTextBlock()
    podcast = PodcastBlock()
    image = CustomImageBlock()
    newsletter_signup = NewsletterSignupBlock()
    video = VideoBlock()
    list = ListBlock()
    spacer = SpacerBlock()
    quote = QuoteBlock()
    link_button = LinkButtonBlock()
    fru_element = FruElementBlock()
    gallery_card = GalleryCardBlock()


class ThreeColumnContainerBlock(BaseBlock):
    background_color = BackgroundColorChoiceBlock()
    vertical_alignment = ChoiceBlock(
        choices=[
            ("top", "Top"),
            ("middle", "Middle"),
            ("bottom", "Bottom"),
        ],
        default="middle",
        help_text="Vertical alignment of the columns content",
    )
    left_column = ThreeColumnStreamBlock(label="Left Column", required=False)
    center_column = ThreeColumnStreamBlock(label="Center Column", required=False)
    right_column = ThreeColumnStreamBlock(label="Right Column", required=False)

    class Meta:
        template_name = "three_column_container_block.html"
        icon = "placeholder"
        label = "Three Column Container"
