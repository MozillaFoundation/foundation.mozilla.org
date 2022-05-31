from django.db import models
from django.core import exceptions
from modelcluster import fields as cluster_fields
from wagtail import documents as wagtail_docs
from wagtail import images as wagtail_images
from wagtail.documents import edit_handlers as docs_handlers
from wagtail.admin import edit_handlers
from wagtail.core import fields as wagtail_fields
from wagtail.core import models as wagtail_models
from wagtail.images import edit_handlers as image_handlers
from wagtail.search import index
from wagtail_localize import fields as localize_fields

from networkapi.wagtailpages.pagemodels.customblocks.base_rich_text_options import base_rich_text_options
from networkapi.wagtailpages.pagemodels.research_hub import base as research_base
from networkapi.wagtailpages.pagemodels.research_hub import authors_index


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
            content=(
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
            error_message = 'Please provide either a URL or a document, not both.'
            raise exceptions.ValidationError(
                {'url': error_message, 'document': error_message},
                code='invalid',
            )
        elif not self.url and not self.document:
            error_message = 'Please provide a URL or a document.'
            raise exceptions.ValidationError(
                {'url': error_message, 'document': error_message},
                code='required',
            )

    def get_url(self):
        if self.url:
            return self.url
        elif self.document:
            return self.document.url


class ResearchDetailPage(research_base.ResearchHubBasePage):
    parent_page_types = ['ResearchLibraryPage']

    cover_image = models.ForeignKey(
        wagtail_images.get_image_model_string(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text=(
            'Select a cover image for this research. '
            'The cover image is displayed on the detail page and all research listings.'
        ),
    )
    original_publication_date = models.DateField(
        null=True,
        blank=True,
        help_text='When was the research (not this page) originally published?'
    )
    introduction = models.CharField(
        null=False,
        blank=True,
        max_length=300,
        help_text=(
            'Provide a short blurb about the research '
            'that will be displayed on listing pages and search results.'
        )
    )
    overview = wagtail_fields.RichTextField(
        null=False,
        blank=True,
        features=base_rich_text_options,
        help_text=(
            'Provide an overview about the reseach. '
            'This can be an excerpt from or the executive summary of the original paper.'
        )
    )
    collaborators = models.TextField(
        null=False,
        blank=True,
        help_text='List all contributors that are not the project leading authors.'
    )

    content_panels = wagtail_models.Page.content_panels + [
        image_handlers.ImageChooserPanel('cover_image'),
        edit_handlers.InlinePanel('research_links', heading="Research links", min_num=1),
        edit_handlers.FieldPanel('original_publication_date'),
        edit_handlers.FieldPanel('introduction'),
        edit_handlers.FieldPanel('overview', classname='full'),
        edit_handlers.InlinePanel('research_authors', heading="Authors", min_num=1),
        edit_handlers.FieldPanel('collaborators'),
        edit_handlers.InlinePanel('related_topics', heading="Topics"),
        edit_handlers.InlinePanel('related_regions', heading="Regions"),
    ]

    translatable_fields = [
        localize_fields.TranslatableField('title'),
        localize_fields.SynchronizedField('slug'),
        localize_fields.SynchronizedField('cover_image'),
        localize_fields.SynchronizedField('original_publication_date', overridable=False),
        localize_fields.TranslatableField('introduction'),
        localize_fields.TranslatableField('overview'),
        localize_fields.TranslatableField('research_authors'),
        # Collaborators is translatable incase of connecting words like "and"
        localize_fields.TranslatableField('collaborators'),
        localize_fields.TranslatableField('related_topics'),
        localize_fields.TranslatableField('related_regions'),
    ]

    search_fields = wagtail_models.Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('overview'),
        index.SearchField('collaborators'),
        index.FilterField('original_publication_date'),  # For sorting
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["breadcrumbs"] = self.get_breadcrumbs()
        context["authors_index"] = authors_index.ResearchAuthorsIndexPage.objects.first()
        return context

    def get_research_author_names(self):
        return [
            ra.author_profile.name
            for ra in self.research_authors.all()
        ]

    def get_related_topic_names(self):
        return [
            rt.research_topic.name
            for rt in self.related_topics.all()
        ]

    def get_banner(self):
        return self.get_parent().specific.get_banner()
