import re

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.http import JsonResponse
from django.template import loader

from taggit.models import Tag

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page, Locale
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from wagtail_localize.fields import SynchronizedField, TranslatableField

from .mixin.foundation_metadata import FoundationMetadataPageMixin

from networkapi.wagtailpages.utils import (
    set_main_site_nav_information,
    get_page_tree_information,
    get_locale_from_request,
)


class IndexPage(FoundationMetadataPageMixin, RoutablePageMixin, Page):
    """
    This is a page type for creating "index" pages that
    can show cards for all their child content.
    E.g. a page that list "all blog posts" under it,
    or "all the various campaigns", etc.
    """

    header = models.CharField(
        max_length=250,
        blank=True
    )

    intro = models.CharField(
        max_length=250,
        blank=True,
        help_text='Intro paragraph to show in hero cutout box'
    )

    DEFAULT_PAGE_SIZE = 12

    PAGE_SIZES = (
        (4, '4'),
        (8, '8'),
        (DEFAULT_PAGE_SIZE, str(DEFAULT_PAGE_SIZE)),
        (24, '24'),
    )

    page_size = models.IntegerField(
        choices=PAGE_SIZES,
        default=DEFAULT_PAGE_SIZE,
        help_text='The number of entries to show by default, and per incremental load'
    )

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        FieldPanel('intro'),
        FieldPanel('page_size'),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField('slug'),
        TranslatableField('seo_title'),
        SynchronizedField('show_in_menus'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
        # Content tab fields
        TranslatableField('title'),
        TranslatableField('intro'),
        TranslatableField('header'),
        SynchronizedField('page_size'),
    ]

    def get_context(self, request):
        # bootstrap the render context
        context = super().get_context(request)
        context = set_main_site_nav_information(self, context, 'Homepage')
        context = get_page_tree_information(self, context)

        # perform entry pagination and (optional) filterin
        entries = self.get_entries(context)
        context['has_more'] = self.page_size < len(entries)
        context['entries'] = entries[0:self.page_size]
        return context

    def get_cache_key(self, locale):
        return f'index_items_{self.slug}_{locale}'

    def clear_index_page_cache(self, locale):
        cache.delete(self.get_cache_key(locale))

    def get_all_entries(self, locale):
        """
        Get all (live) child entries, ordered "newest first",
        ideally from cache, or "anew" if the cache expired.
        """
        cache_key = self.get_cache_key(locale)
        child_set = cache.get(cache_key)

        if child_set is None:
            child_set = self.get_children().live().public().order_by('-first_published_at', 'title')
            cache.set(cache_key, child_set, settings.INDEX_PAGE_CACHE_TIMEOUT)

        return child_set

    def get_entries(self, context=dict()):
        """
        Get all child entries, filtered down if required based on
        the `self.filtered` field being set or not.
        """
        DEFAULT_LANGUAGE_CODE = settings.LANGUAGE_CODE
        DEFAULT_LOCALE = Locale.objects.get(language_code=DEFAULT_LANGUAGE_CODE)

        if 'request' in context:
            locale = get_locale_from_request(context['request'])
        else:
            locale = DEFAULT_LOCALE

        entries = self.get_all_entries(locale)

        if hasattr(self, 'filtered'):
            entries = self.filter_entries(entries, context)

        return entries

    def filter_entries(self, entries, context):
        filter_type = self.filtered.get('type')
        context['filtered'] = filter_type

        if filter_type == 'tags':
            entries = self.filter_entries_for_tag(entries, context)

        context['total_entries'] = len(entries)
        return entries

    def filter_entries_for_tag(self, entries, context):
        """
        Realise the 'entries' queryset and filter it for tags presences.
        We need to perform this realisation because there is no guarantee
        that all children for this IndexPage in fact have a `tags` field,
        so in order to test this each entry needs to be "cast" into its
        specific model before we can test for whether i) there are tags
        to work with and then ii) those tags match the specified ones.
        """
        terms = self.filtered.get('terms')

        # "unsluggify" all terms. Note that we cannot use list comprehension,
        # as not all terms might be real tags, and list comprehension cannot
        # be made to ignore throws.
        context['terms'] = list()
        for term in terms:
            try:
                tag = Tag.objects.get(slug=term)
                context['terms'].append(str(tag))
            except Tag.DoesNotExist:
                # ignore non-existent tags
                pass

        entries = [
            entry
            for
            entry in entries.specific()
            if
            hasattr(entry, 'tags')
            and not
            # Determine whether there is any overlap between 'all tags' and
            # the tags specified. This effects ANY matching (rather than ALL).
            set([tag.slug for tag in entry.tags.all()]).isdisjoint(terms)
        ]

        return entries

    """
    Sub routes
    """

    @route('^entries/')
    def generate_entries_set_html(self, request, *args, **kwargs):
        """
        JSON endpoint for getting a set of (pre-rendered) entries
        """

        page = 1
        if 'page' in request.GET:
            try:
                page = int(request.GET['page'])
            except ValueError:
                pass

        page_size = self.page_size
        if 'page_size' in request.GET:
            try:
                page_size = int(request.GET['page_size'])
            except ValueError:
                pass

        start = page * page_size
        end = start + page_size
        entries = self.get_entries()

        # Exclude model types if data-exclude="" has a value in the template
        if 'exclude' in request.GET:
            try:
                # Try to get the content type. Then get the model_class.
                # This allows us to say "exclude 'publicationpage'" and get the model
                # by it's sting name without the AppName.
                ct = ContentType.objects.get(model=request.GET.get("exclude").lower())
                not_model = ct.model_class()
                entries = entries.not_type(not_model)
            except ContentType.DoesNotExist:
                pass

        has_next = end < len(entries)

        hide_classifiers = False
        if hasattr(self, 'filtered'):
            if self.filtered.get('type') == 'category':
                hide_classifiers = True

        html = loader.render_to_string(
            'wagtailpages/fragments/entry_cards.html',
            context={
                'entries': entries[start:end],
                'hide_classifiers': hide_classifiers
            },
            request=request
        )

        return JsonResponse({
            'entries_html': html,
            'has_next': has_next,
        })

    """
    tag routes
    """

    # helper function for /tags/... subroutes
    def extract_tag_information(self, tag):
        terms = list(filter(None, re.split('/', tag)))
        self.filtered = {
            'type': 'tags',
            'terms': terms
        }

    @route(r'^tags/(?P<tag>.+)/entries/')
    def generate_tagged_entries_set_html(self, request, tag, *args, **kwargs):
        """
        JSON endpoint for getting a set of (pre-rendered) tagged entries
        """
        self.extract_tag_information(tag)
        return self.generate_entries_set_html(request, *args, **kwargs)

    @route(r'^tags/(?P<tag>.+)/')
    def entries_by_tag(self, request, tag, *args, **kwargs):
        """
        If this page was called with `/tags/...` as suffix, extract
        the tags to filter prior to rendering this page. Multiple
        tags are specified as subpath: `/tags/tag1/tag2/...`
        """
        self.extract_tag_information(tag)
        return IndexPage.serve(self, request, *args, **kwargs)
