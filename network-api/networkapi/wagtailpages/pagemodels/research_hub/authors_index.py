from wagtail.core import models as wagtail_models
from wagtail.contrib.routable_page import models as routable_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class ResearchAuthorsIndexPage(
    routable_models.RoutablePageMixin,
    foundation_metadata.FoundationMetadataPageMixin,
    wagtail_models.Page,
):
    max_count = 1
    parent_page_types = ['ResearchLandingPage']


    @routable_models.route(r'^test/$')
    def author_detail(self, request):
        return self.render(
            request=request,
            template='wagtailpages/research_author_detail_page.html',
        )

