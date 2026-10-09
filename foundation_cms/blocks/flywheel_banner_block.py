from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

MISSION_CHOICES = [
    ("imagine", "Imagine"),
    ("co-create", "Co-create"),
    ("mobilize", "Mobilize"),
]


class FlywheelBannerBlock(BaseBlock):
    mission = blocks.ChoiceBlock(
        choices=MISSION_CHOICES,
        default="imagine",
        help_text="Select the mission that determines the banner artwork and colors.",
    )
    heading = blocks.CharBlock(
        default="Imagine",
        max_length=50,
        help_text="Defaults to the mission name, but can be customized and translated.",
    )

    class Meta:
        form_template = "patterns/admin/flywheel_banner_block_form.html"
        icon = "image"
        label = "Flywheel Banner"
        template_name = "flywheel_banner_block.html"
