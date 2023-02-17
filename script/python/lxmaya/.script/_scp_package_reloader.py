# coding:utf-8


class Packages(object):
    @classmethod
    def set_reload(cls):
        import lxbasic.objects as bsc_objects
        #
        p = bsc_objects.PyReloader(
            [
                'lxbasic', 'lxscheme', 'lxuniverse', 'lxresolver', 'lxshotgun', 'lxarnold', 'lxusd',
                'lxutil', 'lxutil_gui',
                'lxmaya', 'lxmaya_gui'
            ]
        )
        p.set_reload()
