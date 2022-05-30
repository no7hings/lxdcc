# coding:utf-8
import copy

import collections
# noinspection PyUnresolvedReferences
from pxr import Usd, Sdf, Vt, UsdGeom

from lxusd import usd_configure, usd_core

from lxobj import obj_core

from lxutil import utl_core

import lxbasic.objects as bsc_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxusd.dcc.dcc_operators as usd_dcc_operators

from lxutil.fnc import utl_fnc_obj_abs


class GeometryUvMapExporter(utl_fnc_obj_abs.AbsFncOptionMethod):
    OPTION = dict(
        root_lstrip=False,
        file_0=None,
        file_1=None,
        display_color=(0.25, 0.75, 0.5)
    )
    def __init__(self, file_path, root=None, option=None):
        self._file_path = file_path
        self._root = root
        #
        super(GeometryUvMapExporter, self).__init__(option)
        #
        self._geometry_stage_0 = Usd.Stage.CreateInMemory()
        self._geometry_stage_opt_0 = usd_core.UsdStageOpt(self._geometry_stage_0)
        self._geometry_stage_1 = Usd.Stage.CreateInMemory()
        self._geometry_stage_opt_1 = usd_core.UsdStageOpt(self._geometry_stage_1)
        #
        self._output_stage = Usd.Stage.CreateInMemory()
        self._output_stage_opt = usd_core.UsdStageOpt(self._output_stage)
        #
        self._file_path_0 = self.get('file_0')
        if self._file_path_0 is not None:
            self._geometry_stage_opt_0.set_sublayer_append(self._file_path_0)
            self._geometry_stage_0.Flatten()
        #
        self._file_path_1 = self.get('file_1')
        if self._file_path_1 is not None:
            self._geometry_stage_opt_1.set_sublayer_append(self._file_path_1)
            self._geometry_stage_1.Flatten()
    @classmethod
    def _get_uv_map_names_(cls, mesh):
        lis = []
        usd_primvars = mesh.GetAuthoredPrimvars()
        for uv_primvar in usd_primvars:
            uv_map_name = uv_primvar.GetPrimvarName()
            if uv_primvar.GetIndices():
                lis.append(uv_map_name)
        return lis
    @classmethod
    def _get_uv_map_(cls, mesh, uv_map_name):
        uv_primvar = mesh.GetPrimvar(uv_map_name)
        uv_map_face_vertex_indices = uv_primvar.GetIndices()
        uv_map_coords = uv_primvar.Get()
        return uv_map_face_vertex_indices, uv_map_coords

    def set_uv_map_export(self):
        display_color = self.get('display_color')
        ps = utl_core.Progress.set_create(len([i for i in self._geometry_stage_0.TraverseAll()]))
        #
        for i_usd_prim in self._geometry_stage_0.TraverseAll():
            utl_core.Progress.set_update(ps)
            i_obj_type_name = i_usd_prim.GetTypeName()
            obj_path = i_usd_prim.GetPath().pathString
            output_prim = self._output_stage_opt.set_obj_create_as_override(obj_path)
            if i_obj_type_name == 'Mesh':
                _ = self._geometry_stage_1.GetPrimAtPath(obj_path)
                i_output_usd_mesh = UsdGeom.Mesh(output_prim)
                i_output_usd_mesh_opt = usd_core.UsdMeshOpt(i_output_usd_mesh)
                if _.IsValid() is True:
                    surface_geometry_prim = _
                    input_usd_mesh = UsdGeom.Mesh(surface_geometry_prim)
                    output_prim.CreateAttribute(
                        'userProperties:usd:logs:uv_map_from', Sdf.ValueTypeNames.Asset, custom=False
                    ).Set(self._file_path_1)
                else:
                    input_usd_mesh = UsdGeom.Mesh(i_usd_prim)
                    output_prim.CreateAttribute(
                        'userProperties:usd:logs:uv_map_from', Sdf.ValueTypeNames.Asset, custom=False
                    ).Set(self._file_path_0)
                #
                input_usd_mesh_opt = usd_core.UsdMeshOpt(input_usd_mesh)
                uv_map_names = input_usd_mesh_opt.get_uv_map_names()
                if uv_map_names:
                    for uv_map_name in uv_map_names:
                        uv_map = input_usd_mesh_opt.get_uv_map(uv_map_name)
                        i_output_usd_mesh_opt.set_uv_map_create(uv_map_name, uv_map)
                #
                input_usd_mesh_opt.set_display_color_fill(
                    display_color
                )
                i_output_usd_mesh_opt.set_usd_display_colors(
                    input_usd_mesh_opt.get_usd_display_colors()
                )
        #
        utl_core.Progress.set_stop(ps)
        #
        self._output_stage_opt.set_default_prim(self._root)
        self._output_stage_opt.set_export_to(self._file_path)
        #
        utl_core.Log.set_module_result_trace(
            'fnc-geometry-usd-uv-map-export',
            u'file="{}"'.format(self._file_path)
        )

    def set_run(self):
        self.set_uv_map_export()


