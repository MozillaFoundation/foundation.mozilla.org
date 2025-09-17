from wagtail.blocks import ChoiceBlock, RichTextBlock, StreamBlock

from foundation_cms.base.models.base_block import BaseBlock

from .audio_block import AudioBlock  # Just as an example second block
from .image_block import CustomImageBlock
from .list_block import ListBlock
from .newsletter_signup_block import NewsletterSignupBlock
from .quote_block import QuoteBlock
from .spacer_block import SpacerBlock
from .text_social_block import TextSocialBlock
from .video_block import VideoBlock


class ColumnStreamBlock(StreamBlock):
    rich_text = RichTextBlock()
    audio = AudioBlock()
    image = CustomImageBlock()
    newsletter_signup = NewsletterSignupBlock()
    video = VideoBlock()
    list = ListBlock()
    spacer = SpacerBlock()
    quote = QuoteBlock()
    text_social = TextSocialBlock()


class TwoColumnContainerBlock(BaseBlock):
    vertical_alignment = ChoiceBlock(
        choices=[
            ("top", "Top"),
            ("middle", "Middle"),
            ("bottom", "Bottom"),
        ],
        default="middle",
        help_text="Vertical alignment of the columns content",
    )
    left_column = ColumnStreamBlock(label="Left Column", required=False)
    right_column = ColumnStreamBlock(label="Right Column", required=False)

    class Meta:
        template_name = "two_column_container_block.html"
        icon = "placeholder"
        label = "Two Column Container"
