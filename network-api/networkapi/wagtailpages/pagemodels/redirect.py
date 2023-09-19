from django.db import models
from django.http import HttpResponseRedirect
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page


class RedirectingPage(Page):
    URL = models.URLField(help_text="The fully qualified URL that this page should map to.")

    content_panels = Page.content_panels + [
        FieldPanel("URL"),
    ]

    # This page is deprecated. While we keep the existing pages around,
    # we don't want to create new ones.
    is_creatable = False
    show_in_menus_default = True

    def serve(self, request):
        # Note that due to how this page type works, there is no
        # associated template file in the wagtailpages directory.
        return HttpResponseRedirect(self.URL)
