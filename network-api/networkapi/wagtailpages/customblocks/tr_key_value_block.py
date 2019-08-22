from wagtail.core import blocks


class TRKeyValueBlock(blocks.StructBlock):
    """
    This block is used for one-off page text blocks
    in a way that allows for "easy" translation using
    the wagtail-modeltranslation system of having the
    translations be part of the CMS experience.
    """

    key = blocks.CharBlock(
        required=True,
    )

    textblock = blocks.RichTextBlock(
        required=True,
        features=['bold', 'italic', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'link'],
    )

    class Meta:
        template = 'wagtailpages/blocks/tr_key_value_block.html'
