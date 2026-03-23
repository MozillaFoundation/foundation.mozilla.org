from wagtail.admin.panels import FieldPanel
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_general_page import AbstractGeneralPage
from foundation_cms.mixins.hero_image import HeroImageMixin


class GalleryPage(AbstractGeneralPage, HeroImageMixin):

    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Gallery Hub Gallery Page"

    template = "patterns/pages/gallery_hub/gallery_page.html"
