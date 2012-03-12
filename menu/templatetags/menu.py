from django import template

register = template.Library()

@register.inclusion_tag('menu/menu.html', takes_context=True)
def menu(context):
    menu = context['menu']
    return {'menu': menu}

