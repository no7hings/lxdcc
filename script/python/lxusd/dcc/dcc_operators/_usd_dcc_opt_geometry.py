# coding:utf-8
# noinspection PyUnresolvedReferences
from pxr import Usd, Sdf, Vt, UsdGeom, Gf

from lxbasic import bsc_core

from lxutil import utl_core

from lxutil.dcc import utl_dcc_opt_abs

from lxusd import usd_core


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
    @property
    def path(self):
        return self._prim.GetPath().pathString


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

    def set_visible(self, boolean):
        usd_core.UsdTransformOpt(
            self.prim
        ).set_visible(
            boolean
        )

    def set_customize_attribute_add(self, key, value):
        usd_core.UsdPrimOpt._add_customize_attribute_(
            self.xform, key, value
        )


class MeshOpt(
    AbsUsdOptDef,
    utl_dcc_opt_abs.AbsMeshOptDef
):
    def __init__(self, *args, **kwargs):
        super(MeshOpt, self).__init__(*args, **kwargs)
        self._set_mesh_opt_def_init_()

    def get_usd_mesh(self):
        return UsdGeom.Mesh(self.prim)
    @property
    def usd_mesh(self):
        return self.get_usd_mesh()
    @property
    def mesh(self):
        return self.get_usd_mesh()

    def set_create(self, face_vertices, points, uv_maps=None, normal_maps=None, color_maps=None):
        # prim = self.prim
        # mesh = self.usd_mesh
        face_vertex_counts, face_vertex_indices = face_vertices
        self._set_face_vertex_counts_(face_vertex_counts)
        self._set_face_vertex_indices_(face_vertex_indices)
        self.set_points(points)
        self.set_uv_maps(uv_maps)

    def _set_face_vertex_counts_(self, raw):
        if raw:
            usd_mesh = self.usd_mesh
            if usd_mesh.GetPrim().HasAttribute('faceVertexCounts') is False:
                face_vertex_counts_attr = usd_mesh.CreateFaceVertexCountsAttr()
            else:
                face_vertex_counts_attr = usd_mesh.GetFaceVertexCountsAttr()
            face_vertex_counts_attr.Set(raw)

    def _set_face_vertex_indices_(self, raw):
        if raw:
            usd_mesh = self.usd_mesh
            if usd_mesh.GetPrim().HasAttribute("faceVertexIndices") is False:
                face_vertex_counts_attr = usd_mesh.CreateFaceVertexIndicesAttr()
            else:
                face_vertex_counts_attr = usd_mesh.GetFaceVertexIndicesAttr()
            face_vertex_counts_attr.Set(raw)

    def get_face_vertex_counts(self):
        usd_mesh = self.usd_mesh
        a = usd_mesh.GetFaceVertexCountsAttr()
        if a.GetNumTimeSamples():
            v = a.Get(0)
        else:
            v = a.Get()
        if v:
            return UsdOptCore._get_int_array_(v)
        return []

    def get_face_vertex_indices(self):
        usd_mesh = self.usd_mesh
        a = usd_mesh.GetFaceVertexIndicesAttr()
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
        usd_mesh = self.usd_mesh
        p = usd_mesh.GetPointsAttr()
        if p.GetNumTimeSamples():
            v = p.Get(0)
        else:
            v = p.Get()
        if v:
            return UsdOptCore._get_point_array_(v)
        return []

    def set_points(self, points):
        usd_mesh = self.usd_mesh
        return usd_mesh.GetPointsAttr().Set(points)

    def get_uv_map_names(self):
        lis = []
        usd_mesh = self.usd_mesh
        usd_primvars = usd_mesh.GetAuthoredPrimvars()
        for i_primvar in usd_primvars:
            i_name = i_primvar.GetPrimvarName()
            if i_primvar.GetIndices():
                lis.append(i_name)
        return lis

    def get_uv_map_coords(self, uv_map_name):
        usd_mesh = self.usd_mesh
        uv_primvar = usd_mesh.GetPrimvar(uv_map_name)
        uv_map_coords = uv_primvar.Get()
        return uv_map_coords

    def get_uv_map(self, uv_map_name):
        usd_mesh = self.usd_mesh
        a = usd_mesh.GetPrimvar(uv_map_name)
        uv_map_face_vertex_counts = self.get_face_vertex_counts()
        uv_map_face_vertex_indices = a.GetIndices()
        uv_map_coords = a.Get()
        return uv_map_face_vertex_counts, UsdOptCore._get_int_array_(uv_map_face_vertex_indices), uv_map_coords

    def get_uv_maps(self, default_uv_map_name='st'):
        dic = {}
        uv_map_names = self.get_uv_map_names()
        for i_uv_map_name in uv_map_names:
            uv_map = self.get_uv_map(i_uv_map_name)
            dic[i_uv_map_name] = uv_map
        return dic

    def set_uv_maps(self, raw):
        if raw:
            usd_mesh = self.usd_mesh
            for i_uv_map_name, v in raw.items():
                if i_uv_map_name == 'map1':
                    i_uv_map_name = 'st'
                #
                i_uv_map_name_new = bsc_core.RawTextMtd.clear_up_to(
                    i_uv_map_name
                )
                if i_uv_map_name != i_uv_map_name_new:
                    utl_core.Log.set_module_warning_trace(
                        'usd uv-map set',
                        u'uv-map="{1}" in "{0}" is not available, auto convert to "{2}"'.format(
                            self.path,
                            i_uv_map_name,
                            i_uv_map_name_new
                        )
                    )
                    i_uv_map_name = i_uv_map_name_new
                #
                i_uv_map_face_vertex_counts, i_uv_map_face_vertex_indices, i_uv_map_coords = v
                if usd_mesh.HasPrimvar(i_uv_map_name) is False:
                    i_primvar = usd_mesh.CreatePrimvar(
                        i_uv_map_name,
                        Sdf.ValueTypeNames.TexCoord2fArray,
                        UsdGeom.Tokens.faceVarying
                    )
                else:
                    i_primvar = usd_mesh.GetPrimvar(
                        i_uv_map_name
                    )
                #
                i_primvar.Set(i_uv_map_coords)
                i_primvar.SetIndices(Vt.IntArray(i_uv_map_face_vertex_indices))

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
        raw = bsc_core.RawPointArrayOpt(raw).round_to(round_count)
        return bsc_core.HashMtd.get_hash_value(raw, as_unique_id=True)

    def get_uv_maps_as_uuid(self, uv_map_name='st'):
        raw = self.get_uv_maps(uv_map_name)
        return bsc_core.HashMtd.get_hash_value(raw, as_unique_id=True)

    def get_vertex_count(self):
        _ = self.get_face_vertex_indices()
        return max(_) + 1

    def get_face_count(self):
        usd_mesh = self.usd_mesh
        return usd_mesh.GetFaceCount()

    def set_visible(self, boolean):
        usd_core.UsdGeometryOpt(
            self.prim
        ).set_visible(
            boolean
        )

    def set_display_color_fill(self, color):
        usd_core.UsdGeometryMeshOpt(
            self.prim
        ).set_display_color_fill(
            color
        )

    def set_customize_attribute_add(self, key, value):
        usd_core.UsdPrimOpt._add_customize_attribute_(
            self.mesh, key, value
        )


