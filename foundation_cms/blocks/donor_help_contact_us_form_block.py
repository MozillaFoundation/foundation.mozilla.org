from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock


class DonorHelpContactUsFormBlock(BaseBlock):
    heading = blocks.CharBlock(required=False, default="Contact Us")
    subheading = blocks.CharBlock(
        required=False,
        default="Questions about your donation? Get in touch with our team by using the form below.",
    )

    class Meta:
        template_name = "donor_help_contact_us_form_block.html"
        icon = "mail"
        label = "Donor Help Contact Us Form"
