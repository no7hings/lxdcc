# coding:utf-8
# noinspection PyUnresolvedReferences
from Katana import Utils, Configuration, NodegraphAPI


def _get_is_ui_mode_():
    return Configuration.get('KATANA_UI_MODE') == '1'


def set_undo_mark_mdf(method):
    def sub_method(*args, **kwargs):
        Utils.UndoStack.OpenGroup(method.__name__)
        # noinspection PyBroadException
        try:
            _method = method(*args, **kwargs)
            return _method
        except Exception:
            if _get_is_ui_mode_() is True:
                from lxutil import utl_core
                utl_core.ExceptionCatcher.set_create()
            else:
                from lxbasic import bsc_core
                bsc_core.ExceptionMtd.set_print()
            raise
        #
        finally:
            Utils.UndoStack.CloseGroup()
    return sub_method
