from adminsortable.models import SortableMixin
from django.db import models
from django.db.models import Q
from django.utils import timezone
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.models import TranslatableMixin
from wagtail.search import index
from wagtail_localize.fields import TranslatableField

from foundation_cms.legacy_apps.utility.images import get_image_upload_path


def get_highlights_image_upload_path(instance, filename):
    return get_image_upload_path(
        app_name="highlights",
        prop_name="title",
        instance=instance,
        current_filename=filename,
    )


class HighlightQuerySet(models.query.QuerySet):
    """
    A QuerySet for highlights that filters for published highlights.
    """

    def published(self):
        now = timezone.now()
        return self.filter(
            Q(expires__gt=now) | Q(expires__isnull=True),
            publish_after__lt=now,
        )


class Highlight(TranslatableMixin, SortableMixin):
    """
    An data type to highlight things like pulse
    projects, custom pages, etc
    Especially on the homepage under "Get Involved"
    """

    title = models.CharField(
        max_length=300,
        help_text="Title of the highlight",
    )
    description = models.TextField(
        max_length=5000,
        help_text="Description of the highlight",
    )
    link_label = models.CharField(
        max_length=300,
        help_text="Text to show that links to this highlight's " "details page",
    )
    link_url = models.URLField(
        max_length=2048,
        help_text="Link to this highlight's details page",
    )
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="+",
    )
    footer = RichTextField(
        "footer",
        help_text="Content to appear after description (view more projects " "link or something similar)",
        null=True,
    )
    publish_after = models.DateTimeField(
        help_text="Make this highlight visible only " "after this date and time (UTC)",
        null=True,
    )
    expires = models.DateTimeField(
        help_text="Hide this highlight after this date and time (UTC)",
        default=None,
        null=True,
        blank=True,
    )
    order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True,
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("link_label"),
        FieldPanel("link_url"),
        FieldPanel("image"),
        FieldPanel("footer"),
        FieldPanel("publish_after"),
        FieldPanel("expires"),
    ]

    translatable_fields = [
        TranslatableField("title"),
        TranslatableField("description"),
        TranslatableField("link_label"),
        TranslatableField("footer"),
    ]

    search_fields = [
        index.SearchField("title", boost=10),
        index.SearchField("link_label"),
        index.FilterField("locale_id"),
    ]

    objects = HighlightQuerySet.as_manager()

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "highlights"
        ordering = ("order",)

    def __str__(self):
        return str(self.title)
