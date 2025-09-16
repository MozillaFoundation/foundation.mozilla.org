from django.db import models
from django.shortcuts import get_object_or_404
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField
from wagtail.models import Page

from foundation_cms.base.models.abstract_base_page import Topic
from foundation_cms.base.models.abstract_home_page import AbstractHomePage
from foundation_cms.blocks import NarrowTextImageBlock, TwoColumnContainerBlock
from foundation_cms.legacy_apps.wagtailpages.utils import get_default_locale
from foundation_cms.mixins.hero_image import HeroImageMixin


class NothingPersonalHomePage(RoutablePageMixin, AbstractHomePage, HeroImageMixin):
    max_count = 1
    who_we_are_description = models.TextField(blank=True, help_text="Description text for the Who We Are section")

    nothing_personal_block_options = [
        ("two_column_container_block", TwoColumnContainerBlock()),
        ("narrow_text_image_block", NarrowTextImageBlock()),
        # NP Text Image Block
        # product review carousel block
        # 50/50 block
    ]
    body = StreamField(
        nothing_personal_block_options,
        use_json_field=True,
        blank=True,
    )

    parent_page_types = ["core.HomePage"]
    subpage_types = [
        "nothing_personal.NothingPersonalArticleCollectionPage",
        "nothing_personal.NothingPersonalArticlePage",
        "nothing_personal.NothingPersonalProductReviewPage",
    ]

    content_panels = AbstractHomePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_image"),
                FieldPanel("hero_image_alt_text"),
            ],
            heading="Hero Image",
        ),
        FieldPanel("body"),
        FieldPanel("who_we_are_description"),
    ]

    class Meta:
        verbose_name = "Nothing Personal Home Page"

    template = "patterns/pages/nothing_personal/home_page.html"

    def get_context(self, request, virtual_page_name=None):
        context = super().get_context(request)

        if virtual_page_name:
            context["page_type_bem"] = self._to_bem_case(virtual_page_name)

        return context

    # TODO:FIXME Topic listing route should not live under the NP tree
    @route(r"^topics/(?P<slug>[-\w]+)/$")
    def topic_listing(self, request, slug):
        (DEFAULT_LOCALE, DEFAULT_LOCALE_ID) = get_default_locale()

        topic = get_object_or_404(Topic, slug=slug)

        # Grabbing all pages in the DB with this topic, in the default locale.
        base_qs = (
            Page.objects.live()
            .public()
            .filter(locale_id=DEFAULT_LOCALE_ID)
            .filter(topic_relations__tag=topic)
            .select_related("search_image")
            .prefetch_related("topics")
        )

        total_pages_count = base_qs.count()

        # Separating child pages of the NothingPersonalHomePage from the original queryset.
        np_pages = base_qs.child_of(self)

        # All other pages with this topic, excluding the above child pages.
        other_pages = base_qs.exclude(id__in=np_pages.values_list("id", flat=True))

        # Ordering both querysets by most recently published first, and converting to specific.
        np_pages = np_pages.order_by("-last_published_at").specific()
        other_pages = other_pages.order_by("-last_published_at").specific()

        return self.render(
            request,
            context_overrides={
                "topic": topic,
                "np_pages": np_pages,
                "other_pages": other_pages,
                "total_pages_count": total_pages_count,
                "page_type_bem": self._to_bem_case("TopicListingPage"),
            },
            template="patterns/pages/core/topic_listing_page.html",
        )
