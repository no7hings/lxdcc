# coding:utf-8
import os

import glob

import platform

import subprocess

import fnmatch

import shutil

import json

import collections

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxobj import obj_configure, obj_core


class AbsAttributes(object):
    PATHSEP = None
    def __init__(self, obj, raw):
        self._obj = obj
        if isinstance(raw, dict):
            self._value = raw
        else:
            raise TypeError()
    @property
    def obj(self):
        return self._obj
    @property
    def value(self):
        return self._value

    def _get_all_keys_(self):
        def _rcs_fnc(k_, v_):
            for _k, _v in v_.items():
                if k_ is not None:
                    _key = '{}.{}'.format(k_, _k)
                else:
                    _key = _k
                lis.append(_key)
                if isinstance(_v, dict):
                    _rcs_fnc(_key, _v)
        lis = []
        _rcs_fnc(None, self._value)
        return lis

    def get_keys(self, regex=None):
        _ = self._get_all_keys_()
        if regex is not None:
            return fnmatch.filter(_, regex)
        return _

    def get(self, key_path, default_value=None):
        ks = key_path.split(self.PATHSEP)
        v = self._value
        for k in ks:
            if isinstance(v, dict):
                if k in v:
                    v = v[k]
                else:
                    return default_value
            else:
                return default_value
        return v

    def get_branch_keys(self, key_path):
        value = self.get(key_path)
        if isinstance(value, dict):
            return value.keys()
        return []

    def set(self, key_path, value):
        ks = key_path.split(self.PATHSEP)
        v = self._value
        seq_last = len(ks) - 1
        for seq, k in enumerate(ks):
            if seq == seq_last:
                v[k] = value
            else:
                if k not in v:
                    v[k] = collections.OrderedDict()
                v = v[k]

    def __str__(self):
        return json.dumps(
            self.value,
            indent=4
        )


class AbsProperties(object):
    PATHSEP = None
    def __init__(self, obj, raw):
        self._obj = obj
        if isinstance(raw, dict):
            self._value = raw
        else:
            raise TypeError()
    @property
    def obj(self):
        return self._obj
    @property
    def value(self):
        return self._value

    def _get_all_keys_(self):
        def _rcs_fnc(k_, v_):
            for _k, _v in v_.items():
                if k_ is not None:
                    _key = '{}.{}'.format(k_, _k)
                else:
                    _key = _k
                lis.append(_key)
                if isinstance(_v, dict):
                    _rcs_fnc(_key, _v)
        lis = []
        _rcs_fnc(None, self._value)
        return lis

    def _get_last_keys_(self):
        def _rcs_fnc(k_, v_):
            for _k, _v in v_.items():
                if k_ is not None:
                    _key = '{}.{}'.format(k_, _k)
                else:
                    _key = _k
                #
                if isinstance(_v, dict):
                    _rcs_fnc(_key, _v)
                else:
                    lis.append(_key)

        lis = []
        _rcs_fnc(None, self._value)
        return lis

    def get_keys(self, regex=None):
        _ = self._get_all_keys_()
        if regex is not None:
            return fnmatch.filter(_, regex)
        return _

    def get(self, key_path, default_value=None):
        ks = key_path.split(self.PATHSEP)
        v = self._value
        for k in ks:
            if isinstance(v, dict):
                if k in v:
                    v = v[k]
                else:
                    return default_value
            else:
                return default_value
        return v

    def get_branch_keys(self, key_path):
        value = self.get(key_path)
        if isinstance(value, dict):
            return value.keys()
        return []

    def set(self, key_path, value):
        ks = key_path.split(self.PATHSEP)
        v = self._value
        seq_last = len(ks) - 1
        for seq, k in enumerate(ks):
            if seq == seq_last:
                v[k] = value
            else:
                if k not in v:
                    v[k] = collections.OrderedDict()
                v = v[k]

    def __str__(self):
        return json.dumps(
            self.value,
            indent=4
        )


# stack
class AbsObjStack(object):
    """
    abstract for <obj-stack>
        obj-register
        obj-query
        obj-gain
    """
    def __init__(self):
        self._key_list = []
        self._obj_list = []

    def get_key(self, obj):
        """
        :param obj: instance(<obj>)
        :return: str(<obj-key>)
        """
        raise NotImplementedError()

    def get_index(self, key):
        """
        :param key: str(<obj-key>)
        :return: int(<obj-index>)
        """
        return self._key_list.index(key)

    def get_object(self, key):
        """
        :param key: str(<obj-key>)
        :return: instance(<obj>)
        """
        if key in self._key_list:
            index = self._key_list.index(key)
            return self._obj_list[index]

    def get_object_at(self, index):
        """
        :param index: int(<obj-index>)
        :return: instance(<obj>)
        """
        return self._obj_list[index]

    def get_objects(self, regex=None):
        """
        :param regex: str(<fnmatch-pattern>)
        :return: list[instance(<obj>), ...]
        """
        if regex:
            keys = self.get_keys(regex)
            if keys:
                return [self._obj_list[self._key_list.index(key)] for key in keys]
            return []
        return self._obj_list

    def get_keys(self, regex=None):
        """
        :param regex: str(<fnmatch-pattern>)
        :return: list[str(<obj-key>), ...]
        """
        if regex:
            return fnmatch.filter(self._key_list, regex)
        return self._key_list

    def get_object_exists(self, key):
        """
        :param key: str(<obj-key>)
        :return: bool
        """
        return key in self._key_list

    def get_objects_exists(self, regex=None):
        """
        :param regex: str(<fnmatch-pattern>)
        :return: bool
        """
        if regex:
            keys = self.get_keys(regex)
            return keys != []
        return self._key_list != []

    def set_object_add(self, obj):
        """
        :param obj: instance(<obj>)
        :return: bool
        """
        key = self.get_key(obj)
        if key not in self._key_list:
            self._key_list.append(key)
            self._obj_list.append(obj)
            return True
        return False

    def set_object_del(self, obj):
        """
        :param obj: instance(<obj>)
        :return: bool
        """
        key = self.get_key(obj)
        if key in self._key_list:
            self._key_list.remove(key)
            self._obj_list.remove(obj)
            return True
        return False

    def set_object_override(self, old_obj, new_obj):
        """
        :param old_obj: instance(<obj>)
        :param new_obj: instance(<obj>)
        :return:
        """
        old_key = self.get_key(old_obj)
        if old_key in self._key_list:
            index = self._key_list.index(old_key)
            new_key = self.get_key(new_obj)
            self._key_list[index] = new_key
            self._obj_list[index] = new_obj

    def set_restore(self):
        """
        clear all register <obj>
        :return: None
        """
        self._key_list = []
        self._obj_list = []

    def _set_object_register_(self, obj):
        """
        if <obj> is exists return exists <obj> else add it
        :param obj: instance(<obj>)
        :return: instance(<obj>)
        """
        key = self.get_key(obj)
        if self.get_object_exists(key) is True:
            return self.get_object(key)
        self.set_object_add(obj)
        return obj

    def get_object_count(self):
        """
        :return: int
        """
        return len(self._key_list)

    def get_object_indices(self):
        """
        :return: list[int(<obj-index>), ...]
        """
        return range(len(self.get_object_indices()))

    def __getitem__(self, index):
        """
        :param index: int(<obj-index>)
        :return: instance(<obj>)
        """
        return self.get_object_at(index)

    def __contains__(self, key):
        """
        :param key: str(<obj-key>)
        :return: bool
        """
        return self.get_object_exists(key)


class AbsObjToken(object):
    """
    abstract for <obj-token>
    """
    TYPE_PATHSEP = None
    OBJ_PATHSEP = None
    PORT_PATHSEP = None
    PORT_ASSIGN_PATHSEP = None
    @classmethod
    def _get_port_source_token_(cls, source_port_path):
        return cls._get_port_token_(
            obj_configure.PortAssign.OUTPUTS, source_port_path
        )
    @classmethod
    def _get_obj_source_token_(cls, source_obj_path, source_port_path):
        return cls.PORT_PATHSEP.join(
            [source_obj_path, cls._get_port_source_token_(source_port_path)]
        )
    @classmethod
    def _get_port_target_token_(cls, target_port_path):
        return cls._get_port_token_(
            obj_configure.PortAssign.INPUTS, target_port_path
        )
    @classmethod
    def _get_obj_target_token_(cls, target_obj_path, target_port_path):
        return cls.PORT_PATHSEP.join(
            [target_obj_path, cls._get_port_target_token_(target_port_path)]
        )
    @classmethod
    def _get_obj_connection_token_(cls, source_obj_path, source_port_path, target_obj_path, target_port_path):
        source_token = cls._get_obj_source_token_(source_obj_path, source_port_path)
        target_token = cls._get_obj_target_token_(target_obj_path, target_port_path)
        return ' >> '.join(
            [source_token, target_token]
        )
    @classmethod
    def _get_port_token_(cls, port_assign, port_path):
        return cls.PORT_ASSIGN_PATHSEP.join(
            [port_assign, port_path]
        )


# type/def
class AbsCategoryDef(object):
    """
    abstract for <category>/<obj-category> definition
        type-register
        type-query
        type-gain
    """
    # str(<type-pathsep>/<obj-type-pathsep>)
    PATHSEP = None
    # class(<type>/<obj-type>)
    TYPE_CLASS = None
    def _set_category_def_init_(self, universe, name, type_stack):
        """
        :param universe: instance(<obj-universe>)
        :param name: str(<category-name>/<obj-category-name>)
        :param type_stack: instance(<type-stack>/<obj-type-stack>)
        :return:
        """
        self._universe = universe
        self._name = name
        self._type_stack = type_stack
    @property
    def universe(self):
        """
        :return: instance(<obj-universe>)
        """
        return self._universe
    @property
    def name(self):
        """
        :return: str(<category-name>/<obj-category-name>)
        """
        return self._name
    @property
    def path(self):
        """
        :return: str(<category-path>/<obj-category-path>)
        """
        return self.name
    @property
    def pathsep(self):
        """
        :return: str(<type-pathsep>/<obj-type-pathsep>)
        """
        return self.TYPE_CLASS.PATHSEP
    #
    def _set_type_create_as_new_(self, type_name):
        """
        :param type_name: str(<type-name>/<obj-type-name>)
        :return: instance(<type>)
        """
        return self.TYPE_CLASS(self, type_name)

    def set_type_create(self, type_name):
        category = self
        category_name = self.name
        stack = self._type_stack
        key = self._get_type_path_(category_name, type_name)
        if stack.get_object_exists(key) is True:
            return stack.get_object(key)
        type_ = category._set_type_create_as_new_(type_name)
        stack.set_object_add(type_)
        return type_

    def _get_type_force_(self, type_name):
        return self.set_type_create(type_name)

    def get_type(self, type_name):
        """
        :param type_name: str(<type-name>)
        :return:
        """
        category_name = self.name
        return self._type_stack.get_object(
            self._get_type_path_(category_name, type_name)
        )

    def get_types(self):
        """
        :return: list[instance(<type>), ...]
        """
        category_name = self.name
        type_name = '*'
        regex = self._get_type_path_(category_name, type_name)
        return self._type_stack.get_objects(regex=regex)

    def _get_stack_key_(self):
        """
        method for <obj-stack>
        :return: str
        """
        return self.path

    def _format_dict_(self):
        """
        method for variant-convert
        :return: dict
        """
        return {
            'self': self,
            'category': self
        }
    @classmethod
    def _get_type_path_(cls, category_name, type_name):
        """
        :param category_name: str(<category-name>/<obj-category-name>)
        :param type_name: str(<type-name>/<obj-type-name>)
        :return: str(<type-path>/<obj-type-path>)
        """
        type_pathsep = cls.TYPE_CLASS.PATHSEP
        return type_pathsep.join(
            [category_name, type_name]
        )
    @classmethod
    def _get_type_path_args_(cls, type_path):
        type_pathsep = cls.TYPE_CLASS.PATHSEP
        return type_path.split(type_pathsep)

    def __str__(self):
        return '{}(path="{}")'.format(
            self.__class__.__name__,
            self.path
        )

    def __repr__(self):
        return self.__str__()


