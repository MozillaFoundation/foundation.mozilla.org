from django.shortcuts import get_object_or_404
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_base_page import Topic
from foundation_cms.base.models.abstract_home_page import AbstractHomePage
from foundation_cms.blocks import HeroAccordionBlock
from foundation_cms.legacy_apps.wagtailpages.utils import get_default_locale


class HomePage(RoutablePageMixin, AbstractHomePage):
    hero_accordion = StreamField(
        HeroAccordionBlock(),
        min_num=2,
        max_num=3,
        verbose_name="Hero Accordion",
        blank=True,
    )

    content_panels = AbstractHomePage.content_panels + [
        FieldPanel("hero_accordion"),
        FieldPanel("body"),
    ]

    translatable_fields = AbstractHomePage.translatable_fields + [
        # Content tab fields
        TranslatableField("hero_accordion"),
        TranslatableField("body"),
    ]

    search_fields = AbstractHomePage.search_fields + [
        index.SearchField("body", boost=8),
        # Hero accordion content indexing
        index.RelatedFields(
            "hero_accordion",
            [
                index.SearchField("label", boost=6),
                index.SearchField("heading", boost=6),
            ],
        ),
        # Homepage filters
        index.FilterField("first_published_at"),
    ]

    template = "patterns/pages/core/home_page.html"

    class Meta:
        verbose_name = "Home Page"

    def get_context(self, request):
        context = super().get_context(request)
        return context

    @route(r"^topics/(?P<slug>[-\w]+)/$")
    def topic_listing(self, request, slug):
        from foundation_cms.nothing_personal.models import NothingPersonalHomePage

        (DEFAULT_LOCALE, DEFAULT_LOCALE_ID) = get_default_locale()

        topic = get_object_or_404(Topic, slug=slug)
        np_home = NothingPersonalHomePage.objects.live().first()

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

        if np_home:
            np_pages = base_qs.child_of(np_home)
            # All other pages with this topic, excluding the NP child pages.
            other_pages = base_qs.exclude(id__in=np_pages.values_list("id", flat=True))
        else:
            np_pages = Page.objects.none()
            other_pages = base_qs

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
