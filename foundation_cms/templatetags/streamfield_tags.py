from django import template

register = template.Library()


@register.simple_tag
def get_block_context_value(block, page, key):
    """Get a value from block's context."""
    if hasattr(block.block, "get_context"):
        context = block.block.get_context(block.value, parent_context={"page": page})
        return context.get(key, False)
    return False
