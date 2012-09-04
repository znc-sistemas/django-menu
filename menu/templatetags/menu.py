from django import template
from django.conf import settings

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


def get_submenu(path, menu,  path_menu=''):
    '''

    '''
    # active = False
    menu_items = []
    sub_menu = None
    if menu[2] is not None:  # check if it have  a submenu
        for menu_item in menu[2]:
            url_menu = "%s/%s" % (path_menu, menu_item[0])
            if path.find(url_menu) == 0:
                path_menu = url_menu
                sub_menu = menu_item
            menu_items.append((menu_item[0], menu_item[1], url_menu))
        if sub_menu:
            menu_items = get_submenu(path, sub_menu, path_menu)
    return menu_items


def submenu(request, depth=1):
    path = "/".join(request.path.split("/")[:depth]) or "/"

    #return {'menu': _check_permissions(request, _prepare_menu(path, raw_menu))}
    return {'submenu': get_submenu(path, settings.MENU)}

