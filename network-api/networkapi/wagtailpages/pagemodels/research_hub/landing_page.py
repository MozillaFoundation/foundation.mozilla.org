from django.apps import apps
from django.db import models
from wagtail.core import models as wagtail_models
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages.pagemodels.research_hub import base as research_base


class ResearchLandingPage(research_base.ResearchHubBasePage):
    max_count = 1
    subpage_types = [
        'ResearchLibraryPage',
        'ResearchAuthorsIndexPage',
    ]

    intro = models.CharField(
        blank=True,
        max_length=250,
    )
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Image that will render at the top of the page.',
    )

    content_panels = wagtail_models.Page.content_panels + [
        FieldPanel('intro'),
        ImageChooserPanel('banner_image'),
        InlinePanel('featured_topics', heading="Featured Topics"),
    ]

    translatable_fields = [
        TranslatableField('title'),
        SynchronizedField('banner_image'),
        TranslatableField('intro'),
        TranslatableField('featured_topics'),
        # Promote tab fields
        SynchronizedField('slug'),
        TranslatableField('seo_title'),
        SynchronizedField('show_in_menus'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        ResearchLibraryPage = apps.get_model("wagtailpages", "ResearchLibraryPage")
        context['library_page'] = ResearchLibraryPage.objects.first()
        context['latest_research_detail_pages'] = self.get_latest_research_pages
        return context

    def get_latest_research_pages(self):
        active_locale = wagtail_models.Locale.get_active()

        ResearchDetailPage = apps.get_model('wagtailpages', 'ResearchDetailPage')
        research_detail_pages = ResearchDetailPage.objects.live()
        research_detail_pages = research_detail_pages.filter(locale=active_locale)
        research_detail_pages = research_detail_pages.order_by('-original_publication_date')
        research_detail_pages = research_detail_pages[:3]

        return research_detail_pages
