from django.db import models
from mezzanine.pages.models import Page
from mezzanine.core.fields import RichTextField


class Petition(models.Model):
    title = models.CharField(
        max_length=100,
        help_text="Identify this component for other editors",
    )

    header = models.CharField(
        max_length=500,
        help_text="Signup heading that will display on page"
    )

    description = RichTextField(
        "description",
        help_text="Body of signup component"
    )

    newsletter = models.CharField(
        max_length=100,
        help_text="The (pre-existing) SalesForce newsletter to sign up for",
        default="mozilla-leadership-network"
    )

    google_forms_url = models.URLField(
        help_text="Google form to post petition data to",
        max_length=2048,
        null=True
    )

    checkbox_1 = models.CharField(
        max_length=1024,
        help_text="label for the first checkbox option (may contain HTML)",
        blank=True
    )

    checkbox_2 = models.CharField(
        max_length=1024,
        help_text="label for the second checkbox option (may contain HTML)",
        blank=True
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = 'petition widgets'
        verbose_name = 'petition widget'


class Campaign(Page):

    header = models.CharField(
        max_length=500,
        help_text="Page title, appears above content",
    )

    content = RichTextField("Main body content")

    petition = models.ForeignKey(
        Petition,
        related_name='page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Choose existing or create new petition form",
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Custom Campaign Page'
        verbose_name_plural = 'Custom Campaign Pages'
