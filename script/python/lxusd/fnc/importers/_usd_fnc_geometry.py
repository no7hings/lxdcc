# coding:utf-8
from lxusd.warp import *

from lxusd.fnc import usd_fnc_abstract


class GeometryImporter(usd_fnc_abstract.AbsUsdScene):
    def __init__(self, file_path, root=None, option=None):
        super(GeometryImporter, self).__init__(file_path, root)
        self._usd_stage = self._set_stage_create_()
        self._set_reference_add_(self._usd_stage, self._file_path, self._root)

    def get_path_by_face_vertices_uuid_dict(self):
        for prim in self._usd_stage.TraverseAll():
            pass
