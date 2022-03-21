from django import http, shortcuts
from django.utils import text as text_utils
from wagtail.core import models as wagtail_models
from wagtail.contrib.routable_page import models as routable_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata
from networkapi.wagtailpages.pagemodels import profiles


class RoutableProfileMixin(routable_models.RoutablePageMixin):
    context_profile_object_name = 'profile'
    profile_template = ''

    @routable_models.route(r'^(?P<profile_id>[0-9]+)/(?P<profile_slug>[-a-z]+)/$')
    def profile_route(self, request: http.HttpRequest, profile_id: str, profile_slug: str):
        context_overrides = self.get_profile_context_overrides(
            request=request,
            profile_id=int(profile_id),
            profile_slug=profile_slug,
        )
        return self.render(
            request=request,
            template=self.get_profile_template(),
            context_overrides=context_overrides,
        )

    def get_profile_template(self):
        if not self.profile_template:
            raise ValueError('No template for the profile route configured.')
        return self.profile_template

    def get_profile_context_overrides(self, request: http.HttpRequest, profile_id: int, profile_slug: str):
        profile = self.get_profile_object(profile_id=profile_id, profile_slug=profile_slug)
        context_profile_object_name = self.get_context_profile_object_name()
        return {
            context_profile_object_name: profile
        }

    def get_profile_object(self, profile_id: int, profile_slug: str):
        profile = shortcuts.get_object_or_404(
            profiles.Profile,
            id=profile_id,
        )
        if not text_utils.slugify(profile.name) == profile_slug:
            raise http.Http404('Slug does not match id')
        return profile

    def get_context_profile_object_name(self):
        return self.context_profile_object_name


class ResearchAuthorsIndexPage(
    RoutableProfileMixin,
    foundation_metadata.FoundationMetadataPageMixin,
    wagtail_models.Page,
):
    max_count = 1
    parent_page_types = ['ResearchLandingPage']

    context_profile_object_name = 'author_profile'
    profile_template = 'wagtailpages/research_author_detail_page.html'

    def get_context(self, request):
        context = super().get_context(request)
        context["author_profiles"] = profiles.Profile.objects.all()
        return context
