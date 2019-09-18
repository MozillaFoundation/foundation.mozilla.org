from django.apps import apps
from django.db.models import Count
from django.utils.translation import gettext as _


def set_main_site_nav_information(page, context, homepage_class_name):
    # Find the homepage, and then record all pages that should end up as nav items. Note
    # that subclasses can bypass this, because the MozfestHomepage doesn't need any of
    # this work to be done.

    root = list(filter(
        lambda x: x.specific.__class__.__name__ == homepage_class_name,
        page.get_ancestors(True)  # incude ourselves!
    ))[0]

    context['menu_root'] = root
    context['menu_items'] = root.get_children().live().in_menu()
    return context


def get_page_tree_information(page, context):
    '''
    Helper function for abstracting details about page trees
    of the same type. Information returned is:
    - what the root of the tree is
    - what the root page's title is
    - whether the reference page is the tree root
    - whether this is a singleton "tree"
    '''

    ancestors = page.get_ancestors()
    root = next((n for n in ancestors if n.specific_class == page.specific_class), page)
    context['root'] = root

    is_top_page = (root == page)
    context['is_top_page'] = is_top_page

    children = page.get_children().live()
    has_children = len(children) > 0
    context['singleton_page'] = (is_top_page and not has_children)

    mchildren = root.get_children().live().in_menu()
    context['uses_menu'] = len(mchildren) > 0

    return context


def get_descendants(node, list, authenticated=False, depth=0, max_depth=2):
    '''
    helper function to get_menu_pages for performing a depth-first
    discovery pass of all menu-listable children to some root node.
    '''
    if (depth <= max_depth):
        title = node.title
        header = getattr(node.specific, 'header', None)
        if header:
            title = header
        menu_title = title if depth > 0 else _('Overview')
        restriction = node.get_view_restrictions().first()
        try:
            restriction_type = restriction.restriction_type
        except AttributeError:
            restriction_type = None

        list.append({
            'page': node,
            'menu_title': menu_title,
            'depth': depth,
            'restriction': restriction_type,
        })

        nextset = node.get_children().in_menu()

        # Do not show draft/private pages to users who are
        # not logged into the CMS itself.
        if authenticated is False:
            nextset = nextset.live().public()

        for child in nextset:
            get_descendants(child, list, authenticated, depth + 1)


def get_menu_pages(root, authenticated=False):
    '''
    convenience function for getting all (menu listable) child
    pages for some root node.
    '''
    menu_pages = list()
    get_descendants(root, menu_pages, authenticated)
    return menu_pages


def get_mini_side_nav_data(context, page, no_minimum_page_count=False):
    user = context['user']
    authenticated = user.is_authenticated if user else False
    menu_pages = get_menu_pages(context['root'], authenticated)

    # We need at least 2 pages, or a nav menu is meaningless.
    if no_minimum_page_count is False and len(menu_pages) < 2:
        menu_pages = False

    # Return the list of values we need to have our template
    # generate the appropriate sidebar HTML.
    return {
        'singleton_page': context['singleton_page'],
        'current': page,
        'menu_pages': menu_pages,
    }


def get_content_related_by_tag(page, result_count=3):
    """
    Get all posts that feel related to this page, based
    on its `.tags` content. If it has tags.
    """

    tagged_post_types = (
        apps.get_model('wagtailpages', 'BlogPage'),
        # Add more models here as we add tags to more types
    )

    own_tags = page.tags.all()

    related_qs = False

    for post_type in tagged_post_types:
        related_posts = post_type.objects.filter(tags__in=own_tags).distinct()

        # Exlude "this page" from the result set for the page's own.
        # page type, so we don't yield "this page is similar to itself".
        if page.__class__ is post_type:
            related_posts = related_posts.exclude(pk=page.pk)

        if related_qs is False:
            related_qs = related_posts
        else:
            related_qs = related_qs | related_posts

    # Annotate the results by adding a column that, effectively, records
    # a `countDistinct(result_table.tag)` for each related post.
    annotated = related_qs.annotate(num_common_tags=Count('pk'))

    # Finally, we sort on those tag count values, with publication
    # date as secondary sorting, so that "the same number of matching
    # tags" is further sorted such that the most recent post shows
    # up first (note that this is done on the database side, not in python).
    ordered = annotated.order_by(
        '-num_common_tags',
        '-last_published_at'
    )

    return ordered[:result_count]
