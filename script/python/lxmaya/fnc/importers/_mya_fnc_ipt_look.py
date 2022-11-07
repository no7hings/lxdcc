# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

from lxutil import utl_core

from lxmaya_fnc import ma_fnc_configure, ma_fnc_core

import lxmaya.modifiers as mya_modifiers

from lxmaya import ma_configure, ma_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_operators as mya_dcc_operators

import lxobj.core_objects as core_objects

import lxbasic.objects as bsc_objects

from lxutil.fnc import utl_fnc_obj_abs

from lxutil.fnc.importers import utl_fnc_ipt_abs

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxarnold import and_configure

import lxarnold.dcc.dcc_objects as and_dcc_objects

import lxarnold.dcc.dcc_operators as and_dcc_operators

from lxbasic import bsc_core


class LookAssignImporter(object):
    def __init__(self, file_path, root=None, look='default', root_lstrip=None):
        self._file_path = file_path
        self._root = root
        self._look = look
        self._path_lstrip = root_lstrip
        #
        self._raw_content = bsc_objects.Configure(value=self._file_path)
        self._look_content = ma_fnc_core.LookContent(self._file_path)

    def set_run(self):
        g = mya_dcc_objects.Group(self._root)
        #
        var = 'geometry'
        #
        geometry_paths = g.get_all_shape_paths(include_obj_type=ma_fnc_configure.Look.GEOMETRY_TYPES)
        for seq, geometry_path in enumerate(geometry_paths):
            obj_type = mya_dcc_objects.Node(geometry_path).type
            if obj_type == ma_configure.Util.MESH_TYPE:
                mesh_obj = mya_dcc_objects.Mesh(geometry_path)
                geometry_mtd = mya_dcc_operators.MeshOpt(mesh_obj)
                look_opt = mya_dcc_operators.MeshLookOpt(mesh_obj)
                #
                points_uuid = geometry_mtd.get_points_as_uuid(ordered=True)
                face_vertices_uuid = geometry_mtd.get_face_vertices_as_uuid()
                key_dict = {
                    ma_fnc_configure.Look.POINTS_UUID: points_uuid,
                    ma_fnc_configure.Look.FACE_VERTICES_UUID: face_vertices_uuid,
                }
                material_assigns = self._look_content.get_material_assigns(self._look, var, key_dict)
                if material_assigns:
                    look_opt.set_material_assigns(material_assigns)
                else:
                    utl_core.Log.set_module_warning_trace(
                        'look-assign-importer',
                        'material-assigns: "{}" is Non-exists'.format(geometry_path)
                    )
                properties = self._look_content.get_properties(self._look, var, key_dict)
                if properties:
                    look_opt.set_properties(properties)
                else:
                    utl_core.Log.set_module_warning_trace(
                        'look-assign-importer',
                        'properties: "{}" is Non-exists'.format(geometry_path)
                    )
                visibilities = self._look_content.get_visibilities(self._look, var, key_dict)
                if visibilities:
                    look_opt.set_visibilities(visibilities)
                else:
                    utl_core.Log.set_module_warning_trace(
                        'look-assign-importer',
                        'visibilities: "{}" is Non-exists'.format(geometry_path)
                    )
        #
        var = 'hair'
        hair_paths = g.get_all_shape_paths(include_obj_type=ma_fnc_configure.Look.HAIR_TYPES)
        for seq, hair_path in enumerate(hair_paths):
            obj_type = mya_dcc_objects.Node(hair_path).type
            if obj_type == ma_configure.Util.XGEN_DESCRIPTION:
                xgen_description = mya_dcc_objects.XgenDescription(hair_path)
                xgen_description_opt = mya_dcc_operators.XgenDescriptionOpt(xgen_description)
                look_opt = mya_dcc_operators.XgenDescriptionLookMtd(xgen_description)
                name = xgen_description_opt.get_name()
                #
                key_dict = {
                    ma_fnc_configure.Look.NAME: name,
                }
                material_assigns = self._look_content.get_material_assigns(self._look, var, key_dict)
                if material_assigns:
                    look_opt.set_material_assigns(material_assigns)
                #
                properties = self._look_content.get_properties(self._look, var, key_dict)
                if properties:
                    look_opt.set_properties(properties)
                #
                visibilities = self._look_content.get_visibilities(self._look, var, key_dict)
                if visibilities:
                    look_opt.set_visibilities(visibilities)


