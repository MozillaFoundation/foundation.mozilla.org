from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def render_sortable_objects(
    context,
    objects,
    sortable_objects_template='adminsortable/shared/objects.html'
):
    context.update({'objects': objects})
    tmpl = template.loader.get_template(sortable_objects_template)
    return tmpl.render({
        'objects': objects,
        'opts': context.get('opts'),
    })


@register.simple_tag(takes_context=True)
def render_nested_sortable_objects(
    context,
    objects,
    group_expression,
    sortable_nested_objects_template='adminsortable/shared/nested_objects.html'
):
    context.update({'objects': objects, 'group_expression': group_expression})
    tmpl = template.loader.get_template(sortable_nested_objects_template)
    return tmpl.render({
        'objects': objects,
        'group_expression': group_expression,
        'opts': context.get('opts'),
    })


@register.simple_tag(takes_context=True)
def render_list_items(
    context,
    list_objects,
    sortable_list_items_template='adminsortable/shared/list_items.html'
):
    tmpl = template.loader.get_template(sortable_list_items_template)
    return tmpl.render({
        'list_objects': list_objects,
        'opts': context.get('opts'),
    })


@register.simple_tag(takes_context=True, name='render_object_rep')
def render_object_rep(
    context,
    obj,
    forloop
):
    tmpl = template.loader.get_template(
        '{app_name}/adminsortable_objects_custom.html'.format(
            app_name=context.get('opts').app_label
        )
    )
    return tmpl.render({
        'object': obj,
        'forloop': forloop,
        'opts': context.get('opts'),
    })
