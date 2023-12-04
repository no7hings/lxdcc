# coding:utf-8
import lxlog.core as log_core


Log = log_core.Log

LogContext = log_core.LogContext

LogProcessContext = log_core.LogProcessContext

LogException = log_core.LogException


if __name__ == '__main__':
    print(Log.get('Test'))
    print(Log.get(u'测试'))
    print(Log.get_result(u'测试'))

    Log.result('Test')
    Log.result(u'测试 0')
    #
    Log.trace_result(u'测试 1')
    Log.trace_warning(u'测试 2')
    Log.trace_error(u'测试 3')
    Log.debug('Test')

    Log.trace_method_error(u'测试', u'测试')

    c = 100
    with LogProcessContext.create_as_bar(maximum=c, label='test') as l_p:
        for _i in range(c):
            l_p.do_update()
