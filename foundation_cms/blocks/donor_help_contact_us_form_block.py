from urllib.parse import urlencode

from wagtail import blocks
from wagtail.images.blocks import ImageBlock

from foundation_cms.base.models.base_block import BaseBlock


class DonorHelpContactUsFormBlock(BaseBlock):
    heading = blocks.CharBlock(required=True, default="Contact Us")
    subheading = blocks.CharBlock(
        required=False,
        default="Questions about your donation? Get in touch with our team by using the form below.",
    )
    image = ImageBlock(required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        request = context.get("request")
        page = context.get("page")
        if request and page and hasattr(page, "get_full_url"):
            params = request.GET.dict()
            params["thank_you"] = "true"
            context["thank_you_url"] = page.get_full_url(request) + "?" + urlencode(params) + "#contact-form"
            context["show_formassembly_thank_you"] = request.GET.get("thank_you") == "true"
        return context

    class Meta:
        template_name = "donor_help_contact_us_form_block.html"
        icon = "mail"
        label = "Donor Help Contact Us Form"
