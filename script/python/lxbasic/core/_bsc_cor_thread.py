# coding:utf-8
from ._bsc_cor_utility import *

import threading

from lxbasic.core import _bsc_cor_process


class TrdSignal(object):
    # noinspection PyUnusedLocal
    def __init__(self, *args, **kwargs):
        self._fncs = []

    def connect_to(self, fnc):
        self._fncs.append(fnc)

    def send_emit(self, *args, **kwargs):
        if self._fncs:
            ts = [threading.Thread(target=i, args=args, kwargs=kwargs) for i in self._fncs]
            for t in ts:
                t.start()
            for t in ts:
                t.join()


class TrdCommandPool(threading.Thread):
    STACK = []
    # MAXIMUM = int(CPU_COUNT*.75)
    MAXIMUM = 8
    EVENT = threading.Event()
    LOCK = threading.Lock()
    #
    Status = bsc_configure.Status

    def __init__(self, cmd, index=0):
        threading.Thread.__init__(self)
        self._cmd = cmd
        self._index = index

        self._status = self.Status.Started

        self.__status_changed_signal = TrdSignal(int, int)
        self.__completed_signal = TrdSignal(int, list)
        self.__failed_signal = TrdSignal(int, list)
        self.__finished_signal = TrdSignal(int, int, list)

        self._is_kill = False

        self._options = {}

    def __set_status_update(self, status):
        self._status = status
        if self._is_kill is False:
            self.__status_changed_signal.send_emit(
                self._index, status
            )

    def __set_completed(self, results):
        if self._is_kill is False:
            self.__completed_signal.send_emit(
                self._index, results
            )

    def __set_failed(self, results):
        if self._is_kill is False:
            self.__failed_signal.send_emit(
                self._index, results
            )

    def __set_finished(self, status, results):
        if self._is_kill is False:
            self.__finished_signal.send_emit(
                self._index, status, results
            )

    @property
    def status_changed(self):
        return self.__status_changed_signal

    @property
    def completed(self):
        return self.__completed_signal

    @property
    def failed(self):
        return self.__failed_signal

    @property
    def finished(self):
        return self.__finished_signal

    def run(self):
        self.__set_status_update(self.Status.Running)
        #
        status = self.Status.Running
        return_dicts = []
        try:
            # single process
            if isinstance(self._cmd, six.string_types):
                return_dict = {}
                return_dicts.append(return_dict)
                _bsc_cor_process.SubProcessMtd.execute_as_block(
                    self._cmd, clear_environ='auto', return_dict=return_dict
                )
                status = self.Status.Completed
            # many process execute one by one
            elif isinstance(self._cmd, (set, tuple, list)):
                for i_cmd in self._cmd:
                    i_return_dict = {}
                    return_dicts.append(i_return_dict)
                    _bsc_cor_process.SubProcessMtd.execute_as_block(
                        i_cmd, clear_environ='auto', return_dict=i_return_dict
                    )
                status = self.Status.Completed
        except subprocess.CalledProcessError:
            status = self.Status.Failed
        finally:
            TrdCommandPool.LOCK.acquire()
            TrdCommandPool.STACK.remove(self)
            # unlock
            if len(TrdCommandPool.STACK) < TrdCommandPool.MAXIMUM:
                TrdCommandPool.EVENT.set()
                TrdCommandPool.EVENT.clear()
            TrdCommandPool.LOCK.release()

            results = []
            for i_return_dict in return_dicts:
                results.extend(i_return_dict['results'])

            self.__set_status_update(status)
            if status == self.Status.Completed:
                self.__set_completed(results)
            elif status == self.Status.Failed:
                self.__set_failed(results)
            #
            self.__set_finished(self._status, results)

    @staticmethod
    def get_is_busy():
        return len(TrdCommandPool.STACK) >= TrdCommandPool.MAXIMUM

    @staticmethod
    def set_wait():
        TrdCommandPool.LOCK.acquire()
        # lock
        if len(TrdCommandPool.STACK) >= TrdCommandPool.MAXIMUM:
            TrdCommandPool.LOCK.release()
            TrdCommandPool.EVENT.wait()
        else:
            TrdCommandPool.LOCK.release()

    @staticmethod
    def set_start(cmd, index=0):
        TrdCommandPool.LOCK.acquire()
        t = TrdCommandPool(cmd, index)
        TrdCommandPool.STACK.append(t)
        TrdCommandPool.LOCK.release()
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


class TrdCommand(threading.Thread):
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
        self.__status_changed_signal = TrdSignal(int)
        self._logging_signal = TrdSignal(str)
        #
        self.__completed_signal = TrdSignal(tuple)
        self.__failed_signal = TrdSignal(tuple)
        self.__finished_signal = TrdSignal(tuple)

    def __set_status_update(self, status):
        self._status = status
        self.__status_changed_signal.send_emit(
            status
        )

    def __set_completed(self, results):
        self.__completed_signal.send_emit(
            (self._status, ''.join(results))
        )

    def __set_failed(self, results):
        self.__failed_signal.send_emit(
            (self._status, ''.join(results))
        )

    def __set_finished(self, results):
        self.__finished_signal.send_emit(
            (self._status, ''.join(results))
        )

    def __set_logging(self, text):
        self._logging_signal.send_emit(
            text
        )

    @property
    def status_changed(self):
        return self.__status_changed_signal

    @property
    def completed(self):
        return self.__completed_signal

    @property
    def failed(self):
        return self.__failed_signal

    @property
    def finished(self):
        return self.__finished_signal

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

        self.__status_changed_signal = TrdSignal(int, int)
        self.__completed_signal = TrdSignal(int, list)
        self.__failed_signal = TrdSignal(int, list)
        self.__finished_signal = TrdSignal(int, int, list)

    @property
    def status_changed(self):
        return self.__status_changed_signal

    @property
    def completed(self):
        return self.__completed_signal

    @property
    def failed(self):
        return self.__failed_signal

    @property
    def finished(self):
        return self.__finished_signal

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
        self.__completed_signal.send_emit(
            self._index, results
        )

    def __set_failed(self, results):
        self.__failed_signal.send_emit(
            self._index, results
        )

    def __set_finished(self, status, results):
        self.__finished_signal.send_emit(
            self._index, status, results
        )

    def __set_status_update(self, status):
        self._status = status
        self.__status_changed_signal.send_emit(
            self._index, status
        )

    def get_status(self):
        return self._status


