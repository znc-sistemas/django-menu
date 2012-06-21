from django.conf import settings
'''
/menu1
/menu2
   /menu21
   /menu22
   /menu23
/menu3/
   /menu31
       /menu311/
           /menu3111
       /menu312
       /menu313

>>> str = "/"
>>> str.split('/')
['', '']
>>> str = "/manu1"
>>> str.split('/')
['', 'manu1']
>>> str = "/manu1/menu2"
>>> str.split('/')
['', 'manu1', 'menu2']

def main():
    menu = get_submenu("/menu4", MENU)
    print menu

if __name__ == "__main__":
    main()

MENU = (
   '', '', (
       ('menu1', 'menu 1', None),
       ('menu2', 'menu 2', (
           ('menu21', 'menu2 sub1', None),
           ('menu22', 'menu2 sub2', None)
           )
           ),
       ('menu3', 'menu 3', (
           ('menu31', 'menu3 sub1', None),
           ('menu32', 'menu3 sub2', None),
           ('menu33', 'menu3 sub3', (
               ('menu331', 'menu33 sub1', None),
               ('menu332', 'menu33 sub2', None),
               ('menu333', 'menu33 sub3', None)
               ),
               ),
           ),
           ),
       ('menu4', 'menu 4', None),)
   )

'''


def get_submenu(path, menu,  path_menu=''):
    '''
    '/music/bands/the_beatles/' =  ['', 'music', 'bands', 'the_beatles', '']
    '''
    # active = False
    menu_items = []
    sub_menu = None
    if menu[2] is not None:
        for menu_item in menu[2]:
            url_menu = "%s/%s" % (path_menu, menu_item[0])
            if path.find(url_menu) == 0:
                path_menu = url_menu
                sub_menu = menu_item
            menu_items.append((menu_item[0], menu_item[1], url_menu))
        if sub_menu:
            menu_items = get_submenu(path, sub_menu, path_menu)
    return menu_items



def menu(request):
    #return {'menu': _check_permissions(request, _prepare_menu(path, raw_menu))}
    return {'menu': get_submenu("/", settings.MENU)}


def submenu(request):
    #return {'menu': _check_permissions(request, _prepare_menu(path, raw_menu))}
    return {'submenu': get_submenu(request.path, settings.MENU)}
