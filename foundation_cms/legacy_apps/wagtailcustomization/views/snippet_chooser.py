from wagtail.admin.forms.choosers import (
    BaseFilterForm,
    CollectionFilterMixin,
    SearchFilterMixin,
)
from wagtail.admin.views.generic.chooser import (
    ChooseResultsViewMixin,
    ChooseViewMixin,
    CreationFormMixin,
)
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.models import CollectionMember, Locale, TranslatableMixin
from wagtail.search.index import class_is_indexed
from wagtail.snippets.views.chooser import BaseSnippetChooseView


class DefaultLocaleSnippetChooseView(ChooseViewMixin, CreationFormMixin, BaseSnippetChooseView):
    """
    BaseChooseView with LocaleFilterMixin excluded as we don't want to show language
    filter in the snippet chooser.

    See wagtail.admin.views.generic.chooser.BaseChooseView for original implementation.
    """

    def get_object_list(self):
        if not issubclass(self.model_class, TranslatableMixin):
            return super().get_object_list()

        return super().get_object_list().filter(locale__id=Locale.get_default().id)

    # Identical to get_filter_form_class() in BaseChooseView but with LocaleFilterMixin excluded.
    # See https://github.com/wagtail/wagtail/blob/v4.1.6/wagtail/admin/views/generic/chooser.py#L103C1-L123C1
    def get_filter_form_class(self):
        if self.filter_form_class:
            return self.filter_form_class
        else:
            bases = [BaseFilterForm]
            if self.model_class:
                if class_is_indexed(self.model_class):
                    bases.insert(0, SearchFilterMixin)
                if issubclass(self.model_class, CollectionMember):
                    bases.insert(0, CollectionFilterMixin)

            return type(
                "FilterForm",
                tuple(bases),
                {},
            )


class DefaultLocaleSnippetChooseResultsView(ChooseResultsViewMixin, CreationFormMixin, BaseSnippetChooseView):
    def get_object_list(self):
        if not issubclass(self.model_class, TranslatableMixin):
            return super().get_object_list()

        return super().get_object_list().filter(locale__id=Locale.get_default().id)


class DefaultLocaleSnippetChooserViewSet(ChooserViewSet):
    choose_view_class = DefaultLocaleSnippetChooseView
    choose_results_view_class = DefaultLocaleSnippetChooseResultsView
