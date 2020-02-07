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
def redirect_to_main_cms_site_decorator(func):
    def wrapper(request, *args, **kwargs):
        wagtail_sites = Site.objects.all()
        secondary_wagtail_sites = []
        main_wagtail_site = ''
        for site in wagtail_sites:
            if site.is_default_site:
                main_wagtail_site = site.hostname
            else:
                secondary_wagtail_sites.append(site.hostname)

        current_site = request.get_host()
        if current_site in secondary_wagtail_sites:
            return redirect(f"https://{main_wagtail_site}{request.path}")
        return func(request, *args, **kwargs)
    return wrapper
