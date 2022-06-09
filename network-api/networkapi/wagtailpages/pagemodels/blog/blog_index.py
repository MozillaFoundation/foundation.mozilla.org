from django.conf import settings
from django.db import models
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from wagtail.admin.edit_handlers import PageChooserPanel, InlinePanel
from wagtail.contrib.routable_page.models import route
from wagtail.core.models import Orderable as WagtailOrderable
from wagtail_localize.fields import SynchronizedField

from modelcluster.fields import ParentalKey
from networkapi.wagtailpages.utils import (
    titlecase,
    get_locale_from_request,
    get_default_locale,
)

from sentry_sdk import capture_exception, push_scope

from ..index import IndexPage
from .blog_topic import BlogPageTopic


class FeaturedBlogPages(WagtailOrderable, models.Model):
    page = ParentalKey(
        'wagtailpages.BlogIndexPage',
        related_name='featured_pages',
    )

    blog = models.ForeignKey(
        'wagtailpages.BlogPage',
        on_delete=models.CASCADE,
        related_name='+'
    )

    panels = [
        PageChooserPanel('blog', 'wagtailpages.BlogPage'),
    ]

    class Meta:
        ordering = ['sort_order']  # not automatically inherited!

    def __str__(self):
        return self.page.title + '->' + self.blog.title


class BlogIndexPage(IndexPage):
    """
    The blog index is specifically for blog pages,
    with additional logic to explore topics.
    """

    subpage_types = [
        'BlogPage'
    ]

    content_panels = IndexPage.content_panels + [
        InlinePanel(
            'featured_pages',
            label='Featured',
            help_text='Choose two blog pages to feature',
            min_num=0,
            max_num=2,
        )
    ]

    translatable_fields = IndexPage.translatable_fields + [
        SynchronizedField('featured_pages'),
    ]

    template = 'wagtailpages/blog_index_page.html'

    # superclass override
    def get_all_entries(self, locale):
        """
        Do we need to filter the featured blog entries
        out, so they don't show up twice?
        """
        if hasattr(self, 'filtered'):
            return super().get_all_entries(locale)

        featured = [
            entry.blog.get_translation(locale).pk for entry in self.featured_pages.all()
        ]

        return super().get_all_entries(locale).exclude(pk__in=featured)

    def filter_entries(self, entries, context):
        entries = super().filter_entries(entries, context)

        if context['filtered'] == 'topic':
            entries = self.filter_entries_for_topic(entries, context)
            context['total_entries'] = len(entries)

        return entries

    def filter_entries_for_topic(self, entries, context):

        topic = self.filtered.get('topic')

        # The following code first updates page share metadata when filtered by topic.
        # First, updating metadata that is not localized
        #
        # make sure we bypass "x results for Y"
        context['no_filter_ui'] = True

        # and that we don't show the primary tag/topic
        context['hide_classifiers'] = True

        # store the base topic name
        context['terms'] = [topic.name, ]

        # then explicitly set all the metadata that can be localized, making
        # sure to use the localized topic for those fields:
        locale = get_locale_from_request(context['request'])
        try:
            localized_topic = topic.get_translation(locale)
        except ObjectDoesNotExist:
            localized_topic = topic

        context['index_intro'] = localized_topic.intro
        context['index_title'] = titlecase(f'{localized_topic.name} {self.title}')

        if localized_topic.title:
            context['index_title'] = localized_topic.title

        # update seo fields
        self.set_seo_fields_from_topic(localized_topic)

        # This code is not efficient, but its purpose is to get us logs
        # that we can use to figure out what's going wrong more than
        # being efficient.
        #
        # See https://github.com/mozilla/foundation.mozilla.org/issues/6255
        #

        in_topics = []

        try:
            for entry in entries.specific():
                if hasattr(entry, 'topics'):
                    entry_topics = entry.topics.all()
                    try:
                        if topic in entry_topics:
                            in_topics.append(entry)
                    except Exception as e:
                        if settings.SENTRY_ENVIRONMENT is not None:
                            push_scope().set_extra(
                                'reason',
                                f'entry_topics has an iteration problem; {str(entry_topics)}'
                            )
                            capture_exception(e)

        except Exception as e:
            if settings.SENTRY_ENVIRONMENT is not None:
                push_scope().set_extra('reason', 'entries.specific threw')
                capture_exception(e)

        entries = in_topics

        return entries

    def set_seo_fields_from_topic(self, topic):
        if topic.title:
            setattr(self, 'seo_title', topic.title)
        elif topic.name:
            setattr(self, 'seo_title', topic.name)

        # If description not set, default to topic's "intro" text.
        # If "intro" is not set, use the foundation's default meta description.
        if topic.share_description:
            setattr(self, 'search_description', topic.share_description)
        elif topic.intro:
            setattr(self, 'search_description', topic.intro)

        # If the topic has a search image set, update page metadata.
        if topic.share_image:
            setattr(self, 'search_image_id', topic.share_image_id)

    # helper function to resolve topic slugs to actual objects
    def get_topic_object_for_slug(self, topic_slug):
        (DEFAULT_LOCALE, DEFAULT_LOCALE_ID) = get_default_locale()

        english_topics = BlogPageTopic.objects.filter(
            locale_id=DEFAULT_LOCALE_ID
        )

        # We can't use .filter for @property fields,
        # so we have to run through all topics =(
        for blog_page_topic in english_topics:

            if blog_page_topic.slug == topic_slug:
                topic_object = blog_page_topic
                break
        else:
            topic_object = None

        return topic_object

    # helper function for /topic/... subroutes
    def extract_topic_information(self, topic_slug):

        topic_object = self.get_topic_object_for_slug(topic_slug)

        if topic_object is None:
            raise ObjectDoesNotExist

        self.filtered = {
            'type': 'topic',
            'topic': topic_object
        }

    @route(r'^topic/(?P<topic>.+)/entries/')
    def generate_topic_entries_set_html(self, request, topic, *args, **kwargs):
        """
        JSON endpoint for getting a set of (pre-rendered) topic entries
        """
        try:
            self.extract_topic_information(topic)

        except ObjectDoesNotExist:
            return redirect(self.full_url)

        return self.generate_entries_set_html(request, *args, **kwargs)

    @route(r'^topic/(?P<topic>.+)/')
    def entries_by_topic(self, request, topic, *args, **kwargs):
        """
        If this page was called with `/topic/...` as suffix, extract
        the topic to filter prior to rendering this page. Only one
        topic can be specified (unlike tags)
        """
        try:
            self.extract_topic_information(topic)

        except ObjectDoesNotExist:
            return redirect(self.full_url)

        return IndexPage.serve(self, request, *args, **kwargs)

    @route(r'^search/')
    def search(self, request):
        """Render search results view."""
        return self.render(
            request,
            context_overrides={
                'index_title': 'Search',
                'entries': self.get_search_entries(),
            },
            template="wagtailpages/blog_index_search.html"
        )

    def get_search_entries(self):
        return self.get_entries()[:6]
