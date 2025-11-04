from wagtail.blocks import ChoiceBlock

from .choices import BACKGROUND_COLOR_CHOICES


class BackgroundColorChoiceBlock(ChoiceBlock):
    def __init__(self, **kwargs):
        super().__init__(
            choices=BACKGROUND_COLOR_CHOICES,
            default="white",
            **kwargs,
        )
