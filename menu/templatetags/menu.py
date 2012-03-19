from django import template

register = template.Library()

def _menuing(raw_menu, old_label=''):
    menu = ''
    for label, link in raw_menu:
        if isinstance(link, tuple):
            if old_label:
                menu += '<li><a href="%s">%s</a><ul>%s</ul></li>' %\
                    (label.lower(), label, _menuing(link, old_label + '/' + label.lower()))
            else:
                menu += '<li><a href="%s">%s</a><ul>%s</ul></li>' %\
                    (label.lower(), label, _menuing(link, label.lower()))
        else:
            if old_label:
                menu += '<li><a href="%s">%s</a></li>' % (old_label + '/' + link, label)
            else:
                menu += '<li><a href="%s">%s</a></li>' % (link, label)
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
