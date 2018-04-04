from django.utils.translation import ugettext_lazy as _
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks
from django.urls import reverse


class HowToWagtailMenuItem(MenuItem):
    def is_shown(self, request):
        return True


@hooks.register('register_admin_menu_item')
def register_howto_menu_item():
    return HowToWagtailMenuItem(
        _('How Do I Wagtail'), reverse('how-do-i-wagtail'),
        name='howdoIwagtail', classnames='icon icon-help', order=900
    )
