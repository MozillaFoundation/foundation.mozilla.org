from wagtail import blocks
from wagtail.snippets.blocks import SnippetChooserBlock


class NewsletterSignupBlock(blocks.StructBlock):
    signup = SnippetChooserBlock("wagtailpages.Signup")

    class Meta:
        icon = "placeholder"
        template = "wagtailpages/blocks/newsletter_signup_block.html"


class BlogNewsletterSignupBlock(blocks.StructBlock):
    signup = SnippetChooserBlock("wagtailpages.BlogSignup")

    class Meta:
        icon = "placeholder"
        template = "wagtailpages/blocks/blog_newsletter_signup_block.html"
