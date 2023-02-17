# coding:utf-8
import six

import collections

import threading
#
import time
# noinspection PyUnresolvedReferences
from Katana import NodegraphAPI, Nodes3DAPI, FnGeolib, ScenegraphManager, Utils, Callbacks, Configuration
# noinspection PyUnresolvedReferences
from UI4 import App

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

import lxkatana.modifiers as ktn_modifiers

from lxutil import utl_core

import fnmatch

import sys


def _get_is_ui_mode_():
    return Configuration.get('KATANA_UI_MODE') == '1'


# katana scene graph operator
class KtnSGObjOpt(object):
    def __init__(self, scene_graph_opt, obj_path):
        self._scene_graph_opt = scene_graph_opt
        self._obj_path = obj_path
        self._traversal = scene_graph_opt._get_traversal_(obj_path)

    def get_port(self, port_path, use_global=False):
        tvl = self._traversal
        if tvl.valid():
            # print dir(tvl.getLocationData())
            if use_global is True:
                attrs = tvl.getLocationData().getAttrs()
            else:
                attrs = tvl.getLocationData().getAttrs()
            if attrs:
                return attrs.getChildByName(port_path)

    def get_port_raw(self, port_path, use_global=False):
        port = self.get_port(port_path, use_global)
        if port is not None:
            return port.getValue()

    def get(self, key, use_global=False):
        return self.get_port_raw(key, use_global)


class KtnSGStageOpt(object):
    OBJ_PATHSEP = '/'
    PORT_PATHSEP = '.'
    #
    GEOMETRY_ROOT = '/root/world/geo'
    OBJ_OPT_CLS = KtnSGObjOpt
    def __init__(self, ktn_obj=None):
        if ktn_obj is not None:
            if isinstance(ktn_obj, six.string_types):
                self._ktn_obj = NodegraphAPI.GetNode(ktn_obj)
            else:
                self._ktn_obj = ktn_obj
        else:
            self._ktn_obj = NodegraphAPI.GetViewNode()
        #
        self._runtime = FnGeolib.GetRegisteredRuntimeInstance()
        self._transaction = self._runtime.createTransaction()
        self._client = self._transaction.createClient()
        #
        self._transaction.setClientOp(self._client, Nodes3DAPI.GetOp(self._transaction, self._ktn_obj))
        self._runtime.commit(self._transaction)

    def _get_traversal_(self, location):
        return FnGeolib.Util.Traversal(
            self._client, location
        )

    def _test_(self, location):
        tvl = self._get_traversal_(location)
        # print dir(tvl)

    def get_obj_exists(self, obj_path):
        t = self._get_traversal_(obj_path)
        return t.valid()

    def get_obj(self, obj_path):
        return self._get_traversal_(obj_path)

    def get_obj_opt(self, obj_path):
        return self.OBJ_OPT_CLS(self, obj_path)

    def get_descendant_paths_at(self, location):
        list_ = []
        tvl = self._get_traversal_(location)
        while tvl.valid():
            i_obj_path = tvl.getLocationPath()
            if not i_obj_path == location:
                list_.append(i_obj_path)
            tvl.next()
        return list_

    def get_port(self, atr_path):
        _ = atr_path.split(self.PORT_PATHSEP)
        obj_path = _[0]
        port_path = self.PORT_PATHSEP.join(_[1:])
        tvl = self._get_traversal_(obj_path)
        if tvl.valid():
            atrs = tvl.getLocationData().getAttrs()
            return tvl.getLocationData().getAttrs().getChildByName(port_path)

    def get_port_raw(self, atr_path):
        p = self.get_port(atr_path)
        if p is not None:
            c = p.getTupleSize()
            if c == 1:
                return p.getValue()
            else:
                return p.getData()

    def get(self, key):
        return self.get_port_raw(key)

    def get_all_paths_at(self, location, include_types=None, exclude_types=None):
        list_ = []
        tvl = self._get_traversal_(
            location
        )
        # timeout for kill block
        timeout = 60
        start_time = int(time.time())
        while True:
            if (int(time.time())-start_time) > timeout:
                raise RuntimeError(
                    utl_core.Log.set_module_error_trace(
                        'location traversal is timeout'
                    )
                )
            #
            if tvl.valid() is False:
                break
            #
            i_path = tvl.getLocationPath()
            i_attrs = tvl.getLocationData().getAttrs()
            # call next in here
            tvl.next()
            # include filter
            if isinstance(include_types, (tuple, list)):
                i_type_name = i_attrs.getChildByName('type').getValue()
                if i_type_name not in include_types:
                    continue
            # exclude filter
            if isinstance(exclude_types, (tuple, list)):
                i_attrs = tvl.getLocationData().getAttrs()
                i_type_name = i_attrs.getChildByName('type').getValue()
                if i_type_name in exclude_types:
                    continue
            #
            list_.append(i_path)
        return list_

    def get_all_port_raws_at(self, location, port_path, include_types=None, exclude_types=None):
        list_ = []
        tvl = self._get_traversal_(
            location
        )
        # timeout for kill block
        timeout = 60
        start_time = int(time.time())
        while True:
            if (int(time.time())-start_time) > timeout:
                raise RuntimeError(
                    utl_core.Log.set_module_error_trace(
                        'location traversal is timeout'
                    )
                )
            #
            if tvl.valid() is False:
                break
            #
            i_attrs = tvl.getLocationData().getAttrs()
            # call next in here
            tvl.next()
            # include filter
            if isinstance(include_types, (tuple, list)):
                i_type_name = i_attrs.getChildByName('type').getValue()
                if i_type_name not in include_types:
                    continue
            # exclude filter
            if isinstance(exclude_types, (tuple, list)):
                i_attrs = tvl.getLocationData().getAttrs()
                i_type_name = i_attrs.getChildByName('type').getValue()
                if i_type_name in exclude_types:
                    continue
            #
            i_attr = i_attrs.getChildByName(port_path)
            if i_attr is not None:
                i_ = i_attr.getValue()
                list_.append(i_)
        #
        list__ = list(set(list_))
        list__.sort(key=list_.index)
        return list__

    def get_all_paths_at_as_dynamic(self, frame_range, location, include_types=None, exclude_types=None):
        start_frame, end_frame = frame_range
        if start_frame == end_frame:
            NGObjOpt(
                NodegraphAPI.GetRootNode()
            ).set('currentTime', start_frame)
            return self.get_all_paths_at(
                location, include_types, exclude_types
            )
        else:
            list_ = []
            for i_frame in range(start_frame, end_frame+1):
                NGObjOpt(
                    NodegraphAPI.GetRootNode()
                ).set('currentTime', i_frame)
                #
                i_paths = self.get_all_paths_at(
                    location, include_types, exclude_types
                )
                list_.extend(i_paths)
            #
            list__ = list(set(list_))
            list__.sort(key=list_.index)
            return list__

    def __str__(self):
        return '{}(node="{}")'.format(
            self.__class__.__name__,
            self._ktn_obj.getName()
        )


class KtnSGSelectionOpt(object):
    def __init__(self, *args):
        self._paths = args[0]
        self._scene_graph = ScenegraphManager.getActiveScenegraph()

    def set_all_select(self):
        paths = self._paths
        list_ = []
        for path in paths:
            ps = bsc_core.DccPathDagOpt(path).get_ancestor_paths()
            for p in ps:
                if p not in list_:
                    if p != '/':
                        list_.append(p)
        #
        self._scene_graph.addOpenLocations(list_, replace=True)
        self._scene_graph.addSelectedLocations(paths, replace=True)
    @classmethod
    def set_clear(cls):
        ScenegraphManager.getActiveScenegraph().clearOpenLocations()
        ScenegraphManager.getActiveScenegraph().addSelectedLocations([], replace=True)


class GuiNodeGraphBase(object):
    @classmethod
    def get_node_position(cls, ktn_obj):
        if isinstance(ktn_obj, six.string_types):
            return NodegraphAPI.GetNodePosition(
                NodegraphAPI.GetNode(ktn_obj)
            )
        return NodegraphAPI.GetNodePosition(ktn_obj)
    @classmethod
    def set_node_position(cls, ktn_obj, position):
        if isinstance(ktn_obj, six.string_types):
            return NodegraphAPI.SetNodePosition(
                NodegraphAPI.GetNode(ktn_obj), position
            )
        return NodegraphAPI.SetNodePosition(ktn_obj, position)


class GuiNodeGraphOpt(GuiNodeGraphBase):
    def __init__(self, ktn_gui=None):
        if ktn_gui is None:
            self._ktn_gui = App.Tabs.FindTopTab('Node Graph').getNodeGraphWidget()
        else:
            self._ktn_gui = ktn_gui

    def get_track_position(self):
        x, y, z = self._ktn_gui.getEyePoint()
        return x, y

    def move_node_to_view_center(self, ktn_obj):
        x, y = self.get_track_position()
        self.set_node_position(ktn_obj, (x, y))


class GuiNodeGraphTabOpt(GuiNodeGraphBase):
    def __init__(self, ktn_gui=None):
        if ktn_gui is None:
            self._ktn_gui = App.Tabs.FindTopTab('Node Graph')
        else:
            self._ktn_gui = ktn_gui

    def set_current_node(self, ktn_obj):
        self._ktn_gui.setCurrentNodeView(
            ktn_obj
        )

    def set_selection_view_fit(self):
        self._ktn_gui.frameSelection()

    def get_current_group(self):
        return self._ktn_gui.getEnteredGroupNode()

    def get_node_graph(self):
        return self._ktn_gui.getNodeGraphWidget()

    def get_node_graph_opt(self):
        return GuiNodeGraphOpt(self.get_node_graph())


