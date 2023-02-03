# coding:utf-8
from ._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_process


class TrdSignal(object):
    # noinspection PyUnusedLocal
    def __init__(self, *args, **kwargs):
        self._fncs = []

    def set_connect_to(self, fnc):
        self._fncs.append(fnc)

    def set_emit_send(self, *args, **kwargs):
        if self._fncs:
            ts = [threading.Thread(target=i, args=args, kwargs=kwargs) for i in self._fncs]
            for t in ts:
                t.start()
            for t in ts:
                t.join()


class TrdCmdProcess(threading.Thread):
    STACK = []
    # MAXIMUM = int(CPU_COUNT*.75)
    MAXIMUM = 6
    EVENT = threading.Event()
    LOCK = threading.Lock()
    #
    Status = bsc_configure.Status
    def __init__(self, cmd, index=0):
        threading.Thread.__init__(self)
        self._cmd = cmd
        self._index = index

        self._status = self.Status.Started

        self._status_changed_signal = TrdSignal(int, int)
        self._completed_signal = TrdSignal(int, list)
        self._failed_signal = TrdSignal(int, list)
        self._finished_signal = TrdSignal(int, int, list)

        self._is_kill = False

    def __set_status_update(self, status):
        self._status = status
        if self._is_kill is False:
            self._status_changed_signal.set_emit_send(
                self._index, status
            )

    def __set_completed(self, results):
        if self._is_kill is False:
            self._completed_signal.set_emit_send(
                self._index, results
            )

    def __set_failed(self, results):
        if self._is_kill is False:
            self._failed_signal.set_emit_send(
                self._index, results
            )

    def __set_finished(self, status, results):
        if self._is_kill is False:
            self._finished_signal.set_emit_send(
                self._index, status, results
            )
    @property
    def status_changed(self):
        return self._status_changed_signal
    @property
    def completed(self):
        return self._completed_signal
    @property
    def failed(self):
        return self._failed_signal
    @property
    def finished(self):
        return self._finished_signal

    def run(self):
        self.__set_status_update(self.Status.Running)
        results = []
        try:
            if isinstance(self._cmd, six.string_types):
                results = _bsc_cor_process.SubProcessMtd.set_run_as_block(
                    self._cmd
                )
                self.__set_status_update(self.Status.Completed)
                self.__set_completed(results)
            elif isinstance(self._cmd, (set, tuple, list)):
                for i_cmd in self._cmd:
                    results.extend(
                        _bsc_cor_process.SubProcessMtd.set_run_as_block(
                            i_cmd
                        )
                    )
                self.__set_status_update(self.Status.Completed)
                self.__set_completed(results)
        except subprocess.CalledProcessError as _exc:
            # o = exc.output
            # s = exc.returncode
            results = []
            self.__set_status_update(self.Status.Failed)
            self.__set_failed(results)
        finally:
            TrdCmdProcess.LOCK.acquire()
            TrdCmdProcess.STACK.remove(self)
            # unlock
            if len(TrdCmdProcess.STACK) < TrdCmdProcess.MAXIMUM:
                TrdCmdProcess.EVENT.set()
                TrdCmdProcess.EVENT.clear()

            TrdCmdProcess.LOCK.release()

            self.__set_finished(self._status, results)
    @staticmethod
    def get_is_busy():
        return len(TrdCmdProcess.STACK) >= TrdCmdProcess.MAXIMUM
    @staticmethod
    def set_wait():
        TrdCmdProcess.LOCK.acquire()
        # lock
        if len(TrdCmdProcess.STACK) >= TrdCmdProcess.MAXIMUM:
            TrdCmdProcess.LOCK.release()
            TrdCmdProcess.EVENT.wait()
        else:
            TrdCmdProcess.LOCK.release()
    @staticmethod
    def set_start(cmd, index=0):
        TrdCmdProcess.LOCK.acquire()
        t = TrdCmdProcess(cmd, index)
        TrdCmdProcess.STACK.append(t)
        TrdCmdProcess.LOCK.release()
        t.start()
        return t

    def get_status(self):
        return self._status

    def set_kill(self):
        self.__set_status_update(
            self.Status.Killed
        )
        self._is_kill = True

    def set_quit(self):
        pass


