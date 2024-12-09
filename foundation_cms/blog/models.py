from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import RichTextField


class BlogIndexPage(Page):
    """
    BlogIndexPage serves as a parent for BlogPage instances.
    """
    subpage_types = ['blog.BlogPage']  # Restrict child pages to BlogPage only
    body = RichTextField(blank=True, help_text="Main content of the blog index page")
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    def get_context(self, request):
        # Get all live blog pages that are children of this page
        blogs = BlogPage.objects.live().descendant_of(self).order_by('-first_published_at')

        # Update template context
        context = super().get_context(request)
        context['blogs'] = blogs
        return context

class BlogPage(Page):
    """
    BlogPage represents individual blog entries.
    """
    author = models.CharField(max_length=255, default="Mozilla Foundation", help_text="Author of the blog")
    body = RichTextField(blank=True, help_text="Main content of the blog")

    parent_page_types = ['blog.BlogIndexPage']  # Restrict parent to BlogIndexPage only
    subpage_types = []  # Prevent creating child pages under BlogPage

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "Blog Page"
