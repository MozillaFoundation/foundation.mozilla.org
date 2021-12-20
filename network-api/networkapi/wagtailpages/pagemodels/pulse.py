from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet


@register_snippet
class PulseFilter(ClusterableModel):
    name = models.CharField(
        help_text='Identify this filter for other editors.',
        max_length=255,
        unique=True,
    )
    filter_key = models.CharField(
        choices=[
            ('profile_type', 'Profile Type'),
            ('program_type', 'Program Type'),
            ('program_year', 'Program Year'),
        ],
        help_text='The profile detail to filter on.',
        max_length=255,
    )
    filter_key_label = models.CharField(
        help_text='A label for when displaying the filter type to users. (e.g. "Spaces" for program types)',
        max_length=255,
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('filter_key'),
        FieldPanel('filter_key_label'),
        InlinePanel('options', label='Options', min_num=1),
    ]

    def __str__(self):
        return self.name


class PulseFilterOption(models.Model):
    pulse_filter = ParentalKey(
        'wagtailpages.PulseFilter',
        related_name='options',
    )
    filter_value = models.CharField(
        help_text=(
            'The exact value to filter by in the directory;'
            ' e.g. "staff", "mozfest ambassador", "mozfest wrangler" for profile types.'
        ),
        max_length=255,
    )
    filter_label = models.CharField(
        help_text=(
            'The label to display on the tabs;'
            ' e.g. "Facilitators", "Ambassadors", "Wranglers" for profile types.'
        ),
        max_length=255,
    )
    enable_subfiltering = models.BooleanField(
        blank=True,
        default=True,
        help_text='Display additional filtering options if available.',
    )

    panels = [
        FieldPanel('filter_value'),
        FieldPanel('filter_label'),
        FieldPanel('enable_subfiltering'),
    ]

    def __str__(self):
        return self.filter_label
