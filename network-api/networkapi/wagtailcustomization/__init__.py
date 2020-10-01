from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html

from wagtail.core import hooks


@hooks.register("insert_global_admin_css")
def global_admin_css():
    link = static("css/admin-interface.css")
    return format_html(f'<link rel="stylesheet" href="{link}">')
