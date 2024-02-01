import typing
from functools import cached_property

from django import shortcuts
from django.db import models
from wagtail import images as wagtail_images
from wagtail import models as wagtail_models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page import models as routable_models
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages import utils
from networkapi.wagtailpages.pagemodels.base import BasePage
from networkapi.wagtailpages.pagemodels.libraries import constants as base_constants

if typing.TYPE_CHECKING:
    from typing import List

    from wagtail.models import Page


class BaseAuthorsIndexPage(
    routable_models.RoutablePageMixin,
    BasePage,
):
    max_count = 1

    subpage_types: "List[Page]" = []

    template = "pages/libraries/authors_index_page.html"

    banner_image = models.ForeignKey(
        wagtail_images.get_image_model_string(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text=(
            "The image to be used as the banner background image for the author index and all author detail pages."
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

    class Meta:
        abstract = True

    @property
    def author_profiles(self):
        """Return the author profiles associated with this library.

        Author profiles should be localised via the `utils.localize_queryset` method.
        When the index is displayed in a non-default locale, then want to show
        the profile associated with that locale. But, profiles do not necessarily
        exist in all locales. We prefer showing the profile for the locale, but fall
        back to the profile on the default locale.

        """
        raise NotImplementedError("Please implement this property in your subclass.")

    @property
    def library_page(self):
        """Return the library page that this index page is for."""
        raise NotImplementedError("Please implement this property in your subclass.")

    @cached_property
    def article_detail_pages(self):
        """Return the article detail pages that are associated with this library in this locale."""
        return self.get_parent().specific.detail_pages

    def get_author_detail_context(self, profile_slug: str):
        """Return a custom context for the author detail routable page."""
        author_profiles = utils.localize_queryset(self.author_profiles)
        author_profile = shortcuts.get_object_or_404(
            author_profiles,
            slug=profile_slug,
        )

        return {
            "author_profile": author_profile,
            "author_article_count": self.get_author_articles_count(author_profile=author_profile),
            # On author detail pages to include the link to the authors index.
            "latest_articles": self.get_latest_author_articles(author_profile=author_profile),
            "library_page": self.library_page,
        }

    def get_latest_author_articles(self, author_profile):
        """Return the latest articles for the given author."""
        author_articles = self.get_author_articles(author_profile)
        author_articles = author_articles.order_by("-original_publication_date")
        latest_research = author_articles[: base_constants.LATEST_ARTICLES_COUNT]
        return latest_research

    def get_author_articles_count(self, author_profile):
        """Return the number of articles for the given author."""
        return self.get_author_articles(author_profile).count()

    def get_author_articles(self, author_profile):
        """Return the localized articles for the given author."""
        author_articles = self.article_detail_pages
        # During tree sync, an alias is created for every detail page. But, these
        # aliases are still associated with the profile in the default locale. So, when
        # displaying the author page for a non-default locale author, we also want to
        # the detail pages for active locale that are still associated with the default
        # locales author. We know the default locale's author will have the same
        # `translation_key` as the current locale's author. So, instead of filtering
        # for the author `id`, we filter by `translation_key`.
        author_articles = author_articles.filter(
            authors__author_profile__translation_key=author_profile.translation_key
        )
        # And then we fitler for the active locale.
        author_articles = author_articles.filter(locale=wagtail_models.Locale.get_active())

        return author_articles

    def get_banner(self):
        return self.banner_image
