"""
These are utility blocks used for the LinkBlock.
"""

from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock


class InternalLinkBlockStructValue(blocks.StructValue):
    @property
    def link_url(self):
        link = self.get("link")
        if link and hasattr(link, "localized"):
            return link.localized.url
        return None


class ExternalLinkBlockStructValue(blocks.StructValue):
    @property
    def link_url(self):
        return self.get("link")


class DocumentLinkBlockStructValue(blocks.StructValue):
    @property
    def link_url(self):
        document = self.get("document")
        if document and hasattr(document, "localized"):
            return document.localized.url
        return None


class InternalLinkBlock(blocks.StructBlock):
    link = blocks.PageChooserBlock(help_text="Page that this should link out to.")

    class Meta:
        value_class = InternalLinkBlockStructValue


class ExternalLinkBlock(blocks.StructBlock):
    link = blocks.URLBlock(help_text="URL that this should link out to.")

    class Meta:
        value_class = ExternalLinkBlockStructValue


class DocumentLinkBlock(blocks.StructBlock):
    document = DocumentChooserBlock(help_text="Document that this should link out to.")

    class Meta:
        value_class = DocumentLinkBlockStructValue


class LabelledLinkBaseBlock(blocks.StructBlock):
    label = blocks.CharBlock(help_text="Label for this link.")


class LabelledInternalLinkBlock(InternalLinkBlock, LabelledLinkBaseBlock):
    pass


class LabelledExternalLinkBlock(ExternalLinkBlock, LabelledLinkBaseBlock):
    pass


class LabelledDocumentLinkBlock(DocumentLinkBlock, LabelledLinkBaseBlock):
    pass
