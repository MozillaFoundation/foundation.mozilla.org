from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from wagtail import blocks


class BaseBlock(blocks.StructBlock):
    def get_theme(self, context):
        page = context.get("page")
        if hasattr(page, "get_theme"):
            return page.get_theme()
        return context.get("theme", "default")

    def get_template(self, context=None):
        theme = self.get_theme(context or {})
        template_name = self.meta.template_name
        themed_path = f"patterns/blocks/{theme}/{template_name}"

        # Check if the themed template exists.
        try:
            get_template(themed_path)
            return themed_path
        # If not, return the default template.
        except TemplateDoesNotExist:
            return f"patterns/blocks/{template_name}"

    class Meta:
        abstract = True
        template_name = None
