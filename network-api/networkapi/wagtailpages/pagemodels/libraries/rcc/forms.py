from django import forms
from django.utils.translation import pgettext_lazy

from networkapi.wagtailpages import utils
from networkapi.wagtailpages.pagemodels.libraries.rcc import taxonomies
from networkapi.wagtailpages.pagemodels.libraries.rcc import utils as rcc_utils


def _get_author_options():
    author_profiles = rcc_utils.get_rcc_authors()
    author_profiles = utils.localize_queryset(author_profiles).order_by("name")
    return [(author_profile.id, author_profile.name) for author_profile in author_profiles]


def _get_content_type_options():
    content_types = taxonomies.RCCContentType.objects.all()
    content_types = utils.localize_queryset(content_types)
    return [(content_type.id, content_type.name) for content_type in content_types]


def _get_curricular_area_options():
    curricular_areas = taxonomies.RCCCurricularArea.objects.all()
    curricular_areas = utils.localize_queryset(curricular_areas)
    return [(curricular_area.id, curricular_area.name) for curricular_area in curricular_areas]


def _get_topic_options():
    topics = taxonomies.RCCTopic.objects.all()
    topics = utils.localize_queryset(topics)
    return [(topic.id, topic.name) for topic in topics]


class RCCLibraryPageFilterForm(forms.Form):
    topics = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        choices=_get_topic_options,
        label=pgettext_lazy("Filter form field label", "Topics"),
    )
    curricular_areas = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        choices=_get_curricular_area_options,
        label=pgettext_lazy("Filter form field label", "Curricular Area"),
    )
    content_types = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        choices=_get_content_type_options,
        label=pgettext_lazy("Filter form field label", "Content Type"),
    )
    authors = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        choices=_get_author_options,
        label=pgettext_lazy("Filter form field label - Authors of RCC articles", "Contributors"),
    )
