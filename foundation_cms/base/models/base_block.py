from wagtail import blocks


class BaseBlock(blocks.StructBlock):
    def get_theme(self, context):
        page = context.get("page")
        if hasattr(page, "get_theme"):
            return page.get_theme()
        return context.get("theme", "default")

    def get_template(self, context=None):
        theme = self.get_theme(context or {})
        return f"patterns/blocks/{theme}/{self.meta.template_name}"

    class Meta:
        abstract = True
        template_name = None
