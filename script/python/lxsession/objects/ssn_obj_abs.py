# coding:utf-8
import collections

from lxbasic import bsc_configure, bsc_core

import lxbasic.objects as bsc_objects

import lxresolver.commands as rsv_commands

from lxutil import utl_core

import lxshotgun.objects as stg_objects


class AbsSsnGuiDef(object):
    @property
    def configure(self):
        raise NotImplementedError()

    def _set_gui_def_init_(self):
        self._gui_configure = self.configure.get_content(
            'option.gui'
        )

    def get_gui_configure(self):
        return self._gui_configure
    gui_configure = property(get_gui_configure)
    @property
    def gui_group_name(self):
        return self._gui_configure.get(
            'group_name'
        )
    @property
    def gui_name(self):
        return self._gui_configure.get(
            'name'
        )
    @property
    def gui_icon_name(self):
        return self._gui_configure.get(
            'icon_name'
        )


class AbsSsnObj(
    AbsSsnGuiDef
):
    Platform = bsc_configure.Platform
    Application = bsc_configure.Application
    def __init__(self, *args, **kwargs):
        if 'type' in kwargs:
            self._type = kwargs['type']
        else:
            self._type = None
        #
        if 'name' in kwargs:
            self._name = kwargs['name']
        else:
            self._name = None
        #
        if 'hook' in kwargs:
            self._hook = kwargs['hook']
        else:
            self._hook = None
        #
        if 'configure' in kwargs:
            self._configure = kwargs['configure']
        else:
            raise KeyError()
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
        self._user = bsc_core.SystemMtd.get_user_name()
        self._platform = bsc_core.SystemMtd.get_platform()
        self._application = bsc_core.SystemMtd.get_application()
        self._system = bsc_core.SystemMtd.get_current()
        self._system_includes = bsc_core.SystemMtd.get_system_includes(
            self._configure.get(
                'option.systems'
            ) or []
        )
        self._variants['user'] = self._user
        self._variants['platform'] = self._platform
        self._variants['application'] = self._application
        #
        self._hook_python_file = None
        self._hook_yaml_file = None

        self._set_gui_def_init_()

    def get_type(self):
        return self._type
    type = property(get_type)

    def get_name(self):
        return self._name
    name = property(get_name)

    def get_group(self):
        pass

    def get_configure(self):
        return self._configure
    configure = property(get_configure)
    @property
    def utl_gui_configure(self):
        return self._configure.get_content('option.gui')
    #
    def get_platform(self):
        return self._platform
    platform = property(get_platform)

    def get_application(self):
        return self._application
    application = property(get_application)

    def get_user(self):
        return self._user
    @property
    def system(self):
        return self._system
    @property
    def system_includes(self):
        return self._system_includes
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

    def set_reload(self):
        self._configure.set_reload()
        self._configure.set_flatten()
    @classmethod
    def set_cmd_run(cls, cmd):
        utl_core.HookMtd.set_cmd_run(
            cmd
        )

    def get_engine(self):
        return self._configure.get(
            'hook_option.engine'
        )

    def get_hook(self):
        return self._hook

    def get_rez_extend_packages(self):
        return self._configure.get(
            'hook_option.rez.extend_packages'
        ) or []

    def __str__(self):
        return self._configure.get_str_as_yaml_style()


