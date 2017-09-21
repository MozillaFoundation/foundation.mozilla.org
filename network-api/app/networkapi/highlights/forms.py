from django import forms
from django.utils import timezone
from django.contrib.admin.widgets import AdminSplitDateTime

from networkapi.highlights.models import Highlight


class HighlightAdminForm(forms.ModelForm):
    publish_after = forms.SplitDateTimeField(
        widget=AdminSplitDateTime,
        initial=lambda: timezone.now(),
        help_text='Make this highlight visible only '
                  'after this date and time (UTC)',
    )

    class Meta:
        model = Highlight
        fields = (
            'title',
            'description',
            'link_label',
            'link_url',
            'image',
            'footer',
            'publish_after',
            'expires',
        )
