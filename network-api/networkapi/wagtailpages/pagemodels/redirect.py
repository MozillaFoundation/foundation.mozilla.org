from django.db import models
from django.http import HttpResponseRedirect

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page


class RedirectingPage(Page):
    URL = models.URLField(
        help_text='The fully qualified URL that this page should map to.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('URL'),
    ]

    show_in_menus_default = True

    def serve(self, request):
        # Note that due to how this page type works, there is no
        # associated template file in the wagtailpages directory.
        return HttpResponseRedirect(self.URL)
