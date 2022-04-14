# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.api.OpenMaya as om2

from lxbasic import bsc_core

from lxutil import utl_abstract, utl_core

from lxutil_gui.qt import utl_gui_qt_core

from lxmaya import ma_configure, ma_core


class ObjPortsOpt(object):
    def __init__(self, obj_path):
        self._obj_path = obj_path

    def get_port_names(self):
        return cmds.listAttr(
            self._obj_path, read=1, write=1, inUse=1, multi=1
        ) or []
    @classmethod
    def _get_ports_raw_(cls, obj_path, port_names):
        lis = []
        #
        if port_names:
            for port_name in port_names:
                print port_name
        return lis


class ObjAtrSetter(object):
    pass


class AbsMyaPort(utl_abstract.AbsDccPort):
    PATHSEP = ma_configure.Util.PORT_PATHSEP
    def __init__(self, obj, path, port_assign=None):
        super(AbsMyaPort, self).__init__(obj, path, port_assign=port_assign)
        self._obj_atr_query = ma_core.CmdAtrQueryOpt(self.path)
    @property
    def type(self):
        if self.get_is_exists() is True:
            return cmds.getAttr(self.path, type=True)
        elif self.get_query_is_exists() is True:
            return self._obj_atr_query.type
    @property
    def data_type(self):
        if self._obj_atr_query.get_is_exists() is True:
            return self._obj_atr_query.type
        return ''
    @property
    def port_query(self):
        return self._obj_atr_query

    def get_is_exists(self):
        return cmds.objExists(self.path)

    def get_query_is_exists(self):
        return self._obj_atr_query.get_is_exists()

    def set_create(self, raw_type, default_raw=None):
        if self.get_is_exists() is False:
            if raw_type == 'string':
                cmds.addAttr(
                    self.obj.path,
                    longName=self.name,
                    dataType=raw_type
                )
            else:
                cmds.addAttr(
                    self.obj.path,
                    longName=self.name,
                    attributeType=raw_type
                )
            if default_raw is not None:
                self.set(default_raw)

    def get(self, as_string=False):
        if self.type == 'message':
            return None
        if self.get_is_exists() is True:
            if as_string is True:
                return cmds.getAttr(self.path, asString=True) or ''
            #
            _ = cmds.getAttr(self.path)
            if self.get_channel_names():
                return _[0]
            return _

    def get_enumerate_strings(self):
        if self.get_is_exists() is True:
            return ma_core.CmdPortOpt(self.obj.path, self.port_path).get_enumerate_strings()
        return []

    def get_is_value_changed(self):
        return self.get_default() != self.get()

    def get_default(self):
        _ = self._obj_atr_query.get_default()
        if self.type == 'bool':
            return bool(int(_))
        return _

    def set(self, value):
        if self.get_is_exists() is True:
            if self.get_has_source() is False:
                if self.type == 'string':
                    cmds.setAttr(self.path, value, type=self.type)
                elif self.type == 'enum':
                    if isinstance(value, (str, unicode)):
                        enumerate_strings = self._obj_atr_query.get_enumerate_strings()
                        index = enumerate_strings.index(value)
                        cmds.setAttr(self.path, index)
                    else:
                        cmds.setAttr(self.path, value)
                else:
                    if isinstance(value, (tuple, list)):
                        if self.type == 'matrix':
                            # ((1, 1, 1), ...)
                            if isinstance(value[0], (tuple, list)):
                                value = [j for i in value for j in i]
                            #
                            cmds.setAttr(self.path, value, type='matrix')
                        else:
                            cmds.setAttr(self.path, *value, clamp=1)
                    else:
                        # Debug ( Clamp Maximum or Minimum Value )
                        cmds.setAttr(self.path, value, clamp=1)
                #
                # utl_core.Log.set_module_result_trace(
                #     'port-set',
                #     u'atr-path="{}" value="{}"'.format(self.path, value)
                # )
            else:
                utl_core.Log.set_module_warning_trace(
                    'port-set',
                    'atr-path="{}" has source'.format(self.path)
                )

    def _set_as_array_(self, values):
        parent_path = self.get_parent_path()
        for seq, value in enumerate(values):
            parent_path_ = '{}[{}]'.format(parent_path, seq)
            atr_path = self.PATHSEP.join(
               [self.obj.path, parent_path_, self.port_name]
            )
            if self.type == 'string':
                cmds.setAttr(atr_path, value, type=self.type)
            else:
                if isinstance(value, (tuple, list)):
                    cmds.setAttr(atr_path, *value)
                else:
                    # Debug ( Clamp Maximum or Minimum Value )
                    cmds.setAttr(atr_path, value, clamp=1)
            #
            # utl_core.Log.set_module_result_trace(
            #     'port-set',
            #     'atr-path="{}" value="{}"'.format(self.path, value)
            # )

    def set_source(self, output_port, validation=False):
        self._set_connect_(output_port, self, validation=validation)

    def set_source_disconnect(self):
        source = self.get_source()
        if source:
            cmds.disconnectAttr(
                source.path, self.path
            )

    def get_source(self):
        _ = cmds.connectionInfo(
            self.path,
            sourceFromDestination=1
        )
        if _:
            a = bsc_core.DccAttrPathOpt(_)
            obj_path = a.obj_path
            port_path = a.port_path
            return self.obj.__class__(obj_path).get_port(port_path)

    def get_has_source(self):
        _ = cmds.connectionInfo(self.path, isExactDestination=1)
        if self.get_has_channels():
            if _ is True:
                return _
            return True in [i.get_has_source() for i in self.get_channels()]
        return _

    def set_target(self, input_port, validation=False):
        self._set_connect_(self, input_port, validation=validation)

    def get_has_targets(self):
        return cmds.connectionInfo(self.path, isExactSource=1)
    #
    def get_targets(self):
        lis = []
        _ = cmds.connectionInfo(
            self.path,
            destinationFromSource=1
        ) or []
        for i in _:
            a = bsc_core.DccAttrPathOpt(i)
            i_obj_path = a.obj_path
            i_port_path = a.port_path
            lis.append(
                self.obj.__class__(i_obj_path).get_port(i_port_path)
            )
        return lis
    # array
    def get_element_indices(self):
        return ma_core.CmdAtrQueryOpt(self.path).get_element_indices()
    # channel
    def get_channel_names(self, alpha=False):
        return ma_core.CmdAtrQueryOpt(self.path).get_channel_names(alpha=alpha)

    def get_has_channels(self, alpha=False):
        return self.get_channel_names(alpha=alpha) != []

    def get_channels_count(self, alpha=False):
        return len(self.get_channel_names(alpha=alpha))

    def get_alpha_channel_name(self):
        return ma_core.CmdAtrQueryOpt(self.path).get_alpha_channel_name()

    def get_alpha_channel(self):
        channel_name = self.get_alpha_channel_name()
        if channel_name is not None:
            return self.obj.get_port(channel_name)

    def get_has_alpha_channel(self):
        return self.get_alpha_channel_name() is not None

    def get_channels(self, alpha=False):
        lis = []
        if self.get_has_channels(alpha=alpha):
            channel_names = self.get_channel_names(alpha=alpha)
            for channel_name in channel_names:
                channel = self.obj.get_port(
                    '{}.{}'.format(self.port_path, channel_name)
                )
                lis.append(channel)
        return lis

    def get_channel_at(self, index, alpha=False):
        channels = self.get_channels(alpha=alpha)
        if index < len(channels):
            return channels[index]

    def get_is_channel(self):
        return self._obj_atr_query.get_is_channel()

    def get_parent_path(self):
        return self._obj_atr_query.get_parent_path()

    def get_parent(self):
        _ = self.get_parent_path()
        if _ is not None:
            return self.__class__(
                self.obj, _
            )
    @classmethod
    def _set_connect_(cls, source, target, validation=False):
        source_path, target_path = source.path, target.path
        if cmds.isConnected(source_path, target_path) is False:
            if validation is False:
                cmds.connectAttr(source_path, target_path, force=1)
            else:
                source_data_type, target_data_type = (
                    source.data_type,
                    target.data_type
                )
                if source_data_type == target_data_type:
                    cmds.connectAttr(source_path, target_path, force=1)
                else:
                    source_is_channel = source.get_is_channel()
                    source_has_channels = source.get_has_channels()
                    target_is_channel = target.get_is_channel()
                    target_has_channels = target.get_has_channels()
                    check = [source_is_channel, source_has_channels, target_is_channel, target_has_channels]
                    # port / channel >> port / channel
                    if check in [
                        # port >> port
                        [False, False, False, False],
                        # port >> channel
                        [False, False, True, False],
                        # channel >> channel
                        [True, False, True, False],
                        # channel >> port
                        [True, False, False, False],
                    ]:
                        if cmds.isConnected(source_path, target_path) is False:
                            cmds.connectAttr(source_path, target_path, force=1)
                            utl_core.Log.set_module_result_trace(
                                'port connect',
                                u'connection="{} >> {}"'.format(
                                    source_path,
                                    target_path
                                )
                            )
                    # port / channel >> [channel, channel, ...]
                    elif check in [
                        # port >> [channel, channel, ...]
                        [False, False, False, True],
                        # channel >> [channel, channel, ...]
                        [True, False, False, True],
                    ]:
                        target_channels = target.get_channels()
                        for target_channel in target_channels:
                            source_path, target_path = (
                                source.path, target_channel.path
                            )
                            if cmds.isConnected(source_path, target_path) is False:
                                cmds.connectAttr(source_path, target_path, force=1)
                                utl_core.Log.set_module_result_trace(
                                    'port connect',
                                    u'connection="{} >> {}"'.format(
                                        source_path, target_path
                                    )
                                )
                    # [channel, channel, ...] >> [channel, channel, ...]
                    elif check == [False, True, False, True]:
                        source_channels = source.get_channels()
                        for seq, source_channel in enumerate(source_channels):
                            target_channel = target.get_channel_at(seq)
                            if target_channel is not None:
                                source_path, target_path = (
                                    source_channel.path, target_channel.path
                                )
                                if cmds.isConnected(source_path, target_path) is False:
                                    cmds.connectAttr(source_path, target_path, force=1)
                                    utl_core.Log.set_module_result_trace(
                                        'port connect',
                                        u'connection="{} >> {}"'.format(
                                            source_path, target_path
                                        )
                                    )
                    # [channel, channel, ...] >> port / channel
                    elif check in [
                        # [channel, channel, ...] >> port
                        [False, True, False, False],
                        # [channel, channel, ...] >> channel
                        [False, True, True, False],
                    ]:
                        # alpha_channel = source.get_alpha_channel()
                        # if alpha_channel is not None:
                        #     source_channel = alpha_channel
                        # else:
                        #     source_channels = source.get_channels()
                        #     source_channel = source_channels[0]
                        #
                        source_channels = source.get_channels()
                        source_channel = source_channels[0]
                        #
                        source_path, target_path = (
                            source_channel.path, target.path
                        )
                        if cmds.isConnected(source_path, target_path) is False:
                            cmds.connectAttr(source_path, target_path, force=1)
                            utl_core.Log.set_module_result_trace(
                                'port connect',
                                u'connection="{} >> {}"'.format(
                                    source_path, target_path
                                )
                            )
                    else:
                        utl_core.Log.set_warning_trace(
                            'port connect',
                            u'connection="{} >> {}" is not available'.format(
                                source_path, target_path
                            )
                        )


