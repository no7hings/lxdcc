# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

import os

import collections

import copy

from lxutil import utl_core

import lxmaya.modifiers as mya_modifiers

from lxmaya import ma_configure, ma_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_operators as mya_dcc_operators

from lxmaya_fnc import ma_fnc_configure, ma_fnc_core

from lxmaya.modifiers import _ma_mdf_utility

from lxobj import obj_configure, obj_core

import lxutil.scripts as utl_scripts

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects


class LookAssExporter(object):
    PLUG_NAME = 'mtoa'
    def __init__(self, file_path, root=None, frame=None, camera=None):
        self._file_path = file_path
        #
        self._root = obj_core.DccPathDagMtd.get_dag_pathsep_replace(
            root, pathsep_tgt=ma_configure.Util.OBJ_PATHSEP
        )
        #
        self._star_frame, self._end_frame = mya_dcc_objects.Scene.get_frame_range(frame)
        self._camera_path = mya_dcc_objects.Scene.get_current_render_camera_path(camera)
        #
        self._results = []
    @classmethod
    def _set_cmd_run_(cls, **kwargs):
        """
        There's no documentation for the command. Another customer put together this:

        -b, -batch
        Looks like this flag is never used. I could be wrong.

        -s -selected
        This flag will export selection, or a list of object at the end of the argument
        E.g. arnoldExportAss -s -sf 10 -ef 14 pCube3 pCube1

        -f, -filename
        filename to export to. this argument can take tokens.
        eg. arnoldExportAss -sf 10 -ef 12 -f "/tmp/<Scene>/<RenderLayer>"

        -cam, -camera
        This will force the provided camera to be exported and set as renderCamera and ignore the one set in renderGlobals
        E.g. arnoldExportAss -cam topShape

        -sf, -startFrame
        self explanatory

        -ef, -endFrame
        self explanatory

        -o -options
        Not implemented, but i guess the idea is to be able to export a aiOptions node as the default options.
        E.g. createNode -n myCustomOptions aiOptions; arnoldExportAss -o myCustomOptions

        -c, --compressed
        Export a gzipped ass archive. .ass.gz

        -bb -boundingBox
        Export an asstoc file along with the ass file to use as a fast lookup of the ass scenes bounding box.
        Used to know the bounds of a deferred loaded procedural, and to show the bounding box of a standin in the maya viewport without the need to open the ass file.

        -a -asciiAss
        Force everything in the ass to bee ascii text, otherwise some parts will be binary encoded.

        -m -mask
        This is a mask of what objects to be exported.
        These are the node types you can filter on.
        """
        cmds.loadPlugin(cls.PLUG_NAME, quiet=1)
        return cmds.arnoldExportAss(**kwargs)
    @_ma_mdf_utility.set_undo_mark_mdf
    def set_run(self):
        # noinspection PyUnresolvedReferences
        import arnold as ai
        #
        mask = ai.AI_NODE_SHADER + ai.AI_NODE_SHAPE
        #
        kwargs = dict(
            filename=self._file_path,
            camera=self._camera_path,
            mask=mask,
            fullPath=1,
            boundingBox=1,
        )
        _selected_paths = []
        if self._root is not None:
            _selected_paths = cmds.ls(selection=1, long=1) or []
            cmds.select(self._root)
            kwargs['selected'] = 1
        #
        if self._star_frame != self._end_frame:
            kwargs['startFrame'] = self._star_frame
            kwargs['endFrame'] = self._end_frame
        #
        self._results = self._set_cmd_run_(**kwargs)
        if self._results:
            for i in self._results:
                fr = utl_scripts.DotAssFileReader(i)
                fr._set_file_paths_convert_()
                utl_core.Log.set_module_result_trace(
                    'maya-look-ass-exporter',
                    u'file="{}"'.format(i)
                )
        #
        if 'selected' in kwargs:
            if _selected_paths:
                cmds.select(_selected_paths)
            else:
                cmds.select(clear=1)
        return self._results

    def get_outputs(self):
        return self._results


