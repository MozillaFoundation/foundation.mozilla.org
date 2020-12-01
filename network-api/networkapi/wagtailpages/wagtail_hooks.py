# RichTextEditor customization:
#   See https://docs.wagtail.io/en/v2.7/advanced_topics/customisation/extending_draftail.html
#   And https://medium.com/@timlwhite/custom-in-line-styles-with-draftail-939201c2bbda
from cloudinary import uploader

from django.conf import settings

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.core import hooks

from networkapi.wagtailpages.pagemodels.products import ProductPage


# Extended rich text features for our site
@hooks.register('register_rich_text_features')
def register_large_feature(features):
    """
    Registering the 'large' Draftail feature which
    adds a span around the selected text with its class
    set to 'body-large'
    """

    # 1. Set up variables for use below
    feature_name = 'large'
    type_ = 'LARGE'

    # 2. Set up a dictionary to pass to Draftail to configure
    # how it handles this feature in its toolbar.
    # The 'style' attribute controls how Draftail formats that text
    # in the editor - does not affect the final rendered HTML
    # In this case, I am adding similar formatting to what
    # the CSS will do to that 'small-caption' class in the template
    control = {
        'type': type_,
        'label': 'L',
        'description': 'Large body text',
        'style': {
            'font-size': '125%'
        }
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail',
        feature_name,
        draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.

    # The "From" version uses a CSS selector to find spans with a class of 'body-large'
    # The "To" version adds a span with a class of 'body-large' surrounding the selected text
    db_conversion = {
        'from_database_format': {
            'span[class="body-large"]':
                InlineStyleElementHandler(type_)
        },
        'to_database_format': {
            'style_map': {type_: 'span class="body-large"'}
        },
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule(
        'contentstate',
        feature_name,
        db_conversion
    )

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append('large')


# Ensure that pages in the PageChooserPanel listings are ordered on most-recent-ness
@hooks.register('construct_page_chooser_queryset')
def order_pages_in_chooser(pages, request):
    # Change listings in the "page chooser" modal:
    if "choose-page" in request.path:
        return pages.order_by('-first_published_at')

    # Don't change search results (shown in ./admin/pages/search)
    return pages


@hooks.register('before_delete_page')
def before_delete_page(request, page):
    """
    If ANY page is deleted that has the `cloudinary_image` field in it,
    check if the app is a review app (don't delete from review apps).
    Delete cloudinary_images from pages that have this field.
    """
    if hasattr(page, 'cloudinary_image'):
        if settings.REVIEW_APP or settings.DEBUG:
            pass
        else:
            uploader.destroy(page.cloudinary_image.public_id, invalidate=True)

    if isinstance(page, ProductPage) and page.votes:
        # Delete the vote from ProductPages
        page.votes.delete()
