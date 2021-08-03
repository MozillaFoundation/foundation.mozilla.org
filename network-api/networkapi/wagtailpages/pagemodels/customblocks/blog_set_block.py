from wagtail.core import blocks
from wagtail.core.blocks import PageChooserBlock


class BlogSetBlock(blocks.StructBlock):
    title = blocks.CharBlock()

    top_divider = blocks.BooleanBlock(
        required=False,
        help_text='Optional divider above content block.',
    )

    bottom_divider = blocks.BooleanBlock(
        required=False,
        help_text='Optional divider below content block.',
    )

    blog_pages = blocks.ListBlock(PageChooserBlock(
        target_model='wagtailpages.BlogPage'
    ))

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        context['entries'] = value.get("blog_pages", list())
        context['more_entries'] = False
        context['root'] = None

        # Optional dividers
        divider_styles = []
        if value.get("top_divider"):
            divider_styles.append('div-top-thick pt-4')
        if value.get("bottom_divider"):
            divider_styles.append('div-bottom-thick pb-4')
        context['divider_styles'] = ' '.join(divider_styles)

        return context

    class Meta:
        icon = 'grip'
        template = 'wagtailpages/blocks/blog_set_block.html'