class NGObjsOpt(object):
    def __init__(self, type_name=None):
        self._type_name = type_name

    def get_obj_names(self, pattern=None):
        if self._type_name is not None:
            _ = NodegraphAPI.GetAllNodesByType(self._type_name) or []
        else:
            _ = NodegraphAPI.getAllNodes() or []
        #
        obj_names = [i.getName() for i in _]
        if pattern is not None:
            return fnmatch.filter(
                obj_names, pattern
            )
        return obj_names


class NGLayout(object):
    class Direction(object):
        RightToLeft = 'r-l'
        LeftToRight = 'l-r'
        TopToBottom = 't-b'
        BottomToTop = 'b-t'
    def __init__(self, data, layout=(Direction.RightToLeft, Direction.TopToBottom), position=(0, 0), size=(320, 80), option=None):
        self._data = data
        self._layout = layout
        self._position = position
        self._size = size
        self._option = option

    def layout_fnc(self, obj, position):
        #
        x, y = position
        i_atr = dict(
            x=x, y=y,
        )
        i_atr_ = obj.getAttributes()
        i_atr_.update(i_atr)
        obj.setAttributes(i_atr_)
        if isinstance(self._option, dict):
            expanded = self._option.get('expanded')
            collapsed = self._option.get('collapsed')
            shader_view_state = self._option.get('shader_view_state')
            obj_opt = NGObjOpt(obj)
            if expanded is True:
                obj_opt.set_shader_gui_expanded()
            #
            elif collapsed is True:
                obj_opt.set_shader_gui_collapsed()
            #
            if isinstance(shader_view_state, (int, float)):
                obj_opt.set_shader_view_state(float(shader_view_state))
    @classmethod
    def _get_h_(cls, x, w, column, layout):
        if layout == 'r-l':
            return x - column * w * 2
        elif layout == 'l-r':
            return x + column * w * 2
        else:
            raise ValueError()

    def get_v(self, row, row_count, layout):
        pass

    def run(self):
        if self._data:
            layout_h, layout_v = self._layout
            x, y = self._position
            w, h = self._size
            for i_column, v in self._data.items():
                if v:
                    row_count = len(v)
                    if layout_h == 'r-l':
                        s_x = x - i_column * w * 2
                    elif layout_h == 'l-r':
                        s_x = x + i_column * w * 2
                    else:
                        raise ValueError()
                    #
                    if layout_v == 't-b':
                        s_y = y + ((row_count-(row_count % 2))*h) / 2
                    elif layout_v == 'b-t':
                        s_y = y - ((row_count-(row_count % 2))*h) / 2
                    else:
                        raise ValueError()
                    #
                    for j_row, i_obj in enumerate(v):
                        i_x = s_x
                        if layout_v == 't-b':
                            i_y = s_y - j_row*h
                        elif layout_v == 'b-t':
                            i_y = s_y + j_row*h
                        else:
                            raise ValueError()
                        #
                        self.layout_fnc(i_obj, (i_x, i_y))


