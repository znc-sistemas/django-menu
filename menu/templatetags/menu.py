from django import template

register = template.Library()

def do_menu(parser, token):
    try:
        inline = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires an argument.' % token.content.split()[0])

    return MenuNode(inline)

class MenuNode(template.Node):
    def __init__(self, inline):
        self.inline = inline

    def _menuing(self, t):
        menu = ''
        for label, link in t:
            if isinstance(link, tuple):
                menu += '<li><a href="#">%s</a><ul>%s</ul></li>' % (label, self._menuing(link))
            else:
                menu += '<li><a href="%s">%s</a></li>' % (link, label)

        return menu


    def render(self, context):
        return self._menuing(context['menu'])

register.tag('menu', do_menu)