class AbsTypeDef(object):
    """
    abstract for <type>/<obj-type> definition
    """
    # str(<type-pathsep>/<obj-type-pathsep>)
    PATHSEP = None
    def _set_type_def_init_(self, category, name):
        """
        :param category: instance(<category>/<obj-category>)
        :param name: str(<type-name>)
        :return:
        """
        self._category = category
        self._name = name
    @property
    def category(self):
        """
        :return: instance(<category>/<obj-category>)
        """
        return self._category
    @property
    def universe(self):
        """
        :return: instance(<obj-universe>)
        """
        return self.category.universe
    @property
    def name(self):
        """
        :return: str(<category-name>/<obj-category-name>)
        """
        return self._name
    @property
    def path(self):
        """
        :return: str(<category-path>/<obj-category-path>)
        """
        return self.category._get_type_path_(
            self.category.name, self.name
        )
    @property
    def pathsep(self):
        """
        :return: str(<type-pathsep>/<obj-type-pathsep>)
        """
        return self.PATHSEP

    def _get_stack_key_(self):
        """
        method for <obj-stack>
        :return: str
        """
        return self.path

    def _format_dict_(self):
        """
        method for variant-convert
        :return: dict
        """
        return {
            'self': self,
            'category': self._category,
            'type': self,
        }

    def __str__(self):
        return '{}(path="{}")'.format(
            self.__class__.__name__,
            self.path
        )

    def __repr__(self):
        return self.__str__()


# <category>
class AbsCategory(AbsCategoryDef):
    """
    abstract for <category>
    """
    def __init__(self, universe, name):
        """
        :param universe: instance(<obj-universe>)
        :param name: str(<category-name>)
        """
        self._set_category_def_init_(universe, name, universe._type_stack)


# <type>
class AbsType(AbsTypeDef):
    """
    abstract for <type>
    """
    def __init__(self, category, name):
        """
        :param category: instance(<obj-universe>)
        :param name: str(<type-name>)
        """
        self._set_type_def_init_(category, name)
    # <type-constant>
    def get_is_constant(self):
        return self.category.name == obj_configure.Category.CONSTANT

    def get_is_boolean(self):
        type_name = self.name
        return obj_configure.Type.get_is_boolean(type_name)
    # <type-tuple>
    def get_is_color(self):
        type_name = self.name
        return obj_configure.Type.get_is_color(type_name)

    def get_is_vector(self):
        type_name = self.name
        return obj_configure.Type.get_is_vector(type_name)

    def get_is_tuple(self):
        type_name = self.name
        return obj_configure.Type.get_is_tuple(type_name)
    #
    def get_tuple_size(self):
        if self.get_is_array() is False:
            type_name = self.name
            return obj_configure.Type.get_tuple_size(type_name)
        return -1
    # <type-matrix>
    def get_is_matrix(self):
        type_name = self.name
        return obj_configure.Type.get_is_matrix(type_name)

    def get_channel_type(self):
        if self.get_is_array() is False:
            category_name = self.category.name
            if self.get_is_vector() or self.get_is_color():
                channel_category_name = obj_configure.Category.CONSTANT
            elif self.get_is_matrix():
                channel_category_name = obj_configure.Category.VECTOR
            else:
                return None
            type_name = obj_configure.Type.get_channel_type_name(category_name)
            category = self.universe.get_category(channel_category_name)
            return category._get_type_force_(type_name)
    # <type-array>
    def get_is_array(self):
        return self.category.name == obj_configure.Category.ARRAY

    def get_element_type(self):
        if self.get_is_array():
            if self.get_is_color():
                element_category_name = obj_configure.Category.COLOR
            elif self.get_is_vector():
                element_category_name = obj_configure.Category.VECTOR
            elif self.get_is_matrix():
                element_category_name = obj_configure.Category.MATRIX
            else:
                element_category_name = obj_configure.Category.CONSTANT
            type_name = self.name
            category = self.universe.get_category(element_category_name)
            return category._get_type_force_(type_name)

    def set_value_create(self, raw):
        type_name = self.name
        is_array = self.get_is_array()
        #
        cls = self._get_value_class_(type_name, is_array)
        return cls(self, raw)
    @classmethod
    def get_raw_flatten(cls, raw):
        def _rcs_fnc(i_):
            if isinstance(i_, (tuple, list)):
                for _j in i_:
                    _rcs_fnc(_j)
            else:
                lis.append(i_)
        lis = []
        _rcs_fnc(raw)
        return lis

    def _get_stack_key_(self):
        return self.path

    def _get_value_class_(self, type_name, is_array):
        raise NotImplementedError()


# obj/def
class AbsObjDef(object):
    """
    abstract for <obj> definition
        etc: <dcc-obj>, <plf-obj>("file", "directory"), ...
    """
    def _set_obj_def_init_(self, name):
        """
        :param name:
        :return: None
        """
        self._name = name
    @property
    def name(self):
        return self._name

    def get_is_naming_match(self, pattern):
        return fnmatch.filter(
            [self.name], pattern
        ) != []


# obj/type/def
class AbsObjTypeDef(object):
    """
    abstract for <obj-type> definition
    """
    def _set_obj_type_def_init_(self, obj_type):
        """
        :param obj_type: instance(<obj-type>)
        :return: None
        """
        self._obj_type = obj_type
    @property
    def universe(self):
        """
        :return: instance(<obj-universe>)
        """
        return self.type.universe
    @property
    def category(self):
        """
        :return: instance(<obj-category>)
        """
        return self.type.category
    @property
    def type(self):
        """
        :return: instance(<obj-type>)
        """
        return self._obj_type
    @property
    def type_path(self):
        return self.type.path
    @property
    def type_name(self):
        return self.type.name


# obj/dag/def
class AbsObjDagDef(object):
    """
    abstract for <obj-dag>
        parent(s) gain
        child(s) gain
    """
    # str(<obj-pathsep>), etc: "/"
    PATHSEP = None
    def _set_obj_dag_def_init_(self, path):
        """
        :param path: str(<obj-path>), etc: "/obj"
        :return: None
        """
        self._path = path
    @classmethod
    def _get_path_args_(cls, path):
        """
        :param path: str(<obj-path>)
        :return: list[str(<obj-name>), ...]
        """
        if cls.PATHSEP is None:
            raise TypeError()
        # is <root-obj>, etc: "/"
        if path == cls.PATHSEP:
            return [cls.PATHSEP, ]
        # is <obj>, etc: "/obj"
        return path.split(cls.PATHSEP)
    @classmethod
    def _get_obj_name_(cls, path):
        """
        :param path:
        :return:
        """
        # is <root-obj>, etc: "/"
        if path == cls.PATHSEP:
            return cls.PATHSEP
        # is <obj>, etc: "/obj"
        return cls._get_path_args_(path)[-1]
    @classmethod
    def _get_parent_path_(cls, path):
        """
        :param path:
        :return:
        """
        pathsep = cls.PATHSEP
        path_args = cls._get_path_args_(path)
        # windows file-path-root etc: "D:/directory"
        if ':' in path_args[0]:
            if len(path_args) == 1:
                return None
            else:
                return pathsep.join(path_args[:-1])
        else:
            if len(path_args) == 1:
                return None
            elif len(path_args) == 2:
                return pathsep
            else:
                return pathsep.join(path_args[:-1])
    @classmethod
    def _get_dag_paths_(cls, path):
        def _rcs_fnc(lis_, path_):
            if path_ is not None:
                lis_.append(path_)
                _parent_path = cls._get_parent_path_(path_)
                if _parent_path:
                    _rcs_fnc(lis_, _parent_path)

        lis = []
        _rcs_fnc(lis, path)
        return lis
    @property
    def pathsep(self):
        """
        :return: str(<obj-pathsep>)
        """
        return self.PATHSEP
    @property
    def path(self):
        """
        :return: str(<obj-path>)
        """
        return self._path
    #
    def get_root(self):
        return self._set_dag_create_(self.PATHSEP)
    #
    def get_is_root(self):
        return self.path == self.PATHSEP
    # branch
    def get_dag_component_paths(self):
        """
        :return: list[str(<obj-path>)]
        """
        def _rcs_fnc(lis_, path_):
            if path_ is not None:
                lis_.append(path_)
                _parent_path = self._get_parent_path_(path_)
                if _parent_path:
                    _rcs_fnc(lis_, _parent_path)

        lis = []
        _rcs_fnc(lis, self.path)
        return lis

    def get_dag_components(self):
        return [self._set_dag_create_(i) for i in self.get_dag_component_paths()]

    def get_dag_element_objs(self):
        """
        :return: list[instance(<obj>), ...]
        """
        return [self._set_dag_create_(i) for i in self.get_dag_component_paths()]
    #
    def set_ancestors_create(self):
        """
        :return: None
        """
        [self._set_dag_create_(i) for i in self.get_ancestor_paths()]

    def set_dag_components_create(self):
        pass

    def _set_dag_create_(self, path):
        raise NotImplementedError()

    def get_parent_path(self):
        """
        :return: str(<obj-path>)
        """
        return self._get_parent_path_(self.path)

    def get_parent_exists(self):
        """
        :return: bool
        """
        return self.get_parent_path() is not None

    def get_parent(self):
        """
        :return: instance(<obj>)
        """
        parent_path = self.get_parent_path()
        if parent_path is not None:
            return self._set_dag_create_(self.get_parent_path())

    def get_ancestor_paths(self):
        """
        :return: list[str(<obj-path>), ...]
        """
        return self.get_dag_component_paths()[1:]

    def get_ancestors(self):
        """
        :return: list[instance(<obj>), ...]
        """
        return [self._set_dag_create_(i) for i in self.get_ancestor_paths()]
    # child
    def _get_child_paths_(self, *args, **kwargs):
        raise NotImplementedError()

    def _set_child_create_(self, path):
        raise NotImplementedError()

    def get_child_paths(self):
        """
        :return: list[str(<obj-path>), ...]
        """
        return self._get_child_paths_(self.path)
    # list of all child <obj-path>
    def get_descendant_paths(self, *args, **kwargs):
        """
        :return: list[str(<obj-path>), ...]
        """
        def _rcs_fnc(lis_, path_):
            if path_ is not None:
                _child_paths = self._get_child_paths_(path_)
                if _child_paths:
                    for _child_path in _child_paths:
                        lis_.append(_child_path)
                        _rcs_fnc(lis_, _child_path)

        lis = []
        _rcs_fnc(lis, self.path)
        return lis
    #
    def get_children_exists(self):
        """
        :return: bool
        """
        return self.get_child_paths() != []
    # list of child <obj>
    def get_children(self):
        """
        :return: list[instance(<obj>), ...]
        """
        return [self._set_child_create_(i) for i in self.get_child_paths()]
    # list of all child <obj>
    def get_descendants(self, *args, **kwargs):
        """
        :return: list[instance(<obj>), ...]
        """
        return [self._set_child_create_(i) for i in self.get_descendant_paths()]

    def __eq__(self, other):
        return self._path == other._path

    def __ne__(self, other):
        return self.path != self.path


