from foundation_cms.base.factories import ImageFactory


def build_clean_image(alt_text="Alt text"):
    """
    Build an image value ready to pass ImageBlock.clean() directly.

    StructBlockFactory assigns raw field values without running them through
    to_python(), but ImageBlock.clean() expects an already-converted image
    instance with `contextual_alt_text`/`decorative` set (normally attached by
    ImageBlock.to_python()). Without these, clean() raises AttributeError
    instead of the intended ValidationError.
    """
    image = ImageFactory()
    image.contextual_alt_text = alt_text
    image.decorative = False
    return image
