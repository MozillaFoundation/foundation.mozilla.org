import json
from django.apps import apps
from wagtail.core import blocks


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

    # TODO: add in validation so that if there are no tags or category
    #       filled in we don't allow the page to be saved, with a wagtail
    #       error indication what's wrong.


    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        IndexPage = apps.get_model('wagtailpages.IndexPage')
        blogpage = IndexPage.objects.get(title="blog")
        entries = []

        # If tag_filter is chosen we want to load json response of entries by tag
        if 'tag_filter' in value:
            tag = value.get("tag_filter")
            blogpage.extract_tag_information(tag)
            entries = blogpage.get_entries(context)

        # If category_filter is chosen we want to load json response of entries by category
        if 'category_filter' in value:
            category = value.get("category_filter")
            blogpage.extract_category_information(category)
            entries = blogpage.get_entries(context)

        context['entries'] = entries

        # this data does not belong "on a root document" but is pulled for
        # transclusion in arbitrary pages, so don't try to figure out the
        # page hierarachy.
        context['root'] = None

        return context

    class Meta:
        template = 'wagtailpages/blocks/recent_blog_entries.html'
        icon = 'site'