class AbsObjDagPath(object):
    def __init__(self, path):
        self._pathsep = path[0]
        self._path = path
    @property
    def name(self):
        return obj_core.DccPathDagMtd.get_dag_name(
            path=self._path, pathsep=self._pathsep
        )
    @property
    def pathsep(self):
        return self._pathsep
    @property
    def path(self):
        return self._path

    def get_root(self):
        return self.__class__(self.pathsep)

    def get_is_root(self):
        return self.path == self.pathsep

    def get_parent_path(self):
        return obj_core.DccPathDagMtd.get_dag_parent(
            path=self._path, pathsep=self._pathsep
        )

    def set_parent_path(self, path):
        # noinspection PyAugmentAssignment
        self._path = path + self._path

    def get_ancestor_paths(self):
        return self.get_component_paths()[1:]

    def get_parent(self):
        _ = self.get_parent_path()
        if _:
            return self.__class__(
                self.get_parent_path()
            )

    def get_component_paths(self):
        return obj_core.DccPathDagMtd.get_dag_component_paths(
            path=self._path, pathsep=self._pathsep
        )

    def get_components(self):
        return [self.__class__(i) for i in self.get_component_paths()]

    def set_translate_to(self, pathsep):
        return self.__class__(
            obj_core.DccPathDagMtd.get_dag_pathsep_replace(
                self.path,
                pathsep_src=self.pathsep,
                pathsep_tgt=pathsep
            )
        )

    def set_namespace_clear_to(self):
        return self.__class__(
            obj_core.DccPathDagMtd.get_dag_path_with_namespace_clear(
                self.path,
                pathsep=self.pathsep,
                namespacesep=':'
            )
        )

    def __str__(self):
        return self._path

    def to_string(self):
        return self._path


class AbsPortDagPath(object):
    PATHSEP = '.'
    def __init__(self, path):
        self._pathsep = self.PATHSEP
        self._path = path
    @property
    def name(self):
        return obj_core.PortPathMethod.get_dag_name(
            path=self._path, pathsep=self._pathsep
        )
    @property
    def pathsep(self):
        return self._pathsep
    @property
    def path(self):
        return self._path

    def get_parent_path(self):
        return obj_core.DccPathDagMtd.get_dag_parent(
            path=self._path, pathsep=self._pathsep
        )


# obj/gui/def
class AbsObjGuiDef(object):
    def _set_obj_gui_def_init_(self):
        self._language = 'english'
        self._custom_raw = {}
    @property
    def gui_attributes(self):
        return self._custom_raw
    @gui_attributes.setter
    def gui_attributes(self, raw):
        if isinstance(raw, dict):
            self._custom_raw = raw
        else:
            raise TypeError()
    @property
    def label(self):
        return self.get_gui_attribute('label')
    @property
    def description(self):
        return self.get_gui_attribute('description')

    def set_description(self, text):
        self.set_gui_attribute('description', text)
    @property
    def icon(self):
        return self.get_gui_attribute('icon')
    @property
    def icon_file(self):
        return self.icon
    @property
    def pathsep(self):
        raise NotImplementedError()
    @property
    def path(self):
        raise NotImplementedError()
    #
    def get_path_prettify(self):
        p = self.path
        pathsep = self.pathsep
        #
        _ = p.split(pathsep)
        if len(_) > 6:
            if bsc_core.StoragePathMtd.get_path_is_windows(p):
                return u'{0}{2}...{2}{1}'.format(pathsep.join(_[:3]), pathsep.join(_[-3:]), pathsep)
            elif bsc_core.StoragePathMtd.get_path_is_linux(p):
                return u'{0}{2}...{2}{1}'.format(pathsep.join(_[:2]), pathsep.join(_[-3:]), pathsep)
            else:
                return p
        else:
            return p

    def get_path_prettify_(self, maximum=32):
        p = self.path
        #
        c = len(p)
        if c > maximum:
            return u'{}...{}'.format(p[:(int(maximum/2)-3)], p[-(int(maximum/2)):])
        return p

    def set_gui_attribute(self, key, value):
        self._custom_raw[key] = value

    def get_gui_attribute(self, key):
        return self._custom_raw.get(key)

    def set_obj_gui(self, gui):
        self.set_gui_attribute('gui_obj', gui)

    def get_obj_gui(self):
        return self.get_gui_attribute('gui_obj')

    def set_gui_ng_graph_node(self, gui):
        self.set_gui_attribute('gui_ng_graph_node', gui)

    def get_gui_ng_graph_node(self):
        return self.get_gui_attribute('gui_ng_graph_node')

    def set_gui_ng_tree_node(self, gui):
        self.set_gui_attribute('gui_ng_tree_node', gui)

    def get_gui_ng_tree_node(self):
        return self.get_gui_attribute('gui_ng_tree_node')

    def set_gui_menu_raw(self, raw):
        self.set_gui_attribute('gui_menu', raw)

    def set_gui_menu_raw_append(self, raw):
        pre_raw = self.get_gui_attribute('gui_menu') or []
        pre_raw.append(raw)
        self.set_gui_menu_raw(pre_raw)

    def set_gui_menu_raw_extend(self, raw):
        pre_raw = self.get_gui_attribute('gui_menu') or []
        pre_raw.extend(raw)
        self.set_gui_menu_raw(pre_raw)

    def get_gui_menu_raw(self):
        return self.get_gui_attribute('gui_menu')

    def set_gui_extra_menu_raw(self, raw):
        self.set_gui_attribute('gui_extra_menu', raw)

    def get_gui_extra_menu_raw(self):
        return self.get_gui_attribute('gui_extra_menu')
    #
    def set_gui_extend_menu_raw(self, raw):
        self.set_gui_attribute('gui_extend_menu', raw)

    def get_gui_extend_menu_raw(self):
        return self.get_gui_attribute('gui_extend_menu')

    def set_gui_menu_content(self, content):
        self.set_gui_attribute('gui_menu_content', content)

    def get_gui_menu_content(self):
        return self.get_gui_attribute('gui_menu_content')


class AbsObjOsDef(object):
    PATHSEP = '/'
    @classmethod
    def _set_symlink_create_(cls, src_path, tgt_path):
        tgt_dir_path = os.path.dirname(tgt_path)
        src_rel_path = os.path.relpath(src_path, tgt_dir_path)
        if os.path.exists(tgt_path) is False:
            os.symlink(src_rel_path, tgt_path)
    @classmethod
    def _set_os_path_reduce_(cls, path):
        path_ = path.replace('\\', cls.PATHSEP)
        _ = path_.split(cls.PATHSEP)
        new_path = cls.PATHSEP.join([i for i in _ if i])
        if path_.startswith(cls.PATHSEP):
            return cls.PATHSEP + new_path
        return new_path

    def _set_obj_os_def_init_(self):
        self._root = bsc_core.StoragePathMtd.get_root(
            self.path
        )
    @property
    def root_name(self):
        return self._root
    @property
    def normcase_root_name(self):
        return os.path.normcase(self._root)
    @property
    def path(self):
        """
        :return: str(<plf-path>)
        """
        raise NotImplementedError()
    @property
    def normcase_path(self):
        """
        get path as normal case
        :return: str(path)
        """
        return os.path.normcase(self.path)
    @property
    def name(self):
        """
        :return: str(<plf-name>)
        """
        raise NotImplementedError()
    @property
    def normcase_name(self):
        return os.path.basename(self.name)

    def get_is_directory(self):
        raise NotImplementedError()

    def get_is_file(self):
        raise NotImplementedError

    def get_is_driver(self):
        # windows
        return ':' in self.name

    def get_is_exists(self):
        raise NotImplementedError()

    def get_is_exists_file(self):
        return os.path.isfile(self.path)
    @staticmethod
    def get_is_linux():
        return platform.system() == 'Linux'
    @staticmethod
    def get_is_windows():
        return platform.system() == 'Windows'

    def set_create(self):
        raise NotImplementedError()

    def set_open(self):
        if os.path.exists(self.path):
            if self.get_is_windows():
                cmd = u'explorer /select,"{}"'.format(self.path.replace('/', '\\'))
                subprocess.Popen(cmd, shell=True)
            elif self.get_is_linux():
                cmd = u'nautilus "{}" --select'.format(self.path)
                subprocess.Popen(cmd, shell=True)

    def get_is_same_to(self, file_path):
        return os.path.normpath(self.path) == os.path.normpath(file_path)

    def get_permission(self):
        return bsc_core.StoragePathMtd.get_permission(self.path)

    def get_is_writeable(self):
        return bsc_core.StoragePathMtd.get_is_writeable(self.path)

    def set_link_to(self, tgt_path, force=False):
        pass


# port/def
class AbsPortDef(object):
    OBJ_TOKEN = None
    PATHSEP = None
    def _set_port_def_init_(self, obj, type_path, port_path, port_assign):
        self._obj = obj
        if isinstance(type_path, (str, unicode)):
            _type = self.obj.universe._get_type_(type_path)
        else:
            _type = type_path
        #
        self._type = _type
        self._port_path = port_path
        self._port_name = port_path.split(self.PATHSEP)[-1]
        self._port_assign = port_assign
        #
        self._is_custom = False
    # obj
    @property
    def obj(self):
        return self._obj
    @property
    def obj_path(self):
        return self.obj.path
    @property
    def category(self):
        return self.type.category
    @property
    def type(self):
        return self._type
    @property
    def type_path(self):
        return self.type.path
    @property
    def type_name(self):
        return self.type.name
    @property
    def name(self):
        return self._port_name
    # obj
    @property
    def path(self):
        return self.PATHSEP.join(
            (self.obj.path, self.port_path)
        )
    @property
    def token(self):
        return self.PATHSEP.join(
            (self.obj.path, self.port_token)
        )
    @property
    def query_path(self):
        return ''
    # port
    @property
    def port_path(self):
        return self._port_path
    @property
    def port_name(self):
        return self._port_name
    @property
    def port_token(self):
        port_assign = self.port_assign
        port_path = self.port_path
        return self.OBJ_TOKEN._get_port_token_(
            port_assign, port_path
        )
    @property
    def pathsep(self):
        return self.PATHSEP
    # port_assign
    @property
    def port_assign(self):
        return self._port_assign

    def get_is_element(self):
        raise NotImplementedError

    def get_is_channel(self):
        raise NotImplementedError
    # port_assign
    def get_is_input_port(self):
        return self.port_assign == obj_configure.PortAssign.INPUTS

    def get_is_output_port(self):
        return self.port_assign == obj_configure.PortAssign.OUTPUTS
    # gain
    def _get_stack_key_(self):
        return self.port_token
    #
    def _get_element_port_path_(self, element_index):
        format_dict = {
            'pathsep': self.PATHSEP,
            'port_path': self.port_path,
            'element_index': element_index
        }
        return obj_configure.Port.ELEMENT_PATH_FORMAT.format(**format_dict)

    def _get_channel_port_path_(self, channel_name):
        format_dict = {
            'pathsep': self.PATHSEP,
            'port_path': self.port_path,
            'channel_name': channel_name
        }
        return obj_configure.Port.CHANNEL_PATH_FORMAT.format(**format_dict)

    def set_custom(self, boolean):
        self._is_custom = boolean

    def get_is_custom(self):
        return self._is_custom

    def _format_dict_(self):
        return {
            'obj': self.obj,
            'parent': self.parent,
            'type': self.type,
            'name': self.name,
            'port_assign': self.port_assign,
            'path': self.path,
            'port_path': self.port_path,
            'token': self.token,
            'port_token': self.port_token
        }
    @classmethod
    def _get_port_token_(cls, port_path, port_assign):
        format_dict = {
            'port_assign_pathsep': cls.PATHSEP,
            'port_path': port_path,
            'port_assign': port_assign
        }
        return obj_configure.Port.PORT_TOKEN_FORMAT.format(**format_dict)
    @classmethod
    def _get_channel_path_(cls, port_path, channel_name):
        format_dict = {
            'pathsep': cls.PATHSEP,
            'port_path': port_path,
            'channel_name': channel_name
        }
        return obj_configure.Port.CHANNEL_PATH_FORMAT.format(**format_dict)
    @property
    def parent(self):
        raise NotImplementedError()

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type.path,
            self.path,
        )

    def __repr__(self):
        return self.__str__()


