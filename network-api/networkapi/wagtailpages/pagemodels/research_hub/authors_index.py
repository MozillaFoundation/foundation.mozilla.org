from django import http, shortcuts
from django.core import exceptions
from wagtail.core import models as wagtail_models
from wagtail.contrib.routable_page import models as routable_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata
from networkapi.wagtailpages.pagemodels import profiles


class ResearchAuthorsIndexPage(
    routable_models.RoutablePageMixin,
    foundation_metadata.FoundationMetadataPageMixin,
    wagtail_models.Page,
):
    max_count = 1
    parent_page_types = ['ResearchLandingPage']


    def get_context(self, request):
        context = super().get_context(request)
        context["author_profiles"] = profiles.Profile.objects.all()
        context["test"] = "the value"
        return context

    @routable_models.route(r'^(?P<author_id>[0-9]+)/$')
    def author_detail(self, request: http.HttpRequest, author_id: str):
        author_profile = shortcuts.get_object_or_404(
            profiles.Profile,
            id=int(author_id),
        )

        return self.render(
            request=request,
            template='wagtailpages/research_author_detail_page.html',
            context_overrides={'author_profile': author_profile},
        )

