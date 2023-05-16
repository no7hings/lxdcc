# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds, mel

import os

import collections

import copy

import glob

from lxutil import utl_core

import lxmaya.modifiers as mya_modifiers

from lxmaya import ma_configure, ma_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_operators as mya_dcc_operators

from lxmaya_fnc import ma_fnc_configure, ma_fnc_core

from lxmaya.modifiers import _mya_mdf_utility

from lxuniverse import unr_configure

import lxutil.scripts as utl_scripts

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxutil.fnc import utl_fnc_obj_abs

import lxutil.dcc.dcc_objects as utl_dcc_objects


class FncLookAssExporter(utl_fnc_obj_abs.AbsFncOptionBase):
    PLUG_NAME = 'mtoa'
    OPTION = dict(
        file='',
        location='',
        frame=None,
        camera=None,
        #
        texture_use_environ_map=False,
    )
    def __init__(self, option=None):
        super(FncLookAssExporter, self).__init__(option)
        self._file_path = self.get('file')
        self._location = self.get('location')
        self._frame = self.get('frame')
        self._camera = self.get('camera')
        self._texture_use_environ_map = self.get('texture_use_environ_map')
        #
        self._root = bsc_core.DccPathDagMtd.get_dag_pathsep_replace(
            self._location, pathsep_tgt=ma_configure.Util.OBJ_PATHSEP
        )
        #
        self._star_frame, self._end_frame = mya_dcc_objects.Scene.get_frame_range(self._frame)
        self._camera_path = mya_dcc_objects.Scene.get_current_render_camera_path(self._camera)
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
        # noinspection PyArgumentList
        return cmds.arnoldExportAss(**kwargs)
    @_mya_mdf_utility.set_undo_mark_mdf
    def execute(self):
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
        # map texture use environ
        self._results = self._set_cmd_run_(**kwargs)
        if self._results:
            if self._texture_use_environ_map is True:
                with utl_core.LogProgressRunner.create_as_bar(maximum=len(self._results), label='texture environ-map') as l_p:
                    for i in self._results:
                        l_p.set_update()
                        #
                        fr = utl_scripts.DotAssFileReader(i)
                        fr._set_file_paths_convert_()
            #
            utl_core.Log.set_module_result_trace(
                'ass export',
                u'file="{}"'.format(self._file_path)
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
    def __init__(self, file_path, root=None, look='default', ass_file_path=None, path_lstrip=None):
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
        self._path_lstrip = path_lstrip
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
                key = mesh_dcc_path.replace(ma_configure.Util.OBJ_PATHSEP, unr_configure.Obj.PATHSEP)
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
    @_mya_mdf_utility.set_undo_mark_mdf
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
            exporter = FncLookAssExporter(
                option=dict(
                    file=self._ass_file_path,
                    location=self._root,
                    texture_use_environ_map=True,
                )
            )
            exporter.execute()
        #
        if os.path.isfile(self._ass_file_path) is True:
            self._scene = ar_commands.set_scene_load_from_dot_ass(
                file_path=self._ass_file_path,
                path_lstrip=self._path_lstrip
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
    def __init__(self, file_path, root=None, look='default', path_lstrip=None):
        self._file_path = file_path
        self._root = root
        self._look = look
        self._path_lstrip = path_lstrip
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
                look_opt = mya_dcc_operators.XgenDescriptionLookOpt(xgen_description)
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


class TextureBaker(utl_fnc_obj_abs.AbsFncOptionBase):
    OPTION = dict(
        directory='',
        location='',
        include_indices=[],
        frame=None,
        resolution=512,
        aa_samples=3
    )
    @classmethod
    def _set_cmd_run_(cls, mya_mesh_path, **kwargs):
        # folder = '',
        # shader=shader,
        # resolution=512,
        # aa_samples=3,
        # filter='gaussian',
        # filter_width=2.0,
        # all_udims=True,
        # udims=udims,
        # uv_set=uv_set,
        # normal_offset=normalOffset,
        # enable_aovs=enableAovs,
        # extend_edges=extendEdges,
        # u_start=uStart,
        # u_scale=uScale,
        # v_start=vStart,
        # v_scale=vScale,
        # sequence=useSequence,
        # frame_start=frameStart,
        # frame_end=frameEnd,
        # frame_step=frameStep,
        # frame_padding=framePadding
        #
        cmds.select(mya_mesh_path)
        cmds.arnoldRenderToTexture(
            **kwargs
        )
        cmds.select(clear=1)
    @classmethod
    def convert_arnold_visibilities_fnc(cls, mya_set):
        from lxarnold import and_configure
        #
        c = and_configure.Visibility.MAYA_VISIBILITY_DICT
        cmd_obj_opt = ma_core.CmdObjOpt(mya_set.path)
        for k, v in c.items():
            cmd_obj_opt.set_customize_attribute_create(v, False)
    @classmethod
    def convert_preview_shaders_fnc(cls, directory, mya_mesh):
        beauty_texture_exr_path_pattern = '{}/*_{}_[0-9][0-9][0-9][0-9].exr'.format(
            directory.path, mya_mesh.name
        )
        transmission_texture_exr_path_pattern = '{}/*_{}_[0-9][0-9][0-9][0-9].transmission.exr'.format(
            directory.path, mya_mesh.name
        )
        opacity_texture_exr_path_pattern = '{}/*_{}_[0-9][0-9][0-9][0-9].opacity.exr'.format(
            directory.path, mya_mesh.name
        )
        texture_exr_path_patterns = [
            ('beauty', beauty_texture_exr_path_pattern),
            ('transmission', transmission_texture_exr_path_pattern),
            ('opacity', opacity_texture_exr_path_pattern),
        ]
        dic = cls.convert_preview_textures_fnc(texture_exr_path_patterns)
        beauty_texture_jpgs = dic.get('beauty') or []
        if beauty_texture_jpgs:
            beauty_texture_jpg = beauty_texture_jpgs[0]
            cls.create_preview_shaders_fnc(
                mya_mesh, beauty_texture_jpg
            )
    @classmethod
    def convert_preview_textures_fnc(cls, patterns):
        dic = {}
        for i_key, i_pattern in patterns:
            i_texture_exr_paths = glob.glob(i_pattern) or []
            for j_texture_exr_path in i_texture_exr_paths:
                j_texture_exr = utl_dcc_objects.OsTexture(j_texture_exr_path)
                j_texture_jpg = j_texture_exr.get_as_tgt_ext('.jpg')
                #
                dic.setdefault(
                    i_key, []
                ).append(
                    j_texture_jpg
                )
                if j_texture_jpg.get_is_exists() is False:
                    j_texture_exr._set_unit_jpg_create_(
                        j_texture_exr_path
                    )
        return dic
    @classmethod
    def create_preview_shaders_fnc(cls, mya_mesh, texture_jpg):
        material_name = '{}__material'.format(mya_mesh.name)
        material = mya_dcc_objects.Material(material_name)
        if material.get_is_exists() is False:
            material.set_create(
                'shadingEngine'
            )
        #
        shader_name = '{}__shader'.format(mya_mesh.name)
        shader = mya_dcc_objects.Shader(shader_name)
        if shader.get_is_exists() is False:
            shader.set_create(
                'lambert'
            )
            material.get_port('surfaceShader').set_source(
                shader.get_port('outColor')
            )
        #
        image_name = '{}__image'.format(mya_mesh.name)
        image = mya_dcc_objects.Shader(image_name)
        if image.get_is_exists() is False:
            image.set_create('file')
            shader.get_port('color').set_source(
                image.get_port('outColor')
            )
            image.set('colorSpace', 'ACES - ACEScg')
            image.set('ignoreColorSpaceFileRules', True)
        #
        image.set('fileTextureName', texture_jpg.path)
        image.set('uvTilingMode', 3)
        #
        mya_mesh_look_opt = mya_dcc_operators.MeshLookOpt(mya_mesh)
        mya_mesh_look_opt.set_material(material.path)
        if ma_core.get_is_ui_mode() is True:
            mel.eval('generateUvTilePreview {}'.format(image.path))
    @classmethod
    def create_arnold_options_fnc(cls):
        # noinspection PyUnresolvedReferences
        import mtoa.core as core
        core.createOptions()
        #
        mya_dcc_objects.Node(
            'defaultArnoldRenderOptions'
        ).set(
            'ignoreDisplacement', True
        )
    @classmethod
    def create_arnold_lights_fnc(cls):
        light = mya_dcc_objects.Shape('light')
        if light.get_is_exists() is False:
            light = light.set_create('aiStandIn')
        #
        atr_raw = dict(dso='/l/resource/td/asset/ass/look-preview-light.ass')
        [light.get_port(k).set(v) for k, v in atr_raw.items()]
        return light.transform.path
    @classmethod
    def create_arnold_aovs_fnc(cls):
        from lxarnold import and_configure
        #
        dic = {
            'transmission': {'type': 'rgb'},
            'opacity': {'type': 'rgb'}
        }
        lis = []
        for k, v in dic.items():
            i_aov_name = 'aiAOV_{}'.format(k)
            if cmds.objExists(i_aov_name) is False:
                i_aov = cmds.createNode(
                    'aiAOV', name='aiAOV_{}'.format(k), skipSelect=True
                )
                cmds.setAttr('{}.name'.format(i_aov), k, type='string')
                cmds.setAttr('{}.type'.format(i_aov), and_configure.Aov.get_index(v['type']))
                lis.append(i_aov)

        cls.set_aovs_link_create(lis)
    @classmethod
    def set_aovs_link_create(cls, aovs):
        def set_option_link_create_fnc_(aov_):
            _maximum = 100
            _is_end = False
            _index = 0
            _output_atr_path = '{}.message'.format(aov_)
            while _is_end is False:
                _input_atr_path = 'defaultArnoldRenderOptions.aovList[{}]'.format(_index)
                if cmds.objExists(_input_atr_path) is True:
                    if cmds.connectionInfo(_input_atr_path, isExactDestination=1) is True:
                        _index += 1
                    else:
                        cmds.connectAttr(_output_atr_path, _input_atr_path)
                        _is_end = True
                        break
                #
                if _index == _maximum:
                    _is_end = True
                    break
        #
        def set_driver_create_fnc_(aov_):
            _output_atr_path = 'defaultArnoldDriver.message'
            _input_atr_path = '{}.outputs[0].driver'.format(aov_)
            if cmds.connectionInfo(_input_atr_path, isExactDestination=1) is False:
                cmds.connectAttr(_output_atr_path, _input_atr_path)
        #
        def set_filter_create_fnc_(aov_):
            _output_atr_path = 'defaultArnoldFilter.message'
            _input_atr_path = '{}.outputs[0].filter'.format(aov_)
            if cmds.connectionInfo(_input_atr_path, isExactDestination=1) is False:
                cmds.connectAttr(_output_atr_path, _input_atr_path)
        #
        if aovs:
            for i_aov in aovs:
                set_option_link_create_fnc_(i_aov)
                set_driver_create_fnc_(i_aov)
                set_filter_create_fnc_(i_aov)

    def __init__(self, option):
        super(TextureBaker, self).__init__(option)

    def set_run(self):
        directory_path = self.get('directory')
        location_path = self.option.get('location')
        include_indices = self.get('include_indices')
        directory = utl_dcc_objects.OsDirectory_(directory_path)
        directory.set_create()
        #
        mya_hide_set = mya_dcc_objects.Set('look_preview_export_hide_set')
        if mya_hide_set.get_is_exists() is False:
            mya_hide_set.set_create(
                'set'
            )
            self.convert_arnold_visibilities_fnc(mya_hide_set)
        #
        mya_hide_set.set_elements_clear()
        #
        mya_show_set = mya_dcc_objects.Set('look_preview_export_show_set')
        if mya_show_set.get_is_exists() is False:
            mya_show_set.set_create(
                'set'
            )
            self.convert_arnold_visibilities_fnc(mya_show_set)
            #
            mya_show_set.get_port('primaryVisibility').set(True)
            # debug, render a black texture when "castsShadows" is "False"
            mya_show_set.get_port('castsShadows').set(True)
        #
        mya_location_path = bsc_core.DccPathDagOpt(location_path).translate_to('|').get_value()
        #
        mya_group = mya_dcc_objects.Group(mya_location_path)
        mya_mesh_paths = mya_group.get_all_shape_paths(
            include_obj_type=['mesh']
        )
        for i_mya_mesh_path in mya_mesh_paths:
            mya_hide_set.add_element(i_mya_mesh_path)
        #
        self.create_arnold_options_fnc()
        self.create_arnold_lights_fnc()
        self.create_arnold_aovs_fnc()
        #
        if include_indices:
            mya_mesh_paths = [mya_mesh_paths[i] for i in include_indices]
        #
        utl_core.Log.set_module_result_trace(
            'texture bake',
            'objs=[{}]'.format(', '.join(['"{}"'.format(i) for i in mya_mesh_paths]))
        )
        #
        with utl_core.LogProgressRunner.create_as_bar(maximum=len(mya_mesh_paths), label='texture bake') as l_p:
            for i_mya_mesh_path in mya_mesh_paths:
                l_p.set_update()
                #
                mya_hide_set.set_element_remove(i_mya_mesh_path)
                mya_show_set.add_element(i_mya_mesh_path)
                #
                self._set_cmd_run_(
                    i_mya_mesh_path,
                    folder=directory.path,
                    resolution=self.option.get('resolution'),
                    aa_samples=self.option.get('aa_samples'),
                    filter='gaussian',
                    filter_width=2.0,
                    #
                    all_udims=True,
                    extend_edges=True,
                    enable_aovs=True
                )
                #
                mya_hide_set.add_element(i_mya_mesh_path)
                mya_show_set.set_element_remove(i_mya_mesh_path)
                #
                i_mya_mesh = mya_dcc_objects.Mesh(i_mya_mesh_path)
                #
                # self.convert_preview_shaders_fnc(directory, i_mya_mesh)
        #
        # file_path = mya_dcc_objects.Scene.get_current_file_path()
        # import os
        # base, ext = os.path.splitext(file_path)
        # mya_dcc_objects.Scene.set_file_save_to(
        #     '{}.bck.ma'.format(base)
        # )

    def set_convert_run(self):
        directory_path = self.get('directory')
        location_path = self.option.get('location')
        directory = utl_dcc_objects.OsDirectory_(directory_path)

        mya_group = mya_dcc_objects.Group(
            bsc_core.DccPathDagOpt(location_path).translate_to('|').get_value()
        )
        mya_mesh_paths = mya_group.get_all_shape_paths(
            include_obj_type=['mesh']
        )
        with utl_core.LogProgressRunner.create_as_bar(maximum=len(mya_mesh_paths), label='texture bake') as l_p:
            for i_mya_mesh_path in mya_mesh_paths:
                l_p.set_update()
                #
                i_mya_mesh = mya_dcc_objects.Mesh(i_mya_mesh_path)
                #
                self.convert_preview_shaders_fnc(directory, i_mya_mesh)


class FncLookYamlExporter(utl_fnc_obj_abs.AbsFncOptionBase):
    OPTION = dict(
        file='',
        root='',
        locations=[],
        pathsep='|',
        #
        ignore_default_properties=False,
    )
    EXCLUDE_TYPE_NAMES = [
        'transform', 'mesh',
        'shadingEngine',
        'groupId',
        'displayLayerManager', 'displayLayer',
        'xgmSplineGuide', 'xgmSplineGuide', 'xgmGuideData', 'xgmMakeGuide', 'xgmSubdPatch',
        #
        'colorManagementGlobals'
    ]
    def __init__(self, option=None):
        super(FncLookYamlExporter, self).__init__(option)

    def update_node_fnc(self, scheme, obj_path):
        key = '{}.{}'.format(scheme, obj_path)
        if self._raw.get(key) is None:
            self._raw.set(
                '{}.{}.properties.type'.format(scheme, obj_path),
                'maya/{}'.format(ma_core.CmdObjOpt(obj_path).get_type_name())
            )
            return True
        return False

    def update_node_properties_fnc(self, scheme, obj_path, definition=False, customize=False, definition_includes=None, customize_includes=None):
        if definition is True:
            self._raw.set(
                '{}.{}.properties.definition-attributes'.format(scheme, obj_path),
                self.get_node_definition_properties_fnc(obj_path, definition_includes)
            )
        else:
            self._raw.set(
                '{}.{}.properties.definition-attributes'.format(scheme, obj_path),
                collections.OrderedDict()
            )
        if customize is True:
            self._raw.set(
                '{}.{}.properties.customize-attributes'.format(scheme, obj_path),
                self.get_node_customize_properties_fnc(obj_path, customize_includes)
            )
        else:
            self._raw.set(
                '{}.{}.properties.customize-attributes'.format(scheme, obj_path),
                collections.OrderedDict()
            )

    def update_geometry_material_assign_fnc(self, scheme, obj_path, material_assigns):
        self._raw.set(
            '{}.{}.properties.material-assigns'.format(scheme, obj_path),
            material_assigns
        )
    @classmethod
    def get_node_definition_properties_fnc(cls, obj_path, includes=None):
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
    @classmethod
    def get_node_customize_properties_fnc(cls, obj_path, includes=None):
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

    def update_by_location_fnc(self, location, pathsep):
        location_cur = bsc_core.DccPathDagOpt(location).translate_to(pathsep).get_value()
        group = mya_dcc_objects.Group(location_cur)
        nodes = group.get_descendants()
        if nodes:
            with utl_core.GuiProgressesRunner.create(
                maximum=len(nodes), label='export look yaml at "{}"'.format(location)
            ) as g_p:
                for i_node in nodes:
                    g_p.set_update()
                    if i_node.type == 'mesh':
                        i_mesh = mya_dcc_objects.Mesh(i_node.path)
                        i_mesh_opt = mya_dcc_operators.MeshLookOpt(i_mesh)
                        #
                        self.update_node_fnc('geometry', i_node.path)
                        self.update_node_properties_fnc('geometry', i_node.path, customize=True)
                        self.update_geometry_material_assign_fnc(
                            'geometry', i_node.path, i_mesh_opt.get_material_assigns()
                        )
                        #
                        i_materials = i_mesh_opt.get_materials()
                        for j_material in i_materials:
                            j_material = mya_dcc_objects.Node(j_material.path)
                            if self.update_node_fnc('material', j_material.path) is True:
                                self.update_node_properties_fnc(
                                    'material', j_material.path,
                                    definition=True,
                                    definition_includes=['surfaceShader', 'displacementShader', 'volumeShader']
                                )
                                #
                                source_objs = j_material.get_all_source_objs()
                                for i_source_node in source_objs:
                                    i_source_node_obj_type_name = i_source_node.type_name
                                    if i_source_node_obj_type_name not in self.EXCLUDE_TYPE_NAMES:
                                        if self.update_node_fnc('node-graph', i_source_node.path) is True:
                                            self.update_node_properties_fnc(
                                                'node-graph', i_source_node.path,
                                                definition=True
                                            )
                    elif i_node.type == 'transform':
                        self.update_node_fnc('transform', i_node.path)
                        self.update_node_properties_fnc(
                            'transform', i_node.path,
                            definition=True, customize=True, definition_includes=['visibility']
                        )
                        source_objs = i_node.get_all_source_objs()
                        for i_source_node in source_objs:
                            i_source_node_obj_type_name = i_source_node.type_name
                            if i_source_node_obj_type_name not in self.EXCLUDE_TYPE_NAMES:
                                if self.update_node_fnc('node-graph', i_source_node.path) is True:
                                    self.update_node_properties_fnc(
                                        'node-graph', i_source_node.path,
                                        definition=True
                                    )

    def execute(self):
        file_path = self.get('file')

        self._raw = bsc_objects.Content(
            value=collections.OrderedDict()
        )

        root = self.get('root')

        locations = self.get('locations')
        if locations:
            pathsep = self.get('pathsep')
            with utl_core.GuiProgressesRunner.create(
                maximum=len(locations), label='export look yaml'
            ) as g_p:
                for i_location in locations:
                    g_p.set_update()
                    self.update_by_location_fnc(i_location, pathsep)

        bsc_core.StgFileOpt(file_path).set_write(
            self._raw.get_value()
        )
