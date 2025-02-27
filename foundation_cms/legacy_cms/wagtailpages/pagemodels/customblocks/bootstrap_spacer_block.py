from wagtail import blocks


class BootstrapSpacerBlock(blocks.StructBlock):
    """
    See https://getbootstrap.com/docs/4.0/utilities/spacing/
    """

    # property = blocks.ChoiceBlock(
    #    choices=[
    #        ('m', 'Margin'),
    #        #('p', 'Padding'),
    #    ],
    #    default='m',
    # )

    # sides = blocks.ChoiceBlock(
    #    choices=[
    #        ('t', 'top'),
    #        ('b', 'bottom'),
    #        ('l', 'left'),
    #        ('r', 'right'),
    #        ('x', 'left + right'),
    #        ('y', 'top+bottom'),
    #        ('', 'all sides'),
    #    ],
    #    default='',
    # )

    size = blocks.ChoiceBlock(
        choices=[
            # ('0', 'no spacing'),
            ("1", "quarter spacing"),
            ("2", "half spacing"),
            ("3", "single spacing"),
            ("4", "one and a half spacing"),
            ("5", "triple spacing"),
            # ('auto', 'automagical'),
        ],
        default="3",
    )

    class Meta:
        icon = "arrows-up-down"
        template = "wagtailpages/blocks/bootstrap_spacer_block.html"
        help_text = "A bootstrap based vertical spacing block."