class NGObjOpt(object):
    PATHSEP = '/'
    PORT_PATHSEP = '.'
    #
    @classmethod
    def _get_path_(cls, name):
        def _rcs_fnc(name_):
            _ktn_obj = NodegraphAPI.GetNode(name_)
            if _ktn_obj is not None:
                _parent = _ktn_obj.getParent()
                if _parent is None:
                    list_.append('')
                else:
                    _parent_name = _parent.getName()
                    list_.append(_parent_name)
                    _rcs_fnc(_parent_name)
        #
        list_ = [name]
        _rcs_fnc(name)
        list_.reverse()
        return cls.PATHSEP.join(list_)
    @classmethod
    def _set_create_(cls, path, type_name):
        path_opt = bsc_core.DccPathDagOpt(path)
        name = path_opt.name
        parent_opt = path_opt.get_parent()
        parent_name = parent_opt.get_name()
        ktn_obj = NodegraphAPI.GetNode(name)
        if ktn_obj is None:
            parent = cls(parent_name)
            parent_ktn_obj = parent.ktn_obj
            if parent_ktn_obj is not None:
                ktn_obj = NodegraphAPI.CreateNode(type_name, parent_ktn_obj)
                if ktn_obj is None:
                    raise RuntimeError('type="{}" is unknown'.format(type_name))
                #
                name_ktn_port = ktn_obj.getParameter('name')
                if name_ktn_port is not None:
                    name_ktn_port.setValue(str(name), 0)
                #
                ktn_obj.setName(name)
                return ktn_obj
            else:
                raise RuntimeError('obj="{}" is non-exists'.format(parent_name))
        return ktn_obj
    @classmethod
    def _get_is_parent_for_(cls, parent_ktn_obj, child_ktn_obj):
        return child_ktn_obj.getParent().getName() == parent_ktn_obj.getName()
    @classmethod
    def _get_create_args_(cls, path, type_name):
        path_opt = bsc_core.DccPathDagOpt(path)
        name = path_opt.name
        parent_opt = path_opt.get_parent()
        parent_name = parent_opt.get_name()
        ktn_obj = NodegraphAPI.GetNode(name)
        if ktn_obj is None:
            parent = cls(parent_name)
            parent_ktn_obj = parent.ktn_obj
            if parent_ktn_obj is not None:
                ktn_obj = NodegraphAPI.CreateNode(type_name, parent_ktn_obj)
                if ktn_obj is None:
                    raise RuntimeError('type="{}" is unknown'.format(type_name))
                #
                name_ktn_port = ktn_obj.getParameter('name')
                if name_ktn_port is not None:
                    name_ktn_port.setValue(str(name), 0)
                #
                ktn_obj.setName(name)
                return ktn_obj, True
            else:
                raise RuntimeError('obj="{}" is non-exists'.format(parent_name))
        return ktn_obj, False
    @classmethod
    def _get_shader_create_args_(cls, path, type_name, shader_type_name):
        ktn_obj, is_create = cls._get_create_args_(path, type_name)
        if is_create is True:
            type_ktn_port = ktn_obj.getParameter('nodeType')
            if type_ktn_port is not None:
                type_ktn_port.setValue(str(shader_type_name), 0)
                ktn_obj.checkDynamicParameters()
        return ktn_obj, is_create
    @classmethod
    def _get_usd_shader_create_args_(cls, path, shader_type_name):
        ktn_obj, is_create = cls._get_create_args_(path, 'UsdShadingNode')
        if is_create is True:
            type_ktn_port = ktn_obj.getParameter('nodeType')
            if type_ktn_port is not None:
                type_ktn_port.setValue(str(shader_type_name), 0)
                ktn_obj.checkDynamicParameters()
        return ktn_obj, is_create
    @classmethod
    def _create_connections_by_data_(cls, connections_data, extend_kwargs=None):
        """
        :param connections_data: etc. [
            'node_a.a.b',
            'node_b.a.b'
        ]
        :return:
        """
        for seq, i in enumerate(connections_data):
            if not (seq + 1) % 2:
                i_source_attr_path = connections_data[seq - 1]
                i_target_attr_path = i
                if isinstance(extend_kwargs, dict):
                    i_source_attr_path = i_source_attr_path.format(**extend_kwargs)
                    i_target_attr_path = i_target_attr_path.format(**extend_kwargs)
                #
                i_args_src = i_source_attr_path.split('.')
                i_obj_path_src, i_port_path_src = i_args_src[0], '.'.join(i_args_src[1:])
                i_args_tgt = i_target_attr_path.split('.')
                i_obj_path_tgt, i_port_path_tgt = i_args_tgt[0], '.'.join(i_args_tgt[1:])
                #
                i_obj_src = cls._get_ktn_obj_(i_obj_path_src)
                if i_obj_src is None:
                    raise RuntimeError(
                        'node="{}" is non-exists'.format(i_obj_path_src)
                    )
                #
                i_obj_tgt = cls._get_ktn_obj_(i_obj_path_tgt)
                if i_obj_tgt is None:
                    raise RuntimeError(
                        'node="{}" is non-exists'.format(i_obj_path_tgt)
                    )
                #
                if i_obj_src.getName() == i_obj_tgt.getName():
                    source_mtd, target_mtd = 'getSendPort', 'getReturnPort'
                else:
                    i_condition = (
                        cls._get_is_parent_for_(i_obj_src, i_obj_tgt),
                        cls._get_is_parent_for_(i_obj_tgt, i_obj_src)
                    )
                    if i_condition == (False, False):
                        #
                        source_mtd, target_mtd = 'getOutputPort', 'getInputPort'
                    elif i_condition == (True, False):
                        #
                        source_mtd, target_mtd = 'getSendPort', 'getInputPort'
                    elif i_condition == (False, True):
                        #
                        source_mtd, target_mtd = 'getOutputPort', 'getReturnPort'
                    else:
                        raise RuntimeError()
                #
                i_port_src = i_obj_src.__getattribute__(source_mtd)(i_port_path_src)
                if i_port_src is None:
                    raise RuntimeError(
                        'method="{}", attribute="{}" is non-exists'.format(source_mtd, i_source_attr_path)
                    )
                #
                i_port_tgt = i_obj_tgt.__getattribute__(target_mtd)(i_port_path_tgt)
                if i_port_tgt is None:
                    raise RuntimeError(
                        'method="{}", attribute="{}" is non-exists'.format(target_mtd, i_target_attr_path)
                    )
                #
                i_port_src.connect(
                    i_port_tgt
                )
    @classmethod
    def _get_is_exists_(cls, string_arg):
        return cls._get_ktn_obj_(string_arg) is not None
    @classmethod
    def _get_ktn_obj_(cls, string_arg):
        if string_arg.startswith(cls.PATHSEP):
            return NodegraphAPI.GetNode(
                bsc_core.DccPathDagOpt(string_arg).get_name()
            )
        else:
            return NodegraphAPI.GetNode(string_arg)

    def __init__(self, ktn_obj):
        if isinstance(ktn_obj, six.string_types):
            if ktn_obj.startswith(self.PATHSEP):
                self._ktn_obj = NodegraphAPI.GetNode(
                    bsc_core.DccPathDagOpt(ktn_obj).get_name()
                )
            else:
                self._ktn_obj = NodegraphAPI.GetNode(ktn_obj)
        else:
            self._ktn_obj = ktn_obj

    def get_ktn_obj(self):
        return self._ktn_obj
    ktn_obj = property(get_ktn_obj)

    def get_type(self):
        return self.ktn_obj.getType()
    type = property(get_type)

    def get_type_name(self):
        return self.get_type()
    type_name = property(get_type_name)

    def get_shader_type_name(self):
        return self.get('nodeType')
    shader_type_name = property(get_shader_type_name)

    def get_path(self):
        return self._get_path_(self.get_name())
    path = property(get_path)

    def get_name(self):
        return self.ktn_obj.getName()
    name = property(get_name)

    def set_rename(self, new_name):
        if isinstance(new_name, unicode):
            new_name = str(new_name)
        #
        name_ktn_port = self._ktn_obj.getParameter('name')
        if name_ktn_port is not None:
            name_ktn_port.setValue(new_name, 0)
        self._ktn_obj.setName(new_name)

    def get_stage_opt(self):
        return KtnSGStageOpt(
            self._ktn_obj
        )

    def set_shader_gui_expanded(self):
        attributes = self.ktn_obj.getAttributes()
        if 'ns_expandedPages' in attributes and 'ns_collapsedPages' in attributes:
            attributes['ns_expandedPages'] = 'Outputs##BUILTIN | Parameters##BUILTIN | '
            attributes['ns_collapsedPages'] = 'Outputs | Parameters | '
            self.ktn_obj.setAttributes(attributes)

    def set_shader_gui_collapsed(self):
        attributes = self.ktn_obj.getAttributes()
        if 'ns_expandedPages' in attributes:
            attributes['ns_expandedPages'] = 'Outputs | Parameters | '
            attributes['ns_collapsedPages'] = 'Outputs##BUILTIN | Parameters##BUILTIN | '
            self.ktn_obj.setAttributes(attributes)

    def set_shader_view_state(self, value):
        self.set_attributes(dict(ns_viewState=value))

    def get_sources(self, **kwargs):
        list_ = []
        _ = self.ktn_obj.getInputPorts() or []
        for i_ktn_port in _:
            i_ktn_ports_src = i_ktn_port.getConnectedPorts()
            if i_ktn_ports_src:
                list_.extend(i_ktn_ports_src)
        return list_

    def get_source_objs(self, **kwargs):
        list_ = []
        if 'inward' in kwargs:
            _ = self._get_sources_inward_(self._ktn_obj)
        else:
            _ = self.get_sources(**kwargs)
        for i_ktn_port in _:
            i_ktn_obj = i_ktn_port.getNode()
            if i_ktn_obj not in list_:
                list_.append(i_ktn_obj)
        return list_
    @classmethod
    def _get_sources_inward_(cls, ktn_obj):
        list_ = []
        _ = ktn_obj.getOutputPorts() or []
        for i_ktn_port in _:
            i_ktn_ports_rtn = ktn_obj.getReturnPort(i_ktn_port.getName())
            i_ktn_ports_src = i_ktn_ports_rtn.getConnectedPorts()
            if i_ktn_ports_src:
                list_.extend(i_ktn_ports_src)
        return list_
    @classmethod
    def _get_source_objs_inward_(cls, ktn_obj):
        list_ = []
        _ = cls._get_sources_inward_(ktn_obj)
        for i_ktn_port in _:
            i_ktn_obj = i_ktn_port.getNode()
            if i_ktn_obj not in list_:
                list_.append(i_ktn_obj)
        return list_

    def get_all_source_objs(self, **kwargs):
        def rcs_fnc_(list__, ktn_obj):
            _ktn_objs = self.__class__(ktn_obj).get_source_objs(**kwargs)
            for _i_ktn_obj in _ktn_objs:
                if _i_ktn_obj not in list__:
                    if hasattr(_i_ktn_obj, 'getChildren'):
                        _i_ktn_objs = self._get_source_objs_inward_(_i_ktn_obj)
                        for _j_ktn_obj in _i_ktn_objs:
                            if _j_ktn_obj not in list__:
                                list__.append(_j_ktn_obj)
                                rcs_fnc_(list__, _j_ktn_obj)
                    else:
                        list__.append(_i_ktn_obj)
                        rcs_fnc_(list__, _i_ktn_obj)
        #
        inward = kwargs.get('inward', False)
        #
        list_ = []
        rcs_fnc_(list_, self._ktn_obj)
        return list_

    def set_gui_layout(self, layout=(NGLayout.Direction.RightToLeft, NGLayout.Direction.TopToBottom), size=(320, 80), expanded=False, collapsed=False, shader_view_state=None):
        def rcs_fnc_(ktn_obj_, column_):
            if hasattr(ktn_obj_, 'getChildren'):
                _source_ktn_objs = self._get_source_objs_inward_(ktn_obj_)
            else:
                _source_ktn_objs = self.__class__(ktn_obj_).get_source_objs()
            #
            if _source_ktn_objs:
                column_ += 1
                if column_ not in ktn_obj_in_column_dict:
                    _i_ktn_objs = []
                    ktn_obj_in_column_dict[column_] = _i_ktn_objs
                else:
                    _i_ktn_objs = ktn_obj_in_column_dict[column_]
                #
                for _row, _i_ktn_obj in enumerate(_source_ktn_objs):
                    if not _i_ktn_obj in ktn_obj_stack:
                        ktn_obj_stack.append(_i_ktn_obj)
                        _i_ktn_objs.append(_i_ktn_obj)
                        rcs_fnc_(_i_ktn_obj, column_)
                    else:
                        pass
        #
        ktn_obj_stack = [
            self._ktn_obj
        ]
        ktn_obj_in_column_dict = {}
        #
        rcs_fnc_(self._ktn_obj, 0)
        #
        NGLayout(
            ktn_obj_in_column_dict,
            layout=layout,
            position=NodegraphAPI.GetNodePosition(self.ktn_obj),
            size=size,
            option=dict(
                expanded=expanded,
                collapsed=collapsed,
                shader_view_state=shader_view_state
            )
        ).run()

    def get_port_raw(self, port_path):
        port = self.ktn_obj.getParameter(port_path)
        if port:
            return NGPortOpt(port).get()

    def set_port_raw(self, port_path, raw):
        port = self.ktn_obj.getParameter(port_path)
        if port:
            NGPortOpt(port).set(raw)

    def set(self, key, value):
        self.set_port_raw(key, value)

    def get(self, key):
        return self.get_port_raw(key)

    def set_parameters_by_data(self, data):
        pass

    def set_shader_parameters_by_data(self, data, extend_kwargs=None):
        """
        :param data: {
            <port_path>: <value>
        }
        :param extend_kwargs:
        :return:
        """
        for i_port_path, i_value in data.items():
            #
            i_port_path = i_port_path.replace('/', '.')
            if isinstance(extend_kwargs, dict):
                if isinstance(i_value, (unicode, str)):
                    i_value = i_value.format(**extend_kwargs)
            # turn on enable first
            i_enable_key = 'parameters.{}.enable'.format(i_port_path)
            self.set(i_enable_key, True)
            #
            i_value_key = 'parameters.{}.value'.format(i_port_path)
            # turn off the expression-flag
            if self.get_is_expression(i_value_key) is True:
                self.set_expression_enable(i_value_key, False)
            self.set(i_value_key, i_value)

    def set_shader_hints(self, data):
        pass

    def set_shader_expressions_by_data(self, data, extend_kwargs=None):
        for i_port_path, i_value in data.items():
            #
            i_port_path = i_port_path.replace('/', '.')
            if isinstance(extend_kwargs, dict):
                if isinstance(i_value, (unicode, str)):
                    i_value = i_value.format(**extend_kwargs)
            # turn on enable first
            i_enable_key = 'parameters.{}.enable'.format(i_port_path)
            self.set(i_enable_key, True)
            #
            i_value_key = 'parameters.{}.value'.format(i_port_path)
            # turn on the expression-flag
            self.set_expression_enable(i_value_key, True)
            self.set_expression(i_value_key, i_value)

    def set_shader_hints_by_data(self, data, extend_kwargs=None):
        for i_port_path, i_value in data.items():
            #
            i_port_path = i_port_path.replace('/', '.')
            # if isinstance(extend_kwargs, dict):
            #     if isinstance(i_value, (unicode, str)):
            #         i_value = i_value.format(**extend_kwargs)
            #
            i_hints_key = 'parameters.{}.hints'.format(i_port_path)
            #
            self.set_port_create(i_hints_key, 'string', i_value)

    def set_expression_enable(self, key, boolean):
        p = self.ktn_obj.getParameter(key)
        if p:
            p.setExpressionFlag(boolean)

    def set_expression(self, key, value):
        p = self.ktn_obj.getParameter(key)
        if p:
            p.setExpression(value)

    def get_is_expression(self, key):
        p = self.ktn_obj.getParameter(key)
        if p:
            return p.isExpression()

    def get_as_enumerate(self, key):
        port = self.ktn_obj.getParameter(key)
        if port:
            return NGPortOpt(port).get_enumerate_strings()
        return []

    def set_port_enumerate_raw(self, port_path, raw):
        port = self.ktn_obj.getParameter(port_path)
        if port:
            NGPortOpt(port).set_enumerate_strings(raw)

    def set_as_enumerate(self, key, value):
        self.set_port_enumerate_raw(key, value)

    def get_port(self, port_path):
        return self.ktn_obj.getParameter(port_path)

    def get_input_port(self, port_path):
        return self._ktn_obj.getInputPort(port_path)

    def get_output_port(self, port_path):
        return self._ktn_obj.getOutputPort(port_path)

    def get_output_ports(self):
        return self._ktn_obj.getOutputPorts()
    # send and return
    def get_send_port(self, port_path):
        return self._ktn_obj.getSendPort(port_path)

    def get_return_port(self, port_path):
        return self._ktn_obj.getReturnPort(port_path)

    def get_targets(self, port_path):
        p = self.get_output_port(port_path)
        if p:
            return p.getConnectedPorts()

    def set_port_create(self, port_path, port_type, default_value):
        _ = self.get_port(port_path)
        port_parent = bsc_core.DccPortPathMtd.get_dag_parent(
            path=port_path, pathsep=self.PORT_PATHSEP
        )
        port_name = bsc_core.DccPortPathMtd.get_dag_name(
            path=port_path, pathsep=self.PORT_PATHSEP
        )
        if _ is None:
            if port_parent is not None:
                parent_ktn_port = self.ktn_obj.getParameter(port_parent)
            else:
                parent_ktn_port = self.ktn_obj.getParameters()
            #
            if parent_ktn_port is not None:
                if port_type == 'string':
                    parent_ktn_port.createChildString(port_name, str(default_value))
        else:
            self.set(port_path, default_value)

    def set_delete(self):
        self.ktn_obj.delete()

    def get_position(self):
        return NodegraphAPI.GetNodePosition(self.ktn_obj)

    def set_position(self, x, y):
        atr = self._ktn_obj.getAttributes()
        atr.update(
            dict(
                x=x,
                y=y
            )
        )
        self._ktn_obj.setAttributes(atr)

    def set_color(self, rgb):
        r, g, b = rgb
        atr = self._ktn_obj.getAttributes()
        atr.update(
            dict(
                ns_colorr=r,
                ns_colorg=g,
                ns_colorb=b
            )
        )
        self._ktn_obj.setAttributes(atr)

    def move_to_view_center(self):
        GuiNodeGraphOpt().move_node_to_view_center(
            self._ktn_obj
        )

    def set_ports_clear(self, port_path=None):
        if port_path is None:
            ktn_root_port = self._ktn_obj.getParameters()
            for i in ktn_root_port.getChildren():
                ktn_root_port.deleteChild(i)
        else:
            ktn_root_port = self._ktn_obj.getParameter(port_path)
        #
        if ktn_root_port is not None:
            for i in ktn_root_port.getChildren():
                ktn_root_port.deleteChild(i)

    def get_children(self, include_type_names=None):
        _ = self._ktn_obj.getChildren()
        if include_type_names is not None:
            if isinstance(include_type_names, (tuple, list)):
                return [i for i in _ if self.__class__(i).get_type() in include_type_names]
        return _

    def set_port_execute(self, port_path):
        ktn_port = self._ktn_obj.getParameter(port_path)
        if ktn_port:
            hint_string = ktn_port.getHintString()
            if hint_string:
                hint_dict = eval(hint_string)
                if hint_dict['widget'] in ['scriptButton']:
                    script = hint_dict['scriptText']
                    # noinspection PyUnusedLocal
                    node = self._ktn_obj
                    exec script

    def set_input_port_create(self, port_path):
        _ = self._ktn_obj.getInputPort(port_path)
        if _ is None:
            self._ktn_obj.addInputPort(port_path)

    def create_input_ports_by_data(self, ports_data):
        for i in ports_data:
            self.set_input_port_create(i)

    def set_output_port_create(self, port_path):
        _ = self._ktn_obj.getOutputPort(port_path)
        if _ is None:
            self._ktn_obj.addOutputPort(port_path)

    def create_output_ports_by_data(self, ports_data):
        for i in ports_data:
            self.set_output_port_create(i)

    def get_parent(self):
        return self._ktn_obj.getParent()

    def get_parent_opt(self):
        parent = self.get_parent()
        if parent:
            return self.__class__(parent)

    def get_attributes(self):
        return self._ktn_obj.getAttributes()

    def set_attributes(self, attributes):
        attributes_ = self._ktn_obj.getAttributes()
        attributes_.update(attributes)
        self._ktn_obj.setAttributes(attributes_)

    def set_edited(self, boolean):
        NodegraphAPI.SetNodeEdited(
            self._ktn_obj,
            edited=boolean, exclusive=True
        )


