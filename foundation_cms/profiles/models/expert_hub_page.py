from django.core.exceptions import ValidationError
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.fields import RichTextField
from wagtail.models import Orderable, TranslatableMixin
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_base_page import AbstractBasePage
from foundation_cms.profiles.models.expert_directory_page import ExpertDirectoryPage


# `title` lives on Wagtail's base `wagtailcore_page` table, not on this model's
# table, so we can't override its max_length via a field definition or migration.
# Instead we enforce the limit at the form level (maxlength attr + field validation)
# and in clean() below as a model-level backstop.
class ExpertHubPageAdminForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].max_length = 25
        self.fields["title"].widget.attrs["maxlength"] = 25


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

    panels = [
        PageChooserPanel("expert"),
    ]

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        verbose_name = "Featured Expert"


class ExpertHubPage(AbstractBasePage):
    max_count = 1
    base_form_class = ExpertHubPageAdminForm

    description = RichTextField(
        blank=True,
        max_length=120,
        help_text="Optional description to display on the experts hub page (max 120 characters).",
        features=["bold", "italic", "link"],
    )

    subpage_types = ["profiles.ExpertDirectoryPage", "profiles.ExpertProfilePage"]
    template = "patterns/pages/profiles/expert_hub_page.html"

    content_panels = AbstractBasePage.content_panels + [
        FieldPanel("description"),
        MultiFieldPanel(
            [InlinePanel("featured_experts", label="Expert", min_num=1, max_num=13)],
            heading="Featured Experts",
            classname="collapsible",
            help_text="Experts will be grouped by their first assigned topic.",
        ),
        FieldPanel("body"),
    ]

    translatable_fields = AbstractBasePage.translatable_fields + [
        TranslatableField("description"),
        SynchronizedField("featured_experts"),
    ]

    class Meta:
        verbose_name = "Expert Hub Page"

    def clean(self):
        super().clean()
        if len(self.title) > 25:
            raise ValidationError({"title": "Title must be 25 characters or fewer."})

    def get_context(self, request):
        context = super().get_context(request)

        featured_experts = []
        for fe in (
            self.featured_experts.exclude(expert=None)
            .select_related("expert", "expert__image")
            .prefetch_related("expert__topics")
        ):
            topic = fe.expert.topics.first()
            featured_experts.append({"expert": fe.expert, "topic": topic})

        context["featured_experts"] = featured_experts

        directory = self.get_children().type(ExpertDirectoryPage).live().first()
        if directory:
            context["directory_url"] = directory.url

        return context
