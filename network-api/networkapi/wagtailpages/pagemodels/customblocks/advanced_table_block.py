"""
The "Advanced" table block uses StreamBlocks to create rows and cells inside of each row.
Every cell can have rich text, and a column width (colspan), along with centered text.

We are using StreamBlocks instead of ListBlocks to account for wagtail-localize's lack of ListBlock support.
"""

from django.core.validators import MaxValueValidator, MinValueValidator

from wagtail.core import blocks
from .base_rich_text_options import base_rich_text_options


class Cell(blocks.StructBlock):
    centered_text = blocks.BooleanBlock(required=False)
    column_width = blocks.IntegerBlock(
        default=1,
        help_text='Enter the number of extra cell columns you want to merge together. '
                  'Merging a cell column will expand a cell to the right. To merge two '
                  'cells together, set the column width to 2. For 3, set 3. Default is 1. '
                  'Min 1. Max 20.',
        validators=[MaxValueValidator(20), MinValueValidator(1)]
    )
    content = blocks.RichTextBlock(features=base_rich_text_options + ['ul', 'ol'])


class Row(blocks.StreamBlock):
    cell = Cell()


class Table(blocks.StreamBlock):
    row = Row()


class AdvancedTableBlock(blocks.StructBlock):
    header = blocks.BooleanBlock(
        required=False,
        help_text='Display the first row as a header.',
    )
    column = blocks.BooleanBlock(
        required=False,
        help_text='Display the first column as a header.',
    )
    caption = blocks.CharBlock(
        required=False,
        help_text='A heading that identifies the overall topic of the table, and is useful for screen reader users',
    )

    table = Table()

    class Meta:
        template = 'wagtailpages/blocks/advanced_table_block.html'
