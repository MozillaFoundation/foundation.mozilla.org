from django import forms

from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.forms import WagtailAdminModelForm

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)

from networkapi.wagtailpages.models import (
    ProductPage,
    BuyersGuidePage,
    GeneralProductPage,
    SoftwareProductPage,
)

from networkapi.buyersguide.models import (
    Update,
    BuyersGuideProductCategory
)


class HomePageEditMenuItem(MenuItem):
    """
    See https://stackoverflow.com/a/57774659
    """
    def get_context(self, request):
        context = super().get_context(request)
        pni_homepage = BuyersGuidePage.objects.get(slug='privacynotincluded')
        context['url'] = f"/cms/pages/{str(pni_homepage.id)}/edit/"
        return context


@hooks.register('register_admin_menu_item')
def register_edit_pni_homepage_menu_item():
    return HomePageEditMenuItem('Edit PNI homepage', 'edit_link', classnames='icon icon-folder-inverse', order=500)


class WagtailBuyersGuideGeneralProductAdmin(ModelAdmin):
    model = GeneralProductPage
    menu_label = 'Products: general'
    menu_icon = 'pick'
    add_to_settings_menu = False
    exclude_from_explorer = False

    list_display = ('live', 'review_date', 'title', 'company', 'url')
    search_fields = ('title', 'company')
    index_template_name = 'admin/index_view.html'


class WagtailBuyersGuideSoftwareProductAdmin(ModelAdmin):
    model = SoftwareProductPage
    menu_label = 'Products: software'
    menu_icon = 'pick'
    add_to_settings_menu = False
    exclude_from_explorer = False

    list_display = ('live', 'review_date', 'title', 'company', 'url')
    search_fields = ('title', 'company')
    index_template_name = 'admin/index_view.html'


class WagtailBuyersGuideCategoryAdmin(ModelAdmin):
    model = BuyersGuideProductCategory
    menu_label = 'Product Categories'
    menu_icon = 'pick'
    add_to_settings_menu = False
    exclude_from_explorer = False

    list_display = ('featured', 'title', 'description')
    search_fields = ('title')


class WagtailBuyersGuideUpdateAdmin(ModelAdmin):
    model = Update
    menu_label = 'Updates'
    menu_icon = 'pick'
    add_to_settings_menu = False
    exclude_from_explorer = False

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
