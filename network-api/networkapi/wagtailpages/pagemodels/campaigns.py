import json

from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.core.models import TranslatableMixin, Page
from wagtail.core.fields import RichTextField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from wagtail_localize.fields import SynchronizedField, TranslatableField

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from .modular import MiniSiteNameSpace
from .primary import PrimaryPage
from .mixin.foundation_metadata import FoundationMetadataPageMixin
from ..utils import (
    get_page_tree_information,
    get_content_related_by_tag
)


class CTA(models.Model):
    name = models.CharField(
        default='',
        max_length=100,
        help_text='Identify this component for other editors',
    )

    header = models.CharField(
        max_length=500,
        help_text='Heading that will display on page for this component',
        blank=True
    )

    description = RichTextField(
        help_text='Body (richtext) of component',
        blank=True
    )

    newsletter = models.CharField(
        max_length=100,
        help_text='The (pre-existing) SalesForce newsletter to sign up for',
        default='mozilla-foundation'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'CTA'


@register_snippet
class Signup(TranslatableMixin, CTA):
    campaign_id = models.CharField(
        max_length=20,
        help_text='Which campaign identifier should this petition be tied to?',
        null=True,
        blank=True,
    )

    ask_name = models.BooleanField(
        help_text='Check this box to show (optional) name fields',
        default=False,
    )

    translatable_fields = [
        # Fields from the CTA model
        TranslatableField('header'),
        TranslatableField('description'),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = 'signup snippet'


class OpportunityPage(MiniSiteNameSpace):

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        StreamFieldPanel('body'),
    ]

    subpage_types = [
        'OpportunityPage',
        'RedirectingPage',
        'PublicationPage',
        'ArticlePage'
    ]

    translatable_fields = [
        # Promote tab fields
        TranslatableField('seo_title'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
        # Content tab fields
        TranslatableField('title'),
        TranslatableField('header'),
        TranslatableField('body'),
    ]

    class Meta:
        verbose_name = "Default Page"
        verbose_name_plural = "Default pages"


@register_snippet
class Petition(TranslatableMixin, CTA):
    campaign_id = models.CharField(
        max_length=20,
        help_text='Which campaign identifier should this petition be tied to?',
        null=True,
        blank=True,
    )

    requires_country_code = models.BooleanField(
        default=False,
        help_text='Will this petition require users to specify their country?',
    )

    requires_postal_code = models.BooleanField(
        default=False,
        help_text='Will this petition require users to specify their postal code?',
    )

    COMMENT_CHOICES = (
        ('none', 'No comments'),
        ('optional', 'Optional comments'),
        ('required', 'Required comments'),
    )

    comment_requirements = models.CharField(
        choices=COMMENT_CHOICES,
        default='none',
        help_text='What is the comments policy for this petition?',
        max_length=8,
    )

    checkbox_1 = models.CharField(
        editable=False,
        max_length=1024,
        help_text='label for the first checkbox option (may contain HTML)',
        blank=True,
    )

    checkbox_2 = models.CharField(
        editable=False,
        max_length=1024,
        help_text='label for the second checkbox option (may contain HTML)',
        blank=True,
    )

    share_link = models.URLField(
        max_length=1024,
        help_text='Link that will be put in share button',
        blank=True,
        editable=False,
    )

    share_link_text = models.CharField(
        max_length=20,
        help_text='Text content of the share button',
        default='Share this',
        blank=True,
        editable=False,
    )

    share_twitter = models.CharField(
        max_length=20,
        help_text='Share Progress id for twitter button, including the sp_... prefix',
        blank=True,
    )

    share_facebook = models.CharField(
        max_length=20,
        help_text='Share Progress id for facebook button, including the sp_... prefix',
        blank=True,
    )

    share_email = models.CharField(
        max_length=20,
        help_text='Share Progress id for email button, including the sp_... prefix',
        blank=True,
    )

    thank_you = models.CharField(
        max_length=140,
        help_text='Message to show after thanking people for signing',
        default='Thank you for signing too!',
    )

    translatable_fields = [
        # This models fields
        SynchronizedField('requires_country_code'),
        SynchronizedField('requires_postal_code'),
        TranslatableField('comment_requirements'),
        TranslatableField('checkbox_1'),
        TranslatableField('checkbox_2'),
        SynchronizedField('share_twitter'),
        SynchronizedField('share_facebook'),
        SynchronizedField('share_email'),
        TranslatableField('thank_you'),
        # Fields from the CTA model
        TranslatableField('header'),
        TranslatableField('description'),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = 'petition snippet'


class CampaignPage(MiniSiteNameSpace):
    """
    these pages come with sign-a-petition CTAs
    """
    cta = models.ForeignKey(
        'Petition',
        related_name='page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Choose existing or create new sign-up form'
    )

    def get_donation_modal_json(self):
        modals = self.donation_modals.all()
        # This is where we can do server-side A/B testing,
        # by either sending all modals down the pipe, or
        # selectively only sending a single one based on
        # things like geolocation, time of day, etc.
        modals_json = [m.to_simple_dict() for m in modals]
        return json.dumps(modals_json)

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        SnippetChooserPanel('cta'),
        InlinePanel('donation_modals', label='Donation Modal', max_num=4),
        StreamFieldPanel('body'),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField('slug'),
        TranslatableField('seo_title'),
        SynchronizedField('show_in_menus'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
        # Content tab fields
        TranslatableField('cta'),
        TranslatableField('title'),
        TranslatableField('header'),
        SynchronizedField('narrowed_page_content'),
        SynchronizedField('zen_nav'),
        TranslatableField('body'),
        TranslatableField('donation_modals'),
    ]

    subpage_types = [
        'CampaignPage',
        'RedirectingPage',
        'PublicationPage',
        'ArticlePage'

    ]


class BanneredCampaignTag(TaggedItemBase):
    content_object = ParentalKey(
        'wagtailpages.BanneredCampaignPage',
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )


class BanneredCampaignPage(PrimaryPage):
    """
    title, header, intro, and body are inherited from PrimaryPage
    """

    # Note that this is a different related_name, as the `page`
    # name is already taken as back-referenced to CampaignPage.
    cta = models.ForeignKey(
        'Petition',
        related_name='bcpage',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Choose an existing, or create a new, pettition form'
    )

    signup = models.ForeignKey(
        'Signup',
        related_name='bcpage',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Choose an existing, or create a new, sign-up form'
    )

    tags = ClusterTaggableManager(through=BanneredCampaignTag, blank=True)

    panel_count = len(PrimaryPage.content_panels)
    n = panel_count - 1

    content_panels = PrimaryPage.content_panels[:n] + [
        SnippetChooserPanel('cta'),
        SnippetChooserPanel('signup'),
    ] + PrimaryPage.content_panels[n:]

    promote_panels = FoundationMetadataPageMixin.promote_panels + [
        FieldPanel('tags'),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField('slug'),
        TranslatableField('seo_title'),
        SynchronizedField('show_in_menus'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
        # Content tab fields
        TranslatableField('header'),
        TranslatableField('intro'),
        TranslatableField('body'),
        TranslatableField("title"),
        SynchronizedField("banner"),
        SynchronizedField("narrowed_page_content"),
        SynchronizedField("zen_nav"),
        TranslatableField("cta"),
        TranslatableField("signup"),
    ]

    subpage_types = [
        'BanneredCampaignPage',
        'RedirectingPage',
        'PublicationPage',
        'OpportunityPage',
        'ArticlePage'
    ]

    show_in_menus_default = True

    def get_context(self, request):
        context = super().get_context(request)
        context['related_posts'] = get_content_related_by_tag(self)
        return context

    class Meta:
        verbose_name = "Banner Page"
        verbose_name_plural = "Banner pages"
