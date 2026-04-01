from django.core.paginator import EmptyPage, Paginator
from django.db import models
from django.http import JsonResponse
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.models import Orderable, TranslatableMixin
from wagtail_localize.fields import SynchronizedField

from foundation_cms.base.models.abstract_base_page import AbstractBasePage, Topic
from foundation_cms.profiles.models.expert_profile_page import ExpertProfilePage


class ExpertHubFeaturedExpert(TranslatableMixin, Orderable):
    hub_page = ParentalKey(
        "profiles.ExpertHubPage",
        related_name="featured_experts",
        on_delete=models.CASCADE,
    )
    expert = models.ForeignKey(
        "profiles.ExpertProfilePage",
        related_name="+",
        on_delete=models.CASCADE,
    )
    display_topic = models.ForeignKey(
        Topic,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Topic to display on the card. If empty, the first topic is used.",
    )

    panels = [
        PageChooserPanel("expert"),
        FieldPanel("display_topic"),
    ]

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        verbose_name = "Featured Expert"


class ExpertHubFeaturedTopic(TranslatableMixin, Orderable):
    hub_page = ParentalKey(
        "profiles.ExpertHubPage",
        related_name="featured_topics",
        on_delete=models.CASCADE,
    )
    topic = models.ForeignKey(
        Topic,
        related_name="+",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("topic")]

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        verbose_name = "Featured Topic"


class ExpertHubPage(RoutablePageMixin, AbstractBasePage):
    PAGE_SIZE = 11
    max_count = 1

    subpage_types = ["profiles.ExpertProfilePage"]
    template = "patterns/pages/profiles/expert_hub_page.html"

    content_panels = AbstractBasePage.content_panels + [
        InlinePanel("featured_experts", label="Featured Experts", min_num=1, max_num=12),
        InlinePanel("featured_topics", label="Featured Issue Areas", max_num=10),
        FieldPanel("body"),
    ]

    translatable_fields = AbstractBasePage.translatable_fields + [
        SynchronizedField("featured_experts"),
        SynchronizedField("featured_topics"),
    ]

    class Meta:
        verbose_name = "Expert Hub Page"

    def get_experts(self, topic_slug=None):
        """Return live, public ExpertProfilePage, optionally filtered by topic."""

        qs = (
            ExpertProfilePage.objects.live()
            .public()
            .select_related("image")
            .prefetch_related("topics")
            .order_by("title")
        )
        if topic_slug:
            qs = qs.filter(topics__slug=topic_slug).distinct()

        return qs

    @staticmethod
    def _serialize_expert(expert):
        """Serialize an ExpertProfilePage to a JSON-friendly dict."""
        image = None
        if expert.image:
            image = {
                "url": expert.image.file.url,
                "width": expert.image.width,
                "height": expert.image.height,
                "alt": expert.image.title,
            }

        return {
            "id": expert.pk,
            "title": expert.title,
            "url": expert.url,
            "role": expert.role,
            "location": (
                {
                    "code": str(expert.location),
                    "name": expert.location.name,
                }
                if expert.location
                else None
            ),
            "affiliation": getattr(expert, "affiliation", ""),
            "image": image,
            "topics": [{"name": topic.name, "slug": topic.slug} for topic in expert.topics.all()],
        }

    def get_context(self, request):
        context = super().get_context(request)
        featured_experts = []
        for featured_expert in self.featured_experts.select_related(
            "expert", "expert__image", "display_topic"
        ).prefetch_related("expert__topics"):
            topics = list(featured_expert.expert.topics.all())
            topic = featured_expert.display_topic or (topics[0] if topics else None)
            featured_experts.append({"expert": featured_expert.expert, "topic": topic})

        # Group by topic
        featured_experts.sort(key=lambda item: (item["topic"].name if item["topic"] else ""))

        context["featured_experts"] = featured_experts
        context["featured_topic_objects"] = [
            featured_topic.topic for featured_topic in self.featured_topics.select_related("topic")
        ]
        context["total_experts_count"] = ExpertProfilePage.objects.live().public().count()

        return context

    @route(r"^experts/$")
    def experts_api(self, request):
        """JSON endpoint for paginated expert cards."""
        topic_slug = request.GET.get("topic")
        page_number = request.GET.get("page", "0")

        try:
            page_number = int(page_number)
        except (ValueError, TypeError):
            page_number = 0

        experts = self.get_experts(topic_slug=topic_slug)
        paginator = Paginator(experts, self.PAGE_SIZE)

        try:
            page_obj = paginator.page(page_number + 1)
        except EmptyPage:
            return JsonResponse(
                {
                    "experts": [],
                    "pagination": {
                        "current_page": page_number,
                        "total_pages": paginator.num_pages,
                        "total_count": paginator.count,
                        "has_next": False,
                        "has_previous": page_number > 0,
                        "page_size": self.PAGE_SIZE,
                    },
                }
            )

        return JsonResponse(
            {
                "experts": [self._serialize_expert(expert) for expert in page_obj],
                "pagination": {
                    "current_page": page_number,
                    "total_pages": paginator.num_pages,
                    "total_count": paginator.count,
                    "has_next": page_obj.has_next(),
                    "has_previous": page_obj.has_previous(),
                    "page_size": self.PAGE_SIZE,
                },
            }
        )
