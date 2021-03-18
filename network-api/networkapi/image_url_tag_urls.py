"""
Dynamic Wagtail Images.
https://docs.wagtail.io/en/stable/advanced_topics/images/image_serve_view.html

Typically with Wagtail we use an {% image img.object fill-XXXxYYY %} template tag
to create an image rendition. Creating renditions is a blocking process, which is typically
fine for a standard page with a normal amount of images. Every rendition costs one
database query, and if the rendition doesn't exist, it needs to also create the image.
On a page with 200 images, that's 200 extra database queries, plus rendition-creation
time. If you have 200 images, with 10 renditions each for mobile support, that's 2000
database queries plus rendition-creation time, which is unacceptably slow.

Instead of performing all those queries up front, along with performing rendition
creation upfront, we can use dynamic image URLs to generate an image URL and when
that URL is requested, Wagtail will find the original image, create the rendition, and
serve the image. This off loads the heavy lifting in the upfront HTTP request and defers
the rendition-creation to a different HTTP request. To take advantage of this, we use
the custom URL in this file, along with a slightly different template tag and syntax.

Blocking image rendition example:       {% image product.image fill-250x250 %}
Non-block image rendition example:      {% image_url product.image 'fill-250x250' %}
"""

from django.urls import re_path
from wagtail.images.views.serve import ServeView


urlpatterns = [
    re_path(
        r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$',
        ServeView.as_view(action='redirect'),
        name='wagtailimages_serve',
    ),
]