class AbsPortSourceDef(object):
    """
    <output-port> >> self
    """
    OBJ_TOKEN = None
    def _set_port_input_def_init_(self):
        pass
    @property
    def obj(self):
        raise NotImplementedError()
    @property
    def obj_path(self):
        return self.obj.path
    @property
    def port_path(self):
        raise NotImplementedError()
    # source
    def get_source_exists(self):
        universe = self.obj.universe
        #
        source_obj_path = '*'
        source_port_path = '*'
        target_obj_path = self.obj.path
        target_port_path = self.port_path
        regex = self.OBJ_TOKEN._get_obj_connection_token_(
            source_obj_path, source_port_path, target_obj_path, target_port_path
        )
        return universe.get_connections_exists(regex=regex)

    def get_source_connection(self):
        universe = self.obj.universe
        #
        source_obj_path = '*'
        source_port_path = '*'
        target_obj_path = self.obj.path
        target_port_path = self.port_path
        regex = self.OBJ_TOKEN._get_obj_connection_token_(
            source_obj_path, source_port_path, target_obj_path, target_port_path
        )
        connections = universe.get_connections(regex=regex)
        if connections:
            return connections[-1]

    def get_source(self):
        source_connection = self.get_source_connection()
        if source_connection:
            return source_connection.source

    def set_connect_from(self, output_port):
        source_obj_args = output_port.obj_path
        source_port_args = output_port.port_path
        target_obj_args = self.obj_path
        target_port_args = self.port_path
        #
        return self.obj.universe.set_connection_create(
            source_obj_args, source_port_args,
            target_obj_args, target_port_args
        )

    def set_source(self, output_port):
        self.set_connect_from(output_port)

    def _format_dict_(self):
        raise NotImplementedError()


class AbsPortTargetDef(object):
    """
    self >> [<input-port>, ...]
    """
    OBJ_TOKEN = None
    def _set_port_output_def_init_(self):
        pass
    @property
    def obj(self):
        raise NotImplementedError()
    @property
    def obj_path(self):
        return self.obj.path
    @property
    def port_path(self):
        raise NotImplementedError()
    # target
    def get_targets_exists(self):
        universe = self.obj.universe
        #
        source_obj_path = self.obj.path
        source_port_path = self.port_path
        target_obj_path = '*'
        target_port_path = '*'
        regex = self.OBJ_TOKEN._get_obj_connection_token_(
            source_obj_path, source_port_path, target_obj_path, target_port_path
        )
        return universe.get_connections_exists(regex=regex)

    def get_target_connections(self):
        universe = self.obj.universe
        #
        source_obj_path = self.obj.path
        source_port_path = self.port_path
        target_obj_path = '*'
        target_port_path = '*'
        regex = self.OBJ_TOKEN._get_obj_connection_token_(
            source_obj_path, source_port_path, target_obj_path, target_port_path
        )
        return universe.get_connections(regex=regex)

    def get_targets(self):
        target_connections = self.get_target_connections()
        return [i.target for i in target_connections]

    def set_connect_to(self, input_port):
        source_obj_args = self.obj_path
        source_port_args = self.port_path
        target_obj_args = input_port.obj_path
        target_port_args = input_port.port_path
        #
        return self.obj.universe.set_connection_create(
            source_obj_args, source_port_args,
            target_obj_args, target_port_args
        )

    def set_target(self, input_port):
        self.set_connect_to(input_port)

    def _format_dict_(self):
        raise NotImplementedError()


class AbsPortElementDef(object):
    PORT_ELEMENT_STACK_CLASS = None
    PORT_ELEMENT_CLASS = None
    # init
    def _set_port_element_def_init_(self):
        self._port_element_stack = self.PORT_ELEMENT_STACK_CLASS()
    @property
    def obj(self):
        raise NotImplementedError()
    @property
    def port_assign(self):
        raise NotImplementedError()
    # method
    def _set_element_add_(self, port_element):
        self._port_element_stack.set_object_add(port_element)
        # add to obj
        self.obj._set_port_add_(port_element)

    def _set_element_create_(self, index):
        port_element = self.PORT_ELEMENT_CLASS(self, index)
        self._set_element_add_(port_element)
        return port_element

    def get_elements_exists(self, regex=None):
        return self._port_element_stack.get_objects_exists(regex)

    def get_element_indices(self):
        return self._port_element_stack.get_object_indices()

    def get_elements(self, regex=None):
        return self._port_element_stack.get_objects(regex)

    def get_element_exists(self, index):
        return self._port_element_stack.get_object_exists(index)

    def get_element(self, index):
        return self._port_element_stack.get_object_at(index)

    def get_element_at(self, index):
        return self._port_element_stack.get_object_at(index)

    def __getitem__(self, index):
        return self.get_element(index)


class AbsPortChannelDef(object):
    PORT_CHANNEL_STACK_CLASS = None
    PORT_CHANNEL_CLASS = None
    # init
    def _set_port_channel_def_init_(self):
        self._channel_stack = self.PORT_CHANNEL_STACK_CLASS()
    @property
    def obj(self):
        raise NotImplementedError()
    @property
    def port_assign(self):
        raise NotImplementedError()
    # method
    def _set_channel_add_(self, channel):
        # add to parent
        self._channel_stack.set_object_add(channel)
        # add to obj
        self.obj._set_port_add_(channel)

    def _set_channel_create_(self, name):
        channel = self.PORT_CHANNEL_CLASS(self, name)
        self._set_channel_add_(channel)
        return channel

    def get_channels_exists(self, regex=None):
        return self._channel_stack.get_objects_exists(regex)

    def get_channel_names(self):
        return self._channel_stack.get_keys()

    def get_channels(self, regex=None):
        return self._channel_stack.get_objects(regex)

    def get_channel_exists(self, channel_name):
        return self._channel_stack.get_object_exists(channel_name)

    def get_channel(self, channel_name):
        """
        :param channel_name: str(channel_name)
        :return: instance(Channel)
        """
        return self._channel_stack.get_object(channel_name)

    def get_channel_index(self, channel_name):
        """
        :param channel_name: str(channel_name)
        :return: int(index)
        """
        return self._channel_stack.get_index(channel_name)

    def get_channel_at(self, index):
        return self._channel_stack.get_object_at(index)

    def __getitem__(self, index):
        return self.get_channel_at(index)


class AbsPortValueDef(object):
    def _set_port_value_def_init_(self):
        self._value = self.type.set_value_create(None)
        self._value_default = self.type.set_value_create(None)
        #
        self._is_enumerate = False
        self._enumerate_raw = []
    @property
    def parent(self):
        raise NotImplementedError()
    @property
    def type(self):
        raise NotImplementedError()
    @property
    def name(self):
        raise NotImplementedError()

    def get_value(self):
        return self._value
    # <value-default>
    def get_value_default(self):
        return self._value_default

    def set(self, raw):
        self.get_value().set(raw)

    def set_default(self, raw):
        self.get_value_default().set(raw)

    def get(self):
        return self.get_value().get()

    def get_as_string(self):
        return self.get_value().get_as_string()

    def get_as_obj(self):
        return self.get_value().get_as_obj()

    def get_default(self):
        return self.get_default().get()

    def get_is_value_changed(self):
        return self._value != self._value_default

    def set_enumerate(self, boolean):
        self._is_enumerate = boolean

    def get_is_enumerate(self):
        return self._is_enumerate

    def set_enumerate_raw(self, enumerate_raw):
        self._enumerate_raw = enumerate_raw

    def get_enumerate_strings(self):
        return self._enumerate_raw

    def get_as_index(self):
        if self.get_is_enumerate():
            raw = self.get()
            return self.get_enumerate_strings().index(raw)


class AbsPortChannelValueDef(object):
    @property
    def type(self):
        raise NotImplementedError()
    @property
    def parent(self):
        raise NotImplementedError()
    @property
    def index(self):
        raise NotImplementedError()

    def get_value(self):
        return self.parent.get_value().get_channel(self.index)

    def get(self):
        return self.get_value().get()

    def get_as_string(self):
        return self.get_value().get_as_string()

    def get_as_obj(self):
        return self.get_value().get_as_obj()


class AbsPortElementValueDef(object):
    @property
    def type(self):
        raise NotImplementedError()

    @property
    def parent(self):
        raise NotImplementedError()

    @property
    def index(self):
        raise NotImplementedError()

    def get_value(self):
        return self.parent.get_value().get_element(self.index)

    def get(self):
        return self.get_value().get()

    def get_as_string(self):
        return self.get_value().get_as_string()

    def get_as_obj(self):
        return self.get_value().get_as_obj()


class AbsPortChannel(
    # <port>
    AbsPortDef,
    # <port-source>
    AbsPortSourceDef,
    # <port-target>
    AbsPortTargetDef,
    # <port-value>
    AbsPortChannelValueDef
):
    def __init__(self, parent, name):
        self._parent = parent
        # port
        self._set_port_def_init_(
            parent.obj, parent.type,
            name, parent.port_assign
        )
        self._set_port_input_def_init_()
        self._set_port_output_def_init_()
    @property
    def obj(self):
        return self.parent.obj
    @property
    def type(self):
        return self.parent.type
    #
    @property
    def parent(self):
        return self._parent
    @property
    def port_path(self):
        return self.parent._get_channel_port_path_(
            self.name
        )
    @property
    def index(self):
        return self.parent.get_channel_index(self.name)

    def get_is_element(self):
        return False

    def get_is_channel(self):
        return True


class AbsPortElement(
    # <port>
    AbsPortDef,
    # <port-channel>
    AbsPortChannelDef,
    # <port-source>
    AbsPortSourceDef,
    # <port-target>
    AbsPortTargetDef,
    # <port-value>
    AbsPortElementValueDef,
):
    def __init__(self, parent, index):
        self._parent = parent
        # port
        self._set_port_def_init_(
            parent.obj, parent.type,
            str(index), parent.port_assign
        )
        # <port-channel>
        self._set_port_channel_def_init_()
        # <port-input>
        self._set_port_input_def_init_()
        # <port-output>
        self._set_port_output_def_init_()
    @property
    def parent(self):
        return self._parent
    @property
    def obj(self):
        return self.parent.obj
    @property
    def type(self):
        return self.parent.type
    @property
    def port_path(self):
        return self.parent._get_element_port_path_(
            self.index
        )
    @property
    def index(self):
        return int(self.name)

    def get_is_element(self):
        return True

    def get_is_channel(self):
        return False


class AbsPort(
    # <port>
    AbsPortDef,
    # <port-element>
    AbsPortElementDef,
    # <port-channel>
    AbsPortChannelDef,
    # <port-source>
    AbsPortSourceDef,
    # <port-target>
    AbsPortTargetDef,
    # <port-value>
    AbsPortValueDef,
    # <obj-gui>
    AbsObjGuiDef,
):
    def __init__(self, obj, type_path, port_path, port_assign):
        self._set_port_def_init_(
            obj, type_path,
            port_path, port_assign
        )
        self._set_port_element_def_init_()
        self._set_port_channel_def_init_()
        self._set_port_value_def_init_()
        self._set_port_input_def_init_()
        self._set_port_output_def_init_()
        self._set_obj_gui_def_init_()
    @property
    def parent(self):
        return None

    def get_is_element(self):
        return False

    def get_is_channel(self):
        return False

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type.path,
            self.path
        )

    def __repr__(self):
        return self.__str__()


# obj/type/def
class AbsObjTypeObjDef(object):
    # class(<obj>)
    DCC_OBJ_CLASS = None
    def _set_obj_type_obj_def_init_(self):
        pass
    @property
    def universe(self):
        raise NotImplementedError()
    @property
    def category(self):
        raise NotImplementedError()
    @property
    def name(self):
        raise NotImplementedError()

    def _set_obj_branches_create_(self):
        pass

    def set_obj_create(self, obj_path_args, default_obj_type=None):
        # etc: /a/b/c
        if isinstance(obj_path_args, (str, unicode)):
            obj_path = obj_path_args
        # etc: [a, b, c, ...]
        elif isinstance(obj_path_args, (tuple, list)):
            obj_path = self._get_obj_path_(obj_path_args)
        else:
            raise TypeError()
        #
        obj = self.universe.get_obj(obj_path)
        if obj is not None:
            if obj.type.name == obj_configure.ObjType.NULL:
                old_obj = obj
                new_obj = self._set_obj_create_(obj_path)
                self.universe._set_obj_override_(old_obj, new_obj)
                return new_obj
        else:
            obj = self._set_obj_create_(obj_path)
            self.universe._set_obj_add_(obj)
        return obj
    @property
    def obj_pathsep(self):
        return self.DCC_OBJ_CLASS.PATHSEP
    @classmethod
    def _get_obj_path_(cls, obj_path_args):
        return cls.DCC_OBJ_CLASS.PATHSEP.join(obj_path_args)

    def _set_obj_create_(self, obj_path):
        new_obj = self.DCC_OBJ_CLASS(self, obj_path)
        new_obj.set_ancestors_create()
        return new_obj

    def get_objs(self):
        """
        regex-etc: "obj_category_name/obj_type_name@*"
        :return: list[instance(<obj>), ...]
        """
        obj_category_name = self.category.name
        obj_type_name = self.name
        obj_string = '*'
        regex = self.category._get_obj_token_(
            obj_category_name, obj_type_name, obj_string
        )
        return self.universe._obj_stack.get_objects(regex=regex)


