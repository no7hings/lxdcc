# coding:utf-8
from lxutil.fnc import utl_fnc_obj_abs


class GeometryUsdImporter(utl_fnc_obj_abs.AbsFncOptionMethod):
    OPTION = dict(
        file='',
        root='',
        hou_location='',
    )
    def __init__(self, option):
        super(GeometryUsdImporter, self).__init__(option)

    def set_run(self):
        pass
