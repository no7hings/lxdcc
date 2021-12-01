# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds


def set_undo_mark_mdf(method):
    def sub_method(*args, **kwargs):
        cmds.undoInfo(openChunk=1, undoName=method.__name__)
        # noinspection PyBroadException
        try:
            _method = method(*args, **kwargs)
            return _method
        except Exception:
            from lxutil import utl_core
            utl_core.ExceptionCatcher.set_create()
            raise
        #
        finally:
            cmds.undoInfo(closeChunk=1, undoName=method.__name__)
    return sub_method
