from django.test import TestCase
from django.template import Template, Context


class TemplatetagsTest(TestCase):

    def test_simple_menu_should_render(self):
        context = Context({'menu': [['home', 'Home', None, False]]})
        out = Template(
            '{% load menu %}'
            '{% menu %}'
        ).render(context)
        self.assertEqual(out, '<ul><li><a href="/home">Home</a></li></ul>')

    def test_submenu_should_render(self):
        context = Context({'submenu': [['subhome', 'Sub Home', None, False]]})
        out = Template(
            '{% load menu %}'
            '{% submenu %}'
        ).render(context)
        self.assertEqual(out, '<ul><li><a href="/subhome">Sub Home</a></li></ul>')

    def test_menu_with_submenu_should_render(self):
        context = Context({'menu': [['home', 'Home', [['subhome', 'Sub Home', None, False]], False]], 'submenu': [['home/subhome', 'Sub Home', None, False]]})
        out = Template(
            '{% load menu %}'
            '{% menu %}'
            '{% submenu %}'
        ).render(context)
        self.assertEqual(out, '<ul><li><a href="/home">Home</a><ul><li><a href="/home/subhome">Sub Home</a></li></ul></li></ul><ul><li><a href="/home/subhome">Sub Home</a></li></ul>')
