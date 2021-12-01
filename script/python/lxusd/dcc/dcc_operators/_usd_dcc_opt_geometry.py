# coding:utf-8
# noinspection PyUnresolvedReferences
from pxr import Usd, Sdf, Vt, UsdGeom, Gf

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxutil.dcc import utl_dcc_opt_abs

from lxutil import utl_core


class UsdOptCore(object):
    @classmethod
    def _get_int_array_(cls, usd_int_array):
        return list(usd_int_array)
    @classmethod
    def _get_point_array_(cls, usd_point_array):
        return [tuple(i) for i in usd_point_array]
    @classmethod
    def _get_coord_array_(cls, usd_coord_array):
        return [tuple(i) for i in usd_coord_array]
    @classmethod
    def _get_matrix_(cls, usd_matrix):
        lis = []
        for row in usd_matrix:
            for column in row:
                lis.append(column)
        return lis
    @classmethod
    def _get_usd_matrix_(cls, matrix):
        lis = []
        for i in range(4):
            rows = []
            for j in range(4):
                rows.append(matrix[i * 4 + j])
            lis.append(rows)
        #
        return Gf.Matrix4d(lis)


class AbsUsdOptDef(object):
    def __init__(self, *args, **kwargs):
        self._prim = args[0]
    @property
    def prim(self):
        return self._prim
    @property
    def stage(self):
        return self.prim.GetStage()


class TransformOpt(AbsUsdOptDef):
    def __init__(self, *args, **kwargs):
        super(TransformOpt, self).__init__(*args, **kwargs)
    @property
    def xform(self):
        return UsdGeom.Xform(self.prim)

    def set_matrix(self, matrix):
        xform = self.xform
        op = xform.MakeMatrixXform()
        op.Set(UsdOptCore._get_usd_matrix_(matrix))

    def get_matrix(self):
        xform = self.xform
        op = xform.MakeMatrixXform()
        usd_matrix = op.Get()
        if usd_matrix is None:
            usd_matrix = Gf.Matrix4d()
        return UsdOptCore._get_matrix_(usd_matrix)


