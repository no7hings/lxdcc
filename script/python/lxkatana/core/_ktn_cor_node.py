# coding:utf-8
from ._ktn_cor_utility import *


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


class NGLayoutOpt(object):
    class Orientation(object):
        Horizontal = 'h'
        Vertical = 'v'

    class Direction(object):
        RightToLeft = 'r-l'
        LeftToRight = 'l-r'
        TopToBottom = 't-b'
        BottomToTop = 'b-t'

    def __init__(self, graph_data, scheme=(Orientation.Horizontal, Direction.RightToLeft, Direction.TopToBottom), size=(320, 80), option=None):
        self._source_dict, self._index_dict, self._graph_dict = graph_data
        self._scheme = scheme
        self._size = size
        self._option = option or {}
        self._data_dict = self._get_data_query_()

    def _get_data_query_(self):
        dict_ = {}
        for i_key, i_data in self._graph_dict.items():
            i_start_name, i_depth, i_index = i_key
            i_count = len(i_data)
            for j_sub_index, j_name in enumerate(i_data):
                dict_[j_name] = i_count, i_index, j_sub_index
        return dict_

    def _layout_fnc_(self, name, position):
        #
        x, y = position
        i_atr = dict(
            x=x, y=y,
        )
        obj_opt = NGObjOpt(name)
        i_atr_ = obj_opt.ktn_obj.getAttributes()
        i_atr_.update(i_atr)
        obj_opt.ktn_obj.setAttributes(i_atr_)
        if isinstance(self._option, dict):
            expanded = self._option.get('expanded')
            collapsed = self._option.get('collapsed')
            if expanded is True:
                obj_opt.set_shader_gui_expanded()
            #
            elif collapsed is True:
                obj_opt.set_shader_gui_collapsed()
            #
            shader_view_state = self._option.get('shader_view_state')
            if isinstance(shader_view_state, (int, float)):
                obj_opt.set_shader_view_state(float(shader_view_state))

    def _get_position_(self, x, y, w, h, count, index, sub_index):
        ort, drt_h, drt_v = self._scheme
        if ort == self.Orientation.Horizontal:
            if drt_h == 'r-l':
                s_x = x - index * w * 2
            elif drt_h == 'l-r':
                s_x = x + index * w * 2
            else:
                raise ValueError()
            #
            if drt_v == 't-b':
                s_y = y + ((count - (count % 2)) * h) / 2
            elif drt_v == 'b-t':
                s_y = y - ((count - (count % 2)) * h) / 2
            else:
                raise ValueError()
            #
            j_x = s_x
            if drt_v == 't-b':
                j_y = s_y - sub_index * h
            elif drt_v == 'b-t':
                j_y = s_y + sub_index * h
            else:
                raise ValueError()
            return j_x, j_y
        elif ort == self.Orientation.Vertical:
            if drt_v == 't-b':
                s_y_ = y - index * h * 2
            elif drt_v == 'b-t':
                s_y_ = y + index * h * 2
            else:
                raise ValueError()
            #
            if drt_h == 'r-l':
                s_x_ = x + ((count - (count % 2)) * w) / 2
            elif drt_h == 'l-r':
                s_x_ = x - ((count - (count % 2)) * w) / 2
            else:
                raise ValueError()
            #
            j_y_ = s_y_
            if drt_h == 'r-l':
                j_x_ = s_x_ - sub_index * w
            elif drt_h == 'l-r':
                j_x_ = s_x_ + sub_index * w
            else:
                raise ValueError()
            return j_x_, j_y_

    def run(self, depth_maximum=-1):
        if not self._graph_dict:
            return
        #
        w, h = self._size
        ort, drt_h, drt_v = self._scheme
        #
        position_dict = {}
        for i_key, i_data in self._graph_dict.items():
            i_start_name, i_depth, i_index = i_key
            if i_depth > 0:
                x, y = 0, 0
            else:
                x, y = NGObjOpt(i_start_name).get_position()
            #
            if i_data:
                i_count = len(i_data)
                for j_sub_index, j_name in enumerate(i_data):
                    j_x, j_y = self._get_position_(
                        x, y, w, h, i_count, i_index, j_sub_index
                    )
                    if NGObjOpt(j_name).get_type_name() in ['Dot']:
                        i_source_name = self._source_dict[j_name]
                        if i_source_name in self._index_dict:
                            j_count_, j_index_, j_sub_index_ = self._data_dict[i_source_name]
                            j_x_, j_y_ = self._get_position_(
                                x, y, w, h, j_count_, j_index_, j_sub_index_
                            )
                            if ort == self.Orientation.Horizontal:
                                j_y = j_y_
                            elif ort == self.Orientation.Vertical:
                                j_x = j_x_
                    position_dict[j_name] = (j_x, j_y)
        #
        if position_dict:
            for k, v in position_dict.items():
                self._layout_fnc_(k, v)


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
    def _get_group_stack_child_create_args_(cls, path, type_name):
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
                input_port = ktn_obj.getInputPorts()[0]
                output_port = ktn_obj.getOutputPorts()[0]
                #
                parent_return_port = NGObjOpt(parent_ktn_obj).get_return_ports()[0]
                cur_output_port = parent_return_port.getConnectedPorts()[0]
                cur_output_port.connect(input_port)
                #
                output_port.connect(parent_return_port)
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
        if 'inner' in kwargs:
            _ = self._get_sources_inner_(self._ktn_obj)
        else:
            _ = self.get_sources(**kwargs)
        for i_ktn_port in _:
            i_ktn_obj = i_ktn_port.getNode()
            if i_ktn_obj not in list_:
                list_.append(i_ktn_obj)
        return list_
    @classmethod
    def _get_sources_inner_(cls, ktn_obj):
        list_ = []
        _ = ktn_obj.getOutputPorts() or []
        for i_ktn_port in _:
            i_ktn_ports_rtn = ktn_obj.getReturnPort(i_ktn_port.getName())
            i_ktn_ports_src = i_ktn_ports_rtn.getConnectedPorts()
            if i_ktn_ports_src:
                list_.extend(i_ktn_ports_src)
        return list_
    @classmethod
    def _get_source_objs_inner_(cls, ktn_obj):
        list_ = []
        _ = cls._get_sources_inner_(ktn_obj)
        for i_ktn_port in _:
            i_ktn_obj = i_ktn_port.getNode()
            if i_ktn_obj not in list_:
                list_.append(i_ktn_obj)
        return list_

    def get_all_source_objs(self, **kwargs):
        def rcs_fnc_(list__, ktn_obj_):
            _ktn_objs = self.__class__(ktn_obj_).get_source_objs(**kwargs)
            for _i_ktn_obj in _ktn_objs:
                if _i_ktn_obj not in list__:
                    if hasattr(_i_ktn_obj, 'getChildren'):
                        _i_ktn_objs = self._get_source_objs_inner_(_i_ktn_obj)
                        for _j_ktn_obj in _i_ktn_objs:
                            if _j_ktn_obj not in list__:
                                list__.append(_j_ktn_obj)
                                rcs_fnc_(list__, _j_ktn_obj)
                    else:
                        list__.append(_i_ktn_obj)
                        rcs_fnc_(list__, _i_ktn_obj)
        #
        inner = kwargs.get('inner', False)
        #
        list_ = []
        rcs_fnc_(list_, self._ktn_obj)
        return list_

    def get_graph_data(self, **kwargs):
        def rcs_fnc_(ktn_obj_, start_name_, source_name_, depth_, index_):
            if hasattr(ktn_obj_, 'getChildren'):
                _source_name = ktn_obj_.getName()
                outer_fnc_(ktn_obj_, start_name_, _source_name, depth_, index_)
                # inner
                if inner is True:
                    _group_name = ktn_obj_.getName()
                    inner_fnc_(ktn_obj_, _group_name, _source_name, depth_, index_)
            else:
                _source_name = ktn_obj_.getName()
                outer_fnc_(ktn_obj_, start_name_, _source_name, depth_, index_)
        #
        def outer_fnc_(ktn_obj_, start_name_, source_name_, depth_, index_):
            _source_ktn_objs = self.__class__(ktn_obj_).get_source_objs()
            #
            if _source_ktn_objs:
                index_ += 1
                add_fnc_(_source_ktn_objs, start_name_, source_name_, depth_, index_)
        #
        def inner_fnc_(ktn_obj_, start_name_, source_name_, depth_, index_):
            depth_ += 1
            #
            _source_ktn_objs = self._get_source_objs_inner_(ktn_obj_)
            if _source_ktn_objs:
                #
                index_ += 1
                add_fnc_(_source_ktn_objs, start_name_, source_name_, depth_, index_)
        #
        def add_fnc_(source_ktn_objs_, start_name_, source_name_, depth_, index_):
            _index_cur = (start_name_, depth_, index_)
            if _index_cur not in graph_dict:
                _data_in_index_cur = []
                graph_dict[_index_cur] = _data_in_index_cur
            else:
                _data_in_index_cur = graph_dict[_index_cur]
            #
            for _row, _i_ktn_obj in enumerate(source_ktn_objs_):
                _i_type_name = _i_ktn_obj.getType()
                _i_name = _i_ktn_obj.getName()
                if _i_name not in source_dict:
                    source_dict[_i_name] = source_name_
                _i_index_cur = _index_cur
                # break the self-cycle
                if _i_name != start_name_:
                    # try move to end
                    if _i_name in index_dict:
                        _i_index_pre = index_dict[_i_name]
                        if _i_index_pre != _i_index_cur:
                            if _i_index_pre in graph_dict:
                                _data_in_index_pre = graph_dict[_i_index_pre]
                                _data_in_index_pre.remove(_i_name)
                                _data_in_index_cur.append(_i_name)
                                index_dict[_i_name] = _i_index_cur
                    else:
                        index_dict[_i_name] = _i_index_cur
                        _data_in_index_cur.append(_i_name)
                    #
                    rcs_fnc_(_i_ktn_obj, start_name_, source_name_, depth_, index_)
        #
        inner = kwargs.get('inner', False)
        #
        source_dict = {}
        index_dict = {}
        #
        name = self._ktn_obj.getName()
        depth = 0
        #
        graph_dict = {
            # (start_name, depth, index): [name, ...]
        }
        #
        rcs_fnc_(self._ktn_obj, name, name, depth, 0)
        return source_dict, index_dict, graph_dict

    def gui_layout_shader_graph(self, scheme=(NGLayoutOpt.Orientation.Horizontal, NGLayoutOpt.Direction.RightToLeft, NGLayoutOpt.Direction.TopToBottom), size=(320, 80), expanded=False, collapsed=False, shader_view_state=None):
        graph_dara = self.get_graph_data(inner=True)
        #
        NGLayoutOpt(
            graph_dara,
            scheme=scheme,
            size=size,
            option=dict(
                expanded=expanded,
                collapsed=collapsed,
                shader_view_state=shader_view_state
            )
        ).run()
    @Modifier.undo_debug_run
    def gui_layout_node_graph(self, scheme=(NGLayoutOpt.Orientation.Vertical, NGLayoutOpt.Direction.LeftToRight, NGLayoutOpt.Direction.BottomToTop), size=(320, 40)):
        graph_dara = self.get_graph_data(inner=True)
        NGLayoutOpt(
            graph_dara,
            scheme=scheme,
            size=size,
        ).run(
            depth_maximum=1
        )

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

    def set_parameters_by_data(self, data, extend_kwargs=None):
        for i_port_path, i_args in data.items():
            #
            i_port_path = i_port_path.replace('/', '.')
            #
            i_p = self.ktn_obj.getParameter(i_port_path)
            if i_p is None:
                bsc_core.LogMtd.trace_warning(
                    'port="{}" is non-exists'.format(i_port_path)
                )
                continue
            #
            i_value = i_args
            if isinstance(i_args, dict):
                #
                i_size = i_args.get('size')
                if i_size is not None:
                    i_p.resizeArray(i_size)
                #
                i_tuple_size = i_args.get('tuple_size')
                if i_tuple_size is not None:
                    i_p.setTupleSize(i_tuple_size)
                #
                i_value = i_args.get('value')
                if i_value is None:
                    return
            #
            if isinstance(extend_kwargs, dict):
                if isinstance(i_value, (unicode, str)):
                    i_value = i_value.format(**extend_kwargs)
            # turn off the expression-flag
            if self.get_is_expression(i_port_path) is True:
                self.set_expression_enable(i_port_path, False)
            #
            self.set(i_port_path, i_value)

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

    def set_arnold_geometry_properties_by_data(self, data, extend_kwargs=None):
        convert_dict = dict(
            subdiv_iterations='iterations',
            disp_zero_value='zero_value'
        )
        for i_port_path, i_value in data.items():
            i_port_path = i_port_path.replace('/', '.')
            #
            if i_port_path in convert_dict:
                i_port_path = convert_dict[i_port_path]
            if isinstance(extend_kwargs, dict):
                if isinstance(i_value, (unicode, str)):
                    i_value = i_value.format(**extend_kwargs)
            #
            i_enable_key = 'args.arnoldStatements.{}.enable'.format(i_port_path)
            self.set(i_enable_key, True)
            #
            i_value_key = 'args.arnoldStatements.{}.value'.format(i_port_path)
            # turn off the expression-flag
            if self.get_is_expression(i_value_key) is True:
                self.set_expression_enable(i_value_key, False)
            self.set(i_value_key, i_value)

    def set_expressions_by_data(self, data, extend_kwargs=None):
        for i_port_path, i_expression in data.items():
            i_port_path = i_port_path.replace('/', '.')
            if isinstance(extend_kwargs, dict):
                if isinstance(i_expression, (unicode, str)):
                    i_expression = i_expression.format(**extend_kwargs)
            #
            self.set_expression_enable(i_port_path, True)
            self.set_expression(i_port_path, i_expression)

    def set_shader_expressions_by_data(self, data, extend_kwargs=None):
        for i_port_path, i_expression in data.items():
            #
            i_port_path = i_port_path.replace('/', '.')
            if isinstance(extend_kwargs, dict):
                if isinstance(i_expression, (unicode, str)):
                    i_expression = i_expression.format(**extend_kwargs)
            # turn on enable first
            i_enable_key = 'parameters.{}.enable'.format(i_port_path)
            self.set(i_enable_key, True)
            #
            i_value_key = 'parameters.{}.value'.format(i_port_path)
            # turn on the expression-flag
            self.set_expression_enable(i_value_key, True)
            self.set_expression(i_value_key, i_expression)

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

    def set_enumerate_strings(self, port_path, raw):
        port = self.ktn_obj.getParameter(port_path)
        if port:
            NGPortOpt(port).set_enumerate_strings(raw)

    def set_as_enumerate(self, key, value):
        self.set_enumerate_strings(key, value)

    def get_port(self, port_path):
        return self.ktn_obj.getParameter(port_path)

    def get_input_port(self, port_path):
        return self._ktn_obj.getInputPort(port_path)

    def get_output_port(self, port_path):
        return self._ktn_obj.getOutputPort(port_path)

    def get_output_ports(self):
        return self._ktn_obj.getOutputPorts()

    def get_return_ports(self):
        return [self._ktn_obj.getReturnPort(i.getName()) for i in self._ktn_obj.getOutputPorts()]
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

    def clear_ports(self, port_path=None):
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

    def clear_children(self, include_type_names=None):
        for i in self.get_children(include_type_names):
            i.delete()

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

    def set_input_port_create(self, port_path, **create_kwargs):
        _ = self._ktn_obj.getInputPort(port_path)
        if _ is not None:
            return _
        return self._ktn_obj.addInputPort(port_path, **create_kwargs)

    def create_input_ports_by_data(self, ports_data):
        for i in ports_data:
            if isinstance(i, six.string_types):
                i_name = i
                self.set_input_port_create(i_name)
            elif isinstance(i, dict):
                i_name = i.keys()[0]
                i_metadata = i.values()[0]
                self.set_input_port_create(i_name)
                i_port = self._ktn_obj.getInputPort(i_name)
                for j_k, j_v in i_metadata.items():
                    i_port.addOrUpdateMetadata(
                        j_k, j_v
                    )

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

    def create_ports_by_data(self, data):
        for k, v in data.items():
            k = k.replace('/', '.')
            self.create_port_by_data(k, v)

    def create_port_by_data(self, port_path, data):
        root_ktn_port = self._ktn_obj.getParameters()
        #
        _port_path = port_path.split('.')
        group_names = _port_path[:-1]
        port_name = _port_path[-1]
        current_group_port = root_ktn_port
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
        group_ktn_obj = current_group_port
        #
        self._create_port_by_data(
            group_ktn_obj,
            dict(
                widget=data.get('widget'),
                name=port_name,
                value=data.get('value'),
                default=data.get('default'),
                expression=data.get('expression'),
                tool_tip=data.get('tool_tip'),
                lock=data.get('lock')
            )
        )
    @classmethod
    def _create_port_by_data(cls, group_ktn_obj, data):
        name = data['name']
        widget = data['widget']
        value = data['value']
        default = data['default']
        expression = data['expression']
        tool_tip = data['tool_tip']
        lock = data['lock']
        label = bsc_core.RawStringUnderlineOpt(name).to_prettify(capitalize=False)
        ktn_port = group_ktn_obj.getChild(name)
        if ktn_port is None:
            if isinstance(value, (bool,)):
                ktn_port = group_ktn_obj.createChildNumber(name, value)
                ktn_port.setHintString(str({'widget': 'checkBox', 'constant': 'True'}))
            elif isinstance(value, six.string_types):
                ktn_port = group_ktn_obj.createChildString(name, value)
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
                ktn_port = group_ktn_obj.createChildNumber(name, value)
                if widget in ['boolean']:
                    ktn_port.setHintString(
                        str({'widget': 'boolean'})
                    )
            elif isinstance(value, (list,)):
                if widget in ['enumerate']:
                    ktn_port = group_ktn_obj.createChildString(name, value[0])
                    ktn_port.setHintString(
                        str(dict(widget='popup', options=list(value)))
                    )
                    if default is not None:
                        ktn_port.setValue(default, 0)
                elif widget in ['color3']:
                    c = 3
                    ktn_port = group_ktn_obj.createChildNumberArray(name, c)
                    for i in range(c):
                        i_ktn_port = ktn_port.getChildByIndex(i)
                        i_ktn_port.setValue(value[i], 0)
                    #
                    ktn_port.setHintString(
                        str(dict(widget='color'))
                    )
                elif widget in ['float3']:
                    c = 3
                    ktn_port = group_ktn_obj.createChildNumberArray(name, c)
                    for i in range(c):
                        i_ktn_port = ktn_port.getChildByIndex(i)
                        i_ktn_port.setValue(value[i], 0)
                elif widget in ['string2']:
                    c = 2
                    ktn_port = group_ktn_obj.createChildStringArray(name, c)
                    for i in range(c):
                        i_ktn_port = ktn_port.getChildByIndex(i)
                        i_ktn_port.setValue(value[i], 0)
                else:
                    c = len(value)
                    if isinstance(value[0], six.string_types):
                        ktn_port = group_ktn_obj.createChildStringArray(name, c)
                    elif isinstance(value[0], (int, float)):
                        ktn_port = group_ktn_obj.createChildNumberArray(name, c)
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
            if lock is True:
                hint_dict['readOnly'] = True
            hint_dict['label'] = label
            ktn_port.setHintString(
                str(hint_dict)
            )

    def save_as_macro(self, file_path):
        UserNodes.PublishNode(
            self._ktn_obj, file_path
        )


