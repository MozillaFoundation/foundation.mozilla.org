from wagtail.core import models as wagtail_models
from django.apps import apps

from networkapi.wagtailpages import utils
from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class ResearchHubBasePage(
    foundation_metadata.FoundationMetadataPageMixin,
    wagtail_models.Page,
):

    def get_context(self, request):
        context = super().get_context(request)
        context = utils.set_main_site_nav_information(self, context, "Homepage")
        return context

    def get_breadcrumbs(self, include_self=False):
        ResearchLandingPageModel = apps.get_model("wagtailpages", "ResearchLandingPage")
        research_landing_page = self.get_ancestors().type(ResearchLandingPageModel).first()
        page_ancestors = self.get_ancestors(include_self).descendant_of(research_landing_page, True)
        breadcrumb_list = [{"title": ancestor_page.title, "url": ancestor_page.url}
                           for ancestor_page in page_ancestors]

        return breadcrumb_list

    class Meta:
        abstract = True
