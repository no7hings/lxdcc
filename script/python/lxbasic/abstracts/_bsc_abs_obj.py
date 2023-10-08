# coding:utf-8
import six

import fnmatch

import parse

import subprocess

from lxbasic import bsc_configure


class AbsFileReader(object):
    SEP = '\n'
    LINE_MATCHER_CLS = None
    PROPERTIES_CLS = None

    def __init__(self, file_path):
        self._file_path = file_path
        self._set_line_raw_update_()

    def _set_line_raw_update_(self):
        self._lines = []
        if self._file_path is not None:
            with open(self._file_path) as f:
                raw = f.read()
                sep = self.SEP
                self._lines = self._get_lines_(raw, sep)

    @classmethod
    def _get_lines_(cls, raw, sep):
        return [r'{}{}'.format(i, sep) for i in raw.split(sep)]

    @property
    def file_path(self):
        return self._file_path

    def get_lines(self):
        return self._lines

    lines = property(get_lines)

    @classmethod
    def _get_matches_(cls, pattern, lines):
        lis = []
        pattern_0 = cls.LINE_MATCHER_CLS(pattern)
        lines = fnmatch.filter(
            lines, pattern_0.pattern
        )
        for line in lines:
            p = parse.parse(
                pattern_0.format, line, case_sensitive=True
            )
            if p:
                variants = p.named
                lis.append((line, variants))
        #
        return lis


class AbsProcess(object):
    LOGGER = None
    #
    Status = bsc_configure.Status
    SubProcessStatus = bsc_configure.SubProcessStatus

    def __init__(self, *args, **kwargs):
        self._name = 'unknown'
        self._status = self.Status.Started
        self._elements = []
        self._thread_maximum = 10
        self._sub_process = None

    def __set_running_(self, sub_process=None):
        if sub_process is not None:
            self._sub_process = sub_process
        #
        self.__set_status_(self.Status.Running)

    def __set_waiting_(self):
        self.__set_status_(self.Status.Waiting)

    def __set_processing_(self):
        if self._status is self.Status.Waiting:
            result = self._set_sub_process_create_fnc_()
            if result is None:
                self.__set_waiting_()
            else:
                self.__set_running_(result)

    def __set_completed_(self):
        self.__set_status_(self.Status.Completed)
        self._set_finished_fnc_run_()

    def __set_failed_(self):
        self.__set_status_(self.Status.Failed)
        self._set_finished_fnc_run_()

    def _set_sub_process_create_fnc_(self):
        raise NotImplementedError()

    def _set_finished_fnc_run_(self):
        raise NotImplementedError()

    def __get_is_completed_(self):
        sp = self._sub_process
        if isinstance(sp, subprocess.Popen):
            if sp.poll() is self.SubProcessStatus.Completed:
                return True
            elif sp.poll() is self.SubProcessStatus.Failed:
                self.__set_failed_()
            elif sp.poll() is self.SubProcessStatus.Error:
                self.__set_error_occurred_()
            return False
        elif isinstance(sp, bool):
            return sp

    def __get_elements_is_completed_(self):
        elements = self.get_elements()
        count = len(elements)
        return [i_element.get_status() for i_element in elements] == count*[bsc_configure.Status.Completed]

    def __get_elements_status_(self):
        pass

    def __set_status_update_(self):
        pre_status = self._status
        if pre_status != self.Status.Completed:
            if self.get_elements():
                elements = self.get_elements()
                #
                [i_element.__set_processing_() for i_element in elements]
                #
                if self.__get_elements_is_completed_() is True:
                    self.__set_completed_()
            else:
                self.__set_processing_()
                if self.__get_is_completed_() is True:
                    self.__set_completed_()

    def set_name(self, text):
        self._name = text

    def get_name(self):
        return self._name

    def __set_status_(self, status):
        pre_status = self._status
        if pre_status != status:
            self._status = status
            if self.LOGGER is not None:
                self.LOGGER.set_module_result_trace(
                    'process-status changed',
                    '"{}" status is change to "{}"'.format(
                        self._name,
                        str(self._status)
                    )
                )

    def __set_error_occurred_(self):
        self._status = self.Status.Error
        if self.LOGGER is not None:
            self.LOGGER.set_module_error_trace(
                'process-error-occurred',
                '"{}" status is change to "{}"'.format(
                    self._name,
                    str(self._status)
                )
            )

    def set_start(self):
        if self.get_elements():
            self.__set_running_()
            [i_element.set_start() for i_element in self.get_elements()]
        else:
            result = self._set_sub_process_create_fnc_()
            if result is None:
                self.__set_waiting_()
            else:
                self.__set_running_(result)

    def add_element(self, element):
        self._elements.append(element)

    def get_elements(self):
        return self._elements

    def get_is_completed(self):
        return self._status is self.Status.Completed

    def get_status(self):
        self.__set_status_update_()
        return self._status

    def set_thread_maximum(self, maximum):
        self._thread_maximum = maximum
