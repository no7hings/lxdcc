# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)

    def set_check_run(self):
        pass
