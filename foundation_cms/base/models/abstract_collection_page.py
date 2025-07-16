from django.db import models
from django.db.models import Q
from wagtail.models import Page

from foundation_cms.base.models.abstract_base_page import AbstractBasePage


class AbstractCollectionPage(AbstractBasePage):
    page_type_filter = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional. Limit results to a specific page type by model name.",
    )

    def get_collection_items(self, request):
        # Example that could return a list of pages filtered
        # via ?tag=... and an optional page type field
        query = Q()

        tag = request.GET.get("tag")
        if tag:
            query &= Q(tags__name=tag)

        if self.page_type_filter:
            query &= Q(content_type__model=self.page_type_filter)

        return Page.objects.live().descendant_of(self).filter(query).specific()

    def get_context(self, request):
        context = super().get_context(request)
        context["items"] = self.get_collection_items(request)
        context["active_tag"] = request.GET.get("tag")
        return context

    class Meta:
        abstract = True
