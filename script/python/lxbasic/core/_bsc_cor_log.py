# coding:utf-8
from __future__ import print_function

import six

import sys

import time

import fnmatch

from lxbasic.core import _bsc_cor_pattern


class LogMtd(object):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    @classmethod
    def get_time(cls):
        return time.strftime(cls.TIME_FORMAT, time.localtime(time.time()))
    @classmethod
    def get(cls, text):
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        return '{} {}'.format(cls.get_time(), text)
    #
    @classmethod
    def get_result(cls, text):
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        return cls.get('''        | {}'''.format(text))
    @classmethod
    def get_warning(cls, text):
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        return cls.get('''warning | {}'''.format(text))
    @classmethod
    def get_error(cls, text):
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        return cls.get(''' error  | {}'''.format(text))
    #
    @classmethod
    def trace(cls, text):
        sys.stdout.write(
            cls.get(text+'\n')
        )
    #
    @classmethod
    def trace_result(cls, text):
        sys.stdout.write(
            cls.get_result(text+'\n')
        )
    @classmethod
    def trace_warning(cls, text):
        sys.stdout.write(
            cls.get_warning(text+'\n')
        )
    @classmethod
    def trace_error(cls, text):
        sys.stdout.write(
            cls.get_error(text+'\n')
        )
    #
    @classmethod
    def get_method_result(cls, name, text):
        if isinstance(name, six.text_type):
            name = name.encode('utf-8')
        #
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        #
        return cls.get_result(
            '<{}> {}'.format(name, text)
        )
    @classmethod
    def get_method_warning(cls, name, text):
        if isinstance(name, six.text_type):
            name = name.encode('utf-8')
        #
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        #
        return cls.get_warning(
            '<{}> {}'.format(name, text)
        )
    @classmethod
    def get_method_error(cls, name, text):
        if isinstance(name, six.text_type):
            name = name.encode('utf-8')
        #
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        #
        return cls.get_error(
            '<{}> {}'.format(name, text)
        )
    #
    @classmethod
    def trace_method_result(cls, name, text):
        if isinstance(name, six.text_type):
            name = name.encode('utf-8')
        #
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        #
        return cls.trace_result(
            '<{}> {}'.format(name, text)
        )
    @classmethod
    def trace_method_warning(cls, name, text):
        if isinstance(name, six.text_type):
            name = name.encode('utf-8')
        #
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        #
        return cls.trace_warning(
            '<{}> {}'.format(name, text)
        )
    @classmethod
    def trace_method_error(cls, name, text):
        if isinstance(name, six.text_type):
            name = name.encode('utf-8')
        #
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        #
        return cls.trace_error(
            '<{}> {}'.format(name, text)
        )
    @classmethod
    def find_all(cls, text):
        p = _bsc_cor_pattern.PtnParseOpt(
            (
                '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
                ' [0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
                ' {status} | {content}'
            )
        )
        ts = text.split('\n')
        lines = fnmatch.filter(
            ts, p.fnmatch_pattern
        )
        return '\n'.join(lines)


if __name__ == '__main__':
    print(LogMtd.get('Test'))
    print(LogMtd.get(u'测试'))
    print(LogMtd.get_result(u'测试'))

    LogMtd.trace('Test')
    LogMtd.trace(u'测试 0')
    #
    LogMtd.trace_result(u'测试 1')
    LogMtd.trace_warning(u'测试 2')
    LogMtd.trace_error(u'测试 3')

    LogMtd.trace_method_error(u'测试', u'测试')

    print(LogMtd.find_all(
        '''
2023-02-02 18:02:04 Test
2023-02-02 18:02:04 测试 0
2023-02-02 18:02:04         | 测试 1
2023-02-02 18:02:04 warning | 测试 2
2023-02-02 18:02:04  error  | 测试 3
2023-02-02 18:02:04  error  | <测试> 测试
        '''
    ))

