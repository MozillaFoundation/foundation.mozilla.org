import typing

from foundation_cms.legacy_apps.wagtailpages.pagemodels.profiles import Profile

if typing.TYPE_CHECKING:
    from django.db.models.query import QuerySet


def get_research_authors() -> "QuerySet[Profile]":
    """Filter a queryset of profiles to only those who are research authors."""
    return Profile.objects.filter(authored_research__isnull=False).distinct()
