django-menu
===========

Dynamic menus for Django Apps

Installing
==========

To install, put this in settings.py

```python
INSTALLED_APPS = (
    ...
    'menu',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'menu.context_processors.menu',
    'menu.context_processors.submenu',
)
```

Setting up
==========

To set up your menu:

```python
MENU = (
            ('Link name', 'Link', 'Link permission (optional)'),
        )
```

To use a submenu:

```python
MENU = (
            ('Link name', (('Submenu', 'submenu', 'Link permission (optional)'),), 'Link permission (optional)'),
        )
```