class NurbsCurveOpt(
    AbsUsdOptDef,
    utl_dcc_opt_abs.AbsCurveOptDef
):
    def __init__(self, *args, **kwargs):
        super(NurbsCurveOpt, self).__init__(*args, **kwargs)
        self._set_curve_opt_def_init_()

    def get_usd_fnc(self):
        return UsdGeom.NurbsCurves(self.prim)
    @property
    def usd_fnc(self):
        return self.get_usd_fnc()

    def set_create(self, points, knots, ranges, widths, order):
        self.set_points(points)
        self.set_knots(knots)
        self.set_ranges(ranges)
        self.set_widths(widths)
        self.set_order(order)

    def set_points(self, values):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetPointsAttr()
        if p is None:
            p = usd_fnc.CreatePointsAttr()
        #
        p.Set(values)
        p = usd_fnc.GetCurveVertexCountsAttr()
        if p is None:
            p = usd_fnc.CreateCurveVertexCountsAttr()
        p.Set([len(values)])

    def get_points(self):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetPointsAttr()
        if p.GetNumTimeSamples():
            v = p.Get(0)
        else:
            v = p.Get()
        if v:
            return UsdOptCore._get_point_array_(v)
        return []

    def get_point_count(self):
        return len(self.get_points())

    def set_knots(self, values):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetKnotsAttr()
        if p is None:
            p = usd_fnc.CreateKnotsAttr()
        p.Set(values)

    def set_ranges(self, values):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetRangesAttr()
        if p is None:
            p = usd_fnc.CreateRangesAttr()
        p.Set(values)

    def set_widths(self, values):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetWidthsAttr()
        if p is None:
            p = usd_fnc.CreateWidthsAttr()
        p.Set(values)

    def set_extent(self, extent):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetPrim().HasAttribute('extent')
        if p is None:
            p = usd_fnc.CreateExtentAttr()
        p.Set(extent)

    def set_order(self, order):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetOrderAttr()
        if p is None:
            p = usd_fnc.CreateOrderAttr()
        p.Set(order)

    def set_display_color_fill(self, color):
        usd_core.UsdGeometryMeshOpt(
            self.prim
        ).set_display_color_fill(
            color
        )


class BasisCurveOpt(
    AbsUsdOptDef,
    utl_dcc_opt_abs.AbsCurveOptDef
):
    def __init__(self, *args, **kwargs):
        super(BasisCurveOpt, self).__init__(*args, **kwargs)
        self._set_curve_opt_def_init_()

    def get_usd_fnc(self):
        return UsdGeom.BasisCurves(self.prim)
    @property
    def usd_fnc(self):
        return self.get_usd_fnc()

    def set_create(self, counts, points, widths):
        self.set_curve_basis(
            UsdGeom.Tokens.catmullRom
        )
        self.set_curve_type(
            UsdGeom.Tokens.cubic
        )
        self.set_curve_vertex_counts(counts)
        self.set_points(points)
        self.set_widths(widths)

    def set_curve_type(self, value):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetTypeAttr()
        if p is not None:
            p = usd_fnc.CreateTypeAttr()

        p.Set(value)

    def set_curve_basis(self, value):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetBasisAttr()
        if p is not None:
            p = usd_fnc.CreateBasisAttr()

        p.Set(value)

    def set_curve_vertex_counts(self, values):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetCurveVertexCountsAttr()
        if p is None:
            p = usd_fnc.CreateCurveVertexCountsAttr()
        p.Set(values)

    def set_points(self, values):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetPointsAttr()
        if p is None:
            p = usd_fnc.CreatePointsAttr()
        p.Set(values)

    def get_points(self):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetPointsAttr()
        if p.GetNumTimeSamples():
            v = p.Get(0)
        else:
            v = p.Get()
        if v:
            return UsdOptCore._get_point_array_(v)
        return []

    def set_widths(self, values):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetWidthsAttr()
        if p is None:
            p = usd_fnc.CreateWidthsAttr()
        p.Set(values)

    def set_display_color_fill(self, color):
        usd_fnc = self.get_usd_fnc()
        usd_core.UsdGeometryOpt_(
            usd_fnc
        ).set_display_color_fill(
            color
        )
