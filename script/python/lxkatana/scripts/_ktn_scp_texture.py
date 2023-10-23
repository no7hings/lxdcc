# coding:utf-8
import threading

from lxbasic import bsc_core

import lxcontent.objects as ctt_objects

from lxkatana import ktn_core


class ScpTextureImportFromDatabase(object):
    """
# coding:utf-8
import lxkatana

lxkatana.set_reload()

from lxbasic import bsc_core

from lxutil import utl_core

from lxkatana import ktn_core

import lxdatabase.objects as dtb_objects

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

import lxdatabase.scripts as dtb_scripts

import lxkatana.scripts as ktn_scripts

data = {
    'specular_roughness': u'/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/tx/mossy_ground_umkkfcolw.roughness.tx',
    'normal': u'/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/tx/mossy_ground_umkkfcolw.normal.tx',
    'diffuse_color': u'/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/tx/mossy_ground_umkkfcolw.albedo.tx',
    'displacement': u'/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/tx/mossy_ground_umkkfcolw.displacement.tx',
    'metalness': '',
    'specular': '',
    'opacity': '',
    'transmission': '',
}

tab_opt = ktn_core.GuiNodeGraphTabOpt()
ktn_group = tab_opt.get_current_group()

ktn_group_opt = ktn_core.NGObjOpt(ktn_group)
resource_name = 'resource_name'
ktn_scripts.ScpTextureImportFromDatabase(
    ktn_group_opt.get_path(),
    resource_name,
    data,
).create_auto()
    """
    TEXTURE_MAPPER = {
        'albedo': 'base_color',
    }

    def __init__(self, root, resource, texture_data):
        self._root_opt = ktn_core.NGObjOpt(root)
        self._cfg = ctt_objects.Configure(
            value=bsc_core.RscConfigure.get_yaml('katana/node-graph/asset-texture-resource')
        )
        self._cfg.set(
            'option.root', self._root_opt.get_path(),
        )
        self._cfg.set(
            'option.resource', resource
        )
        self._cfg.set(
            'option.time_tag', bsc_core.TimeExtraMtd.get_time_tag_36_(multiply=100)
        )

        self._texture_data = texture_data

    @ktn_core.Modifier.undo_debug_run
    def create_auto(self):
        def post_fnc_():
            self.gui_layout_nodes()

        if self._root_opt.get_name() == 'rootNode':
            self._cfg.set_flatten()
            #
            self.create_material_group_and_material(to_view_center=True)
            self.create_node_groups()
            self.create_outer_nodes()
            self.create_inner_nodes()
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
                self.create_node_groups()
                self.create_outer_nodes(to_view_center=True)
                # self.create_node_backdrop()
                self.create_inner_nodes()
                self.create_arnold_textures()
                self.create_usd_textures()
                #
                timer = threading.Timer(.25, post_fnc_)
                timer.start()
            elif type_name == 'Group':
                self._cfg.set_flatten()
                #
                self.create_material_group_and_material(to_view_center=True)
                self.create_node_groups()
                self.create_outer_nodes()
                self.create_inner_nodes()
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
        mtl_grp_ktn_obj, is_create = ktn_core.NGObjOpt._get_node_create_args_(mtl_grp_path, mtl_grp_type_name)
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

    @classmethod
    def _set_material_collapsed_update_(cls, mtl_grp_obj_opt, mtl_name):
        attributes_ = mtl_grp_obj_opt.get_attributes()
        if 'ns_collapsedPages' in attributes_:
            v = attributes_['ns_collapsedPages']
            if v:
                if mtl_name not in v:
                    v += '{} | '.format(mtl_name)

                mtl_grp_obj_opt.set_attributes(
                    dict(ns_collapsedPages=v)
                )
            else:
                mtl_grp_obj_opt.set_attributes(
                    dict(ns_collapsedPages='{} | '.format(mtl_name))
                )
        else:
            mtl_grp_obj_opt.set_attributes(
                dict(ns_collapsedPages='{} | '.format(mtl_name))
            )

    def create_material(self):
        mtl_grp_path = self._cfg.get('node.material_group.path')
        #
        mtl_type_name = self._cfg.get('node.material.type')
        mtl_path = self._cfg.get('node.material.path')
        #
        mtl_grp_obj_opt = ktn_core.NGObjOpt(mtl_grp_path)
        mtl_grp_obj_opt.get_ktn_obj().addNetworkMaterialNode()
        mtl_ktn_objs = mtl_grp_obj_opt.get_children(include_type_names=[mtl_type_name])
        if mtl_ktn_objs:
            mtl_obj_opt = ktn_core.NGObjOpt(mtl_ktn_objs[-1])
            mtl_name = bsc_core.DccPathDagOpt(mtl_path).get_name()
            mtl_obj_opt.set_rename(mtl_name)
            self._set_material_collapsed_update_(mtl_grp_obj_opt, mtl_name)

    def create_node_backdrop(self):
        data = self._cfg.get('node.node_backdrop')
        #
        node_bdp_type_name = data.get('type')
        node_bdp_path = data.get('path')
        #
        w, h = 320, 80
        #
        node_bdp_ktn_obj, is_create = ktn_core.NGObjOpt._get_node_create_args_(node_bdp_path, node_bdp_type_name)
        if is_create is True:
            resource = self._cfg.get('option.resource')
            node_bdp_obj_opt = ktn_core.NGObjOpt(node_bdp_ktn_obj)

            sdr_path = self._cfg.get('node.arnold_surface_shader.path')
            sdr_obj_opt = ktn_core.NGObjOpt(sdr_path)
            x, y = sdr_obj_opt.get_position()
            r, g, b = bsc_core.RawTextOpt(resource).to_rgb_(maximum=1.0, s_p=25, v_p=25)
            attributes = dict(
                x=x-w,
                y=y,
                ns_sizeX=w*4,
                ns_sizeY=h*4,
                ns_colorr=r,
                ns_colorg=g,
                ns_colorb=b,
                ns_text=resource,
                ns_fontScale=2.0
            )
            node_bdp_obj_opt.set_attributes(
                attributes
            )

    def create_node_groups(self, to_view_center=False):
        ktn_obj = self.create_node_group('node_group')
        if to_view_center is True:
            obj_opt = ktn_core.NGObjOpt(ktn_obj)
            obj_opt.move_to_view_center()

    def create_node_group(self, key):
        type_name = self._cfg.get('node.{}.type'.format(key))
        path = self._cfg.get('node.{}.path'.format(key))
        ktn_obj, is_create = ktn_core.NGObjOpt._get_node_create_args_(path, type_name)
        if is_create is True:
            obj_opt = ktn_core.NGObjOpt(ktn_obj)
            obj_opt.set_color((.25, .25, .5))
            #
            obj_opt.create_input_ports_by_data(self._cfg.get('node.{}.input_ports'.format(key)) or [])
            obj_opt.create_output_ports_by_data(self._cfg.get('node.{}.output_ports'.format(key)) or [])
            #
            ktn_core.NGObjOpt._create_connections_by_data_(self._cfg.get('node.{}.connections'.format(key)) or [])
        return ktn_obj

    #
    def create_outer_nodes(self, to_view_center=False):
        for i_key in [
            'arnold_surface_shader',
        ]:
            self.create_shader(i_key, to_view_center=to_view_center)

    #
    def create_inner_nodes(self):
        for i_key in [
            'node_passthrough'
        ]:
            self.create_node_group(i_key)
        #
        for i_key in [
            'arnold_texture_basic_mode',
            #
            'arnold_texture_uv_map_proxy',
            'arnold_texture_triplanar_proxy',
            'arnold_texture_triplanar_translate',
            'arnold_texture_triplanar_rotate',
            'arnold_texture_triplanar_scale',
            #
            'usd_shader',
            'usd_uv_transform',
            'usd_uv',
        ]:
            self.create_shader(i_key)

    def create_shader(self, key, extend_kwargs=None, to_view_center=False):
        data = self._cfg.get('node.{}'.format(key))
        return self._create_shader_(data, extend_kwargs=extend_kwargs, to_view_center=to_view_center)

    @classmethod
    def _create_shader_(cls, data, extend_kwargs=None, to_view_center=False):
        type_name = data['type']
        shader_type_name = data['shader_type']
        path = data['path']
        if isinstance(extend_kwargs, dict):
            path = path.format(**extend_kwargs)
        #
        ktn_obj, is_create = ktn_core.NGObjOpt._get_shader_create_args_(path, type_name, shader_type_name)
        if is_create is True:
            obj_opt = ktn_core.NGObjOpt(ktn_obj)
            if to_view_center is True:
                obj_opt.move_to_view_center()
            #
            obj_opt.set_attributes(dict(ns_viewState=0.0))
            obj_opt.set_color(bsc_core.RawTextOpt(shader_type_name).to_rgb_(maximum=1.0, s_p=25, v_p=25))
            #
            obj_opt.set_shader_parameters_by_data(
                data.get('shader_parameters') or {},
                extend_kwargs=extend_kwargs
            )
            obj_opt.set_shader_expressions_by_data(
                data.get('shader_expressions') or {},
                extend_kwargs=extend_kwargs
            )
            obj_opt.set_shader_hints_by_data(
                data.get('shader_hints') or {},
                extend_kwargs=extend_kwargs
            )
            #
            ktn_core.NGObjOpt._create_connections_by_data_(
                data.get('connections') or [],
                extend_kwargs=extend_kwargs
            )
        return ktn_obj

    @classmethod
    def _create_node_(cls, data, extend_kwargs=None, to_view_center=False):
        type_name = data['type']
        path = data['path']
        if isinstance(extend_kwargs, dict):
            path = path.format(**extend_kwargs)
        #
        ktn_obj, is_create = ktn_core.NGObjOpt._get_node_create_args_(path, type_name)
        if is_create is True:
            obj_opt = ktn_core.NGObjOpt(ktn_obj)
            if to_view_center is True:
                obj_opt.move_to_view_center()
            #
            obj_opt.set_attributes(dict(ns_viewState=0.0))
            obj_opt.set_color(bsc_core.RawTextOpt(type_name).to_rgb_(maximum=1.0, s_p=25, v_p=25))
            #
            obj_opt.set_shader_parameters_by_data(
                data.get('shader_parameters') or {},
                extend_kwargs=extend_kwargs
            )
            obj_opt.set_shader_expressions_by_data(
                data.get('shader_expressions') or {},
                extend_kwargs=extend_kwargs
            )
            obj_opt.set_shader_hints_by_data(
                data.get('shader_hints') or {},
                extend_kwargs=extend_kwargs
            )
            #
            ktn_core.NGObjOpt._create_connections_by_data_(
                data.get('connections') or [],
                extend_kwargs=extend_kwargs
            )
        return ktn_obj

    @classmethod
    def _create_shader_node_graph_node_connections_(cls, data, extend_kwargs=None):
        ktn_core.NGObjOpt._create_connections_by_data_(
            data.get('connections') or [],
            extend_kwargs=extend_kwargs
        )

    def create_shader_node_graph(self, key, sub_key, extend_kwargs=None):
        data = self._cfg.get('{}.{}.node_graph'.format(key, sub_key)) or {}
        for k, v in data.items():
            if 'shader_type' in v:
                self._create_shader_(v, extend_kwargs)
            else:
                self._create_node_(v, extend_kwargs)

    def create_shader_node_graph_connections(self, key, sub_key, extend_kwargs=None):
        data = self._cfg.get('{}.{}.node_graph'.format(key, sub_key)) or {}
        for k, v in data.items():
            self._create_shader_node_graph_node_connections_(v, extend_kwargs)

    def create_arnold_textures(self):
        key = 'arnold_texture'
        for i_sub_key, i_texture in self._texture_data.items():
            i_c = self._cfg.get(
                '{}.{}'.format(key, i_sub_key)
            )
            if i_c:
                self.create_shader_node_graph(
                    key, i_sub_key,
                    extend_kwargs=dict(
                        texture=i_texture
                    )
                )
                ktn_core.NGObjOpt._create_connections_by_data_(
                    i_c.get('connections') or [],
                )
        # create connections after
        for i_sub_key, i_texture in self._texture_data.items():
            i_c = self._cfg.get(
                '{}.{}'.format(key, i_sub_key)
            )
            if i_c:
                self.create_shader_node_graph_connections(
                    key, i_sub_key,
                    extend_kwargs=dict(
                        texture=i_texture
                    )
                )

    def create_usd_textures(self):
        key = 'usd_texture'
        for i_sub_key, i_texture in self._texture_data.items():
            i_c = self._cfg.get(
                '{}.{}'.format(key, i_sub_key)
            )
            if i_c:
                self.create_shader_node_graph(
                    key, i_sub_key,
                    extend_kwargs=dict(
                        texture=i_texture
                    )
                )
                ktn_core.NGObjOpt._create_connections_by_data_(
                    i_c.get('connections') or [],
                )
        # create connections after
        for i_sub_key, i_texture in self._texture_data.items():
            i_c = self._cfg.get(
                '{}.{}'.format(key, i_sub_key)
            )
            if i_c:
                self.create_shader_node_graph_connections(
                    key, i_sub_key,
                    extend_kwargs=dict(
                        texture=i_texture
                    )
                )

    def gui_layout_nodes(self):
        sdr_path = self._cfg.get('node.arnold_surface_shader.path')
        ktn_core.NGObjOpt(sdr_path).gui_layout_shader_graph(
            size=(320, 80), shader_view_state=0.0
        )

# if __name__ == '__main__':
#     # coding:utf-8
#     import lxkatana
#
#     lxkatana.set_reload()
#
#     from lxkatana import ktn_core
#
#     import lxkatana.scripts as ktn_scripts
#
#     KatanaFile.Load('/data/f/katana_drop_test/test_1.katana')
#
#     ktn_scripts.ScpTextureImportFromDatabase(
#         'NetworkMaterialCreate',
#         'Concrete_Damaged',
#         {
#             'albedo': '/l/resource/library/texture/all/surface/concrete_damaged_pkngj0/v0001/texture/acescg/tx/concrete_damaged_pkngj0.albedo.tx',
#             'roughness': '/l/resource/library/texture/all/surface/concrete_damaged_pkngj0/v0001/texture/acescg/tx/concrete_damaged_pkngj0.roughness.tx',
#             'normal': '/l/resource/library/texture/all/surface/concrete_damaged_pkngj0/v0001/texture/acescg/tx/concrete_damaged_pkngj0.normal.tx',
#             'displacement': '/l/resource/library/texture/all/surface/concrete_damaged_pkngj0/v0001/texture/acescg/tx/concrete_damaged_pkngj0.displacement.tx'
#         },
#     ).create_auto()
