from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import PageChooserPanel


class UniversalLink(models.model):
    """
    A model that can be used by other models for specifying
    a link that is either an internal Wagtail page, or an
    external plain link.

    Used as:

        field_name = models.ForeignKey(
            'wagtailpages.UniversalLink',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='+',
        )

    With an inline panel to surface its admin UI:

        panels = [
            InlinePanel('field_name', label='link')
        ]

    """

    external_link = models.URLField(
        blank=True
    )

    internal_link = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='internal_link',
    )

    panels = [
        FieldPanel('external_link'),
        PageChooserPanel('internal_link'),
    ]

    @property
    def url(self):
        if self.internal_link:
            return self.internal_link.url
        return self.external_link

    def clean(self):
        """
        Validation to ensure both internal or external links have
        been added to the partners section.
        """
        super().clean()
        if self.internal_link and self.external_link:
            # Both fields are filled out
            message = "Please ensure only one field has a value."
            raise ValidationError({
                'external_link': ValidationError(message),
                'internal_link': ValidationError(message),
            })
        if not self.internal_link and not self.external_link:
            message = "Please pick either a page or specify an external URL"
            raise ValidationError({
                'external_link': ValidationError(message),
                'internal_link': ValidationError(message),
            })

    class Meta:
        verbose_name = 'link'
        verbose_name_plural = 'links'
