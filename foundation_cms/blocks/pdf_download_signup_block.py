from wagtail.snippets.blocks import SnippetChooserBlock

from foundation_cms.base.models.base_block import BaseBlock


class PdfDownloadSignupBlock(BaseBlock):
    pdf_download_signup = SnippetChooserBlock(
        "snippets.PdfDownloadSignup",
        max_num=1,
    )

    class Meta:
        template_name = "pdf_download_signup_block.html"
        icon = "mail"
        label = "PDF Download Signup"
