from wagtail import blocks

from .. import customblocks
from .full_content_rich_text_options import full_content_rich_text_options

"""
We'll need to figure out which components are truly "base" and
which are bits that should be used in subclassing template-based
page types.
"""

base_fields = [
    (
        "paragraph",
        blocks.RichTextBlock(
            features=full_content_rich_text_options + ["large"],
            template="wagtailpages/blocks/rich_text_block.html",
        ),
    ),
    ("card_grid", customblocks.CardGridBlock()),
    ("image", customblocks.AnnotatedImageBlock()),
    ("image_text", customblocks.ImageTextBlock()),
    ("image_text_mini", customblocks.ImageTextMini()),
    ("image_grid", customblocks.ImageGridBlock()),
    ("video", customblocks.VideoBlock()),
    ("iframe", customblocks.iFrameBlock()),
    ("linkbutton", customblocks.LinkButtonBlock()),
    ("spacer", customblocks.BootstrapSpacerBlock()),
    ("single_quote", customblocks.SingleQuoteBlock()),
    ("pulse_listing", customblocks.PulseProjectList()),
    ("profile_listing", customblocks.LatestProfileList()),
    ("profile_by_id", customblocks.ProfileById()),
    ("profile_directory", customblocks.ProfileDirectory()),
    ("recent_blog_entries", customblocks.RecentBlogEntries()),
    ("blog_set", customblocks.BlogSetBlock()),
    ("airtable", customblocks.AirTableBlock()),
    ("datawrapper", customblocks.DatawrapperContainerBlock()),
    ("listing", customblocks.ListingBlock()),
    ("profiles", customblocks.ProfileBlock()),
    ("article_teaser_block", customblocks.ArticleTeaserBlock()),
    ("group_listing_block", customblocks.GroupListingBlock()),
    ("image_feature", customblocks.ImageFeatureBlock()),
    ("image_teaser_block", customblocks.ImageTeaserBlock()),
    ("text_only_teaser", customblocks.TextOnlyTeaserBlock()),
    ("block_with_aside", customblocks.BlockWithAside()),
    ("accordion", customblocks.AccordionBlock()),
]
