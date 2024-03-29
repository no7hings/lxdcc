# coding:utf-8
import lxbasic.log as bsc_log

from . import configure as bsc_cor_configure

from . import base as bsc_cor_base

from . import environ as bsc_cor_environ

from . import process as bsc_cor_process


class ExcBaseMtd(object):
    @classmethod
    def oiiotool(cls):
        if bsc_cor_base.SysBaseMtd.get_is_windows():
            name = 'oiiotool.exe'
            _ = bsc_cor_environ.EnvBaseMtd.find_execute(name)
            if _:
                return name
            return '{}/windows/oiiotool.exe'.format(bsc_cor_configure.BscRoot.Execute)
        elif bsc_cor_base.SysBaseMtd.get_is_linux():
            name = 'oiiotool'
            _ = bsc_cor_environ.EnvBaseMtd.find_execute(name)
            if _:
                return name
            return '{}/linux/oiiotool'.format(bsc_cor_configure.BscRoot.Execute)

    @classmethod
    def oslc(cls):
        if bsc_cor_base.SysBaseMtd.get_is_windows():
            name = 'oslc.exe'
            _ = bsc_cor_environ.EnvBaseMtd.find_execute(name)
            if _:
                return name
            return '{}/windows/oslc.exe'.format(bsc_cor_configure.BscRoot.Execute)
        elif bsc_cor_base.SysBaseMtd.get_is_linux():
            name = 'oslc'
            _ = bsc_cor_environ.EnvBaseMtd.find_execute(name)
            if _:
                return name
            return '{}/linux/oslc'.format(bsc_cor_configure.BscRoot.Execute)

    @classmethod
    def oslinfo(cls):
        if bsc_cor_base.SysBaseMtd.get_is_windows():
            name = 'oslinfo.exe'
            _ = bsc_cor_environ.EnvBaseMtd.find_execute(name)
            if _:
                return name
            return '{}/windows/oslinfo.exe'.format(bsc_cor_configure.BscRoot.Execute)
        elif bsc_cor_base.SysBaseMtd.get_is_linux():
            name = 'oslinfo'
            _ = bsc_cor_environ.EnvBaseMtd.find_execute(name)
            if _:
                return name
            return '{}/linux/oslinfo'.format(bsc_cor_configure.BscRoot.Execute)

    @classmethod
    def ffmpeg(cls):
        if bsc_cor_base.SysBaseMtd.get_is_windows():
            return 'l:/packages/pg/third_party/app/ffmpeg/4.4.0/platform-windows/bin/ffmpeg.exe'
        elif bsc_cor_base.SysBaseMtd.get_is_linux():
            return '/l/packages/pg/third_party/app/ffmpeg/4.4.0/platform-linux/bin/ffmpeg'


class ExcExtraMtd(object):
    @staticmethod
    def execute_python_file(file_path, **kwargs):
        # use for python 3
        # with open(file_path, 'r') as f:
        #     exec (f.read())
        # use for python 2
        bsc_log.Log.trace_method_result(
            'option-hook', 'start for : "{}"'.format(
                file_path
            )
        )
        kwargs['__name__'] = '__main__'
        execfile(file_path, kwargs)
        bsc_log.Log.trace_method_result(
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
        bsc_log.Log.trace_method_result(
            'option-hook', 'start for : "{}"'.format(
                file_path
            )
        )
        if bsc_cor_base.SysPlatformMtd.get_is_linux():
            cmds = [
                'gnome-terminal', '-t', kwargs.get('title') or 'untitled',
                '-e "bash -l {}"'.format(file_path)
            ]
            bsc_cor_process.PrcBaseMtd.execute_as_trace(
                ' '.join(cmds)
            )
        elif bsc_cor_base.SysPlatformMtd.get_is_windows():
            cmds = ['start', 'cmd', '/k', file_path]
            bsc_cor_process.PrcBaseMtd.execute_as_trace(
                ' '.join(cmds)
            )
        bsc_log.Log.trace_method_result(
            'option-hook', 'complete for: "{}"'.format(
                file_path
            )
        )

    @staticmethod
    def execute_shell_script_use_terminal(cmd, **kwargs):
        if bsc_cor_base.SysPlatformMtd.get_is_linux():
            cmds = [
                'gnome-terminal',
                '-t', kwargs.get('title') or 'untitled',
                '--', 'bash', '-l', '-c', cmd
            ]
            bsc_cor_process.PrcBaseMtd.execute_as_trace(
                ' '.join(cmds)
            )
        elif bsc_cor_base.SysPlatformMtd.get_is_windows():
            cmds = ['start', 'cmd', '/k', cmd]
            bsc_cor_process.PrcBaseMtd.execute_as_trace(
                ' '.join(cmds)
            )

    @staticmethod
    def execute_shell_script(cmd, use_thread=True):
        if use_thread is True:
            bsc_cor_process.PrcBaseMtd.execute_use_thread(cmd)
        else:
            bsc_cor_process.PrcBaseMtd.execute(cmd)
