# coding:utf-8
# noinspection PyUnresolvedReferences
from pxr import Usd, Sdf, Vt, UsdGeom


class Usd2Usda(object):
    def __init__(self, file_path, option=None):
        self._file_path = file_path
        #
        self._stage = Usd.Stage.Open(self._file_path)
        import os
        base, ext = os.path.splitext(self._file_path)
        self._stage.Export(base + '.usda')