class LookAssImporter(utl_fnc_obj_abs.AbsFncOptionMethod):
    PLUG_NAME = 'mtoa'
    OPTION = dict(
        look_pass='default',
        root_lstrip=None,
        assign_selection=False,
        #
        with_material=True,
        with_assign=True,
        #
        name_join_time_tag=False
    )
    def __init__(self, option=None):
        super(LookAssImporter, self).__init__(option)

        self._file_path = self.get('file')
        self._location = self.get('location')
        #
        self._look_pass_name = self.get('look_pass')
        self._assign_selection_enable = self.get('assign_selection')
        self._name_join_time_tag = self.get('name_join_time_tag')
        #
        self._dcc_importer_configure = bsc_objects.Configure(
            value=and_configure.Data.DCC_IMPORTER_CONFIGURE_PATH
        )
        #
        is_plug_loaded = cmds.pluginInfo(self.PLUG_NAME, query=True, loaded=True)
        if is_plug_loaded is False:
            cmds.loadPlugin(self.PLUG_NAME, quiet=1)
        #
        self.__set_obj_universe_create_()
    #
    def __set_obj_universe_create_(self):
        obj_scene = and_dcc_objects.Scene(
            option=dict(
                shader_rename=True,
                look_pass=self._look_pass_name
            )
        )
        file_ = utl_dcc_objects.OsFile(self._file_path)
        if file_.get_is_exists() is True:
            if self._name_join_time_tag is True:
                time_tag = bsc_core.IntegerOpt(
                    int(file_.get_modify_timestamp())
                ).set_encode_to_36()
            else:
                time_tag = None
            #
            obj_scene.set_load_from_dot_ass(
                self._file_path,
                root_lstrip='/root/world/geo',
                time_tag=time_tag
            )
        else:
            raise RuntimeError()
        #
        self._and_obj_universe = obj_scene.universe
    @mya_modifiers.set_undo_mark_mdf
    def set_run(self):
        self.__set_look_create_()

    def __set_look_create_(self):
        # geometry
        mesh_and_type = self._and_obj_universe.get_obj_type(and_configure.ObjType.LYNXI_MESH)
        mesh_and_objs = mesh_and_type.get_objs() if mesh_and_type is not None else []
        curve_and_type = self._and_obj_universe.get_obj_type(and_configure.ObjType.LYNXI_CURVE)
        curve_and_objs = curve_and_type.get_objs() if curve_and_type is not None else []
        xgen_and_type = self._and_obj_universe.get_obj_type(and_configure.ObjType.LYNXI_XGEN_DESCRIPTION)
        xgen_and_objs = xgen_and_type.get_objs() if xgen_and_type is not None else []
        #
        geometry_and_objs = mesh_and_objs + curve_and_objs + xgen_and_objs
        # material
        material_and_type = self._and_obj_universe.get_obj_type(and_configure.ObjType.LYNXI_MATERIAL)
        if material_and_type is not None:
            material_and_objs = material_and_type.get_objs()
            #
            method_args = [
                (self.__set_look_materials_create_, (material_and_objs, ), self.get('with_material')),
                (self.__set_look_assigns_create_, (geometry_and_objs,), self.get('with_assign'))
            ]
            if method_args:
                with utl_core.gui_progress(maximum=len(method_args), label='execute look create method') as g_p:
                    for i_method, i_args, i_enable in method_args:
                        g_p.set_update()
                        if i_enable is True:
                            i_method(*i_args)
        else:
            raise RuntimeError(
                utl_core.Log.set_module_error_trace(
                    'look import',
                    'material(s) is not found'
                )
            )
    @classmethod
    def _set_look_create_by_geometry_obj_path_(cls, geometry_and_obj):
        obj_universe = geometry_and_obj.universe
        if geometry_and_obj is not None:
            geometry_and_obj_path = geometry_and_obj.path
            geometry_dcc_dag_path = core_objects.ObjDagPath(geometry_and_obj_path).set_translate_to(
                ma_configure.Util.OBJ_PATHSEP
            )
            geometry_and_obj_opt = and_dcc_operators.ShapeLookOpt(geometry_and_obj)
            geometry_dcc_obj = mya_dcc_objects.Geometry(geometry_dcc_dag_path.path)
            geometry_dcc_obj_opt = mya_dcc_operators.ShapeLookOpt(geometry_dcc_obj)
            material_assigns = geometry_and_obj_opt.get_material_assigns()
            for k, v in material_assigns.items():
                for i in v:
                    material_and_obj = obj_universe.get_obj(i)
                    # self.__set_look_material_create_(material_and_obj)
                    # self.__set_look_geometry_material_assign_create_(geometry_and_obj_opt, geometry_dcc_obj_opt)
                    # self.__set_look_geometry_properties_create_(geometry_and_obj_opt, geometry_dcc_obj_opt)
                    # self._set_look_geometry_visibilities_create_(geometry_and_obj_opt, geometry_dcc_obj_opt)

    def __set_look_materials_create_(self, material_and_objs):
        if material_and_objs:
            with utl_core.gui_progress(maximum=len(material_and_objs), label='create material') as g_p:
                for material_seq, material_and_obj in enumerate(material_and_objs):
                    g_p.set_update()
                    self.__set_look_material_create_(material_and_obj)
    #
    def __set_look_material_create_(self, material_and_obj):
        material_and_obj_name = material_and_obj.name
        material_dcc_obj_name = material_and_obj_name
        #
        material_dcc_obj = mya_dcc_objects.Material(material_dcc_obj_name)
        if material_dcc_obj.get_is_exists() is False:
            material_dcc_obj.set_create(mya_dcc_objects.Material.OBJ_TYPE)
            #
            self.__set_material_shaders_create_(material_and_obj, material_dcc_obj)
            #
            ma_core.CmdObjOpt(material_dcc_obj.path).set_customize_attributes_create(
                dict(
                    arnold_name=material_and_obj_name
                )
            )
    #
    def __set_material_shaders_create_(self, material_and_obj, material_dcc_obj):
        convert_dict = {
            'surface': 'surfaceShader',
            'displacement': 'displacementShader',
            'volume': 'volumeShader'
        }
        for i_shader_and_bind_port_name in convert_dict.keys():
            raw = material_and_obj.get_input_port(i_shader_and_bind_port_name).get()
            if raw is not None:
                shader_and_obj = self._and_obj_universe.get_obj(raw)
                shader_dcc_obj, is_create = self.__set_material_shader_create_(shader_and_obj)
                if shader_dcc_obj is not None:
                    # debug
                    # do not check create, material can use same shader
                    i_shader_dcc_bind_port_name = convert_dict[i_shader_and_bind_port_name]

                    i_shader_and_source_and_port = shader_and_obj.get_output_ports()[0]
                    i_shader_and_source_and_port_path = i_shader_and_source_and_port.port_path
                    if i_shader_and_source_and_port.get_is_channel():
                        key = 'output-ports.to-maya.channels.{}'.format(i_shader_and_source_and_port_path)
                    else:
                        key = 'output-ports.to-maya.{}'.format(i_shader_and_source_and_port_path)

                    source_dcc_port_path = self._dcc_importer_configure.get(key)

                    shader_dcc_obj.get_port(source_dcc_port_path).set_target(
                        material_dcc_obj.get_port(i_shader_dcc_bind_port_name)
                    )

    def __set_material_shader_create_(self, shader_and_obj):
        create_args = self.__set_shader_create_(shader_and_obj)
        if create_args is not None:
            shader_dcc_obj, is_create = create_args
            if is_create is True:
                self.__set_shader_ports_(shader_and_obj, shader_dcc_obj)
                self.__set_shader_node_graph_create_(shader_and_obj)
                #
                ma_core.CmdObjOpt(shader_dcc_obj.path).set_customize_attributes_create(
                    dict(
                        arnold_name=shader_and_obj.name
                    )
                )
            return shader_dcc_obj, is_create

    def _set_material_shader_node_graph_rename_(self, material_seq, shader_and_bind_port_name, shader_and_obj):
        all_source_objs = shader_and_obj.get_all_source_objs()
        label = 'material__{}__{}'.format(material_seq, shader_and_bind_port_name)
        for obj_seq, and_obj in enumerate(all_source_objs):
            self._set_shader_obj_rename_(obj_seq + 1, and_obj, label)
        self._set_shader_obj_rename_(0, shader_and_obj, label)
    @classmethod
    def _set_shader_obj_rename_(cls, shader_seq, shader_and_obj, label):
        and_obj_name = shader_and_obj.name
        dcc_obj_name = and_obj_name
        obj_type_name = shader_and_obj.type.name
        new_obj_name = '{}__{}__{}'.format(label, obj_type_name, shader_seq)
        shader_dcc_obj = mya_dcc_objects.AndShader(dcc_obj_name)
        shader_dcc_obj.set_rename(new_obj_name)

    def __set_shader_node_graph_create_(self, and_obj):
        source_and_objs = and_obj.get_all_source_objs()
        for seq, source_and_obj in enumerate(source_and_objs):
            _ = self.__set_shader_create_(source_and_obj)
            if _ is not None:
                source_dcc_obj, is_create = _
                self.__set_shader_ports_(source_and_obj, source_dcc_obj)
        #
        and_connections = and_obj.get_all_source_connections()
        self._set_connections_create_(and_connections)
    
    def _set_connections_create_(self, and_connections):
        for i_and_connection in and_connections:
            self._set_connection_create_(i_and_connection)

    def _set_connection_create_(self, and_connection):
        source_and_obj, target_and_obj = (
            and_connection.source_obj, and_connection.target_obj
        )
        source_and_obj_type_name, target_and_obj_type_name = (
            source_and_obj.type.name, target_and_obj.type.name
        )
        source_and_port, target_and_port = (
            and_connection.source, and_connection.target
        )
        #
        source_and_port_path, target_and_port_path = (
            source_and_port.port_path, target_and_port.port_path
        )
        if source_and_port.get_is_channel():
            key = 'output-ports.to-maya.channels.{}'.format(source_and_port_path)
        else:
            key = 'output-ports.to-maya.{}'.format(source_and_port_path)
        #
        source_dcc_port_path = self._dcc_importer_configure.get(key)
        #
        if target_and_port.get_is_channel():
            a, b = target_and_port_path.split('.')
            target_dcc_port_path = '{0}.{0}{1}'.format(a, b.upper())
        else:
            target_dcc_port_path = bsc_objects.StrUnderline(target_and_port_path).to_camelcase()
        #
        and_obj_type_names = self._dcc_importer_configure.get_branch_keys(
            'input-ports.to-maya'
        )
        if target_and_obj_type_name in and_obj_type_names:
            and_port_names = self._dcc_importer_configure.get_branch_keys(
                'input-ports.to-maya.{}'.format(target_and_obj_type_name)
            )
            if target_and_port_path in and_port_names:
                if target_and_port.get_is_channel():
                    a, b = target_and_port_path.split('.')
                    a = self._dcc_importer_configure.get(
                        'input-ports.to-maya.{}.{}'.format(target_and_obj_type_name, target_and_port_path)
                    )
                    target_dcc_port_path = '{0}.{0}{1}'.format(a, b.upper())
                else:
                    target_dcc_port_path = self._dcc_importer_configure.get(
                        'input-ports.to-maya.{}.{}'.format(target_and_obj_type_name, target_and_port_path)
                    )

        source_and_obj_name, target_and_obj_name = (
            source_and_obj.name, target_and_obj.name
        )
        #
        source_dcc_obj_name, target_dcc_obj_name = (
            source_and_obj_name, target_and_obj_name
        )

        source_dcc_obj, target_dcc_obj = (
            mya_dcc_objects.AndShader(source_dcc_obj_name), mya_dcc_objects.AndShader(target_and_obj_name)
        )
        #
        if source_dcc_obj.get_is_exists() is False:
            utl_core.Log.set_module_warning_trace(
                'connection create',
                'obj="{}" is non-exists'.format(source_and_obj.path)
            )
            return

        if target_dcc_obj.get_is_exists() is False:
            utl_core.Log.set_module_warning_trace(
                'connection create',
                'obj="{}" is non-exists'.format(target_and_obj.path)
            )
            return

        if source_dcc_port_path is None:
            return

        source_dcc_port, target_dcc_port = (
            source_dcc_obj.get_port(source_dcc_port_path), target_dcc_obj.get_port(target_dcc_port_path)
        )
        if source_dcc_port.get_is_exists() is False:
            utl_core.Log.set_module_warning_trace(
                'connection create', 'atr-src-path:"{}" is non-exists'.format(source_dcc_port.path)
            )
            return

        if target_dcc_port.get_is_exists() is False:
            utl_core.Log.set_module_warning_trace(
                'connection create', 'atr-tgt-path:"{}" is non-exists'.format(target_dcc_port.path)
            )
            return

        source_dcc_port.set_target(target_dcc_port, validation=True)

    def __set_shader_create_(self, and_obj):
        and_obj_type_name = and_obj.type.name
        all_and_obj_types = mya_dcc_objects.AndShader.CATEGORY_DICT.keys()
        dcc_type = self._dcc_importer_configure.get('shaders.to-maya.{}'.format(and_obj_type_name))
        if dcc_type is not None:
            and_obj_name = and_obj.name
            dcc_obj_name = and_obj_name
            dcc_obj = mya_dcc_objects.AndShader(dcc_obj_name)
            if dcc_obj.get_is_exists() is False:
                dcc_obj.set_create(dcc_type)
                #
                ma_core.CmdObjOpt(dcc_obj.path).set_customize_attributes_create(
                    dict(
                        arnold_name=and_obj.get_port('name').get()
                    )
                )
                return dcc_obj, True
            return dcc_obj, False
        else:
            if and_obj_type_name in all_and_obj_types:
                and_obj_name = and_obj.name
                dcc_obj_name = and_obj_name
                dcc_obj = mya_dcc_objects.AndShader(dcc_obj_name)
                if dcc_obj.get_is_exists() is False:
                    dcc_obj.set_create(and_obj_type_name)
                    ma_core.CmdObjOpt(dcc_obj.path).set_customize_attributes_create(
                        dict(
                            arnold_name=and_obj.get_port('name').get()
                        )
                    )
                    return dcc_obj, True
                return dcc_obj, False
            else:
                utl_core.Log.set_module_warning_trace(
                    'shader create',
                    'obj-type="{}" is not available'.format(and_obj_type_name)
                )
    #
    def __set_shader_ports_(self, and_obj, dcc_obj):
        and_obj_type_name = and_obj.type.name
        and_obj_type_names = self._dcc_importer_configure.get_branch_keys(
            'input-ports.to-maya'
        )
        for and_port in and_obj.get_input_ports():
            if and_port.get_is_element() is False and and_port.get_is_channel() is False:
                and_port_name = and_port.port_name
                #
                dcc_port_name = bsc_objects.StrUnderline(and_port_name).to_camelcase()
                #
                if and_obj_type_name in and_obj_type_names:
                    and_port_names = self._dcc_importer_configure.get_branch_keys(
                        'input-ports.to-maya.{}'.format(and_obj_type_name)
                    )
                    if and_port_name in and_port_names:
                        dcc_port_name = self._dcc_importer_configure.get(
                            'input-ports.to-maya.{}.{}'.format(and_obj_type_name, and_port_name)
                        )
                #
                dcc_port = dcc_obj.get_port(dcc_port_name)
                if dcc_port.get_is_exists() is True:
                    if and_port.get_is_enumerate():
                        raw = and_port.get_as_index()
                    else:
                        raw = and_port.get()
                    #
                    if raw is not None:
                        dcc_port.set(raw)
                elif dcc_port.get_query_is_exists():
                    raw = and_port.get()
                    if raw is not None:
                        dcc_port._set_as_array_(raw)
                else:
                    if and_port_name == 'name':
                        pass
                    else:
                        utl_core.Log.set_module_warning_trace(
                            'shader-port set',
                            'attribute="{}" is non-exists'.format(dcc_port.path)
                        )

    def __set_look_assigns_create_(self, geometry_and_objs):
        if geometry_and_objs:
            with utl_core.gui_progress(maximum=len(geometry_and_objs), label='create assign') as g_p:
                for geometry_seq, geometry_and_obj in enumerate(geometry_and_objs):
                    g_p.set_update()
                    #
                    geometry_and_obj_path = geometry_and_obj.path
                    geometry_dcc_dag_path = core_objects.ObjDagPath(geometry_and_obj_path).set_translate_to(
                        ma_configure.Util.OBJ_PATHSEP
                    )
                    geometry_dcc_obj = mya_dcc_objects.Geometry(geometry_dcc_dag_path.path)
                    self._set_geometry_assign_create_(geometry_and_obj, geometry_dcc_obj)
            #
            if self._assign_selection_enable is True:
                self._set_look_assign_selection_(geometry_and_objs)

    def _set_geometry_assign_create_(self, geometry_and_obj, geometry_dcc_obj):
        geometry_and_obj_opt = and_dcc_operators.ShapeLookOpt(geometry_and_obj)
        geometry_dcc_obj_opt = mya_dcc_operators.ShapeLookOpt(geometry_dcc_obj)
        if geometry_dcc_obj.get_is_exists() is True:
            self.__set_look_geometry_material_assign_create_(geometry_and_obj_opt, geometry_dcc_obj_opt)
            self.__set_look_geometry_properties_create_(geometry_and_obj_opt, geometry_dcc_obj_opt)
            self._set_look_geometry_visibilities_create_(geometry_and_obj_opt, geometry_dcc_obj_opt)

    def _set_look_assign_selection_(self, geometry_and_objs):
        selection_paths = mya_dcc_objects.Selection.get_selected_paths(include=['mesh'])
        for i_geometry_path in selection_paths:
            i_and_geometry = geometry_and_objs[0]
            i_dcc_geometry = mya_dcc_objects.Mesh(i_geometry_path)
            self._set_geometry_assign_create_(i_and_geometry, i_dcc_geometry)

    def __set_look_geometry_material_assign_create_(self, geometry_and_obj_opt, geometry_dcc_obj_opt):
        material_assigns = geometry_and_obj_opt.get_material_assigns()
        for k, v in material_assigns.items():
            for i in v:
                i_and_material = self._and_obj_universe.get_obj(i)
                i_and_material_name = i_and_material.name
                i_dcc_material = i_and_material_name
                geometry_dcc_obj_opt.set_material(i_dcc_material)
    @classmethod
    def __set_look_geometry_properties_create_(cls, geometry_and_obj_opt, geometry_dcc_obj_opt):
        mya_properties = geometry_and_obj_opt.set_properties_convert_to(application='maya')
        geometry_dcc_obj_opt.set_properties(mya_properties)
    @classmethod
    def _set_look_geometry_visibilities_create_(cls, geometry_and_obj_opt, geometry_dcc_obj_opt):
        mya_visibilities = geometry_and_obj_opt.set_visibilities_convert_to(application='maya')
        geometry_dcc_obj_opt.set_visibilities(mya_visibilities)