class MeshOpt(
    AbsUsdOptDef,
    utl_dcc_opt_abs.AbsMeshOptDef
):
    def __init__(self, *args, **kwargs):
        super(MeshOpt, self).__init__(*args, **kwargs)
    @property
    def mesh(self):
        return UsdGeom.Mesh(self.prim)

    def set_create(self, face_vertices, points, uv_maps=None, normal_maps=None, color_maps=None):
        prim = self.prim
        mesh = self.mesh
        face_vertex_counts, face_vertex_indices = face_vertices
        self._set_face_vertex_counts_(face_vertex_counts)
        self._set_face_vertex_indices_(face_vertex_indices)
        self.set_points(points)
        self.set_uv_maps(uv_maps)

    def _set_face_vertex_counts_(self, raw):
        if raw:
            mesh = self.mesh
            if mesh.GetPrim().HasAttribute('faceVertexCounts') is False:
                face_vertex_counts_attr = mesh.CreateFaceVertexCountsAttr()
            else:
                face_vertex_counts_attr = mesh.GetFaceVertexCountsAttr()
            face_vertex_counts_attr.Set(raw)

    def _set_face_vertex_indices_(self, raw):
        if raw:
            mesh = self.mesh
            if mesh.GetPrim().HasAttribute("faceVertexIndices") is False:
                face_vertex_counts_attr = mesh.CreateFaceVertexIndicesAttr()
            else:
                face_vertex_counts_attr = mesh.GetFaceVertexIndicesAttr()
            face_vertex_counts_attr.Set(raw)

    def get_face_vertex_counts(self):
        mesh = self.mesh
        a = mesh.GetFaceVertexCountsAttr()
        if a.GetNumTimeSamples():
            v = a.Get(0)
        else:
            v = a.Get()
        if v:
            return UsdOptCore._get_int_array_(v)
        return []

    def get_face_vertex_indices(self):
        mesh = self.mesh
        a = mesh.GetFaceVertexIndicesAttr()
        if a.GetNumTimeSamples():
            v = a.Get(0)
        else:
            v = a.Get()
        if v:
            return UsdOptCore._get_int_array_(v)
        return []
    @classmethod
    def _get_face_vertex_reverse_(cls, face_vertex_counts, face_vertex_indices):
        lis = []
        index = 0
        for seq, face_vertex_count in enumerate(face_vertex_counts):
            indices = face_vertex_indices[index:index + face_vertex_count]
            indices.reverse()
            lis.extend(indices)
            index += face_vertex_count
        return lis

    def get_face_vertices(self):
        return self.get_face_vertex_counts(), self.get_face_vertex_indices()

    def get_points(self):
        mesh = self.mesh
        a = mesh.GetPointsAttr()
        if a.GetNumTimeSamples():
            v = a.Get(0)
        else:
            v = a.Get()
        if v:
            return UsdOptCore._get_point_array_(v)
        return []

    def set_points(self, points):
        mesh = self.mesh
        return mesh.GetPointsAttr().Set(points)

    def get_uv_map_names(self):
        lis = []
        mesh = self.mesh
        usd_primvars = mesh.GetAuthoredPrimvars()
        for uv_primvar in usd_primvars:
            name = uv_primvar.GetPrimvarName()
            if uv_primvar.GetIndices():
                lis.append(name)
        return lis

    def get_uv_map_coords(self, uv_map_name):
        mesh = self.mesh
        uv_primvar = mesh.GetPrimvar(uv_map_name)
        uv_map_coords = uv_primvar.Get()
        return uv_map_coords

    def get_uv_map(self, uv_map_name):
        mesh = self.mesh
        a = mesh.GetPrimvar(uv_map_name)
        uv_map_face_vertex_counts = self.get_face_vertex_counts()
        uv_map_face_vertex_indices = a.GetIndices()
        uv_map_coords = a.Get()
        return uv_map_face_vertex_counts, UsdOptCore._get_int_array_(uv_map_face_vertex_indices), uv_map_coords

    def get_uv_maps(self, default_uv_map_name='st'):
        dic = {}
        uv_map_names = self.get_uv_map_names()
        for uv_map_name in uv_map_names:
            uv_map = self.get_uv_map(uv_map_name)
            dic[uv_map_name] = uv_map
        return dic

    def set_uv_maps(self, raw):
        if raw:
            mesh = self.mesh
            for uv_map_name, v in raw.items():
                if uv_map_name == 'map1':
                    uv_map_name = 'st'
                uv_map_face_vertex_counts, uv_map_face_vertex_indices, uv_map_coords = v
                if mesh.HasPrimvar(uv_map_name) is False:
                    primvar = mesh.CreatePrimvar(
                        uv_map_name,
                        Sdf.ValueTypeNames.TexCoord2fArray,
                        UsdGeom.Tokens.faceVarying
                    )
                else:
                    primvar = mesh.GetPrimvar(
                        uv_map_name
                    )
                primvar.Set(uv_map_coords)
                primvar.SetIndices(Vt.IntArray(uv_map_face_vertex_indices))

    def get_face_vertices_as_uuid(self):
        raw = self.get_face_vertices()
        return bsc_core.HashMtd.get_hash_value(raw, as_unique_id=True)

    def get_uv_map_face_vertices_as_uuid(self, uv_map_name='st'):
        uv_map_face_vertex_counts, uv_map_face_vertex_indices, uv_map_coords = self.get_uv_map(uv_map_name)
        raw = (uv_map_face_vertex_counts, uv_map_face_vertex_indices)
        return bsc_core.HashMtd.get_hash_value(raw, as_unique_id=True)

    def get_points_as_uuid(self, ordered=False, round_count=4):
        raw = self.get_points()
        if ordered is True:
            raw.sort()
        #
        raw = bsc_core.PointArrayOpt(raw).round_to(round_count)
        return bsc_core.HashMtd.get_hash_value(raw, as_unique_id=True)

    def get_uv_maps_as_uuid(self, uv_map_name='st'):
        raw = self.get_uv_maps(uv_map_name)
        return bsc_core.HashMtd.get_hash_value(raw, as_unique_id=True)

    def get_vertex_count(self):
        _ = self.get_face_vertex_indices()
        return max(_) + 1

    def get_face_count(self):
        mesh = self.mesh
        return mesh.GetFaceCount()
