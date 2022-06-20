# coding:utf-8
import collections
import functools

import re

import os

import threading

from lxbasic import bsc_configure, bsc_core

THREAD_MAXIMUM = threading.Semaphore(1024)


class StrCamelcase(object):
    def __init__(self, string):
        self._string = string

    def to_prettify(self):
        return ' '.join([i.capitalize() for i in re.findall(r'[a-zA-Z][a-z]*[0-9]*', self._string)])

    def to_underline(self):
        return re.sub(re.compile(r'([a-z]|\d)([A-Z])'), r'\1_\2', self._string).lower()


class StrUnderline(object):
    def __init__(self, string):
        self._string = string

    def to_prettify(self):
        return ' '.join([i.capitalize() for i in self._string.split('_')])

    def to_camelcase(self):
        return re.sub(r'_(\w)', lambda x: x.group(1).upper(), self._string)


class String(object):
    def __init__(self, string):
        self._string = string


class SignalInstance(object):
    def __init__(self, *args, **kwargs):
        self._methods = []

    def set_connect_to(self, method):
        self._methods.append(method)

    def set_emit_send(self, *args, **kwargs):
        if self._methods:
            for i in self._methods:
                print i
                i(*args, **kwargs)
            # THREAD_MAXIMUM.acquire()
            # #
            # ts = [threading.Thread(target=i_method, args=args, kwargs=kwargs) for i_method in self._methods]
            # for t in ts:
            #     t.start()
            # for t in ts:
            #     t.join()
            # #
            # THREAD_MAXIMUM.release()

    def get_methods(self):
        return self._methods


