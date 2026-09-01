from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from wagtail import blocks
from wagtail.models import Page

from foundation_cms.base.models.base_block import BaseBlock

EXPERT_PROFILE_ARTICLE_LIMIT = 9
EXPERT_PROFILE_LINK_ROW_LIMIT = 10


def _localized_public_page(page):
    if not page:
        return None

    localized_page = page.localized
    return Page.objects.live().public().filter(pk=localized_page.pk).specific().first()


class ManualProjectBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255)
    description = blocks.TextBlock(required=False, max_length=600)
    url = blocks.URLBlock(
        required=True,
        help_text="Enter a full URL including http:// or https://",
    )
    link_label = blocks.CharBlock(
        required=False,
        max_length=80,
        help_text="Optional link label. Defaults to Learn more.",
    )

    class Meta:
        icon = "link"
        label = "Manual project"


class ProjectsSectionBlock(BaseBlock):
    SOURCE_CURATED = "curated"
    SOURCE_RELATED = "related"

    source = blocks.ChoiceBlock(
        choices=[
            (SOURCE_CURATED, "Curated projects"),
            (SOURCE_RELATED, "Projects related to this expert"),
        ],
        default=SOURCE_CURATED,
        help_text=(
            "Curated projects use the ordered items below. Related projects are selected automatically "
            "from projects assigned to this expert."
        ),
    )
    items = blocks.StreamBlock(
        [
            (
                "cms_project",
                blocks.PageChooserBlock(
                    required=True,
                    page_type="gallery_hub.ProjectPage",
                    label="Mozilla Foundation project",
                ),
            ),
            ("manual_project", ManualProjectBlock()),
        ],
        required=False,
        help_text="Add Mozilla Foundation or manual projects in display order.",
    )

    def clean(self, value):
        cleaned = super().clean(value)
        source = cleaned.get("source")
        items = cleaned.get("items")
        errors = {}

        if source == self.SOURCE_CURATED and not items:
            errors["items"] = ErrorList([ValidationError("Add at least one curated project.")])
        elif source == self.SOURCE_RELATED and items:
            errors["items"] = ErrorList(
                [ValidationError("Remove curated items when using automatically related projects.")]
            )

        if errors:
            raise blocks.StructBlockValidationError(block_errors=errors)

        return cleaned

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        rendered_items = []

        if value.get("source") == self.SOURCE_RELATED:
            page = context.get("page")
            if page:
                rendered_items = [
                    {
                        "type": "cms_project",
                        "value": {"project": project},
                    }
                    for project in page.get_related_projects()
                ]
        else:
            for item in value.get("items", []):
                if item.block_type == "cms_project":
                    project = _localized_public_page(item.value)
                    if project:
                        rendered_items.append(
                            {
                                "type": "cms_project",
                                "value": {"project": project},
                            }
                        )
                else:
                    rendered_items.append({"type": "manual_project", "value": item.value})

        context["rendered_items"] = rendered_items
        return context

    class Meta:
        icon = "image"
        label = "Projects section"
        template_name = "expert_profile_projects_section_block.html"


class ManualArticleBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255)
    description = blocks.TextBlock(required=False, max_length=600)
    url = blocks.URLBlock(
        required=True,
        help_text="Enter a full URL including http:// or https://",
    )

    class Meta:
        icon = "link"
        label = "Manual article"


class ArticlesSectionBlock(BaseBlock):
    visible_count = 3

    items = blocks.StreamBlock(
        [
            (
                "cms_article",
                blocks.PageChooserBlock(
                    required=True,
                    page_type="nothing_personal.NothingPersonalArticlePage",
                    label="Mozilla Foundation article",
                ),
            ),
            ("manual_article", ManualArticleBlock()),
        ],
        min_num=1,
        max_num=EXPERT_PROFILE_ARTICLE_LIMIT,
        help_text="Add up to 9 Mozilla Foundation or manual articles in display order.",
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        rendered_items = []

        for item in value.get("items", []):
            if item.block_type == "cms_article":
                article = _localized_public_page(item.value)
                if article:
                    rendered_items.append({"type": "cms_article", "value": article})
            else:
                rendered_items.append({"type": "manual_article", "value": item.value})

        context["rendered_items"] = rendered_items
        context["visible_count"] = self.visible_count
        return context

    class Meta:
        icon = "doc-full"
        label = "Articles section"
        template_name = "expert_profile_articles_section_block.html"


class LinkRowBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255)
    description = blocks.TextBlock(required=False, max_length=600)
    url = blocks.URLBlock(
        required=False,
        help_text="Optional full URL including http:// or https://",
    )

    class Meta:
        icon = "link"
        label = "Link row"


class LinkSectionBlock(BaseBlock):
    heading = blocks.CharBlock(required=True, max_length=255)
    rows = blocks.StreamBlock(
        [("link", LinkRowBlock())],
        min_num=1,
        max_num=EXPERT_PROFILE_LINK_ROW_LIMIT,
        help_text="Add between 1 and 10 rows in display order. A URL is optional.",
    )

    class Meta:
        icon = "list-ul"
        label = "Link section"
        template_name = "expert_profile_link_section_block.html"
