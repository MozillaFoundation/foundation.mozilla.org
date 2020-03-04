import re

from django.apps import apps
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template import loader

from taggit.models import Tag

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from .mixin.foundation_metadata import FoundationMetadataPageMixin

from networkapi.wagtailpages.utils import (
    set_main_site_nav_information,
    get_page_tree_information,
    titlecase
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

    def get_all_entries(self):
        """
        Get all (live) child entries, ordered "newest first"
        """
        return self.get_children().live().public().order_by('-first_published_at')

    def get_entries(self, context=dict()):
        """
        Get all child entries, filtered down if required based on
        the `self.filtered` field being set or not.
        """
        entries = self.get_all_entries()
        if hasattr(self, 'filtered'):
            entries = self.filter_entries(entries, context)
        return entries

    def filter_entries(self, entries, context):
        filter_type = self.filtered.get('type')
        context['filtered'] = filter_type

        if filter_type == 'tags':
            entries = self.filter_entries_for_tag(entries, context)

        if filter_type == 'category':
            entries = self.filter_entries_for_category(entries, context)

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

    def filter_entries_for_category(self, entries, context):
        category = self.filtered.get('category')

        # make sure we bypass "x results for Y"
        context['no_filter_ui'] = True

        # and that we don't show the primary tag/category
        context['hide_classifiers'] = True

        # explicitly set the index page title and intro
        context['index_title'] = titlecase(f'{category.name} {self.title}')
        context['index_intro'] = category.intro

        # and then the filtered content
        context['terms'] = [category.name, ]
        entries = [
            entry
            for
            entry in entries.specific()
            if
            hasattr(entry, 'category')
            and
            category in entry.category.all()
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
            page = int(request.GET['page'])

        page_size = self.page_size
        if 'page_size' in request.GET:
            page_size = int(request.GET['page_size'])

        start = page * page_size
        end = start + page_size
        entries = self.get_entries()
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

    """
    category routes
    """

    # helper function to resolve category slugs to actual objects
    def get_category_object_for_slug(self, category_slug):
        # FIXME: this should not need to be an app consult
        BlogPageCategory = apps.get_model('wagtailpages', 'BlogPageCategory')

        # We can't use .filter for @property fields,
        # so we have to run through all categories =(
        for bpc in BlogPageCategory.objects.all():
            if bpc.slug == category_slug:
                category_object = bpc
                break
        else:
            category_object = None

        return category_object

    # helper function for /category/... subroutes
    def extract_category_information(self, category_slug):
        category_object = self.get_category_object_for_slug(category_slug)

        if category_object is None:
            raise ObjectDoesNotExist

        self.filtered = {
            'type': 'category',
            'category': category_object
        }

    @route(r'^category/(?P<category>.+)/entries/')
    def generate_category_entries_set_html(self, request, category, *args, **kwargs):
        """
        JSON endpoint for getting a set of (pre-rendered) category entries
        """
        try:
            self.extract_category_information(category)

        except ObjectDoesNotExist:
            return redirect(self.full_url)

        return self.generate_entries_set_html(request, *args, **kwargs)

    @route(r'^category/(?P<category>.+)/')
    def entries_by_category(self, request, category, *args, **kwargs):
        """
        If this page was called with `/category/...` as suffix, extract
        the category to filter prior to rendering this page. Only one
        category can be specified (unlike tags)
        """
        try:
            self.extract_category_information(category)

        except ObjectDoesNotExist:
            return redirect(self.full_url)

        return IndexPage.serve(self, request, *args, **kwargs)
