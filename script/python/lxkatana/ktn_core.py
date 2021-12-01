# coding:utf-8
# noinspection PyUnresolvedReferences
from Katana import NodegraphAPI, Nodes3DAPI, FnGeolib, ScenegraphManager, Utils, Callbacks, Configuration
# noinspection PyUnresolvedReferences
from UI4 import App

from lxbasic import bsc_core

from lxutil import utl_core

from lxobj import obj_core

import fnmatch

import sys


class SceneGraphObjOpt(object):
    def __init__(self, scene_graph_opt, obj_path):
        self._scene_graph_opt = scene_graph_opt
        self._obj_path = obj_path
        self._traversal = scene_graph_opt._get_traversal_(obj_path)

    def get_port(self, port_path):
        if self._traversal.valid():
            return self._traversal.getLocationData().getAttrs().getChildByName(port_path)

    def get_port_raw(self, port_path):
        port = self.get_port(port_path)
        if port is not None:
            return port.getData()[0]


class SceneGraphOpt(object):
    OBJ_PATHSEP = '/'
    PORT_PATHSEP = '.'
    #
    GEOMETRY_ROOT = '/root/world/geo'
    OBJ_OPT_CLS = SceneGraphObjOpt
    def __init__(self, ktn_obj=None):
        if ktn_obj is not None:
            if isinstance(ktn_obj, (str, unicode)):
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
        op = Nodes3DAPI.GetOp(self._transaction, self._ktn_obj)
        self._transaction.setClientOp(self._client, op)
        self._runtime.commit(self._transaction)

    def _get_traversal_(self, obj_path):
        return FnGeolib.Util.Traversal(self._client, obj_path)

    def get_obj(self, obj_path):
        return self._get_traversal_(obj_path)

    def get_obj_opt(self, obj_path):
        return self.OBJ_OPT_CLS(self, obj_path)

    def get_obj_descendant_paths(self, obj_path):
        lis = []
        tvl = self._get_traversal_(obj_path)
        while tvl.valid():
            i_obj_path = tvl.getLocationPath()
            if not i_obj_path == obj_path:
                lis.append(i_obj_path)
            tvl.next()
        return lis

    def get_port(self, atr_path):
        _ = atr_path.split(self.PORT_PATHSEP)
        obj_path = _[0]
        port_path = self.PORT_PATHSEP.join(_[1:])
        tvl = self._get_traversal_(obj_path)
        if tvl.valid():
            return tvl.getLocationData().getAttrs().getChildByName(port_path)

    def get_port_raw(self, atr_path):
        port = self.get_port(atr_path)
        if port is not None:
            return port.getData()

    def __str__(self):
        return '{}(node="{}")'.format(
            self.__class__.__name__,
            self._ktn_obj.getName()
        )


class SceneGraphSelection(object):
    def __init__(self, *args):
        self._paths = args[0]
        self._scene_graph = ScenegraphManager.getActiveScenegraph()

    def set_all_select(self):
        paths = self._paths
        lis = []
        for path in paths:
            ps = bsc_core.DccPathDagOpt(path).get_ancestor_paths()
            for p in ps:
                if p not in lis:
                    if p != '/':
                        lis.append(p)
        #
        self._scene_graph.addOpenLocations(lis, replace=True)
        self._scene_graph.addSelectedLocations(paths, replace=True)
    @classmethod
    def set_clear(cls):
        ScenegraphManager.getActiveScenegraph().clearOpenLocations()
        ScenegraphManager.getActiveScenegraph().addSelectedLocations([], replace=True)


def get_node_graph_tag():
    return App.Tabs.FindTopTab('Node Graph')


class NodeGraphTabOpt(object):
    def __init__(self, tab=None):
        self._tag = App.Tabs.FindTopTab('Node Graph')

    def set_current_node(self, ktn_obj):
        self._tag.setCurrentNodeView(
            ktn_obj
        )

    def set_selection_view_fit(self):
        self._tag.frameSelection()


class NodeGraphOpt(object):
    def __init__(self, ktn_gui):
        self._ktn_gui = ktn_gui


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


