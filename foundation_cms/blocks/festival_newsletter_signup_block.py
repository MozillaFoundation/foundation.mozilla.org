from wagtail import blocks
from wagtail.images.blocks import ImageBlock

from foundation_cms.base.models.base_block import BaseBlock


class FestivalNewsletterSignupBlock(BaseBlock):
    heading = blocks.CharBlock(
        required=True,
        max_length=60,
        label="Heading",
        help_text="Maximum 60 characters.",
    )
    illustration = ImageBlock(
        required=False,
        label="Illustration",
        help_text="Optional decorative illustration.",
    )

    class Meta:
        template_name = "festival_newsletter_signup_block.html"
        icon = "mail"
        label = "Festival Newsletter Signup"
