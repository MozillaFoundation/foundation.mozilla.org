from django import template

register = template.Library()


# Instantiate a horizontal nav based on the current page's relation to other pages
@register.inclusion_tag('category_nav_links.html', takes_context=True)
def category_nav(context, current_category, all_categories):
    return {
        'current_category': current_category,
        'sorted_categories': all_categories.order_by('-featured'), # featured categories first
    }
