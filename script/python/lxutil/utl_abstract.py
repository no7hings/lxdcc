# coding:utf-8
import sys

import os

import platform

import fnmatch

from lxobj import obj_configure, obj_core, obj_abstract

from . import utl_core


def get_is_linux():
    return platform.system() == 'Linux'


def get_is_windows():
    return platform.system() == 'Windows'


class AbsObjGuiDef(object):
    def _set_obj_gui_def_init_(self):
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
    @property
    def data_type(self):
        return None
    @property
    def name(self):
        return self._name
    @property
    def path(self):
        return self._path
    @property
    def icon(self):
        raise NotImplementedError()

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
        return self.path == other.path

    def __ne__(self, other):
        return self.path != self.path


class AbsDccMtd(object):
    @classmethod
    def get_is_maya(cls):
        _ = os.environ.get('MAYA_APP_DIR')
        if _:
            return True
        return False
    @classmethod
    def get_is_houdini(cls):
        _ = os.environ.get('HIP')
        if _:
            return True
        return False
    @classmethod
    def get_is_katana(cls):
        _ = os.environ.get('KATANA_ROOT')
        if _:
            return True
        return False


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
    @property
    def name(self):
        return self._port_path
    @property
    def icon(self):
        return utl_core.Icon.get_port()
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

    def get_has_source(self):
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

    def get_children(self):
        pass

    def get_child(self, port_name):
        pass

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
    CONNECTION_CLASS = None
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
        pathsep = self.CONNECTION_CLASS.PORT_PATHSEP
        for source_atr_path, target_atr_path in connection_raw:
            source_obj_path, source_port_path = obj_core.AtrPathMtd.set_atr_path_split(
                source_atr_path, pathsep=pathsep
            )
            target_obj_path, target_port_path = obj_core.AtrPathMtd.set_atr_path_split(
                target_atr_path, pathsep=pathsep
            )
            source = source_obj_cls(source_obj_path).get_port(source_port_path)
            target = source_obj_cls(target_obj_path).get_port(target_port_path)
            lis.append(
                self.CONNECTION_CLASS(source, target)
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
                    keys.append(_key)
                    lis.append(_connection)
                    _rcs_fnc(_connection.source.obj)

        keys = []
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


class AbsDccObjTargetDef(object):
    CONNECTION_CLASS = None
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
        pathsep = self.CONNECTION_CLASS.PORT_PATHSEP
        for source_atr_path, target_atr_path in connection_raw:
            source_obj_path, source_port_path = obj_core.AtrPathMtd.set_atr_path_split(
                source_atr_path, pathsep=pathsep
            )
            target_obj_path, target_port_path = obj_core.AtrPathMtd.set_atr_path_split(
                target_atr_path, pathsep=pathsep
            )
            source = self.__class__(source_obj_path).get_port(source_port_path)
            target = self.__class__(target_obj_path).get_port(target_port_path)
            lis.append(
                self.CONNECTION_CLASS(source, target)
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
                    keys.append(_key)
                    lis.append(_connection)
                    _rcs_fnc(_connection.target.obj)
        #
        keys = []
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
    obj_abstract.AbsObjDagDef,
    obj_abstract.AbsObjGuiDef,
    # AbsObjGuiDef
):
    # attribute
    PORT_CLASS = None
    CONNECTION_CLASS = None
    def __init__(self, path):
        self._set_obj_dag_def_init_(path)
        if self.path.startswith(self.PATHSEP):
            self._name = self.path.split(self.PATHSEP)[-1]
        else:
            self._name = self.path

        self._set_obj_gui_def_init_()
    # property ******************************************************************************************************* #
    @property
    def type(self):
        raise NotImplementedError()
    @property
    def type_name(self):
        return self.type
    @property
    def name(self):
        return self._name
    # gui property *************************************************************************************************** #
    @property
    def icon(self):
        raise NotImplementedError()
    # attribute ****************************************************************************************************** #
    def get_port(self, port_path, port_assign=obj_configure.PortAssign.VARIANTS):
        if self.PORT_CLASS is not None:
            return self.PORT_CLASS(
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
            port_assign=obj_configure.PortAssign.INPUTS
        )

    def get_output_port(self, port_path):
        return self.get_port(
            port_path,
            port_assign=obj_configure.PortAssign.OUTPUTS
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

    def _set_dag_create_(self, path):
        pass

    def _get_child_paths_(self, path):
        pass

    def _set_child_create_(self, path):
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
    REFERENCE_FILE_CLASS = None
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

    def set_file_save_to(self, *args, **kwargs):
        raise NotImplementedError()


class AbsFileReferenceDef(object):
    PORT_CLASS = None
    OS_FILE_CLASS = None
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

    def set_file_path(self, file_path):
        if file_path is not None:
            self._file = self.OS_FILE_CLASS(file_path)
        else:
            self._file = None

    def get_file_path(self):
        file_attribute = self.get_file_port()
        if file_attribute:
            return file_attribute.get()

    def get_file(self):
        file_path = self.get_file_path()
        if file_path is not None:
            return self.OS_FILE_CLASS(file_path)

    def get_file_port_path(self):
        return self._file_attribute_name

    def set_file_port_path(self, port_path):
        if port_path:
            self._file_attribute_name = port_path

    def get_file_port(self):
        if self._file_attribute_name:
            return self.PORT_CLASS(self, self._file_attribute_name)

    def get_is_multiply_reference(self):
        raise NotImplementedError()

    def set_reference_raw_clear(self):
        self._reference_raw = {}

    def set_file_port_raw_add(self, port_path, file_path=None):
        self._reference_raw[port_path] = file_path

    def get_file_port_paths(self):
        return self._reference_raw.keys()

    def get_file_ports(self):
        return [self.PORT_CLASS(self, i) for i in self.get_file_port_paths()]

    def set_os_file_path_add(self, port_path, file_path):
        self._reference_raw.setdefault(port_path, []).append(file_path)
        os_file = self.OS_FILE_CLASS(file_path)
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
        os_file = self.OS_FILE_CLASS(file_plf_path)
        os_file.set_dcc_attribute_name(port_dcc_path)
        return os_file


class AbsDccObjs(object):
    INCLUDE_DCC_TYPES = []
    EXCLUDE_DCC_PATHS = []
    #
    DCC_OBJ_CLASS = None
    def __init__(self, *args):
        pass
    @classmethod
    def _set_obj_create_(cls, path_):
        return cls.DCC_OBJ_CLASS(path_)
    @classmethod
    def get_paths(cls, **kwargs):
        raise NotImplementedError()
    @classmethod
    def get_objs(cls, **kwargs):
        return [cls._set_obj_create_(i) for i in cls.get_paths(**kwargs)]
    @classmethod
    def get_custom_paths(cls, **kwargs):
        return [i for i in cls.get_paths(**kwargs) if i not in cls.EXCLUDE_DCC_PATHS]
    @classmethod
    def get_custom_nodes(cls, **kwargs):
        return [cls._set_obj_create_(i) for i in cls.get_custom_paths(**kwargs)]


class AbsSetup(object):
    def __init__(self, root):
        self._root = root
    @classmethod
    def _set_environ_(cls, key, value):
        os.environ[key] = value
        utl_core.Log.set_module_result_trace(
            'environ set',
            u'key="{}", value="{}"'.format(key, value)
        )
    @classmethod
    def _set_environ_add_(cls, key, value):
        if key in os.environ:
            v = os.environ[key]
            if value not in v:
                os.environ[key] += os.pathsep + value
                utl_core.Log.set_module_result_trace(
                    'environ add',
                    u'key="{}", value="{}"'.format(key, value)
                )
        else:
            os.environ[key] = value
            utl_core.Log.set_module_result_trace(
                'environ set',
                u'key="{}", value="{}"'.format(key, value)
            )
    @classmethod
    def _set_python_setup_(cls, path):
        python_paths = sys.path
        if path not in python_paths:
            sys.path.insert(0, path)
            utl_core.Log.set_module_result_trace(
                'python-path add',
                u'value="{}"'.format(path)
            )
    @classmethod
    def _set_library_setup_(cls, *args):
        [cls._set_environ_add_('LD_LIBRARY_PATH', i) for i in args]
    @classmethod
    def _set_bin_setup_(cls, *args):
        [cls._set_environ_add_('PATH', i) for i in args]

    def set_run(self):
        raise NotImplementedError()
