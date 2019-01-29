from django import template

register = template.Library()


# Instantiate a horizontal nav based on the current page's relation to other pages
@register.inclusion_tag('category_nav_links.html', takes_context=True)
def category_nav(context, current_category, all_categories):
    return {
        'current_category': current_category,
        'categories': all_categories,
        'featured_categories': all_categories.filter(featured=True),
        'other_categories': all_categories.filter(featured=False)
    }
