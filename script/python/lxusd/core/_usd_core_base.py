# coding:utf-8
# noinspection PyUnresolvedReferences
from pxr import Usd, UsdShade, Sdf, UsdGeom, Gf

import six


class UsdShaderOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        self._usd_fnc = UsdShade.Shader(self._usd_prim)

    def set_file(self, file_path):
        _ = self._usd_fnc.GetInput('file')
        if _ is None:
            _ = self._usd_fnc.CreateInput('file', Sdf.ValueTypeNames.Asset)
        _.Set(file_path)


class UsdMaterialAssignOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim

    def assign(self, *args):
        arg = args[0]
        r = self._usd_prim.CreateRelationship('material:binding')
        if isinstance(arg, six.string_types):
            r.AddTarget(
                self._usd_prim.GetStage().GetPrimAtPath(arg).GetPath()
            )
        elif isinstance(arg, Sdf.Path):
            r.AddTarget(
                arg
            )
        elif isinstance(arg, Usd.Prim):
            r.AddTarget(
                arg.GetPath()
            )


class UsdXformOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        self._usd_fnc = UsdGeom.Xform(self._usd_prim)

    def set_translate(self, x, y, z):
        pass

    def set_matrix(self, matrix):
        op = self._usd_fnc.MakeMatrixXform()
        op.Set(Gf.Matrix4d(matrix))
