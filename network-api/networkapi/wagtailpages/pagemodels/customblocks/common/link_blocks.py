"""
These are utility blocks used for StructBlocks related to MozFest.
"""

from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock


class InternalLinkBlockStructValue(blocks.StructValue):
    @property
    def link_url(self):
        return self.get('link').url


class ExternalLinkBlockStructValue(blocks.StructValue):
    @property
    def link_url(self):
        return self.get('link')


class DocumentLinkBlockStructValue(blocks.StructValue):
    @property
    def link_url(self):
        return self.get('document').url


class InternalLinkBlock(blocks.StructBlock):
    link = blocks.PageChooserBlock(help_text='Page that this should link out to.')

    class Meta:
        value_class = InternalLinkBlockStructValue


class ExternalLinkBlock(blocks.StructBlock):
    link = blocks.URLBlock(help_text='URL that this should link out to.')

    class Meta:
        value_class = ExternalLinkBlockStructValue


class DocumentLinkBlock(blocks.StructBlock):
    document = DocumentChooserBlock(help_text='Document that this should link out to.')

    class Meta:
        value_class = DocumentLinkBlockStructValue


class LabelledLinkBaseBlock(blocks.StructBlock):
    label = blocks.CharBlock(help_text='Label for this link.')


class LabelledInternalLinkBlock(InternalLinkBlock, LabelledLinkBaseBlock):
    pass


class LabelledExternalLinkBlock(ExternalLinkBlock, LabelledLinkBaseBlock):
    pass


class LabelledDocumentLinkBlock(DocumentLinkBlock, LabelledLinkBaseBlock):
    pass
