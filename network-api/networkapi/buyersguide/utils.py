from django.shortcuts import redirect
from wagtail.core.models import Site


def tri_to_quad(input):
    if input is True:
        return 'Yes'
    if input is False:
        return 'No'
    return 'U'


def quad_to_tri(input):
    if input == 'Yes':
        return True
    if input == 'No':
        return False
    return None


# Redirect to the same page, but using the default CMS site.
# Ex: PNI should only be accessible on foundation.mozilla.org
main_site = Site.objects.get(is_default_site=True).hostname
secondary_wagtail_sites = [site.hostname for site in list(Site.objects.filter(is_default_site=False))]


def redirect_to_main_cms_site_decorator(func):
    def wrapper(request, *args, **kwargs):
        current_site = request.get_host()
        if current_site in secondary_wagtail_sites:
            return redirect(f"https://{main_site}{request.path}")
        return func(request, *args, **kwargs)
    return wrapper
