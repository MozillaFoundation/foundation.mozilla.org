from django.db import models
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from modelcluster import fields as cluster_fields
from wagtail import documents as wagtail_docs
from wagtail.documents import edit_handlers as docs_handlers
from wagtail.admin import edit_handlers
from wagtail.core import models as wagtail_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class ResearchDetailLink(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    research_detail_page = cluster_fields.ParentalKey(
        'ResearchDetailPage',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='research_links',
    )

    label = models.CharField(null=False, blank=False, max_length=50)

    url = models.URLField(null=False, blank=True)
    document = models.ForeignKey(
        wagtail_docs.get_document_model_string(),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    panels = [
        edit_handlers.HelpPanel(
            content=_(
                'Please provide an external link to the original source or upload a document and select it here. '
                'If you wish to provide both, please create two separate "research links"'
            )
        ),
        edit_handlers.FieldPanel('label'),
        edit_handlers.FieldPanel('url'),
        docs_handlers.DocumentChooserPanel('document'),
    ]

    def __str__(self):
        return self.label

    def clean(self):
        super().clean()
        if self.url and self.document:
            error_message = _('Please provide a URL or a document, not both.')
            raise exceptions.ValidationError(
                {'url': error_message, 'document': error_message},
                code='invalid',
            )
        elif not self.url and not self.document:
            error_message = _('Please provide a URL or a document.')
            raise exceptions.ValidationError(
                {'url': error_message, 'document': error_message},
                code='required',
            )


class ResearchDetailPage(foundation_metadata.FoundationMetadataPageMixin, wagtail_models.Page):
    parent_page_types = ['ResearchLibraryPage']

    content_panels = wagtail_models.Page.content_panels + [
        edit_handlers.InlinePanel('research_links', heading="Research links", min_num=1),
        edit_handlers.InlinePanel('research_authors', heading="Authors", min_num=1),
        edit_handlers.InlinePanel('related_topics', heading="Topics"),
        edit_handlers.InlinePanel('related_regions', heading="Regions"),
    ]
