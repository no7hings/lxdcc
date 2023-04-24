# coding:utf-8
from ._ktn_cor_utility import *

from lxkatana.core import _ktn_cor_node


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
        bsc_core.LogMtd.trace_method_result(
            'event register',
            'event-type="{}"'.format(self._event_type)
        )

    def set_unregister(self):
        if self.get_is_register() is True:
            Utils.EventModule.UnregisterEventHandler(
                handler=self._handler,
                eventType=self._event_type
            )
            bsc_core.LogMtd.trace_method_result(
                'event deregister',
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
        bsc_core.LogMtd.trace_method_result(
            'callback register',
            'callback-type="{}"'.format(self._callback_type)
        )

    def set_delete(self):
        Callbacks.delCallback(
            callbackType=self._callback_type,
            callbackFcn=self._function
        )
        bsc_core.LogMtd.trace_method_result(
            'callback deregister',
            'callback-type="{}"'.format(self._callback_type)
        )


class EventMtd(object):
    @classmethod
    def get_all_event_types(cls):
        pass

    @classmethod
    def set_port_value(cls, *args, **kwargs):
        event_type, event_id = args
        ktn_obj = kwargs['node']
        ktn_port = kwargs['param']
        ktn_obj_opt = _ktn_cor_node.NGObjOpt(ktn_obj)
        if ktn_obj_opt.type == 'ArnoldShadingNode':
            shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
            if shader_type_name in ['ramp_rgb', 'ramp_float']:
                ktn_port_opt = _ktn_cor_node.NGPortOpt(ktn_port)
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
        ktn_obj_opt = _ktn_cor_node.NGObjOpt(ktn_obj)
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
        ktn_obj_opt = _ktn_cor_node.NGObjOpt(ktn_obj)
        if ktn_obj_opt:
            if ktn_obj_opt.type == 'ArnoldShadingNode':
                shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
                if shader_type_name in ['ramp_rgb', 'ramp_float']:
                    cls.set_arnold_ramp_read(ktn_obj_opt)

    @classmethod
    def set_node_create(cls, *args, **kwargs):
        event_type, event_id = args
        ktn_obj = kwargs['node']
        ktn_obj_opt = _ktn_cor_node.NGObjOpt(ktn_obj)
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
        ktn_obj_opt = _ktn_cor_node.NGObjOpt(ktn_obj)
        if ktn_obj_opt.type == 'ArnoldShadingNode':
            shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
            if shader_type_name in ['ramp_rgb', 'ramp_float']:
                cls.set_arnold_ramp_read(ktn_obj_opt)

    @classmethod
    def set_arnold_ramp_write(cls, ktn_obj_opt):
        cls._set_arnold_ramp_write_(ktn_obj_opt)
        # bsc_core.LogMtd.trace_method_result(
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
                i_ktn_port_opt = _ktn_cor_node.NGPortOpt(i_ktn_port)
                i_ktn_port_opt.set(str(ramp_value_dict))
        #
        # Utils.UndoStack.CloseGroup()

    @classmethod
    def set_arnold_ramp_read(cls, ktn_obj_opt):
        def fnc_():
            cls._set_arnold_ramp_read_(ktn_obj_opt)
            # bsc_core.LogMtd.trace_method_result(
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
            ramp_value_port_opt = _ktn_cor_node.NGPortOpt(ramp_value_port)
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
    DIRECTORY_KEY = 'user.extra.texture_directory'
    DIRECTORY_VALUE = '/texture_directory'

    @classmethod
    def create_material_fnc(cls, *args, **kwargs):
        if kwargs['nodeType'] == 'NetworkMaterialCreate':
            node_opt = _ktn_cor_node.NGObjOpt(kwargs['node'])
            cls._create_material_(node_opt)

    @classmethod
    def _create_material_(cls, node_opt):
        """
        # coding:utf-8
        import lxkatana

        lxkatana.set_reload()

        from lxkatana import ktn_core

        ktn_core.ArnoldEventMtd._create_material_(
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
            if not _parent_opt.get_port(_key):
                return False
            #
            node_opt.set_expression(_key, 'getParent().{}'.format(_key))
            return True

        #
        p_ns = [
            (cls.DIRECTORY_KEY, dict(widget='file', value=cls.DIRECTORY_VALUE)),
        ]
        for i_p_n, i_p_r in p_ns:
            if node_opt.get_port(i_p_n) is None:
                _ktn_cor_node.NGObjOpt(node_opt.ktn_obj).create_port_by_data(
                    i_p_n, i_p_r
                )

        connect_fnc_()

    @classmethod
    def create_image_fnc(cls, *args, **kwargs):
        if kwargs['nodeType'] == 'ArnoldShadingNode':
            node_opt = _ktn_cor_node.NGObjOpt(kwargs['node'])
            if node_opt.get('nodeType') in ['image']:
                cls._create_image_(node_opt)

    @classmethod
    def _create_image_(cls, node_opt):
        """
        # coding:utf-8
        import lxkatana

        lxkatana.set_reload()

        from lxkatana import ktn_core

        ktn_core.ArnoldEventMtd._create_image_(
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
                        _key, 'getParent().{}'.format(_key)
                    )
                    return True
                elif _parent_type == 'ShadingGroup':
                    ___parent_opt = _parent_opt.get_parent_opt()
                    if ___parent_opt.get_type() == 'NetworkMaterialCreate':
                        if not ___parent_opt.get(_key):
                            return False
                        #
                        node_opt.set_expression(
                            _key, 'getParent().getParent().{}'.format(_key)
                        )
                        return True

        def post_connect_fnc_():
            _key = cls.DIRECTORY_KEY
            #
            if not node_opt.get(cls.DIRECTORY_KEY):
                return False
            #
            if not node_opt.get('parameters.filename.value'):
                node_opt.set(
                    'parameters.filename.enable', 1
                )
                node_opt.set_expression(
                    'parameters.filename.value', '{}+\'/tx\'+\'/texture_name.<udim>.tx\''.format(_key)
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
                _ktn_cor_node.NGObjOpt(node_opt.ktn_obj).create_port_by_data(
                    i_p_n, i_p_r
                )
        #
        connect_fnc_()
        #
        timer = threading.Timer(1, post_connect_fnc_)
        timer.start()


class CallbackMtd(object):
    @classmethod
    def set_scene_load(cls, *args, **kwargs):
        # {'filename': '/data/f/event_test.katana', 'objectHash': None}
        file_path = kwargs['filename']
        _ = NodegraphAPI.GetAllNodesByType('ArnoldShadingNode') or []

        for ktn_obj in _:
            ktn_obj_opt = _ktn_cor_node.NGObjOpt(ktn_obj)
            shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
            if shader_type_name in ['ramp_rgb', 'ramp_float']:
                # noinspection PyBroadException
                try:
                    EventMtd.set_arnold_ramp_write(ktn_obj_opt)
                except Exception:
                    print ktn_obj_opt.name

    @classmethod
    def add_arnold_callbacks(cls):
        ss = [
            (cls.set_scene_load, Callbacks.Type.onSceneLoad),
        ]
        for function, callback_type in ss:
            callback_opt = CallbackOpt(function=function, callback_type=callback_type)
            callback_opt.set_add()

    @classmethod
    def add_callbacks(cls, data):
        for function, callback_type in data:
            pass

    @classmethod
    def add_as_startup_complete(cls, fnc):
        callback_opt = CallbackOpt(function=fnc, callback_type=Callbacks.Type.onStartupComplete)
        callback_opt.set_add()

    @classmethod
    def add_as_scene_new(cls, fnc):
        callback_opt = CallbackOpt(function=fnc, callback_type=Callbacks.Type.onNewScene)
        callback_opt.set_add()

    @classmethod
    def add_as_scene_open(cls, fnc):
        callback_opt = CallbackOpt(function=fnc, callback_type=Callbacks.Type.onSceneLoad)
        callback_opt.set_add()

    @classmethod
    def add_as_scene_save(cls, fnc):
        callback_opt = CallbackOpt(function=fnc, callback_type=Callbacks.Type.onSceneSave)
        callback_opt.set_add()

    @classmethod
    def add_as_render_setup(cls, fnc):
        callback_opt = CallbackOpt(function=fnc, callback_type=Callbacks.Type.onRenderSetup)
        callback_opt.set_add()


class VariablesSetting(object):
    def __init__(self):
        self._ktn_obj = NodegraphAPI.GetNode('rootNode')

    def set(self, key, value):
        port_path = 'variables.{}.options'.format(key)
        p = self._ktn_obj.getParameter(port_path)
        if p is None:
            pass
        _ktn_cor_node.NGPortOpt(p).set(value)

    def get(self, key):
        pass

    def get_branches(self, key):
        p = self._ktn_obj.getParameter('variables.{}.options'.format(key))
        if p:
            return _ktn_cor_node.NGPortOpt(p).get()
        return []

    def set_register(self, key, values):
        ktn_port = self._ktn_obj.getParameter('variables')
        group_ktn_port = ktn_port.getChild(key)
        if group_ktn_port is not None:
            ktn_port.deleteChild(group_ktn_port)
            _ = _ktn_cor_node.NGObjOpt(self._ktn_obj).get_port_raw('variables.{}.value'.format(key))
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
            i_key = _ktn_cor_node.NGPortOpt(i).name
            i_values = _ktn_cor_node.NGPortOpt(
                self._ktn_obj.getParameter('variables.{}.options'.format(i_key))
            ).get()
            dic[i_key] = i_values
        return dic


class WorkspaceSetting(object):
    def __init__(self):
        self._cfg = bsc_objects.Configure(
            value=bsc_core.CfgFileMtd.get_yaml(
                'katana/script/scene'
            )
        )
        self._cfg.set_flatten()
        self._obj_opt = _ktn_cor_node.NGObjOpt(NodegraphAPI.GetNode('rootNode'))

    def setup(self):
        # self._obj_opt.clear_ports(self._cfg.get('main.clear_start'))
        self._obj_opt.create_ports_by_data(
            self._cfg.get('main.ports')
        )

    def build_env_ports(self):
        root = self._cfg.get('main.environment.root')
        if self._obj_opt.get_port_is_exists(root) is False:
            # self._obj_opt.clear_ports(root)
            self._obj_opt.create_ports_by_data(
                self._cfg.get('main.environment.ports')
            )

    def save_env(self, index, key, env_key, env_value):
        root = self._cfg.get('main.environment.root')
        self._obj_opt.set(
            '{}.data_{}.i0'.format(root, index), key, ignore_changed=True
        )
        self._obj_opt.set(
            '{}.data_{}.i1'.format(root, index), env_key, ignore_changed=True
        )
        self._obj_opt.set(
            '{}.data_{}.i2'.format(root, index), env_value, ignore_changed=True
        )

    def get_env_data(self):
        data = []
        root = self._cfg.get('main.environment.root')
        for i_index in range(20):
            i_key = self._obj_opt.get(
                '{}.data_{}.i0'.format(root, i_index)
            )
            i_env_key = self._obj_opt.get(
                '{}.data_{}.i1'.format(root, i_index)
            )
            i_env_value = self._obj_opt.get(
                '{}.data_{}.i2'.format(root, i_index)
            )
            if i_key and i_env_key and i_env_value:
                data.append(
                    (i_key, i_env_key, i_env_value)
                )
        return data

    def get_task_kwargs(self):
        dict_ = {}
        data = self.get_env_data()
        for i_index, (i_key, i_env_key, i_env_value) in enumerate(data):
            dict_[i_key] = i_env_value
        return dict_

    def build_look_ports(self):
        root = self._cfg.get('main.look.root')
        if self._obj_opt.get_port_is_exists(root) is False:
            # self._obj_opt.clear_ports(root)
            self._obj_opt.create_ports_by_data(
                self._cfg.get('main.look.ports')
            )
    @classmethod
    def get_look_output_nodes(cls):
        return _ktn_cor_node.NGObjsMtd.find_nodes(
            type_name='LookFileBake', ignore_bypassed=True
        )
    @classmethod
    def get_look_output_node_opts(cls):
        return [
            _ktn_cor_node.NGObjOpt(i) for i in cls.get_look_output_nodes()
        ]

    def set_current_look_output(self, node_name):
        root = self._cfg.get('main.look.root')
        self._obj_opt.set(
            '{}.output'.format(root), node_name
        )

    def get_current_look_output(self):
        root = self._cfg.get('main.look.root')
        return self._obj_opt.get(
            '{}.output'.format(root)
        )

    def get_current_look_output_opt(self):
        _ = self.get_current_look_output()
        if _:
            if _ktn_cor_node.NGObjOpt._get_is_exists_(_):
                return _ktn_cor_node.NGObjOpt(_)

    def update_current_look_output_with_dialog(self):
        if get_is_ui_mode():
            opts = self.get_look_output_node_opts()
            if opts:
                if len(opts) > 1:
                    def yes_fnc_():
                        _n = o.get('dcc.node')
                        self.set_current_look_output(_n)
                    #
                    w = utl_core.DialogWindow.set_create(
                        'Workspace Setting',
                        content=(
                            'More then one "LookFileBake" in scene:\n'
                            '   1, choose one use as current\n'
                            '   2, press "Confirm" to continue'
                        ),
                        status=utl_core.DialogWindow.ValidatorStatus.Warning,
                        options_configure=self._cfg.get('main.look.dialog_options'),
                        #
                        yes_method=yes_fnc_,
                        #
                        yes_label='Confirm',
                        #
                        no_visible=False, cancel_visible=False,
                        show=False,
                        window_size=(480, 240)
                    )

                    o = w.get_options_node()

                    o.set('dcc.node', [i.get_name() for i in opts])

                    w.set_window_show()

                    if w.get_result() is True:
                        return self.get_current_look_output()
                else:
                    name = opts[0].get_name()
                    self.set_current_look_output(name)
                    return name

    def get_current_look_output_opt_force(self):
        opt = self.get_current_look_output_opt()
        if opt is not None:
            return opt
        else:
            opts = self.get_look_output_node_opts()
            if opts:
                if len(opts) > 1:
                    if get_is_ui_mode():
                        def yes_fnc_():
                            _n = o.get('dcc.node')
                            self.set_current_look_output(_n)
                        #
                        w = utl_core.DialogWindow.set_create(
                            'Workspace Setting',
                            content=(
                                'More then one "LookFileBake" in scene:\n'
                                '   1, choose one use as current\n'
                                '   2, press "Confirm" to continue'
                            ),
                            status=utl_core.DialogWindow.ValidatorStatus.Warning,
                            options_configure=self._cfg.get('main.look.dialog_options'),
                            #
                            yes_method=yes_fnc_,
                            #
                            yes_label='Confirm',
                            #
                            no_visible=False, cancel_visible=False,
                            show=False,
                            window_size=(480, 240)
                        )

                        o = w.get_options_node()

                        o.set('dcc.node', [i.get_name() for i in opts])

                        w.set_window_show()

                        if w.get_result() is True:
                            return self.get_current_look_output_opt()
                    else:
                        return opts[0]
                else:
                    return opts[0]


class LayoutNodeHotKey(object):
    """
# coding:utf-8
import lxkatana
lxkatana.set_reload()

from lxkatana import ktn_core

ktn_core.LayoutNodeHotKey().register()
    """
    NAME = 'Layout Node'
    ID = 'F4331532-D52B-11ED-8C7C-2CFDA1C062BB'
    HOT_KEY = 'Alt+L'

    def __init__(self):
        self._ktn_gui = App.Tabs.FindTopTab('Node Graph')

    def press_fnc(self, *args, **kwargs):
        pass
    @classmethod
    def _release_fnc_(cls, ktn_gui):
        ss = NodegraphAPI.GetAllSelectedNodes()
        if ss:
            group = ktn_gui.getEnteredGroupNode()
            if group.getType() in {'NetworkMaterialCreate', 'ShadingGroup'}:
                ss_ = [i_s for i_s in ss if i_s.getParent() == group]
                _ktn_cor_node.NGGuiLayout(
                    ss_
                ).layout_shader_graph(
                    size=(320, 320)
                )

    def release_fnc(self, *args, **kwargs):
        ktn_gui = args[0]
        self._release_fnc_(ktn_gui)

    def register(self):
        self._ktn_gui.registerKeyboardShortcut(
            self.ID, self.NAME, self.HOT_KEY, self.press_fnc, self.release_fnc
        )