class AbsSsnRsvObj(AbsSsnObj):
    def __init__(self, *args, **kwargs):
        self._rsv_obj = args[0]
        self._rsv_properties = self._rsv_obj.properties
        #
        kwargs['variants'] = self._rsv_properties.value
        super(AbsSsnRsvObj, self).__init__(
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


class AbsSsnShotgunDef(object):
    def _set_shotgun_def_init_(self):
        pass

    def get_shotgun_connector(self):
        return stg_objects.StgConnector()
    shotgun_connector = property(get_shotgun_connector)


class AbsSsnRsvUnitDef(object):
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


class AbsSsnRsvObjAction(
    AbsSsnRsvObj,
    AbsSsnShotgunDef
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnRsvObjAction, self).__init__(*args, **kwargs)
        #
        if self.get_is_loadable():
            self._set_shotgun_def_init_()


class AbsSsnRsvUnitAction(
    AbsSsnRsvObj,
    AbsSsnRsvUnitDef,
    AbsSsnShotgunDef
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnRsvUnitAction, self).__init__(*args, **kwargs)
        #
        rsv_obj = args[0]
        if self.get_is_loadable():
            self._set_rsv_unit_def_init_(rsv_obj, self._configure)
            self._set_shotgun_def_init_()

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


class AbsSsnRsvOptionExecuteDef(object):
    EXECUTOR = None
    @classmethod
    def _get_rsv_task_version_(cls, rsv_task_properties):
        if rsv_task_properties.get('shot'):
            return '{project}.{shot}.{step}.{task}.{version}'.format(**rsv_task_properties.value)
        elif rsv_task_properties.get('asset'):
            return '{project}.{asset}.{step}.{task}.{version}'.format(**rsv_task_properties.value)
        else:
            raise TypeError()
    #
    def _set_hook_execute_def_init_(self, ddl_configure):
        self._ddl_configure = ddl_configure
        self._ddl_job_id = None

    def get_ddl_configure(self):
        return self._ddl_configure

    def set_ddl_dependent_job_ids_find(self, *args, **kwargs):
        pass

    def get_ddl_dependent_unique_id(self):
        pass

    def get_executor(self):
        return self.EXECUTOR(
            self
        )

    def set_execute_by_deadline(self):
        executor = self.get_executor()
        executor.set_run_with_deadline()

    def set_ddl_job_id(self, ddl_job_id):
        self._ddl_job_id = ddl_job_id

    def get_ddl_job_id(self):
        return self._ddl_job_id

    def set_execute_by_shell(self):
        executor = self.get_executor()
        executor.set_run_with_shell()


class AbsToolPanelSession(AbsSsnObj):
    def __init__(self, *args, **kwargs):
        super(AbsToolPanelSession, self).__init__(*args, **kwargs)


class AbsSsnOptionGui(
    AbsSsnObj,
    AbsSsnRsvOptionExecuteDef
):
    def __init__(self, *args, **kwargs):
        if 'option' in kwargs:
            self._option_opt = bsc_core.KeywordArgumentsOpt(
                kwargs.pop('option')
            )
        else:
            self._option_opt = None
        #
        super(AbsSsnOptionGui, self).__init__(*args, **kwargs)
        #
        if self._option_opt is not None:
            self.__set_option_completion_()
            #
            self._set_hook_execute_def_init_(
                self._configure.get_content('hook_option.deadline')
            )

    def __set_option_completion_(self):
        option_opt = self.get_option_opt()
        #
        hook_engine = self._configure.get('hook_option.engine')
        option_opt.set('hook_engine', hook_engine)

    def get_option_opt(self):
        return self._option_opt
    option_opt = property(get_option_opt)

    def get_option(self):
        return self._option_opt.to_string()
    option = property(get_option)


class AbsSsnGui(
    AbsSsnObj
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnGui, self).__init__(*args, **kwargs)


class AbsSsnOptionDef(object):
    def _set_option_def_init_(self, option):
        self._option_opt = bsc_core.KeywordArgumentsOpt(
            option
        )

    def get_option_opt(self):
        return self._option_opt
    option_opt = property(get_option_opt)

    def get_option(self):
        return self._option_opt.to_string()
    option = property(get_option)


class AbsSsnOptionAction(
    AbsSsnObj,
    AbsSsnOptionDef
):
    def __init__(self, *args, **kwargs):
        self._set_option_def_init_(kwargs.pop('option'))
        super(AbsSsnOptionAction, self).__init__(*args, **kwargs)


class AbsSsnShellExecuteDef(object):
    EXECUTOR = None
    @property
    def configure(self):
        raise NotImplementedError()
    @property
    def option_opt(self):
        raise NotImplementedError()

    def _set_shell_execute_def_init_(self, configure):
        self.__set_execute_option_completion_()

    def get_executor(self):
        return self.EXECUTOR(
            self
        )

    def set_execute_by_shell(self):
        executor = self.get_executor()
        executor.set_run_with_shell()

    def __set_execute_option_completion_(self):
        hook_engine = self.configure.get('hook_option.engine')
        self.option_opt.set('hook_engine', hook_engine)
        #
        rez_extend_packages = self.configure.get('hook_option.rez.extend_packages') or []
        if rez_extend_packages:
            self.option_opt.set('rez_extend_packages', rez_extend_packages)
        #
        rez_add_environs = self.configure.get('hook_option.rez.add_environ') or []


class AbsSsnOptionToolPanel(
    AbsSsnObj,
    AbsSsnOptionDef,
    AbsSsnShellExecuteDef
):
    def __init__(self, *args, **kwargs):
        self._set_option_def_init_(kwargs.pop('option'))
        super(AbsSsnOptionToolPanel, self).__init__(*args, **kwargs)
        #
        self._set_shell_execute_def_init_(self._configure)


# session for deadline job
class AbsOptionMethodSession(
    AbsSsnObj,
    AbsSsnOptionDef,
    AbsSsnRsvOptionExecuteDef
):
    def __init__(self, *args, **kwargs):
        self._set_option_def_init_(kwargs.pop('option'))
        #
        super(AbsOptionMethodSession, self).__init__(*args, **kwargs)
        #
        self.__set_option_completion_()
        self.__set_script_option_completion_()
        #
        self._set_hook_execute_def_init_(
            self._configure.get_content('hook_option.deadline')
        )

    def __set_option_completion_(self):
        option_opt = self.get_option_opt()
        #
        hook_engine = self._configure.get('hook_option.engine')
        option_opt.set('hook_engine', hook_engine)
        #
        rez_extend_packages = self._configure.get('hook_option.rez.extend_packages') or []
        if rez_extend_packages:
            option_opt.set('rez_extend_packages', rez_extend_packages)

    def __set_script_option_completion_(self):
        option_opt = self.get_option_opt()
        #
        inherit_keys = option_opt.get('inherit_keys')
        script_option = self._configure.get('hook_option.script') or {}
        for k, v in script_option.items():
            if option_opt.get_key_is_exists(k) is False:
                if isinstance(v, dict):
                    pass
                else:
                    option_opt.set(k, v)

    def get_option_opt(self):
        return self._option_opt
    option_opt = property(get_option_opt)

    def get_option(self):
        return self._option_opt.to_string()
    option = property(get_option)

    def set_ddl_dependent_job_ids_find(self, *args, **kwargs):
        return


class AbsRsvDef(object):
    def _set_rsv_def_init_(self):
        self._resolver = rsv_commands.get_resolver()

    def get_resolver(self):
        return self._resolver
    resolver = property(get_resolver)


# session for rsv task deadline job
class AbsOptionRsvTaskMethodSession(
    AbsOptionMethodSession,
    AbsRsvDef
):
    def __init__(self, *args, **kwargs):
        super(AbsOptionRsvTaskMethodSession, self).__init__(*args, **kwargs)
        self._set_rsv_def_init_()
        #
        self.__set_system_option_completion_()
        #
        self._rsv_task_properties = None
        self._rsv_task = None
        #
        option_opt = self.get_option_opt()
        #
        self._batch_file_path = option_opt.pop('batch_file')
        self._file_path = option_opt.get('file')
        if self._batch_file_path:
            self._rsv_task_properties = self.resolver.get_task_properties_by_any_scene_file_path(
                self._batch_file_path
            )
            self._rsv_task = self.resolver.get_rsv_task_by_any_file_path(
                self._batch_file_path
            )
        else:
            if self._file_path:
                self._rsv_task_properties = self.resolver.get_task_properties_by_any_scene_file_path(
                    self._file_path
                )
                self._rsv_task = self.resolver.get_rsv_task_by_any_file_path(
                    self._file_path
                )
        #
        self.__set_rsv_task_option_completion_()
        #
        # print self.get_option_opt()
        # print self.get_option()

    def __set_system_option_completion_(self):
        option_opt = self.get_option_opt()
        for i_key in ['user', 'time_tag']:
            if option_opt.get(i_key) is None:
                option_opt.set(i_key, bsc_core.SystemMtd.get(i_key))

    def __set_rsv_task_option_completion_(self):
        option_opt = self.get_option_opt()
        for i_key in ['project']:
            option_opt.set(
                i_key, self._rsv_task_properties.get(i_key)
            )

    def get_batch_key(self):
        option_opt = self.get_option_opt()
        return bsc_core.SessionYamlMtd.get_key(
            version=self.get_rsv_version_name(),
            time_tag=option_opt.get('time_tag'),
        )

    def get_batch_file_path(self):
        option_opt = self.get_option_opt()
        file_path = bsc_core.SessionYamlMtd.get_file_path(
            version=self.get_rsv_version_name(),
            time_tag=option_opt.get('time_tag'),
        )
        if bsc_core.StoragePathMtd.get_path_is_exists(file_path) is False:
            raw = dict(
                version=self.get_rsv_version_name(),
                time_tag=option_opt.get('time_tag'),
            )
            utl_core.File.set_write(file_path, raw)
        return file_path

    def set_ddl_result_update(self, hook_option, ddl_job_id):
        hook_option_opt = bsc_core.KeywordArgumentsOpt(
            hook_option
        )
        option_hook_key = hook_option_opt.get('option_hook_key')
        f = self.get_batch_file_path()
        c = bsc_objects.Configure(value=f)
        #
        keys = [option_hook_key]
        option_hook_key_extend = hook_option_opt.get('option_hook_key_extend', as_array=True)
        if option_hook_key_extend:
            keys.extend(option_hook_key_extend)
        #
        hook_dependencies = hook_option_opt.get('dependencies')
        #
        key = '/'.join(keys)
        c.set(
            'deadline.{}.job_id'.format(key), ddl_job_id
        )
        c.set(
            'deadline.{}.option'.format(key), hook_option
        )
        c.set_save_to(
            f
        )

    def set_ddl_job_id_find(self, hook_option):
        hook_option_opt = bsc_core.KeywordArgumentsOpt(
            hook_option
        )
        option_hook_key = hook_option_opt.get('option_hook_key')
        f = self.get_batch_file_path()
        c = bsc_objects.Configure(value=f)
        #
        keys = [option_hook_key]
        option_hook_key_extend = hook_option_opt.get('option_hook_key_extend', as_array=True)
        if option_hook_key_extend:
            keys.extend(option_hook_key_extend)
        #
        key = '/'.join(keys)
        #
        return c.get(
            'deadline.{}.job_id'.format(key)
        )
    @classmethod
    def get_dependencies(cls, hook_option):
        lis = []
        hook_option_opt = bsc_core.KeywordArgumentsOpt(
            hook_option
        )
        main_key = hook_option_opt.get('option_hook_key')
        #
        dependent_option_hook_keys = hook_option_opt.get(
            'dependencies', as_array=True
        ) or []
        for i_key in dependent_option_hook_keys:
            i_option_hook_key = bsc_core.SessionMtd.get_hook_abs_path(
                main_key, i_key
            )
            lis.append(i_option_hook_key)
        return lis

    def set_ddl_dependent_job_ids_find(self, hook_option):
        lis = []
        hook_option_opt = bsc_core.KeywordArgumentsOpt(
            hook_option
        )
        main_key = hook_option_opt.get('option_hook_key')
        f = self.get_batch_file_path()
        c = bsc_objects.Configure(value=f)
        #
        dependent_option_hook_keys = hook_option_opt.get(
            'dependencies', as_array=True
        ) or []
        for i_key in dependent_option_hook_keys:
            i_option_hook_key = bsc_core.SessionMtd.get_hook_abs_path(
                main_key, i_key
            )
            i_ddl_job_id = c.get(
                'deadline.{}.job_id'.format(i_option_hook_key)
            )
            if i_ddl_job_id:
                lis.append(i_ddl_job_id)
        return lis

    def get_rsv_task_properties(self):
        return self._rsv_task_properties

    def get_rsv_task(self):
        return self._rsv_task

    def get_rsv_version_name(self):
        return self._get_rsv_task_version_(
            self.get_rsv_task_properties()
        )

    def get_ddl_dependent_unique_id(self):
        option_opt = self.get_option_opt()
        return bsc_core.SessionYamlMtd.get_key(
            version=self.get_rsv_version_name(),
            # user=option_opt.get('user'),
            time_tag=option_opt.get('time_tag'),
        )

    def get_group(self):
        return self.get_rsv_version_name()

    def get_ddl_name(self):
        return self.get_name()

    def get_executor(self):
        return self.EXECUTOR(
            self
        )


class AbsOptionRsvTaskBatcherSession(
    AbsOptionRsvTaskMethodSession
):
    def __init__(self, *args, **kwargs):
        super(AbsOptionRsvTaskBatcherSession, self).__init__(*args, **kwargs)


class AbsApplicationSession(AbsSsnObj):
    def __init__(self, *args, **kwargs):
        super(AbsApplicationSession, self).__init__(*args, **kwargs)
