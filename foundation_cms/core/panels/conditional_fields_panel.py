from django.utils.html import format_html
from wagtail.admin.panels import MultiFieldPanel


class ConditionalFieldsPanel(MultiFieldPanel):
    """MultiFieldPanel that shows child panels based on the value of a trigger field."""

    def __init__(self, children=(), trigger_field="", **kwargs):
        self.trigger_field = trigger_field
        super().__init__(children, **kwargs)

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs["trigger_field"] = self.trigger_field
        return kwargs

    @staticmethod
    def show_when(*values):
        """Return panel attrs that show the panel only when the trigger field is one of `values`."""
        return {"data-conditional-fields-target": "field", "data-condition": " ".join(values)}

    class BoundPanel(MultiFieldPanel.BoundPanel):
        def render_html(self, parent_context):
            # Hidden inputs stay enabled: a disabled StreamField omits its `-count`
            # input from POST, and StreamBlock.value_from_datadict raises a KeyError.
            return format_html(
                '<div data-controller="conditional-fields" '
                'data-conditional-fields-trigger-field-value="{}" '
                'data-conditional-fields-disable-hidden-value="false">{}</div>',
                self.panel.trigger_field,
                super().render_html(parent_context),
            )
