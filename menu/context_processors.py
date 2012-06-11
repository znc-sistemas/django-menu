from django.conf import settings

def _prepare_menu(path, raw_menu):
    '''
        verifica se o menu tem submenus
        marca menu se ativo
        apennda NONE para menus sem submenus
    '''
    menu = []
    import pdb; pdb.set_trace()
    for i in raw_menu:
        active = False
        

        if isinstance(i[2], list):
            try:
                subpath = '/'.join(path.lower().split('/')[1:])
            except:
                pass

            i[1] = _prepare_menu(subpath, i[2])
            #i[1] = list(i[1])

        #if len(i) == 2:
        #    i.append(None)

        if path.startswith(i[0].lower()):
            active = True
        i.append(active)
        menu.append(i)
        #print "menu prepared %s" % menu
    return menu

def _check_permissions(request, raw_menu):
    menu = []
    import pdb; pdb.set_trace()
    for item in raw_menu:
        
        uri, label, submenu, active = item
        if request.user.has_perm(uri) or request.user.is_superuser:
            if isinstance(submenu, list):
                uri = tuple(_check_permissions(request, uri))
            menu.append((label, uri, active))
    return menu

def menu(request):
    import pdb; pdb.set_trace()
    raw_menu = [list(i) for i in settings.MENU]

    path = request.path[1:].lower()
    #print "menu context menu %s" % raw_menu
    menu = _check_permissions(request, _prepare_menu(path, raw_menu))
    return {'menu': menu}

def submenu(request):
    raw_menu = [list(i) for i in settings.MENU]
    submenu = []

    # check if URI is /path/subpath
    try:
        path = '/'.join(request.path[1:].lower().split('/')[1:])
    except:
        path = ''
    for item in raw_menu:
        #print "request.path -> %s" % request.path[1:]
        #print "item [0] -> %s" % item[0].lower()
        #print  " item[n] starts with %s" % request.path[1:].startswith(item[0].lower())
        #print "========================================="
        if request.path[1:].startswith(item[0].lower()) and isinstance(item[1], tuple):
            submenu = item[1]
    #print "submenu = %s" %  submenu
    return {'submenu': _check_permissions(request, _prepare_menu(path, submenu))}
