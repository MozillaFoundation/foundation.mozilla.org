from datetime import date

from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms.widgets import SelectDateWidget
from django.utils import timezone

from foundation_cms.legacy_apps.news.models import News


class NewsAdminForm(forms.ModelForm):
    date = forms.DateField(
        widget=SelectDateWidget(
            years=range(date.today().year + 3, date.today().year - 8, -1),
        ),
        initial=lambda: date.today(),
        help_text="Publish date of the media",
    )

    publish_after = forms.SplitDateTimeField(
        widget=AdminSplitDateTime,
        initial=lambda: timezone.now(),
        help_text="Make this news visible only " "after this date and time (UTC)",
    )

    class Meta:
        model = News
        fields = (
            "headline",
            "outlet",
            "date",
            "link",
            "excerpt",
            "author",
            "thumbnail",
            "is_video",
            "publish_after",
            "expires",
        )
        labels = {
            "is_video": "Is Video?",
        }
