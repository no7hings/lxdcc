# coding:utf-8
# noinspection PyUnresolvedReferences
from pxr import Usd, Sdf, Vt, UsdGeom

from lxbasic import bsc_core

from lxusd import usd_configure

from lxutil import utl_core

from lxobj import obj_configure

import os


class UsdStageOpt(object):
    def __init__(self, stage=None):
        if stage is None:
            stage = Usd.Stage.CreateInMemory()
        #
        self._usd_stage = stage
        self._usd_stage.SetMetadata("metersPerUnit", 0.01)
        UsdGeom.SetStageUpAxis(self._usd_stage, UsdGeom.Tokens.y)
    @property
    def usd_instance(self):
        return self._usd_stage

    def set_sublayer_append(self, file_path):
        root_layer = self._usd_stage.GetRootLayer()
        if os.path.isfile(file_path) is True:
            root_layer.subLayerPaths.append(file_path)
            utl_core.Log.set_module_result_trace(
                'usd-layer-append',
                u'file="{}"'.format(file_path)
            )
        else:
            utl_core.Log.set_module_warning_trace(
                'usd-layer-append',
                u'file="{}" is non-exist'.format(file_path)
            )

    def set_flatten(self):
        self._usd_stage.Flatten()

    def set_sublayer_prepend(self, file_path):
        root_layer = self._usd_stage.GetRootLayer()
        if os.path.isfile(file_path) is True:
            root_layer.subLayerPaths.insert(0, file_path)
            utl_core.Log.set_module_result_trace(
                'usd-layer-prepend',
                u'file="{}"'.format(file_path)
            )
        else:
            utl_core.Log.set_module_warning_trace(
                'usd-layer-prepend',
                u'file="{}" is non-exist'.format(file_path)
            )

    def set_default_prim(self, obj_path):
        prim = self._usd_stage.GetPrimAtPath(obj_path)
        self._usd_stage.SetDefaultPrim(prim)
        #
        utl_core.Log.set_module_result_trace(
            'usd-stage-set-default-prim',
            u'obj="{}"'.format(obj_path)
        )

    def set_export_to(self, file_path):
        self._usd_stage.Export(file_path)
        utl_core.Log.set_module_result_trace(
            'usd-export',
            u'file="{}"'.format(file_path)
        )
        #
        # import os
        # base, ext = os.path.splitext(file_path)
        # self._usd_stage.Export(base + '.usda')
        # #
        # utl_core.Log.set_module_result_trace(
        #     'usd-geometry-export',
        #     'file-path: "{}"'.format(file_path)
        # )

    def set_obj_create_as_override(self, obj_path):
        utl_core.Log.set_module_result_trace(
            'override-prim-create',
            u'obj="{}"'.format(obj_path)
        )
        return self._usd_stage.OverridePrim(obj_path)

    def get_obj(self, obj_path):
        return self._usd_stage.GetPrimAtPath(obj_path)

    def set_root_create(self, root, override=False):
        dag_path_comps = bsc_core.DccPathDagMtd.get_dag_component_paths(
            root, pathsep=usd_configure.Obj.PATHSEP
        )
        if dag_path_comps:
            dag_path_comps.reverse()
        #
        for i_path in dag_path_comps:
            if i_path != usd_configure.Obj.PATHSEP:
                if override is True:
                    self.set_obj_create_as_override(i_path)
                else:
                    self._usd_stage.DefinePrim(i_path, usd_configure.ObjType.TRANSFORM)
        #
        default_prim_path = self._usd_stage.GetPrimAtPath(dag_path_comps[-1])
        self._usd_stage.SetDefaultPrim(default_prim_path)


class UsdStageDataOpt(object):
    def __init__(self, stage=None):
        self._usd_stage = stage
    @property
    def usd_instance(self):
        return self._usd_stage

    def set_create(self, type_, value):
        print type_


class UsdPrimOpt(object):
    def __init__(self, prim):
        self._usd_prim = prim

    def get_customize_ports(self):
        return self._usd_prim.GetAuthoredAttributes() or []

    def get_customize_attributes(self, includes=None):
        dic = {}
        _ = self.get_customize_ports()
        for i in _:
            p = i.GetName().split(':')[-1]
            if isinstance(includes, (tuple, list)):
                if p not in includes:
                    continue
            dic[p] = i.Get()
        return dic


