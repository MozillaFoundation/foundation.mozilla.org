from django.db import models
from django.shortcuts import get_object_or_404
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.models import Page

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.base.models.abstract_base_page import Topic
from foundation_cms.base.models.abstract_home_page import AbstractHomePage


class NothingPersonalHomePage(RoutablePageMixin, AbstractHomePage):
    max_count = 1

    DEFAULT_PAGE_SIZE = 12

    PAGE_SIZES = (
        (4, "4"),
        (8, "8"),
        (DEFAULT_PAGE_SIZE, str(DEFAULT_PAGE_SIZE)),
        (24, "24"),
    )

    topic_page_list_size = models.IntegerField(
        choices=PAGE_SIZES,
        default=DEFAULT_PAGE_SIZE,
        help_text="The number of entries to show by default, and per incremental load",
    )

    content_panels = AbstractHomePage.content_panels + [
        # Placeholder for NothingPersonalHomePage blocks
        FieldPanel("topic_page_list_size"),
    ]

    parent_page_types = ["core.HomePage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Nothing Personal Home Page"

    template = "patterns/pages/nothing_personal/home_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        return context

    @route(r"^topics/(?P<slug>[-\w]+)/$")
    def topic_listing(self, request, slug):
        topic = get_object_or_404(Topic, slug=slug)

        pages = (
            Page.objects.live()
            .public()
            .descendant_of(self)
            .filter(topic_relations__tag=topic)
            .prefetch_related("topic_relations__tag")
            .specific()
            .order_by("-last_published_at")
        )

        return self.render(
            request,
            context_overrides={"topic": topic, "pages": pages},
            template="patterns/pages/nothing_personal/topic_page.html",
        )
