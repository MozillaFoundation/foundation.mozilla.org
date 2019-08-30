from wagtail.core import blocks


class PulseProjectQueryValue(blocks.StructValue):
    @property
    def size(self):
        max_number_of_results = self['max_number_of_results']
        return '' if max_number_of_results <= 0 else max_number_of_results

    @property
    def rev(self):
        # The default API behaviour is newest-first, so the "rev" attribute
        # should only have an attribute value when oldest-first is needed.
        newest_first = self['newest_first']
        return True if newest_first else ''


class RecentBlogEntries(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
    )

    tag_filter = blocks.CharBlock(
        help_text='Test your search at mozillapulse.org/tags',
        label='Filter by Tag',
        required=False,
    )

    direct_link = blocks.BooleanBlock(
        default=False,
        label='Direct link',
        help_text='Checked: user goes to project link. Unchecked: user goes to pulse entry',
        required=False,
    )

    top_divider = blocks.BooleanBlock(
        required=False,
        help_text='Optional divider above content block.',
    )
    bottom_divider = blocks.BooleanBlock(
        required=False,
        help_text='Optional divider below content block.',
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        divider_styles = []
        if value.get("top_divider"):
            divider_styles.append('div-top')
        if value.get("bottom_divider"):
            divider_styles.append('div-bottom')
        context['divider_styles'] = ' '.join(divider_styles)
        return context

    class Meta:
        template = 'wagtailpages/blocks/recent_blog_entries.html'
        icon = 'site'
        value_class = PulseProjectQueryValue
