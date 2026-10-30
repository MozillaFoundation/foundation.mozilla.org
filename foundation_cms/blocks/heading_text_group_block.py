from django.core.exceptions import ValidationError
from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.link_block import LinkWithDynamicLabelBlock

LABEL_TYPE_CHOICES = [
    ("default", "Default"),
    ("tag", "Tag"),
    ("notification", "Notification"),
    ("big_label", "Big Label"),
]
BIG_LABEL_STYLE_CHOICES = [("number", "Number"), ("highlight", "Highlight")]
TAG_COLOR_CHOICES = [("white", "White"), ("warm-grey", "Warm Grey")]
ACCENT_COLOR_CHOICES = [
    ("yellow", "Yellow"),
    ("blue", "Blue"),
    ("green", "Green"),
    ("orange", "Orange"),
    ("pink", "Pink"),
]
HEADING_LEVEL_CHOICES = [("h1", "H1"), ("h2", "H2"), ("h3", "H3"), ("h4", "H4")]
ACTION_TYPE_CHOICES = [("link", "Link"), ("button", "Button")]


class HeadingTextGroupBlock(BaseBlock):
    is_cosmos_block = True

    label_type = blocks.ChoiceBlock(
        choices=LABEL_TYPE_CHOICES,
        default="default",
        help_text="Big Label: a numbered or highlighted label over an H2 statement, with no subheading or action.",
    )
    label = blocks.CharBlock(
        required=False,
        max_length=50,
        help_text="Optional. Plain text above the heading; it is not a heading.",
    )
    big_label_style = blocks.ChoiceBlock(choices=BIG_LABEL_STYLE_CHOICES, default="number")
    number = blocks.CharBlock(required=False, max_length=10, help_text='For example "01".')
    highlight_color = blocks.ChoiceBlock(choices=ACCENT_COLOR_CHOICES, default="green")
    tag_color = blocks.ChoiceBlock(choices=TAG_COLOR_CHOICES, default="warm-grey")
    notification_color = blocks.ChoiceBlock(choices=ACCENT_COLOR_CHOICES, default="yellow")

    heading = blocks.CharBlock(max_length=150)
    heading_level = blocks.ChoiceBlock(
        choices=HEADING_LEVEL_CHOICES,
        default="h2",
        help_text="Choose the level that fits the page outline.",
    )
    subheading = blocks.CharBlock(required=False, max_length=300, help_text="Optional. One short paragraph.")

    action_type = blocks.ChoiceBlock(choices=ACTION_TYPE_CHOICES, default="link")
    action = blocks.ListBlock(
        LinkWithDynamicLabelBlock(label_max_length=20, label="Action"),
        min_num=0,
        max_num=1,
        default=[],
        label="Action",
        help_text="Optional. The label is limited to 20 characters.",
    )

    class Meta:
        icon = "title"
        label = "Heading Text Group"
        template_name = "heading_text_group_block.html"
        # Attaches the Stimulus controller that hides the fields a label type doesn't use.
        form_attrs = {"data-controller": "heading-text-group"}

    def clean(self, value):
        cleaned = super().clean(value)
        errors = {}

        if cleaned["label_type"] == "big_label":
            if not cleaned["label"]:
                errors["label"] = ValidationError("Big Label needs label text.")
            if cleaned["big_label_style"] == "number" and not cleaned["number"]:
                errors["number"] = ValidationError("Enter the number for this Big Label.")

        if errors:
            raise blocks.StructBlockValidationError(errors)

        return cleaned
