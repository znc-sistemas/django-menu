from django.conf import settings


def _prepare_menu(path, raw_menu):
    menu = []

    for i in raw_menu:
        active = False
        i = list(i)
        if isinstance(i[2], tuple):
            i[2] = _prepare_menu(path, i[2])
            i[2] = list(i[2])

        if len(i) == 3:
            i.append(None)
        if path.startswith(i[0].lower()):
            active = True
        i.append(active)
        menu.append(i)
    return menu


def _check_permissions(request, raw_menu):
    menu = []

    for item in raw_menu:
        uri, label, sub, permission, active = item
        if permission == None or request.user.has_perm(permission) or request.user.is_superuser:
            if isinstance(uri, list):
                uri = tuple(_check_permissions(request, uri))
            menu.append((uri, label, sub,  active))
    return menu


def menu(request):
    raw_menu = [list(i) for i in settings.MENU]
    path = request.path[1:].lower()

    return {'menu': _check_permissions(request, _prepare_menu(path, raw_menu))}


def submenu(request):
    raw_menu = [list(i) for i in settings.MENU]
    submenu = []
    path = request.path[1:].lower()

    for item in raw_menu:
        if request.path[1:].startswith(item[0].lower()) and isinstance(item[2], tuple):
            submenu = item[2]
    return {'submenu': _check_permissions(request, _prepare_menu(path, submenu))}
