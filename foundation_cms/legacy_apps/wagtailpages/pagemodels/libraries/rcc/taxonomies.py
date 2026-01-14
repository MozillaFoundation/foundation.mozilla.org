from wagtail.models import TranslatableMixin

from foundation_cms.legacy_apps.wagtailpages.pagemodels.taxonomy import BaseTaxonomy


class RCCContentType(BaseTaxonomy):
    class Meta(TranslatableMixin.Meta):
        verbose_name = "RCC Content Type (Legacy)"
        verbose_name_plural = "RCC Content Types (Legacy)"


class RCCCurricularArea(BaseTaxonomy):
    class Meta(TranslatableMixin.Meta):
        verbose_name = "RCC Curricular Area (Legacy)"
        verbose_name_plural = "RCC Curricular Areas (Legacy)"


class RCCTopic(BaseTaxonomy):
    class Meta(TranslatableMixin.Meta):
        verbose_name = "RCC Topic (Legacy)"
        verbose_name_plural = "RCC Topics (Legacy)"
