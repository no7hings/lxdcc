# coding:utf-8
from lxutil.fnc import utl_fnc_obj_abs

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


class FncSceneExporter(utl_fnc_obj_abs.AbsFncOptionBase):
    OPTION = dict(
        file=''
    )

    def __init__(self, option=None):
        super(FncSceneExporter, self).__init__(option)

    def execute(self):
        ktn_dcc_objects.Scene.set_file_export_to(
            self.get('file')
        )
