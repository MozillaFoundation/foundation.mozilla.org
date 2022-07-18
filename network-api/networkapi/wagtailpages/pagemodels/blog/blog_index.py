from typing import TYPE_CHECKING, Union, Optional

from django import http
from django.conf import settings
from django.core import paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.shortcuts import redirect, get_object_or_404
from django.template import loader

from wagtail.admin.edit_handlers import PageChooserPanel, InlinePanel, FieldPanel
from wagtail.contrib.routable_page.models import route
from wagtail.core.models import Orderable as WagtailOrderable
from wagtail.core.models import Locale
from wagtail_localize.fields import SynchronizedField
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from sentry_sdk import capture_exception, push_scope

from networkapi.wagtailpages.models import Profile
from networkapi.wagtailpages.utils import (
    titlecase,
    get_locale_from_request,
    get_default_locale,
    localize_queryset,
)

from ..index import IndexPage
from .blog_topic import BlogPageTopic
from networkapi.wagtailpages.forms import BlogIndexPageForm


if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest, HttpResponse
    from wagtail.search.backends.database.fallback import DatabaseSearchResults


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


class FeaturedVideoPost(WagtailOrderable, models.Model):
    page = ParentalKey(
        'wagtailpages.BlogIndexPage',
        related_name='featured_video_post',
    )

    blog_page = models.ForeignKey(
        'wagtailpages.BlogPage',
        on_delete=models.CASCADE,
        related_name='+'
    )
    video_url = models.URLField(
        help_text='For YouTube: Go to your YouTube video and copy the URL '
                  'from your browsers navigation bar. '
                  'If this video is not for our YouTube channel, '
                  'please host it on Vimeo.'
                  'For Vimeo: Log into Vimeo using 1Password '
                  'and upload the desired video. '
                  'Then select the video and '
                  'click "Advanced", "Distribution", '
                  'and "Video File Links". Copy and paste the link here.',
        blank=False,
    )

    panels = [
        PageChooserPanel('blog_page', 'wagtailpages.BlogPage'),
        FieldPanel("video_url"),
    ]

    def __str__(self):
        return self.blog_page.title


class BlogIndexPage(IndexPage):
    """
    The blog index is specifically for blog pages,
    with additional logic to explore topics.
    """

    base_form_class = BlogIndexPageForm

    related_topics = ParentalManyToManyField(
        BlogPageTopic,
        help_text='Which topics would you like to feature on the page? '
                  'Please select a max of 7.',
        blank=True
    )

    subpage_types = [
        'BlogPage'
    ]

    content_panels = IndexPage.content_panels + [
        InlinePanel(
            'featured_pages',
            label='Featured',
            help_text='Choose five blog pages to feature',
            min_num=5,
            max_num=5,
        ),
        InlinePanel(
            'featured_video_post',
            label='Featured Video Post',
            help_text='Choose a blog page with video to feature',
            min_num=0,
            max_num=1,
        ),
        FieldPanel('related_topics', widget=CheckboxSelectMultiple)
    ]

    translatable_fields = IndexPage.translatable_fields + [
        SynchronizedField('featured_pages'),
        SynchronizedField('featured_video_post'),
    ]

    template = 'wagtailpages/blog_index_page.html'

    def get_context(self, request):
        context = super().get_context(request)
        context["related_topics"] = self.get_related_topics()
        return context

    # Superclass override
    def get_entries(self, context=dict()):
        """
        Get list of index entries/child pages.

        We filter the featured blog posts, because they are displayed separately.
        """
        entries = super().get_entries(context=context)

        if not hasattr(self, 'filtered'):
            featured = [
                feature.blog.localized.pk for feature in self.featured_pages.all()
            ]
            featured.extend([
                feature.blog_page.localized.pk for feature in self.featured_video_post.all()
            ])
            entries = entries.exclude(pk__in=featured)

        return entries

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

        # TODO: REMOVE all of the following. The filtering should not be done in Python
        #       at all, but rather in the database. There should be no need to iterate.
        #       See also: https://stackoverflow.com/questions/4507893/django-filter-many-to-many-with-contains

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

    @route(r'^authors/$')
    def blog_author_index(self, request: 'HttpRequest', *args, **kwargs) -> 'HttpResponse':
        """If the page is called with /authors/, render a list of Profile
        objects that have been referenced in blog pages.

        Args:
            request (HttpRequest)
        Returns:
            HttpResponse: Response containing new template and a queryset of all
            Profiles used as blog authors.
        """
        author_profiles = Profile.objects.all()
        author_profiles = author_profiles.filter_blog_authors()
        author_profiles = localize_queryset(author_profiles)

        return self.render(
            request,
            context_overrides={
                'title': 'Blog authors',
                'author_profiles': author_profiles
            },
            template="wagtailpages/blog_author_index_page.html"
        )

    @route(r'^authors/(?P<profile_slug>.+)/', name='blog-author-detail')
    def blog_author_detail(self, request: 'HttpRequest', profile_slug: str, *args, **kwargs) -> 'HttpResponse':
        """If the page is /blog/authors/[profile_slug] is requested, render a template
        showing the blog authors profile data

        Args:
            request (HttpRequest)
            profile_slug (str): The value of Profile.slug

        Returns:
            HttpResponse: Response containing new template and Profile data for
            the profile_slug queried.
        """
        author_profile = get_object_or_404(Profile, slug=profile_slug)
        return self.render(
            request,
            context_overrides={
                'author': author_profile,
                'page': self,
            },
            template="wagtailpages/blog_author_detail_page.html"
        )

    @route(r'^search/$')
    def search(self, request: 'HttpRequest') -> 'HttpResponse':
        """Render search results view."""

        query = request.GET.get('q', '')

        entries = self.get_search_entries(query=query)

        context_overrides = {
            'index_title': 'Search',
            'entries': entries[:self.page_size],
            'has_more': entries.count() > self.page_size,
            'query': query,
        }

        return self.render(
            request,
            context_overrides=context_overrides,
            template='wagtailpages/blog_index_search.html',
        )

    @route(r'^search/entries/$')
    def search_entries(self, request: 'HttpRequest') -> 'HttpResponse':
        query: str = request.GET.get('q', '')

        page_parameter: str = request.GET.get('page', '')
        if not page_parameter:
            return http.HttpResponseBadRequest(reason='No page number defined.')

        try:
            page_number: int = int(page_parameter)
        except ValueError:
            return http.HttpResponseBadRequest(reason='Page number is not an integer.')

        entries = self.get_search_entries(query=query)

        entries_paginator = paginator.Paginator(
            object_list=entries,
            per_page=self.page_size,
            allow_empty_first_page=False,
        )
        try:
            # JS is using 0 based page number, but the paginator is using 1 based.
            entries_page = entries_paginator.page(page_number + 1)
        except paginator.EmptyPage:
            return http.HttpResponseNotFound(reason='No entries for this page number.')

        entries_html = loader.render_to_string(
            'wagtailpages/fragments/blog_search_item_loop.html',
            context={'entries': entries_page},
            request=request
        )

        return http.JsonResponse(
            data={
                'entries_html': entries_html,
                'has_next': entries_page.has_next(),
            }
        )

    def get_search_entries(
        self,
        query: str = '',
        locale: Optional[Locale] = None,
    ) -> Union['QuerySet', 'DatabaseSearchResults']:
        locale = locale or Locale.get_active()
        entries = self.get_all_entries(locale=locale).specific()
        if query:
            entries = entries.search(
                query,
                partial_match=False,
                order_by_relevance=True,
            )
        return entries

    def get_related_topics(self):
        related_topics = self.related_topics.all()
        return related_topics
