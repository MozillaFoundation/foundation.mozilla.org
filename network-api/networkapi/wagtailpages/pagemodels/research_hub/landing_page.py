from django.apps import apps
from wagtail.core import models as wagtail_models
from django.db import models


from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata
from wagtail.admin.edit_handlers import (
    FieldPanel
)

from ...utils import (
    TitleWidget
)

class ResearchLandingPage(foundation_metadata.FoundationMetadataPageMixin, wagtail_models.Page):
    max_count = 1
    subpage_types = [
        'ResearchLibraryPage',
        'ResearchAuthorsIndexPage',
    ]

    intro = models.CharField(
        blank=True,
        max_length=250,
    )

    content_panels = [
        FieldPanel(
            'title',
            classname='full title',
            widget=TitleWidget(attrs={"class": "max-length-warning", "data-max-length": 60})
        ),
        FieldPanel('intro'),

    ]

    def get_context(self, request):
        context = super().get_context(request)
        ResearchLibraryPage = apps.get_model("wagtailpages", "ResearchLibraryPage")
        context['library_page'] = ResearchLibraryPage.objects.first()
        return context
