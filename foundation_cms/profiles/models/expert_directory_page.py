from django.core.paginator import EmptyPage, Paginator
from django.db import models
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django_countries.fields import Country
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import RichTextField
from wagtail.models import Orderable, TranslatableMixin
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_base_page import (
    AbstractBasePage,
    PageTopic,
    Topic,
)
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
    PAGE_SIZE = 15
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
    ]

    translatable_fields = AbstractBasePage.translatable_fields + [
        TranslatableField("description"),
        SynchronizedField("featured_topics"),
    ]

    class Meta:
        verbose_name = "Expert Directory Page"

    def get_experts(self, topic_slugs=None, countries=None, roles=None):
        """Return live, public ExpertProfilePage children of the hub, optionally filtered.

        Each filter accepts a list of values and is applied as OR within the list.
        """
        qs = (
            ExpertProfilePage.objects.live()
            .public()
            .child_of(self.get_parent())
            .select_related("image")
            .prefetch_related("topics")
            .order_by("title")
        )
        if topic_slugs:
            qs = qs.filter(topic_relations__tag__slug__in=topic_slugs).distinct()
        if countries:
            qs = qs.filter(location__in=countries)
        if roles:
            qs = qs.filter(role__in=roles)
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

    def _get_listing_context(self, request):
        """Build the context needed to render the listing fragment only.

        Skips the filter option queries (topics, countries, roles)
        so partial requests triggered by filter changes are cheaper.
        """
        context = super().get_context(request)

        context["featured_topic_objects"] = [
            ft.topic for ft in self.featured_topics.select_related("topic") if ft.topic
        ]

        active_topics = request.GET.getlist("topic")
        active_countries = request.GET.getlist("country")
        active_roles = request.GET.getlist("role")

        experts = self.get_experts(
            topic_slugs=active_topics or None,
            countries=active_countries or None,
            roles=active_roles or None,
        )
        paginator = Paginator(experts, self.PAGE_SIZE)
        experts_page = paginator.get_page(request.GET.get("page", 1))

        context["experts_page"] = experts_page
        context["total_experts_count"] = paginator.count
        context["expert_image_ratio"] = self.IMAGE_RATIO

        return context

    def get_context(self, request):
        context = self._get_listing_context(request)

        all_experts = ExpertProfilePage.objects.live().public().child_of(self.get_parent())

        used_topic_ids = (
            PageTopic.objects.filter(content_object_id__in=all_experts.values("id"))
            .values_list("tag_id", flat=True)
            .distinct()
        )
        context["filter_topics"] = list(
            Topic.objects.filter(id__in=used_topic_ids).order_by("name").values_list("slug", "name")
        )

        used_country_codes = {
            str(code) for code in all_experts.exclude(location="").values_list("location", flat=True)
        }
        context["filter_countries"] = sorted(
            [(code, Country(code).name) for code in used_country_codes],
            key=lambda pair: pair[1],
        )

        role_names = sorted(all_experts.exclude(role="").values_list("role", flat=True).distinct())
        context["filter_roles"] = [(role_name, role_name) for role_name in role_names]

        context["active_topics"] = request.GET.getlist("topic")
        context["active_countries"] = request.GET.getlist("country")
        context["active_roles"] = request.GET.getlist("role")

        return context

    def serve(self, request, *args, **kwargs):
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            context = self._get_listing_context(request)
            return TemplateResponse(
                request,
                "patterns/pages/profiles/_expert_listing.html",
                context,
            )
        return super().serve(request, *args, **kwargs)

    @route(r"^experts/$")
    def experts_api(self, request):
        """JSON endpoint for paginated expert cards."""
        topic_slugs = request.GET.getlist("topic")
        countries = request.GET.getlist("country")
        roles = request.GET.getlist("role")
        page_number = request.GET.get("page", "0")

        try:
            page_number = int(page_number)
        except (ValueError, TypeError):
            page_number = 0

        experts = self.get_experts(topic_slugs=topic_slugs or None, countries=countries or None, roles=roles or None)
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
