from django import http, shortcuts
from django.utils import text as text_utils
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
        context["author_profiles"] = profiles.Profile.objects.filter_research_authors()
        return context

    @routable_models.route(r'^(?P<profile_id>[0-9]+)/(?P<profile_slug>[-a-z]+)/$')
    def author_detail(self, request: http.HttpRequest, profile_id: str, profile_slug: str):
        context_overrides = self.get_author_detail_context(profile_id=int(profile_id))

        slugified_profile_name = text_utils.slugify(
            context_overrides['author_profile'].name
        )
        if not slugified_profile_name == profile_slug:
            raise http.Http404('Slug does not fit profile name')

        return self.render(
            request=request,
            template='wagtailpages/research_author_detail_page.html',
            context_overrides=context_overrides,
        )

    def get_author_detail_context(self, profile_id: int):
        author_profiles = profiles.Profile.objects.filter_research_authors()
        author_profile = shortcuts.get_object_or_404(
            author_profiles,
            id=profile_id,
        )
        LATEST_RESERACH_LIMIT = 3
        latest_research = [
            ar.research_detail_page
            for ar in (
                author_profile.authored_research.all()
                .order_by('-research_detail_page__original_publication_date')
                [:LATEST_RESERACH_LIMIT]
            )
        ]
        return {
            'author_profile': author_profile,
            'latest_research': latest_research,
        }
