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

    return context


def get_descendants(node, list, depth=0, max_depth=2):
    '''
    helper function to get_menu_pages for performing a depth-first
    discovery pass of all menu-listable children to some root node.
    '''
    if (depth <= max_depth):
        title = node.specific.header if node.specific.header else node.title
        menu_title = title if depth > 0 else 'Overview'
        list.append({
            'page': node,
            'menu_title': menu_title,
            'depth': depth,
        })
        for child in node.get_children().live().in_menu():
            get_descendants(child, list, depth + 1)


def get_menu_pages(root):
    '''
    convenience function for getting all (menu listable) child
    pages for some root node.
    '''
    menu_pages = list()
    get_descendants(root, menu_pages)
    return menu_pages
