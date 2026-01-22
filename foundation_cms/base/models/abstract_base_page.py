import re

from django.apps import apps
from django.db import models
from django.template.loader import select_template
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TagBase, TaggedItemBase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Locale, Page
from wagtail.snippets.models import register_snippet
from wagtail_ab_testing.models import AbTest
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.blocks.block_registry import BlockRegistry
from foundation_cms.mixins.foundation_metadata import FoundationMetadataPageMixin

BASE_BLOCK_NAMES = sorted(
    [
        "rich_text",
        "image",
        "podcast_block",
        "tabbed_content",
        "two_column_container_block",
        "link_button_block",
        "portrait_card_set_block",
        "spotlight_card_set_block",
        "spacer_block",
        "iframe_block",
        "impact_numbers",
        "newsletter_signup",
        "newsletter_unsubscribe",
        "timely_activations_cards",
        "quote",
        "list_block",
        "video_block",
        "pillar_card_set",
        "featured_card_block",
        "fru_element_block",
        "divider",
        "title_block",
    ]
)


# Shared StreamField block types for use across pages that inherit from AbstractBasePage.
# Extend this list in specific page models (e.g., HomePage) to add more blocks as needed.
base_page_block_options = BlockRegistry.get_blocks(BASE_BLOCK_NAMES)


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(
        get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="author_image"
    )
    bio = models.TextField(blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("image"),
        FieldPanel("bio"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Authors"


@register_snippet
class Topic(TagBase):
    free_tagging = False
    description = models.TextField(blank=True, help_text="Optional description shown on topic listing page.")

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    class Meta:
        verbose_name = "Page Topic"
        verbose_name_plural = "Page Topics"

    def get_topic_listing_url(self):
        return f"/topics/{self.slug}/"


class AbstractBasePage(FoundationMetadataPageMixin, Page):
    theme = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[("default", "Default"), ("nothing_personal", "Nothing Personal")],
        help_text="Optional. If unset, theme will be inherited from section root.",
    )
    body = StreamField(
        base_page_block_options,
        use_json_field=True,
        blank=True,
    )
    topics = ClusterTaggableManager(
        through="base.PageTopic",
        blank=True,
        verbose_name="Page Topics",
        help_text=(
            "Add one or more existing topics. Start typing to search, then press “Down” arrow "
            "on your keyboard to select topic. If topic is unavailable check if Topic exists by "
            "going to the left side-nav to Snippet > Page Topics > Check if topic exists. "
            "If not, click “Add new page topics”."
        ),
    )
    author = models.ForeignKey(
        "base.Author",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_pages",
    )

    promote_panels = FoundationMetadataPageMixin.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel("author"),
                FieldPanel("topics"),
            ],
            heading="Additional Metadata",
        )
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel("theme"),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
        SynchronizedField("author"),
        SynchronizedField("topics"),
        # Content tab fields
        TranslatableField("title"),
        # Settings tab fields
        SynchronizedField("theme"),
    ]

    class Meta:
        abstract = True

    def get_theme(self):
        # per-instance memoize for this render
        if hasattr(self, "_resolved_theme"):
            return self._resolved_theme

        # return if theme is explicitly set on this page
        if self.theme:
            self._resolved_theme = self.theme
            return self._resolved_theme

        # walk up nearest-first ancestor to try to find a theme
        ancestors = self.get_ancestors(inclusive=False).select_related("content_type").defer_streamfields()

        for ancestor in reversed(ancestors):
            sp = ancestor.specific
            if isinstance(sp, AbstractBasePage):
                theme = getattr(sp, "theme", None)
                if theme:
                    self._resolved_theme = theme
                    return theme

        # default theme is fallback
        self._resolved_theme = "default"
        return self._resolved_theme

    def themed_template_names(self, base_template: str) -> list[str]:
        """
        Build a ordered list of page templates. Order matters since wagtail will render the first one it finds.
        `base_template` can be a full default path (e.g. "patterns/pages/core/general_page.html")
        or just a filename (e.g. "general_page.html").
        """
        filename = base_template.rsplit("/", 1)[-1]
        theme = self.get_theme()

        return [
            f"patterns/pages/themes/{theme}/{filename}",
            (base_template if "/" in base_template else f"patterns/pages/core/{filename}"),
        ]

    def get_template(self, request, *args, **kwargs):
        return self.themed_template_names(self.template)

    def get_preview_template(self, request, mode_name):
        return self.get_template(request)

    def get_donate_banner(self, request):
        return self.get_sitewide_ab_tested_content(
            request,
            page_model=("core", "SitewideDonateBannerPage"),
            field_name="donate_banner",
        )

    def get_footer_newsletter_signup(self, request):
        return self.get_sitewide_ab_tested_content(
            request,
            page_model=("core", "SitewideFooterNewsletterSignupPage"),
            field_name="newsletter_signup",
        )

    def get_sitewide_ab_tested_content(self, request, page_model, field_name):
        app_label, model_name = page_model
        SitewidePageModel = apps.get_model(app_label, model_name)

        # Check if the sitewide page exists (using the default locale).
        default_locale = Locale.get_default()
        page = SitewidePageModel.objects.filter(locale=default_locale).first()

        # If there is no page, return None.
        if not page:
            return None

        # Get the field we want from the page (e.g. donate_banner or newsletter_signup).
        field_value = getattr(page, field_name)

        # If the field is not set on the page, return None.
        if not field_value:
            return None

        # Check if the user has Do Not Track enabled by inspecting the DNT header.
        dnt_enabled = request.headers.get("DNT") == "1"

        # Default values (whats served if there is no AB test or DNT is enabled).
        served_value = field_value
        variant_version = "N/A"
        active_ab_test_name = "N/A"

        # If DNT is NOT enabled, we are allowed to run A/B tests.
        if not dnt_enabled:
            # Check if there is an active A/B test attached to this page.
            active_ab_test = AbTest.objects.filter(
                page=page,
                status=AbTest.STATUS_RUNNING,
            ).first()

            if active_ab_test:
                # Check for the cookie related to this A/B test.
                test_cookie_name = f"wagtail-ab-testing_{active_ab_test.id}_version"
                test_version = request.COOKIES.get(test_cookie_name)

                # If no version cookie is found, grab a test version for the current user.
                if not test_version:
                    test_version = active_ab_test.get_new_participant_version()

                # Determine whether the user is seeing the variant.
                if test_version == "variant":
                    is_variant = True
                else:
                    is_variant = False

                # Attach active test and variant flag to the request for
                # the {% wagtail_ab_testing_script %} template tag.
                request.wagtail_ab_testing_test = active_ab_test
                request.wagtail_ab_testing_serving_variant = is_variant

                # If the user is supposed to be served the variant, pull the value from the variant revision.
                if is_variant:
                    variant_page = active_ab_test.variant_revision.as_object()
                    served_value = getattr(variant_page, field_name)

                variant_version = test_version
                active_ab_test_name = active_ab_test.name

        # Localize the returned value and attach metadata.
        content = served_value.localized
        content.variant_version = variant_version
        content.active_ab_test = active_ab_test_name

        # Only the donate banner needs CTA button data.
        if field_name == "donate_banner":
            content.cta_button_data = {
                "donate-banner-cta-button": "",  # flag for JS event listeners
            }

        return content

    def get_context(self, request):
        context = super().get_context(request)
        theme = self.get_theme()
        context["theme"] = theme
        context["theme_base"] = select_template(
            [
                f"base/themes/{theme}/base.html",
                "base/base.html",
            ]
        ).template.name
        context["donate_banner"] = self.get_donate_banner(request)
        context["footer_newsletter_signup"] = self.get_footer_newsletter_signup(request)
        context["page_type_bem"] = self._to_bem_case(self.specific_class.__name__)
        context["theme_class_bem"] = self._to_bem_case(theme) if theme else ""
        return context

    def _to_bem_case(self, name):
        """Convert CamelCase to kebab-case"""
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
        """ Replace underscore with just dash """
        s1 = s1.replace("_", "-")
        return re.sub("([a-z0-9])([A-Z])", r"\1-\2", s1).lower()


class PageTopic(TaggedItemBase):
    """
    Through model connecting a Page to a Topic.
    """

    # must be named 'tag' for django-taggit to work.
    tag = models.ForeignKey(Topic, related_name="page_relations", on_delete=models.CASCADE)
    content_object = ParentalKey(to="wagtailcore.Page", on_delete=models.CASCADE, related_name="topic_relations")
