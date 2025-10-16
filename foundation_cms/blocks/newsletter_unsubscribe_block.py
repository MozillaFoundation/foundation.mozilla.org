from wagtail.snippets.blocks import SnippetChooserBlock

from foundation_cms.base.models.base_block import BaseBlock


class NewsletterUnsubscribeBlock(BaseBlock):
    newsletter_unsubscribe = SnippetChooserBlock(
        "snippets.NewsletterUnsubscribe",
        max_num=1,
    )

    class Meta:
        template_name = "newsletter_unsubscribe_block.html"
        icon = "mail"
        label = "Newsletter Unsubscribe"