class LookYamlImporter(utl_fnc_ipt_abs.AbsDccLookYamlImporter):
    def __init__(self, option):
        super(LookYamlImporter, self).__init__(option)
        self._obj_index = 0
        self._name_dict = {}
        self._connections = []
    @mya_modifiers.set_undo_mark_mdf
    def set_run(self):
        #
        look_pass_name = self._option['look_pass']
        version_name = self._option['version']
        #
        roots = self._raw.get_branch_keys('root')
        for i_root in roots:
            self._set_obj_create_(
                'root', i_root, i_root, customize=True
            )
        #
        materials = self._raw.get_branch_keys('material')
        for i_material in materials:
            type_name = self._raw.get(
                '{}.{}.properties.type'.format('material', i_material)
            ).split('/')[-1]
            #
            new_name = '{}__{}__{}__{}'.format(
                look_pass_name, version_name, type_name, len(self._name_dict)
            )
            self._name_dict[i_material] = new_name
            self._set_obj_create_(
                'material', i_material, new_name, create=True, definition=True
            )
        #
        nodes = self._raw.get_branch_keys('node-graph')
        for i_node in nodes:
            type_name = self._raw.get(
                '{}.{}.properties.type'.format('node-graph', i_node)
            ).split('/')[-1]
            #
            new_name = '{}__{}__{}__{}'.format(
                look_pass_name, version_name, type_name, len(self._name_dict)
            )
            self._name_dict[i_node] = new_name
            self._set_obj_create_(
                'node-graph', i_node, new_name, create=True, definition=True, clear_array_ports=True
            )
        # transforms
        transforms = self._raw.get_branch_keys('transform')
        for i_transform in transforms:
            self._set_obj_create_(
                'transform', i_transform, i_transform, definition=True
            )
        #
        self._set_obj_connections_create_()
        # geometries
        geometries = self._raw.get_branch_keys('geometry')
        for i_geometry in geometries:
            self._set_obj_create_(
                'geometry', i_geometry, i_geometry, assigns=True
            )

    def _set_obj_create_(self, scheme, obj_key, obj_path, create=False, definition=False, customize=False, assigns=False, clear_array_ports=False):
        if create is True:
            type_name = self._raw.get(
                '{}.{}.properties.type'.format(scheme, obj_key)
            ).split('/')[-1]
            #
            if ma_core.CmdObjOpt._get_is_exists_(obj_path) is True:
                ma_core.CmdObjOpt(obj_path).set_file_new()
            #
            ma_core.CmdObjOpt._set_create_(obj_path, type_name)
        #
        if ma_core.CmdObjOpt._get_is_exists_(obj_path) is True:
            obj = ma_core.CmdObjOpt(obj_path)
            if clear_array_ports is True:
                obj.set_array_ports_clear()
            #
            if definition is True:
                definition_attributes = self._raw.get(
                    '{}.{}.properties.definition-attributes'.format(scheme, obj_key),
                )
                if obj_path in self._name_dict:
                    new_name = self._name_dict[obj_path]
                    obj_path = new_name
                self._set_obj_definition_attributes_(obj_path, definition_attributes)
            #
            if customize is True:
                customize_attributes = self._raw.get(
                    '{}.{}.properties.customize-attributes'.format(scheme, obj_key),
                )
                if obj_path in self._name_dict:
                    new_name = self._name_dict[obj_path]
                    obj_path = new_name
                self._set_obj_customize_attributes_(obj_path, customize_attributes)

            if assigns is True:
                material_assigns = self._raw.get(
                    '{}.{}.properties.material-assigns'.format(scheme, obj_key),
                )
                self._set_obj_material_assign_create_(obj_path, material_assigns)

    def _set_obj_customize_attributes_(self, obj_path, attributes):
        for port_path, v in attributes.items():
            type_name = v['type'].split('/')[-1]
            value = v.get('value')
            atr_path_src = v.get('connection')
            if atr_path_src is None:
                enumerate_strings = v.get(
                    'enumerate-strings'
                )
                if ma_core.CmdPortOpt._get_is_exists_(obj_path, port_path) is False:
                    ma_core.CmdPortOpt._set_create_(
                        obj_path, port_path, type_name, enumerate_strings
                    )
                #
                port = ma_core.CmdPortOpt(obj_path, port_path)
                if value is not None:
                    port.set(value, enumerate_strings)
            else:
                self._connections.append(
                    (atr_path_src, ma_core.CmdPortOpt._get_atr_path_(obj_path, port_path))
                )

    def _set_obj_definition_attributes_(self, obj_path, attributes):
        for port_path, v in attributes.items():
            value = v.get('value')
            atr_path_src = v.get('connection')
            if atr_path_src is None:
                port = ma_core.CmdPortOpt(obj_path, port_path)
                if value is not None:
                    # noinspection PyBroadException
                    try:
                        port.set(value)
                    except:
                        bsc_core.ExceptionMtd.set_print()
                        utl_core.Log.set_module_error_trace(
                            'attribute-set',
                            'obj="{}", port="{}" >> value="{}"'.format(
                                obj_path, port_path, value
                            )
                        )
            else:
                self._connections.append(
                    (atr_path_src, ma_core.CmdPortOpt._get_atr_path_(obj_path, port_path))
                )

    def _set_obj_connections_create_(self):
        for atr_path_src, atr_path_tgt in self._connections:
            obj_path_src, port_path_src = bsc_core.DccAttrPathOpt(atr_path_src).to_args()
            if obj_path_src in self._name_dict:
                obj_path_src = self._name_dict[obj_path_src]
            atr_path_src = bsc_core.AtrPathMtd.get_atr_path(obj_path_src, port_path_src)
            ma_core.CmdPortOpt._set_connection_create_(atr_path_src, atr_path_tgt)

    def _set_obj_material_assign_create_(self, obj_path, material_assigns):
        obj = mya_dcc_objects.Mesh(obj_path)
        obj_opt = mya_dcc_operators.MeshLookOpt(obj)
        #
        dic = {}
        for k, v in material_assigns.items():
            if v in self._name_dict:
                v = self._name_dict[v]
            dic[k] = v
        #
        obj_opt.set_material_assigns(
            dic,
            force=self._option['material_assign_force']
        )
