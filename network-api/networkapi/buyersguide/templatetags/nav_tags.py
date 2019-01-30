from django import template

register = template.Library()

# Determine if a link should be active
@register.simple_tag(name='bg_active_nav')
def bg_active_nav(current, target):
    return 'active' if current == target else ''

# Instantiate a list of category page links based on the current page's relation to them
@register.inclusion_tag('category_nav_links.html', takes_context=True)
def category_nav(context, current_url, current_category, all_categories):
    return {
        'current_url': current_url,
        'current_category': current_category,
        'sorted_categories': all_categories.order_by('-featured'), # featured categories first
    }
