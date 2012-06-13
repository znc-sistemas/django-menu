from django.conf import settings


def _prepare_menu(path, raw_menu):
    menu = []

    for i in raw_menu:
        active = False
        i = list(i)

        if isinstance(i[2], tuple):
            try:
                subpath = '/'.join(path.lower().split('/')[1:])
            except:
                pass

            i[2] = _prepare_menu(subpath, i[2])
            i[2] = list(i[2])

        if len(i) == 3:  # adiciona permissao NONE  no final
            i.append(None)

        if path.startswith(i[0]):
            active = True
        i.append(active)

        menu.append(i)
    return menu


def _check_permissions(request, raw_menu):
    menu = []

    for item in raw_menu:
        uri, label, sub, permission, active = item
        if permission == None or request.user.has_perm(uri) or request.user.is_superuser:
            if isinstance(sub, list):
                sub = list(_check_permissions(request, sub))
            menu.append([uri, label, sub,  active])
    return menu


def menu(request):
    raw_menu = [list(i) for i in settings.MENU]
    path = request.path[1:]
    return {'menu': _check_permissions(request, _prepare_menu(path, raw_menu))}


def submenu(request):
    raw_menu = [list(i) for i in settings.MENU]
    submenu = []

    # check if URI is /path/subpath
    try:
        path = '/'.join(request.path[1:].lower().split('/')[1:])
    except:
        path = ''

    for item in raw_menu:
        if request.path[1:].startswith(item[0]) and isinstance(item[2], tuple):
            submenu = item[2]
    return {'submenu': _check_permissions(request, _prepare_menu(path, submenu))}
