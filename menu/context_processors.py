from django.conf import settings

def _prepare_menu(path, raw_menu):
    menu = []

    for i in raw_menu:
        active = False
        i = list(i)

        if isinstance(i[1], tuple):
            try:
                subpath = '/'.join(path.lower().split('/')[1:])
            except:
                pass

            i[1] = _prepare_menu(subpath, i[1])
            i[1] = list(i[1])

        if len(i) == 2:
            i.append(None)

        if path.startswith(i[0].lower()):
            active = True
        i.append(active)
        menu.append(i)
    return menu

def _check_permissions(request, raw_menu):
    menu = []

    for item in raw_menu:
        label, uri, permission, active = item
        if permission == None or request.user.has_perm(permission):
            if isinstance(uri, list):
                uri = tuple(_check_permissions(request, uri))
            menu.append((label, uri, active))
    return menu

def menu(request):
    raw_menu = [list(i) for i in settings.MENU]
    path = request.path[1:].lower()

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
        if request.path[1:].startswith(item[0].lower()) and isinstance(item[1], tuple):
            submenu = item[1]
    return {'submenu': _check_permissions(request, _prepare_menu(path, submenu))}
