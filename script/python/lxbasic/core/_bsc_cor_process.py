# coding:utf-8
# from ._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_utility

import sys

import six

import os

import platform

import copy

import subprocess

import fnmatch

import re

import threading

import functools

import lxlog.core as log_core

from lxbasic.core import _bsc_cor_environ


class SubProcessMtd(object):
    if platform.system().lower() == 'windows':
        # noinspection PyUnresolvedReferences
        NO_WINDOW = subprocess.STARTUPINFO()
        NO_WINDOW.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    else:
        NO_WINDOW = None
    #
    ENVIRON_MARK = copy.copy(os.environ)

    #
    @classmethod
    def get_environs(cls, **kwargs):
        environs_extend = kwargs.get('environs_extend', {})
        if environs_extend:
            environs_old = dict(os.environ)
            environs = {str(k): str(v) for k, v in environs_old.items()}
            env_opt = _bsc_cor_environ.EnvironsOpt(environs)
            for k, v in environs_extend.items():
                if isinstance(v, six.string_types):
                    env_opt.set(
                        k, v
                    )
                    log_core.Log.trace_method_result(
                        'sub-process',
                        'environ set: "{}"="{}"'.format(k, v)
                    )
                elif isinstance(v, tuple):
                    i_v, i_opt = v
                    if i_opt == 'set':
                        env_opt.set(
                            k, v
                        )
                        log_core.Log.trace_method_result(
                            'sub-process',
                            'environ set: "{}"="{}"'.format(k, v)
                        )
                    elif i_opt == 'append':
                        env_opt.append(
                            k, i_v
                        )
                        log_core.Log.trace_method_result(
                            'sub-process',
                            'environ append: "{}"="{}"'.format(k, i_v)
                        )
                    elif i_opt == 'prepend':
                        env_opt.prepend(
                            k, i_v
                        )
                        log_core.Log.trace_method_result(
                            'sub-process',
                            'environ prepend: "{}"="{}"'.format(k, i_v)
                        )
            return environs
        return {str(k): str(v) for k, v in dict(os.environ).items()}

    @classmethod
    def get_clear_environs(cls, keys_exclude):
        environs_old = dict(os.environ)
        environs = {k: v for k, v in environs_old.items() if k not in keys_exclude}
        return environs

    @classmethod
    def check_command_clear_environ(cls, cmd):
        # todo, read form configure?

        ps = [
            r'(.*)/paper-bin\s(.*)', r'paper\s(.*)',
            r'(.*)/windows/paper\s(.*)'
        ]

        # print 'command is', cmd
        for i_p in ps:
            if re.search(i_p, cmd) is not None:
                return True
        return False

    @classmethod
    def execute_with_result_in_windows(cls, cmd, **kwargs):
        cmd = re.sub(r'(?<!&)&(?!&)', '^&', cmd)
        #
        clear_environ = kwargs.get('clear_environ', False)
        if clear_environ == 'auto':
            clear_environ = cls.check_command_clear_environ(cmd)
        #
        if clear_environ is True:
            s_p = subprocess.Popen(
                cmd,
                shell=True,
                # close_fds=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=cls.NO_WINDOW,
                env=dict()
            )
        else:
            environs_extend = kwargs.get('environs_extend', {})
            if environs_extend:
                environs = cls.get_environs(**kwargs)
                s_p = subprocess.Popen(
                    cmd,
                    shell=True,
                    # close_fds=True,
                    universal_newlines=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    startupinfo=cls.NO_WINDOW,
                    env=environs
                )
            else:
                s_p = subprocess.Popen(
                    cmd,
                    shell=True,
                    # close_fds=True,
                    universal_newlines=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    startupinfo=cls.NO_WINDOW,
                )
        #
        while True:
            next_line = s_p.stdout.readline()
            #
            return_line = next_line
            if return_line == '' and s_p.poll() is not None:
                break
            #
            return_line = return_line.decode('gbk', 'ignore')
            # noinspection PyBroadException
            try:
                print(return_line.encode('gbk').rstrip())
            except Exception:
                pass
        #
        retcode = s_p.poll()
        if retcode:
            raise subprocess.CalledProcessError(retcode, cmd)
        #
        s_p.stdout.close()

    @classmethod
    def execute_with_result_in_linux(cls, cmd, **kwargs):
        clear_environ = kwargs.get('clear_environ', False)
        if clear_environ == 'auto':
            clear_environ = cls.check_command_clear_environ(cmd)
        #
        if clear_environ is True:
            s_p = subprocess.Popen(
                cmd,
                shell=True,
                # close_fds=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=cls.NO_WINDOW,
                env=dict()
            )
        else:
            environs_extend = kwargs.get('environs_extend', {})
            if environs_extend:
                environs = cls.get_environs(**kwargs)
                s_p = subprocess.Popen(
                    cmd,
                    shell=True,
                    # close_fds=True,
                    universal_newlines=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    startupinfo=cls.NO_WINDOW,
                    env=environs
                )
            else:
                s_p = subprocess.Popen(
                    cmd,
                    shell=True,
                    # close_fds=True,
                    universal_newlines=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    startupinfo=cls.NO_WINDOW,
                )
        #
        while True:
            next_line = s_p.stdout.readline()
            #
            return_line = next_line
            if return_line == '' and s_p.poll() is not None:
                break
            #
            return_line = return_line.decode('utf-8', 'ignore')
            return_line = return_line.replace(u'\u2018', "'").replace(u'\u2019', "'")
            # noinspection PyBroadException
            try:
                print(return_line.encode('utf-8').rstrip())
            except Exception:
                pass
        #
        retcode = s_p.poll()
        if retcode:
            raise subprocess.CalledProcessError(retcode, cmd)
        #
        s_p.stdout.close()

    @classmethod
    def execute_with_result(cls, cmd, **kwargs):
        if _bsc_cor_utility.SystemMtd.get_is_windows():
            cls.execute_with_result_in_windows(cmd, **kwargs)
        elif _bsc_cor_utility.SystemMtd.get_is_linux():
            cls.execute_with_result_in_linux(cmd, **kwargs)

    @classmethod
    def set_run(cls, cmd):
        _sp = subprocess.Popen(
            cmd,
            shell=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            startupinfo=cls.NO_WINDOW,
        )
        return _sp

    @classmethod
    def set_run_with_result_use_thread(cls, cmd, **kwargs):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.execute_with_result,
                cmd=cmd,
                **kwargs
            )
        )
        t_0.start()
        # t_0.join()

    @classmethod
    def execute_with_result_use_thread(cls, cmd, **kwargs):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.execute_with_result,
                cmd=cmd,
                **kwargs
            )
        )
        t_0.start()

    @classmethod
    def execute_as_block(cls, cmd, **kwargs):
        clear_environ = kwargs.get('clear_environ', False)
        if clear_environ == 'auto':
            clear_environ = cls.check_command_clear_environ(cmd)
        #
        return_dict = kwargs.get('return_dict', {})
        if clear_environ is True:
            s_p = subprocess.Popen(
                cmd,
                shell=True,
                # close_fds=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=cls.NO_WINDOW,
                env=dict()
            )
        else:
            s_p = subprocess.Popen(
                cmd,
                shell=True,
                # close_fds=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=cls.NO_WINDOW,
            )
        #
        output, unused_err = s_p.communicate()
        #
        if s_p.returncode != 0:
            for i in output.decode('utf-8').splitlines():
                sys.stderr.write(i+'\n')
            return_dict['results'] = output.decode('utf-8').splitlines()
            raise subprocess.CalledProcessError(s_p.returncode, cmd)
        #
        s_p.wait()
        return_dict['results'] = output.decode('utf-8').splitlines()
        return output.decode('utf-8').splitlines()

    @classmethod
    def generator(cls, cmd, **kwargs):
        clear_environ = kwargs.get('clear_environ', False)
        if clear_environ == 'auto':
            clear_environ = cls.check_command_clear_environ(cmd)

        if clear_environ is True:
            s_p = subprocess.Popen(
                cmd,
                shell=True,
                # close_fds=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=cls.NO_WINDOW,
                env=dict()
            )
        else:
            environs_extend = kwargs.get('environs_extend', {})
            if environs_extend:
                environs = cls.get_environs(**kwargs)
                s_p = subprocess.Popen(
                    cmd,
                    shell=True,
                    # close_fds=True,
                    universal_newlines=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    startupinfo=cls.NO_WINDOW,
                    env=environs
                )
            else:
                s_p = subprocess.Popen(
                    cmd,
                    shell=True,
                    # close_fds=True,
                    universal_newlines=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    startupinfo=cls.NO_WINDOW,
                )
        return s_p

    @classmethod
    def execute(cls, cmd):
        s_p = subprocess.Popen(
            cmd,
            shell=True,
            # close_fds=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            startupinfo=cls.NO_WINDOW,
        )
        #
        output, unused_err = s_p.communicate()
        #
        if s_p.returncode != 0:
            for i in output.decode('utf-8').splitlines():
                sys.stderr.write(i+'\n')
            raise subprocess.CalledProcessError(s_p.returncode, cmd)
        s_p.wait()
        return output.decode('utf-8').splitlines()

    @classmethod
    def execute_(cls, cmd):
        s_p = subprocess.Popen(
            cmd,
            shell=True,
            # close_fds=True,
            universal_newlines=True,
            stdout=subprocess.STDOUT,
            stderr=subprocess.STDOUT,
            startupinfo=cls.NO_WINDOW,
        )
        #
        output, unused_err = s_p.communicate()
        #
        if s_p.returncode != 0:
            for i in output.decode('utf-8').splitlines():
                sys.stderr.write(i+'\n')
            raise subprocess.CalledProcessError(s_p.returncode, cmd)
        s_p.wait()
        return output.decode('utf-8').splitlines()

    @classmethod
    def execute_use_thread(cls, cmd):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.execute,
                cmd=cmd
            )
        )
        t_0.start()


if __name__ == '__main__':
    pass
    # text = '/job/PLE/support/wrappers/paper-bin --j'
    # p = r'(.*)/paper-bin\s(.*)'
    # m = re.search(p, text)
    # print m.group(1)
    # print m.group(2)


