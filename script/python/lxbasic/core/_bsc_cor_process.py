# coding:utf-8
import six
from ._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_log, _bsc_cor_environ


class SubProcessMtd(object):
    if platform.system().lower() == 'windows':
        # noinspection PyUnresolvedReferences
        NO_WINDOW = subprocess.STARTUPINFO()
        NO_WINDOW.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    else:
        NO_WINDOW = None
    #
    ENVIRON_MARK = os.environ
    #
    def __init__(self):
        pass
    @classmethod
    def get_environs(cls, **kwargs):
        environs_extend = kwargs.get('environs_extend', {})
        if environs_extend:
            environs = dict(os.environ)
            environs = {str(k): str(v) for k, v in environs.items()}
            env_opt = _bsc_cor_environ.EnvironsOpt(environs)
            for k, v in environs_extend.items():
                if isinstance(v, six.string_types):
                    env_opt.set(
                        k, v
                    )
                    _bsc_cor_log.LogMtd.trace_method_result(
                        'sub-process execute',
                        'environ set: "{}"="{}"'.format(k, v)
                    )
                elif isinstance(v, tuple):
                    i_v, i_opt = v
                    if i_opt == 'set':
                        env_opt.set(
                            k, v
                        )
                        _bsc_cor_log.LogMtd.trace_method_result(
                            'sub-process execute',
                            'environ set: "{}"="{}"'.format(k, v)
                        )
                    elif i_opt == 'append':
                        env_opt.append(
                            k, i_v
                        )
                        _bsc_cor_log.LogMtd.trace_method_result(
                            'sub-process execute',
                            'environ append: "{}"="{}"'.format(k, i_v)
                        )
                    elif i_opt == 'prepend':
                        env_opt.prepend(
                            k, i_v
                        )
                        _bsc_cor_log.LogMtd.trace_method_result(
                            'sub-process execute',
                            'environ prepend: "{}"="{}"'.format(k, i_v)
                        )
            return environs
    @classmethod
    def set_run_with_result_in_windows(cls, cmd, **kwargs):
        cmd = cmd.replace("&", "^&")
        #
        clear_environ = kwargs.get('kwargs', False)
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
                # env=cls.ENVIRON_MARK
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
            except:
                pass
        #
        retcode = s_p.poll()
        if retcode:
            raise subprocess.CalledProcessError(retcode, cmd)
        #
        s_p.stdout.close()
    @classmethod
    def set_run_with_result_in_linux(cls, cmd, **kwargs):
        clear_environ = kwargs.get('kwargs', False)
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
                # env=cls.ENVIRON_MARK
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
            except:
                pass
        #
        retcode = s_p.poll()
        if retcode:
            raise subprocess.CalledProcessError(retcode, cmd)
        #
        s_p.stdout.close()
    @classmethod
    def set_run_with_result(cls, cmd, **kwargs):
        if SystemMtd.get_is_windows():
            cls.set_run_with_result_in_windows(cmd, **kwargs)
        elif SystemMtd.get_is_linux():
            cls.set_run_with_result_in_linux(cmd, **kwargs)
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
    def set_run_with_result_use_thread(cls, cmd):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.set_run_with_result,
                cmd=cmd
            )
        )
        t_0.start()
        # t_0.join()
    @classmethod
    def set_run_as_block(cls, cmd):
        process = subprocess.Popen(
            cmd,
            shell=True,
            # close_fds=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            startupinfo=cls.NO_WINDOW
        )
        output, unused_err = process.communicate()
        #
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, cmd)
        process.wait()
        return output.decode().splitlines()