class NGGroupStackOpt(NGObjOpt):
    def __init__(self, ktn_obj):
        super(NGGroupStackOpt, self).__init__(ktn_obj)

    def _get_last_(self):
        ktn_obj = self._ktn_obj
        _ = ktn_obj.getReturnPort('out').getConnectedPorts()
        if _:
            return _[0].getNode()
        return ktn_obj

    def set_child_create(self, name):
        src_ktn_obj = self._ktn_obj
        type_name = src_ktn_obj.getChildNodeType()
        tgt_ktn_obj = NodegraphAPI.GetNode(name)
        if tgt_ktn_obj is not None:
            return tgt_ktn_obj, False
        #
        tgt_ktn_obj = NodegraphAPI.CreateNode(type_name, src_ktn_obj)
        if tgt_ktn_obj is None:
            raise TypeError('unknown-obj-type: "{}"'.format(type_name))
        name_ktn_port = tgt_ktn_obj.getParameter('name')
        if name_ktn_port is not None:
            name_ktn_port.setValue(str(name), 0)
        tgt_ktn_obj.setName(name)
        #
        last_ktn_obj = self._get_last_()
        if last_ktn_obj.getName() == self.name:
            src_ktn_obj.getSendPort('in').connect(
                tgt_ktn_obj.getInputPorts()[0]
            )
        else:
            x, y = NodegraphAPI.GetNodePosition(last_ktn_obj)
            NodegraphAPI.SetNodePosition(tgt_ktn_obj, (x, y-48))
            #
            last_ktn_obj.getOutputPorts()[0].connect(
                tgt_ktn_obj.getInputPorts()[0]
            )
        #
        tgt_ktn_obj.getOutputPorts()[0].connect(src_ktn_obj.getReturnPort('out'))
        return tgt_ktn_obj, True


class NGMaterialGroupOpt(NGObjOpt):
    def __init__(self, ktn_obj):
        super(NGMaterialGroupOpt, self).__init__(ktn_obj)


class NGPortOpt(object):
    PATHSEP = '.'
    def __init__(self, ktn_port):
        self._ktn_port = ktn_port
        self._atr_path = self._get_atr_path_(self._ktn_port)
    @property
    def ktn_port(self):
        return self._ktn_port
    @property
    def ktn_obj(self):
        return self.ktn_port.getNode()
    @property
    def type(self):
        return self.ktn_port.getType()
    @property
    def path(self):
        return self._atr_path

    def get_name(self):
        return self._ktn_port.getName()
    name = property(get_name)
    @classmethod
    def _get_atr_path_(cls, ktn_port):
        def rcs_fnc_(ktn_port_):
            if ktn_port_ is not None:
                _port_name = ktn_port_.getName()
                list_.append(_port_name)
                _parent_ktn_port = ktn_port_.getParent()
                rcs_fnc_(_parent_ktn_port)
        #
        list_ = []
        #
        rcs_fnc_(ktn_port)
        #
        list_.reverse()
        return cls.PATHSEP.join(list_)
    #
    def get(self, frame=0):
        _children = self.ktn_port.getChildren() or []
        if _children:
            return [i.getValue(frame) for i in _children]
        else:
            return self.ktn_port.getValue(frame)

    def set(self, value, frame=0):
        if isinstance(value, (tuple, list)):
            size = len(value)
            self.ktn_port.resizeArray(size)
            [self.ktn_port.getChildByIndex(i).setValue(value[i], frame) for i in range(size)]
        else:
            _value = value
            if isinstance(value, unicode):
                _value = str(value)
            #
            if self.get_is_enumerate() is True:
                if isinstance(value, int):
                    strings = self.get_enumerate_strings()
                    index = max(min(value, len(strings)-1), 0)
                    _value = strings[index]
            #
            self.ktn_port.setValue(_value, frame)

    def set_help_string(self, value):
        hint_string = self.ktn_port.getHintString()
        if hint_string:
            hint_dict = eval(hint_string)
        else:
            hint_dict = {}
        #
        hint_dict['help'] = value
        #
        self.ktn_port.setHintString(
            str(hint_dict)
        )

    def get_is_enumerate(self):
        hint_string = self.ktn_port.getHintString()
        if hint_string:
            hint_dict = eval(hint_string)
            return hint_dict.get('widget') == 'popup'

    def set_enumerate_strings(self, value, frame=0):
        hint_string = self.ktn_port.getHintString()
        if hint_string:
            hint_dict = eval(hint_string)
        else:
            hint_dict = {}
        #
        hint_dict['options'] = list(value)
        #
        self.ktn_port.setHintString(
            str(hint_dict)
        )
        self.ktn_port.setValue(
            str(value[0]), frame
        )

    def get_enumerate_strings(self):
        hint_string = self.ktn_port.getHintString()
        if hint_string:
            hint_dict = eval(hint_string)
            return map(str, hint_dict.get('options', []))
        return []

    def set_connect_to(self, input_port):
        self._ktn_port.connect(
            input_port
        )

    def set_target(self, input_port):
        self._ktn_port.connect(
            input_port
        )

    def set_expression(self, raw):
        self._ktn_port.setExpression(raw)

    def get_expression(self):
        return self._ktn_port.getExpression()

    def get_is_expression(self):
        return self._ktn_port.isExpression()

    def get_children(self):
        return [self._ktn_port.getChildren()]

    def clear_children(self):
        [self._ktn_port.deleteChild(i) for i in self.get_children()]


