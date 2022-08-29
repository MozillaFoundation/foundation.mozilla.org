from django.apps import apps
from django.template.defaultfilters import slugify

from wagtail.core import blocks

from networkapi.wagtailpages.utils import get_locale_from_request
from ..blog.blog_topic import BlogPageTopic


class RecentBlogEntries(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
    )

    tag_filter = blocks.CharBlock(
        label='Filter by Tag',
        required=False,
        help_text='Test this filter at foundation.mozilla.org/blog/tags/',
    )

    topic_filter = blocks.ChoiceBlock(
        label='Filter by Topic',
        required=False,
        choices=BlogPageTopic.get_topics(),
        help_text='Test this filter at foundation.mozilla.org/blog/topic/',
    )

    top_divider = blocks.BooleanBlock(
        required=False,
        help_text='Optional divider above content block.',
    )

    bottom_divider = blocks.BooleanBlock(
        required=False,
        help_text='Optional divider below content block.',
    )

    # TODO: add in validation so that if there are no tags or topic
    #       filled in we don't allow the page to be saved, with a wagtail
    #       error indication what's wrong.

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        BlogIndexPage = apps.get_model('wagtailpages.BlogIndexPage')
        locale = get_locale_from_request(context['request'])
        blog_page = BlogIndexPage.objects.get(title__iexact="blog", locale=locale)

        tag = value.get("tag_filter", False)
        topic = value.get("topic_filter", False)

        # default filter and query
        type = "tags"
        query = "mozilla"
        entries = []

        # If only tag_filter is chosen we want to load entries by tag and update the url accordingly
        if tag and not topic:
            tag = slugify(tag)
            query = tag
            blog_page.extract_tag_information(tag)
            entries = blog_page.get_entries(context)

        '''
        If topic_filter is chosen at all, we want to load entries by topic and
        update the url accordingly. Once we add validation, we'll be able to remove
        the prioritization of topic and instead notify the user that they must/can
        only choose one filter option.
        '''
        if topic and topic != "All":
            type = "topic"
            query = slugify(topic)
            try:
                # verify this topic exists, and set up a filter for it
                topic_object = BlogPageTopic.objects.get(name=topic, locale=locale)
                blog_page.extract_topic_information(topic_object.slug)
            except BlogPageTopic.DoesNotExist:
                # do nothing
                pass

        # get the entries based on prefiltering
        entries = blog_page.get_entries(context)

        # Updates the href for the 'More from our blog' button
        url = f"/{blog_page.slug}/{type}/{query}"
        context['more_entries_link'] = url

        # We only want to grab no more than the first 6 entries
        context['entries'] = entries[0:6]

        # We only want to display the 'More from our blog' button if
        # there's more than 6 entries
        context['more_entries'] = len(entries) > 6

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
