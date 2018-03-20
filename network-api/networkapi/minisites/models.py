from django.db import models

from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet

from wagtail.embeds.blocks import EmbedBlock
from adminsortable.models import SortableMixin

class LinkButtonValue(blocks.StructValue):
    # and https://stackoverflow.com/questions/49374083
    # see http://docs.wagtail.io/en/v2.0/topics/streamfield.html#custom-value-class-for-structblock

    @property
    def css(self):
        # Note that StructValue is a dict-like object, so `styling` and `outline`
        # need to be accessed as dictionary keys
        btn_class = self['styling']
        if self['outline'] is True:
            btn_class = btn_class.replace('btn-', 'btn-outline-')
        return btn_class

class LinkButtonBlock(blocks.StructBlock):
    label = blocks.CharBlock()

    # We use a char block because UrlBlock does not
    # allow for relative linking.
    URL = blocks.CharBlock()

    # Buttons can have different looks, so we
    # offer the choice to decide which styling
    # should be used.
    styling = blocks.ChoiceBlock(
        choices=[
            ('btn-primary', 'Primary button'),
            ('btn-secondary', 'Secondary button'),
            ('btn-success', 'Success button'),
            ('btn-info', 'Info button'),
            ('btn-warning', 'Warning button'),
            ('btn-error', 'Error button'),
        ],
        default='btn-info',
    )

    outline = blocks.BooleanBlock(default=False)

    class Meta:
        icon = 'link'
        template = 'minisites/blocks/link_button_block.html'
        value_class = LinkButtonValue


class ImageTextBlock(blocks.StructBlock):
    text = blocks.CharBlock()
    image = ImageChooserBlock()
    ordering = blocks.ChoiceBlock(
        choices=[
            ('left', 'Image on the left'),
            ('right', 'Image on the right'),
        ],
        default='left',
    )

    class Meta:
        icon = 'doc-full'
        template = 'minisites/blocks/image_text_block.html'


class VerticalSpacerBlock(blocks.StructBlock):
    rem = blocks.IntegerBlock()

    class Meta:
        icon = 'arrows-up-down'
        template = 'minisites/blocks/vertical_spacer_block.html'
        help_text = 'the number of "rem" worth of vertical spacing'


class VideoBlock(blocks.StructBlock):
    url = blocks.CharBlock(
        help_text='Please make sure this is a proper embed URL, or your video will not show up on the page.'
    )
    width = blocks.IntegerBlock(default=800)
    height = blocks.IntegerBlock(default=450)

    class Meta:
        template = 'minisites/blocks/video_block.html'


class  iFrameBlock(blocks.StructBlock):
    url = blocks.CharBlock(
        help_text='Please note that only URLs from white-listed domains will work.'
    )
    width = blocks.IntegerBlock(default=800)
    height = blocks.IntegerBlock(default=450)

    class Meta:
        template = 'minisites/blocks/iframe_block.html'


"""
We'll need to figure out which components are truly "base" and
which are bits that should be used in subclassing template-based
page types.
"""
base_fields = [
    ('heading', blocks.CharBlock()),
    ('paragraph', blocks.RichTextBlock()),
    ('image_text', ImageTextBlock()),
    ('image', ImageChooserBlock()),
    ('video', VideoBlock()),
    ('iframe', iFrameBlock()),
    ('linkbutton', LinkButtonBlock()),
    ('spacer', VerticalSpacerBlock()),
]


class ModularPage(Page):
    """
    The base class offers universal component picking
    """

    header = models.CharField(
        max_length=250,
        blank=True
    )

    body = StreamField(base_fields)

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        StreamFieldPanel('body'),
    ]

    show_in_menus_default = True


class MiniSiteNameSpace(ModularPage):
    subpage_types = [
        'CampaignPage',
        'OpportunityPage',
    ]

    """
    This is basically an abstract page type for setting up
    minisite namespaces such as "campaign", "opportunity", etc.
    """
    def get_context(self, request):
        """
        Extend the context so that mini-site pages know what kind of tree
        they live in, and what some of their local aspects are:
        """
        context = super(MiniSiteNameSpace, self).get_context(request)
        ancestors = self.get_ancestors()
        root = next((n for n in ancestors if n.specific_class == self.specific_class), self)
        context['mini_site_title'] = root.title

        children = self.get_children().live()
        has_children = len(children) > 0
        ancestors = self.get_ancestors()
        root = next((root for root in ancestors if root.specific_class == self.specific_class), self)
        context['root'] = root

        is_top_page = (root == self)
        context['is_top_page'] = is_top_page

        context['singleton_page'] = (is_top_page and not has_children)

        return context


class CTA(SortableMixin):
    title = models.CharField(
        default='',
        max_length=100,
        help_text='Identify this component for other editors',
    )

    @property
    def name(self):
        return self.title

    @name.setter
    def name(self, value):
        self.title = value

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

    order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'cta'
        ordering = ('order',)


@register_snippet
class Signup(CTA):

    class Meta:
        verbose_name = 'signup snippet'


class OpportunityPage(MiniSiteNameSpace):
    """
    these pages come with sign-up-for-xyz CTAs
    """
    cta = models.ForeignKey(
        'Signup',
        related_name='page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Choose existing or create new petition form"
    )

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        SnippetChooserPanel('cta'),
        StreamFieldPanel('body'),
    ]

    subpage_types = [
        'OpportunityPage',
    ]


@register_snippet
class Petition(CTA):
    google_forms_url = models.URLField(
        help_text='Google form to post petition data to',
        max_length=2048,
        null=True
    )

    checkbox_1 = models.CharField(
        max_length=1024,
        help_text='label for the first checkbox option (may contain HTML)',
        blank=True
    )

    checkbox_1_form_field = models.CharField(
        max_length=1024,
        help_text='Google form field name for Checkbox 1',
        verbose_name='First checkbox Google Form field',
        blank=True
    )

    checkbox_2 = models.CharField(
        max_length=1024,
        help_text='label for the second checkbox option (may contain HTML)',
        blank=True
    )

    checkbox_2_form_field = models.CharField(
        max_length=1024,
        help_text='Google form field name for Checkbox 1',
        verbose_name='Second checkbox Google Form field',
        blank=True
    )

    given_name_form_field = models.CharField(
        max_length=1024,
        help_text='Google form field name for Given Name(s)',
        verbose_name='Given Name(s) Google Form field',
        blank=True,
    )

    surname_form_field = models.CharField(
        max_length=1024,
        help_text='Google form field name for Surname',
        verbose_name='Surname Google Form field',
        blank=True,
    )

    email_form_field = models.CharField(
        max_length=1024,
        help_text='Google form field name for Email',
        verbose_name='Email Google Form field',
        blank=True,
    )

    newsletter_signup_form_field = models.CharField(
        max_length=1024,
        help_text='Google form field name for Mozilla Newsletter checkbox',
        verbose_name='Mozilla Newsletter signup checkbox Google Form field',
        blank=True,
    )

    share_link = models.URLField(
        max_length=1024,
        help_text='Link that will be put in share button',
        blank=True
    )

    share_link_text = models.CharField(
        max_length=20,
        help_text='Text content of the share button',
        default='Share this',
        blank=True
    )

    thank_you = models.CharField(
        max_length=140,
        help_text='Message to show after thanking people for signing',
        default='Thank you for signing too!',
    )

    class Meta:
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
        help_text="Choose existing or create new sign-up form"
    )

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        SnippetChooserPanel('cta'),
        StreamFieldPanel('body'),
    ]

    subpage_types = [
        'CampaignPage',
    ]
