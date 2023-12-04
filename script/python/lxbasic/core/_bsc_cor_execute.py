# coding:utf-8
import lxlog.core as log_core

from ..core import \
    _bsc_cor_configure, \
    _bsc_cor_base, \
    _bsc_cor_environ, \
    _bsc_cor_process


class Executes(object):
    @classmethod
    def oiiotool(cls):
        if _bsc_cor_base.SystemMtd.get_is_windows():
            name = 'oiiotool.exe'
            _ = _bsc_cor_environ.EnvironMtd.find_execute(name)
            if _:
                return name
            return '{}/windows/oiiotool.exe'.format(_bsc_cor_configure.BscRoot.Execute)
        elif _bsc_cor_base.SystemMtd.get_is_linux():
            name = 'oiiotool'
            _ = _bsc_cor_environ.EnvironMtd.find_execute(name)
            if _:
                return name
            return '{}/linux/oiiotool'.format(_bsc_cor_configure.BscRoot.Execute)

    @classmethod
    def oslc(cls):
        if _bsc_cor_base.SystemMtd.get_is_windows():
            name = 'oslc.exe'
            _ = _bsc_cor_environ.EnvironMtd.find_execute(name)
            if _:
                return name
            return '{}/windows/oslc.exe'.format(_bsc_cor_configure.BscRoot.Execute)
        elif _bsc_cor_base.SystemMtd.get_is_linux():
            name = 'oslc'
            _ = _bsc_cor_environ.EnvironMtd.find_execute(name)
            if _:
                return name
            return '{}/linux/oslc'.format(_bsc_cor_configure.BscRoot.Execute)

    @classmethod
    def oslinfo(cls):
        if _bsc_cor_base.SystemMtd.get_is_windows():
            name = 'oslinfo.exe'
            _ = _bsc_cor_environ.EnvironMtd.find_execute(name)
            if _:
                return name
            return '{}/windows/oslinfo.exe'.format(_bsc_cor_configure.BscRoot.Execute)
        elif _bsc_cor_base.SystemMtd.get_is_linux():
            name = 'oslinfo'
            _ = _bsc_cor_environ.EnvironMtd.find_execute(name)
            if _:
                return name
            return '{}/linux/oslinfo'.format(_bsc_cor_configure.BscRoot.Execute)

    @classmethod
    def ffmpeg(cls):
        if _bsc_cor_base.SystemMtd.get_is_windows():
            return 'l:/packages/pg/third_party/app/ffmpeg/4.4.0/platform-windows/bin/ffmpeg.exe'
        elif _bsc_cor_base.SystemMtd.get_is_linux():
            return '/l/packages/pg/third_party/app/ffmpeg/4.4.0/platform-linux/bin/ffmpeg'


class ExcExtra(object):
    @staticmethod
    def execute_python_file(file_path, **kwargs):
        # use for python 3
        # with open(file_path, 'r') as f:
        #     exec (f.read())
        # use for python 2
        log_core.Log.trace_method_result(
            'option-hook', 'start for : "{}"'.format(
                file_path
            )
        )
        kwargs['__name__'] = '__main__'
        execfile(file_path, kwargs)
        log_core.Log.trace_method_result(
            'option-hook', 'complete for: "{}"'.format(
                file_path
            )
        )

    @staticmethod
    def execute_python_script(cmd, **kwargs):
        # noinspection PyUnusedLocal
        session = kwargs['session']
        exec cmd

    @staticmethod
    def execute_shell_file_use_terminal(file_path, **kwargs):
        log_core.Log.trace_method_result(
            'option-hook', 'start for : "{}"'.format(
                file_path
            )
        )
        if _bsc_cor_base.PlatformMtd.get_is_linux():
            cmds = [
                'gnome-terminal', '-t', kwargs.get('title') or 'untitled',
                '-e "bash -l {}"'.format(file_path)
            ]
            _bsc_cor_process.SubProcessMtd.execute_as_trace(
                ' '.join(cmds)
            )
        elif _bsc_cor_base.PlatformMtd.get_is_windows():
            cmds = ['start', 'cmd', '/k', file_path]
            _bsc_cor_process.SubProcessMtd.execute_as_trace(
                ' '.join(cmds)
            )
        log_core.Log.trace_method_result(
            'option-hook', 'complete for: "{}"'.format(
                file_path
            )
        )

    @staticmethod
    def execute_shell_script_use_terminal(cmd, **kwargs):
        if _bsc_cor_base.PlatformMtd.get_is_linux():
            cmds = [
                'gnome-terminal',
                '-t', kwargs.get('title') or 'untitled',
                '--', 'bash', '-l', '-c', cmd
            ]
            _bsc_cor_process.SubProcessMtd.execute_as_trace(
                ' '.join(cmds)
            )
        elif _bsc_cor_base.PlatformMtd.get_is_windows():
            cmds = ['start', 'cmd', '/k', cmd]
            _bsc_cor_process.SubProcessMtd.execute_as_trace(
                ' '.join(cmds)
            )

    @staticmethod
    def execute_shell_script(cmd, use_thread=True):
        if use_thread is True:
            _bsc_cor_process.SubProcessMtd.execute_use_thread(cmd)
        else:
            _bsc_cor_process.SubProcessMtd.execute(cmd)
