from django.utils.text import slugify
from wagtail.blocks import CharBlock, ChoiceBlock

from foundation_cms.base.models.base_block import BaseBlock


class TitleBlock(BaseBlock):
    """
    A simple title block that can be used to create visual breaks in content with two style options.
    """

    title = CharBlock(required=True, help_text="Title for the block")

    style = ChoiceBlock(
        choices=[
            ("shape", "Shape"),
            ("loop-line", "Loop Line"),
        ],
        default="shape",
        help_text="Select the style of the title",
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        title_anchor_ids = getattr(context.get("page"), "title_anchor_ids", {})
        context["anchor_id"] = title_anchor_ids.get(context.get("block_id")) or slugify(value["title"])
        return context

    class Meta:
        template_name = "title_block.html"
        label = "Title"
