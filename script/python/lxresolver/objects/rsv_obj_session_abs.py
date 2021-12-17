# coding:utf-8
import os

import inspect

from lxbasic import bsc_configure, bsc_core

import lxbasic.objects as bsc_objects

import lxshotgun.objects as stg_objects

from lxutil import utl_core


class AbsSession(object):
    Platform = bsc_configure.Platform
    Application = bsc_configure.Application
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
        self._platform = bsc_core.SystemMtd.get_platform()
        self._application = bsc_core.SystemMtd.get_application()
        self._system = bsc_core.SystemMtd.get_current()
        self._system_includes = bsc_core.SystemMtd.get_system_includes(
            self._configure.get(
                'option.systems'
            ) or []
        )
        self._variants['application'] = self._application
        #
        self._hook_python_file = None
        self._hook_yaml_file = None
    @property
    def configure(self):
        return self._configure
    @property
    def gui_configure(self):
        return self._configure.get_content('option.gui')
    #
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
    # gui
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
    @staticmethod
    def _set_file_execute_(file_path, kwargs):
        # use for python 3
        # with open(file_path, 'r') as f:
        #     exec (f.read())
        #
        # use for python 2
        kwargs['__name__'] = '__main__'
        execfile(file_path, kwargs)

    def get_is_system_matched(self, system_key):
        return self.system in bsc_core.SystemMtd.get_system_includes([system_key])

    def set_execute_fnc(self, fnc):
        pass

    def set_hook_python_file(self, file_path):
        self._hook_python_file = file_path

    def get_hook_python_file(self):
        return self._hook_python_file

    def set_hook_yaml_file(self, file_path):
        self._hook_yaml_file = file_path

    def get_hook_yaml_file(self):
        return self._hook_yaml_file

    def set_hook_python_file_open(self):
        cmd = 'rez-env sublime_text -- sublime_text "{}"'.format(
            self._hook_python_file
        )
        bsc_core.SubProcessMtd.set_run(cmd)

    def set_hook_yaml_file_open(self):
        cmd = 'rez-env sublime_text -- sublime_text "{}"'.format(
            self._hook_yaml_file
        )
        bsc_core.SubProcessMtd.set_run(cmd)


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

    def get_obj_gui(self):
        return self._rsv_obj.get_gui_attribute('gui_obj')


class AbsShotgunDef(object):
    def _set_shotgun_def_(self):
        pass

    def get_shotgun_connector(self):
        return stg_objects.StgConnector()
    shotgun_connector = property(get_shotgun_connector)


class AbsRsvUnitDef(object):
    def _set_rsv_unit_def_init_(self, rsv_obj, configure):
        keyword = configure.get('resolver.rsv_unit.keyword')
        self._rsv_unit_version = configure.get('resolver.rsv_unit.version')
        self._rsv_unit_extend_variants = configure.get('resolver.rsv_unit.extend_variants')
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
    @property
    def rsv_unit_extend_variants(self):
        return self._rsv_unit_extend_variants


class AbsRsvObjActionDef(object):
    def _set_rsv_obj_action_def_init_(self, configure):
        self._gui_group_name = configure.get(
            'option.gui.group_name'
        )
    @property
    def gui_group_name(self):
        return self._gui_group_name


class AbsRsvObjActionSession(
    AbsRsvObjSession,
    AbsRsvObjActionDef,
    AbsShotgunDef
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvObjActionSession, self).__init__(*args, **kwargs)
        #
        if self.get_is_loadable():
            self._set_rsv_obj_action_def_init_(self._configure)
            self._set_shotgun_def_()


class AbsRsvUnitActionSession(
    AbsRsvObjSession,
    AbsRsvUnitDef,
    AbsRsvObjActionDef,
    AbsShotgunDef
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvUnitActionSession, self).__init__(*args, **kwargs)
        #
        rsv_obj = args[0]
        if self.get_is_loadable():
            self._set_rsv_unit_def_init_(rsv_obj, self._configure)
            self._set_rsv_obj_action_def_init_(self._configure)
            self._set_shotgun_def_()

    def get_is_executable(self):
        if self.rsv_unit is not None:
            result = self.rsv_unit.get_result(
                version=self.rsv_unit_version,
                extend_variants=self.rsv_unit_extend_variants
            )
            if result:
                return True
            return False
        return False


class AbsToolPanelSession(AbsSession):
    def __init__(self, *args, **kwargs):
        super(AbsToolPanelSession, self).__init__(*args, **kwargs)


class AbsKitPanelSession(AbsSession):
    def __init__(self, *args, **kwargs):
        super(AbsKitPanelSession, self).__init__(*args, **kwargs)
