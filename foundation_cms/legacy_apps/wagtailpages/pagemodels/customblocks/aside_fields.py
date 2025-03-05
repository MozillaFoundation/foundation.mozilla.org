from .aside import AsideContentBlock
from .bootstrap_spacer_block import BootstrapSpacerBlock
from .link_button_block import LinkButtonBlock

aside_fields = [
    ("aside_content", AsideContentBlock()),
    ("linkbutton", LinkButtonBlock()),
    ("spacer", BootstrapSpacerBlock()),
]
