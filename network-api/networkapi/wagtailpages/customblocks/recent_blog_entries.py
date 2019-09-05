import json

from wagtail.core import blocks
from networkapi.wagtailpages.models import IndexPage


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
    blogpage = IndexPage.objects.get(title="blog")

    title = blocks.CharBlock(
        required=True,
    )

    # Finds out which filter is in-use. If both are chosen, category is prioritized
    def tag_or_category(self):
        selection = self.tag_filter or self.category_filter
        if self.tag_filter and self.category_filter:
            selection = self.category_filter
            print("You've selected a category")
        return selection

    tag_filter = blocks.CharBlock(
        label='Filter by Tag',
        required=False,
        validator=tag_or_category
    )

    category_filter = blocks.ChoiceBlock(
        label='Filter by Category',
        required=False,
        choices=[
            ('all', 'All'),
            ('Mozilla Festival', 'Mozilla Festival'),
            ('Open Leadership & Events', 'Open Leadership & Events'),
            ('Internet Health', 'Internet Health'),
            ('Fellowships & Awards', 'Fellowships & Awards'),
            ('Advocacy', 'Advocacy'),
        ],
        validator=tag_or_category,
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

    def renderHTML(selection, self, value):
        context = {}

        # If tag_filter is chosen we want to load json response of entries by tag
        if selection is self.tag_filter:
            tag = value.get("tag_filter")
            response = f'./tags/{tag}/entries/?page=0&page_size=6'

        # If category_filter is chosen we want to load json response of entries by category
        if selection is self.category_filter:
            category = value.get("category_filter")
            response = f'./categories/{category}/entries/?page=0&page_size=6'

        # Load final json response to be used in template
        html = json.loads(response).get('html')
        context['htmlblock'] = html
        return context

    # Add optional dividers
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
