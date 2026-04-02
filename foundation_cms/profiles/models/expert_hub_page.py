from django.core.paginator import EmptyPage, Paginator
from django.db import models
from django.http import JsonResponse
from django_countries import countries
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import RichTextField
from wagtail.models import Orderable, TranslatableMixin
from wagtail_localize.fields import SynchronizedField, TranslatableField

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
        related_name="expert_page_featured_in",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    display_topic = models.ForeignKey(
        Topic,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="topic_featured_in_expert_pages",
        help_text="Topic to feature for this expert card and that will be used to group experts by topic (optional). "
        "If not set, the first topic assigned to the expert will be used.",
    )

    panels = [
        PageChooserPanel("expert"),
        FieldPanel("display_topic"),
    ]

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        verbose_name = "Featured Expert"

    def clean(self):
        super().clean()
        if self.display_topic and self.expert_id:
            if not self.expert.topics.filter(pk=self.display_topic_id).exists():
                from django.core.exceptions import ValidationError

                raise ValidationError(
                    {
                        "display_topic": (
                            "Selected topic is not assigned to this expert. "
                            "Please select a topic that is assigned to the expert "
                            "or remove the display topic."
                        )
                    }
                )


class ExpertHubFeaturedTopic(TranslatableMixin, Orderable):
    hub_page = ParentalKey(
        "profiles.ExpertHubPage",
        related_name="featured_topics",
        on_delete=models.CASCADE,
    )
    topic = models.ForeignKey(
        Topic,
        related_name="expert_hub_featured_topics",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    panels = [FieldPanel("topic")]

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        verbose_name = "Featured Topic"


class ExpertHubPage(RoutablePageMixin, AbstractBasePage):
    PAGE_SIZE = 11
    max_count = 1

    listing_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Heading for the experts listing section.",
    )
    description = RichTextField(
        blank=True,
        help_text="Optional description for the hub page.",
        features=["bold", "italic", "link"],
    )

    subpage_types = ["profiles.ExpertProfilePage"]
    template = "patterns/pages/profiles/expert_hub_page.html"

    content_panels = AbstractBasePage.content_panels + [
        FieldPanel("description"),
        FieldPanel("listing_title"),
        MultiFieldPanel(
            [InlinePanel("featured_experts", label="Featured Experts", min_num=1, max_num=12)],
            heading="Featured Experts",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [InlinePanel("featured_topics", label="Featured Issue Areas", max_num=5)],
            heading="Featured Issue Areas",
            classname="collapsible",
        ),
        FieldPanel("body"),
    ]

    translatable_fields = AbstractBasePage.translatable_fields + [
        TranslatableField("description"),
        TranslatableField("listing_title"),
        SynchronizedField("featured_experts"),
        SynchronizedField("featured_topics"),
    ]

    class Meta:
        verbose_name = "Expert Hub Page"

    def get_experts(self, topic_slug=None, country=None, role=None):
        """Return live, public ExpertProfilePage, optionally filtered by topic, country, and role."""

        qs = (
            ExpertProfilePage.objects.live()
            .public()
            .child_of(self)
            .select_related("image")
            .prefetch_related("topics")
            .order_by("title")
        )
        if topic_slug:
            qs = qs.filter(topic_relations__tag__slug=topic_slug).distinct()
        if country:
            qs = qs.filter(location=country)
        if role:
            qs = qs.filter(role=role)

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

        # Featured experts
        featured_experts = []
        for featured_expert in self.featured_experts.select_related(
            "expert", "expert__image", "display_topic"
        ).prefetch_related("expert__topics"):
            if not featured_expert.expert:
                continue
            topics = list(featured_expert.expert.topics.all())
            topic = featured_expert.display_topic or (topics[0] if topics else None)
            featured_experts.append({"expert": featured_expert.expert, "topic": topic})

        featured_experts.sort(key=lambda item: (item["topic"].name if item["topic"] else ""))
        context["featured_experts"] = featured_experts

        # Featured topics
        context["featured_topic_objects"] = [
            ft.topic for ft in self.featured_topics.select_related("topic") if ft.topic
        ]

        # All experts (filtered)
        active_topic = request.GET.get("topic", "")
        active_country = request.GET.get("country", "")
        active_role = request.GET.get("role", "")

        experts = self.get_experts(
            topic_slug=active_topic or None,
            country=active_country or None,
            role=active_role or None,
        )

        context["filter_topics"] = [(topic.slug, topic.name) for topic in Topic.objects.all().order_by("name")]
        context["filter_countries"] = countries
        context["filter_roles"] = sorted(
            ExpertProfilePage.objects.live()
            .public()
            .child_of(self)
            .exclude(role="")
            .values_list("role", flat=True)
            .distinct()
        )

        # Pagination
        paginator = Paginator(experts, self.PAGE_SIZE)
        page_obj = paginator.get_page(request.GET.get("page", 1))

        context["experts_page"] = page_obj
        context["total_experts_count"] = paginator.count
        context["active_topic"] = active_topic
        context["active_country"] = active_country
        context["active_role"] = active_role

        return context

    @route(r"^experts/$")
    def experts_api(self, request):
        """JSON endpoint for paginated expert cards."""
        topic_slug = request.GET.get("topic")
        country = request.GET.get("country")
        role = request.GET.get("role")
        page_number = request.GET.get("page", "0")

        try:
            page_number = int(page_number)
        except (ValueError, TypeError):
            page_number = 0

        experts = self.get_experts(topic_slug=topic_slug, country=country, role=role)
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