class NGObjOpt(object):
    PATHSEP = '/'
    PORT_PATHSEP = '.'
    def __init__(self, ktn_obj):
        if isinstance(ktn_obj, (str, unicode)):
            self._ktn_obj = NodegraphAPI.GetNode(ktn_obj)
        else:
            self._ktn_obj = ktn_obj
    @property
    def ktn_obj(self):
        return self._ktn_obj
    @property
    def type(self):
        return self.ktn_obj.getType()
    @property
    def name(self):
        return self.ktn_obj.getName()

    def set_gui_expanded(self):
        attributes = self.ktn_obj.getAttributes()
        if 'ns_expandedPages' in attributes and 'ns_collapsedPages' in attributes:
            attributes['ns_expandedPages'] = 'Outputs##BUILTIN | Parameters##BUILTIN | '
            attributes['ns_collapsedPages'] = 'Outputs | Parameters | '
            self.ktn_obj.setAttributes(attributes)

    def set_gui_collapsed(self):
        attributes = self.ktn_obj.getAttributes()
        if 'ns_expandedPages' in attributes:
            attributes['ns_expandedPages'] = 'Outputs | Parameters | '
            attributes['ns_collapsedPages'] = 'Outputs##BUILTIN | Parameters##BUILTIN | '
            self.ktn_obj.setAttributes(attributes)

    def get_sources(self):
        lis = []
        _ = self.ktn_obj.getInputPorts() or []
        for target_ktn_port in _:
            source_ktn_ports = target_ktn_port.getConnectedPorts()
            if source_ktn_ports:
                lis.extend(source_ktn_ports)
        return lis

    def get_source_objs(self):
        lis = []
        source_ktn_ports = self.get_sources()
        for source_ktn_port in source_ktn_ports:
            ktn_obj = source_ktn_port.getNode()
            if ktn_obj not in lis:
                lis.append(ktn_obj)
        return lis

    def set_gui_layout(self, layout=('r-l', 't-b'), size=(320, 960), expanded=False, collapsed=False):
        def rcs_fnc_(ktn_obj_, column_):
            _source_ktn_objs = self.__class__(ktn_obj_).get_source_objs()
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
        #
        ktn_obj_stack = []
        ktn_obj_in_column_dict = {}
        #
        layout_x, layout_y = layout
        x, y = NodegraphAPI.GetNodePosition(self.ktn_obj)
        w, h = size
        rcs_fnc_(self.ktn_obj, 0)
        if ktn_obj_in_column_dict:
            for column, v in ktn_obj_in_column_dict.items():
                c = len(v)
                if layout_x == 'r-l':
                    s_x = x-column*w*2
                elif layout_x == 'l-r':
                    s_x = x+column*w*2
                else:
                    raise ValueError()
                #
                if layout_y == 't-b':
                    s_y = y+c*h/2
                elif layout_y == 'b-t':
                    s_y = y-c*h/2
                else:
                    raise ValueError()
                if v:
                    for seq, i_ktn_obj in enumerate(v):
                        i_x = s_x
                        if layout_y == 't-b':
                            i_y = s_y-seq*h
                        elif layout_y == 'b-t':
                            i_y = s_y+seq*h
                        else:
                            raise ValueError()
                        #
                        i_atr = dict(
                            x=i_x,
                            y=i_y,
                        )
                        i_atr_ = i_ktn_obj.getAttributes()
                        i_atr_.update(i_atr)
                        i_ktn_obj.setAttributes(i_atr_)
                        if expanded is True:
                            self.__class__(i_ktn_obj).set_gui_expanded()
                        elif collapsed is True:
                            self.__class__(i_ktn_obj).set_gui_collapsed()

    def get_port_raw(self, port_path):
        port = self.ktn_obj.getParameter(port_path)
        if port:
            return NGPortOpt(port).get()

    def set_port_raw(self, port_path, raw):
        port = self.ktn_obj.getParameter(port_path)
        if port:
            NGPortOpt(port).set(raw)

    def get_port(self, port_path):
        return self.ktn_obj.getParameter(port_path)

    def set_port_create(self, port_path, type_, value):
        _ = self.get_port(port_path)
        port_parent = obj_core.PortPathMethod.get_dag_parent(
            path=port_path, pathsep=self.PORT_PATHSEP
        )
        port_name = obj_core.PortPathMethod.get_dag_name(
            path=port_path, pathsep=self.PORT_PATHSEP
        )
        if _ is None:
            if port_parent is not None:
                parent_ktn_port = self.ktn_obj.getParameter(port_parent)
            else:
                parent_ktn_port = self.ktn_obj.getParameters()
            #
            if parent_ktn_port is not None:
                if type_ == 'string':
                    parent_ktn_port.createChildString(port_name, str(value))

    def set_delete(self):
        self.ktn_obj.delete()


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
        obj_type_name = src_ktn_obj.getChildNodeType()
        tgt_ktn_obj = NodegraphAPI.GetNode(name)
        if tgt_ktn_obj is not None:
            return tgt_ktn_obj, False
        #
        tgt_ktn_obj = NodegraphAPI.CreateNode(obj_type_name, src_ktn_obj)
        if tgt_ktn_obj is None:
            raise TypeError('unknown-obj-type: "{}"'.format(obj_type_name))
        name_ktn_port = tgt_ktn_obj.getParameter('name')
        if name_ktn_port is not None:
            name_ktn_port.setValue(name, 0)
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
    @property
    def name(self):
        return self.ktn_port.getName()
    @classmethod
    def _get_atr_path_(cls, ktn_port):
        def rcs_fnc_(ktn_port_):
            if ktn_port_ is not None:
                _port_name = ktn_port_.getName()
                lis.append(_port_name)
                _parent_ktn_port = ktn_port_.getParent()
                rcs_fnc_(_parent_ktn_port)
        #
        lis = []
        #
        rcs_fnc_(ktn_port)
        #
        lis.reverse()
        return cls.PATHSEP.join(lis)
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
            self.ktn_port.setValue(_value, frame)

    def set_connect_to(self, input_port):
        pass


