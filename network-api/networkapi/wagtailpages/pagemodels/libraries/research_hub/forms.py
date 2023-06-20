from django import forms
from django.utils.translation import pgettext_lazy

from networkapi.wagtailpages import utils
from networkapi.wagtailpages.pagemodels import profiles as profile_models
from networkapi.wagtailpages.pagemodels.libraries.research_hub import (
    detail_page,
    taxonomies,
)


def _get_author_options():
    author_profiles = utils.get_research_authors(profile_models.Profile.objects.all())
    author_profiles = utils.localize_queryset(author_profiles)
    return [(author_profile.id, author_profile.name) for author_profile in author_profiles]


def _get_topic_options():
    topics = taxonomies.ResearchTopic.objects.all()
    topics = utils.localize_queryset(topics)
    return [(topic.id, topic.name) for topic in topics]


def _get_region_options():
    regions = taxonomies.ResearchRegion.objects.all()
    regions = utils.localize_queryset(regions)
    return [(region.id, region.name) for region in regions]


def _get_year_options():
    dates = detail_page.ResearchDetailPage.objects.dates(
        "original_publication_date",
        "year",
        order="DESC",
    )
    year_options = [(date.year, date.year) for date in dates]
    empty_option = (
        "",
        pgettext_lazy("Option in a list of years", "Any"),
    )
    return [empty_option] + year_options


class ResearchLibraryPageFilterForm(forms.Form):
    topics = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "rh-checkbox"}),
        choices=_get_topic_options,
        label=pgettext_lazy("Filter form field label", "Topics"),
    )
    year = forms.ChoiceField(
        required=False,
        choices=_get_year_options,
        widget=forms.RadioSelect(attrs={"class": "rh-radio"}),
        label=pgettext_lazy("Filter form field label", "Publication Date"),
    )
    authors = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "rh-checkbox"}),
        choices=_get_author_options,
        label=pgettext_lazy("Filter form field label", "Authors"),
    )
    regions = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "rh-checkbox"}),
        choices=_get_region_options,
        label=pgettext_lazy("Filter form field label", "Regions"),
    )