class NGAndObjTypeOpt(object):
    def __init__(self, type_name):
        self._obj_type_name = type_name

    def get_ktn_objs(self):
        list_ = []
        for i_ktn_obj in NodegraphAPI.GetAllNodesByType('ArnoldShadingNode') or []:
            i_ktn_obj_opt = NGObjOpt(i_ktn_obj)
            i_shader_type_name = i_ktn_obj_opt.get_port_raw('nodeType')
            if i_shader_type_name in [self._obj_type_name]:
                list_.append(i_ktn_obj)
        return list_

    def get_obj_opts(self):
        list_ = []
        for i_ktn_obj in NodegraphAPI.GetAllNodesByType('ArnoldShadingNode') or []:
            i_ktn_obj_opt = NGObjOpt(i_ktn_obj)
            i_shader_type_name = i_ktn_obj_opt.get_port_raw('nodeType')
            if i_shader_type_name in [self._obj_type_name]:
                list_.append(i_ktn_obj_opt)
        return list_


class NodeGraphInputPort(object):
    pass


class NGObjTypeOpt(object):
    def __init__(self, obj_type_name):
        self._obj_type_name = obj_type_name

    def get_objs(self):
        return NodegraphAPI.GetAllNodesByType(self._obj_type_name)


class EventOpt(object):
    class EventType(object):
        NodeCreate = 'node_create'
    #
    def __init__(self, handler, event_type):
        self._handler = handler
        self._event_type = event_type

    def set_register(self):
        self.set_unregister()
        #
        Utils.EventModule.RegisterEventHandler(
            handler=self._handler,
            eventType=self._event_type,
            enabled=True
        )
        #
        utl_core.Log.set_module_result_trace(
            'register-event',
            'event-type="{}"'.format(self._event_type)
        )

    def set_unregister(self):
        if self.get_is_register() is True:
            Utils.EventModule.UnregisterEventHandler(
                handler=self._handler,
                eventType=self._event_type
            )
            utl_core.Log.set_module_result_trace(
                'unregister-event',
                'event-type="{}"'.format(self._event_type)
            )

    def get_is_register(self):
        return Utils.EventModule.IsHandlerRegistered(
            handler=self._handler,
            eventType=self._event_type
        )


class CallbackOpt(object):
    def __init__(self, function, callback_type):
        self._function = function
        self._callback_type = callback_type

    def set_add(self):
        Callbacks.addCallback(
            callbackType=self._callback_type,
            callbackFcn=self._function
        )
        #
        utl_core.Log.set_module_result_trace(
            'add-callback',
            'callback-type="{}"'.format(self._callback_type)
        )

    def set_delete(self):
        Callbacks.delCallback(
            callbackType=self._callback_type,
            callbackFcn=self._function
        )
        utl_core.Log.set_module_result_trace(
            'delete-callback',
            'callback-type="{}"'.format(self._callback_type)
        )


class EventMethod(object):
    @classmethod
    def get_all_event_types(cls):
        pass
    @classmethod
    def set_port_value(cls, *args, **kwargs):
        event_type, event_id = args
        ktn_obj = kwargs['node']
        ktn_port = kwargs['param']
        ktn_obj_opt = NGObjOpt(ktn_obj)
        if ktn_obj_opt.type == 'ArnoldShadingNode':
            shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
            if shader_type_name in ['ramp_rgb', 'ramp_float']:
                ktn_port_opt = NGPortOpt(ktn_port)
                if fnmatch.filter([ktn_port_opt.path], '*.parameters.ramp_Knots.value.*'):
                    cls.set_arnold_ramp_write(ktn_obj_opt)
                elif fnmatch.filter([ktn_port_opt.path], '*.parameters.ramp_Floats.value.*'):
                    cls.set_arnold_ramp_write(ktn_obj_opt)
                elif fnmatch.filter([ktn_port_opt.path], '*.parameters.ramp_Colors.value.*'):
                    cls.set_arnold_ramp_write(ktn_obj_opt)
    @classmethod
    def set_port_connect(cls, *args, **kwargs):
        event_type, event_id = args
        source = kwargs['portA']
        target = kwargs['portB']
        ktn_obj = target.getNode()
        ktn_obj_opt = NGObjOpt(ktn_obj)
        if ktn_obj_opt:
            if ktn_obj_opt.type == 'ArnoldShadingNode':
                shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
                if shader_type_name in ['ramp_rgb', 'ramp_float']:
                    cls.set_arnold_ramp_read(ktn_obj_opt)
    @classmethod
    def set_port_disconnect(cls, *args, **kwargs):
        event_type, event_id = args
        source = kwargs['portA']
        target = kwargs['portB']
        ktn_obj = target.getNode()
        ktn_obj_opt = NGObjOpt(ktn_obj)
        if ktn_obj_opt:
            if ktn_obj_opt.type == 'ArnoldShadingNode':
                shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
                if shader_type_name in ['ramp_rgb', 'ramp_float']:
                    cls.set_arnold_ramp_read(ktn_obj_opt)
    @classmethod
    def set_node_create(cls, *args, **kwargs):
        event_type, event_id = args
        ktn_obj = kwargs['node']
        ktn_obj_opt = NGObjOpt(ktn_obj)
        if ktn_obj_opt.type == 'ArnoldShadingNode':
            shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
            if shader_type_name in ['ramp_rgb', 'ramp_float']:
                cls.set_arnold_ramp_read(ktn_obj_opt)
            #
            cls._set_arnold_obj_name_update_(ktn_obj_opt)
    @classmethod
    def set_node_edit(cls, *args, **kwargs):
        event_type, event_id = args
        ktn_obj = kwargs['node']
        ktn_obj_opt = NGObjOpt(ktn_obj)
        if ktn_obj_opt.type == 'ArnoldShadingNode':
            shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
            if shader_type_name in ['ramp_rgb', 'ramp_float']:
                cls.set_arnold_ramp_read(ktn_obj_opt)
    @classmethod
    def set_arnold_ramp_write(cls, ktn_obj_opt):
        cls._set_arnold_ramp_write_(ktn_obj_opt)
        # utl_core.Log.set_module_result_trace(
        #     'ramp-write',
        #     'obj-name="{}"'.format(ktn_obj_opt.name)
        # )
    @classmethod
    def _set_arnold_ramp_write_(cls, ktn_obj_opt):
        # noinspection PyUnresolvedReferences
        key = sys._getframe().f_code.co_name
        # Utils.UndoStack.OpenGroup(key)
        #
        ramp_value_dict = {}
        shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
        if shader_type_name == 'ramp_rgb':
            keys = ['ramp', 'ramp_Knots', 'ramp_Interpolation', 'ramp_Colors']
        elif shader_type_name == 'ramp_float':
            keys = ['ramp', 'ramp_Knots', 'ramp_Interpolation', 'ramp_Floats']
        else:
            raise
        for i_key in keys:
            value_port_path = 'parameters.{}.value'.format(i_key)
            value = ktn_obj_opt.get_port_raw(value_port_path)
            #
            ramp_value_dict[i_key] = value
            i_port_path = 'lx_ramp_value'
            i_ktn_port = ktn_obj_opt.get_port(i_port_path)
            if i_ktn_port is None:
                ktn_obj_opt.set_port_create(i_port_path, 'string', str(ramp_value_dict))
            else:
                i_ktn_port_opt = NGPortOpt(i_ktn_port)
                i_ktn_port_opt.set(str(ramp_value_dict))
        #
        # Utils.UndoStack.CloseGroup()
    @classmethod
    def set_arnold_ramp_read(cls, ktn_obj_opt):
        def fnc_():
            cls._set_arnold_ramp_read_(ktn_obj_opt)
            # utl_core.Log.set_module_result_trace(
            #     'ramp-read',
            #     'obj-name="{}"'.format(ktn_obj_opt.name)
            # )
        #
        import threading
        timer = threading.Timer(1, fnc_)
        timer.start()
    @classmethod
    def _set_arnold_ramp_read_(cls, ktn_obj_opt):
        # noinspection PyUnresolvedReferences
        key = sys._getframe().f_code.co_name
        # Utils.UndoStack.OpenGroup(key)
        #
        ramp_value_port = ktn_obj_opt.get_port('lx_ramp_value')
        if ramp_value_port is not None:
            ramp_value_port_opt = NGPortOpt(ramp_value_port)
            ramp_value_dict = eval(ramp_value_port_opt.get() or '{}')
            for key, value in ramp_value_dict.items():
                enable_port_path = 'parameters.{}.enable'.format(key)
                value_port_path = 'parameters.{}.value'.format(key)
                ktn_obj_opt.set_port_raw(enable_port_path, 1)
                ktn_obj_opt.set_port_raw(value_port_path, value)
        #
        # Utils.UndoStack.CloseGroup()
    @classmethod
    def _set_arnold_obj_name_update_(cls, ktn_obj_opt):
        # noinspection PyUnresolvedReferences
        key = sys._getframe().f_code.co_name
        # Utils.UndoStack.OpenGroup(key)
        #
        shader_obj_name = ktn_obj_opt.get_port_raw('name')
        obj_name = ktn_obj_opt.name
        ktn_obj = ktn_obj_opt.ktn_obj
        if ktn_obj.isRenameAllowed() is True:
            if ktn_obj.isAutoRenameAllowed() is False:
                ktn_obj_opt.set_port_raw('name', obj_name)
                ktn_obj.setAutoRenameAllowed(True)
        #
        # Utils.UndoStack.CloseGroup()
    @classmethod
    def set_events_register(cls):
        ss = [
            (cls.set_port_value, 'parameter_setValue'),
            (cls.set_port_connect, 'port_connect'),
            (cls.set_port_disconnect, 'port_disconnect'),
            (cls.set_node_create, 'node_create'),
            (cls.set_node_edit, 'node_setEdited')
        ]
        #
        for handler, event_type in ss:
            event_opt = EventOpt(handler=handler, event_type=event_type)
            event_opt.set_register()


