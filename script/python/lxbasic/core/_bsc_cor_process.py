# coding:utf-8
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
                    _bsc_cor_log.LogMtd.trace_method_result(
                        'sub-process',
                        'environ set: "{}"="{}"'.format(k, v)
                    )
                elif isinstance(v, tuple):
                    i_v, i_opt = v
                    if i_opt == 'set':
                        env_opt.set(
                            k, v
                        )
                        _bsc_cor_log.LogMtd.trace_method_result(
                            'sub-process',
                            'environ set: "{}"="{}"'.format(k, v)
                        )
                    elif i_opt == 'append':
                        env_opt.append(
                            k, i_v
                        )
                        _bsc_cor_log.LogMtd.trace_method_result(
                            'sub-process',
                            'environ append: "{}"="{}"'.format(k, i_v)
                        )
                    elif i_opt == 'prepend':
                        env_opt.prepend(
                            k, i_v
                        )
                        _bsc_cor_log.LogMtd.trace_method_result(
                            'sub-process',
                            'environ prepend: "{}"="{}"'.format(k, i_v)
                        )
            return environs
    @classmethod
    def get_clear_environs(cls, keys_exclude):
        environs_old = dict(os.environ)
        environs = {k: v for k, v in environs_old.items() if k not in keys_exclude}
        return environs
    @classmethod
    def check_command_clear_environ(cls, cmd):
        # todo, read form configure?
        if fnmatch.filter(
            [cmd], '*/paper-bin*'
        ):
            return True
        return False
    @classmethod
    def execute_with_result_in_windows(cls, cmd, **kwargs):
        cmd = cmd.replace("&", "^&")
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
                env=SystemMtd.get_environment()
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
            except:
                pass
        #
        retcode = s_p.poll()
        if retcode:
            raise subprocess.CalledProcessError(retcode, cmd)
        #
        s_p.stdout.close()
    @classmethod
    def execute_with_result(cls, cmd, **kwargs):
        if SystemMtd.get_is_windows():
            cls.execute_with_result_in_windows(cmd, **kwargs)
        elif SystemMtd.get_is_linux():
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
    def set_run_with_result_use_thread(cls, cmd):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.execute_with_result,
                cmd=cmd
            )
        )
        t_0.start()
        # t_0.join()
    @classmethod
    def execute_as_block(cls, cmd, **kwargs):
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
    def execute_use_thread(cls, cmd):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.execute,
                cmd=cmd
            )
        )
        t_0.start()
