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
        # When the index is displayed in a non-default locale, then want to show
        # the profile associated with that locale. But, profiles do not necessarily
        # exist in all locales. We prefer showing the profile for the locale, but fall
        # back to the profile on the default locale.
        default_locale = wagtail_models.Locale.get_default()
        active_locale = wagtail_models.Locale.get_active()
        author_profiles = profiles.Profile.objects.all()
        author_profiles = author_profiles.filter_research_authors()
        author_profiles = author_profiles.filter(
            models.Q(locale=default_locale) | models.Q(locale=active_locale)
        )
        author_profiles = author_profiles.annotate(
            locale_is_default=models.Case(
                models.When(locale=default_locale, then=True),
                default=False,
            )
        )
        author_profiles = author_profiles.order_by(
            'translation_key',
            'locale_is_default',
        )
        author_profiles = author_profiles.distinct('translation_key')
        context["author_profiles"] = author_profiles
        return context

    @routable_models.route(r'^(?P<profile_id>[0-9]+)/(?P<profile_slug>[-a-z]+)/$')
    def author_detail(
        self,
        request: http.HttpRequest,
        profile_id: str,
        profile_slug: str,
    ):
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
        research_author_profiles = profiles.Profile.objects.filter_research_authors()
        author_profile = shortcuts.get_object_or_404(
            research_author_profiles,
            id=profile_id,
        )

        LATEST_RESERACH_COUNT_LIMIT = 3
        latest_research = detail_page.ResearchDetailPage.objects.all()
        latest_research = latest_research.filter(
            research_authors__author_profile__translation_key=(
                author_profile.translation_key
            )
        )
        latest_research = latest_research.filter(
            locale=wagtail_models.Locale.get_active()
        )
        latest_research = latest_research.order_by('-original_publication_date')
        latest_research = latest_research[:LATEST_RESERACH_COUNT_LIMIT]

        return {
            'author_profile': author_profile,
            'latest_research': latest_research,
        }
