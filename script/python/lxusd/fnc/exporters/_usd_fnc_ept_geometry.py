# coding:utf-8
import six
# noinspection PyUnresolvedReferences
from pxr import Usd, Sdf, Vt, UsdGeom

import copy

import collections

from lxbasic import bsc_core

from lxusd import usd_configure, usd_core

from lxutil import utl_core

import lxcontent.objects as ctt_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxusd.dcc.dcc_operators as usd_dcc_operators

from lxutil.fnc import utl_fnc_obj_abs


class GeometryUvMapExporter(utl_fnc_obj_abs.AbsFncOptionBase):
    OPTION = dict(
        file_0=None,
        file_1=None,
        #
        display_color=(0.25, 0.75, 0.5),
        #
        path_lstrip=None,
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
            self._geometry_stage_opt_0.append_sublayer(self._file_path_0)
            self._geometry_stage_0.Flatten()
        #
        self._file_path_1 = self.get('file_1')
        if self._file_path_1 is not None:
            self._geometry_stage_opt_1.append_sublayer(self._file_path_1)
            self._geometry_stage_1.Flatten()

    def set_uv_map_export(self):
        display_color = self.get('display_color')
        with utl_core.LogProgressRunner.create_as_bar(
                maximum=len([i for i in self._geometry_stage_0.TraverseAll()]), label='geometry look export'
                ) as l_p:
            for i_usd_prim in self._geometry_stage_0.TraverseAll():
                l_p.set_update()
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
                            i_output_usd_mesh_opt.create_uv_map(uv_map_name, uv_map)
                    #
                    input_usd_mesh_opt.fill_display_color(
                        display_color
                    )
                    i_output_usd_mesh_opt.set_display_colors(
                        input_usd_mesh_opt.get_display_colors()
                    )
        #
        self._output_stage_opt.set_default_prim(self._root)
        # create directory
        # bsc_core.StgFileOpt(self._file_path).create_directory()
        #
        self._output_stage_opt.export_to(self._file_path)
        #
        utl_core.Log.set_module_result_trace(
            'fnc-geometry-usd-uv-map-export',
            u'file="{}"'.format(self._file_path)
        )

    def set_run(self):
        self.set_uv_map_export()


class GeometryLookPropertyExporter(utl_fnc_obj_abs.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        #
        stage_src=None,
        file_src='',
        #
        asset_name='',
        #
        color_seed=0,
        #
        with_uv_map=False,
        #
        with_object_color=False,
        with_group_color=False,
        with_asset_color=False,
        with_shell_color=False,
        #
        with_display_color=False,
        display_color=(0.25, 0.75, 0.5)
    )

    def __init__(self, *args, **kwargs):
        super(GeometryLookPropertyExporter, self).__init__(*args, **kwargs)
        #
        self._file_path = self.get('file')
        #
        file_path_src = self.get('file_src')
        stage_src = self.get('stage_src')
        #
        self._location_path = self.get('location')
        #
        self._asset_name = self.get('asset_name')
        #
        self._color_seed = self.get('color_seed')

        self._color_scheme = self.get('color_scheme')
        #
        if stage_src is not None:
            self._usd_stage_src = stage_src
        else:
            self._usd_stage_src = Usd.Stage.Open(file_path_src, Usd.Stage.LoadAll)
        #
        self._usd_stage_opt_src = usd_core.UsdStageOpt(self._usd_stage_src)
        #
        self._usd_stage_tgt = Usd.Stage.CreateInMemory()
        self._usd_stage_opt_tgt = usd_core.UsdStageOpt(self._usd_stage_tgt)

    def set_run(self):
        count = len([i for i in self._usd_stage_src.TraverseAll()])
        with utl_core.LogProgressRunner.create_as_bar(
            maximum=count,
            label='geometry look property create'
        ) as l_p:
            display_color = self.get('display_color')
            asset_color = bsc_core.RawTextOpt(self._asset_name).to_rgb_(maximum=1, seed=self._color_seed)
            for i_usd_prim_src in self._usd_stage_src.TraverseAll():
                l_p.set_update()
                #
                i_obj_type_name = i_usd_prim_src.GetTypeName()
                i_obj_path = i_usd_prim_src.GetPath().pathString
                i_obj_path_opt = bsc_core.DccPathDagOpt(i_obj_path)
                #
                i_usd_prim_tgt = self._usd_stage_tgt.OverridePrim(i_obj_path)
                if i_obj_type_name in [usd_configure.ObjType.Mesh, usd_configure.ObjType.NurbsCurves]:
                    i_usd_geometry_opt_tgt = usd_core.UsdGeometryOpt(i_usd_prim_tgt)
                    #
                    if self.get('with_object_color') is True:
                        i_object_color = i_obj_path_opt.get_color_from_name(maximum=1.0, seed=self._color_seed)
                        i_usd_geometry_opt_tgt.create_customize_port_(
                            'object_color', 'color/color3', i_object_color
                        )
                    if self.get('with_group_color') is True:
                        i_group_path_opt = i_obj_path_opt.get_parent().get_parent()
                        i_group_color = i_group_path_opt.get_color_from_name(maximum=1.0, seed=self._color_seed)
                        i_usd_geometry_opt_tgt.create_customize_port_(
                            'group_color', 'color/color3', i_group_color
                        )
                    if self.get('with_asset_color') is True:
                        i_usd_geometry_opt_tgt.create_customize_port_(
                            'asset_color', 'color/color3', asset_color
                        )
                    #
                    if i_obj_type_name == usd_configure.ObjType.Mesh:
                        i_usd_mesh_src = UsdGeom.Mesh(i_usd_prim_src)
                        i_usd_mesh_opt_src = usd_core.UsdMeshOpt(i_usd_mesh_src)
                        #
                        i_usd_mesh_tgt = UsdGeom.Mesh(i_usd_prim_tgt)
                        i_usd_mesh_opt_tgt = usd_core.UsdMeshOpt(i_usd_mesh_tgt)
                        if self.get('with_uv_map') is True:
                            i_uv_map_names = i_usd_mesh_opt_src.get_uv_map_names()
                            if i_uv_map_names:
                                for j_uv_map_name in i_uv_map_names:
                                    uv_map = i_usd_mesh_opt_src.get_uv_map(j_uv_map_name)
                                    i_usd_mesh_opt_tgt.create_uv_map(j_uv_map_name, uv_map)
                        #
                        if self.get('with_shell_color') is True:
                            i_offset = bsc_core.RawTextOpt(i_obj_path_opt.name).get_index()
                            colors = i_usd_mesh_opt_src.get_colors_fom_shell(
                                offset=i_offset, seed=self._color_seed
                            )
                            i_usd_geometry_opt_tgt.create_customize_port_as_face_color(
                                'shell_color', 'array/color3', colors
                            )
                        #
                        if self.get('with_display_color') is True:
                            i_usd_mesh_opt_tgt.fill_display_color(display_color)
        #
        component_paths = bsc_core.DccPathDagOpt(self._location_path).get_component_paths()
        if component_paths:
            component_paths.reverse()
            self._usd_stage_opt_tgt.set_default_prim(
                component_paths[1]
            )

        self._usd_stage_opt_tgt.export_to(self._file_path)


class GeometryDisplayColorExporter(utl_fnc_obj_abs.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        #
        stage_src=None,
        file_src='',
        #
        asset_name='',
        #
        color_seed=0,
        # "object_color", "group_color", "asset_color", "uv_map_color", "shell_color", "enable_color"
        color_scheme='asset_color'
    )

    def __init__(self, *args, **kwargs):
        super(GeometryDisplayColorExporter, self).__init__(*args, **kwargs)
        #
        self._file_path = self.get('file')
        #
        file_path_src = self.get('file_src')
        stage_src = self.get('stage_src')
        #
        self._location_path = self.get('location')
        #
        self._asset_name = self.get('asset_name')
        #
        self._color_seed = self.get('color_seed')

        self._color_scheme = self.get('color_scheme')
        #
        if stage_src is not None:
            self._usd_stage_src = stage_src
        else:
            self._usd_stage_src = Usd.Stage.Open(file_path_src, Usd.Stage.LoadAll)
        #
        self._usd_stage_opt_src = usd_core.UsdStageOpt(self._usd_stage_src)
        #
        self._usd_stage_tgt = Usd.Stage.CreateInMemory()
        self._usd_stage_opt_tgt = usd_core.UsdStageOpt(self._usd_stage_tgt)

    def set_run(self):
        count = len([i for i in self._usd_stage_src.TraverseAll()])
        color_scheme = self.get('color_scheme')
        with utl_core.LogProgressRunner.create_as_bar(
                maximum=count,
                label='geometry display-color create'
        ) as l_p:
            asset_color = bsc_core.RawTextOpt(self._asset_name).to_rgb_(maximum=1, seed=self._color_seed)
            for i_index, i_usd_prim_src in enumerate(self._usd_stage_src.TraverseAll()):
                i_obj_type_name = i_usd_prim_src.GetTypeName()
                i_obj_path = i_usd_prim_src.GetPath().pathString
                i_obj_path_opt = bsc_core.DccPathDagOpt(i_obj_path)
                #
                i_usd_prim_src = self._usd_stage_src.GetPrimAtPath(i_obj_path)
                i_usd_prim_tgt = self._usd_stage_tgt.OverridePrim(i_obj_path)
                if i_obj_type_name in [usd_configure.ObjType.Mesh, usd_configure.ObjType.NurbsCurves]:
                    #
                    i_usd_mesh_src = UsdGeom.Mesh(i_usd_prim_src)
                    i_usd_mesh_opt_src = usd_core.UsdMeshOpt(i_usd_mesh_src)
                    # all use mesh? but it is run completed
                    i_usd_mesh_tgt = UsdGeom.Mesh(i_usd_prim_tgt)
                    i_usd_mesh_opt_tgt = usd_core.UsdMeshOpt(i_usd_mesh_tgt)
                    #
                    if isinstance(color_scheme, six.string_types):
                        if color_scheme == 'object_color':
                            i_object_color = i_obj_path_opt.get_color_from_name(
                                maximum=1.0, seed=self._color_seed
                            )
                            i_usd_mesh_opt_tgt.fill_display_color(i_object_color)
                        elif color_scheme == 'group_color':
                            i_group_path_opt = i_obj_path_opt.get_parent().get_parent()
                            i_group_color = i_group_path_opt.get_color_from_name(
                                maximum=1.0, seed=self._color_seed
                            )
                            i_usd_mesh_opt_tgt.fill_display_color(i_group_color)
                        elif color_scheme == 'asset_color':
                            i_usd_mesh_opt_tgt.fill_display_color(asset_color)
                        # for mesh
                        if i_obj_type_name == usd_configure.ObjType.Mesh:
                            if color_scheme == 'uv_map_color':
                                i_color_map = i_usd_mesh_opt_src.compute_vertex_color_map_from_uv_coord('st')
                                i_usd_mesh_opt_tgt.set_display_colors_as_vertex(i_color_map)
                            elif color_scheme == 'shell_color':
                                i_colors = i_usd_mesh_opt_src.get_colors_fom_shell(
                                    offset=i_index, seed=self._color_seed
                                )
                                i_usd_mesh_opt_tgt.set_display_colors_as_uniform(i_colors)
                    elif isinstance(color_scheme, dict):
                        pass
                #
                l_p.set_update()
        #
        component_paths = bsc_core.DccPathDagOpt(self._location_path).get_component_paths()
        if component_paths:
            component_paths.reverse()
            self._usd_stage_opt_tgt.set_default_prim(
                component_paths[1]
            )

        self._usd_stage_opt_tgt.export_to(self._file_path)


class GeometryDebugger(utl_fnc_obj_abs.AbsFncOptionBase):
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

        with utl_core.LogProgressRunner.create_as_bar(
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


class GeometryInfoXmlExporter(utl_fnc_obj_abs.AbsDccExporter):
    ROOT_LSTRIP = 'path_lstrip'
    GEOMETRY_FILE = 'geometry_file'
    OPTION = dict(
        path_lstrip=None,
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
            self._usd_stage_opt.append_sublayer(geometry_file_path)
        #
        self._usd_stage.Flatten()

    @classmethod
    def _get_info_raw(cls, stage, root=None, lstrip=None):
        info_configure = ctt_objects.Content(value=collections.OrderedDict())
        for prim in stage.TraverseAll():
            i_obj_type_name = prim.GetTypeName()
            obj_path = prim.GetPath().pathString
            #
            obj_path_ = bsc_core.DccPathDagMtd.get_dag_path_lstrip(obj_path, lstrip)
            if obj_path_:
                obj_properties = ctt_objects.Content(value=collections.OrderedDict())
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
            root=self._root, lstrip=self._option.get('path_lstrip')
        )
        #
        f = utl_dcc_objects.OsFile(self._file_path)
        f.set_write(raw)
        #
        # import os
        # base, ext = os.path.splitext(self._file_path)
        # self._usd_stage.Export(base + '.usda')


class FncGeometryExporter(utl_fnc_obj_abs.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        #
        default_prim_path=None,
        with_usda=False,
        #
        path_lstrip=None,
    )

    def __init__(self, *args, **kwargs):
        super(FncGeometryExporter, self).__init__(*args, **kwargs)
        #
        self._file_path = self.get('file')
        self._location_path = self.get('location')
        #
        self._output_stage = Usd.Stage.CreateInMemory()
        self._output_stage_opt = usd_core.UsdStageOpt(self._output_stage)
        #
        self._create_location_fnc_(self._output_stage, self._location_path)

    @classmethod
    def _create_location_fnc_(cls, stage, location):
        dag_path_comps = bsc_core.DccPathDagMtd.get_dag_component_paths(location, pathsep=usd_configure.Obj.PATHSEP)
        if dag_path_comps:
            dag_path_comps.reverse()
        #
        stage.GetPseudoRoot()
        for i in dag_path_comps:
            if i != usd_configure.Obj.PATHSEP:
                stage.DefinePrim(
                    i, usd_configure.ObjType.Xform
                )
        #
        default_prim_path = stage.GetPrimAtPath(dag_path_comps[1])
        stage.SetDefaultPrim(default_prim_path)

    def create_transform_opt(self, obj_path, use_override=False):
        if use_override is True:
            prim = self._output_stage.OverridePrim(obj_path, usd_configure.ObjType.Xform)
        else:
            prim = self._output_stage.DefinePrim(obj_path, usd_configure.ObjType.Xform)
        obj_opt = usd_dcc_operators.TransformOpt(prim)
        return obj_opt

    def create_mesh_opt(self, obj_path, use_override=False):
        if use_override is True:
            prim = self._output_stage.OverridePrim(obj_path, usd_configure.ObjType.Mesh)
        else:
            prim = self._output_stage.DefinePrim(obj_path, usd_configure.ObjType.Mesh)
        #
        obj_opt = usd_dcc_operators.MeshOpt(prim)
        return obj_opt

    def create_nurbs_curve_opt(self, obj_path, use_override=False):
        if use_override is True:
            prim = self._output_stage.OverridePrim(obj_path, usd_configure.ObjType.NurbsCurves)
        else:
            prim = self._output_stage.DefinePrim(obj_path, usd_configure.ObjType.NurbsCurves)
        #
        obj_opt = usd_dcc_operators.NurbsCurveOpt(prim)
        return obj_opt

    def create_basis_curves_opt(self, obj_path, use_override=False):
        if use_override is True:
            prim = self._output_stage.OverridePrim(obj_path, usd_configure.ObjType.BasisCurves)
        else:
            prim = self._output_stage.DefinePrim(obj_path, usd_configure.ObjType.BasisCurves)
        #
        obj_opt = usd_dcc_operators.BasisCurveOpt(prim)
        return obj_opt

    def _get_geometry_fnc_(self, obj_path):
        prim = self._output_stage.GetPrimAtPath(obj_path)
        if prim.IsValid() is True:
            return UsdGeom.Xform(prim)

    def _set_export_run_(self):
        default_prim_path = self.get('default_prim_path')
        if default_prim_path is not None:
            self._output_stage_opt.set_default_prim(
                default_prim_path
            )
        #
        self._output_stage_opt.export_to(self._file_path)

    def execute(self):
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