class NGObjsOpt(object):
    def __init__(self, type_name=None):
        self._type_name = type_name

    def get_obj_names(self, pattern=None):
        if self._type_name is not None:
            _ = NodegraphAPI.GetAllNodesByType(self._type_name) or []
        else:
            _ = NodegraphAPI.GetAllNodes() or []
        #
        obj_names = [i.getName() for i in _]
        if pattern is not None:
            return fnmatch.filter(
                obj_names, pattern
            )
        return obj_names


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


class NGObjTypeOpt(object):
    def __init__(self, obj_type_name):
        self._obj_type_name = obj_type_name

    def get_objs(self):
        return NodegraphAPI.GetAllNodesByType(self._obj_type_name)


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
            if get_is_ui_mode() is False:
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
                if get_is_ui_mode() is True:
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
            if get_is_ui_mode() is True:
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
    def _set_type_port_add_(cls, group_ktn_obj, name, scheme, value, default):
        label = bsc_core.RawStringUnderlineOpt(name).to_prettify(capitalize=False)
        ktn_port = group_ktn_obj.getChild(name)
        if ktn_port is None:
            if isinstance(default, (bool, )):
                ktn_port = group_ktn_obj.createChildNumber(name, value)
                ktn_port.setHintString(str({'widget': 'checkBox', 'constant': 'True'}))
            elif isinstance(default, six.string_types):
                ktn_port = group_ktn_obj.createChildString(name, value)
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
                ktn_port = group_ktn_obj.createChildNumber(name, value)
            elif isinstance(default, (tuple, )):
                if scheme in ['enumerate']:
                    ktn_port = group_ktn_obj.createChildString(name, value[0])
                    ktn_port.setHintString(
                        str(dict(widget='popup', options=list(value)))
                    )
                else:
                    c = len(default)
                    if isinstance(default[0], six.string_types):
                        ktn_port = group_ktn_obj.createChildStringArray(name, c)
                    elif isinstance(default[0], (int, float)):
                        ktn_port = group_ktn_obj.createChildNumberArray(name, c)
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
    @Modifier.undo_debug_run
    def create_by_configure_file(self, file_path, clear_start=None):
        NGObjOpt(self._ktn_obj).clear_ports(clear_start)
        #
        configure = bsc_objects.Configure(value=file_path)
        input_ports = configure.get('input_ports') or []
        #
        NGObjOpt(self._ktn_obj).set_color(
            configure.get('color')
        )
        #
        for i_input_port_path in input_ports:
            NGObjOpt(self._ktn_obj).set_input_port_create(i_input_port_path)
        #
        output_ports = configure.get('output_ports') or []
        for i_output_port_path in output_ports:
            NGObjOpt(self._ktn_obj).set_output_port_create(i_output_port_path)
        #
        parameters = configure.get('parameters') or {}
        for k, v in parameters.items():
            k = k.replace('/', '.')
            NGObjOpt(self._ktn_obj).create_port_by_data(k, v)
    @Modifier.undo_debug_run
    def set_create_to_op_script_by_configure_file(self, file_path, paths=None):
        if paths is not None:
            ktn_op_scripts = [NodegraphAPI.GetNode(i) for i in paths]
        else:
            ktn_op_scripts = NGObjOpt(self._ktn_obj).get_children(include_type_names=['OpScript'])
        for i_ktn_op_script in ktn_op_scripts:
            configure = bsc_objects.Configure(value=file_path)
            parameters = configure.get('parameters') or {}
            NGObjOpt(i_ktn_op_script).clear_ports('user')
            for k, v in parameters.items():
                i_k_s = k.replace('/', '.')
                i_k_t = k.replace('/', '__')
                if v.get('widget') != 'button':
                    i_k_t = 'user.{}'.format(i_k_t)
                    NGObjOpt(i_ktn_op_script).create_port_by_data(i_k_t, v)
                    NGPortOpt(NGObjOpt(i_ktn_op_script).get_port(i_k_t)).set_expression('getParent().{}'.format(i_k_s))

    def set_sub_op_script_create_by_configure_file(self, file_path, key, paths):
        ktn_op_scripts = [NodegraphAPI.GetNode(i) for i in paths]
        for i_ktn_op_script in ktn_op_scripts:
            configure = bsc_objects.Configure(value=file_path)
            parameters = configure.get('op_script.{}.parameters'.format(key)) or {}
            NGObjOpt(i_ktn_op_script).clear_ports('user')
            for k, v in parameters.items():
                k = k.replace('/', '.')
                NGObjOpt(i_ktn_op_script).create_port_by_data(k, v)
            #
            script = configure.get('op_script.{}.script'.format(key))
            NGObjOpt(i_ktn_op_script).set('script.lua', script)
