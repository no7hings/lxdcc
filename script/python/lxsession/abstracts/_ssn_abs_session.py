# coding:utf-8
import fnmatch

import os

import subprocess

from lxbasic import bsc_configure, bsc_core

import lxbasic.objects as bsc_objects

import lxbasic.extra.methods as bsc_etr_methods

import lxresolver.commands as rsv_commands

from lxsession import ssn_core

import lxshotgun.objects as stg_objects

import lxdatabase.objects as dtb_objects


class AbsSsnConfigureBaseDef(object):
    @property
    def configure(self):
        raise NotImplementedError()

    def _init_configure_base_def_(self):
        self._basic_configure = self.configure.get_content(
            'option'
        )
        self._gui_configure = self.configure.get_content(
            'option.gui'
        )

    def get_basic_configure(self):
        return self._basic_configure
    basic_configure = property(get_basic_configure)

    def get_gui_configure(self):
        return self._gui_configure
    gui_configure = property(get_gui_configure)

    @property
    def gui_group_name(self):
        return self._gui_configure.get(
            'group_name'
        )

    def get_gui_name(self):
        return self._gui_configure.get(
            'name'
        )
    gui_name = property(get_gui_name)

    @property
    def gui_icon_name(self):
        return self._gui_configure.get(
            'icon_name'
        )

    def get_is_visible(self):
        return True


class AbsSsnRezDef(object):
    def _set_rez_def_init_(self):
        # self._rez_beta = bsc_core.EnvironMtd.get('REZ_BETA')
        pass
    @classmethod
    def get_is_td_enable(cls):
        return bsc_core.EnvExtraMtd.get_is_td_enable()
    @classmethod
    def get_is_beta_enable(cls):
        return bsc_core.EnvExtraMtd.get_is_beta_enable()