class AbsMyaObjConnection(utl_abstract.AbsDccObjConnection):
    def __init__(self, source, target):
        super(AbsMyaObjConnection, self).__init__(source, target)


class AbsMaShapeDef(object):
    PATHSEP = None
    TRANSFORM_CLASS = None
    def _set_ma_shape_def_init_(self, shape_path):
        transform_path = self.PATHSEP.join(shape_path.split(self.PATHSEP)[:-1])
        self._transform = self.TRANSFORM_CLASS(transform_path)
    @property
    def transform(self):
        return self._transform


class AbsMaUuidDef(object):
    def _set_ma_uuid_def_(self, uuid):
        self._uuid = uuid
    @property
    def unique_id(self):
        return self._uuid
    @property
    def path(self):
        raise NotImplementedError()

    def set_unique_id(self, unique_id):
        if cmds.objExists(self.path):
            if not cmds.ls(unique_id, long=1):
                cmds.rename(self.path, unique_id, uuid=1)
                utl_core.Log.set_result_trace('set unique-id: "{}" >> "{}"'.format(self.path, unique_id))
            else:
                utl_core.Log.set_warning_trace('unique-id: "{}" is Exists'.format(unique_id))


class AbsMyaObj(
    utl_abstract.AbsDccObj,
    AbsMaUuidDef
):
    PATHSEP = ma_configure.Util.OBJ_PATHSEP
    def __init__(self, path):
        _ = path
        if cmds.objExists(_):
            uuid = cmds.ls(_, uuid=1)[0]
            path_arg = cmds.ls(_, long=1)[0]
        else:
            uuid = None
            path_arg = _
        #
        self._set_ma_uuid_def_(uuid)
        super(AbsMyaObj, self).__init__(path_arg)
    @property
    def type(self):
        if cmds.objExists(self.path) is True:
            return cmds.nodeType(self.path)
        return '*'
    @property
    def icon(self):
        return utl_gui_qt_core.QtMayaMtd.get_qt_icon(self.type)
    @classmethod
    def _get_full_path_(cls, path):
        if cmds.objExists(path) is True:
            if not path.startswith(ma_configure.Util.OBJ_PATHSEP):
                return cmds.ls(path, long=1)[0]
            return path
        return path

    def _set_path_update_(self):
        if self.unique_id:
            _ = cmds.ls(self.unique_id, long=1)
            if _:
                self._path = _[0]

    def get_is_exists(self):
        return cmds.objExists(self.path)

    def get_is_referenced(self):
        return cmds.referenceQuery(self.path, isNodeReferenced=1)

    def get_is_lock(self):
        return cmds.lockNode(self.path, query=1, lock=1) == [True]

    def set_unlock(self):
        cmds.lockNode(self.path, lock=0)
        cmds.warning('unlock node: {}'.format(self.path))
        utl_core.Log.set_result_trace(
            'unlock node: {}'.format(self.path)
        )

    def set_lock(self):
        cmds.lockNode(self.path, lock=1)
        cmds.warning('lock node: {}'.format(self.path))
    # noinspection PyUnusedLocal
    def set_delete(self, force=False):
        if self.get_is_exists() is True:
            if self.get_is_lock() is True:
                self.set_unlock()
            #
            cmds.delete(self.path)
            utl_core.Log.set_module_result_trace(
                'obj-delete',
                u'obj="{}"'.format(self.path)
            )

    def set_to_world(self):
        if self.get_is_exists() is True:
            cmds.parent(self.path, world=1)
    # noinspection PyUnusedLocal
    def set_rename(self, new_name, force=False):
        if self.get_is_exists() is True:
            cmds.rename(self.path, new_name)
            utl_core.Log.set_module_result_trace(
                'obj-rename',
                u'obj="{}" >> "{}"'.format(self.path, new_name)
            )

    def set_repath(self, new_obj_path):
        new_dcc_path_dag_opt = bsc_core.DccPathDagOpt(new_obj_path)
        new_dcc_parent_dag_opt = new_dcc_path_dag_opt.get_parent()
        new_parent_dcc_obj = self.__class__(new_dcc_parent_dag_opt.path)
        if new_parent_dcc_obj.get_is_exists() is True:
            self.set_parent(new_parent_dcc_obj)
            new_name = new_dcc_path_dag_opt.name
            if new_name != self.name:
                self._set_path_update_()
                self.set_rename(new_name)

    def get_is_file_reference(self):
        return False

    def set_boolean_attribute_add(self, port_path, value=False):
        attribute = self.get_port(port_path)
        attribute.set_create(raw_type='bool')
        attribute.set(value)
    # naming overlapped
    def get_is_naming_overlapped(self):
        return len(self.get_naming_overlapped_paths()) > 1

    def get_naming_overlapped_paths(self):
        return cmds.ls(self.name) or []
    # instance
    def get_is_instanced(self):
        dag_node = om2.MFnDagNode(om2.MGlobal.getSelectionListByName(self.path).getDagPath(0))
        return dag_node.isInstanced()
    # history
    def get_history_paths(self):
        return ma_core._ma_node__get_history_paths_(self.path)

    def set_history_clear(self):
        cmds.delete(self.path, constructionHistory=1)

    def get_source_node_paths(self, include_types=None):
        if include_types:
            lis = []
            for node_type in include_types:
                _ = cmds.listConnections(self.path, destination=0, source=1, type=node_type) or []
                for i in _:
                    lis.append(i)
            return lis
        return cmds.listConnections(self.path, destination=0, source=1) or []

    def get_target_node_paths(self, include_types=None):
        if include_types:
            lis = []
            for node_type in include_types:
                _ = cmds.listConnections(self.path, destination=1, source=0, type=node_type) or []
                for i in _:
                    lis.append(i)
            return lis
        return cmds.listConnections(self.path, destination=1, source=0) or []

    def set_ancestors_create(self):
        if self.path:
            if cmds.objExists(self.path) is False:
                paths = self.get_ancestor_paths()
                paths.reverse()
                #
                parent_string = None
                for i in paths:
                    name = i.split(self.PATHSEP)[-1]
                    if name:
                        if cmds.objExists(i) is False:
                            if parent_string is not None:
                                parent_string = cmds.group(empty=1, name=name, parent=parent_string)
                            else:
                                parent_string = cmds.group(empty=1, name=name)
                            #
                            utl_core.Log.set_module_result_trace(
                                'transform-obj-create',
                                u'obj-name="{}", parent-path="{}"'.format(name, parent_string)
                            )
                        else:
                            parent_string = i

    def set_dag_components_create(self):
        if self.path:
            if cmds.objExists(self.path) is False:
                paths = self.get_dag_component_paths()
                paths.reverse()
                #
                parent_string = None
                for i in paths:
                    name = i.split(self.PATHSEP)[-1]
                    if name:
                        if cmds.objExists(i) is False:
                            if parent_string is not None:
                                parent_string = cmds.group(empty=1, name=name, parent=parent_string)
                            else:
                                parent_string = cmds.group(empty=1, name=name)
                            #
                            utl_core.Log.set_module_result_trace(
                                'transform-obj-create',
                                u'obj-name="{}"'.format(name)
                            )
                        else:
                            parent_string = i

    def set_parent_path(self, parent_path, create_parent=False):
        if parent_path == self.PATHSEP:
            if cmds.listRelatives(self.path, parent=1):
                cmds.parent(self.path, world=1)
                utl_core.Log.set_module_result_trace(
                    'parent-set',
                    u'obj="{}"'.format(self.PATHSEP)
                )
        else:
            parent_obj = self.__class__(parent_path)
            self.set_parent(parent_obj, create_parent)

    def set_parent(self, parent_obj, create_parent=False):
        if parent_obj.get_is_exists() is True:
            current_parent_path = self.get_parent_path()
            if current_parent_path != parent_obj.path:
                cmds.parent(self.path, parent_obj.path)
                #
                utl_core.Log.set_module_result_trace(
                    'parent-set',
                    u'obj="{}"'.format(parent_obj.path)
                )
            else:
                utl_core.Log.set_module_warning_trace(
                    'parent-set',
                    'obj="{}" is non-changed'.format(parent_obj.path)
                )
        else:
            utl_core.Log.set_module_warning_trace(
                'parent-set',
                'obj="{}" is non-exists'.format(parent_obj.path)
            )

    def get_dcc_instance(self, obj_type, obj_path=None, *args, **kwargs):
        if obj_path is None:
            obj_path = self.path
        #
        parent_path = self.PATHSEP.join(obj_path.split(self.PATHSEP)[:-1]) or None
        name = obj_path.split(self.PATHSEP)[-1]
        _ = obj_path
        is_create = False
        if 'compose' in kwargs:
            is_compose = kwargs['compose']
        else:
            is_compose = False
        #
        if cmds.objExists(obj_path) is False:
            is_create = True
            if is_compose is True:
                shape_name = '{}Shape'.format(name)
                shape_path = self.PATHSEP.join([obj_path, shape_name])
                _ = shape_path
                if cmds.objExists(shape_path) is False:
                    cmds.createNode('transform', name=name, parent=parent_path, skipSelect=1)
                    cmds.createNode(obj_type, name=shape_name, parent=obj_path, skipSelect=1)
            else:
                self.set_create(obj_type)
                # cmds.createNode(obj_type, name=name, parent=parent_path, skipSelect=1)
        return _, is_create

    def set_create(self, obj_type):
        if self.get_is_exists() is False:
            parent_path = self.get_parent_path()
            name = self.name
            utl_core.Log.set_module_result_trace(
                'obj create',
                'obj="{}", type="{}"'.format(self.path, self.type)
            )
            if parent_path is not None:
                return cmds.createNode(obj_type, name=name, parent=parent_path, skipSelect=1)
            else:
                return cmds.createNode(obj_type, name=name, skipSelect=1)

    def set_display_enable(self, boolean):
        self.get_port('visibility').set(boolean)

    def get_is_transform(self):
        if cmds.objExists(self.path):
            if cmds.nodeType(self.path) == 'transform':
                shape_paths = cmds.listRelatives(self.path, children=1, shapes=1, noIntermediate=0, fullPath=1) or []
                if shape_paths:
                    return True
                return False
            return False
        return False

    def get_is_shape(self):
        if cmds.objExists(self.path):
            if cmds.nodeType(self.path) != 'transform':
                transform_paths = cmds.listRelatives(self.path, parent=1, fullPath=1, type='transform') or []
                shape_paths = cmds.listRelatives(self.path, children=1, shapes=1, noIntermediate=0, fullPath=1) or []
                if transform_paths and not shape_paths:
                    return True
                return False
            return False
        return False

    def get_is_group(self):
        if cmds.objExists(self.path):
            if cmds.nodeType(self.path) == 'transform':
                shape_paths = cmds.listRelatives(self.path, children=1, shapes=1, noIntermediate=0, fullPath=1) or []
                if shape_paths:
                    return True
                return False
            return False
        return False
    # node is transform + shape
    def get_is_compose(self):
        return self.get_is_transform() or self.get_is_shape()

    def set_instance_to(self, obj_path):
        dcc_obj = self.__class__(obj_path)
        if dcc_obj.get_is_exists() is False:
            name = dcc_obj.name
            results = cmds.duplicate(
                self.path, name=name,
                instanceLeaf=1, returnRootsOnly=1
            )
            dcc_obj.set_ancestors_create()
            cmds.parent(results[0], dcc_obj.get_parent_path())

    def get_is_reference(self):
        return cmds.referenceQuery(self._path, isNodeReferenced=1)

    def _get_source_connection_raw_(self):
        lis = []
        _ = cmds.listConnections(self.path, destination=0, source=1, connections=1, plugs=1) or []
        # ["source-atr-path", "target-atr-path", ...]
        for seq, i in enumerate(_):
            if seq % 2:
                source_atr_path = i
                target_atr_path = _[seq - 1]
                #
                lis.append((source_atr_path, target_atr_path))
        return lis

    def _get_target_connection_raw_(self):
        lis = []
        _ = cmds.listConnections(self.path, destination=1, source=0, connections=1, plugs=1) or []
        # ["source-atr-path", "target-atr-path", ...]
        for seq, i in enumerate(_):
            if seq % 2:
                source_atr_path = _[seq - 1]
                target_atr_path = i
                #
                lis.append((source_atr_path, target_atr_path))
        return lis

    def set_visible(self, boolean):
        self.get_port('visibility').set(boolean)


class AbsMyaFileReferenceObj(
    AbsMyaObj,
    utl_abstract.AbsFileReferenceDef
):
    def __init__(self, path, file_path=None):
        super(AbsMyaFileReferenceObj, self).__init__(path)
        # init file reference
        self._set_file_reference_def_init_(file_path)

    def get_is_file_reference(self):
        return True

    def get_is_multiply_reference(self):
        return False


class AbsMyaObjs(utl_abstract.AbsDccObjs):
    def __init__(self, *args):
        super(AbsMyaObjs, self).__init__(*args)
    @classmethod
    def get_paths(cls, reference=True, exclude_paths=None):
        def set_exclude_filter_fnc_(paths):
            if exclude_paths is not None:
                [paths.remove(_i) for _i in exclude_paths if _i in paths]
            return paths
        _ = cmds.ls(type=cls.INCLUDE_DCC_TYPES, long=1) or []
        if exclude_paths is not None:
            return set_exclude_filter_fnc_(_)
        if reference is True:
            return _
        return set_exclude_filter_fnc_(
            [i for i in _ if not cmds.referenceQuery(i, isNodeReferenced=1)]
        )
