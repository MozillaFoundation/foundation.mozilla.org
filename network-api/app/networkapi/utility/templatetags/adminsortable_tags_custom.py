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
    return tmpl.render(context)


@register.simple_tag(takes_context=True)
def render_nested_sortable_objects(
    context,
    objects,
    group_expression,
    sortable_nested_objects_template='adminsortable/shared/nested_objects.html'
):
    context.update({'objects': objects, 'group_expression': group_expression})
    tmpl = template.loader.get_template(sortable_nested_objects_template)
    return tmpl.render(context)


@register.simple_tag(takes_context=True)
def render_list_items(
    context,
    list_objects,
    sortable_list_items_template='adminsortable/shared/list_items.html'
):
    context.update({'list_objects': list_objects})
    tmpl = template.loader.get_template(sortable_list_items_template)
    return tmpl.render(context)


@register.simple_tag(takes_context=True, name='render_object_rep')
def render_object_rep(
    context,
    obj,
    forloop
):
    context.update({'object': obj, 'forloop': forloop})
    tmpl = template.loader.get_template(
        '{app_name}/adminsortable_objects_custom.html'.format(
            app_name=context.get('opts').app_label
        )
    )
    return tmpl.render(context)
