from django.apps import apps
from wagtail.core import models as wagtail_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class ResearchLibraryPage(foundation_metadata.FoundationMetadataPageMixin, wagtail_models.Page):
    max_count = 1
    parent_page_types = ['ResearchLandingPage']
    subpage_types = ['ResearchDetailPage']

    def get_context(self, request):
        context = super().get_context(request)

        ResearchDetailPage = apps.get_model('wagtailpages', 'ResearchDetailPage')
        active_locale = wagtail_models.Locale.get_active()
        context['research_detail_pages'] = ResearchDetailPage.objects.filter(locale=active_locale)

        return context
