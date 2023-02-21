# coding:utf-8
import threading

import functools

from lxbasic import bsc_core

import lxbasic.extra.methods as bsc_etr_methods


class AbsRsvAppOpt(object):
    def __init__(self, rsv_app):
        self._rsv_app = rsv_app
        self._rsv_project = rsv_app._rsv_project

    @classmethod
    def _execute_command_(cls, cmd, **sub_progress_kwargs):
        bsc_core.LogMtd.trace_method_result(
            'sub-progress run with result',
            'command=`{}` is started'.format(cmd.decode('utf-8'))
        )
        bsc_core.SubProcessMtd.set_run_with_result(
            cmd, **sub_progress_kwargs
        )
        bsc_core.LogMtd.trace_method_result(
            'sub-progress run with result',
            'command=`{}` is completed'.format(cmd.decode('utf-8'))
        )
    @classmethod
    def _execute_command_use_thread_(cls, cmd, **sub_progress_kwargs):
        t_0 = threading.Thread(
            target=functools.partial(
                cls._execute_command_,
                cmd=cmd,
                **sub_progress_kwargs
            )
        )
        t_0.start()

    def get_environs_extend(self):
        framework_scheme = self._rsv_project.get_framework_scheme()
        m = bsc_etr_methods.get_module(framework_scheme)
        return m.EtrUtility.get_project_environs_extend(
            self._rsv_project.get_name()
        )

    def open(self):
        raise NotImplementedError()

    def open_file(self, *args, **kwargs):
        raise NotImplementedError()

    def get_packages_extend(self):
        framework_scheme = self._rsv_project.get_framework_scheme()
        if framework_scheme == 'default':
            return []
        elif framework_scheme == 'new':
            return ['lxdcc', 'lxdcc_lib', 'lxdcc_gui', 'lxdcc_rsc']
        return []


class RsvMayaOpt(AbsRsvAppOpt):
    def __init__(self, *args, **kwargs):
        super(RsvMayaOpt, self).__init__(*args, **kwargs)

    def open(self):
        cmd = self._rsv_app.get_command(
            args_execute=[
                '-- maya',
            ],
            packages_extend=self.get_packages_extend()
        )
        self._execute_command_use_thread_(
            cmd,
            # clear_environ=True,
            environs_extend=self.get_environs_extend()
        )

    def open_file(self, file_path):
        cmd = self._rsv_app.get_command(
            args_execute=[
                '-- maya',
                r'-command "python(\"import lxmaya.dcc.dcc_objects as mya_dcc_objects; mya_dcc_objects.Scene.set_file_open_as_project(\\\"{}\\\")\")"'.format(
                    file_path
                )
            ],
            packages_extend=self.get_packages_extend()
        )
        self._execute_command_use_thread_(
            cmd,
            # clear_environ=True,
            environs_extend=self.get_environs_extend()
        )


class RsvHoudiniOpt(AbsRsvAppOpt):
    def __init__(self, *args, **kwargs):
        super(RsvHoudiniOpt, self).__init__(*args, **kwargs)

    def open(self):
        cmd = self._rsv_app.get_command(
            args_execute=[
                '-- houdini',
            ],
            packages_extend=self.get_packages_extend()
        )
        self._execute_command_use_thread_(
            cmd,
            # clear_environ=True,
            environs_extend=self.get_environs_extend()
        )

    def open_file(self, file_path):
        pass


class RsvKatanaOpt(AbsRsvAppOpt):
    def __init__(self, *args, **kwargs):
        super(RsvKatanaOpt, self).__init__(*args, **kwargs)

    def open(self):
        cmd = self._rsv_app.get_command(
            args_execute=[
                '-- katana',
            ],
            packages_extend=self.get_packages_extend()
        )
        self._execute_command_use_thread_(
            cmd,
            # clear_environ=True,
            environs_extend=self.get_environs_extend()
        )

    def open_file(self, file_path):
        cmd = self._rsv_app.get_command(
            args_execute=[
                '-- katana',
                '"{}"'.format(
                    file_path
                )
            ],
            packages_extend=self.get_packages_extend()
        )
        self._execute_command_use_thread_(
            cmd,
            # clear_environ=True,
            environs_extend=self.get_environs_extend()
        )
