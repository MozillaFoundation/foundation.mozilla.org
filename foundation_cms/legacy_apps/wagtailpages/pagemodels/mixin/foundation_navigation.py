from wagtail.models import Site

from foundation_cms.core.models.home_page import HomePage as RedesignHomePage
from foundation_cms.legacy_apps.wagtailpages import utils


class FoundationNavigationPageMixin:
    def get_context(self, request):

        context = super().get_context(request)

        site = Site.find_for_request(request)
        site_root = site.root_page.specific

        if isinstance(site_root, RedesignHomePage):
            homepage_type = "redesign"
        else:
            homepage_type = "legacy"
            context = utils.set_main_site_nav_information(self, context, "Homepage")

        context["parent_homepage"] = homepage_type
        return context
