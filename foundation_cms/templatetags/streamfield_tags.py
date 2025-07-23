from django import template

register = template.Library()


@register.filter
def should_wrap_block(block_type):
    # This is used in streamfield.html to determine if a block should be pre-wrapped with .grid-container etc
    NO_WRAP_BLOCKS = {
        "spotlight_card_set_block",
        "portrait_card_set_block",
        "featured_card_block",
    }
    return block_type not in NO_WRAP_BLOCKS
