from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from wagtail.contrib.routable_page.models import route

from networkapi.wagtailpages.utils import titlecase

from ..index import IndexPage
from .blog_category import BlogPageCategory


class BlogIndexPage(IndexPage):
    """
    The blog index is specifically for blog pages,
    with additional logic to explore categories.
    """

    subpage_types = [
        'BlogPage',
    ]

    template = 'wagtailpages/index_page.html'

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