class ArnoldEventMtd(object):
    N = 'texture_directory'
    DIRECTORY_KEY = 'extra.texture_directory'
    DIRECTORY_VALUE = '/texture_directory'
    @classmethod
    def set_material_create(cls, *args, **kwargs):
        if kwargs['nodeType'] == 'NetworkMaterialCreate':
            node_opt = NGObjOpt(kwargs['node'])
            cls._set_material_create_(node_opt)
    @classmethod
    def _set_material_create_(cls, node_opt):
        """
        # coding:utf-8
        import lxkatana

        lxkatana.set_reload()

        from lxkatana import ktn_core

        ktn_core.ArnoldEventMtd._set_material_create_(
            ktn_core.NGObjOpt(
                NodegraphAPI.GetNode('NetworkMaterialCreate')
            )
        )
        :param node_opt:
        :return:
        """
        def connect_fnc_():
            _key = cls.DIRECTORY_KEY
            # ignore when expression is enable
            if node_opt.get_is_expression(_key) is True:
                return False
            # ignore when value is changed
            if node_opt.get(_key) != cls.DIRECTORY_VALUE:
                return False
            # ignore parent is non-exists
            _parent_opt = node_opt.get_parent_opt()
            if not _parent_opt:
                return False
            # ignore parent has not directory
            if not _parent_opt.get_port('user.Texture_Folder'):
                return False
            #
            node_opt.set_expression(_key, 'getParent().user.Texture_Folder')
            return True

        p_ns = [
            (cls.DIRECTORY_KEY, dict(widget='file', value=cls.DIRECTORY_VALUE)),
        ]
        for i_p_n, i_p_r in p_ns:
            if node_opt.get_port(i_p_n) is None:
                NGMacro(node_opt.ktn_obj).set_parameter_create(
                    i_p_n, i_p_r
                )

        connect_fnc_()
    @classmethod
    def _get_material_show_node_(cls, node_opt):
        return [i for i in node_opt.get_children(['Merge'])][0]
    #
    @classmethod
    def set_image_create(cls, *args, **kwargs):
        if kwargs['nodeType'] == 'ArnoldShadingNode':
            node_opt = NGObjOpt(kwargs['node'])
            if node_opt.get('nodeType') in ['image']:
                cls._set_image_create_(node_opt)
    @classmethod
    def _set_image_create_(cls, node_opt):
        """
        # coding:utf-8
        import lxkatana

        lxkatana.set_reload()

        from lxkatana import ktn_core

        ktn_core.ArnoldEventMtd._set_image_create_(
            ktn_core.NGObjOpt(
                NodegraphAPI.GetNode('image')
            )
        )
        :param node_opt:
        :return:
        """
        def connect_fnc_():
            _key = cls.DIRECTORY_KEY
            _parent_opt = node_opt.get_parent_opt()
            if _parent_opt:
                # ignore when expression is enable
                if node_opt.get_is_expression(_key) is True:
                    return False
                if node_opt.get(_key) != cls.DIRECTORY_VALUE:
                    return False
                #
                _parent_type = _parent_opt.get_type()
                if _parent_type == 'NetworkMaterialCreate':
                    if not _parent_opt.get(_key):
                        return False
                    node_opt.set_expression(
                        _key, 'getParent().extra.texture_directory'
                    )
                    return True
                elif _parent_type == 'ShadingGroup':
                    ___parent_opt = _parent_opt.get_parent_opt()
                    if ___parent_opt.get_type() == 'NetworkMaterialCreate':
                        if not ___parent_opt.get(_key):
                            return False
                        #
                        node_opt.set_expression(
                            _key, 'getParent().getParent().extra.texture_directory'
                        )
                        return True

        def post_connect_fnc_():
            if not node_opt.get(cls.DIRECTORY_KEY):
                return False
            #
            if not node_opt.get('parameters.filename.value'):
                node_opt.set(
                    'parameters.filename.enable', 1
                )
                node_opt.set_expression(
                    'parameters.filename.value', 'extra.texture_directory+\'/tx\'+\'/texture_name.<udim>.tx\''
                )
                #
                node_opt.set(
                    'parameters.ignore_missing_textures.enable', 1
                )
                node_opt.set(
                    'parameters.ignore_missing_textures.value', 1
                )
            #
            node_opt.set_attributes(
                dict(
                    ns_colorr=0.3199999928474426,
                    ns_colorg=0.07999999821186066,
                    ns_colorb=0.3199999928474426
                )
            )
        #
        p_ns = [
            (cls.DIRECTORY_KEY, dict(widget='file', value=cls.DIRECTORY_VALUE)),
        ]
        for i_p_n, i_p_r in p_ns:
            if node_opt.get_port(i_p_n) is None:
                NGMacro(node_opt.ktn_obj).set_parameter_create(
                    i_p_n, i_p_r
                )
        #
        connect_fnc_()
        #
        timer = threading.Timer(1, post_connect_fnc_)
        timer.start()


class CallbackMethod(object):
    @classmethod
    def set_scene_load(cls, *args, **kwargs):
        # {'filename': '/data/f/event_test.katana', 'objectHash': None}
        file_path = kwargs['filename']
        _ = NodegraphAPI.GetAllNodesByType('ArnoldShadingNode') or []

        for ktn_obj in _:
            ktn_obj_opt = NGObjOpt(ktn_obj)
            shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
            if shader_type_name in ['ramp_rgb', 'ramp_float']:
                # noinspection PyBroadException
                try:
                    EventMethod.set_arnold_ramp_write(ktn_obj_opt)
                except Exception:
                    print ktn_obj_opt.name
    @classmethod
    def set_callbacks_add(cls):
        ss = [
            (cls.set_scene_load, Callbacks.Type.onSceneLoad),
        ]
        for function, callback_type in ss:
            callback_opt = CallbackOpt(function=function, callback_type=callback_type)
            callback_opt.set_add()


