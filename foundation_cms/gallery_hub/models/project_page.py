import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TagBase, TaggedItemBase
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.images import get_image_model_string
from wagtail.models import Locale, Orderable, TranslatableMixin
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.core.panels.media_panel import MediaPanel
from foundation_cms.mixins.hero_media import HeroMediaMixin
from foundation_cms.validators import validate_vimeo_mp4_url

VIMEO_MP4_HELP_TEXT = (
    "Log into Vimeo using 1Password and upload the desired video. "
    "Then select the video and click '...', 'Video File Links', "
    "and select '(mp4, 1920 x 1080)'. Copy and paste the link here."
)


def current_year():
    return datetime.date.today().year


class ProjectPageHeroMedia(TranslatableMixin, Orderable):
    MEDIA_TYPE_IMAGE = "image"
    MEDIA_TYPE_VIDEO = "video"

    page = ParentalKey(
        "gallery_hub.ProjectPage",
        related_name="hero_gallery_media",
        on_delete=models.CASCADE,
    )
    media_type = models.CharField(
        max_length=25,
        choices=[
            (MEDIA_TYPE_IMAGE, "Image or GIF"),
            (MEDIA_TYPE_VIDEO, "Video"),
        ],
        default=MEDIA_TYPE_IMAGE,
        verbose_name="Media type",
    )
    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image or poster image",
        help_text="Image/GIF for image media, or optional poster image for video media.",
    )
    video_url = models.CharField(
        blank=True,
        max_length=500,
        validators=[validate_vimeo_mp4_url],
        verbose_name="Video URL",
        help_text=VIMEO_MP4_HELP_TEXT,
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Alt Text",
        help_text="Descriptive text for screen readers. Leave blank to use the image's default title.",
    )
    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Caption",
        help_text="Optional caption displayed beneath this hero gallery media item.",
    )

    panels = [
        FieldPanel("media_type"),
        FieldPanel("image"),
        FieldPanel("video_url"),
        FieldPanel("alt_text"),
        FieldPanel("caption"),
    ]

    translatable_fields = [
        SynchronizedField("media_type"),
        SynchronizedField("image"),
        SynchronizedField("video_url"),
        TranslatableField("alt_text"),
        TranslatableField("caption"),
    ]

    def clean(self):
        super().clean()

        errors = {}

        if self.media_type == self.MEDIA_TYPE_IMAGE and not self.image:
            errors["image"] = "Image or GIF media requires an image."

        if self.media_type == self.MEDIA_TYPE_VIDEO and not self.video_url:
            errors["video_url"] = "Video media requires a video URL."

        if errors:
            raise ValidationError(errors)

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        verbose_name = "Hero Gallery Media"
        verbose_name_plural = "Hero Gallery Media"


class ProjectPage(AbstractArticlePage, HeroMediaMixin):
    hero_image_caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Caption",
        help_text="Caption displayed beneath the primary hero image.",
    )

    project_link = models.URLField(
        blank=True,
        verbose_name="Project link",
        help_text="External URL for the project. Include https:// or http://.",
    )

    program_label = ClusterTaggableManager(
        through="gallery_hub.ProjectPageProgramLabel",
        blank=True,
        verbose_name="Program Label",
        help_text=(
            "Add one or more existing program labels. Start typing to search, then press “Down” arrow "
            "on your keyboard to select program label. If program label is unavailable check if it exists by "
            "going to the left side-nav to Snippet > Program Labels > Check if program label exists. "
            "If not, click “Add new program label”."
        ),
    )

    program_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(current_year())],
        default=current_year,
        help_text="Enter a four-digit year.",
    )

    expert = models.ForeignKey(
        "profiles.ExpertProfilePage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="gallery_projects",
    )

    content_panels = AbstractArticlePage.content_panels + [
        MediaPanel.create_default(
            heading="Hero Gallery",
            classname="collapsible",
            trigger_field="displayed_hero_content",
            image_field="hero_image",
            video_field="hero_video_url",
        ),
        MultiFieldPanel(
            [
                FieldPanel("hero_image_caption"),
                InlinePanel("hero_gallery_media", label="Additional Hero Media", max_num=10),
            ],
            heading="Additional Hero Gallery Media",
            classname="collapsible",
        ),
        FieldPanel("program_label"),
        FieldPanel("program_year"),
        FieldPanel("project_link"),
        FieldPanel("lede_text"),
        PageChooserPanel("expert", "profiles.ExpertProfilePage"),
        FieldPanel("body"),
    ]

    translatable_fields = AbstractArticlePage.translatable_fields + [
        SynchronizedField("displayed_hero_content"),
        SynchronizedField("hero_image"),
        TranslatableField("hero_image_alt_text"),
        SynchronizedField("hero_video_url"),
        TranslatableField("hero_image_caption"),
        SynchronizedField("hero_gallery_media"),
        TranslatableField("body"),
        SynchronizedField("expert"),
        SynchronizedField("project_link"),
        TranslatableField("lede_text"),
    ]

    search_fields = AbstractArticlePage.search_fields + [
        index.SearchField("lede_text", boost=6),
        index.SearchField("hero_image_alt_text", boost=2),
        index.SearchField("hero_image_caption", boost=2),
        index.RelatedFields(
            "hero_gallery_media",
            [
                index.SearchField("alt_text", boost=2),
                index.SearchField("caption", boost=2),
            ],
        ),
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


@register_snippet
class ProgramLabel(TagBase):
    free_tagging = False
    description = models.TextField(blank=True, help_text="Optional program label for a project page.")

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    class Meta:
        verbose_name = "Program Label"
        verbose_name_plural = "Program Labels"


class ProjectPageProgramLabel(TaggedItemBase):
    tag = models.ForeignKey(
        ProgramLabel,
        related_name="tagged_projects",
        on_delete=models.CASCADE,
    )
    content_object = ParentalKey(
        "gallery_hub.ProjectPage",
        related_name="program_label_items",
        on_delete=models.CASCADE,
    )
