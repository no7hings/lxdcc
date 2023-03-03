# coding:utf-8
from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxkatana import ktn_core


class ScpMacro(object):
    def __init__(self, file_path):
        self._file_path = file_path
        self._cfg = bsc_objects.Configure(value=self._file_path)
        type_name = self._cfg.get('option.type')
        r, g, b = bsc_core.RawTextOpt(type_name).to_rgb_(maximum=1.0, s_p=25, v_p=25)
        self._cfg.set(
            'option.color.r', r
        )
        self._cfg.set(
            'option.color.g', g
        )
        self._cfg.set(
            'option.color.b', b
        )
        self._cfg.set_flatten()
    #
    @ktn_core.Modifier.undo_debug_run
    def build(self):
        self.build_main()
        self.build_nodes()
        self.gui_layout()

    def build_main(self):
        data = self._cfg.get_content('main')
        ktn_obj, is_create = self._build_node_(data)
        self._ktn_obj_opt = ktn_core.NGObjOpt(ktn_obj)
        if is_create is False:
            self._ktn_obj_opt.clear_ports(
                data.get('clear_start')
            )
            #
            self._ktn_obj_opt.create_ports_by_data(
                data.get('ports') or {}
            )
        #
        if data.get('type') in ['Group']:
            self._ktn_obj_opt.clear_children()

    def build_nodes(self):
        if self._cfg.get_key_is_exists('node') is False:
            return
        node_graph_content = self._cfg.get_content('node')
        for i_key in node_graph_content.get_top_keys():
            i_data = node_graph_content.get_content(i_key)
            self._build_node_(i_data)
    @classmethod
    def _build_node_(cls, data, extend_kwargs=None):
        type_name = data['type']
        path = data['path']
        ktn_obj, is_create = ktn_core.NGObjOpt._get_create_args_(path, type_name)
        if is_create is True:
            obj_opt = ktn_core.NGObjOpt(ktn_obj)
            #
            obj_opt.set_color(bsc_core.RawTextOpt(type_name).to_rgb_(maximum=1.0, s_p=25, v_p=25))
            #
            obj_opt.set_attributes(
                data.get('attributes') or {}
            )
            #
            obj_opt.create_input_ports_by_data(
                data.get('input_ports') or []
            )
            #
            obj_opt.create_output_ports_by_data(
                data.get('output_ports') or []
            )
            #
            obj_opt.create_ports_by_data(
                data.get('ports') or {}
            )
            #
            obj_opt.set_parameters_by_data(
                data.get('parameters') or {},
            )
            #
            obj_opt.set_arnold_geometry_properties_by_data(
                data.get('arnold_geometry_properties') or {}
            )
            #
            obj_opt.set_expressions_by_data(
                data.get('expressions') or {},
                extend_kwargs=extend_kwargs
            )
            #
            ktn_core.NGObjOpt._create_connections_by_data_(
                data.get('connections') or []
            )
            #
            if type_name in ['GroupStack', 'GroupMerge']:
                child_type_name = data.get('child.type')
                if child_type_name is None:
                    raise RuntimeError()
                ktn_obj.setChildNodeType(child_type_name)
                child_nodes = data.get('child.nodes') or {}
                if child_nodes:
                    child_path_pattern = data.get('child.path_pattern')
                    if child_path_pattern is None:
                        raise RuntimeError()
                    #
                    for i_key, i_data in child_nodes.items():
                        i_var = dict(
                            parent=path,
                            key=i_key
                        )
                        i_data['type'] = child_type_name
                        i_data['path'] = child_path_pattern.format(**i_var)
                        cls._build_node_child_(i_data)
        return ktn_obj, is_create
    @classmethod
    def _build_node_child_(cls, data, extend_kwargs=None):
        type_name = data['type']
        path = data['path']
        ktn_obj, is_create = ktn_core.NGObjOpt._get_group_stack_child_create_args_(path, type_name)
        if is_create is True:
            obj_opt = ktn_core.NGObjOpt(ktn_obj)
            #
            obj_opt.set_color(bsc_core.RawTextOpt(type_name).to_rgb_(maximum=1.0, s_p=25, v_p=25))
            #
            obj_opt.set_attributes(
                data.get('attributes') or {}
            )
            #
            obj_opt.set_parameters_by_data(
                data.get('parameters') or {},
            )
            obj_opt.set_arnold_geometry_properties_by_data(
                data.get('arnold_geometry_properties') or {}
            )
            #
            obj_opt.set_expressions_by_data(
                data.get('expressions') or {},
                extend_kwargs=extend_kwargs
            )

    def gui_layout(self):
        self._ktn_obj_opt.gui_layout_node_graph()

    def save(self):
        file_opt = bsc_core.StgFileOpt(self._file_path)
        macro_file_path = '{}.macro'.format(file_opt.path_base)
        self._ktn_obj_opt.save_as_macro(
            macro_file_path
        )


class ScpWspGeometry(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj
        self._ktn_obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

    def update_variant(self):
        from lxusd import usd_core

        asset_usd_file_path = self._ktn_obj_opt.get('cache.asset_usd.file')

        usd_stage_opt = usd_core.UsdStageOpt(asset_usd_file_path)

        usd_prim_opt = usd_core.UsdPrimOpt(usd_stage_opt.get_obj('/master'))
        usd_variant_dict = usd_prim_opt.get_variant_dict()

        for k, v in usd_variant_dict.iteritems():
            if bsc_core.RawTextOpt(k).get_is_matched('*_main'):
                i_p = 'variant.asset_version_main.{}'.format(k[:-len('_main')])
                i_default, i_values = v
                self._ktn_obj_opt.set_enumerate_strings(i_p, i_values)
                self._ktn_obj_opt.set(i_p, i_default)
            elif bsc_core.RawTextOpt(k).get_is_matched('*_override'):
                i_p = 'variant.asset_version_override.{}'.format(k[:-len('_override')])
                i_default, i_values = v
                self._ktn_obj_opt.set_enumerate_strings(i_p, i_values)
                self._ktn_obj_opt.set(i_p, i_default)


class ScpWspVariantRegister(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj
        self._ktn_obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

    def _get_key_(self):
        return self._ktn_obj_opt.get('extra.variant_key')

    def _get_values_(self):
        ktn_port = self._ktn_obj_opt.get_port('patterns')
        return [ktn_core.NGPortOpt(i).get() for i in ktn_core.NGObjOpt(ktn_port).get_children()]

    def register_variable(self):
        key = self._get_key_()
        values = self._get_values_()
        ktn_core.VariablesSetting().set_register(
            key, values
        )
