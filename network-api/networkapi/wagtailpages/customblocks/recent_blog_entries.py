from django.apps import apps
from wagtail.core import blocks

from django.template.defaultfilters import slugify


class RecentBlogEntries(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
    )

    tag_filter = blocks.CharBlock(
        label='Filter by Tag',
        required=False,
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
        ]
    )

    top_divider = blocks.BooleanBlock(
        required=False,
        help_text='Optional divider above content block.',
    )

    bottom_divider = blocks.BooleanBlock(
        required=False,
        help_text='Optional divider below content block.',
    )

    # TODO: add in validation so that if there are no tags or category
    #       filled in we don't allow the page to be saved, with a wagtail
    #       error indication what's wrong.

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        IndexPage = apps.get_model('wagtailpages.IndexPage')
        blogpage = IndexPage.objects.get(title="blog")

        tag = value.get("tag_filter", False)
        category = value.get("category_filter", False)

        # default filter and query
        type = "tags"
        query = "mozilla"
        entries = []

        # If tag_filter is chosen we want to load entries by tag and update the url(L76) accordingly
        if tag and not category:
            tag = slugify(tag)
            type = "tags"
            query = tag
            blogpage.extract_tag_information(tag)
            entries = blogpage.get_entries(context)

        '''
        If category_filter OR category_filter & tag_filter are chosen
        we want to load entries by category and update the url(L76) accordingly.
        Once we add validation(L38), we'll be able to remove the prioritization
        of category and instead notify the user they the must/can only choose one
        filter option.
        '''
        if category:
            category = slugify(category)
            type = "category"
            query = category
            blogpage.extract_category_information(category)
            entries = blogpage.get_entries(context)

        # This will update the href for the 'More from our blog' button
        url = f"/{blogpage.slug}/{type}/{query}"
        context['more_entries'] = url

        # We only want to grab no more than the first 6 entries
        context['entries'] = entries[0:6]

        # this data does not belong "on a root document" but is pulled for
        # transclusion in arbitrary pages, so don't try to figure out the
        # page hierarachy.
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
        template = 'wagtailpages/blocks/recent_blog_entries.html'
        icon = 'site'
