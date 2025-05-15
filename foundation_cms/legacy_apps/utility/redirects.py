from django.shortcuts import redirect
from wagtail.models import Site


# Redirect to the same page, but using the default CMS site.
# Ex: PNI should only be accessible on www.mozillafoundation.org
def redirect_to_default_cms_site(func):
    def wrapper(request, *args, **kwargs):
        wagtail_sites = Site.objects.values("hostname", "is_default_site")
        secondary_wagtail_sites = []
        main_wagtail_site = ""
        for site in wagtail_sites:
            if site["is_default_site"]:
                main_wagtail_site = site["hostname"]
            else:
                secondary_wagtail_sites.append(site["hostname"])

        current_site = request.get_host()
        if current_site in secondary_wagtail_sites:
            return redirect(f"https://{main_wagtail_site}{request.path}")
        return func(request, *args, **kwargs)

    return wrapper
