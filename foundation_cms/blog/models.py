from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from foundation_cms.profiles.models import Profile


class BlogIndexPage(Page):
    """
    BlogIndexPage serves as a parent for BlogPage instances.

    TODO: FUTURE IMPLEMENTATION NOTES
    When implementing the real blog functionality, this model should be updated to:

    1. Inherit from any of our base models(such as AbstractBasePage, AbstractArticlePage) instead of Page directly:

    2. Review and potentially remove/modify current fields that may conflict.

    3. Add appropriate search_fields once inheriting from base models, for example:
       search_fields = AbstractBasePage.search_fields + [
           index.SearchField("body", boost=4),
           # Additional blog-specific search fields
       ]
    """

    subpage_types = ["blog.BlogPage"]  # Restrict child pages to BlogPage only
    body = RichTextField(blank=True, help_text="Main content of the blog index page")

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_context(self, request):
        # Get all live blog pages that are children of this page
        blogs = BlogPage.objects.live().descendant_of(self).order_by("-first_published_at")

        # Update template context
        context = super().get_context(request)

        context["blogs"] = blogs
        return context

    class Meta:
        verbose_name = "Blog Index Page (new)"


class BlogPage(Page):
    """
    BlogPage represents individual blog entries.
    """

    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL, related_name="blogs")
    body = RichTextField(blank=True, help_text="Main content of the blog")

    parent_page_types = ["blog.BlogIndexPage"]  # Restrict parent to BlogIndexPage only

    content_panels = Page.content_panels + [
        FieldPanel("author"),
        FieldPanel("body"),
    ]

    def author_name(self):
        return self.author.title if self.author else "Mozilla Foundation"

    class Meta:
        verbose_name = "Blog Page (new)"
