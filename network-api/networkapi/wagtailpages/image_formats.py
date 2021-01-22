from wagtail.images.formats import Format, register_image_format, unregister_image_format

# We can't override existing image format,
# so we are unregistering it and then re-registering it with new values instead.
# Set it to 2280px because 1140px is the max width of Bootstrap's container.
# Then we multiply that number by 2 so the image can render well on retina.
unregister_image_format('fullwidth')
register_image_format(Format('fullwidth', 'Full width', 'richtext-image full-width', 'width-2280'))
