from django import forms
from django.forms.utils import ErrorList
from django.utils.functional import cached_property
from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockAdapter

from legacy_cms.wagtailpages.validators import RelativeURLValidator


class BaseLinkValue(blocks.StructValue):
    """
    Get active link used in LinkBlock or CustomLinkBlock if there is one
    """

    def get_page_link(self):
        page = self.get("page")
        return page.localized.url if page else None

    def get_external_url_link(self):
        return self.get("external_url")

    def get_relative_url_link(self):
        return self.get("relative_url")

    def get_phone_link(self):
        return self.get("phone")

    def get_email_link(self):
        return self.get("email")

    def get_file_link(self):
        return self.get("file")

    # TODO: Make link_to set on translated pages so no fallback needed
    @property
    def url(self):
        # If link_to is set, dynamically call the corresponding method
        link_to = self.get("link_to")
        if link_to:
            method = getattr(self, f"get_{link_to}_link", None)
            if method:
                return method()

        # Missing link_to field fallback (i.e. translated pages)
        # If link_to not found try to find the value
        # Since self is in memory, this should be efficient.
        for link_type in ["page", "external_url", "relative_url", "phone", "email", "file"]:
            method = getattr(self, f"get_{link_type}_link", None)
            if method:
                result = method()  # Call the method
                if result:  # Return the first valid result
                    return result

    def get_link_to(self):
        """
        Return link type for accessing in templates
        """
        return self.get("link_to")


class BaseLinkBlock(blocks.StructBlock):
    label = blocks.CharBlock()

    link_to = blocks.ChoiceBlock(
        choices=[
            ("page", "Page"),
            ("external_url", "External URL"),
            ("relative_url", "Relative URL"),
        ],
        label="Link to",
    )
    page = blocks.PageChooserBlock(required=False, label="Page")
    external_url = blocks.URLBlock(
        max_length=300,
        required=False,
        label="External URL",
        help_text="Enter a full URL including http:// or https://",
    )
    relative_url = blocks.CharBlock(
        max_length=300,
        required=False,
        validators=[RelativeURLValidator()],
        label="Relative URL",
        help_text='A path relative to this domain. For example, "/foo/bar" or "?foo=bar".',
    )

    class Meta:
        abstract = True
        value_class = BaseLinkValue

    def get_default_values(self):
        return {
            "page": None,
            "external_url": "",
            "relative_url": "",
        }

    def clean(self, value):
        clean_values = super().clean(value)
        errors = {}

        url_default_values = self.get_default_values()
        url_type = clean_values.get("link_to")

        # Check that a value has been uploaded for the chosen link type
        if url_type != "" and clean_values.get(url_type) in [None, ""]:
            errors[url_type] = ErrorList(["You need to add a {} link".format(url_type.replace("_", " "))])
        else:
            try:
                # Remove values added for link types not selected
                url_default_values.pop(url_type, None)
                for field in url_default_values:
                    clean_values[field] = url_default_values[field]
            except KeyError:
                errors[url_type] = ErrorList(["Enter a valid link type"])

        if errors:
            raise blocks.StreamBlockValidationError(block_errors=errors, non_block_errors=ErrorList([]))

        return clean_values


class BaseLinkBlockAdapter(StructBlockAdapter):
    """Custom adapter to register JS for conditionally hiding/showing fields.

    Can be used with any block that extends `BaseLinkBlock`.

    Simply register this adapter with your concrete class.

    See: https://docs.wagtail.org/en/stable/advanced_topics/customisation/streamfield_blocks.html#additional-javascript-on-structblock-forms  # noqa: E501
    """

    js_constructor = "legacy_cms.wagtailpages.customblocks.BaseLinkBlock"

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ["wagtailpages/js/base-link-block.js"], css=structblock_media._css
        )