class NGNmeOpt(object):
    STATE_DICT = {}
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj
    @classmethod
    def _set_status_(cls, key):
        cls.STATE_DICT[key] = True
    @classmethod
    def _get_status_(cls, key):
        return cls.STATE_DICT.get(key, False)

    def set_contents_update(self):
        key = self._ktn_obj.getName()
        pre_status = self._get_status_(key)
        if pre_status is False:
            cls = self._ktn_obj.__class__
            mod = sys.modules[cls.__module__]
            status = mod.UpdateStatus
            #
            if _get_is_ui_mode_() is False:
                print('update "NetworkMaterialEdit" "{}" events is ignored'.format(self._ktn_obj.getName()))
                self._ktn_obj.__dict__['_NetworkMaterialEditNode__queuedNodeGraphEvents'] = []
            #
            updateStatus = self._ktn_obj._NetworkMaterialEditNode__updateContents()
            print updateStatus
            if updateStatus == status.Succeeded:
                print('update "NetworkMaterialEdit" "{}" completed'.format(self._ktn_obj.getName()))
                self._set_status_(key)
                return True
            elif updateStatus == status.UserCancelled:
                print('update "NetworkMaterialEdit" "{}" is cancelled by the user'.format(self._ktn_obj.getName()))
            #
            print('update "NetworkMaterialEdit" "{}" is failed'.format(self._ktn_obj.getName()))
            return False
        return False

    def set_contents_update_(self):
        key = self._ktn_obj.getName()
        pre_status = self._get_status_(key)
        if pre_status is False:
            mod = sys.modules[self._ktn_obj.__class__.__module__]
            status = mod.UpdateStatus
            #
            updateStatus = self._set_contents_update_(self._ktn_obj)
            if updateStatus == status.Succeeded:
                print('update "NetworkMaterialEdit" "{}" completed'.format(self._ktn_obj.getName()))
                self._set_status_(key)
                return True
            elif updateStatus == status.UserCancelled:
                print('update "NetworkMaterialEdit" "{}" is cancelled by the user'.format(self._ktn_obj.getName()))
            #
            print('update "NetworkMaterialEdit" "{}" is failed'.format(self._ktn_obj.getName()))
            return False
        return False
    @classmethod
    def _set_contents_update_(cls, ktn_obj):
        """
        from katana: __plugins2__.NetworkMaterials.v1.NetworkMaterialEditNode.NetworkMaterialEditNode
        :param ktn_obj:
        :return:
        """
        mod = sys.modules[ktn_obj.__class__.__module__]
        UpdateStatus = mod.UpdateStatus
        with ktn_obj._NetworkMaterialEditNode__ignoreChanges():
            upstreamMaterial = ktn_obj._NetworkMaterialEditNode__getIncomingMaterialAttributes()
            producer = ktn_obj._NetworkMaterialEditNode__getEditedGeometryProducer()
            materialAttr = None
            if producer is not None:
                materialAttr = producer.getGlobalAttribute('material')
            status = UpdateStatus.Succeeded
            if not upstreamMaterial or not materialAttr or producer.getType() == 'error':
                ktn_obj._NetworkMaterialEditNode__clearContents()
                status = UpdateStatus.Failed
            elif upstreamMaterial.getHash() != ktn_obj._NetworkMaterialEditNode__lastUpstreamMaterialHash:
                ktn_obj._NetworkMaterialEditNode__clearContents()
                if _get_is_ui_mode_() is True:
                    populated = ktn_obj._NetworkMaterialEditNode__populateFromInputMaterial(upstreamMaterial, materialAttr)
                else:
                    populated = cls._populate_fromInput_material(ktn_obj, upstreamMaterial, materialAttr)
                if not populated:
                    status = UpdateStatus.UserCancelled
            if status == UpdateStatus.UserCancelled:
                ktn_obj._NetworkMaterialEditNode__lastUpstreamMaterialHash = None
            else:
                ktn_obj._NetworkMaterialEditNode__lastUpstreamMaterialHash = materialAttr and upstreamMaterial and upstreamMaterial.getHash()
            #
            if _get_is_ui_mode_() is True:
                ktn_obj._NetworkMaterialEditNode__notifyUpdated()
            return status
    @classmethod
    def _populate_fromInput_material(cls, ktn_obj, incomingMaterial, materialAttr):
        mod = sys.modules[ktn_obj.__class__.__module__]
        #
        ktn_obj._NetworkMaterialEditNode__reconstructionInProgress = True
        nmcNetworkMaterialNodeNameAttr = materialAttr.getChildByName('info.name')
        if nmcNetworkMaterialNodeNameAttr is None:
            return False
        else:
            nmcNetworkMaterialNodeName = nmcNetworkMaterialNodeNameAttr.getValue()
            layoutAttr = materialAttr.getChildByName('layout')
            if layoutAttr is None:
                return False
            parentAttr = layoutAttr.getChildByName('%s.parent' % nmcNetworkMaterialNodeName)
            if parentAttr is None:
                return False
            nmcName = parentAttr.getValue()
            ktn_obj._NetworkMaterialEditNode__nodeSourceNameLookup[ktn_obj] = nmcName
            opArgs = ktn_obj._getGenericOpArgs()
            layoutAttr = materialAttr.getChildByName('layout')
            totalNodes = layoutAttr.getNumberOfChildren()
            progressCallback = mod._GetUpdateProgressCallback(totalNodes)
            orderedNodeNames = mod.LayoutNodesSorter(layoutAttr).build()
            paramExtractor = mod.LayoutParameterExtractor(opArgs, orderedNodeNames)
            try:
                for i in range(totalNodes):
                    nodeName = orderedNodeNames[i]
                    nodeLayoutAttr = layoutAttr.getChildByName(nodeName)
                    node = ktn_obj._NetworkMaterialEditNode__createNodeFromLayoutAttr(paramExtractor, nodeName, nodeLayoutAttr)
                    if node:
                        ktn_obj._NetworkMaterialEditNode__shadingNetworkNodes[nodeName] = node
                        ktn_obj._NetworkMaterialEditNode__nodeSourceNameLookup[node] = nodeName
                #
                ktn_obj._NetworkMaterialEditNode__connectNodes(layoutAttr)
                ktn_obj._NetworkMaterialEditNode__setMaterialLocationCallbackOnNodes(incomingMaterial)
                ktn_obj._NetworkMaterialEditNode__lockNonContributingNodes(materialAttr, orderedNodeNames)
                ktn_obj._NetworkMaterialEditNode__reconstructionInProgress = False
                ktn_obj.invalidateLayout()
                sourceLayoutVersionAttr = materialAttr.getChildByName('info.sourceLayoutVersion')
                nodesToLayout = paramExtractor.getSparseNodes('position')
                viewState = None
                if sourceLayoutVersionAttr is not None and sourceLayoutVersionAttr.getValue() == 0:
                    nodesToLayout = ktn_obj._NetworkMaterialEditNode__shadingNetworkNodes.values()
                    viewState = 1.0
                if nodesToLayout:
                    ktn_obj._NetworkMaterialEditNode__autoLayoutShadingNetworkNodes(nodesToLayout, viewState)
                return True
            finally:
                ktn_obj._NetworkMaterialEditNode__reconstructionInProgress = False
                progressCallback(totalNodes)

    def _test_(self):
        self._set_contents_update_(
            self._ktn_obj
        )


class NGObjCustomizePortOpt(object):
    def __init__(self, ktn_port):
        self._ktn_obj = ktn_port

    def set_ports_add(self, raw):
        # etc:
        # collections.OrderedDict(
        #     [
        #         ('render_settings.camera', ''),
        #         ('render_settings.resolution', '512x512'),
        #         ('render_settings.frame', 1),
        #         #
        #         ('arnold_render_settings.stats_file', ''),
        #         ('arnold_render_settings.profile_file', '')
        #     ]
        # )
        ps = self._ktn_obj.getParameters()
        for k, v in raw.items():
            if isinstance(k, six.string_types):
                i_port_path = k
                scheme = None
            elif isinstance(k, (tuple, )):
                scheme, i_port_path, = k
            else:
                raise TypeError()
            #
            i_ps = i_port_path.split('.')
            i_gs = i_ps[:-1]
            i_p = i_ps[-1]
            c_g = ps
            for i_p_n in i_gs:
                i_g = c_g.getChild(i_p_n)
                if i_g is None:
                    i_g = c_g.createChildGroup(i_p_n)
                #
                i_g_l = bsc_core.RawStringUnderlineOpt(i_p_n).to_prettify(capitalize=False)
                i_g.setHintString(
                    str(
                        str({'label': i_g_l})
                    )
                )
                c_g = i_g
            #
            i_ktn_group_port = c_g
            self._set_type_port_add_(
                i_ktn_group_port, scheme=scheme, name=i_p, value=v, default=v
            )

    def set_port_add(self, key, value):
        pass
    @classmethod
    def _set_port_add_as_enable_(cls):
        pass
    @classmethod
    def _set_type_port_add_(cls, ktn_group_port, name, scheme, value, default):
        label = bsc_core.RawStringUnderlineOpt(name).to_prettify(capitalize=False)
        ktn_port = ktn_group_port.getChild(name)
        if ktn_port is None:
            if isinstance(default, (bool, )):
                ktn_port = ktn_group_port.createChildNumber(name, value)
                ktn_port.setHintString(str({'widget': 'checkBox', 'constant': 'True'}))
            elif isinstance(default, six.string_types):
                ktn_port = ktn_group_port.createChildString(name, value)
                if scheme in ['path']:
                    ktn_port.setHintString(
                        str({'widget': 'scenegraphLocation'})
                    )
                elif scheme in ['file']:
                    ktn_port.setHintString(
                        str({'widget': 'fileInput'})
                    )
                elif scheme in ['script']:
                    ktn_port.setHintString(
                        str({'widget': 'scriptEditor'})
                    )
                elif scheme in ['resolution']:
                    ktn_port.setHintString(
                        str({'widget': 'resolution'})
                    )
                elif scheme in ['button']:
                    ktn_port.setHintString(
                        str({'widget': 'scriptButton', 'buttonText': label, 'scriptText': value})
                    )
            elif isinstance(default, (int, float)):
                ktn_port = ktn_group_port.createChildNumber(name, value)
            elif isinstance(default, (tuple, )):
                if scheme in ['enumerate']:
                    ktn_port = ktn_group_port.createChildString(name, value[0])
                    ktn_port.setHintString(
                        str(dict(widget='popup', options=list(value)))
                    )
                else:
                    c = len(default)
                    if isinstance(default[0], six.string_types):
                        ktn_port = ktn_group_port.createChildStringArray(name, c)
                    elif isinstance(default[0], (int, float)):
                        ktn_port = ktn_group_port.createChildNumberArray(name, c)
                    else:
                        raise TypeError()
                    #
                    for i in range(c):
                        i_ktn_port = ktn_port.getChildByIndex(i)
                        i_ktn_port.setValue(default[i], 0)
            else:
                raise TypeError()
            #
            hint_string = ktn_port.getHintString()
            if hint_string:
                hint_dict = eval(hint_string)
            else:
                hint_dict = {'constant': 'True'}
            #
            hint_dict['label'] = label
            ktn_port.setHintString(
                str(hint_dict)
            )