class LookMtlxExporter(object):
    def __init__(self, file_path, root=None, look='default', ass_file_path=None, root_lstrip=None):
        self._file_path = file_path
        self._root = root
        self._look = look
        #
        if ass_file_path is not None:
            self._ass_file_path = ass_file_path
            self._use_exists_ass = True
        else:
            base, ext = os.path.splitext(file_path)
            self._ass_file_path = '{}.ass'.format(base)
            self._use_exists_ass = False
        #
        self._path_lstrip = root_lstrip
        #
        self._mesh_subdivision_dict = {}
        #
        self._results = []

    def _get_meshes_subdivision_(self):
        group_dcc_obj = mya_dcc_objects.Group(self._root)
        objs = group_dcc_obj.get_descendants()
        for obj in objs:
            if obj.type == ma_configure.Util.MESH_TYPE:
                mesh_dcc_path = obj.path
                mesh_dcc_obj = mya_dcc_objects.Mesh(mesh_dcc_path)
                key = mesh_dcc_path.replace(ma_configure.Util.OBJ_PATHSEP, obj_configure.Obj.PATHSEP)
                value = mesh_dcc_obj.get_display_smooth_iterations()
                if value > 0:
                    self._mesh_subdivision_dict[key] = value

    def _set_meshes_subdivision_(self):
        for k, v in self._mesh_subdivision_dict.items():
            mesh_obj = self._universe.get_obj(k)
            mesh_obj.get_input_port('subdiv_type').set('catclark')
            mesh_obj.get_input_port('subdiv_iterations').set(v)
    @classmethod
    def _set_cache_restore_(cls):
        from LxMtx import mtxObjects
        #
        from lxar2mtx import ar_mtx_obectjs, ar2mtx_objects
        # restore materialx
        mtxObjects.GRH_OBJ_QUEUE.restore()
        # restore arnold materialx
        ar_mtx_obectjs.GRH_OBJ_QUEUE.restore()
        # restore arnold to materialx
        ar2mtx_objects.GRH_TRS_OBJ_QUEUE.restore()
    @_ma_mdf_utility.set_undo_mark_mdf
    def set_run(self):
        from lxarnold import and_configure
        #
        from lxar2mtx import ar2mtx_objects
        #
        import lxarnold.commands as ar_commands
        #
        self._set_cache_restore_()
        #
        self._get_meshes_subdivision_()
        #
        if self._use_exists_ass is False:
            exporter = LookAssExporter(
                file_path=self._ass_file_path,
                root=self._root,
            )
            exporter.set_run()
        #
        if os.path.isfile(self._ass_file_path) is True:
            self._scene = ar_commands.set_scene_load_from_dot_ass(
                file_path=self._ass_file_path,
                root_lstrip=self._path_lstrip
            )
            self._universe = self._scene.universe
            #
            self._set_meshes_subdivision_()
            # mesh
            mesh_type = self._universe.get_obj_type(
                and_configure.ObjType.LYNXI_MESH
            )
            meshes = mesh_type.get_objs() if mesh_type is not None else []
            # curve
            curve_type = self._universe.get_obj_type(
                and_configure.ObjType.LYNXI_CURVE
            )
            curves = curve_type.get_objs() if curve_type is not None else []
            # xgen
            xgen_type = self._universe.get_obj_type(
                and_configure.ObjType.LYNXI_XGEN_DESCRIPTION
            )
            xgens = xgen_type.get_objs() if xgen_type is not None else []
            #
            geometries = meshes + curves + xgens
            if geometries:
                mtx_file = ar2mtx_objects.File(self._file_path)
                #
                l_ = mtx_file.addLook(self._look)
                for geometry in geometries:
                    l_.addSrcGeometry(geometry.path)
                #
                mtx_file.save()
                self._results.append(self._file_path)
            else:
                utl_core.Log.set_warning_trace(
                    'non-geometry(s) to exporter'
                )
        #
        if self._results:
            for i in self._results:
                utl_core.Log.set_module_result_trace(
                    'look-mtlx-exporter',
                    u'file="{}"'.format(i)
                )

    def get_outputs(self):
        return self._results