class UsdDataMapper(object):
    MAPPER = {
        obj_configure.Type.CONSTANT_BOOLEAN: Sdf.ValueTypeNames.Bool,
        obj_configure.Type.CONSTANT_INTEGER: Sdf.ValueTypeNames.Int,
        obj_configure.Type.CONSTANT_FLOAT: Sdf.ValueTypeNames.Float,
        obj_configure.Type.CONSTANT_STRING: Sdf.ValueTypeNames.String,
        obj_configure.Type.ARRAY_STRING: Sdf.ValueTypeNames.StringArray,
    }
    def __init__(self, dcc_type, dcc_value):
        self._dcc_type = dcc_type
        self._dcc_value = dcc_value

    def get_usd_args(self):
        key = self._dcc_type.category.name, self._dcc_type.name
        if key in self.MAPPER:
            usd_type = self.MAPPER[key]
            return usd_type, None
        return None, None


class UsdGeometryOpt(object):
    def __init__(self, prim):
        self._usd_prim = prim
        self._usd_geometry = UsdGeom.Imageable(self._usd_prim)

    def set_customize_port_create(self, port_path, dcc_type, dcc_value):
        usd_type, usd_value = UsdDataMapper(dcc_type, dcc_value).get_usd_args()
        if usd_type is not None:
            p = self._usd_geometry.CreatePrimvar(
                port_path,
                usd_type
            )
            p.Set(dcc_value)
        else:
            print dcc_type


class UsdMeshOpt(object):
    def __init__(self, mesh):
        self._usd_mesh = mesh
        self._usd_prim = mesh.GetPrim()
        self._obj_path = self._usd_prim.GetPath().pathString
    @property
    def usd_instance(self):
        return self._usd_mesh

    def get_uv_map_names(self):
        lis = []
        usd_primvars = self._usd_mesh.GetAuthoredPrimvars()
        for uv_primvar in usd_primvars:
            uv_map_name = uv_primvar.GetPrimvarName()
            if uv_primvar.GetIndices():
                lis.append(uv_map_name)
        return lis

    def get_uv_map(self, uv_map_name):
        uv_primvar = self._usd_mesh.GetPrimvar(uv_map_name)
        uv_map_face_vertex_indices = uv_primvar.GetIndices()
        uv_map_coords = uv_primvar.Get()
        return uv_map_face_vertex_indices, uv_map_coords

    def set_uv_map_name_add(self, uv_map_name):
        pass

    def set_uv_map_name_create(self, uv_map_name):
        if self._usd_mesh.HasPrimvar(uv_map_name) is True:
            return self._usd_mesh.GetPrimvar(uv_map_name)
        else:
            utl_core.Log.set_module_result_trace(
                'uv-map-create',
                u'uv-map-path="{}.{}"'.format(
                    self._obj_path, uv_map_name
                )
            )
            return self._usd_mesh.CreatePrimvar(
                uv_map_name,
                Sdf.ValueTypeNames.TexCoord2fArray,
                UsdGeom.Tokens.faceVarying
            )

    def _get_primvar_(self, primvar_name):
        if self._usd_mesh.HasPrimvar(primvar_name) is True:
            return self._usd_mesh.GetPrimvar(primvar_name)
        else:
            return self._usd_mesh.CreatePrimvar(
                primvar_name,
                Sdf.ValueTypeNames.TexCoord2fArray,
                UsdGeom.Tokens.faceVarying
            )

    def set_uv_map_create(self, uv_map_name, uv_map):
        if uv_map_name == 'map1':
            uv_map_name = 'st'
        #
        primvar = self.set_uv_map_name_create(uv_map_name)
        #
        uv_map_face_vertex_indices, uv_map_coords = uv_map
        primvar.Set(uv_map_coords)
        primvar.SetIndices(Vt.IntArray(uv_map_face_vertex_indices))
    #
    def set_uv_map(self, uv_map_name, uv_map):
        primvar = self._usd_mesh.GetPrimvar(uv_map_name)
        #
        uv_map_face_vertex_indices, uv_map_coords = uv_map
        primvar.Set(uv_map_coords)
        primvar.SetIndices(Vt.IntArray(uv_map_face_vertex_indices))

