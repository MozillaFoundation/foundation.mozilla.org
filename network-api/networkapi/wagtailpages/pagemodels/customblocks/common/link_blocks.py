"""
These are utility blocks used for StructBlocks related to MozFest.
"""

from wagtail.core import blocks


class InternalLinkBlockStructValue(blocks.StructValue):
    @property
    def link_url(self):
        return self.get('link').url


class ExternalLinkBlockStructValue(blocks.StructValue):
    @property
    def link_url(self):
        return self.get('link')


class InternalLinkBlock(blocks.StructBlock):
    link = blocks.PageChooserBlock(help_text='Page that this should link out to.')

    class Meta:
        value_class = InternalLinkBlockStructValue


class ExternalLinkBlock(blocks.StructBlock):
    link = blocks.URLBlock(help_text='URL that this should link out to.')

    class Meta:
        value_class = ExternalLinkBlockStructValue


class LabelledLinkBaseBlock(blocks.StructBlock):
    label = blocks.CharBlock(help_text='Label for this link.')


class LabelledInternalLinkBlock(InternalLinkBlock, LabelledLinkBaseBlock):
    pass


class LabelledExternalLinkBlock(ExternalLinkBlock, LabelledLinkBaseBlock):
    pass
