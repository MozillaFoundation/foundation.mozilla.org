from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.forms.utils import ErrorList
from wagtail.core.blocks.struct_block import StructBlockValidationError


class ImageTeaserBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        help_text='Heading for the card.'
    )
    text = blocks.RichTextBlock(
        features=['bold']
    )
    image = ImageChooserBlock()

    altText = blocks.CharBlock(
        required=True,
        help_text='Image description (for screen readers).'
    )

    url_label = blocks.CharBlock(required=False)
    url = blocks.CharBlock(required=False)
    styling = blocks.ChoiceBlock(
        choices=[
            ('btn-primary', 'Primary button'),
            ('btn-secondary', 'Secondary button'),
        ],
        default='btn-primary',
    )

    def clean(self, value):
        result = super().clean(value)
        errors = {}

        if value['url'] and not value['url_label']:
            errors["url_label"] = ErrorList(["Please add a label value for the URL."])
        if value['url_label'] and not value['url']:
            errors["url"] = ErrorList(["Please add a URL value for the link."])
        if errors:
            raise StructBlockValidationError(errors)

        return result

    class Meta:
        icon = 'doc-full'
        template = 'wagtailpages/blocks/image_teaser_block.html'
