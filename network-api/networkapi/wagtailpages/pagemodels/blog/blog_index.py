from django.conf import settings
from django.db import models
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from wagtail.admin.edit_handlers import PageChooserPanel, InlinePanel
from wagtail.contrib.routable_page.models import route
from wagtail.core.models import Orderable as WagtailOrderable

from modelcluster.fields import ParentalKey
from networkapi.wagtailpages.utils import titlecase

from sentry_sdk import capture_exception, push_scope

from ..index import IndexPage
from .blog_category import BlogPageCategory


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
    with additional logic to explore categories.
    """

    subpage_types = [
        'BlogPage'
    ]

    content_panels = IndexPage.content_panels + [
        InlinePanel(
            'featured_pages',
            label='Featured',
            help_text='Choose two blog pages to feature',
            min_num=2,
            max_num=2,
        )
    ]

    template = 'wagtailpages/blog_index_page.html'

    def get_all_entries(self):
        """
        Do we need to filter the featured blog entries
        out, so they don't show up twice?
        """
        if hasattr(self, 'filtered'):
            return super().get_all_entries()

        featured = [entry.blog.pk for entry in self.featured_pages.all()]
        return super().get_all_entries().exclude(pk__in=featured)

    def filter_entries(self, entries, context):
        entries = super().filter_entries(entries, context)

        if context['filtered'] == 'category':
            entries = self.filter_entries_for_category(entries, context)
            context['total_entries'] = len(entries)

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

        # This code is not efficient, but its purpose is to get us logs
        # that we can use to figure out what's going wrong more than
        # being efficient.
        #
        # See https://github.com/mozilla/foundation.mozilla.org/issues/6255
        #

        in_category = []

        try:
            for entry in entries.specific():
                if hasattr(entry, 'category'):
                    entry_categories = entry.category.all()
                    try:
                        if category in entry_categories:
                            in_category.append(entry)
                    except Exception as e:
                        if settings.SENTRY_ENVIRONMENT is not None:
                            push_scope().set_extra(
                                'reason',
                                f'entry_categories has an iteration problem; {str(entry_categories)}'
                            )
                            capture_exception(e)

        except Exception as e:
            if settings.SENTRY_ENVIRONMENT is not None:
                push_scope().set_extra('reason', 'entries.specific threw')
                capture_exception(e)

        entries = in_category

        # Original code is as follows:
        #
        # entries = [
        #     entry
        #     for
        #     entry in entries.specific()
        #     if
        #     hasattr(entry, 'category')
        #     and
        #     category in entry.category.all()
        # ]

        return entries

    # helper function to resolve category slugs to actual objects
    def get_category_object_for_slug(self, category_slug):
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
