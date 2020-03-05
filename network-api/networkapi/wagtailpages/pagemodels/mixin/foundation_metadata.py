from taggit.models import Tag
from wagtailmetadata.models import MetadataPageMixin
from wagtail.images.models import Image


# Override the MetadataPageMixin to allow for a default
# description and image in page metadata for all Pages on the site
class FoundationMetadataPageMixin(MetadataPageMixin):
    def __init__(self, *args, **kwargs):
        # The first Wagtail image returned that has the specified tag name will
        # be the default image URL in social shares when no Image is specified at the Page level
        super().__init__(*args, **kwargs)
        try:
            default_social_share_tag = 'social share image'
            self.social_share_tag = Tag.objects.get(name=default_social_share_tag)
        except Tag.DoesNotExist:
            self.social_share_tag = None

    # Change this string to update the default description of all pages on the site
    default_description = 'Mozilla is a global non-profit dedicated to putting you in control of your online ' \
                          'experience and shaping the future of the web for the public good. '

    def get_meta_description(self):
        if self.search_description:
            return self.search_description

        parent = self.get_parent()

        while parent:
            if parent.search_description:
                return parent.search_description
            parent = parent.get_parent()

        return self.default_description

    def get_meta_image(self):
        if self.search_image:
            return self.search_image

        parent = self.get_parent()

        while parent:
            if hasattr(parent, 'search_image') and parent.search_image:
                return parent.search_image
            if hasattr(parent, 'homepage') and parent.homepage.search_image:
                return parent.homepage.search_image
            parent = parent.get_parent()

        try:
            return Image.objects.filter(tags=self.social_share_tag).first()
        except Image.DoesNotExist:
            return None

    class Meta:
        abstract = True