class TrdFunction(TrdMethod):
    MAXIMUM = 6

    def __init__(self, fnc, index, *args, **kwargs):
        super(TrdFunction, self).__init__(fnc, index, *args, **kwargs)


class TrdFncsChainPool(object):
    class Trd(threading.Thread):
        def __init__(self, index, fnc):
            threading.Thread.__init__(self)
            self._index = index
            self._fnc = fnc

            self.__started_signal = TrdSignal()
            self.__finished_signal = TrdSignal()
            self.__failed_signal = TrdSignal(str)

            self._is_kill = False

        def run(self):
            if self._is_kill is True:
                return

            self.__started()
            # noinspection PyBroadException
            try:
                self._fnc()
            except Exception:
                import traceback
                self.__failed(
                    traceback.format_exc()
                )
            finally:
                self.__finished()

        def __started(self):
            if self._is_kill is True:
                return

            self.__started_signal.send_emit()

        def connect_started_to(self, fnc):
            self.__started_signal.connect_to(fnc)

        def __finished(self):
            if self._is_kill is True:
                return

            self.__finished_signal.send_emit()

        def connect_finished_to(self, fnc):
            self.__finished_signal.connect_to(fnc)

        def __failed(self, text):
            if self._is_kill is True:
                return
            self.__failed_signal.send_emit(text)

        def connect_failed_to(self, fnc):
            self.__failed_signal.connect_to(fnc)

        @classmethod
        def start_loop(cls, threads):
            t_cur = None
            for i_t in threads:
                if t_cur is not None:
                    t_cur.connect_finished_to(i_t.start)
                t_cur = i_t

            threads[0].start()

        def set_kill(self):
            self._is_kill = True

    def __init__(self):
        self._threads = []
        self._next_fncs = []
        self._maximum = 0

        self._all_finish_signal = TrdSignal(int)

    def add_next_fnc(self, fnc):
        self._next_fncs.append(fnc)

    def create_one(self, fnc):
        index = len(self._threads)
        thread = TrdFncsChainPool.Trd(
            index, fnc
        )
        thread.connect_finished_to(
            functools.partial(self.__update_finish, index)
        )
        self._threads.append(thread)
        return thread

    def start_all(self):
        t_cur = None
        self._maximum = len(self._threads)-1
        for i_t in self._threads:
            if t_cur is not None:
                t_cur.connect_finished_to(i_t.start)
            t_cur = i_t

        self._threads[0].start()

    def kill_all(self):
        for i_index, i in enumerate(self._threads):
            i.set_kill()
            del self._threads[i_index]

    def __update_finish(self, index):
        if index == self._maximum:
            self._all_finish_signal.send_emit()

    def connect_all_finish_to(self, fnc):
        self._all_finish_signal.connect_to(fnc)


class TrdFncProcessing(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__is_killed = False
        self.__started_signal = TrdSignal(object)
        self.__finished_signal = TrdSignal()
        self.__failed_signal = TrdSignal(str)
        self.__start_processing_signal = TrdSignal(int)
        self.__update_processing_signal = TrdSignal()
        self.__update_logging_signal = TrdSignal(str)

    def connect_started_to(self, fnc):
        self.__started_signal.connect_to(fnc)

    def __started(self):
        if self.__is_killed is True:
            return
        self.__started_signal.send_emit()

    def connect_finished_to(self, fnc):
        self.__finished_signal.connect_to(fnc)

    def __finished(self):
        if self.__is_killed is True:
            return
        self.__finished_signal.send_emit()

    def connect_failed_to(self, fnc):
        self.__failed_signal.connect_to(fnc)

    def __failed(self, text):
        if self.__is_killed is True:
            return
        self.__failed_signal.send_emit(text)

    def connect_start_processing_to(self, fnc):
        self.__start_processing_signal.connect_to(fnc)

    def start_processing(self, maximum):
        if self.__is_killed is True:
            return
        self.__start_processing_signal.send_emit(maximum)

    def connect_update_processing_to(self, fnc):
        self.__update_processing_signal.connect_to(fnc)
    
    def update_processing(self):
        if self.__is_killed is True:
            return
        self.__update_processing_signal.send_emit()

    def connect_update_logging_to(self, fnc):
        self.__update_logging_signal.connect_to(fnc)

    def update_logging(self, text):
        if self.__is_killed is True:
            return
        self.__update_logging_signal.send_emit(text)

    def kill(self):
        self.__is_killed = True

    def get_is_killed(self):
        return self.__is_killed

    def run(self):
        # noinspection PyBroadException
        try:
            self.__started()
        except Exception:
            import traceback
            self.__failed(
                traceback.format_exc()
            )
        finally:
            self.__finished()


