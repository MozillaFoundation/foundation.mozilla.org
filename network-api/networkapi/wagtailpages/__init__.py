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
        _('How To Wagtail'), reverse('how-to-wagtail'),
        name='howtowagtail', classnames='icon icon-help', order=900
    )
