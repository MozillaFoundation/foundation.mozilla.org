from django.db import models


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

    def __str__(self):
        return self.title
