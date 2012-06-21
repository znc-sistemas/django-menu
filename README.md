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

```python
MENU = (
            ('URI', 'Label',
            	(
            		('Submenu', 'submenu', None, 'Link permission (optional)'),
            	), 'Link permission (optional)'),
            # Or
            ('URI', 'Label', None, 'Link permission (optional)'),
        )
```
