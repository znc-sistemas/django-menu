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
       ('menu1', 'menu 1', (
           ('menu11', 'menu1 sub1', None),
           ('menu12', 'menu1 sub2', None)
           )
        ),
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


def request_path(request):
    #return {'menu': _check_permissions(request, _prepare_menu(path, raw_menu))}
    return {'request_path': request.path}
