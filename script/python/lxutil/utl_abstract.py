# coding:utf-8
import sys

import os

import fnmatch

import lxbasic.core as bsc_core

import lxuniverse.core as unr_core

import lxuniverse.abstracts as unr_abstracts

from lxutil import utl_core


class AbsGuiExtraDef(object):
    def _init_gui_extra_def_(self):
        self._gui_menu_raw = None
        self._obj_gui = None

    @property
    def icon(self):
        raise NotImplementedError()

    def set_gui_menu_raw(self, data):
        self._gui_menu_raw = data

    def get_gui_menu_raw(self):
        return self._gui_menu_raw

    def set_obj_gui(self, obj):
        self._obj_gui = obj

    def get_obj_gui(self):
        return self._obj_gui


class AbsDccObjDef(object):
    # path
    PATHSEP = None

    def __init__(self, path):
        self._path = path
        self._name = path.split(self.PATHSEP)[-1]

    @property
    def type(self):
        raise NotImplementedError()

    def get_type_name(self):
        return self.type

    type_name = property(get_type_name)

    @property
    def data_type(self):
        return None

    def get_name(self):
        return self._name

    name = property(get_name)

    def get_path(self):
        return self._path

    path = property(get_path)

    @property
    def icon(self):
        raise NotImplementedError()

    @property
    def icon_file(self):
        return self.icon

    def get_is_naming_match(self, pattern):
        return fnmatch.filter(
            [self.name], pattern.format(**self._format_dict_())
        ) != []

    def _format_dict_(self):
        return {
            'self': self
        }

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type,
            self.path
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if other is not None:
            return self._path == other._path
        return False

    def __ne__(self, other):
        return self.path != self.path

    def __hash__(self):
        return hash(self._path)


class AbsDccDagDef(object):
    OBJ_PATHSEP = None
    PORT_PATHSEP = None

    @classmethod
    def _get_obj_path_args_(cls, obj_path):
        return obj_path.split(cls.OBJ_PATHSEP)

    @classmethod
    def _get_attr_path_args_(cls, atr_path):
        _ = atr_path.split(cls.PORT_PATHSEP)
        obj_path = _[0]
        obj_path_args = cls._get_obj_path_args_(obj_path)
        port_path_args = _[1:]
        return obj_path_args, port_path_args


# dcc node *********************************************************************************************************** #
class AbsDccPort(AbsDccObjDef):
    def __init__(self, obj, name, port_assign=None):
        self._obj = obj
        self._port_path = name
        self._port_assign = port_assign

    @property
    def type(self):
        raise NotImplementedError()

    @property
    def path(self):
        return self.PATHSEP.join([self.obj.path, self.name])

    @property
    def port_path(self):
        return self._port_path

    @property
    def port_name(self):
        return self._port_path.split(self.PATHSEP)[-1]

    def get_name(self):
        return self._port_path

    name = property(get_name)

    @property
    def icon(self):
        return bsc_core.ResourceIcon.get('attribute')

    @property
    def node(self):
        return self._obj

    @property
    def obj(self):
        return self._obj

    @property
    def port_assign(self):
        return self._port_assign

    def get_is_exists(self):
        raise NotImplementedError()

    def set_create(self, raw_type, default_raw):
        raise NotImplementedError()

    def set(self, *args):
        raise NotImplementedError()

    def get(self, *args):
        raise NotImplementedError()

    # connection
    def set_source(self, *args):
        pass

    def set_source_disconnect(self):
        pass

    def has_source(self):
        pass

    def get_source(self):
        raise NotImplementedError()

    def get_source_obj(self):
        _ = self.get_source()
        if _ is not None:
            return _.obj

    def set_target(self, *args):
        pass

    def set_target_disconnect(self):
        pass

    def get_has_targets(self):
        pass

    def get_targets(self):
        pass

    def get_target_objs(self):
        return [i.obj for i in self.get_targets()]

    def set_disconnect(self):
        pass

    @classmethod
    def _set_atr_path_split_(cls, atr_path):
        _ = atr_path.split(cls.PATHSEP)
        return _[0], cls.PATHSEP.join(_[1:])

    def get_child(self, port_name):
        pass

    def get_children(self):
        pass

    def get_descendants(self):
        def rcs_fnc_(p_):
            _children = p_.get_children()
            for _i in _children:
                list_.append(_i)
                rcs_fnc_(_i)

        list_ = []
        rcs_fnc_(self)
        return list_

    def __str__(self):
        return '{}(type="{}", path="{}", assign="{}")'.format(
            self.__class__.__name__,
            self.type,
            self.path,
            self.port_assign
        )


