from django import template
from django.conf import settings

register = template.Library()


def get_submenu(path, menu,  path_menu=''):
    '''
    path_menu: do not use this param. Internal using only

    '''
    # active = False
    menu_items = []
    sub_menu = None
    if menu[2] is not None:  # check if path has submenu
        #walk trought submenus items
        for menu_item in menu[2]:
            #for each item in submenu, it check if its part of given path
            url_menu = "%s/%s" % (path_menu, menu_item[0])
            check_path = path.find(url_menu) == 0
            if check_path:
                path_menu = url_menu
                sub_menu = menu_item
            menu_items.append((menu_item[0], menu_item[1], url_menu))
        if sub_menu:
            menu_items = get_submenu(path, sub_menu, path_menu)
    return menu_items


@register.simple_tag(takes_context=True)
def submenu(context, depth=1):
    path = "/".join(context["request_path"].split("/")[:depth]) or "/"
    menu = ""
    if depth > len(context["request_path"].split("/")):
        return ""
    for name, label, uri in get_submenu(path, settings.MENU):
        liclass = ""
        if context["request_path"].find(uri) != -1:
            liclass = ' class="active"'

        menu += '<li%s><a href="%s">%s</a></li>' % (liclass, uri, label)
    return menu


def _menuing(raw_menu, old_uri=None):
    menu = ''

    for name, label, uri in raw_menu:
            menu += '<li%s><a href="%s">%s</a></li>' % ('', uri, label)
    return menu


def do_submenu(parser, token):
    return SubmenuNode()


class SubmenuNode(template.Node):
    def render(self, context):
        return _menuing(context['submenu'])



