# coding:utf-8
import threading

import functools

from lxbasic import bsc_core


class AbsRsvAppOpt(object):
    def __init__(self, rsv_app):
        self._rsv_app = rsv_app

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
            'command=`{}` is completed'.format(cmd)
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

    def open_file(self, *args, **kwargs):
        raise NotImplementedError()


class RsvMayaOpt(AbsRsvAppOpt):
    def __init__(self, rsv_app):
        super(RsvMayaOpt, self).__init__(rsv_app)

    def open_file(self, file_path):
        cmd = self._rsv_app.get_command(
            args_extend=[
                '-- maya',
                r'-command "python(\"import lxmaya.dcc.dcc_objects as mya_dcc_objects; mya_dcc_objects.Scene.set_file_open_as_project(\\\"{}\\\")\")"'.format(
                    file_path
                )
            ]
        )
        self._execute_command_use_thread_(cmd, clear_environ=True)


class RsvKatanaOpt(AbsRsvAppOpt):
    def __init__(self, rsv_app):
        super(RsvKatanaOpt, self).__init__(rsv_app)

    def open_file(self, file_path):
        cmd = self._rsv_app.get_command(
            args_extend=[
                '-- katana',
                '"{}"'.format(
                    file_path
                )
            ]
        )
        self._execute_command_use_thread_(cmd)
