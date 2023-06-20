from django import http, shortcuts
from django.db import models
from wagtail import images as wagtail_images
from wagtail import models as wagtail_models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page import models as routable_models
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages import utils
from networkapi.wagtailpages.pagemodels import profiles
from networkapi.wagtailpages.pagemodels.base import BasePage
from networkapi.wagtailpages.pagemodels.libraries import constants as base_constants
from networkapi.wagtailpages.pagemodels.libraries.research_hub import (
    detail_page,
    library_page,
)


class ResearchAuthorsIndexPage(
    routable_models.RoutablePageMixin,
    BasePage,
):
    max_count = 1

    parent_page_types = ["ResearchLandingPage"]

    template = "pages/libraries/research_hub/authors_index_page.html"

    banner_image = models.ForeignKey(
        wagtail_images.get_image_model_string(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text=(
            "The image to be used as the banner background image for " "the author index and all author detail pages."
        ),
    )

    content_panels = wagtail_models.Page.content_panels + [
        FieldPanel("banner_image"),
    ]

    translatable_fields = [
        # Content tab fields
        SynchronizedField("banner_image"),
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        author_profiles = profiles.Profile.objects.all()
        author_profiles = utils.get_research_authors(author_profiles)
        # When the index is displayed in a non-default locale, then want to show
        # the profile associated with that locale. But, profiles do not necessarily
        # exist in all locales. We prefer showing the profile for the locale, but fall
        # back to the profile on the default locale.
        author_profiles = utils.localize_queryset(author_profiles)
        context["author_profiles"] = author_profiles
        return context

    @routable_models.route(r"^(?P<profile_slug>[-a-z0-9]+)/$", name="research-author-detail")
    def author_detail(
        self,
        request: http.HttpRequest,
        profile_slug: str,
    ):
        context_overrides = self.get_author_detail_context(profile_slug=profile_slug)

        return self.render(
            request=request,
            template="pages/libraries/research_hub/author_detail_page.html",
            context_overrides=context_overrides,
        )

    def get_author_detail_context(self, profile_slug: str):
        author_profiles = utils.localize_queryset(utils.get_research_authors(profiles.Profile.objects.all()))
        author_profile = shortcuts.get_object_or_404(
            author_profiles,
            slug=profile_slug,
        )

        return {
            "author_profile": author_profile,
            "author_article_count": self.get_author_research_count(author_profile=author_profile),
            # On author detail pages to include the link to the authors index.
            "latest_articles": self.get_latest_author_research(author_profile=author_profile),
            "library_page": library_page.ResearchLibraryPage.objects.first(),
        }

    def get_latest_author_research(self, author_profile):
        author_research = self.get_author_research(author_profile)
        author_research = author_research.order_by("-original_publication_date")
        latest_research = author_research[: base_constants.LATEST_ARTICLES_COUNT]
        return latest_research

    def get_author_research_count(self, author_profile):
        return self.get_author_research(author_profile).count()

    @staticmethod
    def get_author_research(author_profile):
        author_research = detail_page.ResearchDetailPage.objects.live().public()

        # During tree sync, an alias is created for every detail page. But, these
        # aliases are still associated with the profile in the default locale. So, when
        # displaying the author page for a non-default locale author, we also want to
        # the detail pages for active locale that are still associated with the default
        # locales author. We know the default locale's author will have the same
        # `translation_key` as the current locale's author. So, instead of filtering
        # for the author `id`, we filter by `translation_key`.
        author_research = author_research.filter(
            authors__author_profile__translation_key=author_profile.translation_key
        )
        # And then we fitler for the active locale.
        author_research = author_research.filter(locale=wagtail_models.Locale.get_active())

        return author_research

    def get_banner(self):
        return self.banner_image