# obf/port/def
class AbsObjPortDef(object):
    OBJ_TOKEN = None
    #
    PORT_CLASS = None
    PORT_STACK_CLASS = None
    def _set_node_port_def_init_(self):
        self._port_stack = self.PORT_STACK_CLASS()
    @property
    def universe(self):
        raise NotImplementedError()

    def _set_ports_build_(self, ports_raw, raw_convert_method=None):
        for k, v in ports_raw.items():
            self._set_port_build_(k, v, raw_convert_method)

    def _set_port_build_(self, key, value, raw_convert_method=None):
        port_path = key.replace('/', obj_configure.Port.PATHSEP)
        if isinstance(value, dict):
            type_path = value.get(
                'type',
                obj_configure.Type.CONSTANT_RAW_
            ).replace('/', obj_configure.Type.PATHSEP)
            port_assign = value.get(
                'port_assign',
                obj_configure.PortAssign.VARIANTS
            )
            if raw_convert_method is not None:
                raw = raw_convert_method(value.get('raw'))
            else:
                raw = value.get('raw')
        else:
            port_assign = obj_configure.PortAssign.VARIANTS
            type_path = obj_configure.Type.CONSTANT_RAW_
            raw = value
        #
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        if self._port_stack.get_object_exists(port_token) is True:
            port = self._port_stack.get_object(port_token)
        else:
            port = self._set_port_create_(
                type_path, port_path, port_assign
            )
            self._port_stack.set_object_add(port)
        #
        port.set(raw)

    def set_port_create(self, type_args, port_path, port_assign):
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        if self._port_stack.get_object_exists(port_token) is True:
            port = self._port_stack.get_object(port_token)
        else:
            port = self._set_port_create_(
                type_args, port_path, port_assign
            )
            self._port_stack.set_object_add(port)
        return port

    def set_variant_port_create(self, type_args, port_path):
        return self.set_port_create(type_args, port_path, obj_configure.PortAssign.VARIANTS)

    def set_input_port_create(self, type_args, port_path):
        return self.set_port_create(type_args, port_path, obj_configure.PortAssign.INPUTS)

    def set_output_port_create(self, type_args, port_path):
        return self.set_port_create(type_args, port_path, obj_configure.PortAssign.OUTPUTS)

    def _set_port_create_(self, type_args, port_path, port_assign):
        port = self.PORT_CLASS(
            self, type_args, port_path, port_assign
        )
        return port
    # port
    def get_port(self, port_string):
        if self.OBJ_TOKEN.PORT_ASSIGN_PATHSEP in port_string:
            port_token = port_string
            return self._port_stack.get_object(port_token)
        else:
            port_assigns = obj_configure.PortAssign.ALL
            port_path = port_string
            for port_assign in port_assigns:
                port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
                _ = self._port_stack.get_object(port_token)
                if _ is not None:
                    return _

    def get_port_is_exists(self, port_token):
        return self._port_stack.get_object_exists(port_token)

    def get_ports(self, regex=None):
        return self._port_stack.get_objects(regex)

    def get_ports_exists(self, regex=None):
        return self._port_stack.get_objects_exists(regex)

    def _set_port_add_(self, port):
        self._port_stack.set_object_add(port)
    # input
    def get_input_port_exists(self, port_path):
        port_assign = obj_configure.PortAssign.INPUTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port_is_exists(port_token)

    def get_input_port(self, port_path):
        port_assign = obj_configure.PortAssign.INPUTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port(port_token)

    def get_input(self, port_path):
        port = self.get_input_port(port_path)
        if port is not None:
            return port.get()

    def get_input_ports(self):
        port_assign = obj_configure.PortAssign.INPUTS
        port_path = '*'
        regex = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self._port_stack.get_objects(regex=regex)
    # output
    def get_output_port_exists(self, port_path):
        port_assign = obj_configure.PortAssign.OUTPUTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port_is_exists(port_token)

    def get_output_port(self, port_path):
        port_assign = obj_configure.PortAssign.OUTPUTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port(port_token)

    def get_output(self, port_path):
        port = self.get_output_port(port_path)
        if port is not None:
            return port.get()

    def get_output_ports(self):
        port_assign = obj_configure.PortAssign.OUTPUTS
        port_path = '*'
        regex = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self._port_stack.get_objects(regex=regex)
    # bind
    def get_bind_port_exists(self, port_path):
        port_assign = obj_configure.PortAssign.BINDS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port_is_exists(port_token)

    def get_bind_port(self, port_path):
        port_assign = obj_configure.PortAssign.BINDS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port(port_token)

    def get_bind(self, port_path):
        port = self.get_bind_port(port_path)
        if port is not None:
            return port.get()

    def get_bind_ports(self):
        port_assign = obj_configure.PortAssign.BINDS
        port_path = '*'
        regex = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self._port_stack.get_objects(regex=regex)
    # variant
    def get_variant_port_exists(self, port_path):
        port_assign = obj_configure.PortAssign.VARIANTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port_is_exists(port_token)

    def get_variant_port(self, port_path):
        port_assign = obj_configure.PortAssign.VARIANTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port(port_token)
    # noinspection PyUnusedLocal
    def get_variant_ports(self, regex=None):
        port_assign = obj_configure.PortAssign.VARIANTS
        port_path = '*'
        regex = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self._port_stack.get_objects(regex=regex)

    def get_variant(self, port_path):
        port_path = port_path.replace('/', self.PORT_CLASS.PATHSEP)
        port = self.get_variant_port(port_path)
        if port is not None:
            return port.get()

    def set_variant(self, port_path, raw):
        port_path = port_path.replace('/', self.PORT_CLASS.PATHSEP)
        port = self.get_variant_port(port_path)
        if port:
            return port.set(raw)

    def get(self, key):
        return self.get_variant(key)

    def set(self, key, value):
        self.set_variant(key, value)

    def _format_dict_(self):
        raise NotImplementedError()


# <port-query>
class AbsPortQuery(object):
    OBJ_TOKEN = None
    #
    PATHSEP = None
    def __init__(self, obj, type_path, port_path, port_assign, raw):
        self._obj = obj
        self._type = self.obj.universe._get_type_(type_path)
        self._port_path = port_path
        self._port_assign = port_assign
        #
        self._value = self.type.set_value_create(raw)
        self._raw = raw
    # type
    @property
    def obj(self):
        return self._obj
    @property
    def category(self):
        return self.type.category
    @property
    def type(self):
        return self._type
    @property
    def type_path(self):
        return self.type.path
    @property
    def type_name(self):
        return self.type.name
    # obj
    @property
    def path(self):
        return self.PATHSEP.join(
            [self.obj.path, self.port_path]
        )
    @property
    def pathsep(self):
        return self.PATHSEP
    # port
    @property
    def port_path(self):
        return self._port_path
    # stack
    @property
    def token(self):
        port_assign = self.port_assign
        port_path = self.port_path
        return self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
    @property
    def port_assign(self):
        return self._port_assign

    def get_value(self):
        return self._value

    def set(self, raw):
        self.get_value().set(raw)

    def get(self):
        return self.get_value().get()

    def _get_stack_key_(self):
        return self.token

    def __str__(self):
        return '{}(path="{}", type="{}", raw="{}")'.format(
            self.__class__.__name__,
            self.path,
            self.type.path,
            self.get()
        )

    def __repr__(self):
        return self.__str__()


# <port-query>
class AbsObjTypePortQueryDef(object):
    OBJ_TOKEN = None
    #
    PORT_QUERY_CLASS = None
    PORT_QUERY_STACK_CLASS = None
    def _set_obj_type_port_query_def_init_(self):
        self._port_query_stack = self.PORT_QUERY_STACK_CLASS()

    def _set_port_queries_build_(self, port_query_raw, raw_convert_method=None):
        for k, v in port_query_raw.items():
            self._set_port_query_build_(k, v, raw_convert_method)

    def _set_port_query_build_(self, key, value, raw_convert_method=None):
        port_path = key.replace('/', obj_configure.Port.PATHSEP)
        if isinstance(value, dict):
            type_path = value.get(
                'type',
                obj_configure.Type.CONSTANT_RAW_
            ).replace('/', obj_configure.Type.PATHSEP)
            port_assign = value.get(
                'port_assign',
                obj_configure.PortAssign.VARIANTS
            )
            raw = value.get('raw')
        else:
            port_assign = obj_configure.PortAssign.VARIANTS
            type_path = obj_configure.Type.CONSTANT_RAW_
            raw = value
        #
        if raw_convert_method is not None:
            raw = raw_convert_method(value.get('raw'))
        #
        token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        if self._port_query_stack.get_object_exists(token) is True:
            port_query = self._port_query_stack.get_object(token)
        else:
            port_query = self._set_port_query_create_(
                type_path, port_path, port_assign, raw
            )
            self._port_query_stack.set_object_add(port_query)
        #
        port_query.set(raw)

    def _set_port_query_create_(self, type_path, port_path, port_assign, raw):
        return self.PORT_QUERY_CLASS(
            self, type_path, port_path, port_assign, raw
        )

    def _set_port_query_inherit_(self, port_query):
        type_path = port_query.type.path
        port_path = port_query.port_path
        port_assign = port_query.port_assign
        raw = port_query.get()
        port_query = self.PORT_QUERY_CLASS(
            self, type_path, port_path, port_assign, raw
        )
        self._port_query_stack.set_object_add(port_query)

    def get_port_queries(self, regex=None):
        return self._port_query_stack.get_objects(regex)

    def get_port_query(self, token):
        return self._port_query_stack.get_object(token)

    def get_port_query_is_exists(self, token):
        return self._port_query_stack.get_object_exists(token)
    #
    def get_input_port_query(self, port_path):
        port_assign = obj_configure.PortAssign.INPUTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port_query(port_token)
    
    def get_input_port_queries(self):
        format_dict = {
            'port_assign': obj_configure.PortAssign.INPUTS,
            'port_assign_pathsep': obj_configure.PortAssign.PATHSEP
        }
        return self._port_query_stack.get_objects(
            regex=obj_configure.Obj.PORTS_GAIN_REGEX.format(**format_dict)
        )

    def get_output_port_query(self, port_path):
        port_assign = obj_configure.PortAssign.OUTPUTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port_query(port_token)

    def get_output_port_queries(self):
        format_dict = {
            'port_assign': obj_configure.PortAssign.OUTPUTS,
            'port_assign_pathsep': obj_configure.PortAssign.PATHSEP
        }
        return self._port_query_stack.get_objects(
            regex=obj_configure.Obj.PORTS_GAIN_REGEX.format(**format_dict)
        )

    def get_variant_port_query(self, port_path):
        port_assign = obj_configure.PortAssign.VARIANTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port_query(port_token)
    # noinspection PyUnusedLocal
    def get_variant_port_queries(self, regex=None):
        format_dict = dict(
            port_assign=obj_configure.PortAssign.VARIANTS,
            port_assign_pathsep=obj_configure.PortAssign.PATHSEP,
            regex_extra=regex
        )
        if regex is not None:
            return self._port_query_stack.get_objects(
                regex=obj_configure.Obj.PORTS_GAIN_REGEX_EXTRA.format(**format_dict)
            )
        return self._port_query_stack.get_objects(
            regex=obj_configure.Obj.PORTS_GAIN_REGEX.format(**format_dict)
        )

    def get_variant(self, port_path):
        port_path = port_path.replace('/', self.PORT_QUERY_CLASS.PATHSEP)
        port_query = self.get_variant_port_query(port_path)
        if port_query:
            return port_query.get()

    def set_variant(self, port_path, raw):
        port_path = port_path.replace('/', self.PORT_QUERY_CLASS.PATHSEP)
        port_query = self.get_variant_port_query(port_path)
        if port_query:
            return port_query.set(raw)


