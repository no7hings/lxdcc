# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

from lxbasic import bsc_core


class Modifier(object):
    @staticmethod
    def undo_run(fnc):
        def sub_fnc_(*args, **kwargs):
            cmds.undoInfo(openChunk=1, undoName=fnc.__name__)
            # noinspection PyBroadException
            try:
                _method = fnc(*args, **kwargs)
                return _method
            except Exception:
                from lxbasic import bsc_core
                bsc_core.ExceptionMtd.set_print()
            #
            finally:
                cmds.undoInfo(closeChunk=1, undoName=fnc.__name__)

        return sub_fnc_
    @staticmethod
    def undo_debug_run(fnc):
        def sub_fnc_(*args, **kwargs):
            cmds.undoInfo(openChunk=1, undoName=fnc.__name__)
            # noinspection PyBroadException
            try:
                _method = fnc(*args, **kwargs)
                return _method
            except Exception:
                from lxutil import utl_core
                is_ui_mode = not cmds.about(batch=1)
                utl_core.ExceptionCatcher.set_create(use_window=is_ui_mode)
                raise
            #
            finally:
                cmds.undoInfo(closeChunk=1, undoName=fnc.__name__)

        return sub_fnc_


class CallbackOpt(object):
    def __init__(self, function, callback_type):
        self._function = function
        self._callback_type = callback_type

    def register(self):
        _index = cmds.scriptJob(
            parent='modelPanel4', event=[self._callback_type, self._function]
        )
        bsc_core.LogMtd.trace_method_result(
            'callback',
            'add as "{}" at "{}"'.format(self._callback_type, _index)
        )

    def deregister(self):
        pass

