# coding:utf-8
from __future__ import print_function

from lxbasic.core._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_raw, _bsc_cor_pattern


class LogMtd(object):
    DEFAULT_CODING = sys.getdefaultencoding()
    #
    SystemMtd.trace(
        'logger is initialization, default coding is "{}"'.format(DEFAULT_CODING)
    )
    ENABLE = True
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    #
    DEBUG = False
    TEST = False
    TIMESTAMP = None
    TIMESTAMP_CACHE = dict()

    LEVEL = 3

    @classmethod
    def get_time(cls):
        return time.strftime(cls.TIME_FORMAT, time.localtime(time.time()))

    @classmethod
    def get(cls, text):
        text = _bsc_cor_raw.auto_encode(text)
        return '{} {}'.format(cls.get_time(), text)

    #
    @classmethod
    def get_result(cls, text):
        text = _bsc_cor_raw.auto_encode(text)
        return cls.get('''        | {}'''.format(text))

    @classmethod
    def get_warning(cls, text):
        text = _bsc_cor_raw.auto_encode(text)
        return cls.get('''warning | {}'''.format(text))

    @classmethod
    def get_error(cls, text):
        text = _bsc_cor_raw.auto_encode(text)
        return cls.get('''  error | {}'''.format(text))

    @classmethod
    def get_debug(cls, text):
        text = _bsc_cor_raw.auto_encode(text)
        return cls.get('''  debug | {}'''.format(text))

    @classmethod
    def get_test(cls, text):
        text = _bsc_cor_raw.auto_encode(text)
        return cls.get('''   test | {}'''.format(text))

    @classmethod
    def result(cls, text):
        if cls.ENABLE is True:
            sys.stdout.write(text+'\n')

    @classmethod
    def error(cls, text):
        if cls.ENABLE is True:
            sys.stderr.write(text+'\n')

    @classmethod
    def trace_result(cls, text):
        if cls.ENABLE is True:
            sys.stdout.write(
                cls.get_result(text+'\n')
            )
            return text

    @classmethod
    def trace_warning(cls, text):
        if cls.ENABLE is True:
            sys.stdout.write(
                cls.get_warning(text+'\n')
            )
            return text

    @classmethod
    def trace_error(cls, text):
        if cls.ENABLE is True:
            sys.stderr.write(
                cls.get_error(text+'\n')
            )
            return text

    #
    @classmethod
    def get_method_result(cls, name, *args):
        name = _bsc_cor_raw.auto_encode(name)
        text = ''.join(_bsc_cor_raw.auto_encode(i) for i in args)
        return cls.get_result(
            '<{}> {}'.format(name, text)
        )

    @classmethod
    def get_method_warning(cls, name, *args):
        name = _bsc_cor_raw.auto_encode(name)
        text = ''.join(_bsc_cor_raw.auto_encode(i) for i in args)
        return cls.get_warning(
            '<{}> {}'.format(name, text)
        )

    @classmethod
    def get_method_error(cls, name, *args):
        """
        :param name: str/unicode
        :param args: str/unicode, ...
        :return:
        """
        name = _bsc_cor_raw.auto_encode(name)
        text = ''.join(_bsc_cor_raw.auto_encode(i) for i in args)
        return cls.get_error(
            '<{}> {}'.format(name, text)
        )

    #
    @classmethod
    def trace_method_result(cls, name, *args):
        """
        :param name: str/unicode
        :param args: str/unicode, ...
        :return:
        """
        if cls.ENABLE is True:
            name = _bsc_cor_raw.auto_encode(name)
            text = ''.join(_bsc_cor_raw.auto_encode(i) for i in args)
            return cls.trace_result(
                '<{}> {}'.format(name, text)
            )

    @classmethod
    def trace_method_warning(cls, name, *args):
        if cls.ENABLE is True:
            name = _bsc_cor_raw.auto_encode(name)
            text = ''.join(_bsc_cor_raw.auto_encode(i) for i in args)
            return cls.trace_warning(
                '<{}> {}'.format(name, text)
            )

    @classmethod
    def trace_method_error(cls, name, *args):
        if cls.ENABLE is True:
            name = _bsc_cor_raw.auto_encode(name)
            text = ''.join(_bsc_cor_raw.auto_encode(i) for i in args)
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

    @classmethod
    def debug(cls, text):
        if cls.DEBUG is True:
            sys.stdout.write(
                cls.get_debug(text+'\n')
            )
            return text

    @classmethod
    def debug_method(cls, name, *args):
        if cls.DEBUG is True:
            name = _bsc_cor_raw.auto_encode(name)
            text = ''.join(_bsc_cor_raw.auto_encode(i) for i in args)
            return cls.debug(
                '<{}> {}'.format(name, text)
            )

    @classmethod
    def test_start(cls, text):
        if cls.TEST is True:
            cls.TIMESTAMP_CACHE[text] = time.time()
            #
            sys.stdout.write(
                cls.get_test(text+' is start'+'\n')
            )
            return text

    @classmethod
    def test_end(cls, text):
        if cls.TEST is True:
            time_pre = cls.TIMESTAMP_CACHE.get(text)
            if time_pre:
                t = time.time()
                sys.stdout.write(
                    cls.get_test(text+' is end '+'cost: {}s\n'.format(t-time_pre))
                )
            else:
                sys.stdout.write(
                    cls.get_test(text+' is end'+'\n')
                )
            return text

    @classmethod
    def filter_process_start(cls, text):
        """
        print LogMtd.filter_process_start(
            '2023-09-13 15:25:20         | <test> process is started, total is 20'
        )
        """
        p = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\|\s<(.*)> process is started, total is (\d+)'
        m = re.search(p, text)
        if m:
            _time = m.group(1)
            _keyword = m.group(2)
            _count = int(m.group(3))
            return _time, _keyword, _count

    @classmethod
    def filter_process(cls, text):
        """
        print LogMtd.filter_process(
            '2023-09-13 15:50:27         | <test> ■□□□□□□□□□□□□□□□□□□□   10%, cost time 00:00:00.5006'
        )
        """
        p = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\|\s<(.*)>.*\s(\d+)\%, cost time (\d+)'
        m = re.search(p, text)
        if m:
            _time = m.group(1)
            _keyword = m.group(2)
            _percent = m.group(3)
            return _time, _keyword, _percent

    @classmethod
    def filter_result(cls, text):
        """
        print LogMtd.filter_result(
            '2023-09-13 15:25:20         | process is started, total is 20'
        )
        """
        p = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\|\s(.*)'
        m = re.search(p, text)
        if m:
            _time = m.group(1)
            _content = m.group(2)
            return _time, _content