# <obj-category>
class AbsObjCategory(
    AbsCategoryDef,
    AbsObjTypePortQueryDef
):
    def __init__(self, universe, name):
        self._set_category_def_init_(universe, name, universe._obj_type_stack)
        self._set_obj_type_port_query_def_init_()

    def _set_type_create_as_new_(self, type_name):
        obj_type = self.TYPE_CLASS(self, type_name)
        for port_query in self.get_port_queries():
            obj_type._set_port_query_inherit_(port_query)
        return obj_type

    def get_objs(self):
        obj_category_name = self.name
        obj_type_name = '*'
        obj_string = '*'
        regex = self._get_obj_token_(
            obj_category_name, obj_type_name, obj_string
        )
        return self.universe._obj_stack.get_objects(regex=regex)
    @classmethod
    def _get_obj_token_(cls, obj_category_name, obj_type_name, obj_string):
        """
        :param obj_category_name:
        :param obj_type_name:
        :param obj_string:
        :return:
        """
        return '@'.join(
            [cls._get_type_path_(obj_category_name, obj_type_name), obj_string]
        )


# <obj-type>
class AbsObjType(
    AbsTypeDef,
    AbsObjTypeObjDef,
    AbsObjTypePortQueryDef
):
    def __init__(self, category, name):
        self._set_type_def_init_(category, name)
        self._set_obj_type_obj_def_init_()
        self._set_obj_type_port_query_def_init_()

    def _set_obj_create_(self, obj_path_args):
        if isinstance(obj_path_args, (str, unicode)):
            obj_path = obj_path_args
        elif isinstance(obj_path_args, (tuple, list)):
            obj_path = self._get_obj_path_(obj_path_args)
        else:
            raise TypeError()
        new_obj = self.DCC_OBJ_CLASS(self, obj_path)
        for port_query in self.get_port_queries():
            type_path = port_query.type.path
            port_path = port_query.port_path
            port_assign = port_query.port_assign
            port = new_obj._set_port_create_(
                type_path, port_path, port_assign
            )
            port.set(port_query.get())
            new_obj._set_port_add_(port)
        #
        new_obj.set_ancestors_create()
        return new_obj


# <obj-source/target>
class AbsObjSourceDef(object):
    """
    abstract for <obj-source> definition
        <input-port>
    """
    OBJ_TOKEN = None
    # str(<connection-pattern>)
    OBJ_SOURCE_CONNECTION_GAIN_REGEX = u'* >> {obj.path}.*'
    def _set_obj_source_def_init_(self):
        """
        :return: None
        """
        pass
    @property
    def universe(self):
        raise NotImplementedError()
    @property
    def path(self):
        raise NotImplementedError()
    #
    def _get_source_connections_(self, obj_path):
        source_obj_path = '*'
        source_port_path = '*'
        target_obj_path = obj_path
        target_port_path = '*'
        regex = self.OBJ_TOKEN._get_obj_connection_token_(
            source_obj_path, source_port_path, target_obj_path, target_port_path
        )
        return self.universe.get_connections(
            regex=regex
        )
    @classmethod
    def _get_source_(cls, obj_connection):
        return obj_connection.source
    @classmethod
    def _get_source_obj_(cls, obj_connection):
        return obj_connection.source_obj

    def get_source_connections(self):
        """
        :return: list[instance(<obj-connection>), ...]
        """
        return self._get_source_connections_(self.path)
    
    def get_sources(self):
        """
        :return: list[instance(<port>), ...]
        """
        return [self._get_source_(i) for i in self.get_source_connections()]

    def get_source_objs(self):
        return [self._get_source_obj_(i) for i in self.get_source_connections()]

    def _get_all_source_connections_(self, obj_path):
        def _rcs_fnc(obj_path_):
            _obj_connections = self._get_source_connections_(obj_path_)
            for _i in _obj_connections:
                lis.append(_i)
                _rcs_fnc(self._get_source_obj_(_i).path)

        lis = []
        _rcs_fnc(obj_path)
        return lis

    def get_all_source_connections(self):
        return self._get_all_source_connections_(self.path)

    def get_all_sources(self):
        return [self._get_source_(i) for i in self.get_all_source_connections()]

    def get_all_source_objs(self):
        return [self._get_source_obj_(i) for i in self.get_all_source_connections()]

    def _format_dict_(self):
        raise NotImplementedError()


class AbsObjTargetDef(object):
    """
    abstract for <obj-target> definition
        <output-port>
    """
    OBJ_TOKEN = None
    # str(<connection-pattern>)
    OBJ_TARGET_CONNECTION_GAIN_REGEX = u'{obj.path}.* >> *'
    def _set_obj_target_def_init_(self):
        pass
    @property
    def universe(self):
        raise NotImplementedError()
    @property
    def path(self):
        raise NotImplementedError()

    def _get_target_connections_(self, obj_path):
        """
        :return: list[instance(<obj-connection>), ...]
        """
        source_obj_path = obj_path
        source_port_path = '*'
        target_obj_path = '*'
        target_port_path = '*'
        regex = self.OBJ_TOKEN._get_obj_connection_token_(
            source_obj_path, source_port_path, target_obj_path, target_port_path
        )
        return self.universe.get_connections(
            regex=regex
        )
    @classmethod
    def _get_target_(cls, obj_connection):
        return obj_connection.target
    @classmethod
    def _get_target_obj_(cls, obj_connection):
        return obj_connection.target_obj

    def get_target_connections(self):
        """
        :return: list[instance(<obj-connection>), ...]
        """
        return self._get_target_connections_(self.path)

    def get_targets(self):
        return [self._get_target_(i) for i in self.get_target_connections()]

    def get_target_objs(self):
        return [self._get_target_obj_(i) for i in self.get_target_connections()]

    def _get_all_target_connections_(self, obj_path):
        def _rcs_fnc(obj_path_):
            _obj_connections = self._get_target_connections_(obj_path_)
            for _i in _obj_connections:
                lis.append(_i)
                _rcs_fnc(self._get_target_obj_(_i).path)

        lis = []
        _rcs_fnc(obj_path)
        return lis

    def get_all_target_connections(self):
        return self._get_all_target_connections_(self.path)

    def get_all_targets(self):
        return [self._get_target_(i) for i in self.get_all_target_connections()]

    def get_all_target_objs(self):
        return [self._get_target_obj_(i) for i in self.get_all_target_connections()]

    def _format_dict_(self):
        raise NotImplementedError()


class AbsObjPropertiesDef(object):
    PROPERTIES_CLASS = None
    def _set_obj_properties_def_init_(self):
        self._obj_properties = None
    @property
    def properties(self):
        return self._obj_properties
    @properties.setter
    def properties(self, raw):
        if isinstance(raw, dict):
            self._obj_properties = self.PROPERTIES_CLASS(self, raw)
        elif isinstance(raw, self.PROPERTIES_CLASS):
            self._obj_properties = raw
        else:
            raise TypeError()


class AbsObjAttributesDef(object):
    ATTRIBUTES_CLASS = None
    def _set_obj_attributes_def_init_(self):
        self._obj_attributes = {}
    @property
    def attributes(self):
        return self._obj_attributes
    @attributes.setter
    def attributes(self, raw):
        if isinstance(raw, dict):
            self._obj_attributes = self.ATTRIBUTES_CLASS(self, raw)
        elif isinstance(raw, self.ATTRIBUTES_CLASS):
            self._obj_attributes = raw
        else:
            raise TypeError()


# <obj>
class AbsObj(
    # <obj-type>
    AbsObjTypeDef,
    # <obj-dag>
    AbsObjDagDef,
    # <obj>
    AbsObjDef,
    # <obj-port>
    AbsObjPortDef,
    # <input-port>
    AbsObjSourceDef,
    # <output-port>
    AbsObjTargetDef,
    # <obj-gui>
    AbsObjGuiDef,
    AbsObjPropertiesDef,
    AbsObjAttributesDef,
):
    """
    abstract for <obj>
    """
    def __init__(self, obj_type, path):
        self._set_obj_type_def_init_(obj_type)
        self._set_obj_dag_def_init_(path)
        self._set_obj_def_init_(
            self._get_obj_name_(path)
        )
        self._set_node_port_def_init_()
        self._set_obj_gui_def_init_()
        self._set_obj_properties_def_init_()
        self._set_obj_attributes_def_init_()

    def _set_dag_create_(self, path):
        """
        :param path: str(<obj-path>)
        :return:
        """
        obj = self.universe.get_obj(path)
        if obj is not None:
            return obj
        else:
            obj = self.universe.get_obj_type(obj_configure.ObjType.NULL)._set_obj_create_(path)
            self.universe._set_obj_add_(obj)
            return obj

    def _get_child_paths_(self, path):
        lis = []
        obj_pathsep = self.PATHSEP
        obj_category_name = '*'
        obj_type_name = '*'
        obj_string_0 = '{}{}*'.format(self.path, obj_pathsep)
        regex = self.category._get_obj_token_(
            obj_category_name, obj_type_name, obj_string_0
        )
        #
        obj_string_1 = '{}{}*{}*'.format(path, obj_pathsep, obj_pathsep)
        pattern = self.category._get_obj_token_(
            obj_category_name, obj_type_name, obj_string_1
        )
        _ = self.universe._obj_stack.get_objects(regex=regex)
        for i in _:
            match = fnmatch.filter([i.path], pattern)
            if match:
                continue
            lis.append(i.path)
        return lis

    def _set_child_create_(self, path):
        return self.universe.get_obj(path)

    def get_descendant_paths(self):
        return [i.path for i in self.get_descendants()]

    def get_descendants(self):
        obj_pathsep = self.PATHSEP
        obj_category_name = '*'
        obj_type_name = '*'
        obj_string = '{}{}*'.format(self.path, obj_pathsep)
        regex = self.category._get_obj_token_(
            obj_category_name, obj_type_name, obj_string
        )
        return self.universe._obj_stack.get_objects(regex=regex)

    def _format_dict_(self):
        return {
            'self': self,
            'category': self.category,
            'type': self.type,
            'obj': self
        }

    def _get_stack_key_(self):
        obj_category_name = self.category.name
        obj_type_name = self.type.name
        obj_string = self.path
        return self.category._get_obj_token_(
            obj_category_name, obj_type_name, obj_string
        )

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type.path,
            self.path
        )

    def __repr__(self):
        return self.__str__()


# <obj-connection>
class AbsObjConnection(object):
    OBJ_TOKEN = None
    OBJ_PATHSEP = None
    def __init__(self, universe, source_obj_path, source_port_path, target_obj_path, target_port_path):
        self._universe = universe

        self._source_obj_path = source_obj_path
        self._source_port_path = source_port_path

        self._target_obj_path = target_obj_path
        self._target_port_path = target_port_path
    @property
    def universe(self):
        return self._universe
    # obj
    @property
    def source_obj(self):
        return self.universe.get_obj(self._source_obj_path)
    @property
    def target_obj(self):
        return self.universe.get_obj(self._target_obj_path)

    def get_source_obj(self):
        return self.universe.get_obj(self._source_obj_path)

    def get_target_obj(self):
        return self.universe.get_obj(self._target_obj_path)
    # port
    @property
    def source(self):
        port_token = self.OBJ_TOKEN._get_port_source_token_(self._source_port_path)
        return self.source_obj.get_port(port_token)
    @property
    def target(self):
        port_token = self.OBJ_TOKEN._get_port_target_token_(self._target_port_path)
        return self.target_obj.get_port(port_token)

    def _get_stack_key_(self):
        return self.OBJ_TOKEN._get_obj_connection_token_(
            self._source_obj_path, self._source_port_path,
            self._target_obj_path, self._target_port_path
        )

    def __str__(self):
        return '{}(source="{}", target="{}")'.format(
            self.__class__.__name__,
            self.OBJ_TOKEN._get_obj_source_token_(self._source_obj_path, self._source_port_path),
            self.OBJ_TOKEN._get_obj_target_token_(self._target_obj_path, self._target_port_path),
        )

    def __repr__(self):
        return self.__str__()


