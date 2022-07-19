"""
Custom CSRF middleware to allow ProductPages to accept POST requests.
Ever other page should accept CSRF as normal.
"""

from django.middleware.csrf import CsrfViewMiddleware

from wagtail.core.views import serve

from networkapi.wagtailpages.pagemodels.buyersguide.products import ProductPage


class CustomCsrfViewMiddleware(CsrfViewMiddleware):

    def process_view(self, request, callback, callback_args, callback_kwargs):

        if callback == serve and request.method == "POST":
            # We are visiting a wagtail page. Check if this is a ProductPage
            # and if so, do not perform any CSRF validation
            path = request.path.rstrip('/').split('/').pop()   # ie general-percy-product

            # Find the page
            try:
                page = ProductPage.objects.get(slug=path)
            except (ProductPage.MultipleObjectsReturned, ProductPage.DoesNotExist):
                return super().process_view(request, callback, callback_args, callback_kwargs)

            # Do one last check that the page is in-fact an instance of a ProductPage
            if isinstance(page, ProductPage):
                # Page that had the POST request is infact a ProductPage
                # Don't perform CSRF validation on ProductPages.
                return None

        return super().process_view(request, callback, callback_args, callback_kwargs)
