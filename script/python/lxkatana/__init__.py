# coding:utf-8


class Packages(object):
    @classmethod
    def set_reload(cls):
        set_reload()


def set_reload(modules=None):
    import lxutil.objects as utl_objects
    if isinstance(modules, (tuple, list)):
        p = utl_objects.PyReloader(modules)
    else:
        p = utl_objects.PyReloader(
            [
                'lxscheme', 'lxsession', 'lxdeadline', 'lxbasic', 'lxobj', 'lxresolver', 'lxarnold',
                'lxusd', 'lxusd_fnc',
                'lxutil', 'lxutil_fnc', 'lxutil_gui',
                'lxshotgun', 'lxshotgun_fnc', 'lxshotgun_gui',
                'lxgui', 'lxgui_fnc',
                'lxkatana', 'lxkatana_fnc', 'lxkatana_gui'
            ]
        )
    p.set_reload()
