from django.db import models
from networkapi.buyersguide.fields import ExtendedYesNoField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

from .base import BaseProduct
from ...utils import tri_to_quad


class SoftwareProduct(BaseProduct):
    product_type = "software"
