from django.forms import Media
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class MediaPanel(MultiFieldPanel):
    """MultiFieldPanel using Stimulus controller"""

    def __init__(self, children, trigger_field="displayed_hero_content", **kwargs):
        self.trigger_field = trigger_field
        # Remove custom kwargs to avoid issues with MultiFieldPanel
        kwargs.pop("image_field", None)
        kwargs.pop("video_field", None)
        super().__init__(children, **kwargs)

    @classmethod
    def create_default(cls, **kwargs):
        """Factory method to create a default MediaPanel instance."""
        from foundation_cms.mixins.hero_media import HeroMediaMixin

        kwargs.setdefault("heading", "Media Section")
        kwargs.setdefault("classname", "collapsible")
        kwargs.setdefault("trigger_field", "content")
        kwargs.setdefault("image_field", "image")
        kwargs.setdefault("video_field", "video_url")

        trigger_field = kwargs["trigger_field"]
        image_field = kwargs["image_field"]
        alt_text_field = image_field + "_alt_text"
        video_field = kwargs["video_field"]

        children = [
            FieldPanel(trigger_field),
            FieldPanel(
                image_field,
                attrs={"data-media-target": "field", "data-condition": HeroMediaMixin.HERO_CONTENT_IMAGE},
            ),
            FieldPanel(
                alt_text_field,
                attrs={"data-media-target": "field", "data-condition": HeroMediaMixin.HERO_CONTENT_IMAGE},
            ),
            FieldPanel(
                video_field,
                attrs={"data-media-target": "field", "data-condition": HeroMediaMixin.HERO_CONTENT_VIDEO},
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
            <div data-controller="media"
                 data-media-trigger-field-value="{self.panel.trigger_field}">
                {inner_html}
            </div>
            """
            )
