from django import template

register = template.Library()


def _menuing(raw_menu, old_uri=None):
    menu = ''

    for name, label, uri in raw_menu:

            menu += '<li%s><a href="%s">%s</a></li>' % ('', uri, label)
    return menu


def do_menu(parser, token):
    return MenuNode()


def do_submenu(parser, token):
    return SubmenuNode()


class MenuNode(template.Node):
    def render(self, context):
        return _menuing(context['menu'])


class SubmenuNode(template.Node):
    def render(self, context):
        return _menuing(context['submenu'])

register.tag('menu', do_menu)
register.tag('submenu', do_submenu)