class LogProgress(object):
    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @classmethod
    def create_as_bar(cls, *args, **kwargs):
        kwargs['use_as_progress_bar'] = True
        return cls.create(*args, **kwargs)

    def __init__(self, maximum, label, use_as_progress_bar=False):
        self.__maximum = maximum
        self.__value = 0
        self.__label = label
        self._use_as_progress_bar = use_as_progress_bar
        #
        self._start_timestamp = TimeMtd.get_timestamp()
        self._pre_timestamp = TimeMtd.get_timestamp()
        #
        self._p = 0
        #
        LogMtd.trace_method_result(
            self.__label,
            'process is started, total is {}'.format(self.__maximum)
        )

    def set_update(self, sub_label=None):
        self.__value += 1
        cur_timestamp = TimeMtd.get_timestamp()
        cost_timestamp = cur_timestamp-self._pre_timestamp
        self._pre_timestamp = cur_timestamp
        #
        percent = float(self.__value)/float(self.__maximum)
        # trace when value is integer
        p = '%3d'%(int(percent*100))
        # if self._p != p:
        #     self._p = p
        if self._use_as_progress_bar is True:
            LogMtd.trace_method_result(
                '{}'.format(self.__label),
                '{} {}%, cost time {}'.format(
                    self._get_progress_bar_string_(percent),
                    p,
                    _bsc_cor_raw.RawIntegerMtd.second_to_time_prettify(cost_timestamp),

                )
            )
        else:
            LogMtd.trace_method_result(
                '{}'.format(self.__label),
                '{}%, cost time {}'.format(
                    p,
                    _bsc_cor_raw.RawIntegerMtd.second_to_time_prettify(cost_timestamp),
                )
            )

    @classmethod
    def _get_progress_bar_string_(cls, percent):
        c = 20
        p = int(percent*c)
        p = max(p, 1)
        return '{}{}'.format(
            p*'■', (c-p)*'□'
        )

    def set_stop(self):
        self.__value = 0
        self.__maximum = 0
        #
        cost_timestamp = TimeMtd.get_timestamp()-self._start_timestamp
        LogMtd.trace_method_result(
            self.__label,
            'process is completed, cost time {}'.format(
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

    LogMtd.result('Test')
    LogMtd.result(u'测试 0')
    #
    LogMtd.trace_result(u'测试 1')
    LogMtd.trace_warning(u'测试 2')
    LogMtd.trace_error(u'测试 3')
    LogMtd.debug('Test')

    LogMtd.trace_method_error(u'测试', u'测试')

    print(
        LogMtd.find_all(
            '''
    2023-02-02 18:02:04 Test
    2023-02-02 18:02:04 测试 0
    2023-02-02 18:02:04         | 测试 1
    2023-02-02 18:02:04 warning | 测试 2
    2023-02-02 18:02:04  error  | 测试 3
    2023-02-02 18:02:04  error  | <测试> 测试
            '''
        )
    )

    # c = 100
    # with LogProgress.create_as_bar(maximum=c, label='test') as l_p:
    #     for _i in range(c):
    #         l_p.set_update()
