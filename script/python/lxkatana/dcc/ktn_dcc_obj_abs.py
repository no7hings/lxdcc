# coding:utf-8
# noinspection PyUnresolvedReferences
import NodegraphAPI
# noinspection PyUnresolvedReferences
from Katana import CacheManager

from lxbasic import bsc_core

from lxobj import obj_configure, obj_core

from lxutil import utl_core, utl_abstract

from lxkatana import ktn_core

from lxkatana.modifiers import _ktn_mdf_utility

import lxbasic.objects as bsc_objects


class AbsKtnPort(utl_abstract.AbsDccPort):
    PATHSEP = '.'
    def __init__(self, node, name, port_assign):
        super(AbsKtnPort, self).__init__(node, name, port_assign)

    def _get_ktn_port_(self):
        if self.port_assign == obj_configure.PortAssign.VARIANTS:
            return NodegraphAPI.GetNode(self.obj.name).getParameter(self.port_path)
        elif self.port_assign == obj_configure.PortAssign.INPUTS:
            return NodegraphAPI.GetNode(self.obj.name).getInputPort(self.port_path)
        elif self.port_assign == obj_configure.PortAssign.OUTPUTS:
            return NodegraphAPI.GetNode(self.obj.name).getOutputPort(self.port_path)
        raise TypeError()

    def get_ktn_obj(self):
        return self.obj.ktn_obj
    @property
    def ktn_obj(self):
        return self.obj.ktn_obj
    @property
    def ktn_port(self):
        return self._get_ktn_port_()
    @property
    def type(self):
        ktn_port = self._get_ktn_port_()
        if ktn_port is not None:
            return ktn_port.getType()
        return ''

    def get_is_exists(self):
        ktn_port = self._get_ktn_port_()
        return ktn_port is not None

    def set_create(self, *args):
        ktn_port = self._get_ktn_port_()
        parent = obj_core.PortPathMethod.get_dag_parent(
            path=self._port_path, pathsep=self.PATHSEP
        )
        if ktn_port is None:
            utl_core.Log.set_module_result_trace(
                'port create',
                'atr-path="{}"'.format(self.path)
            )
            if self.port_assign == obj_configure.PortAssign.VARIANTS:
                if parent is not None:
                    parent_ktn_port = self.ktn_obj.getParameter(parent)
                else:
                    parent_ktn_port = self.ktn_obj.getParameters()
                #
                if parent_ktn_port is not None:
                    type_, value = args[:2]
                    if type_ == 'string':
                        parent_ktn_port.createChildString(self.port_name, str(value))
            elif self.port_assign == obj_configure.PortAssign.INPUTS:
                return self.ktn_obj.addInputPort(self.port_name)
            elif self.port_assign == obj_configure.PortAssign.OUTPUTS:
                return self.ktn_obj.addOutputPort(self.port_name)

    def set_attributes(self, attributes):
        ktn_port = self._get_ktn_port_()
        if ktn_port is not None:
            attributes_ = ktn_port.getAttributes()
            attributes_.update(attributes)
            ktn_port.setAttributes(attributes_)

    def get_dcc_instance(self):
        ktn_port = self._get_ktn_port_()
        if ktn_port is None:
            ktn_port = self.set_create()
            return ktn_port, True
        return ktn_port, False

    def get(self, time=0):
        ktn_port = self._get_ktn_port_()
        if ktn_port is not None:
            children = ktn_port.getChildren() or []
            if children:
                return [i.getValue(time) for i in children]
            else:
                return ktn_port.getValue(time)

    def set(self, value, time=0):
        ktn_port = self._get_ktn_port_()
        if ktn_port is not None:
            if isinstance(value, (tuple, list)):
                self._set_array_value_(ktn_port, value, time=time)
                # utl_core.Log.set_module_result_trace(
                #     'array-port-set',
                #     u'atr-path="{}" value="{}"'.format(self.path, value)
                # )
            else:
                _value = value
                if isinstance(value, unicode):
                    _value = str(value)
                #
                ktn_port.setValue(_value, time)
                # utl_core.Log.set_module_result_trace(
                #     'constant-port-set',
                #     u'atr-path="{}" value="{}"'.format(self.path, _value)
                # )

    def set_expression(self, expression):
        self.ktn_port.setExpression(expression)
    @classmethod
    def _set_array_value_(cls, ktn_port, value, time=0):
        size = len(value)
        ktn_port.resizeArray(size)
        [ktn_port.getChildByIndex(i).setValue(value[i], time) for i in range(size)]
    @classmethod
    def _set_connect_(cls, source, target, validation=False):
        if validation is True:
            ktn_source = source.ktn_port
            ktn_target = target.ktn_port
            if ktn_source is not None and ktn_target is not None:
                ktn_source.connect(ktn_target)
                utl_core.Log.set_module_result_trace(
                    'port-connect',
                    'connection="{} >> {}"'.format(
                        source.path, target.path
                    )
                )
        else:
            source.ktn_port.connect(target.ktn_port)
            utl_core.Log.set_module_result_trace(
                'port-connect',
                'connection="{} >> {}"'.format(
                    source.path, target.path
                )
            )
    @classmethod
    def _set_disconnect_(cls, source, target):
        if source.ktn_port is not None and target.ktn_port is not None:
            source.ktn_port.disconnect(target.ktn_port)
            utl_core.Log.set_module_result_trace(
                'port-disconnect',
                'connection="{} >> {}"'.format(
                    source.path, target.path
                )
            )

    def set_execute(self):
        NodegraphAPI.UserParameters.ExecuteButton(
            self.get_ktn_obj(), self.port_path
        )

    def get_source(self):
        ktn_output_ports = self.ktn_port.getConnectedPorts()
        if ktn_output_ports:
            ktn_source = ktn_output_ports[0]
            ktn_obj = ktn_source.getNode()
            #
            obj = self.obj.__class__(ktn_obj.getName())
            port_name = ktn_source.getName()
            # debug
            if ktn_source.getNode().getOutputPort(port_name) is None:
                return obj.get_input_port(
                    port_name
                ).get_source()
            return obj.get_output_port(
                port_name
            )

    def set_source(self, output_port, validation=False):
        self._set_connect_(output_port, self, validation)

    def set_disconnect(self):
        if self.port_assign == obj_configure.PortAssign.INPUTS:
            source = self.get_source()
            if source is not None:
                self._set_disconnect_(source, self)
        elif self.port_assign == obj_configure.PortAssign.OUTPUTS:
            targets = self.get_targets()
            for i_target in targets:
                self._set_disconnect_(self, i_target)

    def get_targets(self):
        lis = []
        input_ktn_ports = self.ktn_port.getConnectedPorts()
        if input_ktn_ports:
            for i_input_ktn_port in input_ktn_ports:
                i_ktn_obj = i_input_ktn_port.getNode()
                i_obj = self.obj.__class__(i_ktn_obj.getName())
                lis.append(
                    i_obj.get_input_port(i_input_ktn_port.getName())
                )
        return lis

    def set_target(self, input_port, force=False, validation=False):
        if force is True:
            input_port.set_create()
        #
        self._set_connect_(self, input_port, validation=validation)

    def _set_port_dag_create_(self, port_path):
        port_assign = self.port_assign
        return self.__class__(self.obj, port_path, port_assign)

    def get_children(self):
        lis = []
        _ = self.ktn_port.getChildren()
        for i in _:
            lis.append(
               self.get_child(i.getName())
            )
        return lis

    def get_child(self, port_name):
        _ = [i.getName() for i in self.ktn_port.getChildren()]
        if port_name in _:
            port_path = self.PATHSEP.join([self.port_path, port_name])
            return self._set_port_dag_create_(port_path)

    def set_update(self):
        self._get_ktn_port_()


