# coding:utf-8


class Packages(object):
    @classmethod
    def set_reload(cls):
        set_reload()


def set_reload(modules=None):
    import lxbasic.objects as bsc_objects
    if isinstance(modules, (tuple, list)):
        p = bsc_objects.PyReloader(modules)
    else:
        p = bsc_objects.PyReloader(
            [
                'lxscheme', 'lxsession', 'lxdatabase', 'lxdeadline', 'lxbasic', 'lxobj', 'lxresolver', 'lxarnold',
                'lxusd', 'lxusd_fnc',
                'lxutil', 'lxutil_fnc', 'lxutil_gui',
                'lxshotgun', 'lxshotgun_fnc', 'lxshotgun_gui',
                'lxgui', 'lxgui_fnc',
                'lxclarisse', 'lxclarisse_gui',
            ]
        )
    p.set_reload()
