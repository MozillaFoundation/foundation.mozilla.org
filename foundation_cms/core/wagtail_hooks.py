from wagtail import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
)
from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail_ab_testing.events import BaseEvent


# Extended rich text features for our site
@hooks.register("register_rich_text_features")
def register_large_feature(features):
    """
    Registering the 'large' Draftail feature which
    adds a span around the selected text with its class
    set to 'tw-body-large and body-text-large'
    """

    # 1. Set up variables for use below
    feature_name = "large"
    type_ = "LARGE"

    # 2. Set up a dictionary to pass to Draftail to configure
    # how it handles this feature in its toolbar.
    # The 'style' attribute controls how Draftail formats that text
    # in the editor - does not affect the final rendered HTML
    # In this case, we are adding similar formatting to what
    # the CSS will do to that 'small-caption' class in the template
    control = {
        "type": type_,
        "label": "L",
        "description": "Large body text",
        "style": {"font-size": "125%"},
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin("draftail", feature_name, draftail_features.InlineStyleFeature(control))

    # 4.configure the content transform from the DB to the editor and back.

    # The "From" version uses a CSS selector to find spans with a class of 'tw-body-large' and body-text-large
    # The "To" version adds a span with a class of 'tw-body-large' and 'body-text-large' surrounding the selected text
    # TODO: We may need to adjust the CSS classes based on the actual styles used. Class 'tw-body-large' is a class
    #       used in the legacy app, so should be replaced with the correct class used in the new app.
    db_conversion = {
        "from_database_format": {
            'span[class="tw-body-large"]': InlineStyleElementHandler(type_),
            'span[class="body-text-large"]': InlineStyleElementHandler(type_),
            'span[class="tw-body-large body-text-large"]': InlineStyleElementHandler(type_),
            'span[class="body-text-large tw-body-large"]': InlineStyleElementHandler(type_),
        },
        "to_database_format": {"style_map": {type_: 'span class="tw-body-large body-text-large"'}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append("large")


# --------------------------------------------------------------------------------------
# Custom Wagtail A/B Testing Events:
# --------------------------------------------------------------------------------------


class DonateBannerLinkClick(BaseEvent):
    name = "Donate Banner Link Click"
    requires_page = False  # Set to False to create a "Global" event type that could be reached on any page


@hooks.register("register_ab_testing_event_types")
def register_donate_banner_link_click_event_type():
    return {
        "donate-banner-link-click": DonateBannerLinkClick,
    }
