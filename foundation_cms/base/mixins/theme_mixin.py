from django.db import models

class ThemedPageMixin:
    theme = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[("default", "Default"), ("magazine", "Magazine")],
        help_text="Optional. If unset, theme will be inherited from section root."
    )

    def get_theme(self):
        if self.theme:
            return self.theme

        # Traverse ancestors to find a page with an explicitly set theme
        for ancestor in reversed(self.get_ancestors(inclusive=False).live()):
            if hasattr(ancestor, "theme") and ancestor.theme:
                return ancestor.theme

        return "default"