class ProcessMonitor(object):
    Status = bsc_configure.Status
    def __init__(self, process):
        self._process = process
        self._name = process.get_name()
        self._elements = process.get_elements()
        #
        self._time_interval = .5
        self._processing_time_cost = 0
        self._running_time_cost = 0
        self._waiting_time_cost = 0
        self._processing_time_maximum = 3600
        self._running_time_maximum = 3600
        self._waiting_time_maximum = 3600
        #
        self._is_disable = True
        #
        self._timer = None
        self._status = self.Status.Stopped
        self._rate_statuses = [self.Status.Stopped]*len(self._elements)
        #
        self.logging = SignalInstance(str)
        self.status_changed = SignalInstance(int)
        self.element_statuses_changed = SignalInstance(int)
        self.started = SignalInstance()
        self.waiting = SignalInstance(int)
        self.running = SignalInstance(int)
        self.processing = SignalInstance(int)
        self.suspended = SignalInstance()
        self.completed = SignalInstance()
        self.failed = SignalInstance()
        self.stopped = SignalInstance()
        self.error_occurred = SignalInstance(int)
        #
        self._status_update_methods = [
            # Unknown = 0
            self.__set_stopped_,
            # Started = 1
            self.__set_started_,
            # Running = 2
            self.__set_running_,
            # Waiting = 3
            self.__set_waiting_,
            # Completed = 4
            self.__set_completed_,
            # Suspended = 5
            self.__set_suspended_,
            # Failed = 6
            self.__set_failed_,
            # Stopped = 7
            self.__set_stopped_,
            # Error = 8
            self.__set_error_occurred_
        ]
    #
    def __set_status_update_method_run_(self):
        return self._status_update_methods[self._process.get_status()]()
    #
    def __set_started_(self):
        self._is_disable = False
        #
        self._status = self.Status.Started
        #
        self.__set_emit_send_(self.started)
        #
        self.__set_processing_time_update_()
        #
        self.__set_logging_(
            'process-name="{}" is started'.format(
                self._name
            )
        )
    #
    def __set_emit_send_(self, signal, *args, **kwargs):
        # noinspection PyBroadException
        # signal.set_emit_send(*args, **kwargs)
        try:
            signal.set_emit_send(*args, **kwargs)
        except:
            self.__set_error_occurred_()
            raise
    # waiting
    def __set_waiting_(self):
        self._status = self.Status.Waiting
        #
        self.__set_emit_send_(self.waiting, self._waiting_time_cost)
        self.__set_emit_send_(self.processing, self._processing_time_cost)
        #
        self.__set_processing_time_update_()
        self.__set_waiting_time_update_()
    # running
    def __set_running_(self):
        self._status = self.Status.Running
        #
        self.__set_emit_send_(self.running, self._running_time_cost)
        self.__set_emit_send_(self.processing, self._processing_time_cost)
        #
        self.__set_processing_time_update_()
        self.__set_running_time_update_()
    #
    def __set_elements_running_(self):
        pre_element_status = str(self._rate_statuses)
        for index, i_element in enumerate(self._elements):
            i_element_status = i_element.get_status()
            if i_element_status is self.Status.Error:
                pass
            self._rate_statuses[index] = i_element_status
        if pre_element_status != str(self._rate_statuses):
            self.__set_element_statuses_changed_()
    #
    def __set_logging_(self, text):
        print text
        self.__set_emit_send_(self.logging, text)
    # status changed
    def __set_status_changed_(self):
        self.__set_emit_send_(self.status_changed, self._status)

    def __set_element_statuses_changed_(self):
        self.__set_emit_send_(self.element_statuses_changed, self._rate_statuses)

    def __set_suspended_(self):
        self._status = self.Status.Suspended
        #
        self.__set_emit_send_(self.suspended)
        #
        self.__set_logging_(
            'process-name="{}" is suspended'.format(
                self._name
            )
        )

    def __set_completed_(self):
        self._status = self.Status.Completed
        #
        self.__set_emit_send_(self.completed)
        #
        self.__set_logging_(
            'process-name="{}" is completed'.format(
                self._name
            )
        )

    def __set_failed_(self):
        self._is_disable = True
        #
        self._status = self.Status.Failed
        #
        self.__set_emit_send_(self.failed)
        #
        self.__set_logging_(
            'process-name="{}" is failed'.format(
                self._name
            )
        )

    def __set_stopped_(self):
        self._is_disable = True
        #
        self._status = self.Status.Stopped
        self._rate_statuses = [self.Status.Stopped]*len(self._elements)
        #
        self.__set_emit_send_(self.stopped)
        #
        self.__set_logging_(
            'process-name="{}" is stopped'.format(
                self._name
            )
        )
    #
    def __set_error_occurred_(self):
        self._is_disable = True
        #
        self._status = self.Status.Error
        #
        self.__set_logging_(
            'process-name="{}" is error'.format(
                self._name
            )
        )
    #
    def __set_run_(self):
        if self._is_disable is False:
            pre_process_status = self._status
            #
            self.__set_status_update_method_run_()
            #
            if pre_process_status != self._status:
                self.__set_status_changed_()
            #
            self.__set_elements_running_()

    def __set_processing_time_update_(self):
        self._processing_time_cost += self._time_interval
        if self._processing_time_cost >= self._processing_time_maximum:
            self.__set_logging_(
                'process-name="{}" is timeout'.format(
                    self._name
                )
            )
            self.__set_error_occurred_()
            return False
        #
        if self._timer is not None:
            self._timer.cancel()
        self._timer = threading.Timer(self._time_interval, self.__set_run_)
        self._timer.start()
        # self._timer.join()

    def __set_waiting_time_update_(self):
        self._waiting_time_cost += self._time_interval
        if self._waiting_time_cost >= self._waiting_time_maximum:
            self.__set_logging_(
                'process-name="{}" waiting is timeout'.format(
                    self._name
                )
            )
            self.__set_error_occurred_()
            return False

    def __set_running_time_update_(self):
        self._running_time_cost += self._time_interval
        if self._running_time_cost >= self._running_time_maximum:
            self.__set_logging_(
                'process-name="{}" running is timeout'.format(
                    self._name
                )
            )
            self.__set_error_occurred_()
            return False

    def get_running_time_maximum(self):
        return self._running_time_maximum

    def set_start(self):
        self.__set_started_()
        self.__set_status_changed_()

    def set_stop(self):
        self.__set_stopped_()
        #
        self.__set_status_changed_()
        self.__set_element_statuses_changed_()

    def get_is_started(self):
        return self._status == self.Status.Started

    def get_is_running(self):
        return self._status == self.Status.Running

    def get_is_completed(self):
        return self._status == self.Status.Completed

    def get_is_stopped(self):
        return self._status == self.Status.Stopped

    def get_running_time_cost(self):
        return self._running_time_cost

    def get_status(self):
        return self._status

    def get_element_statuses(self):
        return self._rate_statuses


class SubProcess(object):
    Status = bsc_configure.Status
    SubProcessStatus = bsc_configure.SubProcessStatus
    def __init__(self, cmds):
        self._cmds = cmds
        self._sp = None
        #
        self._status = self.Status.Waiting
        #
        self._status_dict = {
            self.SubProcessStatus.Unknown: self.Status.Unknown,
            self.SubProcessStatus.Running: self.Status.Running,
            self.SubProcessStatus.Completed: self.Status.Completed,
            self.SubProcessStatus.Failed: self.Status.Failed,
            self.SubProcessStatus.Stopped: self.Status.Stopped,
            #
            self.SubProcessStatus.Error: self.Status.Error,
        }

    def set_start(self):
        self._sp = bsc_core.SubProcessMtd.set_run(
            self._cmds
        )
        if self._sp is not None:
            self._status = self.Status.Started
        else:
            self._status = self.Status.Failed

    def set_update(self):
        if self._sp is not None:
            status = self._sp.poll()
            self._status = self._status_dict[
                status
            ]
        else:
            self._status = self.Status.Failed

    def get_status(self):
        return self._status

    def get_is_termination(self):
        return self._status in [
            self.Status.Completed,
            self.Status.Failed,
            self.Status.Stopped,
            self.Status.Error,
        ]

    def get_is_normal_termination(self):
        return self._status in [
            self.Status.Completed,
        ]

    def get_is_abnormal_termination(self):
        return self._status in [
            self.Status.Stopped,
            self.Status.Failed,
            self.Status.Error,
        ]


