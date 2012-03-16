from django.conf import settings

def _prepare_menu(request, raw_menu):    
    for i in raw_menu:
        if len(i) == 2:
            i.append(None)

    menu = []
    path = request.path[1:].lower()

    for item in raw_menu:
        label, uri, permission = item
        if permission == None or request.user.has_perm(permission):
            menu.append((label, uri))
    return menu

def menu(request):
    raw_menu = [list(i) for i in settings.MENU]
    return {'menu': _prepare_menu(request, raw_menu)}

def submenu(request):
    raw_menu = [list(i) for i in settings.MENU]
    submenu = []
    for item in raw_menu:
        if request.path[1:].startswith(item[0].lower()) and isinstance(item[1], tuple):
            submenu = item[1]
    return {'submenu': submenu}
