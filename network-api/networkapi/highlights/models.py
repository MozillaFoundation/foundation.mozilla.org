from django.utils import timezone
from django.db import models
from django.db.models import Q
from adminsortable.models import SortableMixin
from wagtail.core.fields import RichTextField
from networkapi.utility.images import get_image_upload_path
from wagtail.snippets.models import register_snippet


def get_highlights_image_upload_path(instance, filename):
    return get_image_upload_path(
        app_name='highlights',
        prop_name='title',
        instance=instance,
        current_filename=filename
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


@register_snippet
class Highlight(SortableMixin):
    """
    An data type to highlight things like pulse
    projects, custom pages, etc
    Especially on the homepage under "Get Involved"
    """
    title = models.CharField(
        max_length=300,
        help_text='Title of the higlight',
    )
    description = models.TextField(
        max_length=5000,
        help_text='Description of the higlight',
    )
    link_label = models.CharField(
        max_length=300,
        help_text='Text to show that links to this higlight\'s '
                  'details page',
    )
    link_url = models.URLField(
        max_length=2048,
        help_text='Link to this higlight\'s details page',
    )
    image = models.FileField(
        max_length=2048,
        help_text='Image representing this highlight',
        upload_to=get_highlights_image_upload_path,
        blank=True,
    )
    footer = RichTextField(
        "footer",
        help_text="Content to appear after description (view more projects "
        "link or something similar)",
        null=True,
    )
    publish_after = models.DateTimeField(
        help_text='Make this highlight visible only '
                  'after this date and time (UTC)',
        null=True,
    )
    expires = models.DateTimeField(
        help_text='Hide this highlight after this date and time (UTC)',
        default=None,
        null=True,
        blank=True,
    )
    order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True,
    )

    objects = HighlightQuerySet.as_manager()

    class Meta:
        verbose_name_plural = 'highlights'
        ordering = ('order',)

    def __str__(self):
        return str(self.title)
