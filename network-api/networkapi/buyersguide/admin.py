from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from wagtail.core import hooks
from wagtail.admin.menu import Menu, MenuItem, SubmenuMenuItem


from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)

from networkapi.wagtailpages.models import (
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

    list_display = ('featured', 'name', 'description')
    search_fields = ('name',)


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


class MyMenu(Menu):

    @property
    def registered_menu_items(self):
        pni_homepage = BuyersGuidePage.objects.get(slug='privacynotincluded')
        pni_homepage_url = reverse('wagtailadmin_pages:edit', args=(pni_homepage.id,))
        return [
            MenuItem(
                _('Edit PNI Homepage'),
                pni_homepage_url,
                classnames='icon icon-edit',
                order=100,
            ),
            MenuItem(
                _('Buyers Guide Categories'),
                '/cms/buyersguide/buyersguideproductcategory/',
                classnames='icon icon-pick',
                order=200,
            ),
        ]


@hooks.register('register_admin_menu_item')
def register_settings_menu():
    return SubmenuMenuItem(
        _('Buyer\'s Guide'),
        MyMenu(register_hook_name='create_pni_menu'),
        icon_name='cogs',
        order=10000)
