from wagtail.blocks import CharBlock, RichTextBlock

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks import CustomImageBlock


class PetitionSignedBlock(BaseBlock):
    header = CharBlock(
        max_length=500, help_text="Donation header", default="Thanks for signing! While you're here, we need your help"
    )

    body = RichTextBlock(
        help_text="Donation text",
        default="Mozilla is a nonprofit organization fighting for "
        "a healthy internet, where privacy is included by "
        "design and you have more control over your personal "
        "information. We depend on contributions from people "
        "like you to carry out this work. Can you donate today?",
    )

    donate_button_text = CharBlock(
        max_length=150,
        help_text="Donate button label",
        default="Yes, I'll chip in $10",
    )

    share_button_text = CharBlock(
        max_length=150,
        help_text="Share button label",
        default="No, I will share instead",
    )

    skip_button_text = CharBlock(
        max_length=150,
        help_text="Skip button label",
        default="Sorry, not right now",
    )

    class Meta:
        template = "campaigns/blocks/petition_signed_block.html"
        icon = "heart"
        label = "Signed Petition Panel"


class PetitionShareBlock(BaseBlock):
    header = CharBlock(max_length=500, help_text="Share header", default="Share this with at least one other person")

    body = RichTextBlock(
        help_text="Share text",
        default="Mozilla is a nonprofit organization fighting for "
        "a healthy internet, where privacy is included by "
        "design and you have more control over your personal "
        "information. We depend on contributions from people "
        "like you to carry out this work. Can you share this petition?",
    )

    skip_button_text = CharBlock(
        max_length=150,
        help_text="Skip button label",
        default="Sorry, not right now",
    )

    class Meta:
        template = "campaigns/blocks/petition_share_block.html"
        icon = "share"
        label = "Share Prompt Panel"


class PetitionThankYouBlock(BaseBlock):
    header = CharBlock(max_length=500, help_text="Thank you header", default="All done here!")

    body = RichTextBlock(
        help_text="Thank you text",
        default="Mozilla is a nonprofit organization fighting for "
        "a healthy internet, where privacy is included by "
        "design and you have more control over your personal "
        "information. We depend on contributions from people "
        "like you to carry out this work. Thank you for helping us!",
    )

    image = CustomImageBlock(required=False)

    class Meta:
        template = "campaigns/blocks/petition_thank_you_block.html"
        icon = "tick"
        label = "Thank You Panel"