class AbsKtnObj(utl_abstract.AbsDccObj):
    PATHSEP = '/'
    CONNECTION_CLASS = None
    def __init__(self, path):
        if not path.startswith(self.PATHSEP):
            path = self._get_ktn_obj_path_(path)
        else:
            path = path
        super(AbsKtnObj, self).__init__(path)
    @property
    def type(self):
        ktn_obj = NodegraphAPI.GetNode(self.name)
        if ktn_obj is not None:
            return ktn_obj.getType()
        return ''
    @property
    def icon(self):
        return utl_core.Icon.get_katana_obj()
    @property
    def ktn_obj(self):
        return self._get_ktn_obj_()

    def _get_ktn_obj_(self):
        return NodegraphAPI.GetNode(self.name)

    def set_create(self, obj_type_name):
        ktn_obj = self._get_ktn_obj_()
        if ktn_obj is None:
            parent = self.get_parent()
            parent_ktn_obj = parent.ktn_obj
            if parent_ktn_obj is not None:
                ktn_obj = NodegraphAPI.CreateNode(obj_type_name, parent_ktn_obj)
                if ktn_obj is None:
                    raise TypeError('unknown-obj-type: "{}"'.format(obj_type_name))
                name_ktn_port = ktn_obj.getParameter('name')
                if name_ktn_port is not None:
                    name_ktn_port.setValue(self.name, 0)
                #
                ktn_obj.setName(self.name)
                utl_core.Log.set_module_result_trace(
                    'obj create',
                    'obj="{}", type="{}"'.format(self.path, self.type)
                )
                return ktn_obj

    def set_ktn_type(self, type_name):
        ktn_obj = self._get_ktn_obj_()
        if ktn_obj is not None:
            type_ktn_port = ktn_obj.getParameter('nodeType')
            if type_ktn_port is not None:
                type_ktn_port.setValue(type_name, 0)

    def get_dcc_instance(self, obj_type_name, base_obj_type_name=None, *args, **kwargs):
        ktn_obj = NodegraphAPI.GetNode(self.name)
        if ktn_obj is None:
            ktn_obj = self.set_create(obj_type_name)
            return ktn_obj, True
        else:
            exists_obj_type_name = ktn_obj.getType()
            if base_obj_type_name is not None:
                check_exists_obj_type_name = base_obj_type_name
            else:
                check_exists_obj_type_name = obj_type_name
            #
            if exists_obj_type_name != check_exists_obj_type_name:
                self.set_delete()
                ktn_obj = self.set_create(obj_type_name)
                return ktn_obj, True
        return ktn_obj, False

    def get_is_file_reference(self):
        pass

    def get_is_exists(self):
        return NodegraphAPI.GetNode(self.name) is not None
    @classmethod
    def _get_ktn_obj_path_args_(cls, name):
        def _rcs_fnc(name_):
            _ktn_obj = NodegraphAPI.GetNode(name_)
            if _ktn_obj is not None:
                _parent = _ktn_obj.getParent()
                if _parent is None:
                    lis.append('')
                else:
                    _parent_name = _parent.getName()
                    lis.append(_parent_name)
                    _rcs_fnc(_parent_name)
        #
        lis = [name]
        _rcs_fnc(name)
        lis.reverse()
        return lis
    @classmethod
    def _get_ktn_obj_path_(cls, name):
        return cls.PATHSEP.join(cls._get_ktn_obj_path_args_(name))

    def _set_dag_create_(self, path):
        return self.__class__(path)

    def get_descendant_paths(self):
        def _rcs_fnc(lis_, path_):
            lis_.append(path_)
            _name = path_.split(pathsep)[-1]
            _ktn_obj = NodegraphAPI.GetNode(_name)
            if hasattr(_ktn_obj, 'getChildren'):
                _ = _ktn_obj.getChildren() or []
                if _:
                    for _i in _:
                        _i_path = '{}{}{}'.format(self.path, pathsep, _i.getName())
                        _rcs_fnc(lis_, _i_path)
        lis = []
        pathsep = self.pathsep
        _rcs_fnc(lis, self.name)
        return lis

    def get_child_paths(self):
        lis = []
        ktn_obj = self._get_ktn_obj_()
        if ktn_obj is not None:
            if hasattr(ktn_obj, 'getChildren'):
                _ = ktn_obj.getChildren() or []
                for i in _:
                    lis.append('{}{}{}'.format(self.path, self.pathsep, i.getName()))
        return lis

    def _set_child_create_(self, path):
        return self.__class__(path)

    def set_delete(self):
        ktn_obj = NodegraphAPI.GetNode(self.name)
        if ktn_obj is not None:
            ktn_obj.delete()
            utl_core.Log.set_module_result_trace(
                'obj-delete',
                '"{}"'.format(self.path)
            )

    def set_rename(self, new_name):
        ktn_obj = NodegraphAPI.GetNode(self.name)
        if ktn_obj is not None:
            name_ktn_port = ktn_obj.getParameter('name')
            if name_ktn_port is not None:
                name_ktn_port.setValue(new_name, 0)
            ktn_obj.setName(new_name)
            return self.__class__(new_name)

    def set_children_clear(self):
        [i.set_delete() for i in self.get_children()]

    def get_source_ktn_connections(self):
        lis = []
        ktn_obj = self._get_ktn_obj_()
        _ = ktn_obj.getInputPorts() or []
        for target_ktn_port in _:
            source_ktn_ports = target_ktn_port.getConnectedPorts()
            if source_ktn_ports:
                for source_ktn_port in source_ktn_ports:
                    lis.append((target_ktn_port, source_ktn_port))
        return lis

    def _get_source_connection_raw_(self):
        lis = []
        ktn_obj = self._get_ktn_obj_()
        _ = ktn_obj.getInputPorts() or []
        for target_ktn_port in _:
            source_ktn_ports = target_ktn_port.getConnectedPorts()
            if source_ktn_ports:
                for source_ktn_port in source_ktn_ports:
                    source_obj_name = source_ktn_port.getNode().getName()
                    source_port_name = source_ktn_port.getName()
                    source_atr_path = bsc_core.AtrPathMtd.get_atr_path(
                        source_obj_name, source_port_name
                    )
                    target_obj_name = target_ktn_port.getNode().getName()
                    target_port_name = target_ktn_port.getName()
                    target_atr_path = bsc_core.AtrPathMtd.get_atr_path(
                        target_obj_name, target_port_name
                    )
                    lis.append((source_atr_path, target_atr_path))
        return lis

    def get_target_connections(self):
        lis = []
        ktn_obj = self._get_ktn_obj_()
        _ = ktn_obj.getOutputPorts() or []
        for source_ktn_port in _:
            target_ktn_ports = source_ktn_port.getConnectedPorts()
            if target_ktn_ports:
                for target_ktn_port in target_ktn_ports:
                    source_ktn_obj = source_ktn_port.getNode()
                    target_ktn_obj = target_ktn_port.getNode()
                    source_port = self.__class__(source_ktn_obj.getName()).get_output_port(source_ktn_port.getName())
                    target_port = self.__class__(target_ktn_obj.getName()).get_input_port(target_ktn_port.getName())
                    lis.append(self.CONNECTION_CLASS(source_port, target_port))
        return lis
    #
    def get_sources(self):
        pass
    @_ktn_mdf_utility.set_undo_mark_mdf
    def set_source_objs_layout(self, layout=('r-l', 't-b'), size=(320, 960)):
        def rcs_fnc_(obj_, column_):
            _source_objs = obj_.get_source_objs()
            if _source_objs:
                _ktn_obj = obj_.ktn_obj
                column_ += 1
                if column_ not in ktn_obj_in_column_dict:
                    _i_ktn_objs = []
                    ktn_obj_in_column_dict[column_] = _i_ktn_objs
                else:
                    _i_ktn_objs = ktn_obj_in_column_dict[column_]
                #
                for _row, _i in enumerate(_source_objs):
                    _i_ktn_obj = _i.ktn_obj
                    if not _i_ktn_obj in ktn_obj_stack:
                        ktn_obj_stack.append(_i_ktn_obj)
                        _i_ktn_objs.append(_i_ktn_obj)
                        rcs_fnc_(_i, column_)
        #
        ktn_obj = self.ktn_obj
        ktn_obj_stack = []
        ktn_obj_in_column_dict = {}
        #
        ktn_parent = ktn_obj.getParent()
        #
        layout_x, layout_y = layout
        x, y = NodegraphAPI.GetNodePosition(ktn_obj)
        w, h = size
        rcs_fnc_(self, 0)
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
                    for j_seq, j_ktn_obj in enumerate(v):
                        i_x = s_x
                        if layout_y == 't-b':
                            i_y = s_y-j_seq*h
                        elif layout_y == 'b-t':
                            i_y = s_y+j_seq*h
                        else:
                            raise ValueError()
                        #
                        j_atr = dict(
                            x=i_x,
                            y=i_y,
                        )
                        j_atr_ = j_ktn_obj.getAttributes()
                        j_atr_.update(j_atr)
                        j_ktn_parent = j_ktn_obj.getParent()
                        if j_ktn_parent.getName() == ktn_parent.getName():
                            j_ktn_obj.setAttributes(j_atr_)
            #
            utl_core.Log.set_module_result_trace(
                'network-layout',
                'obj="{}"'.format(self.path)
            )

    def set_source_objs_colour(self):
        source_objs = self.get_all_source_objs()
        for obj in source_objs:
            obj.set_colour_by_type_name()

    def get_position(self):
        ktn_obj = self._get_ktn_obj_()
        return NodegraphAPI.GetNodePosition(ktn_obj)

    def set_sources_disconnect(self):
        ktn_connections = self.get_source_ktn_connections()
        for s_ktn_obj, t_ktn_obj in ktn_connections:
            s_ktn_obj.disconnect(t_ktn_obj)

    def get_properties(self, keys):
        dic = {}
        for key in keys:
            port = self.get_port(key)
            if port.get_is_exists() is True:
                dic[key] = port.get()
            else:
                utl_core.Log.set_module_warning_trace(
                    'property-get',
                    'port: "{}" is Non-exists'.format(port.path)
                )
        return dic

    def set_properties(self, dic):
        for k, v in dic.items():
            port = self.get_port(k)
            if port.get_is_exists() is True:
                port.set(v)
                utl_core.Log.set_module_result_trace(
                    'property-set',
                    'port: "{}" >> "{}"'.format(port.path, v)
                )
            else:
                utl_core.Log.set_module_warning_trace(
                    'property-set',
                    'port: "{}" is Non-exists'.format(port.path)
                )

    def get_input_ports(self):
        _ = self.ktn_obj.getInputPorts() or []
        return [self.get_input_port(i.getName()) for i in _]

    def set_colour_by_type_name(self):
        type_name = self.type_name
        r, g, b = bsc_core.TextOpt(type_name).to_rgb(maximum=1)
        attributes = self.ktn_obj.getAttributes()
        attributes['ns_colorr'] = r
        attributes['ns_colorg'] = g
        attributes['ns_colorb'] = b
        self.ktn_obj.setAttributes(attributes)

    def get_leaf_ports(self):
        def rcs_fnc_(ktn_port_, parent_port_path):
            _port_name = ktn_port_.getName()
            if parent_port_path is not None:
                _port_path = port_pathsep.join([parent_port_path, _port_name])
            else:
                _port_path = _port_name
            _children = ktn_port_.getChildren()
            if _children:
                for _child in _children:
                    rcs_fnc_(_child, _port_path)
            else:
                _type = ktn_port_.getType()
                if _type != 'group':
                    lis.append(
                        self.get_port(_port_path)
                    )
        #
        lis = []
        port_pathsep = self.PORT_CLASS.PATHSEP
        root_ktn_port = self.ktn_obj.getParameters()
        for i in root_ktn_port.getChildren():
            rcs_fnc_(i, None)

        return lis

    def get_attributes(self):
        attributes = bsc_objects.Properties(self)
        ports = self.get_leaf_ports()
        for port in ports:
            attributes.set(
                port.port_path, port.get()
            )
        return attributes

    def set_attributes(self):
        pass

    def __get_ktn_port_(self, port_path):
        return NodegraphAPI.GetNode(self.path).getParameter(port_path)
    @_ktn_mdf_utility.set_undo_mark_mdf
    def set_customize_attributes_create(self, attributes):
        ktn_core.NGObjCustomizePortOpt(self._get_ktn_obj_()).set_ports_add(attributes)

    def set_input_port_add(self, port_path):
        ktn_obj = self._get_ktn_obj_()
        _ = ktn_obj.getInputPort(port_path)
        if _ is None:
            self.ktn_obj.addInputPort(port_path)

    def set_output_port_add(self, port_path):
        ktn_obj = self._get_ktn_obj_()
        _ = ktn_obj.getOutputPort(port_path)
        if _ is None:
            self.ktn_obj.addOutputPort(port_path)


