from django import http, shortcuts
from django.db import models
from django.utils import text as text_utils
from wagtail import images as wagtail_images
from wagtail.core import models as wagtail_models
from wagtail.contrib.routable_page import models as routable_models
from wagtail.images.edit_handlers import ImageChooserPanel

from networkapi.wagtailpages import utils
from networkapi.wagtailpages.pagemodels import profiles
from networkapi.wagtailpages.pagemodels.research_hub import base as research_base
from networkapi.wagtailpages.pagemodels.research_hub import detail_page
from networkapi.wagtailpages.pagemodels.research_hub import library_page


class ResearchAuthorsIndexPage(
    routable_models.RoutablePageMixin,
    research_base.ResearchHubBasePage,
):
    max_count = 1
    parent_page_types = ['ResearchLandingPage']

    banner_image = models.ForeignKey(
        wagtail_images.get_image_model_string(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text=(
            'The image to be used as the banner background image for '
            'the author index and all author detail pages.'
        ),
    )

    content_panels = wagtail_models.Page.content_panels + [
        ImageChooserPanel('banner_image'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        author_profiles = profiles.Profile.objects.all()
        author_profiles = author_profiles.filter_research_authors()
        # When the index is displayed in a non-default locale, then want to show
        # the profile associated with that locale. But, profiles do not necessarily
        # exist in all locales. We prefer showing the profile for the locale, but fall
        # back to the profile on the default locale.
        author_profiles = utils.localize_queryset(author_profiles)
        context["author_profiles"] = author_profiles
        context["breadcrumbs"] = self.get_breadcrumbs()
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

        author_research_count = self.get_author_research(author_profile).count()
        latest_research = self.get_latest_research(author_profile)

        # On author detail pages to include the link to the authors index.
        detail_page_breadcrumbs = self.get_breadcrumbs(include_self=True)

        return {
            'author_profile': author_profile,
            'author_research_count': author_research_count,
            'breadcrumbs': detail_page_breadcrumbs,
            'latest_research': latest_research,
            'library_page': library_page.ResearchLibraryPage.objects.first(),
        }

    def get_latest_research(self, author_profile):
        LATEST_RESEARCH_COUNT_LIMIT = 3
        author_research = self.get_author_research(author_profile)
        author_research = author_research.order_by('-original_publication_date')
        latest_research = author_research[:LATEST_RESEARCH_COUNT_LIMIT]
        return latest_research

    def get_author_research(self, author_profile):
        author_research = detail_page.ResearchDetailPage.objects.all()
        # During tree sync, an alias is created for every detail page. But, these
        # aliases are still associated with the profile in the default locale. So, when
        # displaying the author page for a non-default locale author, we also want to
        # the detail pages for active locale that are still associated with the default
        # locales author. We know the default locale's author will have the same
        # `translation_key` as the current locale's author. So, instead of filtering
        # for the author `id`, we filter by `translation_key`.
        author_research = author_research.filter(
            research_authors__author_profile__translation_key=(
                author_profile.translation_key
            )
        )
        # And then we fitler for the active locale.
        author_research = author_research.filter(
            locale=wagtail_models.Locale.get_active()
        )
        return author_research

    def get_banner(self):
        return self.banner_image