class GeometryDebugger(utl_fnc_obj_abs.AbsFncOptionMethod):
    OPTION = dict(
        input_file='',
        output_file='',
        location=''
    )
    def __init__(self, option):
        super(GeometryDebugger, self).__init__(option)

    def set_face_vertex_indices_reverse_create(self):
        input_file_path = self.get('input_file')
        output_file_path = self.get('output_file')
        #
        self._input_stage_opt = usd_core.UsdStageOpt(input_file_path)

        self._output_stage_opt = usd_core.UsdStageOpt()

        with utl_core.log_progress_bar(
            maximum=self._input_stage_opt.get_count(),
            label='face vertex indices reverse create'
        ) as l_p:
            for i_input_prim in self._input_stage_opt.usd_instance.TraverseAll():
                l_p.set_update()
                #
                i_obj_type_name = i_input_prim.GetTypeName()
                if i_obj_type_name == 'Mesh':
                    i_input_mesh = UsdGeom.Mesh(i_input_prim)
                    i_input_mesh_opt = usd_core.UsdMeshOpt(i_input_mesh)
                    print i_input_mesh_opt.get_face_vertex_indices()


class GeometryDisplayColorExporter(utl_fnc_obj_abs.AbsFncOptionMethod):
    OPTION = dict(

    )
    def __init__(self, option):
        super(GeometryDisplayColorExporter, self).__init__(option)


class GeometryInfoXmlExporter(utl_fnc_obj_abs.AbsDccExporter):
    ROOT_LSTRIP = 'root_lstrip'
    GEOMETRY_FILE = 'geometry_file'
    OPTION = dict(
        root_lstrip=False,
        geometry_file=None,
    )
    def __init__(self, file_path, root=None, option=None):
        super(GeometryInfoXmlExporter, self).__init__(file_path, root, option)
        #
        self._usd_stage = Usd.Stage.CreateInMemory()
        self._usd_stage_opt = usd_core.UsdStageOpt(self._usd_stage)
        #
        geometry_file_path = self._option.get('geometry_file')
        if geometry_file_path is not None:
            self._usd_stage_opt.set_sublayer_append(geometry_file_path)
        #
        self._usd_stage.Flatten()
    @classmethod
    def _get_info_raw(cls, stage, root=None, lstrip=None):
        info_configure = bsc_objects.Content(value=collections.OrderedDict())
        for prim in stage.TraverseAll():
            i_obj_type_name = prim.GetTypeName()
            obj_path = prim.GetPath().pathString
            #
            obj_path_ = obj_core.DccPathDagMtd.get_dag_path_lstrip(obj_path, lstrip)
            if obj_path_:
                obj_properties = bsc_objects.Content(value=collections.OrderedDict())
                #
                if i_obj_type_name == 'Mesh':
                    obj_type_name_ = 'mesh'
                    obj_attributes = collections.OrderedDict()
                    mesh_obj_opt = usd_dcc_operators.MeshOpt(prim)
                    obj_attributes['face-count'] = mesh_obj_opt.get_face_count()
                    obj_attributes['point-count'] = mesh_obj_opt.get_vertex_count()
                    obj_attributes['face-vertices-uuid'] = mesh_obj_opt.get_face_vertices_as_uuid()
                    obj_attributes['points-uuid'] = mesh_obj_opt.get_points_as_uuid(ordered=True)
                    obj_attributes['uv-maps-uuid'] = mesh_obj_opt.get_uv_maps_as_uuid()
                else:
                    obj_type_name_ = 'transform'
                    obj_attributes = collections.OrderedDict()
                #
                info_key_path = '.'.join([i for i in obj_path_.split('/') if i])
                obj_properties.set('properties.type', obj_type_name_)
                obj_properties.set('properties.attributes', obj_attributes)
                #
                info_configure.set(info_key_path, obj_properties.value)

        j2_template = usd_configure.JinJa2.ENVIRONMENT.get_template('geometry-xml-template.j2')

        ks = dict(
            option=dict(
                indent=4,
                linesep='\n'
            ),
            objs=info_configure.value
        )

        raw = j2_template.render(**ks)
        return raw

    def set_run(self):
        raw = self._get_info_raw(
            self._usd_stage,
            root=self._root, lstrip=self._option.get('root_lstrip')
        )
        #
        f = utl_dcc_objects.OsFile(self._file_path)
        f.set_write(raw)
        #
        # import os
        # base, ext = os.path.splitext(self._file_path)
        # self._usd_stage.Export(base + '.usda')


