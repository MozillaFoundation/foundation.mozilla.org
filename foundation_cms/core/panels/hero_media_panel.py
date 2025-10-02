from django.forms import Media
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class HeroMediaPanel(MultiFieldPanel):
    """MultiFieldPanel using Stimulus controller"""

    def __init__(self, children, trigger_field="displayed_hero_content", **kwargs):
        self.trigger_field = trigger_field
        super().__init__(children, **kwargs)

    @classmethod
    def create_default(cls, **kwargs):
        """Factory method to create a default HeroMediaPanel instance."""
        from foundation_cms.mixins.hero_media import HeroMediaMixin

        kwargs.setdefault("heading", "Hero Section")
        kwargs.setdefault("classname", "collapsible")

        children = [
            FieldPanel("displayed_hero_content"),
            FieldPanel(
                "hero_image",
                attrs={"data-hero-media-target": "field", "data-condition": HeroMediaMixin.HERO_CONTENT_IMAGE},
            ),
            FieldPanel(
                "hero_image_alt_text",
                attrs={"data-hero-media-target": "field", "data-condition": HeroMediaMixin.HERO_CONTENT_IMAGE},
            ),
            FieldPanel(
                "hero_video_url",
                attrs={"data-hero-media-target": "field", "data-condition": HeroMediaMixin.HERO_CONTENT_VIDEO},
            ),
        ]

        return cls(children, **kwargs)

    class BoundPanel(MultiFieldPanel.BoundPanel):
        @property
        def media(self):
            return super().media + Media(js=[static("foundation_cms/_js/admin_controllers.compiled.js")])

        def render_html(self, parent_context):
            inner_html = super().render_html(parent_context)

            return mark_safe(
                f"""
            <div data-controller="hero-media"
                 data-hero-media-trigger-field-value="{self.panel.trigger_field}">
                {inner_html}
            </div>
            """
            )