class AbsKtnObjs(utl_abstract.AbsDccObjs):
    def __init__(self, *args):
        pass
    @classmethod
    def _set_pre_run_(cls):
        pass
    @classmethod
    def get_paths(cls, **kwargs):
        cls._set_pre_run_()
        #
        lis = []
        for i in cls.INCLUDE_DCC_TYPES:
            _ = NodegraphAPI.GetAllNodesByType(i) or []
            for ktn_node in _:
                obj_path = cls.DCC_OBJ_CLASS._get_ktn_obj_path_(ktn_node.getName())
                lis.append(obj_path)
        return lis


class AbsKtnObjConnection(utl_abstract.AbsDccObjConnection):
    def __init__(self, source, target):
        super(AbsKtnObjConnection, self).__init__(source, target)


class AbsKtnFileReferenceObj(
    AbsKtnObj,
    utl_abstract.AbsFileReferenceDef
):
    def __init__(self, path, file_path=None):
        super(AbsKtnFileReferenceObj, self).__init__(path)
        # init file reference
        self._set_file_reference_def_init_(file_path)

    def get_is_file_reference(self):
        return True

    def get_is_multiply_reference(self):
        return False


class AbsSGKtnObj(utl_abstract.AbsDccObj):
    def __init__(self, path):
        pass

    @property
    def type(self):
        return ''

    @property
    def icon(self):
        pass

    def get_is_file_reference(self):
        pass

    def get_is_exists(self):
        pass
