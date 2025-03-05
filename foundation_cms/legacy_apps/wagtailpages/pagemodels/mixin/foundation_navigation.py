from foundation_cms.legacy_apps.wagtailpages import utils


class FoundationNavigationPageMixin:
    def get_context(self, request):
        context = super().get_context(request)
        context = utils.set_main_site_nav_information(self, context, "Homepage")
        return context

    class Meta:
        abstract = True
