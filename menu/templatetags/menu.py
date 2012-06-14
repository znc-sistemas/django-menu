from django import template

register = template.Library()


def _menuing(raw_menu, old_uri=None):
    menu = ''

    for uri, label, sub, active in raw_menu:

        if active:
            act = ' class="active"'
        else:
            act = ''

        if not old_uri == None:
            full_uri = '%s/%s' % (old_uri, uri)
        else:
            full_uri = '/%s' % uri

        if isinstance(sub, list):
            # is a real submenu
            menu += '<li%s><a href="%s">%s</a><ul>%s</ul></li>' % (act, full_uri, label, _menuing(sub, full_uri))
        else:
            menu += '<li%s><a href="%s">%s</a></li>' % (act, full_uri, label)
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