class AbsSsnObj(
    AbsSsnRezDef,
    AbsSsnConfigureBaseDef,
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
        self._host = bsc_core.SystemMtd.get_host()
        self._platform = bsc_core.SystemMtd.get_platform()
        self._application = bsc_core.SystemMtd.get_application()
        self._system = bsc_core.SystemMtd.get_current()
        self._system_includes = bsc_core.SystemMtd.get_system_includes(
            self._configure.get(
                'option.systems'
            ) or []
        )
        self._variants['user'] = self._user
        self._variants['host'] = self._host
        self._variants['platform'] = self._platform
        self._variants['application'] = self._application
        #
        self._hook_yaml_file_path = None
        self._hook_python_file_path = None
        self._hook_shell_file_path = None

        self._set_rez_def_init_()
        self._init_configure_base_def_()

    def get_type(self):
        return self._type
    type = property(get_type)

    def get_name(self):
        if self._name:
            return self._name
        return self._hook
    name = property(get_name)

    def get_hook(self):
        return self._hook
    hook = property(get_hook)

    def get_group(self):
        return self.get_type()
    group = property(get_group)

    def get_configure(self):
        return self._configure
    configure = property(get_configure)

    def reload_configure(self):
        self._configure.set_reload()
    #
    def get_platform(self):
        return self._platform
    platform = property(get_platform)

    def get_application(self):
        return self._application
    application = property(get_application)

    def get_user(self):
        return self._user
    user = property(get_user)
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
                self.pre_run_fnc()
                self.execute()
                self.post_run_fnc()

    def pre_run_fnc(self):
        pass

    def execute(self):
        if self._hook_python_file_path:
            self.execute_python_file_fnc(
                self._hook_python_file_path, session=self
            )

    def post_run_fnc(self):
        pass

    def execute_use_debug(self):
        try:
            self.set_run()
        except Exception:
            from lxutil import utl_core
            utl_core.ExceptionCatcher.set_create()
            raise
    @staticmethod
    def execute_python_file_fnc(file_path, **kwargs):
        # use for python 3
        # with open(file_path, 'r') as f:
        #     exec (f.read())
        # use for python 2
        bsc_core.LogMtd.trace_method_result(
            'option-hook', 'start for : "{}"'.format(
                file_path
            )
        )
        kwargs['__name__'] = '__main__'
        execfile(file_path, kwargs)
        bsc_core.LogMtd.trace_method_result(
            'option-hook', 'complete for: "{}"'.format(
                file_path
            )
        )
    @staticmethod
    def execute_python_command(cmd, **kwargs):
        # noinspection PyUnusedLocal
        session = kwargs['session']
        exec cmd
    @staticmethod
    def execute_shell_file_fnc(file_path, **kwargs):
        bsc_core.LogMtd.trace_method_result(
            'option-hook', 'start for : "{}"'.format(
                file_path
            )
        )
        session = kwargs['session']
        if bsc_core.PlatformMtd.get_is_linux():
            # cmds = ['bash', '-l', '-c', file_path]
            cmds = ['gnome-terminal', '-t', '"{}"'.format(session.gui_configure.get('name')), '--', 'bash', '-l', '"{}"'.format(file_path)]
            # subprocess.Popen(
            #     cmds,
            #     shell=False,
            #     # env=dict(),
            # )
            bsc_core.SubProcessMtd.execute_as_block(
                ' '.join(cmds)
            )
        elif bsc_core.PlatformMtd.get_is_windows():
            cmds = ['start', 'cmd',  '/k', file_path]
            subprocess.Popen(
                cmds,
                shell=True,
                # env=dict()
            )
        bsc_core.LogMtd.trace_method_result(
            'option-hook', 'complete for: "{}"'.format(
                file_path
            )
        )
    @classmethod
    def execute_shell_command(cls, cmd, **kwargs):
        session = kwargs['session']
        if bsc_core.PlatformMtd.get_is_linux():
            # cmds = ['bash', '-l', '-c', file_path]
            cmds = ['gnome-terminal', '-t', session.gui_configure.get('name'), '--', 'bash', '-l', '-c', cmd]
            subprocess.Popen(cmds, shell=False)
        elif bsc_core.PlatformMtd.get_is_windows():
            cmds = ['start', 'cmd', '/k', cmd]
            subprocess.Popen(cmds, shell=True)

    def get_is_system_matched(self, system_key):
        return self.system in bsc_core.SystemMtd.get_system_includes([system_key])
    @classmethod
    def _get_choice_scheme_matched_(cls, choice_scheme, choice_scheme_includes):
        for i_choice_scheme in choice_scheme_includes:
            if fnmatch.filter(
                [choice_scheme], i_choice_scheme
            ):
                return True
        return False

    def set_execute_fnc(self, fnc):
        pass

    def set_configure_yaml_file(self, file_path):
        self._hook_yaml_file_path = file_path

    def get_configure_yaml_file(self):
        return self._hook_yaml_file_path

    def set_python_script_file(self, file_path):
        self._hook_python_file_path = file_path

    def get_python_script_file(self):
        return self._hook_python_file_path

    def get_python_script(self):
        if self._hook_python_file_path:
            return bsc_core.StgFileOpt(self._hook_python_file_path).set_read()

    def set_shell_script_file(self, file_path):
        self._hook_shell_file_path = file_path

    def get_shell_script_file(self):
        return self._hook_shell_file_path

    def get_shell_script(self):
        pass

    def open_configure_file(self):
        if self._hook_yaml_file_path:
            bsc_etr_methods.EtrBase.open_ide(
                self._hook_yaml_file_path
            )

    def open_configure_directory(self):
        if self._hook_yaml_file_path:
            bsc_core.StgFileOpt(self._hook_yaml_file_path).set_open_in_system()

    def open_python_script_file(self):
        if self._hook_python_file_path:
            bsc_etr_methods.EtrBase.open_ide(
                self._hook_python_file_path
            )

    def open_execute_file(self):
        pass

    def set_reload(self):
        self._configure.set_reload()
        self._configure.set_flatten()
    @classmethod
    def set_cmd_run(cls, cmd):
        ssn_core.SsnHookMtd.set_cmd_run(
            cmd
        )

    def get_engine(self):
        return self._configure.get(
            'hook_option.engine'
        )

    def get_packages_extend(self):
        return self._configure.get(
            'hook_option.rez.extend_packages'
        ) or []

    def get_environs_extend(self):
        return self._configure.get(
            'hook_option.rez.extend_environs'
        ) or []

    def get_is_match_condition(self, match_dict):
        condition_string = self._configure.get(
            'rsv-match-condition'
        )
        if condition_string:
            return self._match_fnc_(condition_string, match_dict)
        return True
    @classmethod
    def _match_fnc_(cls, condition_string, match_dict):
        if condition_string:
            for i in condition_string.split('&'):
                i_key, i_condition = i.split('=')
                if i_key not in match_dict:
                    continue
                #
                i_input = match_dict[i_key]
                #
                if not i_input:
                    return False
                #
                if '+' in i_condition:
                    i_values = i_condition.split('+')
                    if i_input not in i_values:
                        return False
                else:
                    if i_condition != i_input:
                        return False
        return True

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
        self._rsv_keyword = configure.get('resolver.rsv_unit.keyword')
        #
        self._rsv_unit_version = configure.get('resolver.rsv_unit.version')
        self._rsv_unit_extend_variants = configure.get('resolver.rsv_unit.extend_variants') or {}
        self._rsv_unit = None
        if self._rsv_keyword:
            variants = configure.get('variants')
            self._rsv_keyword = self._rsv_keyword.format(**variants)
            self._rsv_unit = rsv_obj.get_rsv_unit(
                keyword=self._rsv_keyword
            )
            self._rsv_unit_extend_variants['artist'] = bsc_core.SystemMtd.get_user_name()
    @property
    def rsv_task(self):
        return self._rsv_unit.get_rsv_task()
    @property
    def rsv_step(self):
        return self._rsv_unit.get_rsv_setp()
    @property
    def rsv_entity(self):
        return self._rsv_unit.get_rsv_resource()
    @property
    def rsv_unit(self):
        return self._rsv_unit
    @property
    def rsv_keyword(self):
        return self._rsv_keyword
    @property
    def rsv_unit_version(self):
        return self._rsv_unit_version
    @property
    def rsv_unit_extend_variants(self):
        return self._rsv_unit_extend_variants

    def set_view_gui(self, prx_widget):
        self._view_gui = prx_widget

    def get_view_gui(self):
        return self._view_gui


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

    def get_is_visible(self):
        if self.rsv_unit is not None:
            step_includes = self.configure.get(
                'resolver.step_includes'
            )
            if step_includes:
                step = self.rsv_unit.get('step')
                if step not in step_includes:
                    return False
        return True

    def get_is_executable(self):
        if self.rsv_unit is not None:
            step_includes = self.configure.get(
                'resolver.step_includes'
            )
            if step_includes:
                step = self.rsv_unit.get('step')
                if step not in step_includes:
                    return False
            #
            result = self.rsv_unit.get_result(
                version=self.rsv_unit_version,
                extend_variants=self.rsv_unit_extend_variants
            )
            if result:
                return True
            return False
        return False


class AbsSsnOptionExecuteDef(object):
    EXECUTOR = None
    @classmethod
    def _get_rsv_task_version_(cls, rsv_scene_properties):
        if rsv_scene_properties.get('shot'):
            return '{project}.{shot}.{step}.{task}.{version}'.format(**rsv_scene_properties.value)
        elif rsv_scene_properties.get('asset'):
            return '{project}.{asset}.{step}.{task}.{version}'.format(**rsv_scene_properties.value)
        else:
            raise TypeError()
    #
    def _set_option_execute_def_init_(self, ddl_configure):
        self._ddl_configure = ddl_configure
        self._ddl_job_id = None

    def get_ddl_configure(self):
        return self._ddl_configure

    def set_ddl_dependent_job_ids_find(self, *args, **kwargs):
        pass

    def get_executor(self):
        return self.EXECUTOR(
            self
        )

    def set_execute_by_deadline(self):
        executor = self.get_executor()
        return executor.execute_with_deadline()

    def set_ddl_job_id(self, ddl_job_id):
        self._ddl_job_id = ddl_job_id

    def get_ddl_job_id(self):
        return self._ddl_job_id

    def set_execute_by_shell(self, block=False):
        executor = self.get_executor()
        executor.set_run_with_shell(block)

    def get_shell_script_command(self):
        return self.get_executor().get_shell_command()


class AbsToolPanelSession(AbsSsnObj):
    def __init__(self, *args, **kwargs):
        super(AbsToolPanelSession, self).__init__(*args, **kwargs)


class AbsSsnOptionGui(
    AbsSsnObj,
    AbsSsnOptionExecuteDef
):
    def __init__(self, *args, **kwargs):
        if 'option' in kwargs:
            self._option_opt = bsc_core.ArgDictStringOpt(
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
            self._set_option_execute_def_init_(
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


class AbsSsnRsvGui(
    AbsSsnObj,
    AbsSsnShotgunDef,
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnRsvGui, self).__init__(*args, **kwargs)
        self._set_shotgun_def_init_()


class AbsSsnOptionObj(AbsSsnObj):
    def __init__(self, *args, **kwargs):
        super(AbsSsnOptionObj, self).__init__(*args, **kwargs)
        self._set_option_def_init_(kwargs['option'])

    def _set_option_def_init_(self, option):
        self._option_opt = bsc_core.ArgDictStringOpt(
            option
        )
        self.__set_option_completion_by_script_()

    def __set_option_completion_by_script_(self):
        option_opt = self.get_option_opt()
        #
        # inherit_keys = option_opt.get('inherit_keys')
        script_dict = self.configure.get('hook_option.script') or {}
        for k, v in script_dict.items():
            if option_opt.get_key_is_exists(k) is False:
                if isinstance(v, dict):
                    pass
                else:
                    option_opt.set(
                        k, v
                    )

    def get_option_opt(self):
        return self._option_opt
    option_opt = property(get_option_opt)

    def get_option(self):
        return self._option_opt.to_string()
    option = property(get_option)

    def get_extra_hook_options(self):
        lis = []
        script_dict = self.configure.get('hook_option.script') or {}
        extra_dict = self.configure.get('hook_option.extra') or {}
        for k, v in extra_dict.items():
            i_script_dict = v['script']
            for i_k, i_v in script_dict.items():
                if i_k not in i_script_dict:
                    i_script_dict[i_k] = i_v
            #
            i_hook_option_opt = bsc_core.ArgDictStringOpt(i_script_dict)
            i_hook_option_opt.set(
                'option_hook_key', self.option_opt.get('option_hook_key')
            )
            lis.append(
                i_hook_option_opt.to_string()
            )
        return lis

    def __str__(self):
        return '{}(type="{}", hook={}, option="{}")'.format(
            self.__class__.__name__,
            self._type,
            self.hook,
            self.option
        )


class AbsSsnOptionAction(
    AbsSsnOptionObj
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnOptionAction, self).__init__(*args, **kwargs)


class AbsSsnDatabaseOptionAction(
    AbsSsnOptionObj
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnDatabaseOptionAction, self).__init__(*args, **kwargs)

    def get_database_opt(self):
        return dtb_objects.DtbResourceLibraryOpt(
            self.option_opt.get('database_configure'),
            self.option_opt.get('database_configure_extend')
        )
    database_opt = property(get_database_opt)

    def get_window(self):
        from lxutil_gui.qt import utl_gui_qt_core
        return utl_gui_qt_core.get_lx_window_by_unique_id(
            self.option_opt.get('window_unique_id')
        )


class AbsSsnOptionLauncher(
    AbsSsnOptionObj
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnOptionLauncher, self).__init__(*args, **kwargs)


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

    def set_execute_by_shell(self, block=False):
        self.get_executor().set_run_with_shell(block)

    def get_shell_script_command(self):
        return self.get_executor().get_shell_command()

    def __set_execute_option_completion_(self):
        hook_engine = self.configure.get('hook_option.engine')
        self.option_opt.set('hook_engine', hook_engine)
        #
        rez_extend_packages = self.configure.get('hook_option.rez.extend_packages') or []
        if rez_extend_packages:
            self.option_opt.set('rez_extend_packages', rez_extend_packages)
        #
        rez_add_environs = self.configure.get('hook_option.rez.add_environs') or []


class AbsSsnOptionToolPanel(
    AbsSsnOptionObj,
    AbsSsnShellExecuteDef
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnOptionToolPanel, self).__init__(*args, **kwargs)
        #
        self._set_shell_execute_def_init_(self._configure)


class AbsSsnRsvOptionToolPanel(
    AbsSsnOptionObj,
    AbsSsnShotgunDef,
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnRsvOptionToolPanel, self).__init__(*args, **kwargs)
        #
        self._set_shotgun_def_init_()


# session for deadline job
class AbsSsnOptionMethod(
    AbsSsnOptionObj,
    AbsSsnOptionExecuteDef
):
    STD_KEYS = [
        'user',
        'host',
        'time_tag',
    ]
    def __init__(self, *args, **kwargs):
        super(AbsSsnOptionMethod, self).__init__(*args, **kwargs)
        self._set_system_option_completion_()
        self._set_option_completion_()
        #
        self._set_option_execute_def_init_(
            self._configure.get_content('hook_option.deadline')
        )

    def _set_option_completion_(self):
        option_opt = self.get_option_opt()
        #
        hook_engine = self._configure.get('hook_option.engine')
        option_opt.set('hook_engine', hook_engine)
        #
        rez_extend_packages = self._configure.get('hook_option.rez.extend_packages') or []
        if rez_extend_packages:
            option_opt.set('rez_extend_packages', rez_extend_packages)

    def _set_system_option_completion_(self):
        option_opt = self.get_option_opt()
        for i_key in self.STD_KEYS:
            if option_opt.get(i_key) is None:
                option_opt.set(i_key, bsc_core.SystemMtd.get(i_key))

    def get_batch_file_path(self):
        option_opt = self.get_option_opt()

        file_path = ssn_core.SsnHookServerMtd.get_file_path(
            user=option_opt.get('user'),
            time_tag=option_opt.get('time_tag'),
        )
        if bsc_core.StorageMtd.get_is_exists(file_path) is False:
            raw = dict(
                user=option_opt.get('user'),
                time_tag=option_opt.get('time_tag'),
            )
            bsc_core.StgFileOpt(file_path).set_write(raw)
            bsc_core.LogMtd.trace_method_result(
                'hook batch-file write',
                'file="{}"'.format(file_path)
            )
        return file_path

    def set_ddl_dependent_job_ids_find(self, hook_option):
        lis = []
        hook_option_opt = bsc_core.ArgDictStringOpt(
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
            i_option_hook_key = ssn_core.SsnHookFileMtd.get_hook_abs_path(
                main_key, i_key
            )
            i_ddl_job_id = c.get(
                'deadline.{}.job_id'.format(i_option_hook_key)
            )
            if i_ddl_job_id:
                lis.append(i_ddl_job_id)
        return lis

    def set_ddl_job_id_find(self, hook_option):
        hook_option_opt = bsc_core.ArgDictStringOpt(
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

    def set_ddl_result_update(self, hook_option, ddl_job_id):
        hook_option_opt = bsc_core.ArgDictStringOpt(
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
        c.set(
            'deadline.{}.job_id'.format(key), ddl_job_id
        )
        c.set(
            'deadline.{}.option'.format(key), hook_option
        )
        c.set_save_to(
            f
        )

    def get_batch_name(self):
        return


class AbsSsnRsvDef(object):
    def _set_rsv_def_init_(self):
        self._resolver = rsv_commands.get_resolver()

    def get_resolver(self):
        return self._resolver
    resolver = property(get_resolver)


class ValidationChecker(object):
    class CheckStatus(object):
        Error = 'error'
        Warning = 'warning'

    def __init__(self, session):
        self._session = session
        #
        self._check_options = {}
        self._check_results = []

    def set_options(self, options):
        self._check_options = options

    def register_node_result(self, obj_path, description, check_group, check_status='error'):
        self._check_results.append(
            dict(
                type='node',
                node=obj_path,
                elements=[],
                description=description,
                group=check_group,
                status=check_status,
            )
        )

    def register_node_components_result(self, obj_path, elements, description, check_group, check_status='error'):
        self._check_results.append(
            dict(
                type='component',
                node=obj_path,
                elements=elements,
                description=description,
                group=check_group,
                status=check_status,
            )
        )

    def register_node_files_result(self, obj_path, elements, description, check_group, check_status='error'):
        self._check_results.append(
            dict(
                type='file',
                node=obj_path,
                elements=elements,
                description=description,
                group=check_group,
                status=check_status,
            )
        )

    def register_node_directories_result(self, obj_path, elements, description, check_group, check_status='error'):
        self._check_results.append(
            dict(
                type='directory',
                node=obj_path,
                elements=elements,
                description=description,
                group=check_group,
                status=check_status,
            )
        )

    def _get_data_file_path_(self):
        file_path = self._session.option_opt.get('file')
        return bsc_core.StgTmpYamlMtd.get_file_path(
            file_path, 'asset-validator'
        )

    def get_has_history(self):
        pass

    def set_data_restore(self):
        self._check_options = {}
        self._check_results = []

    def set_data_record(self):
        result_file_path = self._get_data_file_path_()
        bsc_core.StgFileOpt(
            result_file_path
        ).set_write(
            dict(
                check_results=self._check_results
            )
        )

    def get_data(self):
        result_file_path = self._get_data_file_path_()
        print result_file_path
        raw = bsc_core.StgFileOpt(
            result_file_path
        ).set_read()
        self._check_results = raw['check_results']
        return raw

    def get_is_passed(self):
        return self.get_summary() != 'error'

    def get_summary(self):
        if self._check_options:
            if self._check_results:
                for i in self._check_results:
                    i_status = i['status']
                    if i_status == 'error':
                        return 'error'
                return 'warning'
            return 'passed'
        return 'ignore'

    def get_info(self):
        return self._get_info_by_results_(
            self.get_summary(), self._check_options, self._check_results
        )
    @classmethod
    def _get_info_by_results_(cls, summary, check_options, check_results):
        list_ = []
        #
        if check_options:
            list_.append(
                'validation check options:\n'
            )
            for k, v in check_options.items():
                list_.append(
                    (
                        '    {}: {}\n'
                     ).format(k, ['off', 'on'][v])
                )
        #
        error_count = 0
        warning_count = 0
        if check_results:
            list_.append('validation check results:\n')
            for seq, i in enumerate(check_results):
                i_d = (
                    '    result {index}:\n'
                    '        node: {node}\n'
                    '        group: {group}\n'
                    '        status: {status}\n'
                    '        description: {description}\n'
                ).format(index=seq+1, **i)
                list_.append(i_d)
                i_elements = i['elements']
                if i_elements:
                    list_.append('        elements:\n')
                    for j_element in i_elements:
                        j_d = (
                            '            {type}: {element}\n'
                        ).format(
                            element=j_element, **i
                        )
                        list_.append(j_d)
                i_status = i['status']
                if i_status == 'error':
                    error_count += 1
                elif i_status == 'warning':
                    warning_count += 1
            #
            list_.insert(
                0,
                (
                    'validation check summary： {} ( {} error and {} warning )\n'
                ).format(summary, error_count, warning_count)
            )
        #
        return ''.join(list_)


# session for rsv project deadline job
class AbsSsnRsvProjectOptionMethod(
    AbsSsnOptionMethod,
    AbsSsnRsvDef
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnRsvProjectOptionMethod, self).__init__(*args, **kwargs)
        self._set_rsv_def_init_()

        self._rsv_project = None
        self._rsv_properties = None
        self._rsv_scene_properties = None

        option_opt = self.get_option_opt()

        self._batch_name = option_opt.get('batch_name')
        self._batch_file_path = option_opt.pop('batch_file')
        self._file_path = option_opt.get('file')

        if self._batch_file_path:
            self._rsv_project = self._resolver.get_rsv_project_by_any_file_path(self._batch_file_path)
            self._rsv_scene_properties = self._resolver.get_rsv_scene_properties_by_any_scene_file_path(
                self._batch_file_path
            )
        else:
            if self._file_path:
                self._rsv_project = self._resolver.get_rsv_project_by_any_file_path(self._file_path)
                self._rsv_scene_properties = self._resolver.get_rsv_scene_properties_by_any_scene_file_path(
                    self._file_path
                )
        # check is project file
        if self._rsv_project is None:
            raise RuntimeError(
                'file is not valid for any project'
            )
        # when file is match scene file rule use scene properties
        if self._rsv_scene_properties:
            self._rsv_properties = self._rsv_scene_properties
        else:
            self._rsv_properties = self._rsv_project.properties

        self.__completion_option_by_rsv_properties_()

    def get_ddl_job_name(self):
        return bsc_core.StgFileOpt(
            self._file_path
        ).get_name_base()

    def get_group(self):
        return self.get_ddl_job_name()

    def get_rsv_project(self):
        return self._rsv_project

    def get_rsv_properties(self):
        return self._rsv_properties

    def __completion_option_by_rsv_properties_(self):
        if self._rsv_properties is not None:
            option_opt = self.get_option_opt()
            for i_key in ['project']:
                if self._rsv_properties.get_key_is_exists(i_key):
                    option_opt.set(
                        i_key, self._rsv_properties.get(i_key)
                    )
        else:
            raise RuntimeError()

    def get_batch_name(self):
        return self._batch_name


# session for rsv task deadline job
class AbsSsnRsvTaskOptionMethod(
    AbsSsnOptionMethod,
    AbsSsnRsvDef
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnRsvTaskOptionMethod, self).__init__(*args, **kwargs)
        self._set_rsv_def_init_()
        #
        self._rsv_scene_properties = None
        self._rsv_task = None
        #
        option_opt = self.get_option_opt()
        #
        self._batch_file_path = option_opt.pop('batch_file')
        self._file_path = option_opt.get('file')
        if self._batch_file_path:
            self._rsv_scene_properties = self.resolver.get_rsv_scene_properties_by_any_scene_file_path(
                self._batch_file_path
            )
            self._rsv_task = self.resolver.get_rsv_task_by_any_file_path(
                self._batch_file_path
            )
        else:
            if self._file_path:
                self._rsv_scene_properties = self.resolver.get_rsv_scene_properties_by_any_scene_file_path(
                    self._file_path
                )
                self._rsv_task = self.resolver.get_rsv_task_by_any_file_path(
                    self._file_path
                )
        #
        self.__completion_option_by_rsv_scene_properties_()
        #
        # print self.get_option_opt()
        # print self.get_option()

        self._validation_checker = ValidationChecker(self)

    def _set_system_option_completion_(self):
        option_opt = self.get_option_opt()
        for i_key in self.STD_KEYS:
            if option_opt.get(i_key) is None:
                option_opt.set(i_key, bsc_core.SystemMtd.get(i_key))

    def __completion_option_by_rsv_scene_properties_(self):
        if self._rsv_scene_properties is not None:
            option_opt = self.get_option_opt()
            for i_key in ['project', 'workspace', 'asset', 'shot', 'step', 'task', 'version', 'application']:
                if self._rsv_scene_properties.get_key_is_exists(i_key):
                    option_opt.set(
                        i_key, self._rsv_scene_properties.get(i_key)
                    )
        else:
            raise RuntimeError()

    def get_session_key(self):
        option_opt = self.get_option_opt()
        return ssn_core.SsnHookServerMtd.get_key(
            user=option_opt.get('user'),
            time_tag=option_opt.get('time_tag'),
        )

    def get_batch_file_path(self):
        option_opt = self.get_option_opt()

        file_path = ssn_core.SsnHookServerMtd.get_file_path(
            user=option_opt.get('user'),
            time_tag=option_opt.get('time_tag'),
        )
        if bsc_core.StorageMtd.get_is_exists(file_path) is False:
            raw = dict(
                user=option_opt.get('user'),
                time_tag=option_opt.get('time_tag'),
            )
            bsc_core.StgFileOpt(file_path).set_write(raw)
            bsc_core.LogMtd.trace_method_result(
                'hook batch-file write',
                'file="{}"'.format(file_path)
            )
        return file_path

    def set_ddl_result_update(self, hook_option, ddl_job_id):
        hook_option_opt = bsc_core.ArgDictStringOpt(
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
        hook_option_opt = bsc_core.ArgDictStringOpt(
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
        hook_option_opt = bsc_core.ArgDictStringOpt(
            hook_option
        )
        main_key = hook_option_opt.get('option_hook_key')
        #
        dependent_option_hook_keys = hook_option_opt.get(
            'dependencies', as_array=True
        ) or []
        for i_key in dependent_option_hook_keys:
            i_option_hook_key = ssn_core.SsnHookFileMtd.get_hook_abs_path(
                main_key, i_key
            )
            lis.append(i_option_hook_key)
        return lis

    def set_ddl_dependent_job_ids_find(self, hook_option):
        lis = []
        hook_option_opt = bsc_core.ArgDictStringOpt(
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
            i_option_hook_key = ssn_core.SsnHookFileMtd.get_hook_abs_path(
                main_key, i_key
            )
            i_ddl_job_id = c.get(
                'deadline.{}.job_id'.format(i_option_hook_key)
            )
            if i_ddl_job_id:
                lis.append(i_ddl_job_id)
        return lis

    def get_rsv_scene_properties(self):
        return self._rsv_scene_properties

    def get_rsv_task(self):
        return self._rsv_task

    def get_rsv_project(self):
        return self._rsv_task.get_rsv_project()

    def get_rsv_version_name(self):
        return self._get_rsv_task_version_(
            self.get_rsv_scene_properties()
        )

    def get_group(self):
        return self.get_rsv_version_name()

    def get_ddl_name(self):
        return self.get_name()

    def get_executor(self):
        return self.EXECUTOR(
            self
        )

    def get_validation_checker(self):
        return self._validation_checker

    def get_batch_name(self):
        return ''


class AbsOptionRsvTaskBatcherSession(
    AbsSsnRsvTaskOptionMethod
):
    def __init__(self, *args, **kwargs):
        super(AbsOptionRsvTaskBatcherSession, self).__init__(*args, **kwargs)


class AbsApplicationSession(AbsSsnObj):
    def __init__(self, *args, **kwargs):
        super(AbsApplicationSession, self).__init__(*args, **kwargs)


class AbsCommandSession(AbsSsnObj):
    def __init__(self, *args, **kwargs):
        super(AbsCommandSession, self).__init__(*args, **kwargs)

    def execute(self):
        type_ = self.basic_configure.get('type')
        if type_ == 'shell-command':
            shell_file_path = self.get_shell_script_file()
            if shell_file_path:
                self.execute_shell_file_fnc(shell_file_path, session=self)
            else:
                command = self.basic_configure.get('command')
                if command:
                    self.execute_shell_command(command, session=self)
        elif type_ == 'python-command':
            python_file_path = self.get_python_script_file()
            if python_file_path:
                self.execute_python_file_fnc(python_file_path, session=self)
            else:
                command = self.basic_configure.get('command')
                self.execute_python_command(command, session=self)


if __name__ == '__main__':
    print AbsSsnObj._match_fnc_(
        'branch=asset&step=srf',
        {
            "root": "/production/shows",
            "project": "nsa_dev",
            "workspace": "work",
            "workspace_key": "user",
            "branch": "asset",
            "role": "chr",
            "sequence": "",
            "asset": "td_test",
            "shot": "",
            "step": "srf",
            "task": "surface",
            "version": "v000_002",
            "task_extra": "surface",
            "version_extra": "",
            "user": "",
            "artist": "dongchangbao"
        }
    )
