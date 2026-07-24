from wagtail.snippets.blocks import SnippetChooserBlock

from foundation_cms.base.models.base_block import BaseBlock


class IllustratedNewsletterSignupBlock(BaseBlock):
    newsletter_signup = SnippetChooserBlock(
        "snippets.IllustratedNewsletterSignup",
        max_num=1,
    )

    class Meta:
        template_name = "illustrated_newsletter_signup_block.html"
        icon = "mail"
        label = "Illustrated Newsletter Signup"
