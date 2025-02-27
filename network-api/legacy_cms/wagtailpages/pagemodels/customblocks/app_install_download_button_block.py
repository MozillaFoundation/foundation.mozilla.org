from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from legacy_cms.wagtailpages.pagemodels.customblocks.link_block import LinkBlock


class AppInstallDownloadButtonBlock(LinkBlock):
    icon = ImageChooserBlock(required=False, help_text="For best results, please use black or white icons.")
    icon_alt_text = blocks.CharBlock(required=False, help_text="Image description (for screen readers).")

    class Meta:
        template = "wagtailpages/blocks/app_install_download_button_block.html"
