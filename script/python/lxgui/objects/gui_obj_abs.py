# coding:utf-8
import os

import inspect

from lxbasic import bsc_configure, bsc_core

import lxbasic.objects as bsc_objects

from lxutil import utl_core


class AbsSession(object):
    Platform = bsc_configure.Platform
    Application = bsc_configure.Application
    @classmethod
    def _get_current_platform_(cls):
        return utl_core.System.get_platform()
    @classmethod
    def _get_current_application_(cls):
        return utl_core.System.get_application()
    @classmethod
    def _get_current_system_(cls):
        return '{}-{}'.format(
            cls._get_current_platform_(),
            cls._get_current_application_()
        )
    #
    def __init__(self, *args, **kwargs):
        if 'configure' in kwargs:
            self._configure = kwargs['configure']
        else:
            python_file_path = inspect.getfile(self.__class__)
            self._configure_file_path = '{}.yml'.format(os.path.splitext(python_file_path)[0])
            self._configure = bsc_objects.Configure(value=self._configure_file_path)
        #
        if 'variants' in kwargs:
            self._configure.set(
                'variants', kwargs['variants']
            )
            self._variants = kwargs['variants']
        else:
            self._variants = {}
        #
        self._configure.set_flatten()
        #
        self._gui_name = self._configure.get(
            'option.gui.name'
        )
        self._gui_icon_name = self._configure.get(
            'option.gui.icon_name'
        )
        #
        self._platform = self._get_current_platform_()
        #
        self._application = self._get_current_application_()
        self._system = bsc_core.SystemMtd.get_current()
        self._system_includes = bsc_core.SystemMtd.get_system_includes(
            self._configure.get(
                'option.systems'
            ) or []
        )
        self._variants['application'] = self._application
    @property
    def platform(self):
        return self._platform
    @property
    def application(self):
        return self._application
    @property
    def system(self):
        return self._system
    @property
    def system_includes(self):
        return self._system_includes
    @property
    def gui_name(self):
        return self._gui_name
    @property
    def gui_icon_name(self):
        return self._gui_icon_name
    @property
    def variants(self):
        return self._variants

    def get_is_loadable(self):
        return self.system in self.system_includes

    def get_is_executable(self):
        return True

    def set_run(self):
        if self.get_is_loadable():
            if self.get_is_executable():
                self._set_pre_run_()
                self.set_execute()
                self._set_post_run_()

    def _set_pre_run_(self):
        pass

    def set_execute(self):
        pass

    def _set_post_run_(self):
        pass

    def _set_debug_run_(self):
        try:
            self.set_run()
        except Exception:
            from lxutil import utl_core
            utl_core.ExceptionCatcher.set_create()
            raise

    def _set_code_execute_(self, raw):
        try:
            # noinspection PyUnusedLocal
            session = self
            code_exec = compile(raw, '<string>', 'exec')
            exec code_exec
        #
        except Exception:
            from lxutil import utl_core
            utl_core.ExceptionCatcher.set_create()
            raise


class AbsRsvObjSession(AbsSession):
    def __init__(self, *args, **kwargs):
        self._rsv_obj = args[0]
        self._rsv_properties = self._rsv_obj.properties
        #
        kwargs['variants'] = self._rsv_properties.value
        super(AbsRsvObjSession, self).__init__(
            *args, **kwargs
        )
    @property
    def rsv_obj(self):
        return self._rsv_obj
    @property
    def rsv_properties(self):
        return self._rsv_properties


class AbsRsvUnitDef(object):
    def _set_rsv_unit_def_init_(self, rsv_obj, configure):
        keyword = configure.get('resolver.rsv_unit.keyword')
        self._rsv_unit_version = configure.get('resolver.rsv_unit.version')
        self._rsv_unit = None
        if keyword:
            variants = configure.get('variants')
            keyword = keyword.format(**variants)
            self._rsv_unit = rsv_obj.get_rsv_unit(
                keyword=keyword
            )
    @property
    def rsv_unit(self):
        return self._rsv_unit
    @property
    def rsv_unit_version(self):
        return self._rsv_unit_version


class AbsRsvObjActionDef(object):
    def _set_rsv_obj_action_def_init_(self, configure):
        self._gui_group_name = configure.get(
            'option.gui.group_name'
        )
    @property
    def gui_group_name(self):
        return self._gui_group_name


class AbsRsvEntitySession(
    AbsRsvObjSession,
    AbsRsvObjActionDef
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvEntitySession, self).__init__(*args, **kwargs)
        #
        if self.get_is_loadable():
            self._set_rsv_obj_action_def_init_(self._configure)


class AbsRsvTaskSession(
    AbsRsvObjSession,
    AbsRsvObjActionDef
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvTaskSession, self).__init__(*args, **kwargs)
        #
        if self.get_is_loadable():
            self._set_rsv_obj_action_def_init_(self._configure)


class AbsRsvUnitActionSession(
    AbsRsvObjSession,
    AbsRsvUnitDef,
    AbsRsvObjActionDef
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvUnitActionSession, self).__init__(*args, **kwargs)
        #
        rsv_obj = args[0]
        if self.get_is_loadable():
            self._set_rsv_unit_def_init_(rsv_obj, self._configure)
            self._set_rsv_obj_action_def_init_(self._configure)

    def get_is_executable(self):
        if self.rsv_unit is not None:
            result = self.rsv_unit.get_result(
                version=self.rsv_unit_version
            )
            if result:
                return True
            return False
        return False


class AbsRsvPanelSession(AbsSession):
    RSV_PANEL_CLASS = None
    def __init__(self, *args, **kwargs):
        super(AbsRsvPanelSession, self).__init__(*args, **kwargs)

    def set_execute(self):
        if self.application in [
            self.Application.Python
        ]:
            import sys
            #
            from PySide2 import QtWidgets
            #
            app = QtWidgets.QApplication(sys.argv)
            #
            w = self.RSV_PANEL_CLASS(
                configure=self._configure
            )
            w.set_window_show()
            #
            sys.exit(app.exec_())
        #
        elif self.application in [
            self.Application.Maya,
            self.Application.Houdini,
            self.Application.Katana,
        ]:
            w = self.RSV_PANEL_CLASS(
                configure=self._configure
            )
            w.set_window_show()
