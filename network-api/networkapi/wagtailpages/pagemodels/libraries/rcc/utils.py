import typing

from networkapi.wagtailpages.pagemodels.profiles import Profile

if typing.TYPE_CHECKING:
    from django.db.models.query import QuerySet


def get_rcc_authors() -> "QuerySet[Profile]":
    """Filter a queryset of profiles to only those who are authors of RCC articles."""
    return Profile.objects.filter(authored_rcc_articles__isnull=False).distinct()