class GeometryExporter(object):
    OPTION = dict(
        default_prim_path=None,
        with_usda=False,
        root_lstrip=False,
    )
    def __init__(self, file_path, root=None, option=None):
        self._file_path = file_path
        self._root = root
        #
        self._option = copy.deepcopy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                if k in self.OPTION:
                    self._option[k] = v
        #
        self._output_stage = Usd.Stage.CreateInMemory()
        self._output_stage_opt = usd_core.UsdStageOpt(self._output_stage)

        self._set_root_build_()

    def _set_root_build_(self):
        dag_path_comps = obj_core.DccPathDagMtd.get_dag_component_paths(self._root, pathsep=usd_configure.Obj.PATHSEP)
        if dag_path_comps:
            dag_path_comps.reverse()
        #
        root = self._output_stage.GetPseudoRoot()
        for i in dag_path_comps:
            if i != usd_configure.Obj.PATHSEP:
                root = self._output_stage.DefinePrim(i, usd_configure.ObjType.TRANSFORM)
        #
        default_prim_path = self._output_stage.GetPrimAtPath(dag_path_comps[1])
        self._output_stage.SetDefaultPrim(default_prim_path)

    def _set_transform_opt_create_(self, obj_path, use_override=False):
        if use_override is True:
            prim = self._output_stage.OverridePrim(obj_path, usd_configure.ObjType.TRANSFORM)
        else:
            prim = self._output_stage.DefinePrim(obj_path, usd_configure.ObjType.TRANSFORM)
        obj_opt = usd_dcc_operators.TransformOpt(prim)
        return obj_opt

    def _set_mesh_opt_create_(self, obj_path, use_override=False):
        if use_override is True:
            prim = self._output_stage.OverridePrim(obj_path, usd_configure.ObjType.MESH)
        else:
            prim = self._output_stage.DefinePrim(obj_path, usd_configure.ObjType.MESH)
        #
        obj_opt = usd_dcc_operators.MeshOpt(prim)
        return obj_opt

    def _set_curve_create_(self, obj_path, use_override=False):
        if use_override is True:
            prim = self._output_stage.OverridePrim(obj_path, usd_configure.ObjType.CURVE)
        else:
            prim = self._output_stage.DefinePrim(obj_path, usd_configure.ObjType.CURVE)
        #
        obj_opt = usd_dcc_operators.CurveOpt(prim)
        return obj_opt

    def _set_export_run_(self):
        default_prim_path = self._option.get('default_prim_path')
        if default_prim_path is not None:
            self._output_stage_opt.set_default_prim(
                default_prim_path
            )
        #
        self._output_stage_opt.set_export_to(self._file_path)

    def set_run(self):
        self._set_export_run_()


if __name__ == '__main__':
    import lxusd.fnc.exporters as usd_fnc_exporters

    e = usd_fnc_exporters.GeometryInfoXmlExporter(
        file_path='/data/xml_test/test.info.xml',
        root='/master',
        option=dict(
            geometry_file='/l/prod/shl/publish/assets/chr/nn_gongshifu/mod/modeling/nn_gongshifu.mod.modeling.v007/cache/usd/geo/hi.usd'
        )
    )

    e.set_run()

