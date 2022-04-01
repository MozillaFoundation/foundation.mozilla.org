from django import http, shortcuts
from django.db import models
from django.utils import text as text_utils
from wagtail.core import models as wagtail_models
from wagtail.contrib.routable_page import models as routable_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata
from networkapi.wagtailpages.pagemodels import profiles
from networkapi.wagtailpages.pagemodels.research_hub import detail_page


class ResearchAuthorsIndexPage(
    routable_models.RoutablePageMixin,
    foundation_metadata.FoundationMetadataPageMixin,
    wagtail_models.Page,
):
    max_count = 1
    parent_page_types = ['ResearchLandingPage']

    def get_context(self, request):
        context = super().get_context(request)
        context['author_profiles'] = profiles.Profile.objects.filter_research_authors()
        default_locale = wagtail_models.Locale.get_default()
        active_locale = wagtail_models.Locale.get_active()
        # context["author_profiles"] = (
        #     profiles.Profile.objects.all()
        #         .filter_research_authors()
        #         .filter(models.Q(locale=default_locale) | models.Q(locale=active_locale))
        #         .order_by('translation_key', '-locale')
        #         .distinct('translation_key')
        # )
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
        LATEST_RESERACH_COUNT_LIMIT = 3
        latest_research = (
            detail_page.ResearchDetailPage.objects.all()
                .filter(research_authors__author_profile=author_profile)
                .order_by('-original_publication_date')
                [:LATEST_RESERACH_COUNT_LIMIT]
        )
        return {
            'author_profile': author_profile,
            'latest_research': latest_research,
        }
