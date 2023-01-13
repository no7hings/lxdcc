# coding:utf-8
import threading

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxkatana import ktn_configure, ktn_core

import lxkatana.modifiers as ktn_modifiers


class ScpTextureImportFromDatabase(object):
    TEXTURE_MAPPER = {
        'albedo': 'base_color',
    }

    def __init__(self, root, resource, texture_data):
        self._root_opt = ktn_core.NGObjOpt(root)
        self._cfg = bsc_objects.Configure(
            value=ktn_configure.DataFile.TEXTURE_RESOURCE_SHADER_GROUP_CONFIGURE
        )
        self._cfg.set(
            'option.root', self._root_opt.get_path(),
        )
        self._cfg.set(
            'option.resource', resource
        )
        self._cfg.set(
            'option.time_tag', bsc_core.SystemMtd.get_time_tag_36(multiply=10)
        )

        self._texture_data = texture_data
    @ktn_modifiers.set_undo_mark_mdf
    def create_auto(self):
        def post_fnc_():
            self.layout_shader_group()

        if self._root_opt.get_name() == 'rootNode':
            self._cfg.set_flatten()
            self.create_material_group_and_material(to_view_center=True)
            self.create_shader_group()
            #
            self.create_shaders()
            self.create_arnold_textures()
            self.create_usd_textures()
            #
            timer = threading.Timer(.25, post_fnc_)
            timer.start()
        else:
            type_name = self._root_opt.get_type_name()
            if type_name == 'NetworkMaterialCreate':
                self._cfg.set(
                    'node.material_group.path', self._root_opt.get_path()
                )
                self._cfg.set_flatten()
                #
                self.create_material()
                self.create_shader_group(to_view_center=True)
                #
                self.create_shaders()
                self.create_arnold_textures()
                self.create_usd_textures()
                #
                timer = threading.Timer(.25, post_fnc_)
                timer.start()
            elif type_name == 'Group':
                self._cfg.set_flatten()
                self.create_material_group_and_material(to_view_center=True)
                self.create_shader_group()
                #
                self.create_shaders()
                self.create_arnold_textures()
                self.create_usd_textures()
                #
                timer = threading.Timer(.25, post_fnc_)
                timer.start()

    def create_material_group_and_material(self, to_view_center=False):
        mtl_grp_type_name = self._cfg.get('node.material_group.type')
        mtl_grp_path = self._cfg.get('node.material_group.path')
        mtl_type_name = self._cfg.get('node.material.type')
        mtl_path = self._cfg.get('node.material.path')
        mtl_grp_ktn_obj, is_create = ktn_core.NGObjOpt._get_create_args_(mtl_grp_path, mtl_grp_type_name)
        if is_create is True:
            mtl_grp_obj_opt = ktn_core.NGObjOpt(mtl_grp_ktn_obj)
            mtl_grp_obj_opt.set_color((.25, .25, .75))
            if to_view_center is True:
                mtl_grp_obj_opt.move_to_view_center()
            #
            mtl_ktn_objs = mtl_grp_obj_opt.get_children(include_type_names=[mtl_type_name])
            if mtl_ktn_objs:
                mtl_obj_opt = ktn_core.NGObjOpt(mtl_ktn_objs[-1])
                mtl_obj_opt.set_rename(bsc_core.DccPathDagOpt(mtl_path).get_name())
        else:
            mtl_grp_obj_opt = ktn_core.NGObjOpt(mtl_grp_ktn_obj)
            mtl_grp_ktn_obj.addNetworkMaterialNode()
            mtl_ktn_objs = mtl_grp_obj_opt.get_children(include_type_names=[mtl_type_name])
            if mtl_ktn_objs:
                mtl_obj_opt = ktn_core.NGObjOpt(mtl_ktn_objs[-1])
                mtl_obj_opt.set_rename(bsc_core.DccPathDagOpt(mtl_path).get_name())

    def create_material(self):
        mtl_grp_path = self._cfg.get('node.material_group.path')
        mtl_type_name = self._cfg.get('node.material.type')
        mtl_path = self._cfg.get('node.material.path')
        #
        mtl_grp_obj_opt = ktn_core.NGObjOpt(mtl_grp_path)
        mtl_grp_obj_opt.get_ktn_obj().addNetworkMaterialNode()
        mtl_ktn_objs = mtl_grp_obj_opt.get_children(include_type_names=[mtl_type_name])
        if mtl_ktn_objs:
            mtl_obj_opt = ktn_core.NGObjOpt(mtl_ktn_objs[-1])
            mtl_obj_opt.set_rename(bsc_core.DccPathDagOpt(mtl_path).get_name())

    def create_shader_group(self, to_view_center=False):
        sdr_grp_type_name = self._cfg.get('node.shader_group.type')
        sdr_grp_path = self._cfg.get('node.shader_group.path')
        sdr_grp_ktn_obj, is_create = ktn_core.NGObjOpt._get_create_args_(sdr_grp_path, sdr_grp_type_name)
        if is_create is True:
            sdr_grp_obj_opt = ktn_core.NGObjOpt(sdr_grp_ktn_obj)
            sdr_grp_obj_opt.set_color((.25, .25, .5))
            if to_view_center is True:
                sdr_grp_obj_opt.move_to_view_center()
            #
            sdr_grp_obj_opt.create_input_ports_by_data(self._cfg.get('node.shader_group.input_ports') or [])
            sdr_grp_obj_opt.create_output_ports_by_data(self._cfg.get('node.shader_group.output_ports') or [])
            #
            ktn_core.NGObjOpt._create_connections_by_data_(self._cfg.get('node.shader_group.connections') or [])

    def create_shaders(self):
        for i_key in [
            'arnold_surface_shader',
            'arnold_displacement_shader',
            #
            'arnold_normal_map',
            #
            'usd_shader',
        ]:
            self.create_shader_node(i_key)

    def create_shader_node(self, key, extend_kwargs=None):
        type_name = self._cfg.get('node.{}.type'.format(key))
        shader_type_name = self._cfg.get('node.{}.shader_type'.format(key))
        path = self._cfg.get('node.{}.path'.format(key))
        if isinstance(extend_kwargs, dict):
            path = path.format(**extend_kwargs)
        #
        ktn_obj, is_create = ktn_core.NGObjOpt._get_shader_create_args_(path, type_name, shader_type_name)
        if is_create is True:
            obj_opt = ktn_core.NGObjOpt(ktn_obj)
            obj_opt.set_shader_parameters_by_data(
                self._cfg.get('node.{}.shader_parameters'.format(key)) or {},
                extend_kwargs=extend_kwargs
            )
            #
            ktn_core.NGObjOpt._create_connections_by_data_(
                self._cfg.get('node.{}.connections'.format(key)) or [],
                extend_kwargs=extend_kwargs
            )
            ktn_core.NGObjOpt._create_send_connections_by_data_(
                self._cfg.get('node.{}.send_connections'.format(key)) or [],
                extend_kwargs=extend_kwargs
            )
            ktn_core.NGObjOpt._create_return_connections_by_data_(
                self._cfg.get('node.{}.return_connections'.format(key)) or [],
                extend_kwargs=extend_kwargs
            )

        return ktn_obj

    def create_arnold_textures(self):
        key = 'arnold_texture'
        for i_key, i_texture in self._texture_data.items():
            i_kwargs = self._cfg.get(
                'arnold_texture_option.{}'.format(i_key)
            )
            if i_kwargs:
                i_tag = i_kwargs['tag']
                i_ktn_obj = self.create_shader_node(
                    key,
                    extend_kwargs=dict(
                        tag=i_tag,
                        texture=i_texture
                    )
                )
                i_obj_opt = ktn_core.NGObjOpt(i_ktn_obj)
                extend_kwargs = dict(
                    node=i_obj_opt.get_path()
                )
                i_obj_opt._create_connections_by_data_(
                    i_kwargs.get('connections') or [],
                    extend_kwargs=extend_kwargs
                )
                i_obj_opt._create_send_connections_by_data_(
                    i_kwargs.get('send_connections') or [],
                    extend_kwargs=extend_kwargs
                )

    def create_usd_textures(self):
        key = 'usd_texture'
        for i_key, i_texture in self._texture_data.items():
            i_kwargs = self._cfg.get(
                'usd_texture_option.{}'.format(i_key)
            )
            if i_kwargs:
                i_tag = i_kwargs['tag']
                i_ktn_obj = self.create_shader_node(
                    key,
                    extend_kwargs=dict(
                        tag=i_tag,
                        texture=i_texture
                    )
                )
                i_obj_opt = ktn_core.NGObjOpt(i_ktn_obj)
                extend_kwargs = dict(
                    node=i_obj_opt.get_path()
                )
                i_obj_opt._create_connections_by_data_(
                    i_kwargs.get('connections') or [],
                    extend_kwargs=extend_kwargs
                )
                i_obj_opt._create_send_connections_by_data_(
                    i_kwargs.get('send_connections') or [],
                    extend_kwargs=extend_kwargs
                )

    def layout_shader_group(self):
        sdr_grp_path = self._cfg.get('node.shader_group.path')
        ktn_core.NGObjOpt(sdr_grp_path).set_gui_layout(
            size=(320, 240), collapsed=True
        )