# <obj-bind>
class AbsObjBind(object):
    def __init__(self, universe, obj):
        self._universe = universe
        self._obj = obj
    @property
    def universe(self):
        return self._universe
    @property
    def obj(self):
        return self._obj

    def _get_stack_key_(self):
        pass

    def __str__(self):
        return '{}(obj="{}")'.format(
            self.__class__.__name__,
            self.obj.path
        )


# <obj-universe>
class AbsObjUniverseDef(object):
    ROOT = None
    # <type>
    CATEGORY_STACK_CLASS = None
    CATEGORY_CLASS = None
    TYPE_STACK_CLASS = None
    # <obj-type>
    OBJ_CATEGORY_STACK_CLASS = None
    OBJ_CATEGORY_CLASS = None
    OBJ_TYPE_STACK_CLASS = None
    #
    OBJ_STACK_CLASS = None
    #
    OBJ_CONNECTION_STACK_CLASS = None
    OBJ_CONNECTION_CLASS = None
    #
    OBJ_BIND_STACK_CLASS = None
    OBJ_BIND_CLASS = None
    #
    Category = obj_configure.Category
    Type = obj_configure.Type
    PortAssign = obj_configure.PortAssign
    #
    def _set_obj_universe_def_init_(self):
        # <type>
        self._category_stack = self.CATEGORY_STACK_CLASS()
        self._type_stack = self.TYPE_STACK_CLASS()
        # <obj-type>
        self._obj_category_stack = self.OBJ_CATEGORY_STACK_CLASS()
        self._obj_type_stack = self.OBJ_TYPE_STACK_CLASS()
        # <obj>
        self._obj_stack = self.OBJ_STACK_CLASS()
        # <obj-connection>
        self._obj_connection_stack = self.OBJ_CONNECTION_STACK_CLASS()
        self._obj_bind_stack = self.OBJ_BIND_STACK_CLASS()
        #
        self._custom_raw = {}
        #
        for obj_category_name in obj_configure.ObjCategory.ALL:
            obj_category = self._get_obj_category_force_(obj_category_name)
            obj_category._set_port_queries_build_(obj_configure.ObjCategory.PORT_QUERY_RAW)
        #
        for obj_category_name, obj_type_name in obj_configure.ObjType.ALL:
            obj_type = self._get_obj_type_force_(obj_category_name, obj_type_name)
            obj_type._set_port_queries_build_(obj_configure.ObjType.PORT_QUERY_RAW)
        #
        root_type = self.get_obj_type(obj_configure.ObjType.ROOT)
        root_type.set_obj_create(root_type.obj_pathsep)

    def set_gui_attribute(self, key, value):
        self._custom_raw[key] = value

    def get_gui_attribute(self, key, default=None):
        return self._custom_raw.get(key, default)
    # <category>
    def _set_category_create_as_new_(self, category_name):
        return self.CATEGORY_CLASS(self, category_name)

    def set_category_create(self, category_name):
        stack = self._category_stack
        if stack.get_object_exists(category_name) is True:
            return stack.get_object(category_name)
        obj_category = self._set_category_create_as_new_(category_name)
        stack.set_object_add(obj_category)
        return obj_category

    def _get_category_force_(self, category_name):
        return self.set_category_create(category_name)

    def get_categories(self):
        return self._category_stack.get_objects()

    def get_category(self, category_name):
        return self._category_stack.get_object(category_name)
    # <type>
    def _get_type_force_(self, category_name, type_name):
        category = self._get_category_force_(category_name)
        return category._get_type_force_(type_name)

    def _get_type_(self, type_path):
        stack = self._type_stack
        if stack.get_object_exists(type_path) is True:
            return stack.get_object(type_path)
        #
        category_name, type_name = self.CATEGORY_CLASS._get_type_path_args_(type_path)
        category = self._get_category_force_(category_name)
        type_ = category._set_type_create_as_new_(type_name)
        stack.set_object_add(type_)
        return type_

    def get_types(self):
        return self._type_stack.get_objects()

    def get_type(self, type_string):
        pathsep = self.CATEGORY_CLASS.PATHSEP
        if pathsep in type_string:
            regex = '{}'.format(type_string)
        else:
            regex = '*{}{}'.format(pathsep, type_string)
        #
        _ = self._type_stack.get_objects(
            regex=regex
        )
        if _:
            return _[-1]
    # <obj-category>
    def _set_obj_category_create_as_new_(self, obj_category_name):
        return self.OBJ_CATEGORY_CLASS(self, obj_category_name)

    def set_obj_category_create(self, obj_category_name):
        stack = self._obj_category_stack
        if stack.get_object_exists(obj_category_name) is True:
            return stack.get_object(obj_category_name)
        obj_category = self._set_obj_category_create_as_new_(obj_category_name)
        stack.set_object_add(obj_category)
        return obj_category

    def _get_obj_category_force_(self, obj_category_name):
        return self.set_obj_category_create(obj_category_name)

    def get_obj_categories(self):
        return self._obj_category_stack.get_objects()

    def get_obj_category(self, obj_category_name):
        return self._obj_category_stack.get_object(obj_category_name)
    # <obj-type>
    def _get_obj_type_force_(self, obj_category_name, obj_type_name):
        category = self._get_obj_category_force_(obj_category_name)
        return category._get_type_force_(obj_type_name)

    def get_obj_types(self):
        return self._obj_type_stack.get_objects()

    def get_obj_type(self, obj_type_string):
        pathsep = self.OBJ_CATEGORY_CLASS.PATHSEP
        if pathsep in obj_type_string:
            regex = '{}'.format(obj_type_string)
        else:
            regex = '*{}{}'.format(pathsep, obj_type_string)
        #
        _ = self._obj_type_stack.get_objects(
            regex=regex
        )
        if _:
            return _[-1]
    # <obj>
    def _set_obj_add_(self, obj):
        self._obj_stack.set_object_add(obj)

    def _set_obj_override_(self, old_obj, new_obj):
        """
        override <obj> by new <obj>
        :param old_obj: instance(<obj>)
        :param new_obj: instance(<obj>)
        :return:
        """
        self._obj_stack.set_object_override(old_obj, new_obj)
    # noinspection PyMethodMayBeStatic
    def _set_obj_copy_to_(self, source_obj, target_path):
        """
        copy a <obj> to a new <obj-path>
        :param source_obj: str(<obj-path>)
        :param target_path: str(<obj-path>)
        :return: None
        """
        obj_type = source_obj.type
        new_obj = obj_type.set_obj_create(target_path)
        port_dict = {}
        for port in source_obj.get_ports():
            key = port.port_path
            value = port.get()
            port_dict[key] = value
        [new_obj._set_port_build_(k, v) for k, v in port_dict.items()]

    def get_root(self):
        return self.get_obj(self.ROOT)

    def get_objs(self, regex=None):
        """
        :param regex: str("fnmatch regex-pattern")
        :return: list[instance(<obj>), ...]
        """
        return self._obj_stack.get_objects(regex)

    def get_obj(self, obj_string):
        """
        :param obj_string: str(<obj-path>) or str(<obj-name>)
        :return: instance(<obj>) or None
        """
        obj_pathsep = obj_configure.Obj.PATHSEP
        obj_category_name = '*'
        obj_type_name = '*'
        if obj_string.startswith(obj_pathsep):
            obj_path = obj_string
        else:
            obj_path = '*{}{}'.format(obj_pathsep, obj_string)
        regex = self.OBJ_CATEGORY_CLASS._get_obj_token_(
            obj_category_name, obj_type_name, obj_path
        )
        _ = self._obj_stack.get_objects(regex=regex)
        if _:
            return _[-1]

    def get_obj_exists(self, obj_string):
        """
        :param obj_string: str(<obj-path>) or str(<obj-name>)
        :return: bool
        """
        obj_pathsep = obj_configure.Obj.PATHSEP
        obj_category_name = '*'
        obj_type_name = '*'
        if obj_string.startswith(obj_pathsep):
            obj_path = obj_string
        else:
            obj_path = '*{}{}'.format(obj_pathsep, obj_string)
        regex = self.OBJ_CATEGORY_CLASS._get_obj_token_(
            obj_category_name, obj_type_name, obj_path
        )
        return self._obj_stack.get_objects_exists(regex=regex)
    # <obj-connection>
    def set_connection_create(self, source_obj_args, source_port_args, target_obj_args, target_port_args):
        obj_connection = self._set_connection_create_(
            source_obj_args, source_port_args, target_obj_args, target_port_args
        )
        self._obj_connection_stack._set_object_register_(obj_connection)
        return obj_connection
    #
    def _set_connection_create_(self, source_obj_args, source_port_args, target_obj_args, target_port_args):
        def get_obj_path_fnc_(obj_args_):
            if isinstance(obj_args_, (str, unicode)):
                return obj_args_
            elif isinstance(obj_args_, (tuple, list)):
                return self.OBJ_CONNECTION_CLASS.OBJ_PATHSEP.join(obj_args_)
        #
        def get_port_path_fnc_(port_args_):
            if isinstance(port_args_, (str, unicode)):
                return port_args_
            elif isinstance(port_args_, (tuple, list)):
                return self.OBJ_CONNECTION_CLASS.PORT_PATHSEP.join(port_args_)
        #
        obj_connection = self.OBJ_CONNECTION_CLASS(
            self,
            get_obj_path_fnc_(source_obj_args), get_port_path_fnc_(source_port_args),
            get_obj_path_fnc_(target_obj_args), get_port_path_fnc_(target_port_args)
        )
        return obj_connection

    def get_connections(self, regex=None):
        return self._obj_connection_stack.get_objects(regex)

    def get_connections_exists(self, regex=None):
        return self._obj_connection_stack.get_objects_exists(regex)

    def set_bind_create(self):
        pass

    def _set_bind_create_(self):
        pass

    def get_as_dict(self):
        content = bsc_objects.Content()
        for obj in self.get_objs():
            key = obj.path
            #
            content.set(
                key,
                collections.OrderedDict()
            )
            content.set(
                '{}.properties.type'.format(key),
                obj.type.path
            )
            if hasattr(obj, '_temp_attributes'):
                content.set(
                    '{}.properties.attributes'.format(key), obj._temp_attributes
                )
            if hasattr(obj, '_temp_customize_attributes'):
                content.set(
                    '{}.properties.customize-attributes'.format(key), obj._temp_customize_attributes
                )
        #
        return content

    def get_basic_source_objs(self, objs=None):
        if isinstance(objs, (tuple, list)):
            return [i for i in objs if not i.get_target_connections()]
        else:
            return [i for i in self.get_objs() if not i.get_target_connections()]


class AbsObjUniverse(
    AbsObjDef,
    AbsObjUniverseDef
):
    def __init__(self):
        self._set_obj_def_init_('default')
        self._set_obj_universe_def_init_()


# os
class AbsOsFilePackageDef(object):
    PATHSEP = None
    @property
    def path(self):
        raise NotImplementedError()

    def _set_os_file_package_def_init_(self):
        pass

    def get_package_path(self, target_path):
        if not target_path.endswith(self.PATHSEP):
            format_string = u'{}/{}'
        else:
            format_string = u'{}{}'
        return format_string.format(target_path, self.path)


