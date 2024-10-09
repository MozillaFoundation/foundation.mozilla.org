from wagtail import blocks
from wagtail.models import Locale
from wagtail.snippets.blocks import SnippetChooserBlock


class NewsletterSignupBlock(blocks.StructBlock):
    signup = SnippetChooserBlock("wagtailpages.Signup")

    class Meta:
        icon = "placeholder"
        template = "wagtailpages/blocks/newsletter_signup_block.html"


class BlogNewsletterSignupBlock(blocks.StructBlock):
    signup = SnippetChooserBlock("wagtailpages.BlogSignup")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        signup = value.get("signup")

        if signup:
            # Get the default locale signup and pass the signup id back to the context
            unlocalized_signup = signup.get_translation_or_none(Locale.get_default()) or signup
            context["unlocalized_signupid"] = unlocalized_signup.id

        return context

    class Meta:
        icon = "placeholder"
        template = "wagtailpages/blocks/blog_newsletter_signup_block.html"
