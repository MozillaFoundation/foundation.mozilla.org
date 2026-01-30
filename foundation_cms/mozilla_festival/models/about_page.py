from foundation_cms.base.models.abstract_general_page import AbstractGeneralPage


class MozfestAboutPage(AbstractGeneralPage):
    parent_page_types = ["mozilla_festival.MozfestHomePage"]

    content_panels = AbstractGeneralPage.content_panels + [
        # Add any additional panels specific to the Mozfest About Page here
    ]

    translatable_fields = AbstractGeneralPage.translatable_fields + [
        # Add any additional translatable fields specific to the Mozfest About Page here
    ]

    template = "patterns/pages/mozilla_festival/about_page.html"

    class Meta:
        verbose_name = "Mozfest About Page"

    def get_context(self, request):
        context = super().get_context(request)
        return context