class AbsDccObjConnection(object):
    PORT_PATHSEP = None

    def __init__(self, source, target):
        self._source, self._target = source, target

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    def __str__(self):
        return '{}(source="{}", target="{}")'.format(
            self.__class__.__name__,
            self._source.path, self._target.path
        )

    def __repr__(self):
        return self.__str__()


class AbsDccObjSourceDef(object):
    CONNECTION_CLS = None
    SOURCE_OBJ_CLS = None

    def __init__(self, *args):
        pass

    def get_port(self, *args):
        raise NotImplementedError()

    def _get_source_obj_cls_(self):
        if self.SOURCE_OBJ_CLS is not None:
            return self.SOURCE_OBJ_CLS
        return self.__class__

    def _get_source_connection_raw_(self, *args, **kwargs):
        return []

    def get_source_connections(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: list(instance(<obj-connection>), ...)
        """
        lis = []
        #
        source_obj_cls = self._get_source_obj_cls_()
        connection_raw = self._get_source_connection_raw_(*args, **kwargs)
        pathsep = self.CONNECTION_CLS.PORT_PATHSEP
        for source_atr_path, target_atr_path in connection_raw:
            source_obj_path, source_port_path = bsc_core.PthAttributeMtd.set_atr_path_split(
                source_atr_path, pathsep=pathsep
            )
            target_obj_path, target_port_path = bsc_core.PthAttributeMtd.set_atr_path_split(
                target_atr_path, pathsep=pathsep
            )
            source = source_obj_cls(source_obj_path).get_port(source_port_path)
            target = source_obj_cls(target_obj_path).get_port(target_port_path)
            lis.append(
                self.CONNECTION_CLS(source, target)
            )
        return lis

    def get_all_source_connections(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: list(instance(<obj-connection>), ...)
        """

        def _rcs_fnc(obj_):
            _connections = obj_.get_source_connections(*args, **kwargs)
            for _connection in _connections:
                _key = _connection.__str__()
                if _key not in keys:
                    keys.add(_key)
                    lis.append(_connection)
                    _rcs_fnc(_connection.source.obj)

        keys = set()
        lis = []
        _rcs_fnc(self)
        return lis

    def get_sources(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: list(instance(<output-port>), ...)
        """
        lis = []
        connections = self.get_source_connections(*args, **kwargs)
        for connection in connections:
            lis.append(connection.source)
        return lis

    def get_all_sources(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: list(instance(<output-port>), ...)
        """
        return [i.source for i in self.get_all_source_connections(*args, **kwargs)]

    def get_source_objs(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: list(instance(<obj>), ...)
        """
        lis = []
        connections = self.get_source_connections(*args, **kwargs)
        for connection in connections:
            lis.append(connection.source.obj)
        return lis

    def get_all_source_objs(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: list(instance(<obj>), ...)
        """
        return [i.source.obj for i in self.get_all_source_connections(*args, **kwargs)]

    def get_all_source_objs_at(self, key):
        p = self.get_port(key)
        source_obj = p.get_source_obj()
        if source_obj:
            return [source_obj]+source_obj.get_all_source_objs()


class AbsDccObjTargetDef(object):
    CONNECTION_CLS = None

    def __init__(self, *args):
        pass

    def get_port(self, *args):
        raise NotImplementedError()

    def _get_target_connection_raw_(self, *args, **kwargs):
        return []

    def get_target_connections(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: list(instance(<obj-connection>), ...)
        """
        lis = []
        connection_raw = self._get_target_connection_raw_(*args, **kwargs)
        pathsep = self.CONNECTION_CLS.PORT_PATHSEP
        for source_atr_path, target_atr_path in connection_raw:
            source_obj_path, source_port_path = bsc_core.PthAttributeMtd.set_atr_path_split(
                source_atr_path, pathsep=pathsep
            )
            target_obj_path, target_port_path = bsc_core.PthAttributeMtd.set_atr_path_split(
                target_atr_path, pathsep=pathsep
            )
            source = self.__class__(source_obj_path).get_port(source_port_path)
            target = self.__class__(target_obj_path).get_port(target_port_path)
            lis.append(
                self.CONNECTION_CLS(source, target)
            )
        return lis

    def get_all_target_connections(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: list(instance(<obj-connection>), ...)
        """

        def _rcs_fnc(obj_):
            _connections = obj_.get_target_connections(*args, **kwargs)
            for _connection in _connections:
                _key = _connection.__str__()
                if _key not in keys:
                    keys.add(_key)
                    lis.append(_connection)
                    _rcs_fnc(_connection.target.obj)

        #
        keys = set()
        lis = []
        _rcs_fnc(self)
        return lis

    def get_targets(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: list(instance(<input-port>), ...)
        """
        lis = []
        connections = self.get_target_connections(*args, **kwargs)
        for connection in connections:
            lis.append(connection.target)
        return lis

    def get_all_targets(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: list(instance(<input-port>), ...)
        """
        return [i.target for i in self.get_all_target_connections(*args, **kwargs)]

    def get_target_objs(self, *args, **kwargs):
        lis = []
        connections = self.get_target_connections(*args, **kwargs)
        for connection in connections:
            lis.append(connection.target.obj)
        return lis

    def get_all_target_objs(self, *args, **kwargs):
        return [i.target.obj for i in self.get_all_target_connections(*args, **kwargs)]


class AbsDccObj(
    AbsDccObjDef,
    AbsDccObjSourceDef,
    AbsDccObjTargetDef,
    unr_abstracts.AbsObjDagExtraDef,
    unr_abstracts.AbsGuiExtraDef,
    # AbsGuiExtraDef
):
    # attribute
    PORT_CLS = None
    CONNECTION_CLS = None

    def __init__(self, path):
        self._init_obj_dag_extra_def_(path)
        if self.path.startswith(self.PATHSEP):
            self._name = self.path.split(self.PATHSEP)[-1]
        else:
            self._name = self.path

        self._init_gui_extra_def_()

    # property ******************************************************************************************************* #
    @property
    def type(self):
        raise NotImplementedError()

    def get_type_name(self):
        return self.type

    @property
    def type_name(self):
        return self.type

    def get_name(self):
        return self._name

    name = property(get_name)

    # gui property *************************************************************************************************** #
    @property
    def icon(self):
        raise NotImplementedError()

    # attribute ****************************************************************************************************** #
    def get_port(self, port_path, port_assign=unr_core.UnrPortAssign.VARIANTS):
        if self.PORT_CLS is not None:
            return self.PORT_CLS(
                self,
                port_path,
                port_assign
            )

    def set(self, key, value):
        self.get_port(key).set(value)

    def get(self, key):
        return self.get_port(key).get()

    def get_input_port(self, port_path):
        return self.get_port(
            port_path,
            port_assign=unr_core.UnrPortAssign.INPUTS
        )

    def get_output_port(self, port_path):
        return self.get_port(
            port_path,
            port_assign=unr_core.UnrPortAssign.OUTPUTS
        )

    def get_ports(self):
        pass

    def get_input_ports(self):
        pass

    def get_is_file_reference(self):
        raise NotImplementedError()

    #
    def get_naming_overlapped_paths(self):
        pass

    def create_dag_fnc(self, path):
        pass

    def _get_child_paths_(self, path):
        pass

    def _get_child_(self, path):
        pass

    def get_is_exists(self):
        raise NotImplementedError()

    def get_is_display_enable(self):
        pass

    def set_display_enable(self, boolean):
        pass

    def get_is_render_enable(self):
        pass

    def set_render_enable(self, boolean):
        pass

    def get_dcc_instance(self, obj_type, obj_path, *args, **kwargs):
        pass

    def set_create(self, *args, **kwargs):
        pass

    def set_delete(self, *args):
        pass

    def get_leaf_ports(self):
        pass

    def get_attributes(self):
        pass


# dcc scene ********************************************************************************************************** #
class AbsDccScene(AbsDccObjDef):
    REFERENCE_FILE_CLS = None

    def __init__(self):
        self._reference_files = []

    @property
    def type(self):
        raise NotImplementedError()

    @property
    def path(self):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    @property
    def icon(self):
        raise NotImplementedError()

    def get_reference_files(self):
        raise NotImplementedError()

    def get_frame_range(self):
        raise NotImplementedError()

    def set_frame_range(self, start_frame, end_frame):
        raise NotImplementedError()

    def get_current_file_path(self, *args, **kwargs):
        raise NotImplementedError()

    def save_to_file(self, *args, **kwargs):
        raise NotImplementedError()


class AbsFileReferenceDef(object):
    PORT_CLS = None
    OS_FILE_CLS = None

    def _set_file_reference_def_init_(self, file_path):
        self.set_file_path(file_path)
        self._file_attribute_name = None
        # multiply
        self._reference_raw = {}
        self._file_paths = []
        self._files = []

    @property
    def reference_raw(self):
        return self._reference_raw

    def get_reference_raw(self):
        return self._reference_raw

    def set_file_path(self, file_path):
        if file_path is not None:
            self._file = self.OS_FILE_CLS(file_path)
        else:
            self._file = None

    def get_file_path(self):
        file_attribute = self.get_file_port()
        if file_attribute:
            return file_attribute.get()

    def get_file(self):
        file_path = self.get_file_path()
        if file_path is not None:
            return self.OS_FILE_CLS(file_path)

    def get_file_port_path(self):
        return self._file_attribute_name

    def set_file_port_path(self, port_path):
        if port_path:
            self._file_attribute_name = port_path

    def get_file_port(self):
        if self._file_attribute_name:
            return self.PORT_CLS(self, self._file_attribute_name)

    def get_is_multiply_reference(self):
        raise NotImplementedError()

    def set_reference_raw_clear(self):
        self._reference_raw = {}

    def set_file_port_raw_add(self, port_path, file_path=None):
        self._reference_raw[port_path] = file_path

    def get_file_port_paths(self):
        return self._reference_raw.keys()

    def get_file_ports(self):
        return [self.PORT_CLS(self, i) for i in self.get_file_port_paths()]

    def set_os_file_path_add(self, port_path, file_path):
        self._reference_raw.setdefault(port_path, []).append(file_path)
        os_file = self.OS_FILE_CLS(file_path)
        os_file.reference_attribute_name = port_path
        self._file_paths.append(file_path)
        self._files.append(os_file)
        return os_file

    def get_os_file_paths(self):
        return self._reference_raw.values()

    def get_file_plf_objs(self):
        return [
            self._set_file_create_(file_plf_path, port_dcc_path)
            for port_dcc_path, file_plf_path in self._reference_raw.items()
        ]

    def get_file_objs(self):
        lis = []
        # for port_dcc_path, file_plf_path in self._reference_raw.items():
        #     if file_plf_path is not None:
        #         pass
        return [
            self._set_file_create_(file_plf_path, port_dcc_path)
            for port_dcc_path, file_plf_path in self._reference_raw.items()
        ]

    def _set_file_create_(self, file_plf_path, port_dcc_path=None):
        os_file = self.OS_FILE_CLS(file_plf_path)
        os_file.set_relevant_dcc_port_path(port_dcc_path)
        return os_file


class AbsDccObjs(object):
    INCLUDE_DCC_TYPES = []
    EXCLUDE_DCC_PATHS = []
    #
    DCC_NODE_CLS = None

    def __init__(self, *args):
        pass

    @classmethod
    def _create_obj_(cls, path_):
        return cls.DCC_NODE_CLS(path_)

    @classmethod
    def get_paths(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def get_objs(cls, **kwargs):
        return [cls._create_obj_(i) for i in cls.get_paths(**kwargs)]

    @classmethod
    def get_custom_paths(cls, **kwargs):
        return [i for i in cls.get_paths(**kwargs) if i not in cls.EXCLUDE_DCC_PATHS]

    @classmethod
    def get_custom_nodes(cls, **kwargs):
        return [cls._create_obj_(i) for i in cls.get_custom_paths(**kwargs)]


class AbsSetup(object):
    def __init__(self, root):
        self._root = root
        self._variants = dict(
            root=self._root
        )

    def _path_process_(self, path):
        _ = path.format(**self._variants)
        if os.path.exists(_):
            return _

    @classmethod
    def set_environ_fnc(cls, key, value):
        if value is not None:
            os.environ[key] = value
            bsc_core.Log.trace_method_result(
                'environ set',
                u'key="{}", value="{}"'.format(key, value)
            )

    @classmethod
    def add_environ_fnc(cls, key, value):
        if value is not None:
            if key in os.environ:
                v = os.environ[key]
                if value not in v:
                    os.environ[key] += os.pathsep+value
                    bsc_core.Log.trace_method_result(
                        'environ add',
                        u'key="{}", value="{}"'.format(key, value)
                    )
            else:
                os.environ[key] = value
                bsc_core.Log.trace_method_result(
                    'environ set',
                    u'key="{}", value="{}"'.format(key, value)
                )

    def add_pythons(self, *args):
        paths_exists = sys.path
        for i_path in args:
            i_path = self._path_process_(i_path)
            if i_path is not None:
                if i_path not in paths_exists:
                    sys.path.insert(0, i_path)
                    bsc_core.Log.trace_method_result(
                        'python-path add',
                        'value="{}"'.format(i_path)
                    )

    def add_libraries(self, *args):
        if bsc_core.SysPlatformMtd.get_is_windows():
            [self.add_environ_fnc('PATH', i) for i in map(self._path_process_, args)]
        elif bsc_core.SysPlatformMtd.get_is_linux():
            [self.add_environ_fnc('LD_LIBRARY_PATH', i) for i in map(self._path_process_, args)]

    def add_bin_fnc(self, *args):
        [self.add_environ_fnc('PATH', i) for i in map(self._path_process_, args)]

    def set_run(self):
        raise NotImplementedError()
