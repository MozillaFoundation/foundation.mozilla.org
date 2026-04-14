from django.core.paginator import EmptyPage, Paginator
from django.db import models
from django.http import JsonResponse
from django_countries import countries
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import RichTextField
from wagtail.models import Orderable, TranslatableMixin
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_base_page import AbstractBasePage, Topic
from foundation_cms.profiles.models.expert_profile_page import ExpertProfilePage


class ExpertHubFeaturedTopic(TranslatableMixin, Orderable):
    hub_page = ParentalKey(
        "profiles.ExpertDirectoryPage",
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


class ExpertDirectoryPage(RoutablePageMixin, AbstractBasePage):
    PAGE_SIZE = 11
    IMAGE_RATIO = "2:3"
    IMAGE_BASE_WIDTH = 300

    description = RichTextField(
        blank=True,
        help_text="Optional description to display on the experts directory page.",
        features=["bold", "italic", "link"],
    )

    subpage_types: list[str] = []
    parent_page_types = ["profiles.ExpertHubPage"]
    template = "patterns/pages/profiles/expert_directory_page.html"

    content_panels = AbstractBasePage.content_panels + [
        FieldPanel("description"),
        MultiFieldPanel(
            [InlinePanel("featured_topics", label="Topic", max_num=5)],
            heading="Featured Topics",
            classname="collapsible",
        ),
        # TODO: I think we don't need this?
        # FieldPanel("body"),
    ]

    translatable_fields = AbstractBasePage.translatable_fields + [
        TranslatableField("description"),
        SynchronizedField("featured_topics"),
    ]

    class Meta:
        verbose_name = "Expert Directory Page"

    def get_experts(self, topic_slug=None, country=None, role=None):
        """Return live, public ExpertProfilePage children of the hub, optionally filtered."""
        qs = (
            ExpertProfilePage.objects.live()
            .public()
            .child_of(self.get_parent())
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
    def _serialize_expert(expert, ratio, base_width):
        """Serialize an ExpertProfilePage to a JSON-friendly dict."""
        image = None
        if expert.image:
            img = expert.image
            width_ratio, height_ratio = (float(part) for part in ratio.split(":"))
            # Use the 1.5× rendition as src, matching the responsive_image tag default
            w = int(base_width * 1.5)
            h = int(w * height_ratio / width_ratio)
            primary = img.get_rendition(f"fill-{w}x{h}")
            image = {
                "url": primary.url,
                "width": primary.width,
                "height": primary.height,
                "alt": img.title,
            }

        return {
            "id": expert.pk,
            "title": expert.title,
            "url": expert.url,
            "role": expert.role,
            "location": ({"code": str(expert.location), "name": expert.location.name} if expert.location else None),
            "affiliation": getattr(expert, "affiliation", ""),
            "image": image,
            "topics": [{"name": t.name, "slug": t.slug} for t in expert.topics.all()],
        }

    def get_context(self, request):
        context = super().get_context(request)

        context["featured_topic_objects"] = [
            ft.topic for ft in self.featured_topics.select_related("topic") if ft.topic
        ]

        active_topic = request.GET.get("topic", "")
        active_country = request.GET.get("country", "")
        active_role = request.GET.get("role", "")

        context["filter_topics"] = [(t.slug, t.name) for t in Topic.objects.all().order_by("name")]
        context["filter_countries"] = countries
        context["filter_roles"] = sorted(
            ExpertProfilePage.objects.live()
            .public()
            .child_of(self.get_parent())
            .exclude(role="")
            .values_list("role", flat=True)
            .distinct()
        )

        experts = self.get_experts(
            topic_slug=active_topic or None,
            country=active_country or None,
            role=active_role or None,
        )
        paginator = Paginator(experts, self.PAGE_SIZE)
        experts_page = paginator.get_page(request.GET.get("page", 1))

        context["experts_page"] = experts_page
        context["total_experts_count"] = paginator.count
        context["expert_image_ratio"] = self.IMAGE_RATIO
        context["active_topic"] = active_topic
        context["active_country"] = active_country
        context["active_role"] = active_role
        context["page_range"] = paginator.get_elided_page_range(experts_page.number, on_each_side=2, on_ends=1)

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
                "experts": [
                    self._serialize_expert(expert, self.IMAGE_RATIO, self.IMAGE_BASE_WIDTH) for expert in page_obj
                ],
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
