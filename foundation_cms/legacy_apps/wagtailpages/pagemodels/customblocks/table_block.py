from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock


class WideTableBlock(blocks.StructBlock):
    """
    A custom block that contains a table and an option to render it wider than the page body content.
    """

    table = TableBlock()

    wide = blocks.BooleanBlock(
        required=False,
        default=True,
        help_text="If checked, the table will render wider than the other page body content.",
    )

    def get_context(self, value, parent_context=None):
        """
        Override get_context to add the table body logic to the template context.
        If `first_row_is_table_header` is True, it slices the data to skip the first row.
        Otherwise, it returns the full data set.
        """
        context = super().get_context(value, parent_context=parent_context)

        # Check if the first row is a header and slice the data accordingly
        if value.get("table").get("first_row_is_table_header") is True:
            context["table_body"] = value["table"]["data"][1:]  # Skip the first row
        else:
            context["table_body"] = value["table"]["data"]  # Return the full data set

        return context

    class Meta:
        icon = "table"
        label = "Table"
        template = "wagtailpages/blocks/wide_table_block.html"
