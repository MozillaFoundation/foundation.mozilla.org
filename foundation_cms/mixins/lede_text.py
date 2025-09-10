from django.db import models


class LedeTextMixin(models.Model):
    lede_text = models.TextField(blank=True, help_text="Optional introductory lede text (plain text only).")

    class Meta:
        abstract = True