class TrdCmdProcess_(threading.Thread):
    Status = bsc_configure.Status
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self._cmd = cmd
        #
        self._status = self.Status.Started
        #
        self.__is_killed = False
        self.__is_stopped = False
        #
        self._status_changed_signal = TrdSignal(int)
        self._logging_signal = TrdSignal(str)
        #
        self._completed_signal = TrdSignal(tuple)
        self._failed_signal = TrdSignal(tuple)
        self._finished_signal = TrdSignal(tuple)

    def __set_status_update(self, status):
        self._status = status
        self._status_changed_signal.set_emit_send(
            status
        )

    def __set_completed(self, results):
        self._completed_signal.set_emit_send(
            (self._status, ''.join(results))
        )

    def __set_failed(self, results):
        self._failed_signal.set_emit_send(
            (self._status, ''.join(results))
        )

    def __set_finished(self, results):
        self._finished_signal.set_emit_send(
            (self._status, ''.join(results))
        )

    def __set_logging(self, text):
        self._logging_signal.set_emit_send(
            text
        )
    @property
    def status_changed(self):
        return self._status_changed_signal
    @property
    def completed(self):
        return self._completed_signal
    @property
    def failed(self):
        return self._failed_signal
    @property
    def finished(self):
        return self._finished_signal
    @property
    def logging(self):
        return self._logging_signal

    def get_status(self):
        return self._status

    def set_stopped(self):
        self.__is_stopped = True

    def set_kill(self):
        self.__is_killed = True

    def run(self):
        self.__set_status_update(self.Status.Running)
        results = []
        s_p = subprocess.Popen(
            self._cmd,
            shell=True,
            # close_fds=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            startupinfo=_bsc_cor_process.SubProcessMtd.NO_WINDOW
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

            log = return_line.encode('utf-8').rstrip()
            results.append(log)
            #
            if self.__is_stopped is True:
                s_p.kill()
                self.__set_failed(results)
                self.__set_finished(results)
                return False
            if self.__is_killed is True:
                s_p.kill()
                self.__set_logging('process is killed')
                self.__set_status_update(self.Status.Killed)
                #
                self.__set_failed(results)
                self.__set_finished(results)
                return False
            #
            self.__set_logging(
                log
            )
        #
        retcode = s_p.poll()
        if retcode:
            self.__set_status_update(self.Status.Failed)
            self.__set_failed(results)
            self.__set_finished(results)
            return False
        #
        s_p.stdout.close()
        self.__set_status_update(self.Status.Completed)
        self.__set_completed(results)
        self.__set_finished(results)
        return True


class TrdMethod(threading.Thread):
    STACK = []
    MAXIMUM = 256
    EVENT = threading.Event()
    LOCK = threading.Lock()
    #
    Status = bsc_configure.Status
    def __init__(self, fnc, index, *args, **kwargs):
        threading.Thread.__init__(self)
        self._fnc = fnc
        self._args = args
        self._kwargs = kwargs
        #
        self._index = index

        self._status = self.Status.Started

        self._status_changed_signal = TrdSignal(int, int)
        self._completed_signal = TrdSignal(int, list)
        self._failed_signal = TrdSignal(int, list)
        self._finished_signal = TrdSignal(int, int, list)
    @property
    def status_changed(self):
        return self._status_changed_signal
    @property
    def completed(self):
        return self._completed_signal
    @property
    def failed(self):
        return self._failed_signal
    @property
    def finished(self):
        return self._finished_signal

    def run(self):
        self.__set_status_update(self.Status.Running)
        results = []
        try:
            results = self._fnc(*self._args, **self._kwargs) or []
            self.__set_status_update(self.Status.Completed)
            self.__set_completed(results)
        except subprocess.CalledProcessError as _exc:
            # o = exc.output
            # s = exc.returncode
            results = []
            self.__set_status_update(self.Status.Failed)
            self.__set_failed(results)
        finally:
            TrdMethod.LOCK.acquire()
            TrdMethod.STACK.remove(self)
            # unlock
            if len(TrdMethod.STACK) < TrdMethod.MAXIMUM:
                TrdMethod.EVENT.set()
                TrdMethod.EVENT.clear()

            TrdMethod.LOCK.release()

            self.__set_finished(self._status, results)
    @staticmethod
    def get_is_busy():
        return len(TrdMethod.STACK) >= TrdMethod.MAXIMUM
    @staticmethod
    def set_wait():
        TrdMethod.LOCK.acquire()
        # lock
        if len(TrdMethod.STACK) >= TrdMethod.MAXIMUM:
            TrdMethod.LOCK.release()
            TrdMethod.EVENT.wait()
        else:
            TrdMethod.LOCK.release()
    @staticmethod
    def set_start(fnc, index, *args, **kwargs):
        TrdMethod.LOCK.acquire()
        t = TrdMethod(fnc, index, *args, **kwargs)
        TrdMethod.STACK.append(t)
        TrdMethod.LOCK.release()
        t.start()
        return t

    def __set_completed(self, results):
        self._completed_signal.set_emit_send(
            self._index, results
        )

    def __set_failed(self, results):
        self._failed_signal.set_emit_send(
            self._index, results
        )

    def __set_finished(self, status, results):
        self._finished_signal.set_emit_send(
            self._index, status, results
        )

    def __set_status_update(self, status):
        self._status = status
        self._status_changed_signal.set_emit_send(
            self._index, status
        )

    def get_status(self):
        return self._status


class TrdFncProcess(TrdMethod):
    MAXIMUM = 6
    def __init__(self, fnc, index, *args, **kwargs):
        super(TrdFncProcess, self).__init__(fnc, index, *args, **kwargs)
