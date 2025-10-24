from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from wagtail import blocks


class BaseBlock(blocks.StructBlock):
    """
    Theme-aware base block that takes an optional
    `skip_default_wrapper` argument (default False).
    """

    def __init__(self, *args, skip_default_wrapper: bool = False, **kwargs):
        self._skip_default_wrapper = bool(skip_default_wrapper)
        super().__init__(*args, **kwargs)

    def get_theme(self, context):
        page = context.get("page")
        if hasattr(page, "get_theme"):
            return page.get_theme()
        return context.get("theme", "default")

    def get_template(self, context=None):
        theme = self.get_theme(context or {})
        template_name = self.meta.template_name
        themed_path = f"patterns/blocks/themes/{theme}/{template_name}"

        # Check if the themed template exists.
        try:
            get_template(themed_path)
            return themed_path
        # If not, return the default template.
        except TemplateDoesNotExist:
            return f"patterns/blocks/themes/default/{template_name}"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        if self._skip_default_wrapper:
            context["skip_default_wrapper"] = True
        return context

    def deconstruct(self):
        """
        Recommended when introducing custom arguments into the constructor. See:
        https://docs.wagtail.org/en/stable/advanced_topics/customization/streamfield_blocks.html#handling-block-definitions-within-migrations
        """
        path, args, kwargs = super().deconstruct()
        if self._skip_default_wrapper:
            kwargs["skip_default_wrapper"] = True
        return path, args, kwargs

    class Meta:
        abstract = True
        template_name = None
