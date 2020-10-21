from datetime import datetime

from django.db import models

from wagtail.admin.edit_handlers import FieldPanel


class Update(models.Model):
    source = models.URLField(
        max_length=2048,
        help_text='Link to source',
    )

    title = models.CharField(
        max_length=256,
    )

    author = models.CharField(
        max_length=256,
        blank=True,
    )

    featured = models.BooleanField(
        default=False,
        help_text='feature this update at the top of the list?'
    )

    snippet = models.TextField(
        max_length=5000,
        blank=True,
    )

    created_date = models.DateField(
        auto_now=True,
        help_text='The date this product was created',
    )

    panels = [
        FieldPanel('source'),
        FieldPanel('title'),
        FieldPanel('author'),
        FieldPanel('featured'),
        FieldPanel('snippet'),
    ]

    def __str__(self):
        return self.title
