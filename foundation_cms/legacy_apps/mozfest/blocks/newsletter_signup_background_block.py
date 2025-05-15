from wagtail import blocks
from wagtail.snippets.blocks import SnippetChooserBlock


class NewsletterSignupWithBackgroundBlock(blocks.StructBlock):
    snippet = SnippetChooserBlock("mozfest.NewsletterSignupWithBackground")

    class Meta:
        icon = "tag"
        label = "Newsletter Signup With Background"
        template = "fragments/blocks/newsletter_signup_with_background_block.html"