class NGMacro(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_input_port_create(self, port_path):
        _ = self._ktn_obj.getInputPort(port_path)
        if _ is None:
            self._ktn_obj.addInputPort(port_path)

    def set_output_port_create(self, port_path):
        _ = self._ktn_obj.getOutputPort(port_path)
        if _ is None:
            self._ktn_obj.addOutputPort(port_path)

    def set_parameter_create(self, port_path, port_raw):
        ktn_root_port = self._ktn_obj.getParameters()
        #
        _port_path = port_path.split('.')
        group_names = _port_path[:-1]
        port_name = _port_path[-1]
        current_group_port = ktn_root_port
        for i_group_name in group_names:
            i_ktn_group_port = current_group_port.getChild(i_group_name)
            if i_ktn_group_port is None:
                i_ktn_group_port = current_group_port.createChildGroup(i_group_name)
            #
            i_group_label = bsc_core.RawStringUnderlineOpt(i_group_name).to_prettify(capitalize=False)
            i_ktn_group_port.setHintString(
                str(
                    str({'label': i_group_label})
                )
            )
            current_group_port = i_ktn_group_port
        #
        ktn_group_port = current_group_port
        #
        self._set_type_parameter_create_(
            ktn_group_port,
            widget=port_raw.get('widget'),
            name=port_name,
            value=port_raw.get('value'),
            expression=port_raw.get('expression'),
            tool_tip=port_raw.get('tool_tip')
        )
    @classmethod
    def _set_type_parameter_create_(cls, ktn_group_port, name, widget, value, expression, tool_tip):
        label = bsc_core.RawStringUnderlineOpt(name).to_prettify(capitalize=False)
        ktn_port = ktn_group_port.getChild(name)
        if ktn_port is None:
            if isinstance(value, (bool,)):
                ktn_port = ktn_group_port.createChildNumber(name, value)
                ktn_port.setHintString(str({'widget': 'checkBox', 'constant': 'True'}))
            elif isinstance(value, six.string_types):
                ktn_port = ktn_group_port.createChildString(name, value)
                if expression:
                    ktn_port.setExpression(expression)
                if widget in ['path']:
                    ktn_port.setHintString(
                        str({'widget': 'scenegraphLocation'})
                    )
                elif widget in ['file']:
                    ktn_port.setHintString(
                        str({'widget': 'fileInput'})
                    )
                elif widget in ['script']:
                    ktn_port.setHintString(
                        str({'widget': 'scriptEditor'})
                    )
                elif widget in ['resolution']:
                    ktn_port.setHintString(
                        str({'widget': 'resolution'})
                    )
                elif widget in ['button']:
                    ktn_port.setHintString(
                        str({'widget': 'scriptButton', 'buttonText': label, 'scriptText': value})
                    )
            elif isinstance(value, (int, float)):
                ktn_port = ktn_group_port.createChildNumber(name, value)
                if widget in ['boolean']:
                    ktn_port.setHintString(
                        str({'widget': 'boolean'})
                    )
            elif isinstance(value, (list,)):
                if widget in ['enumerate']:
                    ktn_port = ktn_group_port.createChildString(name, value[0])
                    ktn_port.setHintString(
                        str(dict(widget='popup', options=list(value)))
                    )
                elif widget in ['color3']:
                    c = 3
                    ktn_port = ktn_group_port.createChildNumberArray(name, c)
                    for i in range(c):
                        i_ktn_port = ktn_port.getChildByIndex(i)
                        i_ktn_port.setValue(value[i], 0)
                    #
                    ktn_port.setHintString(
                        str(dict(widget='color'))
                    )
                elif widget in ['float3']:
                    c = 3
                    ktn_port = ktn_group_port.createChildNumberArray(name, c)
                    for i in range(c):
                        i_ktn_port = ktn_port.getChildByIndex(i)
                        i_ktn_port.setValue(value[i], 0)
                else:
                    c = len(value)
                    if isinstance(value[0], six.string_types):
                        ktn_port = ktn_group_port.createChildStringArray(name, c)
                    elif isinstance(value[0], (int, float)):
                        ktn_port = ktn_group_port.createChildNumberArray(name, c)
                    else:
                        raise TypeError()
                    #
                    for i in range(c):
                        i_ktn_port = ktn_port.getChildByIndex(i)
                        i_ktn_port.setValue(value[i], 0)
            else:
                raise TypeError()
            #
            hint_string = ktn_port.getHintString()
            if hint_string:
                hint_dict = eval(hint_string)
            else:
                hint_dict = {'constant': 'True'}
            #
            if tool_tip is not None:
                hint_dict['help'] = tool_tip
            hint_dict['label'] = label
            ktn_port.setHintString(
                str(hint_dict)
            )

    def set_ports_clear(self, port_path=None):
        NGObjOpt(self._ktn_obj).set_ports_clear(port_path)
    @ktn_modifiers.set_undo_mark_mdf
    def set_create_by_configure_file(self, file_path, clear_start=None):
        NGObjOpt(self._ktn_obj).set_ports_clear(clear_start)
        #
        configure = bsc_objects.Configure(value=file_path)
        input_ports = configure.get('input_ports') or []
        #
        for i_input_port_path in input_ports:
            self.set_input_port_create(i_input_port_path)
        #
        output_ports = configure.get('output_ports') or []
        for i_output_port_path in output_ports:
            self.set_output_port_create(i_output_port_path)
        #
        parameters = configure.get('parameters') or {}
        for k, v in parameters.items():
            k = k.replace('/', '.')
            self.set_parameter_create(k, v)
    @ktn_modifiers.set_undo_mark_mdf
    def set_create_to_op_script_by_configure_file(self, file_path, paths=None):
        if paths is not None:
            ktn_op_scripts = [NodegraphAPI.GetNode(i) for i in paths]
        else:
            ktn_op_scripts = NGObjOpt(self._ktn_obj).get_children(include_type_names=['OpScript'])
        for i_ktn_op_script in ktn_op_scripts:
            configure = bsc_objects.Configure(value=file_path)
            parameters = configure.get('parameters') or {}
            NGObjOpt(i_ktn_op_script).set_ports_clear('user')
            for k, v in parameters.items():
                i_k_s = k.replace('/', '.')
                i_k_t = k.replace('/', '__')
                if v.get('widget') != 'button':
                    i_k_t = 'user.{}'.format(i_k_t)
                    NGMacro(i_ktn_op_script).set_parameter_create(i_k_t, v)
                    NGPortOpt(NGObjOpt(i_ktn_op_script).get_port(i_k_t)).set_expression('getParent().{}'.format(i_k_s))

    def set_sub_op_script_create_by_configure_file(self, file_path, key, paths):
        ktn_op_scripts = [NodegraphAPI.GetNode(i) for i in paths]
        for i_ktn_op_script in ktn_op_scripts:
            configure = bsc_objects.Configure(value=file_path)
            parameters = configure.get('op_script.{}.parameters'.format(key)) or {}
            NGObjOpt(i_ktn_op_script).set_ports_clear('user')
            for k, v in parameters.items():
                k = k.replace('/', '.')
                NGMacro(i_ktn_op_script).set_parameter_create(k, v)
            #
            script = configure.get('op_script.{}.script'.format(key))
            NGObjOpt(i_ktn_op_script).set('script.lua', script)


class LXRenderSettingsOpt(object):
    def __init__(self, ktn_obj):
        pass


class VariablesSetting(object):
    def __init__(self):
        self._ktn_obj = NodegraphAPI.GetNode('rootNode')

    def set(self, key, value):
        port_path = 'variables.{}.options'.format(key)
        ktn_port = self._ktn_obj.getParameter(port_path)
        if ktn_port is None:
            pass
        NGPortOpt(ktn_port).set(value)

    def set_register(self, key, values):
        ktn_port = self._ktn_obj.getParameter('variables')
        group_ktn_port = ktn_port.getChild(key)
        if group_ktn_port is not None:
            ktn_port.deleteChild(group_ktn_port)
            _ = NGObjOpt(self._ktn_obj).get_port_raw('variables.{}.value'.format(key))
            if _ in values:
                value = _
            else:
                value = values[0]
        else:
            value = values[0]
        #
        group_ktn_port = ktn_port.createChildGroup(key)
        group_ktn_port.createChildNumber('enable', 1)
        group_ktn_port.createChildString('value', value)
        c = len(values)
        #
        options_port = group_ktn_port.createChildStringArray('options', c)
        for i in range(c):
            i_ktn_port = options_port.getChildByIndex(i)
            i_ktn_port.setValue(values[i], 0)

    def set_register_by_configure(self, dic):
        for k, v in dic.items():
            self.set_register(k, v)

    def get_variants(self):
        dic = collections.OrderedDict()
        ktn_port = self._ktn_obj.getParameter('variables')
        for i in ktn_port.getChildren():
            i_key = NGPortOpt(i).name
            i_values = NGPortOpt(
                self._ktn_obj.getParameter('variables.{}.options'.format(i_key))
            ).get()
            dic[i_key] = i_values
        return dic


class WorkspaceSettings(object):
    def __init__(self):
        self._ktn_obj = NodegraphAPI.GetNode('rootNode')

    def set(self, key, value):
        ktn_port = self._ktn_obj.getParameter(key)
        if ktn_port is None:
            port_raw = {}
            if isinstance(value, six.string_types):
                port_raw['widget'] = 'string'
                port_raw['value'] = value
            NGMacro(self._ktn_obj).set_parameter_create(
                key, port_raw
            )
        else:
            NGPortOpt(ktn_port).set(value)

    def get(self, key):
        ktn_port = self._ktn_obj.getParameter(key)
        if ktn_port is not None:
            return NGPortOpt(ktn_port).get()
