from wagtail import blocks
from wagtail.snippets.blocks import SnippetChooserBlock
from foundation_cms.snippets.models.newsletter_signup import NewsletterSignup  
from foundation_cms.base.models.base_block import BaseBlock


class NewsletterSignupBlock(BaseBlock):
    newsletter_signup = SnippetChooserBlock(
        "snippets.NewsletterSignup",
        max_num=1,
    )

    class Meta:
        template_name = "newsletter_signup_block.html"
        icon = "mail"
        label = "Newsletter Signup"
