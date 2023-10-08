# coding:utf-8
from lxmaya import ma_core

from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_objs

import lxutil.dcc.dcc_objects as utl_dcc_objects


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # file exists
    def _check_method_0(self, *args):
        raise RuntimeError(
            'this method is removed'
        )

    def _repair_method_0(self, *args):
        pass

    def set_check_run(self):
        raise RuntimeError(
            'this method is removed'
        )
