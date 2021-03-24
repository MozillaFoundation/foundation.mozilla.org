from datetime import date, datetime

from cloudinary import uploader

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from django.utils.text import slugify

from networkapi.buyersguide.fields import ExtendedYesNoField
from ..product_update import Update as ProductUpdate

from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel

from ..cloudinary_image_field import CloudinaryField
from ..get_product_image_upload_path import get_product_image_upload_path
from ..get_product_vote_information import get_product_vote_information


class ProductUpdatesFieldPanel(FieldPanel):
    """
    This is a custom field panel for listing product updates in a regular
    product's admin view - the list is populated by the result from
    calling BaseProduct.get_product_updates, below.
    """
    def on_form_bound(self):
        instance = self.model
        self.form.fields['updates'].queryset = instance.get_product_updates(instance)
        super().on_form_bound()


class RelatedProductFieldPanel(FieldPanel):
    """
    This is a custom field panel for listing related products in a regular
    product's admin view - rather than showing all entries, a large number
    of products should be ignored for cross-linking purposes. See the
    "def get_related_products(self):" function in the Product class, below,
    for more details on the queryset it returns.
    """
    def on_form_bound(self):
        instance = self.model
        self.form.fields['related_products'].queryset = instance.get_related_products(instance)
        super().on_form_bound()

registered_product_types = list()


def register_product_type(ModelClass):
    registered_product_types.append(ModelClass)
