from django import template

register = template.Library()

def _menuing(raw_menu, old_link=''):
    menu = ''

    for label, link, active in raw_menu:

        if active:
            act = ' class="active"'
        else:
            act = ''

        if isinstance(link, tuple):
            # is submenu, so, I use label in link field
            old_link = '%s/%s' % (old_link, label.lower())
            menu += '<li%s><a href="%s">%s</a><ul>%s</ul></li>' % (act, old_link, label, _menuing(link, old_link))
        else:
            menu += '<li%s><a href="%s">%s</a></li>' % (act, '%s/%s' % (old_link, link), label)
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