class AbsOsDirectory(
    AbsObjDagDef,
    AbsObjDef,
    AbsObjOsDef
):
    # <obj-pathsep>
    LOG = None
    PATHSEP = '/'
    def __init__(self, path):
        self._set_obj_dag_def_init_(path)
        self._set_obj_def_init_(
            self._get_obj_name_(path)
        )
        self._set_obj_os_def_init_()
    # dag
    def _set_dag_create_(self, path):
        return self.__class__(path)

    def _get_child_paths_(self, path, includes=None):
        return bsc_core.DirectoryMtd.get_directory_paths__(
            path
        )

    def _set_child_create_(self, path):
        return self.__class__(path)
    @property
    def type(self):
        return 'directory'
    @property
    def type_path(self):
        return 'storage/{}'.format(self.type_name)
    @property
    def type_name(self):
        return 'directory'
    #
    def get_root(self):
        return self._set_dag_create_(self._root)
    # os
    def get_is_directory(self):
        return True

    def get_is_file(self):
        return False

    def get_is_exists(self):
        if self.path is not None:
            return os.path.isdir(self.path)
        return False

    def set_create(self):
        raise NotImplementedError()

    def get_child_file_paths(self):
        return bsc_core.DirectoryMtd.get_file_paths__(
            self.path
        )

    def set_copy_to(self, tgt_directory_path):
        if os.path.exists(tgt_directory_path) is False:
            shutil.copytree(
                self.path, tgt_directory_path
            )

    def get_file_paths(self, include_exts=None):
        return bsc_core.DirectoryMtd.get_file_paths__(
            self.path, include_exts
        )

    def get_all_file_paths(self, include_exts=None):
        return bsc_core.DirectoryMtd.get_all_file_paths__(
            self.path, include_exts
        )

    def set_copy_to_directory(self, tgt_directory_path):
        def copy_fnc_(src_file_path_, tgt_file_path_):
            shutil.copy2(src_file_path_, tgt_file_path_)
            self.LOG.set_module_result_trace(
                'file copy',
                u'file="{}" >> "{}"'.format(src_file_path_, tgt_file_path_)
            )
        #
        src_directory_path = self.path
        file_paths = self.get_all_file_paths()
        #
        threads = []
        for i_src_file_path in file_paths:
            i_local_file_path = i_src_file_path[len(src_directory_path):]
            #
            i_tgt_file_path = tgt_directory_path + i_local_file_path
            if os.path.exists(i_tgt_file_path) is False:
                i_tgt_dir_path = os.path.dirname(i_tgt_file_path)
                if os.path.exists(i_tgt_dir_path) is False:
                    os.makedirs(i_tgt_dir_path)
                    self.LOG.set_module_result_trace(
                        'directory create',
                        u'directory="{}"'.format(i_tgt_dir_path)
                    )
                #
                i_thread = bsc_core.PyThread(
                    copy_fnc_, i_src_file_path, i_tgt_file_path
                )
                threads.append(i_thread)
                i_thread.start()
        #
        [i.join() for i in threads]

    def set_open(self):
        if os.path.exists(self.path):
            bsc_core.SystemMtd.set_directory_open(self.path)

    def __str__(self):
        return u'{}(path="{}")'.format(
            self.__class__.__name__,
            self.path
        ).encode('utf-8')

    def __repr__(self):
        return self.__str__()


class AbsOsFile(
    AbsObjDagDef,
    AbsObjDef,
    AbsObjOsDef
):
    # dag
    PATHSEP = '/'
    # os
    OS_DIRECTORY_CLASS = None
    #
    LOG = None
    def __init__(self, path):
        self._set_obj_dag_def_init_(path)
        self._set_obj_def_init_(
            self._get_obj_name_(path)
        )
        self._set_obj_os_def_init_()
    @classmethod
    def _get_ext_split_(cls, text):
        return os.path.splitext(text)

    def get_ext_split(self):
        return self._get_ext_split_(self.path)
    # dag
    def _set_dag_create_(self, path):
        return self.OS_DIRECTORY_CLASS(path)

    def _set_child_create_(self, path):
        raise TypeError()
    # child
    def _get_child_paths_(self, path):
        return []
    @property
    def type(self):
        if self.ext:
            return self.ext[1:]
        return '*'
    @property
    def type_path(self):
        return 'storage/{}'.format(self.type_name)
    @property
    def type_name(self):
        if self.ext:
            return self.ext[1:]
        return '*'
    #
    def get_root(self):
        return self._set_dag_create_(self._root)
    # os
    def get_is_directory(self):
        return False

    def get_is_file(self):
        return True

    def get_is_exists(self):
        if self.path is not None:
            return os.path.isfile(self.path)
        return False

    def set_create(self):
        pass
    # file
    @property
    def base(self):
        return os.path.splitext(self.name)[0]
    @property
    def name_base(self):
        return os.path.splitext(self.name)[0]
    @property
    def path_base(self):
        return os.path.splitext(self.path)[0]
    @property
    def ext(self):
        return os.path.splitext(self.path)[-1]
    @property
    def directory(self):
        return self.get_parent()

    def set_directory_open(self):
        if self.get_is_exists_file() is True:
            if self.get_is_windows():
                cmd = u'explorer /select,"{}"'.format(self.path.replace('/', '\\'))
                subprocess.Popen(cmd, shell=True)
            elif self.get_is_linux():
                cmd = u'nautilus "{}" --select'.format(self.path)
                subprocess.Popen(cmd, shell=True)
        elif self.directory.get_is_exists() is True:
            if self.get_is_windows():
                cmd = u'explorer "{}"'.format(self.directory.path.replace('/', '\\'))
                subprocess.Popen(cmd, shell=True)
            elif self.get_is_linux():
                cmd = u'nautilus "{}"'.format(self.directory.path)
                subprocess.Popen(cmd, shell=True)

    def set_copy_to(self, target_dir_path, ignore_structure=True):
        if self.get_is_exists() is True:
            if isinstance(target_dir_path, (str, unicode)):
                target_dir_path = [target_dir_path]
            #
            for i_directory_path_tgt in target_dir_path:
                target_file_path = self.get_target_file_path(i_directory_path_tgt, ignore_structure=ignore_structure)
                if os.path.exists(target_file_path) is False:
                    target_directory = os.path.dirname(target_file_path)
                    if os.path.exists(target_directory) is False:
                        os.makedirs(target_directory)
                        self.LOG.set_result_trace(
                            'directory create: "{}"'.format(target_directory)
                        )
                    shutil.copy2(self.path, target_file_path)
                    self.LOG.set_result_trace(
                        'file copy: "{}" >> "{}"'.format(self.path, target_file_path))
                else:
                    self.LOG.set_warning_trace('file copy: target "{}" is exist.'.format(target_file_path))
        else:
            self.LOG.set_warning_trace('file copy: source "{}" is Non-exist.'.format(self.path))

    def get_target_file_path(self, tgt_directory_path, fix_name_blank=False, ignore_structure=True, ext_override=None):
        tgt_directory_path = bsc_core.StoragePathOpt(tgt_directory_path).__str__()
        if ignore_structure is True:
            name = self.name
            if fix_name_blank is True:
                if ' ' in name:
                    name = name.replace(' ', '_')
            if ext_override is not None:
                base, ext = os.path.splitext(name)
                name = '{}{}'.format(base, ext_override)
            return u'{}/{}'.format(tgt_directory_path, name)
        else:
            return u'{}/{}'.format(tgt_directory_path, self.path)

    def get_target_file(self, tgt_directory_path):
        return self.__class__(
            self.get_target_file_path(tgt_directory_path)
        )

    def set_directory_create(self):
        self.directory.set_create()

    def set_copy_to_file(self, target_file_path, force=False):
        if force is True:
            if os.path.exists(target_file_path):
                os.remove(target_file_path)
        #
        if os.path.exists(target_file_path) is False:
            target_directory = os.path.dirname(target_file_path)
            if os.path.exists(target_directory) is False:
                os.makedirs(target_directory)
                self.LOG.set_module_result_trace(
                    'directory create',
                    u'directory="{}"'.format(target_directory)
                )
            # noinspection PyBroadException
            try:
                shutil.copy2(self.path, target_file_path)
                self.LOG.set_module_result_trace(
                    'file copy',
                    u'file="{}" >> "{}"'.format(self.path, target_file_path)
                )
            except:
                bsc_core.ExceptionMtd.set_print()
                return self.path

    def get_orig_file(self, ext):
        if self.ext == ext:
            base, ext = os.path.splitext(self.path)
            glob_pattern = u'{}.*'.format(base)
            _ = bsc_core.DirectoryMtd.get_file_paths_by_glob_pattern__(
                glob_pattern
            )
            lis = []
            if _:
                for i in _:
                    if i == self.path:
                        continue
                    lis.append(i)
            if lis:
                return lis[0]

    def __str__(self):
        return u'{}(path="{}")'.format(
            self.__class__.__name__,
            self.path
        ).encode('utf-8')

    def __repr__(self):
        return self.__str__()


# value
class AbsValue(object):
    def __init__(self, type_, raw):
        self._type = type_
        self._raw = raw
    @property
    def universe(self):
        return self.type.universe
    @property
    def type(self):
        return self._type
    @property
    def type_path(self):
        return self.type.path
    @property
    def type_name(self):
        return self.type.name
    # <type-constant>
    def get_is_constant(self):
        return self.type.get_is_constant()

    def get_is_boolean(self):
        return self.type.get_is_boolean()
    # <type-tuple>
    def get_is_vector(self):
        return self.type.get_is_vector()

    def get_is_color(self):
        return self.type.get_is_color()

    def get_is_tuple(self):
        return self.type.get_is_tuple()

    def get_tuple_size(self):
        return self.type.get_tuple_size()

    def get_channel(self, index):
        if self.get_is_array() is False:
            channel_type = self.type.get_channel_type()
            tuple_size = self.get_tuple_size()
            if tuple_size > 0:
                if index > tuple_size:
                    return channel_type.set_value_create(None)
                return channel_type.set_value_create(self.get()[index])
            return channel_type.set_value_create(None)
    # <type-matrix>
    def get_is_matrix(self):
        return self.type.get_is_matrix()
    # <type-array>
    def get_is_array(self):
        return self.type.get_is_array()

    def get_array_size(self):
        if self.get_is_array():
            return len(self.get())
        return 0

    def get_element(self, index):
        if self.get_is_array():
            element_type = self.type.get_element_type()
            array_size = self.get_array_size()
            if array_size > 0:
                if index > array_size:
                    return element_type.set_value_create(None)
                return element_type.set_value_create(self.get()[index])
            return element_type.set_value_create(None)
    #
    def get(self):
        return self._raw

    def set(self, raw):
        self._raw = raw

    def get_as_string(self):
        if self.get_is_array():
            return u', '.join([self.get_element(i).get_as_string() for i in range(self.get_array_size())])
        elif self.type.get_is_vector() or self.type.get_is_color():
            return u','.join([self.get_channel(i).get_as_string() for i in range(self.get_tuple_size())])
        elif self.type.get_is_matrix():
            return u', '.join([self.get_channel(i).get_as_string() for i in range(self.get_tuple_size())])
        else:
            if self.get_is_boolean():
                return [u'false', u'true'][self.get()]
            else:
                return unicode(self.get())

    def get_as_obj(self):
        obj_string = self.get()
        if isinstance(obj_string, (str, unicode)):
            return self.universe.get_obj(obj_string)

    def _format_dict_(self):
        return {
            'category': self.type.category,
            'type': self.type
        }

    def __str__(self):
        return 'Value(type="{}", raw="{}")'.format(
            self.type.path,
            self.get_as_string(),
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.get() == other.get()

    def __ne__(self, other):
        return self.get() != other.get()


class AbsObjScene(object):
    FILE_CLASS = None
    UNIVERSE_CLASS = None
    def __init__(self, *args, **kwargs):
        self._universe = self.UNIVERSE_CLASS()
        self._path_lstrip = None
    @property
    def universe(self):
        return self._universe
    @property
    def root_lstrip(self):
        return self._path_lstrip

    def set_restore(self):
        self._universe = self.UNIVERSE_CLASS()
        self._path_lstrip = None
