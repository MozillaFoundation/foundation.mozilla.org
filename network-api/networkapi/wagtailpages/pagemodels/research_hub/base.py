from django.apps import apps

from networkapi.wagtailpages.pagemodels.base import BasePage


class ResearchHubBasePage(BasePage):
    def get_breadcrumbs(self, include_self=False):
        ResearchLandingPageModel = apps.get_model("wagtailpages", "ResearchLandingPage")
        research_landing_page = self.get_ancestors().type(ResearchLandingPageModel).first()
        page_ancestors = self.get_ancestors(include_self).descendant_of(research_landing_page, True)
        breadcrumb_list = [
            {"title": ancestor_page.title, "url": ancestor_page.url} for ancestor_page in page_ancestors
        ]

        return breadcrumb_list

    class Meta:
        abstract = True
