# coding:utf-8
from lxbasic import bsc_core


def set_method_exception_catch(method):
    def sub_method(*args, **kwargs):
        # noinspection PyBroadException
        try:
            _method = method(*args, **kwargs)
            return _method
        except:
            from lxutil import utl_core
            #
            utl_core.ExceptionCatcher.set_create()
            raise
    return sub_method


def set_ignore_run(fnc):
    def fnc_(*args, **kw):
        # noinspection PyBroadException
        try:
            return fnc(*args, **kw)
        except:
            bsc_core.ExceptionMtd.set_print()
    return fnc_

