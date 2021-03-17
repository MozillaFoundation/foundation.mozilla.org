from wagtail.core import blocks


class TypeformBlock(blocks.StructBlock):
    embed_id = blocks.CharBlock(
        required=True,
        help_text='The embed id of your Typeform page (e.g. '
                  'if the form is on admin.typeform.com/form/e8zScc6t, the id will be: e8zScc6t)',
    )

    button_type = blocks.ChoiceBlock(
        choices=[
            ('btn-primary', 'Primary button'),
            ('btn-secondary', 'Secondary button'),
        ],
        default='btn-primary',
    )

    button_text = blocks.CharBlock(
        required=True,
        help_text='This is a text prompt for users to open the typeform content',
    )

    class Meta:
        icon = 'placeholder'
        template = 'wagtailpages/blocks/typeform_block.html'
        help_text = 'Note that a page can only contain a single Typeform embed'
