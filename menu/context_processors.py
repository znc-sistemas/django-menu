from django.conf import settings

def menu(request):
    m = [list(i) for i in settings.MENU]
    [ i.append(None) for i in m if len(i) == 2]

    menu = []

    for item in m:
        label, uri, permission = item
        if permission == None:
             menu.append((label, uri))
        elif request.user.has_perm(permission):
             menu.append((label, uri))
    return {'menu': menu}
