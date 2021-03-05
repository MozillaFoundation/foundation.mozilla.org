from . import customblocks
from wagtail.core import blocks

from wagtail_blocks.blocks import HeaderBlock, ListBlock, ImageTextOverlayBlock, CroppedImagesWithTextBlock, \
    ListWithImagesBlock, ThumbnailGalleryBlock, ChartBlock, MapBlock, ImageSliderBlock

"""
We'll need to figure out which components are truly "base" and
which are bits that should be used in subclassing template-based
page types.
"""

base_fields = [
    ('paragraph', blocks.RichTextBlock(
        features=[
            'bold', 'italic', 'large',
            'h2', 'h3', 'h4', 'h5',
            'ol', 'ul',
            'link', 'hr',
        ]
    )),
    ('image', customblocks.AnnotatedImageBlock()),
    ('image_text', customblocks.ImageTextBlock()),
    ('image_text_mini', customblocks.ImageTextMini()),
    ('image_grid', customblocks.ImageGridBlock()),
    ('video', customblocks.VideoBlock()),
    ('iframe', customblocks.iFrameBlock()),
    ('linkbutton', customblocks.LinkButtonBlock()),
    ('spacer', customblocks.BootstrapSpacerBlock()),
    ('quote', customblocks.QuoteBlock()),
    ('pulse_listing', customblocks.PulseProjectList()),
    ('profile_listing', customblocks.LatestProfileList()),
    ('profile_by_id', customblocks.ProfileById()),
    ('profile_directory', customblocks.ProfileDirectory()),
    ('recent_blog_entries', customblocks.RecentBlogEntries()),
    ('airtable', customblocks.AirTableBlock()),
    ('typeform', customblocks.TypeformBlock()),
    ('header', HeaderBlock()),
    ('list', ListBlock()),
    ('image_text_overlay', ImageTextOverlayBlock()),
    ('cropped_images_with_text', CroppedImagesWithTextBlock()),
    ('list_with_images', ListWithImagesBlock()),
    ('thumbnail_gallery', ThumbnailGalleryBlock()),
    ('chart', ChartBlock()),
    ('map', MapBlock()),
    ('image_slider', ImageSliderBlock()),
]
