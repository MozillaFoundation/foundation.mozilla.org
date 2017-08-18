from django.db import models
from mezzanine.pages.models import Page
from mezzanine.core.fields import RichTextField


class Signup(models.Model):
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

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = 'signup widgets'
        verbose_name = 'signup widget'


class LandingPage(Page):

    # featured-image = s3boto3 stuffs

    # featured = models.BooleanField(default=False)

    header = models.CharField(
        max_length=500,
        help_text="Page title, appears above content",
    )

    content = RichTextField("Main body content")

    signup = models.ForeignKey(
        Signup,
        related_name='page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Choose existing or create new mailing list signup form",
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Custom Page'
        verbose_name_plural = 'Custom Pages'