class NGAndObjTypeOpt(object):
    def __init__(self, obj_type_name):
        self._obj_type_name = obj_type_name

    def get_ktn_objs(self):
        lis = []
        for i_ktn_obj in NodegraphAPI.GetAllNodesByType('ArnoldShadingNode') or []:
            i_ktn_obj_opt = NGObjOpt(i_ktn_obj)
            i_shader_type_name = i_ktn_obj_opt.get_port_raw('nodeType')
            if i_shader_type_name in [self._obj_type_name]:
                lis.append(i_ktn_obj)
        return lis

    def get_obj_opts(self):
        lis = []
        for i_ktn_obj in NodegraphAPI.GetAllNodesByType('ArnoldShadingNode') or []:
            i_ktn_obj_opt = NGObjOpt(i_ktn_obj)
            i_shader_type_name = i_ktn_obj_opt.get_port_raw('nodeType')
            if i_shader_type_name in [self._obj_type_name]:
                lis.append(i_ktn_obj_opt)
        return lis


class NodeGraphInputPort(object):
    pass


class EventOpt(object):
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


def _get_is_ui_mode_():
    return Configuration.get('KATANA_UI_MODE') == '1'


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
            if isinstance(k, (str, unicode)):
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
                i_g_l = bsc_core.StrUnderlineOpt(i_p_n).to_prettify(capitalize=False)
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
    @classmethod
    def _set_port_add_as_enable_(cls):
        pass
    @classmethod
    def _set_type_port_add_(cls, ktn_group_port, name, scheme, value, default):
        label = bsc_core.StrUnderlineOpt(name).to_prettify(capitalize=False)
        ktn_port = ktn_group_port.getChild(name)
        if ktn_port is None:
            if isinstance(default, (bool, )):
                ktn_port = ktn_group_port.createChildNumber(name, value)
                ktn_port.setHintString(str({'widget': 'checkBox', 'constant': 'True'}))
            elif isinstance(default, (str, unicode)):
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
                c = len(default)
                if isinstance(default[0], (str, unicode)):
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


class LXRenderSettingsOpt(object):
    def __init__(self, ktn_obj):
        pass
