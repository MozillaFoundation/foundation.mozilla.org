from django.db import models
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField, StreamField
from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from modelcluster.fields import ParentalKey
from .blocks import ResearcherRoleBlock, BlogAuthorRoleBlock, GranteeRoleBlock

@register_snippet
class Profile(models.Model):
    """
    Profile snippet with a StreamField for dynamic roles.
    """
    title = models.CharField(max_length=255)
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    roles = StreamField(
        [
            ("researcher", ResearcherRoleBlock(label="Researcher Role", max_num=1)),
            ("blog_author", BlogAuthorRoleBlock(label="Blog Author Role", max_num=1)),
            ("grantee", GranteeRoleBlock(label="Grantee Role", max_num=1)),
        ],
        block_counts= {
            "researcher":{'max_num': 1},
            "blog_author":{'max_num': 1},
            "blog_author":{'max_num': 1},
        },
        blank=True,
        use_json_field=True,
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("image"),
        FieldPanel("roles"),
    ]

    def __str__(self):
        return self.title
    
class ProfilePage(Page):
    """
    Public-facing page for profiles.
    """
    profile = models.OneToOneField(
        "profiles.Profile", null=True, blank=True, on_delete=models.SET_NULL, related_name="profile_page"
    )
    bio = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("profile"),
        FieldPanel("bio"),
    ]

    def __str__(self):
        return self.title