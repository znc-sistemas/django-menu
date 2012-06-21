from django.test import TestCase
from mock import patch

from menu import context_processors

MENU_MOCK = (
                ('home', 'Home', None),
                ('user', 'User', None),
                ('menu', 'O Menu',
                    (
                        ('submenu', 'Submenu', None),
                    )
                ),
                ('admin', 'Admin', None, 'is_admin'),
            )


class UserMock(object):
    def __init__(self, username):
        self.username = username
        self.is_superuser = username == 'admin' and True or False

    def has_perm(self, permission):
        if self.username == 'admin':
            return True
        return False


class RequestMock(object):
    def __init__(self, path, user):
        self.path = path
        self.user = user


class ContextProcessorsTests(TestCase):

    def setUp(self):
        self.patcher = patch('menu.context_processors.settings', create=True)
        self.patcher.start()
        context_processors.settings.MENU = MENU_MOCK

    def tearDown(self):
        self.patcher.stop()

    def test_menu_with_ordinary_user(self):
        menu_from_context = context_processors.menu(RequestMock('/', UserMock('user')))
        my_menu = {'menu': [['home', 'Home', None, False], ['user', 'User', None, False], ['menu', 'O Menu', [['submenu', 'Submenu', None, False], ], False]]}
        self.assertEquals(menu_from_context, my_menu)

    def test_menu_with_admin_user(self):
        menu_from_context = context_processors.menu(RequestMock('/', UserMock('admin')))
        my_menu = {'menu': [['home', 'Home', None, False], ['user', 'User', None, False], ['menu', 'O Menu', [['submenu', 'Submenu', None, False], ], False], ['admin', 'Admin', None, False]]}
        self.assertEquals(menu_from_context, my_menu)

    def test_submenu_should_be_empty_list(self):
        submenu_from_context = context_processors.submenu(RequestMock('/', UserMock('admin')))
        my_submenu = {'submenu': []}
        self.assertEquals(submenu_from_context, my_submenu)

    def test_submenu_should_be_filled_list(self):
        submenu_from_context = context_processors.submenu(RequestMock('/menu', UserMock('admin')))
        my_submenu = {'submenu': [['submenu', 'Submenu', None,  False]]}
        self.assertEquals(submenu_from_context, my_submenu)

    def test_menu_option_should_be_activated_in_correct_path(self):
        menu_from_context = context_processors.menu(RequestMock('/home', UserMock('user')))
        my_menu = {'menu': [['home', 'Home', None, True], ['user', 'User', None, False], ['menu', 'O Menu', [['submenu', 'Submenu', None, False], ], False]]}
        self.assertEquals(menu_from_context, my_menu)

    def test_submenu_option_should_be_activated_in_correct_path(self):
        menu_from_context = context_processors.menu(RequestMock('/menu/submenu', UserMock('user')))
        my_menu = {'menu': [['home', 'Home', None, False], ['user', 'User', None, False], ['menu', 'O Menu', [['submenu', 'Submenu', None, True], ], True]]}
        self.assertEquals(menu_from_context, my_menu)
