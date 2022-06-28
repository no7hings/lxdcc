# coding:utf-8
import types
# noinspection PyUnresolvedReferences
from Katana import CacheManager, NodegraphAPI

from lxbasic import bsc_core

from lxutil import utl_core

import lxutil.objects as utl_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxkatana import ktn_configure, ktn_core

from lxkatana.dcc.dcc_objects import _ktn_dcc_obj_utility, _ktn_dcc_obj_node, _ktn_dcc_obj_nodes

from lxkatana.modifiers import _ktn_mdf_utility

from lxresolver import rsv_configure


class AssetWorkspace(object):
    CONFIGURE_FILE_PATH = ktn_configure.Data.LOOK_KATANA_WORKSPACE_CONFIGURE_PATH
    def __init__(self, location=None):
        self._look_configure_dict = {}
        self._default_configure = self.set_configure_create()
        if location is not None:
            w, h = self._default_configure.get('option.w'), self._default_configure.get('option.h')
            x, y = _ktn_dcc_obj_node.Node(location).get_position()
            self._default_configure.set('option.x', x)
            self._default_configure.set('option.y', y-h/2)
        #
        self._default_configure.set_flatten()

    def get_configure(self, pass_name='default'):
        if pass_name in self._look_configure_dict:
            return self._look_configure_dict[pass_name]
        else:
            configure = self.set_configure_create(pass_name)
            configure.set_flatten()
            return configure
            # raise TypeError()

    def set_configure_create(self, pass_name='default'):
        configure = utl_objects.Configure(value=self.CONFIGURE_FILE_PATH)
        configure.set('option.look_pass', pass_name)
        self._look_configure_dict[pass_name] = configure
        return configure

    def set_workspace_create(self):
        self._set_workspace_create_by_configure_(self._default_configure)

    def get_look_pass_names(self):
        return self._get_look_pass_names_()

    def get_pass_source_obj(self, pass_name):
        node_key = 'look_outputs'
        dcc_main_obj, ktn_main_obj, (x, y) = self.get_main_args(node_key)
        if dcc_main_obj.get_is_exists() is True:
            input_port = dcc_main_obj.get_input_port(pass_name)
            if input_port.get_is_exists() is True:
                return input_port.get_source_obj()

    def get_all_pass_source_obj(self):
        list_ = []
        pass_names = self.get_look_pass_names()
        for i in pass_names:
            list_.append(
                self.get_pass_source_obj(i)
            )
        return list_

    def get_all_dcc_materials(self):
        list_ = []
        query_dict = _ktn_dcc_obj_nodes.Materials.get_nmc_material_dict()
        dcc_objs = self.get_all_pass_source_obj()
        for i_dcc_obj in dcc_objs:
            i_material_paths = ktn_core.SceneGraphOpt(i_dcc_obj.ktn_obj).get_material_paths()
            for j_material_path in i_material_paths:
                if j_material_path in query_dict:
                    j_material_dcc_path = query_dict[j_material_path]
                    if j_material_dcc_path not in list_:
                        list_.append(
                            j_material_dcc_path
                        )
        return list_

    def get_all_dcc_shaders(self):
        list_ = []
        dcc_objs = self.get_all_dcc_materials()
        for i_dcc_obj in dcc_objs:
            list_.extend(
                i_dcc_obj.get_all_source_objs()
            )
        return list_

    def get_look_pass_color(self, pass_name):
        pass_index = self.get_look_pass_index(pass_name)
        return self._get_look_pass_rgb_(
            pass_index
        )
    @classmethod
    def _get_look_pass_rgb_(cls, pass_index):
        h, s, v = 63 + pass_index * 15, .5, .5
        return bsc_core.ColorMtd.hsv2rgb(
            h, s, v, maximum=1
        )

    def get_look_pass_index(self, pass_name):
        look_passes = self.get_look_pass_names()
        if pass_name in look_passes:
            return look_passes.index(pass_name)
        else:
            raise RuntimeError()

    def set_all_executes_run(self):
        configure = self._default_configure
        pass_name = configure.get('option.look_pass')
        workspace_keys = configure.get('workspace').keys()
        for i_key in workspace_keys:
            for j_sub_key in ['main']:
                j_node_path = configure.get('workspace.{}.{}.path'.format(i_key, j_sub_key))
                j_node = _ktn_dcc_obj_node.Node(j_node_path)
                if j_node.get_is_exists() is True:
                    j_node_executes = configure.get('workspace.{}.{}.executes'.format(i_key, j_sub_key))
                    if j_node_executes:
                        self._set_node_executes_(j_node.ktn_obj, j_node_executes)
            #
            i_node_graph_node_dict = configure.get('workspace.{}.node_graph.nodes'.format(i_key))
            if i_node_graph_node_dict:
                for seq, (j_key, j_node_dict) in enumerate(i_node_graph_node_dict.items()):
                    j_node_path = j_node_dict['path']
                    j_node = _ktn_dcc_obj_node.Node(j_node_path)
                    if j_node.get_is_exists() is True:
                        j_node_executes = j_node_dict.get('executes')
                        if j_node_executes:
                            self._set_node_executes_(j_node.ktn_obj, j_node_executes)

    def set_variables_registry(self):
        keys = ['layer', 'quality', 'camera', 'look_pass', 'light_pass']
        variable_switches = ktn_core.NGObjTypeOpt('VariableSwitch').get_objs()
        for i in variable_switches:
            i_obj_opt = ktn_core.NGObjOpt(i)
            i_key = i_obj_opt.get('lynxi_variants.key')
            if i_key in keys:
                i_obj_opt.set_port_execute('lynxi_variants.register_variable')
        #
        ktn_core.VariablesSetting().set_register_by_configure(
            {
                'variables_enable': ['on', 'off']
            }
        )

    def _get_look_pass_names_(self):
        lis = []
        node_key = 'look_outputs'
        dcc_main_obj, ktn_main_obj, (x, y) = self.get_main_args(node_key)
        if dcc_main_obj.get_is_exists() is True:
            input_ports = dcc_main_obj.get_input_ports()
            for i_input_port in input_ports:
                i_port_path = i_input_port.name
                if not i_port_path in ['orig']:
                    lis.append(i_port_path)
        return lis
    @_ktn_mdf_utility.set_undo_mark_mdf
    def set_look_pass_add(self, pass_name=None):
        pass_names = self.get_look_pass_names()
        pass_count = len(pass_names)
        if pass_name is None:
            pass_name = 'pass_{}'.format(pass_count)
        #
        if pass_name not in pass_names:
            configure = self.set_configure_create(pass_name)
            r, g, b = self._get_look_pass_rgb_(pass_count+1)
            configure.set('option.look_pass_color', dict(r=r, g=g, b=b))
            w = configure.get('option.w')
            offset_x = w * pass_count * 2
            configure.set('option.offset_x', offset_x)
            configure.set_flatten()
            self._set_workspace_create_by_configure_(configure)
            utl_core.Log.set_module_result_trace(
                'look-pass add',
                'look-pass"{}"'.format(pass_name)
            )
        else:
            utl_core.Log.set_module_warning_trace(
                'look pass add',
                'look-pass="{}" is exists'.format(pass_name)
            )
    @classmethod
    def _set_workspace_create_by_configure_(cls, configure):
        workspace_keys = configure.get('workspace').keys()
        #
        method_args = [
            cls._set_workspace_nodes_create_mtd_,
            cls._set_workspace_connections_create_mtd_,
            cls._set_workspace_node_graphs_create_mtd_
        ]
        with utl_core.gui_progress(maximum=len(method_args)) as g_p:
            for i_method in method_args:
                g_p.set_update()
                i_method(configure, workspace_keys)
    @classmethod
    def _set_workspace_nodes_create_mtd_(cls, configure, workspace_keys):
        pass_name = configure.get('option.look_pass')
        with utl_core.gui_progress(maximum=len(workspace_keys)) as g_p:
            for i_key in workspace_keys:
                g_p.set_update()
                for j_sub_key in ['main', 'backdrop']:
                    cls._set_workspace_node_create_(configure, i_key, j_sub_key, pass_name)
    @classmethod
    def _set_workspace_node_create_(cls, configure, key, sub_key, pass_name='default'):
        variable = configure.get('workspace.{}.{}.variable'.format(key, sub_key))
        if pass_name != 'default':
            if not variable:
                return
        #
        node_obj_path = configure.get('workspace.{}.{}.path'.format(key, sub_key))
        if node_obj_path is not None:
            node_obj_type_name = configure.get('workspace.{}.{}.obj_type'.format(key, sub_key))
            node_base_obj_type = configure.get('workspace.{}.{}.base_obj_type'.format(key, sub_key))
            #
            dcc_node = _ktn_dcc_obj_node.Node(node_obj_path)
            ktn_node, is_create = dcc_node.get_dcc_instance(node_obj_type_name, node_base_obj_type)
            if is_create is True:
                node_attributes = configure.get('workspace.{}.{}.attributes'.format(key, sub_key))
                if node_attributes:
                    ktn_node.setAttributes(node_attributes)
                #
                node_pos = configure.get('workspace.{}.{}.pos'.format(key, sub_key))
                if node_pos:
                    NodegraphAPI.SetNodePosition(ktn_node, node_pos)
                #
                node_parameters = configure.get('workspace.{}.{}.parameters'.format(key, sub_key))
                if node_parameters:
                    for i_parameter_port_path, parameter_value in node_parameters.items():
                        i_parameter_port_path = i_parameter_port_path.replace('/', '.')
                        dcc_node.get_port(i_parameter_port_path).set(parameter_value)
                #
                node_executes = configure.get('workspace.{}.{}.executes'.format(key, sub_key))
                if node_executes:
                    cls._set_node_executes_(ktn_node, node_executes)
                #
                child_dcc_type = configure.get('workspace.{}.{}.child_obj_type'.format(key, sub_key))
                if child_dcc_type is not None:
                    ktn_node.setChildNodeType(child_dcc_type)
            #
            node_outputs = configure.get('workspace.{}.{}.outputs'.format(key, sub_key))
            if node_outputs:
                for port_name in node_outputs:
                    ktn_port = ktn_node.getOutputPort(port_name)
                    if ktn_port is None:
                        ktn_node.addOutputPort(port_name)
    @classmethod
    def _set_workspace_connections_create_mtd_(cls, configure, workspace_keys):
        pass_name = configure.get('option.look_pass')
        with utl_core.gui_progress(maximum=len(workspace_keys)) as g_p:
            for key in workspace_keys:
                g_p.set_update()
                for sub_key in ['main', 'node_graph']:
                    cls._set_workspace_connections_create_(configure, key, sub_key, pass_name)
    @classmethod
    def _set_workspace_connections_create_(cls, configure, key, sub_key, pass_name='default'):
        variable = configure.get('workspace.{}.{}.variable'.format(key, sub_key))
        if pass_name != 'default':
            if not variable:
                return
        node_connections = configure.get('workspace.{}.{}.connections'.format(key, sub_key))
        if node_connections:
            cls._set_node_connections_create_(node_connections)
    @classmethod
    def _set_workspace_node_graphs_create_mtd_(cls, configure, workspace_keys):
        pass_name = configure.get('option.look_pass')
        with utl_core.gui_progress(maximum=len(workspace_keys)) as g_p:
            for key in workspace_keys:
                g_p.set_update()
                cls._set_workspace_node_graph_create_(configure, key, pass_name)
    @classmethod
    def _set_workspace_node_graph_create_(cls, configure, key, pass_name):
        node_graph_node_dict = configure.get('workspace.{}.node_graph.nodes'.format(key))
        cls._set_node_graph_nodes_create_(node_graph_node_dict, pass_name)
    @classmethod
    def _set_node_graph_nodes_create_(cls, nodes_dict, pass_name='default'):
        if nodes_dict:
            for seq, (k, i_node_dict) in enumerate(nodes_dict.items()):
                cls._set_node_graph_node_create_(i_node_dict, pass_name)
    @classmethod
    def _set_node_graph_node_create_(cls, node_dict, pass_name='default'):
        variable = node_dict.get('variable')
        if pass_name != 'default':
            if not variable:
                return
        #
        node_obj_path = node_dict['path']
        node_obj_category = node_dict['obj_category']
        node_obj_type = node_dict['obj_type']
        node_base_obj_type = node_dict.get('base_obj_type')
        dcc_node = _ktn_dcc_obj_node.Node(node_obj_path)
        node_ktn_obj, is_create = dcc_node.get_dcc_instance(node_obj_type, node_base_obj_type)
        if is_create is True:
            if node_obj_category == 'group':
                child_dcc_type = node_dict['child_obj_type']
                if child_dcc_type is not None:
                    node_ktn_obj.setChildNodeType(child_dcc_type)
            #
            node_attributes = node_dict.get('attributes')
            if node_attributes:
                node_ktn_obj.setAttributes(node_attributes)
            #
            insert_connections = node_dict.get('insert_connections')
            if insert_connections:
                insert_scheme = node_dict.get('insert_scheme')
                cls._set_node_insert_connections_create_(insert_connections, insert_scheme)
            #
            split_connections = node_dict.get('split_connections')
            if split_connections:
                cls._set_node_spit_connections_create_(split_connections)

            connections = node_dict.get('connections')
            if connections:
                cls._set_node_connections_create_(connections)
            #
            parameters = node_dict.get('parameters')
            if parameters:
                cls._set_node_parameters_(dcc_node, parameters)

            arnold_geometry_properties = node_dict.get('arnold_geometry_properties')
            if arnold_geometry_properties:
                cls._set_arnold_geometry_properties_(dcc_node, arnold_geometry_properties)
            #
            executes = node_dict.get('executes')
            if executes:
                cls._set_node_executes_(node_ktn_obj, executes)
    @classmethod
    def _set_node_connections_create_(cls, node_connections, extend_variants=None):
        if extend_variants is None:
            extend_variants = {}
        for seq, i in enumerate(node_connections):
            if not (seq + 1) % 2:
                source_attr_path = node_connections[seq - 1]
                target_attr_path = i
                if extend_variants:
                    source_attr_path = source_attr_path.format(**extend_variants)
                    target_attr_path = target_attr_path.format(**extend_variants)
                #
                source_obj_path, source_port_name = source_attr_path.split('.')
                target_obj_path, target_port_name = target_attr_path.split('.')
                #
                source_dcc_obj = _ktn_dcc_obj_node.Node(source_obj_path)
                source_dcc_port = source_dcc_obj.get_output_port(source_port_name)
                source_ktn_port, _ = source_dcc_port.get_dcc_instance()
                #
                target_dcc_obj = _ktn_dcc_obj_node.Node(target_obj_path)
                target_dcc_port = target_dcc_obj.get_input_port(target_port_name)
                target_ktn_port, _ = target_dcc_port.get_dcc_instance()
                #
                source_ktn_port.connect(target_ktn_port)
    @classmethod
    def _set_node_executes_(cls, ktn_obj, executes):
        for i_port_path in executes:
            ktn_core.NGObjOpt(ktn_obj).set_port_execute(i_port_path)
    @classmethod
    def _set_node_insert_connections_create_(cls, node_insert_connections, insert_scheme):
        if node_insert_connections:
            for seq, i in enumerate(node_insert_connections):
                if not (seq + 1) % 4:
                    source_attr_path = node_insert_connections[seq - 3]
                    target_attr_path = node_insert_connections[seq - 2]
                    #
                    input_attr_path_ = node_insert_connections[seq - 1]
                    output_attr_path_ = i
                    #
                    s_ktn_port, t_ktn_port = cls._get_node_connect_args_(source_attr_path, target_attr_path)
                    #
                    node_obj_path_, input_port_name_ = input_attr_path_.split('.')
                    node_dcc_obj_ = _ktn_dcc_obj_node.Node(node_obj_path_)
                    node_ktn_obj_ = node_dcc_obj_.ktn_obj
                    #
                    node_obj_path_, output_port_name_ = output_attr_path_.split('.')
                    #
                    i_ktn_obj = node_ktn_obj_.getInputPort(input_port_name_)
                    o_ktn_obj = node_ktn_obj_.getOutputPort(output_port_name_)
                    #
                    if insert_scheme == 'TB':
                        x, y = NodegraphAPI.GetNodePosition(s_ktn_port.getNode())
                        NodegraphAPI.SetNodePosition(node_ktn_obj_, (x, y - 48))
                    elif insert_scheme == 'BT':
                        x, y = NodegraphAPI.GetNodePosition(t_ktn_port.getNode())
                        NodegraphAPI.SetNodePosition(node_ktn_obj_, (x, y + 48*2))
                    #
                    s_ktn_port.connect(i_ktn_obj)
                    o_ktn_obj.connect(t_ktn_port)
    @classmethod
    def _set_node_spit_connections_create_(cls, node_connections):
        if node_connections:
            for seq, i in enumerate(node_connections):
                if not (seq + 1) % 4:
                    source_attr_path = node_connections[seq - 3]
                    target_attr_path = node_connections[seq - 2]
                    #
                    input_attr_path_ = node_connections[seq - 1]
                    output_attr_path_ = i
                    #
                    source_obj_path, source_port_name = source_attr_path.split('.')
                    s_ktn_port = _ktn_dcc_obj_node.Node(source_obj_path).ktn_obj.getOutputPort(source_port_name)
                    target_obj_path, target_port_name = target_attr_path.split('.')
                    t_ktn_port = _ktn_dcc_obj_node.Node(target_obj_path).ktn_obj.getInputPort(target_port_name)
                    #
                    node_obj_path_, input_port_name_ = input_attr_path_.split('.')
                    node_dcc_obj_ = _ktn_dcc_obj_node.Node(node_obj_path_)
                    node_ktn_obj_ = node_dcc_obj_.ktn_obj
                    #
                    node_obj_path_, output_port_name_ = output_attr_path_.split('.')
                    #
                    i_ktn_obj = node_ktn_obj_.getInputPort(input_port_name_)
                    o_ktn_obj = node_ktn_obj_.getOutputPort(output_port_name_)
                    #
                    x, y = NodegraphAPI.GetNodePosition(t_ktn_port.getNode())
                    NodegraphAPI.SetNodePosition(node_ktn_obj_, (x, y + 48*2))
                    #
                    s_ktn_port.connect(i_ktn_obj)
                    o_ktn_obj.connect(t_ktn_port)
    @classmethod
    def _set_node_parameters_(cls, dcc_node, parameters):
        for i_port_path, i_value in parameters.items():
            i_port_path = i_port_path.replace('/', '.')
            dcc_node.get_port(i_port_path).set(i_value)
    # geometry properties
    @classmethod
    def _set_arnold_geometry_properties_(cls, dcc_node, properties_dict):
        for i_port_path, i_value in properties_dict.items():
            i_port_path = i_port_path.replace('/', '.')
            cls._set_arnold_geometry_property_(dcc_node, i_port_path, i_value)
    @classmethod
    def _set_arnold_geometry_property_(cls, dcc_node, parameter_port_name, parameter_value):
        convert_dict = dict(
            subdiv_iterations='iterations',
            disp_zero_value='zero_value'
        )
        if parameter_port_name in convert_dict:
            parameter_port_name = convert_dict[parameter_port_name]
        #
        enable_ktn_port_name = 'args.arnoldStatements.{}.enable'.format(parameter_port_name)
        enable_dcc_port = dcc_node.get_port(enable_ktn_port_name)
        if enable_dcc_port.get_is_exists() is True:
            enable_dcc_port.set(True)
        else:
            utl_core.Log.set_warning_trace(
                'port-name="{}" is unknown'.format(parameter_port_name)
            )
        #
        value_ktn_port_name = 'args.arnoldStatements.{}.value'.format(parameter_port_name)
        value_dcc_port = dcc_node.get_port(value_ktn_port_name)
        if value_dcc_port.get_is_exists() is True:
            value_dcc_port.set(parameter_value)
    #
    @classmethod
    def _get_node_connect_args_(cls, source_attr_path, target_attr_path):
        def rcs_fnc_(o_ktn_port_):
            _target_ktn_ports = o_ktn_port_.getConnectedPorts()
            if _target_ktn_ports:
                _target_ktn_port = _target_ktn_ports[0]
                if _target_ktn_port == i_ktn_port:
                    return o_ktn_port_
                else:
                    _target_node = _target_ktn_port.getNode()
                    _o_ktn_ports = _target_node.getOutputPorts()
                    if _o_ktn_ports:
                        _o_ktn_port = _o_ktn_ports[0]
                        return rcs_fnc_(_o_ktn_port)
        #
        source_obj_path, source_port_name = source_attr_path.split('.')
        o_ktn_port = _ktn_dcc_obj_node.Node(source_obj_path).ktn_obj.getOutputPort(source_port_name)
        target_obj_path, target_port_name = target_attr_path.split('.')
        i_ktn_port = _ktn_dcc_obj_node.Node(target_obj_path).ktn_obj.getInputPort(target_port_name)
        #
        s_ktn_port = rcs_fnc_(o_ktn_port)
        t_ktn_port = i_ktn_port
        #
        return s_ktn_port, t_ktn_port
    @classmethod
    def _get_main_args_(cls, configure, key):
        dcc_path = configure.get('workspace.{}.main.path'.format(key))
        dcc_obj = _ktn_dcc_obj_node.Node(dcc_path)
        ktn_obj = dcc_obj.ktn_obj
        return dcc_obj, ktn_obj, NodegraphAPI.GetNodePosition(ktn_obj)
    @classmethod
    def _get_group_args_(cls, configure, key, group_key):
        dcc_path = configure.get('workspace.{}.node_graph.nodes.{}.path'.format(key, group_key))
        dcc_obj = _ktn_dcc_obj_node.Node(dcc_path)
        ktn_obj = dcc_obj.ktn_obj
        return dcc_obj, ktn_obj, NodegraphAPI.GetNodePosition(ktn_obj)

    def get_main_args(self, key, pass_name='default'):
        configure = self.get_configure(pass_name=pass_name)
        return self._get_main_args_(configure, key)

    def get_group_args(self, key, group_key, pass_name='default'):
        configure = self.get_configure(pass_name=pass_name)
        return self._get_group_args_(configure, key, group_key)
    # asset-geometry-abc
    def set_geometry_abc_import(self, file_path):
        configure = self.get_configure()
        key = 'geometry_abc'
        dcc_main_obj, dcc_node = self._set_main_node_create_(configure, key)
        if dcc_node is not None:
            file_parameter_name = configure.get('node.{}.main.file_parameter'.format(key))
            dcc_node.get_port(file_parameter_name).set(file_path)
            utl_core.Log.set_module_result_trace(
                '{}-import'.format(key),
                u'file="{}"'.format(file_path)
            )
    # asset-geometry-usd
    def set_geometry_usd_import(self, file_path):
        configure = self.get_configure()
        key = 'geometry_usd'
        dcc_main_obj, dcc_node = self._set_main_node_create_(configure, key, break_source_connections=False)
        if dcc_node is not None:
            file_parameter_name = configure.get('node.{}.main.file_parameter'.format(key))
            dcc_node.get_port(file_parameter_name).set(file_path)
            utl_core.Log.set_module_result_trace(
                '{}-import'.format(key),
                u'file="{}"'.format(file_path)
            )
    #
    def set_geometry_xgen_import(self, file_path, extend_variants):
        configure = self.get_configure()
        key = 'geometry_xgen'
        dcc_main_obj, dcc_node = self._set_main_node_create_(
            configure,
            key,
            extend_variants=extend_variants,
            break_source_connections=False
        )
        if dcc_node is not None:
            file_parameter_name = configure.get('node.{}.main.file_parameter'.format(key))
            dcc_node.get_port(file_parameter_name).set(file_path)
            utl_core.Log.set_module_result_trace(
                '{}-import'.format(key),
                u'file="{}"'.format(file_path)
            )
    # model-usd
    def set_model_usd_import(self, file_path):
        configure = self.get_configure()
        key = 'model_usd'
        dcc_main_obj, dcc_node = self._set_main_node_create_(
            configure,
            key,
            break_source_connections=False
        )
        if dcc_node is not None:
            file_parameter_name = configure.get('node.{}.main.file_parameter'.format(key))
            dcc_node.get_port(file_parameter_name).set(file_path)
            utl_core.Log.set_module_result_trace(
                '{}-import'.format(key),
                u'file="{}"'.format(file_path)
            )
    # hair-usd
    def set_groom_geometry_usd_import(self, file_path):
        configure = self.get_configure()
        key = 'groom_geometry_usd'
        dcc_main_obj, dcc_node = self._set_main_node_create_(configure, key, break_source_connections=False)
        if dcc_node is not None:
            file_parameter_name = configure.get('node.{}.main.file_parameter'.format(key))
            dcc_node.get_port(file_parameter_name).set(file_path)
            utl_core.Log.set_module_result_trace(
                'hair-usd-import',
                u'file="{}"'.format(file_path)
            )
    # effect-usd
    def set_effect_usd_import(self, file_path):
        configure = self.get_configure()
        key = 'effect_usd'
        dcc_main_obj, dcc_node = self._set_main_node_create_(configure, key, break_source_connections=False)
        if dcc_node is not None:
            file_parameter_name = configure.get('node.{}.main.file_parameter'.format(key))
            dcc_node.get_port(file_parameter_name).set(file_path)
            utl_core.Log.set_module_result_trace(
                '{}-import'.format(key),
                u'file="{}"'.format(file_path)
            )
    # asset-set
    def set_set_usd_import(self, file_path):
        configure = self.get_configure()
        key = 'set_usd'
        dcc_main_obj, dcc_node = self._set_main_node_create_(configure, key)
        if dcc_node is not None:
            file_parameter_name = configure.get('node.{}.main.file_parameter'.format(key))
            dcc_node.get_port(file_parameter_name).set(file_path)
            utl_core.Log.set_module_result_trace(
                '{}-import'.format(key),
                u'file="{}"'.format(file_path)
            )
        #
        CacheManager.flush()

    def set_camera_persp_abc_import(self, file_path, path):
        configure = self.get_configure()
        key = 'camera_abc'
        dcc_main_obj, dcc_node = self._set_main_node_create_(configure, key, break_source_connections=False)
        camera_root = configure.get('option.camera_root')
        if dcc_node is not None:
            dcc_node.get_port('camera.file').set(file_path)
            dcc_node.get_port('camera.path').set('{}{}'.format(camera_root, path))
            utl_core.Log.set_module_result_trace(
                '{}-import'.format(key),
                u'file="{}"'.format(file_path)
            )
        #
        CacheManager.flush()

    def set_render_camera(self, path):
        configure = self.get_configure()
        key_0 = 'render_settings'
        dcc_main_obj, ktn_main_obj, (x, y) = self._get_main_args_(configure, key_0)
        camera_root = configure.get('option.camera_root')
        dcc_main_obj.get_port(
            'render_settings.camera_enable'
        ).set(True)
        dcc_main_obj.get_port(
            'render_settings.camera'
        ).set(
            '{}{}'.format(camera_root, path)
        )

    def set_render_resolution(self, width, height):
        configure = self.get_configure()
        main_key = 'render_settings'
        dcc_main_obj, ktn_main_obj, (x, y) = self._get_main_args_(configure, main_key)
        #
        dcc_main_obj.get_port(
            'render_settings.resolution_enable'
        ).set(True)
        dcc_main_obj.get_port(
            'render_settings.resolution'
        ).set('{}x{}'.format(width, height))
    @classmethod
    def _get_merge_index_(cls, merge, target_port_name):
        input_port_paths = [i.port_path for i in merge.get_input_ports()]
        if target_port_name in input_port_paths:
            return input_port_paths.index(target_port_name)
        return len(input_port_paths)

    def _set_main_node_create_(self, configure, key, extend_variants=None, break_source_connections=True):
        if extend_variants is None:
            extend_variants = {}
        #
        node_key = configure.get('node.{}.keyword'.format(key))
        dcc_main_obj, ktn_main_obj, (x, y) = self._get_main_args_(configure, node_key)
        #
        if break_source_connections is True:
            dcc_main_obj.set_sources_disconnect()
        #
        if dcc_main_obj.get_is_exists() is True:
            w, h = configure.get('option.w'), configure.get('option.h')
            margin = configure.get('option.margin')
            spacing_x = configure.get('option.spacing_x')
            spacing_y = configure.get('option.spacing_y')
            #
            node_obj_path = configure.get('node.{}.main.path'.format(key))
            node_obj_path = node_obj_path.format(**extend_variants)
            node_obj_type = configure.get('node.{}.main.obj_type'.format(key))
            #
            dcc_node = _ktn_dcc_obj_node.Node(node_obj_path)
            ktn_node, is_create = dcc_node.get_dcc_instance(node_obj_type)
            #
            node_parameters = configure.get('node.{}.main.parameters'.format(key))
            if node_parameters:
                for i_parameter_port_path, i_parameter_value in node_parameters.items():
                    i_parameter_port_path = i_parameter_port_path.replace('/', '.')
                    i_parameter_value = i_parameter_value.format(**extend_variants)
                    dcc_node.get_port(i_parameter_port_path).set(i_parameter_value)
            #
            node_connections = configure.get('node.{}.main.connections'.format(key))
            if node_connections:
                self._set_node_connections_create_(
                    node_connections,
                    extend_variants=extend_variants
                )
            #
            index = len([i.getName() for i in ktn_main_obj.getInputPorts()])
            if is_create is True:
                node_attributes = configure.get('node.{}.main.attributes'.format(key))
                if node_attributes:
                    ktn_node.setAttributes(node_attributes)
                NodegraphAPI.SetNodePosition(ktn_node, (x - w / 2 + spacing_x * index, y + margin + spacing_y * 2))
            return dcc_main_obj, dcc_node

    def set_look_klf_file_export(self, file_path):
        configure = self.get_configure()
        key = 'look_outputs'
        asset_root = configure.get('option.asset_root')
        obj_path = configure.get('workspace.{}.main.path'.format(key))
        dcc_obj = _ktn_dcc_obj_node.Node(obj_path)
        if dcc_obj.get_is_exists() is True:
            ktn_obj = dcc_obj.ktn_obj
            #
            dcc_obj.get_port('rootLocations').set([asset_root])
            dcc_obj.get_port('saveTo').set(file_path)
            #
            os_file = utl_dcc_objects.OsFile(file_path)
            os_file.set_directory_create()
            ktn_obj.WriteToLookFile(None, file_path)
            #
            utl_core.Log.set_module_result_trace(
                'look-klf export',
                '"{}"'.format(file_path)
            )
        else:
            raise RuntimeError(
                utl_core.Log.set_module_error_trace(
                    'look-klf export',
                    'obj="{}" is non-exists'.format(dcc_obj.path)
                )
            )
    @_ktn_mdf_utility.set_undo_mark_mdf
    def set_light_rig_update(self):
        configure = self.get_configure()
        key = 'light_rigs'
        sub_key = 'main'
        node_obj_path = configure.get('workspace.{}.{}.path'.format(key, sub_key))
        node_obj_type_name = configure.get('workspace.{}.{}.obj_type'.format(key, sub_key))
        dcc_node = _ktn_dcc_obj_node.Node(node_obj_path)
        source_connections = dcc_node.get_source_connections()
        target_connections = dcc_node.get_target_connections()
        properties = dcc_node.get_properties(
            [
                'user.render_quality',
                'user.Layer_Name',
                'user.Output_Path',
                'user.camera',
                'user.HDRI',
                'user.Controls.Lighting_rotation',
                'user.Show_Background'
            ]
        )
        #
        dcc_node.set_delete()
        ktn_node, is_create = dcc_node.get_dcc_instance(node_obj_type_name)
        if is_create is True:
            node_attributes = configure.get('workspace.{}.{}.attributes'.format(key, sub_key))
            if node_attributes:
                ktn_node.setAttributes(node_attributes)
            #
            node_pos = configure.get('workspace.{}.{}.pos'.format(key, sub_key))
            if node_pos:
                NodegraphAPI.SetNodePosition(ktn_node, node_pos)
        #
        for i in source_connections:
            source_ktn_port = i.source.ktn_port
            target_ktn_port = i.target.ktn_port
            source_ktn_port.connect(target_ktn_port)
        for i in target_connections:
            source_ktn_port = i.source.ktn_port
            target_ktn_port = i.target.ktn_port
            source_ktn_port.connect(target_ktn_port)
        #
        dcc_node.set_properties(properties)
        return dcc_node

    def get_geometry_usd_model_hi_file_path(self):
        configure = self.get_configure()
        asset_root = configure.get('option.asset_root')
        atr_path = '{}.userProperties.geometry__model__hi'.format(asset_root)
        _ = self._get_stage_port_raw_(atr_path)
        if _:
            return _[0]

    def get_geometry_uv_map_usd_source_file(self):
        configure = self.get_configure()
        asset_root = configure.get('option.asset_root')
        #
        atr_path = '{}.userProperties.geometry__surface__hi'.format(asset_root)
        _ = self._get_stage_port_raw_(atr_path)
        if _:
            return _[0]
        #
        atr_path = '{}.userProperties.usd.variants.asset.surface.override.file'.format(asset_root)
        _ = self._get_stage_port_raw_(atr_path)
        if _:
            f = utl_dcc_objects.OsFile(_[0])
            # TODO fix this bug
            if f.get_is_naming_match('hi.uv_map.usd'):
                return '{}/hi.usd'.format(
                    f.directory.path
                )
            return _[0]

    def get_geometry_usd_check_raw(self):
        dic = {}
        workspace_configure = self.get_configure()
        set_usd_configure = utl_objects.Configure(value=rsv_configure.Data.GEOMETRY_USD_CONFIGURE_PATH)
        for element_label in set_usd_configure.get_branch_keys('elements'):
            asset_root = workspace_configure.get('option.asset_root')
            atr_path = '{}.userProperties.geometry__{}'.format(asset_root, element_label)
            _ = self._get_stage_port_raw_(atr_path)
            if _:
                dic[element_label] = _[0]
        return dic

    def get_asset_usd_check_raw(self):
        obj = _ktn_dcc_obj_node.Node('asset_geometries')
        if obj.get_is_exists() is True:
            pass
        else:
            pass

    def _get_stage_port_raw_(self, atr_path):
        configure = self.get_configure()
        key = 'look_outputs'
        obj_path = configure.get('workspace.{}.main.path'.format(key))
        dcc_obj = _ktn_dcc_obj_node.Node(obj_path)
        if dcc_obj.get_is_exists() is True:
            scene_graph_opt = ktn_core.SceneGraphOpt(dcc_obj.ktn_obj)
            return scene_graph_opt.get_port_raw(atr_path)
        else:
            raise RuntimeError(
                utl_core.Log.set_module_error_trace(
                    'obj="{}" is non-exists'.format(dcc_obj.path)
                )
            )

    def get_sg_geometries(self, pass_name='default'):
        configure = self.get_configure(pass_name)
        geometry_location = configure.get('option.geometry_root')
        #
        root = '{}/master'.format(geometry_location)
        #
        obj_scene = _ktn_dcc_obj_utility.Scene()
        obj_scene.set_load_by_root(
            ktn_obj='{}__material_assigns_merge'.format(pass_name),
            root=root,
        )
        obj_universe = obj_scene.universe
        lis = []
        for i_obj_type_name in ['subdmesh', 'renderer procedural']:
            obj_type = obj_universe.get_obj_type(i_obj_type_name)
            if obj_type is not None:
                lis.extend(obj_type.get_objs())
        return lis

    def get_ng_material_groups(self):
        lis = []
        node_key = 'materials'
        dcc_main_obj, ktn_main_obj, (x, y) = self.get_main_args(node_key)
        if dcc_main_obj.get_is_exists() is True:
            input_ports = dcc_main_obj.get_input_ports()
            for i_input_port in input_ports:
                lis.append(i_input_port.obj)
        return lis
    #
    def set_ng_material_group_create(self, name, pass_name='default'):
        configure = self.get_configure(pass_name)
        w, h = configure.get('option.w'), configure.get('option.h')
        key = 'material_group'
        node_key = configure.get('node.{}.keyword'.format(key))
        dcc_materials_merge, ktn_materials_merge, (x, y) = self.get_main_args(
            node_key,
            pass_name=pass_name
        )
        #
        dcc_path_format = configure.get('node.{}.main.path'.format(key))
        dcc_format = dcc_path_format.format(name=name)
        dcc_type_name = configure.get('node.{}.main.obj_type'.format(key))
        #
        dcc_obj = _ktn_dcc_obj_node.Node(dcc_format)
        if dcc_obj.get_is_exists() is True:
            dcc_obj.set_delete()
        #
        ktn_obj, is_create = dcc_obj.get_dcc_instance(dcc_type_name)
        target_port_name = dcc_obj.name
        #
        index = self._get_merge_index_(dcc_materials_merge, target_port_name)
        d = 8
        if is_create is True:
            _x = index % d
            _y = int(index / d)
            r, g, b = self.get_look_pass_color(pass_name)
            x, y = x + _x * w / 2, y + h + _y * h / 2
            node_attributes = configure.get_content('node.{}.main.attributes'.format(key))
            if node_attributes:
                node_attributes.set('x', x)
                node_attributes.set('y', y)
                node_attributes.set('ns_colorr', r)
                node_attributes.set('ns_colorg', g)
                node_attributes.set('ns_colorb', b)
                ktn_obj.setAttributes(node_attributes.value)
            #
            dcc_materials_merge.get_input_port(target_port_name).set_create()
        #
        dcc_obj.get_output_port('out').set_target(
            dcc_materials_merge.get_input_port(target_port_name)
        )
        return dcc_obj, ktn_obj
    #
    def get_ng_material_group(self, name, pass_name='default'):
        configure = self.get_configure(pass_name)
        key = 'material_group'
        dcc_path_format = configure.get('node.{}.main.path'.format(key))
        dcc_path = dcc_path_format.format(name=name)
        dcc_obj = _ktn_dcc_obj_node.Node(dcc_path)
        return dcc_obj, dcc_obj.ktn_obj
    #
    def set_ng_material_create(self, name, pass_name='default'):
        configure = self.get_configure(pass_name)
        dcc_material_group, ktn_material_group = self.set_ng_material_group_create(
            name=name,
            pass_name=pass_name
        )
        #
        key = 'material'
        dcc_name_format = configure.get('node.{}.main.name'.format(key))
        dcc_name = dcc_name_format.format(name=name)
        #
        dcc_path = '{}/{}'.format(dcc_material_group.path, dcc_name)
        #
        _ktn_dcc_obj_node.Node('{}/NetworkMaterial'.format(dcc_material_group.path)).set_rename(dcc_name)
        #
        dcc_obj = _ktn_dcc_obj_node.Node(dcc_path)
        ktn_obj, is_create = dcc_obj.get_dcc_instance('NetworkMaterial')
        return dcc_obj, ktn_obj
    #
    def get_ng_material_name(self, name, pass_name='default'):
        configure = self.get_configure(pass_name)
        key = 'material'
        dcc_name_format = configure.get('node.{}.main.name'.format(key))
        dcc_name = dcc_name_format.format(name=name)
        return dcc_name

    def get_ng_shader_name(self, name, pass_name='default'):
        configure = self.get_configure(pass_name)
        key = 'shader'
        dcc_name_format = configure.get('node.{}.main.name'.format(key))
        dcc_name = dcc_name_format.format(name=name)
        return dcc_name

    def get_ng_shader_name_0(self):
        pass
    #
    def set_ng_geometry_material_assign_create(self, name, assign=None, pass_name='default'):
        configure = self.get_configure(pass_name)
        key = 'material_assign'
        node_key = configure.get('node.{}.keyword'.format(key))
        dcc_group, ktn_group, (x, y) = self.get_group_args(
            node_key,
            group_key='definition',
            pass_name=pass_name
        )
        #
        dcc_path_format = configure.get('node.{}.main.path'.format(key))
        dcc_path = dcc_path_format.format(name=name)
        #
        dcc_obj = _ktn_dcc_obj_node.Node(dcc_path)
        ktn_obj, is_create = ktn_core.NGGroupStackOpt(ktn_group).set_child_create(
            dcc_obj.name
        )
        if is_create is True:
            node_attributes = configure.get_content('node.{}.main.attributes'.format(key))
            if node_attributes:
                node_attributes.set_update(ktn_obj.getAttributes())
                r, g, b = self.get_look_pass_color(pass_name)
                node_attributes.set('ns_colorr', r)
                node_attributes.set('ns_colorg', g)
                node_attributes.set('ns_colorb', b)
                ktn_obj.setAttributes(node_attributes.value)
        #
        if isinstance(assign, tuple):
            geometry_path, material_path = assign
            dcc_obj.get_port('CEL').set(geometry_path)
            dcc_obj.get_port('args.materialAssign.value').set(material_path)
        return dcc_obj, ktn_obj

    def get_ng_geometry_material_assign(self, name, pass_name='default'):
        configure = self.get_configure(pass_name)
        key = 'material_assign'
        dcc_path_format = configure.get('node.{}.main.path'.format(key))
        dcc_path = dcc_path_format.format(name=name)
        dcc_obj = _ktn_dcc_obj_node.Node(dcc_path)
        return dcc_obj, dcc_obj.ktn_obj

    def get_ng_geometry_property_assign(self, name, pass_name='default'):
        configure = self.get_configure(pass_name)
        key = 'property_assign'
        dcc_path_format = configure.get('node.{}.main.path'.format(key))
        dcc_path = dcc_path_format.format(name=name)
        dcc_obj = _ktn_dcc_obj_node.Node(dcc_path)
        return dcc_obj, dcc_obj.ktn_obj

    def set_ng_geometry_properties_create(self, name, pass_name='default'):
        configure = self.get_configure(pass_name)
        key = 'property_assign'
        node_key = configure.get('node.{}.keyword'.format(key))
        dcc_properties_group, ktn_properties_group, (x, y) = self.get_group_args(
            node_key,
            group_key='definition',
            pass_name=pass_name
        )
        #
        properties_path_format = configure.get('node.{}.main.path'.format(key))
        properties_path = properties_path_format.format(name=name)
        #
        dcc_properties = _ktn_dcc_obj_node.Node(properties_path)
        ktn_properties, is_create = ktn_core.NGGroupStackOpt(ktn_properties_group).set_child_create(
            dcc_properties.name
        )
        if is_create is True:
            node_attributes = configure.get_content('node.{}.main.attributes'.format(key))
            if node_attributes:
                node_attributes.set_update(ktn_properties.getAttributes())
                r, g, b = self.get_look_pass_color(pass_name)
                node_attributes.set('ns_colorr', r)
                node_attributes.set('ns_colorg', g)
                node_attributes.set('ns_colorb', b)
                ktn_properties.setAttributes(node_attributes.value)
        return dcc_properties, ktn_properties

    def get_ng_look_pass(self, pass_name='default'):
        _ = '{}__look'.format(pass_name)
        dcc_obj = _ktn_dcc_obj_node.Node(_)
        return dcc_obj, dcc_obj.ktn_obj
