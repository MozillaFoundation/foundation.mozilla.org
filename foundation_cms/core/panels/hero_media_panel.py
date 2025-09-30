from django.forms import Media
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from wagtail.admin.panels import MultiFieldPanel


class HeroMediaPanel(MultiFieldPanel):
    """MultiFieldPanel using Stimulus controller"""

    def __init__(self, children, trigger_field="displayed_hero_content", **kwargs):
        self.trigger_field = trigger_field
        super().__init__(children, **kwargs)

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
