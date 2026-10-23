from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.link_block import OptionalLinkBlock


class MeetMozillaStepBlock(blocks.StructBlock):
    label = blocks.CharBlock(max_length=30, help_text='A short name for the step, for example "Imagine".')
    statement = blocks.CharBlock(max_length=140, help_text="One sentence, about 100 characters.")

    class Meta:
        icon = "list-ol"
        label = "Step"


class MeetMozillaBlock(BaseBlock):
    """
    LP's Meet Mozilla section (cosmos/blocks/sections/_meet-mozilla.scss).

    Used as the homepage's fixed Meet Mozilla field, not as a body block. The
    section draws its own band, margins and padding. Step numbers come from
    each step's position, and so do the background colors, which follow LP's
    four states in reading order.
    """

    eyebrow = blocks.CharBlock(required=False, max_length=40, help_text='For example "Meet Mozilla".')
    heading = blocks.CharBlock(max_length=100)
    intro = blocks.CharBlock(
        max_length=100,
        help_text="Sits beside the steps on desktop and stays in view as they scroll. About 60 characters.",
    )
    intro_link = OptionalLinkBlock(required=False, label="Intro link")
    steps = blocks.ListBlock(MeetMozillaStepBlock(), min_num=3, max_num=4)

    class Meta:
        icon = "list-ol"
        label = "Meet Mozilla"
        template_name = "meet_mozilla_block.html"