class LookAssignExporter(object):
    GEOMETRY_TYPES = [
        ma_configure.Util.MESH_TYPE
    ]
    HAIR_TYPES = [
        ma_configure.Util.XGEN_DESCRIPTION
    ]
    PATH_KEY = 'path'
    NAME_KEY = 'name'
    POINTS_KEY = 'points'
    FACE_VERTICES_KEY = 'face_vertices'
    #
    SEARCH_ORDER = [
        POINTS_KEY,
        FACE_VERTICES_KEY
    ]
    def __init__(self, file_path, root=None, look='default', root_lstrip=None):
        self._file_path = file_path
        self._root = root
        self._look = look
        self._path_lstrip = root_lstrip
        #
        self._look_content = ma_fnc_core.LookContent(collections.OrderedDict())
        #
        self._results = []

    def set_run(self):
        group = mya_dcc_objects.Group(self._root)
        #
        var = 'geometry'
        geometry_paths = group.get_all_shape_paths(include_obj_type=ma_fnc_configure.Look.GEOMETRY_TYPES)
        for seq, geometry_path in enumerate(geometry_paths):
            obj_type = mya_dcc_objects.Node(geometry_path).type
            if obj_type == ma_configure.Util.MESH_TYPE:
                mesh_obj = mya_dcc_objects.Mesh(geometry_path)
                mesh_obj_opt = mya_dcc_operators.MeshOpt(mesh_obj)
                # key
                name = mesh_obj_opt.get_name()
                points_uuid = mesh_obj_opt.get_points_as_uuid(ordered=True)
                face_vertices_uuid = mesh_obj_opt.get_face_vertices_as_uuid()
                #
                self._look_content.set_name_key(self._look, var, seq, name)
                self._look_content.set_points_uuid_key(self._look, var, seq, points_uuid)
                self._look_content.set_face_vertices_uuid_key(self._look, var, seq, face_vertices_uuid)
                # value

                look_opt = mya_dcc_operators.MeshLookOpt(mesh_obj)
                path = mesh_obj_opt.get_path(lstrip=self._path_lstrip)
                self._look_content.set_type_value(self._look, var, seq, obj_type)
                self._look_content.set_path_value(self._look, var, seq, path)
                material_assigns = look_opt.get_material_assigns()
                properties = look_opt.get_properties()
                visibilities = look_opt.get_visibilities()
                self._look_content.set_material_assigns_value(self._look, var, seq, material_assigns)
                self._look_content.set_properties_value(self._look, var, seq, properties)
                self._look_content.set_visibilities_value(self._look, var, seq, visibilities)
        var = 'hair'
        hair_paths = group.get_all_shape_paths(include_obj_type=ma_fnc_configure.Look.HAIR_TYPES)
        for seq, hair_path in enumerate(hair_paths):
            obj_type = mya_dcc_objects.Node(hair_path).type
            if obj_type == ma_configure.Util.XGEN_DESCRIPTION:
                xgen_description = mya_dcc_objects.XgenDescription(hair_path)
                xgen_description_opt = mya_dcc_operators.XgenDescriptionOpt(xgen_description)
                look_opt = mya_dcc_operators.XgenDescriptionLookMtd(xgen_description)
                path = xgen_description_opt.get_path(lstrip=self._path_lstrip)
                name = xgen_description_opt.get_name()
                material_assigns = look_opt.get_material_assigns()
                properties = look_opt.get_properties()
                visibilities = look_opt.get_visibilities()
                # key
                self._look_content.set_name_key(self._look, var, seq, name)
                # value
                self._look_content.set_type_value(self._look, var, seq, obj_type)
                self._look_content.set_path_value(self._look, var, seq, path)
                self._look_content.set_material_assigns_value(self._look, var, seq, material_assigns)
                self._look_content.set_properties_value(self._look, var, seq, properties)
                self._look_content.set_visibilities_value(self._look, var, seq, visibilities)

        #
        raw = self._look_content.get_raw()
        if raw:
            utl_core.File.set_write(self._file_path, raw)
            self._results = [self._file_path]
        #
        if self._results:
            for i in self._results:
                utl_core.Log.set_module_result_trace(
                    'look-assign-exporter',
                    u'file="{}"'.format(i)
                )

    def get_outputs(self):
        return self._results


