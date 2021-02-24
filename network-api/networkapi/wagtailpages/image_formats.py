from wagtail.images.formats import Format, register_image_format

# Set it to 2280px because 1140px is the max width of Bootstrap's container.
# Then we multiply that number by 2 so the image can render well on retina.
register_image_format(
  Format('fullwidth_high_quality', 'Full width high quality', 'richtext-image full-width high-quality', 'width-2280')
)
