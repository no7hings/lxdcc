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
                'lxbasic', 'lxcontent', 'lxsession', 'lxdatabase', 'lxdeadline', 'lxuniverse', 'lxresolver', 'lxarnold',
                'lxusd',
                'lxutil', 'lxutil_gui',
                'lxshotgun', 'lxshotgun_gui',
                'lxhoudini', 'lxhoudini_gui'
            ]
        )
    p.set_reload()
