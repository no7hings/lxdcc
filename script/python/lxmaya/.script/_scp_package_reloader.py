# coding:utf-8


class Packages(object):
    @classmethod
    def set_reload(cls):
        import lxutil.objects as utl_objects
        #
        p = utl_objects.PyReloader(
            [
                'lxscheme',
                'lxbasic', 'lxobj', 'lxresolver', 'lxshotgun', 'lxarnold', 'lxusd',
                'lxutil', 'lxutil_fnc', 'lxutil_gui',
                'lxmaya', 'lxmaya_fnc', 'lxmaya_gui'
            ]
        )
        p.set_reload()
