from django.apps import apps
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from wagtail import blocks
from wagtail.blocks import StructBlockValidationError

from foundation_cms.legacy_apps.wagtailpages.utils import get_locale_from_request

from ..blog.blog_topic import BlogPageTopic


class RecentBlogEntries(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
    )

    tag_filter = blocks.CharBlock(
        label="Filter by Tag",
        required=False,
        help_text="Test this filter at foundation.mozilla.org/blog/tags/",
    )

    topic_filter = blocks.ChoiceBlock(
        label="Filter by Topic",
        required=False,
        choices=BlogPageTopic.get_topics,
        help_text="Test this filter at foundation.mozilla.org/blog/topic/",
    )

    top_divider = blocks.BooleanBlock(
        required=False,
        help_text="Optional divider above content block.",
    )

    bottom_divider = blocks.BooleanBlock(
        required=False,
        help_text="Optional divider below content block.",
    )

    def clean(self, value):
        validation_errors = {}
        both_filters_error = ValidationError("Please provide either a Tag or a Topic, not both", code="invalid")
        no_filter_error = ValidationError("Please provide a Tag or a Topic", code="required")

        if value["tag_filter"] and value["topic_filter"]:
            validation_errors["tag_filter"] = both_filters_error
            validation_errors["topic_filter"] = both_filters_error

        if not value["tag_filter"] and not value["topic_filter"]:
            validation_errors["tag_filter"] = no_filter_error
            validation_errors["topic_filter"] = no_filter_error

        if validation_errors:
            raise StructBlockValidationError(validation_errors)

        return super().clean(value)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        BlogIndexPage = apps.get_model("wagtailpages.BlogIndexPage")
        locale = get_locale_from_request(context["request"])
        blog_page = BlogIndexPage.objects.filter(locale=locale).live().first()

        tag = value.get("tag_filter", False)
        topic = value.get("topic_filter", False)

        # default filter and query
        query_type = "tags"
        query = "mozilla"
        entries = []

        if tag:
            tag = slugify(tag)
            query = tag
            blog_page.extract_tag_information(tag)
        elif topic and topic != "All":
            query_type = "topic"
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

        # Update the href for the 'More from our blog' button
        blog_page_url = blog_page.get_url()
        url = f"{blog_page_url}{query_type}/{query}"
        context["more_entries_link"] = url

        # We only want to grab no more than the first 6 entries
        context["entries"] = entries[:6]

        # We only want to display the 'More from our blog' button if
        # there's more than 6 entries
        context["more_entries"] = len(entries) > 6

        # this data does not belong "on a root document" but is pulled for
        # transclusion in arbitrary pages, so don't try to figure out the
        # page hierarachy.
        context["root"] = None

        # Optional dividers
        divider_styles = []
        if value.get("top_divider"):
            divider_styles.append("div-top-thick pt-4")
        if value.get("bottom_divider"):
            divider_styles.append("div-bottom-thick pb-4")
        context["divider_styles"] = " ".join(divider_styles)

        return context

    class Meta:
        template = "wagtailpages/blocks/recent_blog_entries.html"
        icon = "site"
