from django.shortcuts import get_object_or_404
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.models import Page

from foundation_cms.base.models.abstract_base_page import Topic
from foundation_cms.base.models.abstract_home_page import AbstractHomePage
from foundation_cms.legacy_apps.wagtailpages.utils import get_default_locale


class NothingPersonalHomePage(RoutablePageMixin, AbstractHomePage):
    max_count = 1

    content_panels = AbstractHomePage.content_panels + [
        # Placeholder for NothingPersonalHomePage blocks
    ]

    parent_page_types = ["core.HomePage"]

    class Meta:
        verbose_name = "Nothing Personal Home Page"

    template = "patterns/pages/nothing_personal/home_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        return context

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
            },
            template="patterns/pages/nothing_personal/topic_page.html",
        )
