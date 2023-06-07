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
from networkapi.wagtailpages.pagemodels.libraries.rcc import detail_page, library_page


class RCCAuthorsIndexPage(
    routable_models.RoutablePageMixin,
    BasePage,
):
    max_count = 1

    parent_page_types = ["RCCLandingPage"]

    template = "pages/libraries/rcc/authors_index_page.html"

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
        author_profiles = utils.get_rcc_authors(author_profiles)
        # When the index is displayed in a non-default locale, then want to show
        # the profile associated with that locale. But, profiles do not necessarily
        # exist in all locales. We prefer showing the profile for the locale, but fall
        # back to the profile on the default locale.
        author_profiles = utils.localize_queryset(author_profiles)
        context["author_profiles"] = author_profiles
        return context

    @routable_models.route(r"^(?P<profile_slug>[-a-z0-9]+)/$", name="rcc-author-detail")
    def author_detail(
        self,
        request: http.HttpRequest,
        profile_slug: str,
    ):
        context_overrides = self.get_author_detail_context(profile_slug=profile_slug)

        return self.render(
            request=request,
            template="pages/libraries/rcc/author_detail_page.html",
            context_overrides=context_overrides,
        )

    def get_author_detail_context(self, profile_slug: str):
        author_profiles = utils.localize_queryset(utils.get_rcc_authors(profiles.Profile.objects.all()))
        author_profile = shortcuts.get_object_or_404(
            author_profiles,
            slug=profile_slug,
        )

        return {
            "author_profile": author_profile,
            "author_article_count": self.get_author_rcc_entries_count(author_profile=author_profile),
            "latest_articles": self.get_latest_author_rcc_entries(author_profile=author_profile),
            "library_page": library_page.RCCLibraryPage.objects.first(),
        }

    def get_latest_author_rcc_entries(self, author_profile):
        LATEST_RESEARCH_COUNT_LIMIT = 3
        author_articles = self.get_author_rcc_entries(author_profile)
        author_articles = author_articles.order_by("-original_publication_date")
        latest_articles = author_articles[:LATEST_RESEARCH_COUNT_LIMIT]
        return latest_articles

    def get_author_rcc_entries_count(self, author_profile):
        return self.get_author_rcc_entries(author_profile).count()

    @staticmethod
    def get_author_rcc_entries(author_profile):
        author_rcc_entries = detail_page.RCCDetailPage.objects.live().public()

        # During tree sync, an alias is created for every detail page. But, these
        # aliases are still associated with the profile in the default locale. So, when
        # displaying the author page for a non-default locale author, we also want to
        # the detail pages for active locale that are still associated with the default
        # locales author. We know the default locale's author will have the same
        # `translation_key` as the current locale's author. So, instead of filtering
        # for the author `id`, we filter by `translation_key`.
        author_rcc_entries = author_rcc_entries.filter(
            rcc_authors__author_profile__translation_key=author_profile.translation_key
        )
        # And then we fitler for the active locale.
        author_rcc_entries = author_rcc_entries.filter(locale=wagtail_models.Locale.get_active())

        return author_rcc_entries

    def get_banner(self):
        return self.banner_image
