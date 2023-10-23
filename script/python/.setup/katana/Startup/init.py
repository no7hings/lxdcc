# coding:utf-8
import sys
# noinspection PyUnresolvedReferences
from Katana import Callbacks


class Setup(object):
    @classmethod
    def build_menu(cls):
        from lxkatana import ktn_core

        if ktn_core.get_is_ui_mode():
            sys.stdout.write('lx-katana menu-setup is started\n')
            from lxkatana import ktn_setup

            ktn_setup.KatanaMenuSetup().set_setup()
            sys.stdout.write('lx-katana menu-setup is completed\n')

    @classmethod
    def build_lua(cls):
        from lxbasic import bsc_core

        bsc_core.EnvExtraMtd.append_lua_path(
            '{}/?.lua'.format(
                bsc_core.Resource.get(
                    'lua-scripts'
                )
            )
        )

    @classmethod
    def build_workspace(cls):
        from lxkatana import ktn_setup

        sys.stdout.write('lx-katana workspace-setup is started\n')
        ktn_setup.KatanaWorkspaceSetup().set_setup()
        sys.stdout.write('lx-katana workspace-setup  is completed\n')

    @classmethod
    def build_hot_key(cls):
        from lxkatana import ktn_core

        if ktn_core.get_is_ui_mode():
            sys.stdout.write('lx-katana hot-key-setup is started\n')
            ktn_core.LayoutNodeHotKey().register()
            sys.stdout.write('lx-katana hot-key-setup  is completed\n')

    @classmethod
    def set_run(cls, *args, **kwargs):
        sys.stdout.write('lx-katana setup is started\n')
        cls.build_menu()
        cls.build_lua()
        cls.build_hot_key()
        cls.build_workspace()
        sys.stdout.write('lx-katana setup is completed\n')


class ArnoldSetup(object):
    @classmethod
    def set_events_register(cls):
        from lxkatana import ktn_core

        ss = [
            (ktn_core.ArnoldEventMtd.on_material_create, ktn_core.EventOpt.EventType.NodeCreate),
            (ktn_core.ArnoldEventMtd.on_image_create, ktn_core.EventOpt.EventType.NodeCreate),
        ]
        #
        for handler, event_type in ss:
            event_opt = ktn_core.EventOpt(
                handler=handler, event_type=event_type
            )
            event_opt.register()

    @classmethod
    def set_callbacks_register(cls):
        pass

    @classmethod
    def set_run(cls, *args, **kwargs):
        sys.stdout.write('lx-arnold setup is started\n')
        cls.set_events_register()
        cls.set_callbacks_register()
        sys.stdout.write('lx-arnold setup is completed\n')


Callbacks.addCallback(
    callbackType=Callbacks.Type.onStartupComplete,
    callbackFcn=Setup.set_run
)

Callbacks.addCallback(
    callbackType=Callbacks.Type.onStartupComplete,
    callbackFcn=ArnoldSetup.set_run
)
