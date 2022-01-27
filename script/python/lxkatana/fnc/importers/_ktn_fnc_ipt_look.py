# coding:utf-8
# noinspection PyUnresolvedReferences
from Katana import CacheManager, NodegraphAPI, KatanaFile

import lxbasic.objects as bsc_objects

from lxbasic import bsc_core

from lxutil import utl_core

from lxutil.fnc import utl_fnc_obj_abs

from lxutil.fnc.importers import utl_fnc_ipt_abs

from lxarnold import and_configure

import lxarnold.dcc.dcc_objects as and_dcc_objects

import lxarnold.dcc.dcc_operators as and_dcc_operators

from lxkatana.modifiers import _ktn_mdf_utility

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

from lxkatana.fnc.builders import _ktn_fnc_bdr_utility


class LookAssImporter(utl_fnc_obj_abs.AbsDccExporter):
    OPTION = dict(
        look_pass='default',
        root_lstrip=None,
        material_root='/root/materials',
        frame=None,
        auto_occlusion_assign=False,
        with_properties=True,
        with_visibilities=True,
    )
    WORKSPACE = _ktn_fnc_bdr_utility.AssetWorkspaceBuilder()
    CONFIGURE = WORKSPACE.get_configure()
    def __init__(self, file_path, root=None, option=None):
        super(LookAssImporter, self).__init__(file_path, root, option)
        #
        self._pass_name = self._option.get('look_pass')
        self._material_root = self._option.get('material_root')
        #
        self._dcc_importer_configure = bsc_objects.Configure(
            value=and_configure.Data.DCC_IMPORTER_CONFIGURE_PATH
        )
        #
        self._with_properties = self._option.get('with_properties') or False
        self._with_visibilities = self._option.get('with_visibilities') or False

    def _set_obj_universe_create_(self):
        obj_scene = and_dcc_objects.Scene(
            option=dict(
                shader_rename=True,
                root_lstrip='/root/world/geo',
                look_pass=self._pass_name
            )
        )
        obj_scene.set_load_from_dot_ass(
            self._file_path,
            root_lstrip='/root/world/geo'
        )
        self._and_obj_universe = obj_scene.universe

    def _set_look_create_(self, pass_name):
        self._ramp_dcc_objs = []
        #
        self.CONFIGURE = self.WORKSPACE.set_configure_create(pass_name=pass_name)
        self.CONFIGURE.set_flatten()
        # geometry
        mesh_and_type = self._and_obj_universe.get_obj_type(and_configure.ObjType.LYNXI_MESH)
        mesh_and_objs = mesh_and_type.get_objs() if mesh_and_type is not None else []
        curve_and_type = self._and_obj_universe.get_obj_type(and_configure.ObjType.LYNXI_CURVE)
        curve_and_objs = curve_and_type.get_objs() if curve_and_type is not None else []
        xgen_and_type = self._and_obj_universe.get_obj_type(and_configure.ObjType.LYNXI_XGEN_DESCRIPTION)
        xgen_and_objs = xgen_and_type.get_objs() if xgen_and_type is not None else []
        #
        and_geometries = mesh_and_objs + curve_and_objs + xgen_and_objs
        # material
        material_and_type = self._and_obj_universe.get_obj_type(and_configure.ObjType.LYNXI_MATERIAL)
        and_materials = material_and_type.get_objs()
        #
        method_args = [
            (self._set_look_materials_create_, (and_materials, )),
            (self._set_look_assigns_create_, (and_geometries, ))
        ]
        if method_args:
            g_p = utl_core.GuiProgressesRunner(maximum=len(method_args))
            for method, args in method_args:
                g_p.set_update()
                #
                method(*args)
            #
            g_p.set_stop()
        #
        self._set_ramp_build_()
    #
    def _set_ramp_build_(self):
        for i in self._ramp_dcc_objs:
            i._set_ramp_dict_write0_()
            i._set_ramp_dict_read_()
    @classmethod
    def _set_look_create_by_geometry_(cls, and_geometry):
        obj_universe = and_geometry.universe
        and_geometry_opt = and_dcc_operators.ShapeLookOpt(and_geometry)
        material_assigns = and_geometry_opt.get_material_assigns()
        for k, v in material_assigns.items():
            for i in v:
                i_and_material = obj_universe.get_obj(i)
    # material
    def _set_look_materials_create_(self, and_materials):
        if and_materials:
            pass_name = self._pass_name
            key = 'material_group'
            node_key = self.CONFIGURE.get('node.{}.keyword'.format(key))
            materials_merge_dcc_obj, materials_merge_ktn_obj, (x, y) = self.WORKSPACE.get_main_args(node_key, pass_name)
            #
            g_p = utl_core.GuiProgressesRunner(maximum=len(and_materials))
            for i_and_material in and_materials:
                g_p.set_update()
                self._set_look_material_create_(i_and_material)
            g_p.set_stop()

    def _set_look_material_create_(self, and_material):
        pass_name = self._pass_name
        #
        dcc_material, ktn_material = self.WORKSPACE.set_ng_material_create(
            name=and_material.name,
            pass_name=pass_name
        )
        dcc_material_group = dcc_material.get_parent()
        dcc_material_group_path = dcc_material_group.path
        #
        self._set_material_shaders_create_(and_material, ktn_material, dcc_material_group_path)
        #
        dcc_material.set_source_objs_layout()
        #
        show_obj = [i for i in dcc_material_group.get_children() if i.type_name == 'Material'][0]
        #
        self._set_tags_add_(show_obj, and_material.path, parent_port_path='shaders.parameters')

    def _set_tags_add_(self, dcc_obj, and_path, parent_port_path=None):
        pass_name = self._pass_name
        tags = [
            ('lx_file', self._file_path),
            ('lx_look_path', pass_name),
            ('lx_obj', and_path),
            ('lx_user', utl_core.System.get_user_name()),
            ('lx_time', utl_core.System.get_time())
        ]
        #
        for k, v in tags:
            if parent_port_path is not None:
                port_path = '{}.{}'.format(parent_port_path, k)
            else:
                port_path = k
            dcc_obj.get_port(port_path).set_create('string', v)

    def _set_material_shaders_create_(self, and_material, ktn_material, dcc_material_group_path):
        convert_dict = {
            'surface': 'arnoldSurface',
            'displacement': 'arnoldDisplacement',
            'volume': 'arnoldVolume'
        }
        pass_name = self._pass_name
        for shader_bind_port_name in convert_dict.keys():
            raw = and_material.get_input_port(shader_bind_port_name).get()
            if raw is not None:
                i_and_shader = self._and_obj_universe.get_obj(raw)
                if i_and_shader is not None:
                    shader_ktn_type = i_and_shader.type.name
                    i_shader_dcc_path = '{}/{}'.format(
                        dcc_material_group_path,
                        self.WORKSPACE.get_ng_shader_name(name=i_and_shader.name, pass_name=pass_name)
                    )
                    shader_dcc_obj = ktn_dcc_objects.Node(i_shader_dcc_path)
                    shader_ktn_obj, _ = shader_dcc_obj.get_dcc_instance('ArnoldShadingNode')
                    #
                    shader_dcc_obj.set_ktn_type(shader_ktn_type)
                    #
                    shader_ktn_obj.checkDynamicParameters()
                    self._set_shader_obj_ports_(i_and_shader, shader_dcc_obj)
                    #
                    shader_source_ktn_obj, shader_target_ktn_obj = (
                        shader_ktn_obj, ktn_material
                    )
                    shader_source_ktn_port_name, shader_target_ktn_port_name = (
                        'out',
                        convert_dict.get(shader_bind_port_name)
                    )
                    shader_source_ktn_port, shader_target_ktn_port = (
                        shader_source_ktn_obj.getOutputPort(shader_source_ktn_port_name),
                        shader_target_ktn_obj.getInputPort(shader_target_ktn_port_name)
                    )
                    shader_source_ktn_port.connect(shader_target_ktn_port)
                    #
                    self._set_shader_obj_node_graph_create_(i_and_shader, dcc_material_group_path)
                    #
                    self._set_tags_add_(shader_dcc_obj, i_and_shader.path)
                else:
                    utl_core.Log.set_module_warning_trace(
                        'shader create',
                        'obj="{}" is non-exists'.format(raw)
                    )

    def _set_shader_obj_node_graph_create_(self, and_shader, dcc_material_group_path):
        convert_dict = {}
        #
        pass_name = self._pass_name
        source_and_objs = and_shader.get_all_source_objs()
        for seq, source_and_obj in enumerate(source_and_objs):
            and_obj_type_name = source_and_obj.type.name
            #
            nod_ktn_type = source_and_obj.type.name
            nod_ktn_path = '{}/{}'.format(
                dcc_material_group_path,
                self.WORKSPACE.get_ng_shader_name(name=source_and_obj.name, pass_name=pass_name)
            )
            #
            if and_obj_type_name in ['ramp_float', 'ramp_rgb']:
                source_dcc_obj = ktn_dcc_objects.AndRamp(nod_ktn_path)
                self._ramp_dcc_objs.append(source_dcc_obj)
            else:
                source_dcc_obj = ktn_dcc_objects.Node(nod_ktn_path)
            #
            source_ktn_obj, _ = source_dcc_obj.get_dcc_instance('ArnoldShadingNode')
            source_dcc_obj.set_ktn_type(nod_ktn_type)
            #
            source_ktn_obj.checkDynamicParameters()
            self._set_shader_obj_ports_(source_and_obj, source_dcc_obj)
            #
            self._set_tags_add_(source_dcc_obj, and_shader.path)
        # connection
        and_obj_connections = and_shader.get_all_source_connections()
        for and_obj_connection in and_obj_connections:
            #
            source_and_obj, target_and_obj = (
                and_obj_connection.source_obj,
                and_obj_connection.target_obj
            )
            source_and_port, target_and_port = (
                and_obj_connection.source,
                and_obj_connection.target
            )
            nod_source_ar_port_path, nod_target_ar_port_path = (
                source_and_port.port_path, target_and_port.port_path
            )
            nod_source_ktn_obj_path, nod_target_ktn_obj_path = (
                '{}/{}'.format(
                    dcc_material_group_path,
                    self.WORKSPACE.get_ng_shader_name(name=source_and_obj.name, pass_name=pass_name)
                ),
                '{}/{}'.format(
                    dcc_material_group_path,
                    self.WORKSPACE.get_ng_shader_name(name=target_and_obj.name, pass_name=pass_name)
                )
            )
            nod_source_dcc_obj, nod_target_dcc_obj = (
                ktn_dcc_objects.Node(nod_source_ktn_obj_path),
                ktn_dcc_objects.Node(nod_target_ktn_obj_path)
            )
            nod_source_ktn_obj, nod_target_ktn_obj = (
                nod_source_dcc_obj.ktn_obj, nod_target_dcc_obj.ktn_obj
            )
            nod_source_ktn_port_path, nod_target_ktn_port_path = (
                '.'.join(['out'] + nod_source_ar_port_path.split('.')[1:]),
                convert_dict.get(nod_target_ar_port_path, nod_target_ar_port_path)
            )
            nod_source_ktn_port, nod_target_ktn_port = (
                nod_source_ktn_obj.getOutputPort(nod_source_ktn_port_path),
                nod_target_ktn_obj.getInputPort(nod_target_ktn_port_path)
            )
            if nod_source_ktn_port is None:
                utl_core.Log.set_error_trace(
                    'connection: "{}" >> "{}"'.format(source_and_port.path, target_and_port.path)
                )
                continue
            if nod_target_ktn_port is None:
                utl_core.Log.set_error_trace(
                    'connection: "{}" >> "{}"'.format(source_and_port.path, target_and_port.path)
                )
                continue
            nod_source_ktn_port.connect(nod_target_ktn_port)

    def _set_shader_obj_ports_(self, and_obj, dcc_obj):
        and_obj_type_name = and_obj.type.name
        convert_and_obj_type_names = self._dcc_importer_configure.get_branch_keys(
            'input-ports.to-katana'
        )
        for i_and_port in and_obj.get_input_ports():
            if i_and_port.get_is_element() is False and i_and_port.get_is_channel() is False:
                i_and_port_name = i_and_port.port_name
                dcc_port_key = i_and_port_name
                if and_obj_type_name in convert_and_obj_type_names:
                    convert_and_port_names = self._dcc_importer_configure.get_branch_keys(
                        'input-ports.to-katana.{}'.format(and_obj_type_name)
                    )
                    if i_and_port_name in convert_and_port_names:
                        dcc_port_key = self._dcc_importer_configure.get(
                            'input-ports.to-katana.{}.{}'.format(and_obj_type_name, i_and_port_name)
                        )
                #
                enable_dcc_port = dcc_obj.get_port('parameters.{}.enable'.format(dcc_port_key))
                value_dcc_port = dcc_obj.get_port('parameters.{}.value'.format(dcc_port_key))
                raw = i_and_port.get()
                if value_dcc_port.get_is_exists() is True:
                    if dcc_port_key in ['ramp_Knots', 'ramp_Interpolation', 'ramp_Floats', 'ramp_Colors']:
                        dcc_obj._set_ramp_value_update_(dcc_port_key, raw)
                    else:
                        value = raw
                        if i_and_port.get_is_enumerate():
                            ktn_type = value_dcc_port.type
                            if ktn_type == 'string':
                                value = str(i_and_port.get_as_index())
                            elif ktn_type == 'number':
                                value = i_and_port.get_as_index()
                        #
                        if value is not None:
                            if i_and_port.get_is_value_changed() is True:
                                enable_dcc_port.set(True)
                                value_dcc_port.set(value)
                else:
                    if i_and_port_name == 'name':
                        dcc_obj.get_port('arnold_name').set_create('string', raw)
                    else:
                        utl_core.Log.set_module_warning_trace(
                            'shader-port-set',
                            'atr-path="{}" is non-exists'.format(value_dcc_port.path)
                        )

    def _set_look_assigns_create_(self, and_geometries):
        if and_geometries:
            pass_name = self._pass_name
            #
            key = 'material_assign'
            node_key = self.CONFIGURE.get('node.{}.keyword'.format(key))
            dcc_group, ktn_group, pos = self.WORKSPACE.get_group_args(node_key, group_key='definition', pass_name=pass_name)
            dcc_group.set_children_clear()
            g_p = utl_core.GuiProgressesRunner(maximum=len(and_geometries))
            for i_gmt_seq, i_and_gmt in enumerate(and_geometries):
                g_p.set_update()
                self._set_look_geometry_material_assign_create_(i_and_gmt)
            #
            g_p.set_stop()
            #
            key = 'property_assign'
            node_key = self.CONFIGURE.get('node.{}.keyword'.format(key))
            dcc_group, ktn_group, pos = self.WORKSPACE.get_group_args(node_key, group_key='definition', pass_name=pass_name)
            dcc_group.set_children_clear()
            #
            g_p = utl_core.GuiProgressesRunner(maximum=len(and_geometries))
            for i_gmt_seq, i_and_gmt in enumerate(and_geometries):
                g_p.set_update()
                self._set_look_geometry_properties_create_(i_and_gmt)
            #
            g_p.set_stop()
    # material assign
    def _set_look_geometry_material_assign_create_(self, and_geometry, geometry_seq=None):
        pass_name = self._pass_name
        #
        geometry_root = self.CONFIGURE.get('option.geometry_root')
        material_root = self.CONFIGURE.get('option.material_root')
        #
        material_paths = and_geometry.get_input_port('material').get()
        if material_paths:
            and_material = self._and_obj_universe.get_obj(material_paths[0])
            dcc_material_name = self.WORKSPACE.get_ng_material_name(and_material.name, pass_name)
            assign_name = and_geometry.name
            if geometry_seq is not None:
                assign_name = '{}__{}'.format(and_geometry.name, geometry_seq)
            #
            dcc_material_assign, ktn_material_assign = self.WORKSPACE.set_ng_material_assign_create(
                name=assign_name,
                assign=(
                    '{}{}'.format(geometry_root, and_geometry.path),
                    '{}/{}'.format(material_root, dcc_material_name)
                ),
                pass_name=pass_name
            )
            #
            self._set_tags_add_(dcc_material_assign, and_geometry.path)
    #
    def _set_look_geometry_properties_create_(self, and_geometry, geometry_seq=None):
        pass_name = self._pass_name
        asset_root = self.CONFIGURE.get('option.asset_root')
        assign_name = and_geometry.name
        if geometry_seq is not None:
            assign_name = '{}__{}'.format(and_geometry.name, geometry_seq)
        #
        dcc_properties, ktn_properties = self.WORKSPACE.set_ng_properties_create(
            name=assign_name,
            pass_name=pass_name
        )
        #
        shape_path = '{}'.format('/'.join([asset_root] + and_geometry.path.split('/')[2:]))
        dcc_properties.get_port('CEL').set(shape_path)
        #
        and_geometry_opt = and_dcc_operators.ShapeLookOpt(and_geometry)
        #
        if self._with_properties is True:
            self._set_geometry_obj_property_ports_(and_geometry_opt, dcc_properties)
        if self._with_visibilities is True:
            self._set_geometry_obj_visibility_ports_(and_geometry_opt, dcc_properties)
        #
        self._set_tags_add_(dcc_properties, and_geometry.path)
    @classmethod
    def _set_geometry_obj_property_ports_(cls, and_geometry_opt, dcc_geometry):
        convert_dict = dict(
            subdiv_iterations='iterations'
        )
        and_geometry = and_geometry_opt.obj
        properties = and_geometry_opt.get_properties()
        for i_and_port_name, v in properties.items():
            i_and_port = and_geometry.get_input_port(i_and_port_name)
            #
            i_dcc_port_name = i_and_port_name
            if i_and_port_name in convert_dict:
                i_dcc_port_name = convert_dict[i_and_port_name]
            if i_and_port.get_is_value_changed() is True:
                enable_ktn_port_name = 'args.arnoldStatements.{}.enable'.format(i_dcc_port_name)
                enable_dcc_port = dcc_geometry.get_port(enable_ktn_port_name)
                if enable_dcc_port.get_is_exists() is True:
                    enable_dcc_port.set(True)
                else:
                    utl_core.Log.set_warning_trace(
                        'unknown-port-name="{}"'.format(i_dcc_port_name)
                    )
                #
                value_ktn_port_name = 'args.arnoldStatements.{}.value'.format(i_dcc_port_name)
                value_dcc_port = dcc_geometry.get_port(value_ktn_port_name)
                if value_dcc_port.get_is_exists() is True:
                    raw = i_and_port.get()
                    if value_dcc_port.type == 'number':
                        if i_and_port.get_is_enumerate():
                            raw = i_and_port.get_as_index()
                    #
                    if raw is not None:
                        value_dcc_port.set(raw)
    @classmethod
    def _set_geometry_obj_visibility_ports_(cls, and_geometry_opt, dcc_geometry):
        convert_dict = dict()
        and_geometry = and_geometry_opt.obj
        properties = and_geometry_opt.get_visibilities()
        for i_and_port_name, v in properties.items():
            i_and_port = and_geometry.get_input_port(i_and_port_name)
            #
            i_dcc_port_name = 'AI_RAY_{}'.format(i_and_port_name.upper())
            # if i_and_port.get_is_value_changed() is True:
            enable_ktn_port_name = 'args.arnoldStatements.visibility.{}.enable'.format(i_dcc_port_name)
            enable_dcc_port = dcc_geometry.get_port(enable_ktn_port_name)
            if enable_dcc_port.get_is_exists() is True:
                enable_dcc_port.set(True)
            else:
                utl_core.Log.set_warning_trace(
                    'unknown-port-name="{}"'.format(i_dcc_port_name)
                )
            #
            value_ktn_port_name = 'args.arnoldStatements.visibility.{}.value'.format(i_dcc_port_name)
            value_dcc_port = dcc_geometry.get_port(value_ktn_port_name)
            if value_dcc_port.get_is_exists() is True:
                raw = i_and_port.get()
                if value_dcc_port.type == 'number':
                    if i_and_port.get_is_enumerate():
                        raw = i_and_port.get_as_index()
                if raw is not None:
                    value_dcc_port.set(raw)
    @_ktn_mdf_utility.set_undo_mark_mdf
    def set_run(self):
        self._set_obj_universe_create_()
        #
        self._set_look_create_(self._pass_name)
        #
        auto_occlusion_assign = self._option['auto_occlusion_assign']
        if auto_occlusion_assign is True:
            self.WORKSPACE.set_auto_occlusion_assign(pass_name=self._pass_name)
    @classmethod
    def _set_pst_run_(cls):
        for i in ktn_dcc_objects.AndShaders().get_objs():
            if i.get_port('nodeType').get() in ['ramp_float', 'ramp_rgb']:
                a = ktn_dcc_objects.AndRamp(i.path)
                a._set_ramp_dict_read_()


class LookYamlImporter(utl_fnc_ipt_abs.AbsDccLookYamlImporter):
    def __init__(self, option):
        super(LookYamlImporter, self).__init__(option)
