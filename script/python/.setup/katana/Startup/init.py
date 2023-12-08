# coding:utf-8
import sys
# noinspection PyUnresolvedReferences
from Katana import Callbacks


class Setup(object):
    KEY = 'katana setup'

    @classmethod
    def build_menu(cls):
        import lxlog.core as log_core

        import lxkatana.core as ktn_core

        if ktn_core.KtnUtil.get_is_ui_mode():
            with log_core.LogContext.create(cls.KEY, 'register menu'):
                ktn_core.KatanaMenuSetup().set_setup()

    @classmethod
    def build_lua(cls):
        import lxbasic.core as bsc_core

        bsc_core.EnvExtraMtd.append_lua_path(
            '{}/?.lua'.format(
                bsc_core.ExtendResource.get(
                    'lua-scripts'
                )
            )
        )

    @classmethod
    def build_workspace(cls):
        import lxlog.core as log_core

        import lxkatana.core as ktn_core

        with log_core.LogContext.create(cls.KEY, 'register workspace'):
            ktn_core.KatanaWorkspaceSetup().set_setup()

    @classmethod
    def build_hot_key(cls):
        import lxlog.core as log_core

        import lxkatana.core as ktn_core

        if ktn_core.KtnUtil.get_is_ui_mode():
            with log_core.LogContext.create(cls.KEY, 'register hot key'):
                ktn_core.HotKeyForNodeGraphLayout().register()
                ktn_core.HotKeyForNodeGraphPaste().register()

    @classmethod
    def set_run(cls, *args, **kwargs):
        import lxlog.core as log_core

        with log_core.LogContext.create(cls.KEY, 'all'):
            cls.build_menu()
            cls.build_lua()
            cls.build_hot_key()
            cls.build_workspace()


class ArnoldSetup(object):
    KEY = 'arnold setup'

    @classmethod
    def set_events_register(cls):
        import lxlog.core as log_core

        import lxkatana.core as ktn_core

        import lxkatana.scripts as ktn_scripts

        with log_core.LogContext.create(cls.KEY, 'register event'):

            ss = [
                (ktn_scripts.ScpEventForArnold.on_material_create, ktn_core.EventOpt.EventType.NodeCreate),
                (ktn_scripts.ScpEventForArnold.on_node_group_create, ktn_core.EventOpt.EventType.NodeCreate),
                (ktn_scripts.ScpEventForArnold.on_shader_create, ktn_core.EventOpt.EventType.NodeCreate),
                (ktn_scripts.ScpEventForArnold.on_image_create, ktn_core.EventOpt.EventType.NodeCreate),
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
        import lxlog.core as log_core

        with log_core.LogContext.create(cls.KEY, 'all'):
            cls.set_events_register()
            cls.set_callbacks_register()


Callbacks.addCallback(
    callbackType=Callbacks.Type.onStartupComplete,
    callbackFcn=Setup.set_run
)

Callbacks.addCallback(
    callbackType=Callbacks.Type.onStartupComplete,
    callbackFcn=ArnoldSetup.set_run
)
