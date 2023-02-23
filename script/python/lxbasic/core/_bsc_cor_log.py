# coding:utf-8
from __future__ import print_function

from lxbasic.core._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_raw, _bsc_cor_pattern


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
        return text
    @classmethod
    def trace_warning(cls, text):
        sys.stdout.write(
            cls.get_warning(text+'\n')
        )
        return text
    @classmethod
    def trace_error(cls, text):
        sys.stdout.write(
            cls.get_error(text+'\n')
        )
        return text
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
        """
        :param name: str/unicode
        :param text: str/unicode
        :return:
        """
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


class LogProgress(object):
    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)
    @classmethod
    def create_as_bar(cls, *args, **kwargs):
        kwargs['use_as_progress_bar'] = True
        return cls.create(*args, **kwargs)

    def __init__(self, maximum, label, use_as_progress_bar=False):
        self._maximum = maximum
        self._value = 0
        self._label = label
        self._use_as_progress_bar = use_as_progress_bar
        #
        self._start_timestamp = TimeMtd.get_timestamp()
        self._pre_timestamp = TimeMtd.get_timestamp()
        #
        self._p = 0
        #
        LogMtd.trace_method_result(
            self._label,
            'is started'
        )

    def set_update(self, sub_label=None):
        self._value += 1
        cur_timestamp = TimeMtd.get_timestamp()
        cost_timestamp = cur_timestamp - self._pre_timestamp
        self._pre_timestamp = cur_timestamp
        #
        percent = float(self._value) / float(self._maximum)
        # trace when value is integer
        p = '%3d' % (int(percent*100))
        if self._p != p:
            self._p = p
            if self._use_as_progress_bar is True:
                LogMtd.trace_method_result(
                    u'{}'.format(self._label),
                    u'is running {} {}%, cost time {}'.format(
                        self._get_progress_bar_string_(percent),
                        p,
                        _bsc_cor_raw.RawIntegerMtd.second_to_time_prettify(cost_timestamp),

                    )
                )
            else:
                LogMtd.trace_method_result(
                    u'{}'.format(self._label),
                    u'is running {}%, cost time {}'.format(
                        p,
                        _bsc_cor_raw.RawIntegerMtd.second_to_time_prettify(cost_timestamp),
                    )
                )
    @classmethod
    def _get_progress_bar_string_(cls, percent):
        c = 20
        p = int(percent*c)
        p = max(p, 1)
        return u'{}{}'.format(
            p*u'■', (c-p)*u'□'
        )

    def set_stop(self):
        self._value = 0
        self._maximum = 0
        #
        cost_timestamp = TimeMtd.get_timestamp() - self._start_timestamp
        LogMtd.trace_method_result(
            self._label,
            'is completed, cost time {}'.format(
                _bsc_cor_raw.RawIntegerMtd.second_to_time_prettify(cost_timestamp),
            )
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.set_stop()


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

    c = 100
    with LogProgress.create_as_bar(maximum=c, label='test') as l_p:
        for i in range(c):
            l_p.set_update()

