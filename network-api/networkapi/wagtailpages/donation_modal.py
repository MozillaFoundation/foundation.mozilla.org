from django.db import models

from wagtail.core.models import TranslatableMixin
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey

from wagtail_localize.fields import SynchronizedField, TranslatableField


@register_snippet
class DonationModal(TranslatableMixin, models.Model):
    name = models.CharField(
        default='',
        max_length=100,
        help_text='Identify this component for other editors',
    )

    header = models.CharField(
        max_length=500,
        help_text='Donation header',
        default="Thanks for signing! While you're here, we need your help.",
    )

    body = models.TextField(
        help_text='Donation text',
        default='Mozilla is a nonprofit organization fighting for '
                'a healthy internet, where privacy is included by '
                'design and you have more control over your personal '
                'information. We depend on contributions from people '
                'like you to carry out this work. Can you donate today?'
    )

    donate_text = models.CharField(
        max_length=150,
        help_text='Donate button label',
        default="Yes, I'll chip in",
    )

    dismiss_text = models.CharField(
        max_length=150,
        help_text='Dismiss button label',
        default="No thanks",
    )

    translatable_fields = [
        TranslatableField('header'),
        TranslatableField('body'),
        TranslatableField('donate_text'),
        TranslatableField('dismiss_text'),
    ]

    def to_simple_dict(self):
        keys = ['name', 'header', 'body', 'donate_text', 'dismiss_text']
        values = map(lambda k: getattr(self, k), keys)
        return dict(zip(keys, values))

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = 'Donation CTA'


class DonationModals(TranslatableMixin, models.Model):
    page = ParentalKey(
        'wagtailpages.CampaignPage',
        related_name='donation_modals',
    )

    donation_modal = models.ForeignKey(
        'DonationModal',
        related_name='campaign',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Choose existing or create new donation modal'
    )

    def to_simple_dict(self):
        modal = DonationModal.objects.get(campaign=self)
        return modal.to_simple_dict()

    panels = [
        SnippetChooserPanel('donation_modal'),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = 'Donation Modals'
        verbose_name_plural = 'Donation Modals'