class LookYamlExporter(object):
    OPTION = dict(
        file='',
        root=''
    )
    def __init__(self, option):
        self._option = copy.copy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                self._option[k] = v
        #
        self._raw = bsc_objects.Content(
            value=collections.OrderedDict()
        )
    @mya_modifiers.set_undo_mark_mdf
    def set_run(self):
        file_path = self._option['file']
        dcc_root = self._option['root']
        dcc_root_dag_path = bsc_core.DccPathDagOpt(dcc_root)
        mya_root_dag_path = dcc_root_dag_path.set_translate_to(
            pathsep='|'
        )
        mya_root = mya_dcc_objects.Group(mya_root_dag_path.value)
        self._set_obj_create_('root', mya_root.path)
        self._set_obj_attributes_create_(
            'root', mya_root.path,
            customize=True, customize_includes=['pg_lookpass']
        )
        mya_objs = mya_root.get_descendants()
        cmds.ls()
        if mya_objs:
            gp = utl_core.GuiProgressesRunner(maximum=len(mya_objs))
            for i_mya_obj in mya_objs:
                gp.set_update()
                if i_mya_obj.type == 'mesh':
                    i_mesh = mya_dcc_objects.Mesh(i_mya_obj.path)
                    i_mesh_opt = mya_dcc_operators.MeshLookOpt(i_mesh)
                    #
                    self._set_obj_create_('geometry', i_mya_obj.path)
                    self._set_obj_attributes_create_('geometry', i_mya_obj.path)
                    self._set_geometry_attributes_create_(
                        'geometry', i_mya_obj.path, i_mesh_opt.get_material_assigns()
                    )
                    materials = i_mesh_opt.get_materials()
                    for i_material in materials:
                        i_material = mya_dcc_objects.Node(i_material.path)
                        if self._set_obj_create_('material', i_material.path) is True:
                            self._set_obj_attributes_create_(
                                'material', i_material.path,
                                definition=True, definition_includes=['surfaceShader', 'displacementShader', 'volumeShader']
                            )
                            #
                            source_objs = i_material.get_all_source_objs()
                            for i_source_node in source_objs:
                                i_source_node_obj_type_name = i_source_node.type_name
                                if i_source_node_obj_type_name not in ['transform', 'mesh', 'shadingEngine', 'groupId', 'displayLayer']:
                                    if self._set_obj_create_('node-graph', i_source_node.path) is True:
                                        self._set_obj_attributes_create_(
                                            'node-graph', i_source_node.path,
                                            definition=True
                                        )
                elif i_mya_obj.type == 'transform':
                    self._set_obj_create_('transform', i_mya_obj.path)
                    self._set_obj_attributes_create_(
                        'transform', i_mya_obj.path,
                        definition=True, definition_includes=['visibility']
                    )
                    source_objs = i_mya_obj.get_all_source_objs()
                    for i_source_node in source_objs:
                        i_source_node_obj_type_name = i_source_node.type_name
                        if i_source_node_obj_type_name not in ['transform', 'mesh', 'shadingEngine', 'groupId']:
                            if self._set_obj_create_('node-graph', i_source_node.path) is True:
                                self._set_obj_attributes_create_(
                                    'node-graph', i_source_node.path,
                                    definition=True
                                )
            gp.set_stop()
        #
        # self._raw.set_print_as_yaml_style()
        self._raw.set_save_to(
            file_path
        )

    def _set_obj_create_(self, scheme, obj_path):
        key = '{}.{}'.format(scheme, obj_path)
        if self._raw.get(key) is None:
            self._raw.set(
                '{}.{}.properties.type'.format(scheme, obj_path),
                'maya/{}'.format(ma_core.CmdObjOpt(obj_path).get_type_name())
            )
            return True
        return False

    def _set_obj_attributes_create_(self, scheme, obj_path, definition=False, customize=False, definition_includes=None, customize_includes=None):
        if definition is True:
            self._raw.set(
                '{}.{}.properties.definition-attributes'.format(scheme, obj_path),
                self._get_obj_definition_attributes_(obj_path, definition_includes)
            )
        else:
            self._raw.set(
                '{}.{}.properties.definition-attributes'.format(scheme, obj_path),
                collections.OrderedDict()
            )
        if customize is True:
            self._raw.set(
                '{}.{}.properties.customize-attributes'.format(scheme, obj_path),
                self._get_obj_customize_attributes_(obj_path, customize_includes)
            )
        else:
            self._raw.set(
                '{}.{}.properties.customize-attributes'.format(scheme, obj_path),
                collections.OrderedDict()
            )

    def _set_geometry_attributes_create_(self, scheme, obj_path, material_assigns):
        self._raw.set(
            '{}.{}.properties.material-assigns'.format(scheme, obj_path),
            material_assigns
        )

    def _get_obj_definition_attributes_(self, obj_path, includes=None):
        dic = collections.OrderedDict()
        ports = ma_core.CmdObjOpt(obj_path).get_ports(includes)
        for i_port in ports:
            i_port_raw = collections.OrderedDict()
            i_port_raw['type'] = 'maya/{}'.format(i_port.get_type_name())
            if i_port.get_has_source_(exact=True):
                i_port_raw['connection'] = i_port.get_source()
                dic[i_port.get_port_path()] = i_port_raw
            else:
                if i_port.get_is_changed() is True:
                    i_port_raw['value'] = i_port.get()
                    dic[i_port.get_port_path()] = i_port_raw
        return dic

    def _get_obj_customize_attributes_(self, obj_path, includes=None):
        dic = collections.OrderedDict()
        ports = ma_core.CmdObjOpt(obj_path).get_customize_ports(includes)
        for i_port in ports:
            i_port_raw = collections.OrderedDict()
            i_port_raw['type'] = 'maya/{}'.format(i_port.get_type_name())
            if i_port.get_has_source_(exact=True):
                i_port_raw['connection'] = i_port.get_source()
            #
            if i_port.get_is_enumerate():
                i_port_raw['enumerate-strings'] = i_port.get_enumerate_strings()
            #
            i_port_raw['value'] = i_port.get()
            dic[i_port.get_port_path()] = i_port_raw
        return dic
