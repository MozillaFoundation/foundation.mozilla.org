from django.db import models
from modelcluster import fields as cluster_fields
from wagtail.core import models as wagtail_models
from wagtail.snippets import edit_handlers as snippet_handlers

from networkapi.wagtailpages import models as wagtailpage_models


class ResearchAuthorRelation(wagtail_models.Orderable):
    research_detail_page = cluster_fields.ParentalKey(
        'wagtailpages.ResearchDetailPage',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='research_authors',
    )
    author_profile = models.ForeignKey(
        'wagtailpages.Profile',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='authored_research',
    )

    panels = [
        snippet_handlers.SnippetChooserPanel('author_profile'),
    ]
