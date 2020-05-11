from django import forms
from wagtail.admin.forms import WagtailAdminModelForm

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)

from networkapi.buyersguide.models import (
    Update,
    Product,
    GeneralProduct,
    SoftwareProduct,
    BuyersGuideProductCategory
)


# Effect custom ordering (in the admin only) for
# the many-to-many fields in Products
class ProductForm(WagtailAdminModelForm):
    """
    See https://stackoverflow.com/a/61525965/740553
    """

    updates = forms.ModelMultipleChoiceField(
        queryset=Update.objects.order_by('title'),
        required=False
    )

    related_products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.order_by('name'),
        required=False
    )


Product.base_form_class = ProductForm


class WagtailBuyersGuideGeneralProductAdmin(ModelAdmin):
    model = GeneralProduct
    menu_label = 'Products: general'
    menu_icon = 'pick'  # change as required
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view

    def get_published(self, obj):
        return not obj.draft

    get_published.short_description = 'Published'
    get_published.boolean = True
    get_published.admin_order_field = 'draft'

    list_display = ('get_published', 'review_date', 'name', 'company', 'url')
    search_fields = ('name', 'company')
    index_template_name = 'admin/index_view.html'


class WagtailBuyersGuideSoftwareProductAdmin(ModelAdmin):
    model = SoftwareProduct
    menu_label = 'Products: software'
    menu_icon = 'pick'  # change as required
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view

    def get_published(self, obj):
        return not obj.draft

    get_published.short_description = 'Published'
    get_published.boolean = True
    get_published.admin_order_field = 'draft'

    list_display = ('get_published', 'review_date', 'name', 'company', 'url')
    search_fields = ('name', 'company')
    index_template_name = 'admin/index_view.html'


class WagtailBuyersGuideCategoryAdmin(ModelAdmin):
    model = BuyersGuideProductCategory
    menu_label = 'Product Categories'
    menu_icon = 'pick'  # change as required
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view

    list_display = ('featured', 'name', 'description')
    search_fields = ('name')


class WagtailBuyersGuideUpdateAdmin(ModelAdmin):
    model = Update
    menu_label = 'Updates'
    menu_icon = 'pick'  # change as required
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view

    list_display = ('featured', 'source', 'title')
    search_fields = ('source', 'title')


class WagtailBuyersGuideAdminGroup(ModelAdminGroup):
    items = (
        WagtailBuyersGuideGeneralProductAdmin,
        WagtailBuyersGuideSoftwareProductAdmin,
        WagtailBuyersGuideCategoryAdmin,
        WagtailBuyersGuideUpdateAdmin,
    )
    menu_label = 'Buyer\'s Guide'
    menu_icon = 'pick'
    menu_order = 500


modeladmin_register(WagtailBuyersGuideAdminGroup)
