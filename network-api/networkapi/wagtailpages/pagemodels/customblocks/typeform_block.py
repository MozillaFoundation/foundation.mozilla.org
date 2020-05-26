from wagtail.core import blocks


class TypeFormBlock(blocks.StructBlock):
    url = blocks.URLBlock(
        help_text="The URL of the published Typeform"
    )

    button_type = blocks.ChoiceBlock(
        choices=[
            ('btn-primary', 'Primary button'),
            ('btn-secondary', 'Secondary button'),
        ],
        default='btn-primary',
    )

    button_text = blocks.CharBlock(
        required=True
    )

    class Meta:
        icon = 'placeholder'
        template = 'wagtailpages/blocks/typeform_block.html'
        help_text = 'We only support a single Typeform per page'
