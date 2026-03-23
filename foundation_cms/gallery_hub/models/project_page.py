from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Locale
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.blocks.block_registry import BlockRegistry
from foundation_cms.mixins.hero_image import HeroImageMixin


class ProjectPage(AbstractArticlePage, HeroImageMixin):

    cta_link = StreamField(
        BlockRegistry.get_blocks(["link_button_block"]),
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    content_panels = AbstractArticlePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_image"),
                FieldPanel("hero_image_alt_text"),
            ],
            heading="Hero Image",
            classname="collapsible",
        ),
        FieldPanel("lede_text"),
        FieldPanel("cta_link"),
        FieldPanel("body"),
    ]

    translatable_fields = AbstractArticlePage.translatable_fields + [
        SynchronizedField("hero_image"),
        TranslatableField("hero_image_alt_text"),
        TranslatableField("lede_text"),
        TranslatableField("cta_link"),
        TranslatableField("body"),
    ]

    search_fields = AbstractArticlePage.search_fields + [
        index.SearchField("lede_text", boost=6),
        index.SearchField("hero_image_alt_text", boost=2),
    ]

    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Gallery Hub Project Page"

    template = "patterns/pages/gallery_hub/project_page.html"

    # TODO common enough pattern to generalize with other article pages (i.e. NothingPersonalArticlePage)?
    def get_latest_projects(self):
        """
        Returns the 2 latest `Project` objects.
        Uses current locale if available, falls back to default locale.
        """

        current_locale = self.locale
        default_locale = Locale.get_default()

        default_projects = (
            ProjectPage.objects.live()
            .public()
            .filter(locale=default_locale)
            .exclude(id=self.id)
            .order_by("-first_published_at")[:2]
        )

        # Get the best available version for each project
        localized_results = []
        for project in default_projects:
            best_version = project.get_translation(locale=current_locale)
            if best_version and best_version.live:
                localized_results.append(best_version)

        return localized_results

    def get_context(self, request):
        context = super().get_context(request)
        context["latest_projects"] = self.get_latest_projects()
        return context
