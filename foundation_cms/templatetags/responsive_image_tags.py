from django import template

register = template.Library()


@register.filter
def is_webp(image):
    """Check if an image file is a WebP format"""
    if not image or not hasattr(image, 'file') or not hasattr(image.file, 'name'):
        return False
    return image.file.name.lower().endswith('.webp')


@register.simple_tag
def colon_to_slash(value):
    """Convert colon-separated ratio to slash format (e.g., '2:3' to '2/3')"""
    return value.replace(":", "/")


@register.simple_tag
def orientation_to_ratio(orientation):
    """Map orientation keywords to aspect ratios"""
    mapping = {
        "landscape": "3:2",
        "portrait": "2:3",
        "square": "1:1",
        "widescreen": "16:9",
    }
    return mapping.get(orientation, "3:2")  # Default to 3:2 if unknown


@register.inclusion_tag("patterns/components/responsive_image.html")
def responsive_image(image, ratio, base_width=300, sizes="(max-width: 639px) 100vw, 33vw", classnames=""):
    """
    Generate responsive images with configurable dimensions.

    Args:
        image: Wagtail image object
        ratio: Aspect ratio as string (e.g., "3:2", "2:3", "16:9", "1:1")
        base_width: Base width for scaling (smallest size)
        sizes: HTML sizes attribute for responsive behavior
        classnames: Optional CSS classes to apply to the <img>

    Returns:
        dict: Template context containing:
            - renditions: List of image renditions with widths
            - sizes: HTML sizes attribute
            - primary_rendition: Default image rendition for src

    Example:
        {% responsive_image page.hero_image ratio="16:9" base_width=400 %}
        {% responsive_image page.hero_image ratio="3:2" classnames="image-block__image" %}
    """
    if not image:
        return {}

    if not ratio:
        raise ValueError("ratio parameter is required")

    # Parse and validate ratio
    try:
        ratio_parts = ratio.split(":")
        if len(ratio_parts) != 2:
            raise ValueError(f"Invalid ratio format: {ratio}")

        width_ratio = float(ratio_parts[0])
        height_ratio = float(ratio_parts[1])

        if width_ratio <= 0 or height_ratio <= 0:
            raise ValueError("Ratio values must be positive")
    except (ValueError, IndexError) as e:
        raise ValueError(f"Error parsing ratio '{ratio}': {str(e)}")

    # Calculate dimensions and generate renditions
    multipliers = [1, 1.5, 2, 3]
    renditions = []

    for mult in multipliers:
        width = int(base_width * mult)
        height = int(width * height_ratio / width_ratio)

        rendition = image.get_rendition(f"fill-{width}x{height}")
        renditions.append(
            {
                "rendition": rendition,
                "width": width,
            }
        )

    # Use the second rendition (1.5x) as the primary/default src
    # 1.5x provides good quality for most devices while keeping file size reasonable
    # The browser can still choose higher resolutions from srcset when needed
    primary_rendition = renditions[1]["rendition"] if len(renditions) > 1 else renditions[0]["rendition"]

    return {
        "renditions": renditions,
        "sizes": sizes,
        "primary_rendition": primary_rendition,
        "classnames": classnames,
    }