class GainSignal(object):
    def __init__(self, *args, **kwargs):
        self._methods = []

    def set_connect_to(self, method):
        self._methods.append(method)

    def set_emit_send(self, *args, **kwargs):
        if self._methods:
            THREAD_MAXIMUM.acquire()
            #
            ts = [threading.Thread(target=i_method, args=args, kwargs=kwargs) for i_method in self._methods]
            for t in ts:
                t.start()
            for t in ts:
                t.join()
            #
            THREAD_MAXIMUM.release()

    def get_methods(self):
        return self._methods


class GainThread(threading.Thread):
    def __init__(self):
        super(GainThread, self).__init__()
        #
        self.run_started = GainSignal()
        self.run_finished = GainSignal()
        #
        self._fnc = None
        #
        self._data = None
    #
    def set_fnc_(self, fnc):
        self._fnc = fnc
    #
    def set_data(self, data):
        self._data = data
        self.run_finished.set_emit_send()
    #
    def get_data(self):
        return self._data
    #
    def run(self):
        THREAD_MAXIMUM.acquire()
        self.run_started.set_emit_send()
        #
        self.set_data(
            self._fnc()
        )

        THREAD_MAXIMUM.release()


class GainThreadsRunner(object):
    def __init__(self):
        self.run_started = GainSignal()
        self.run_finished = GainSignal()
        #
        self._fncs = []
        self._results = []
        self._data = []

    def get_data(self):
        return self._data

    def set_fnc_add(self, fnc):
        self._fncs.append(fnc)
        self._results.append(0)

    def set_result_at(self, thread, index, result):
        self._results[index] = result
        self._data.extend(
            thread.get_data()
        )
        if sum(self._results) == len(self._results):
            self.run_finished.set_emit_send()

    def set_start(self):
        c = len(self._fncs)
        self.run_started.set_emit_send()
        for i in range(c):
            i_fnc = self._fncs[i]
            #
            i_t = GainThread()
            i_t.set_fnc_(i_fnc)
            i_t.run_finished.set_connect_to(
                functools.partial(self.set_result_at, i_t, i, 1)
            )
            #
            i_t.start()
            i_t.join()


class UndoFnc(object):
    def __init__(self, obj):
        self._obj = obj

    def set_redo(self):
        pass

    def set_undo(self):
        pass


class UndoGroup(object):
    def __init__(self, key):
        self._key = key

        self._keys = []
        self._fnc_dict = collections.OrderedDict()

    def set_register(self, key, fnc):
        self._keys.append(key)
        self._fnc_dict[key] = fnc

    def set_run(self):
        for k, v in self._fnc_dict.items():
            print 'undo >> "{}"'.format(k)
            v()


class UndoStack(object):
    def __init__(self, obj):
        self._obj = obj
        #
        self._keys = []
        self._fncs = []
        self._undo_index = None

        self._cur_group = None

    def set_group_open(self, key):
        print 'undo group open: "{}"'.format(key)
        self._cur_group = UndoGroup(key)
        self._keys.append(key)
        self._fncs.append(self._cur_group)
        self._undo_index = len(self._fncs) - 1

    def set_group_close(self):
        print 'undo group close: "{}"'.format(self._cur_group._key)
        self._cur_group = None

    def set_register(self, key, fnc):
        if self._cur_group is not None:
            self._cur_group.set_register(key, fnc)
        else:
            self._keys.append(key)
            self._fncs.append(fnc)
            self._undo_index = len(self._fncs)-1

    def set_redo(self):
        pass

    def set_undo(self):
        if self._fncs and self._undo_index is not None:
            print self._undo_index
            if self._undo_index > 0:
                self._undo_index -= 1
                key = self._keys[self._undo_index]
                fnc = self._fncs[self._undo_index]
                if isinstance(fnc, UndoGroup):
                    print 'undo group >> "{}"'.format(key)
                    fnc.set_run()
                else:
                    print 'undo >> "{}"'.format(key)
                    fnc()
