# coding:utf-8
from lxutil.fnc import utl_fnc_obj_abs

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


class SceneExporter(utl_fnc_obj_abs.AbsDccExporter):
    OPTION = {}
    def __init__(self, file_path, root=None, option=None):
        super(SceneExporter, self).__init__(file_path, root, option)

    def set_run(self):
        ktn_dcc_objects.Scene.set_file_export_to(
            self._file_path
        )
