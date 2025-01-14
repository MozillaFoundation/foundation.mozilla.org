from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from foundation_cms.blog.models import BlogPage


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Add live blog pages to the context
        context['blogs'] = BlogPage.objects.live().order_by('-first_published_at')
        return context