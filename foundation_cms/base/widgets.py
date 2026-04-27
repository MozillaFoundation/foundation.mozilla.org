from django import forms
from django.apps import apps
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class TopicSelectWidget(forms.Widget):
    """
    Tag-picker widget for ClusterTaggableManager fields with free_tagging=False.
    Renders a chip bar with a searchable dropdown of available Topic snippets.
    Use with: FieldPanel("topics", widget=TopicSelectWidget)
    """

    template_name = "patterns/admin/topic_select.html"

    class Media:
        css = {"all": ("wagtailadmin/css/topic-select-widget.css",)}
        js = ("wagtailadmin/js/topic-select-widget.js",)

    def value_from_datadict(self, data, files, name):
        return data.get(name, "")

    def render(self, name, value, attrs=None, renderer=None):
        # Use render_to_string instead of Django's widget renderer, which uses
        # its own isolated template engine that can't find project templates.
        context = self.get_context(name, value, attrs)
        return mark_safe(render_to_string(self.template_name, context))

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        selected = self.parse_selected(value)
        all_topics = list(apps.get_model("base", "Topic").objects.order_by("name").values_list("name", flat=True))
        hidden_value = ", ".join(f'"{t}"' if "," in t else t for t in selected)
        context["widget"].update(
            {
                "selected": selected,
                "all_topics": all_topics,
                "hidden_value": hidden_value,
                "placeholder": "" if selected else "Select topics…",
            }
        )
        return context

    @staticmethod
    def parse_selected(value):
        """Parse a taggit comma-separated string or list into a list of topic names."""
        if isinstance(value, str):
            return [v.strip().strip('"') for v in value.split(",") if v.strip()]
        if isinstance(value, list):
            return [str(v) for v in value if v]
        return []
