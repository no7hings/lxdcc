# coding:utf-8
# noinspection PyUnresolvedReferences
from Katana import Callbacks


class Setup(object):
    @classmethod
    def set_menu_setup(cls):
        print 'lx-katana-menu-setup: start'
        from lxkatana import ktn_setup
        ktn_setup.KatanaMenuSetup().set_setup()
        print 'lx-katana-menu-setup: complete'
    @classmethod
    def set_run(cls, *args, **kwargs):
        print '*'*40
        print 'lx-katana-setup: start'
        cls.set_menu_setup()
        print 'lx-katana-setup: complete'
        print '*' * 40


class ArnoldSetup(object):
    @classmethod
    def set_events_register(cls):
        from lxkatana import ktn_core
        ss = [
            (ktn_core.ArnoldEventMtd.set_material_create, ktn_core.EventOpt.EventType.NodeCreate),
            (ktn_core.ArnoldEventMtd.set_image_create, ktn_core.EventOpt.EventType.NodeCreate),
        ]
        #
        for handler, event_type in ss:
            event_opt = ktn_core.EventOpt(
                handler=handler, event_type=event_type
            )
            event_opt.set_register()
    @classmethod
    def set_callbacks_register(cls):
        pass
    @classmethod
    def set_run(cls, *args, **kwargs):
        print '*' * 40
        print 'lx-arnold-setup: start'
        cls.set_events_register()
        cls.set_callbacks_register()
        print 'lx-arnold-setup: complete'
        print '*' * 40


Callbacks.addCallback(
    callbackType=Callbacks.Type.onStartupComplete,
    callbackFcn=Setup.set_run
)

Callbacks.addCallback(
    callbackType=Callbacks.Type.onStartupComplete,
    callbackFcn=ArnoldSetup.set_run
)
