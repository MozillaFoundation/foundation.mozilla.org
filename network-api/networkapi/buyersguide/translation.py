from .pagemodels.products.base import Product
from .pagemodels.products.general import GeneralProduct
from .pagemodels.products.software import SoftwareProduct
from .pagemodels.product_category import BuyersGuideProductCategory

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from networkapi.buyersguide.pagemodels.privacy import ProductPrivacyPolicyLink


@register(Product)
class ProductTR(TranslationOptions):
    fields = (
        'name',
        'company',
        'blurb',
        'worst_case',
        'signup_requirement_explanation',
        'personal_data_collected',
        'biometric_data_collected',
        'social_data_collected',
        'how_does_it_use_data_collected',
        'how_can_you_control_your_data',
        'track_record_details',
        'offline_use_description',
        'uses_encryption_helptext',
        'security_updates_helptext',
        'strong_password_helptext',
        'manage_vulnerabilities_helptext',
        'privacy_policy_helptext',
        'ai_helptext',
    )


@register(GeneralProduct)
class GeneralProductTR(TranslationOptions):
    fields = (
        'child_rules_helptext',
    )


@register(SoftwareProduct)
class SoftwareProductTR(TranslationOptions):
    fields = (
        'handles_recordings_how',
        'recording_alert_helptext',
        'medical_privacy_compliant_helptext',
        'host_controls',
        'easy_to_learn_and_use_helptext',
    )


@register(BuyersGuideProductCategory)
class BuyersGuideProductCategoryTR(TranslationOptions):
    fields = (
        'name',
        'description',
    )


@register(ProductPrivacyPolicyLink)
class ProductPrivacyPolicyLinkTR(TranslationOptions):
    fields = ('label',)
