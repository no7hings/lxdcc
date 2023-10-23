# coding:utf-8
import os

import sys

import six

import fnmatch

import collections

import json

import re

import copy

import lxlog.core as log_core

import lxcontent.core as ctt_core


class CttBase(object):
    _RE_PATTERN = r'[\\][<](.*?)[\\][>]'
    VARIANT_RE_PATTERN = r'[<](.*?)[>]'

    PATHSEP = '.'

    @classmethod
    def __find_children(cls, path, paths):
        lis = []
        pathsep = cls.PATHSEP
        # etc. r'/shl/chr/test_0/[^/]*'
        if path == pathsep:
            ptn = r'{1}[^{1}]*'.format(path, pathsep)
        else:
            ptn = r'{0}{1}[^{1}]*'.format(path, pathsep)
        #
        for i_path in paths:
            if i_path != pathsep:
                _ = re.match(
                    ptn, i_path
                )
                if _ is not None:
                    if _.group() == i_path:
                        lis.append(i_path)
        return lis

    @classmethod
    def get_absolute_key_name(cls, relative_key, key_local):
        _ = relative_key.split('.')
        es = len([i for i in _ if i == ''])
        return key_local.split('.')[-es]

    @classmethod
    def get_absolute_key_index(cls, relative_key, key_local, keys_all):
        _ = relative_key.split('.')
        es = len([i for i in _ if i == ''])
        k = '.'.join(key_local.split('.')[:-es+1])
        p = '.'.join(key_local.split('.')[:-es])
        cs = cls.__find_children(p, keys_all)
        return cs.index(k)

    @classmethod
    def get_absolute_key(cls, relative_key, key_local):
        _ = relative_key.split('.')
        es = len([i for i in _ if i == ''])
        p = '.'.join(key_local.split('.')[:-es])
        if p:
            return '{}.{}'.format(p, '.'.join(_[es:]))
        else:
            return '.'.join(_[es:])

    @classmethod
    def unfold_fnc(cls, key, keys_all, keys_exclude, get_fnc):
        def rcs_fnc_(key_, value_):
            if isinstance(value_, six.string_types):
                _value_unfold = value_
                # collection excludes, etc. "\\<a\\>"
                _v_ks_0 = re.findall(re.compile(cls._RE_PATTERN, re.S), _value_unfold)
                if _v_ks_0:
                    for _i_v_k_0 in _v_ks_0:
                        keys_exclude.append(_i_v_k_0)
                        _value_unfold = _value_unfold.replace('\\<', '<').replace('\\>', '>')
                # etc. "<a>"
                else:
                    _v_ks_1 = re.findall(re.compile(cls.VARIANT_RE_PATTERN, re.S), _value_unfold)
                    if _v_ks_1:
                        for _i_v_k_1 in set(_v_ks_1):
                            # etc. <a | b>, value=a or b
                            if '|' in _i_v_k_1:
                                _i_v_ks_2 = map(lambda x: x.strip(), _i_v_k_1.split('|'))
                                for _j_v_k_2 in _i_v_ks_2:
                                    if _j_v_k_2 not in keys_all:
                                        raise KeyError('key="{}" is non-exists'.format(_j_v_k_2))
                                    _j_v = get_fnc(_j_v_k_2)
                                    if _j_v is not None:
                                        _value_unfold = _j_v
                                        break
                            # etc. <a % str(x).lower()>, value=str(a).lower()
                            elif '%' in _i_v_k_1:
                                _i_v_ks_2 = map(lambda x: x.strip(), _i_v_k_1.split('%'))
                                _i_v_k_2 = _i_v_ks_2[0]
                                if fnmatch.filter([_i_v_k_2], '*.key'):
                                    _i_v_2 = cls.get_absolute_key_name(_i_v_k_2, key_)
                                elif fnmatch.filter([_i_v_k_2], '*.key_index'):
                                    _i_v_2 = cls.get_absolute_key_index(_i_v_k_2, key_, keys_all)
                                elif fnmatch.filter([_i_v_k_2], '.*'):
                                    _i_v_k_2_ = cls.get_absolute_key(_i_v_k_2, key_)
                                    if _i_v_k_2_ in keys_exclude:
                                        continue
                                    #
                                    if _i_v_k_2_ not in keys_all:
                                        raise KeyError('key="{}" is non-exists'.format(_i_v_k_2_))
                                    #
                                    _i_v_2 = get_fnc(_i_v_k_2_)
                                else:
                                    if _i_v_k_2 not in keys_all:
                                        raise KeyError('key="{}" is non-exists'.format(_i_v_k_2))
                                    _i_v_2 = get_fnc(_i_v_k_2)
                                _i_v_2_fnc = eval('lambda x: {}'.format(_i_v_ks_2[1]))
                                _value_unfold = _value_unfold.replace('<{}>'.format(_i_v_k_1), _i_v_2_fnc(_i_v_2))
                            # etc. <a>, value=a
                            else:
                                # catch value
                                # etc. <a.key>
                                if fnmatch.filter([_i_v_k_1], '*.key'):
                                    _i_v_1 = cls.get_absolute_key_name(_i_v_k_1, key_)
                                elif fnmatch.filter([_i_v_k_1], '*.key_index'):
                                    _i_v_1 = cls.get_absolute_key_index(_i_v_k_1, key_, keys_all)
                                # etc. <.a>
                                elif fnmatch.filter([_i_v_k_1], '.*'):
                                    _i_v_k_1_ = cls.get_absolute_key(_i_v_k_1, key_)
                                    #
                                    if _i_v_k_1_ in keys_exclude:
                                        continue
                                    #
                                    if _i_v_k_1_ not in keys_all:
                                        raise KeyError('key="{}" is non-exists'.format(_i_v_k_1_))

                                    _i_v_1 = get_fnc(_i_v_k_1_)
                                    #
                                    _i_v_1 = rcs_fnc_(_i_v_k_1_, _i_v_1)
                                else:
                                    #
                                    if _i_v_k_1 in keys_exclude:
                                        continue
                                    if _i_v_k_1 not in keys_all:
                                        raise KeyError('key="{}" is non-exists'.format(_i_v_k_1))
                                    _i_v_1 = get_fnc(_i_v_k_1)
                                    #
                                    _i_v_1 = rcs_fnc_(_i_v_k_1, _i_v_1)
                                #
                                if isinstance(_i_v_1, six.string_types):
                                    _value_unfold = _value_unfold.replace('<{}>'.format(_i_v_k_1), _i_v_1)
                                elif isinstance(_i_v_1, (int, float, bool)):
                                    _value_unfold = _value_unfold.replace('<{}>'.format(_i_v_k_1), str(_i_v_1))
                    else:
                        _v_ks_0 = re.findall(re.compile(cls._RE_PATTERN, re.S), _value_unfold)
                # etc: "=0+1"
                if fnmatch.filter([_value_unfold], '=*'):
                    cmd = _value_unfold[1:]
                    _value_unfold = eval(cmd)
                return _value_unfold
            elif isinstance(value_, (tuple, list)):
                return [rcs_fnc_(key_, _i) for _i in value_]
            return value_

        #
        value = get_fnc(key)
        return rcs_fnc_(key, value)


class AbsContent(object):
    DEFAULT_VALUE = collections.OrderedDict()
    PATHSEP = None

    def __init__(self, key=None, value=None):
        self._key = key
        self.__file_path = None
        if isinstance(value, six.string_types):
            file_path = value
            if os.path.isfile(file_path):
                self.__file_path = value
                _ = ctt_core.CttFile(self.__file_path).read()
                if isinstance(_, dict):
                    self._value = _
                else:
                    self._value = collections.OrderedDict()
            else:
                raise OSError(
                    log_core.Log.trace_error(
                        'file is not found: "{}"'.format(value)
                    )
                )

        elif isinstance(value, dict):
            self._value = value
        else:
            self._value = collections.OrderedDict()

        self._unfold_excludes = []

    def save_to(self, file_path):
        ctt_core.CttFile(file_path).write(self._value)

    def save(self):
        ctt_core.CttFile(self.__file_path).write(self._value)

    @property
    def key(self):
        return self._key

    def get_value(self):
        return self._value

    value = property(get_value)

    def set_value(self, value):
        self._value = value

    def get_copy_value(self):
        return copy.deepcopy(self._value)

    copy_value = property(get_copy_value)

    @classmethod
    def _to_key_path_(cls, key):
        return '/'+key.replace('.', '/')

    def _get_all_keys_(self):
        def rcs_fnc_(k_, v_):
            for _k, _v in v_.items():
                if k_ is not None:
                    _key = '{}.{}'.format(k_, _k)
                else:
                    _key = _k
                lis.append(_key)
                if isinstance(_v, dict):
                    rcs_fnc_(_key, _v)

        lis = []
        rcs_fnc_(self._key, self._value)
        return lis

    def _get_leaf_keys_(self):
        def rcs_fnc_(k_, v_):
            for _k, _v in v_.items():
                if k_ is not None:
                    _key = '{}.{}'.format(k_, _k)
                else:
                    _key = _k
                #
                if isinstance(_v, dict):
                    rcs_fnc_(_key, _v)
                    if not _v:
                        lis.append(_key)
                else:
                    lis.append(_key)

        lis = []
        rcs_fnc_(self._key, self._value)
        return lis

    def _get_leaf_values_(self):
        def rcs_fnc_(k_, v_):
            for _k, _v in v_.items():
                if k_ is not None:
                    _key = '{}.{}'.format(k_, _k)
                else:
                    _key = _k
                #
                if isinstance(_v, dict):
                    rcs_fnc_(_key, _v)
                else:
                    lis.append(_v)

        lis = []
        rcs_fnc_(self._key, self._value)
        return lis

    def get_leaf_key_as_paths(self):
        keys = self._get_leaf_keys_()
        return [self._to_key_path_(i) for i in keys]

    def get_leaf_keys(self):
        return self._get_leaf_keys_()

    def get_leaf_values(self):
        return self._get_leaf_values_()

    def get_keys(self, regex=None):
        _ = self._get_all_keys_()
        if regex is not None:
            return fnmatch.filter(_, regex)
        return _

    def get_key_as_paths(self):
        keys = self.get_keys()
        if keys:
            return ['/']+[self._to_key_path_(i) for i in keys]
        return []

    def get_top_keys(self):
        return self._value.keys()

    def get_keys_by_value(self):
        pass

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

    def get_branch_keys(self, key_path=None):
        if key_path:
            value = self.get(key_path)
            if isinstance(value, dict):
                return value.keys()
            return []
        return self.value.keys()

    def get_content(self, key_path):
        key = key_path.split(self.PATHSEP)[-1]
        value = self.get(key_path)
        return self._set_content_create_(key, value)

    def _set_content_create_(self, key, value):
        if isinstance(value, dict) is False:
            raise TypeError()
        return self.__class__(
            key, value
        )

    def set(self, key_path, value):
        ks = key_path.split(self.PATHSEP)
        v = self._value
        #
        maximum = len(ks)-1
        for seq, k in enumerate(ks):
            if seq == maximum:
                v[k] = value
            else:
                if k not in v:
                    v[k] = collections.OrderedDict()
                #
                v = v[k]

    def add_element(self, key, value):
        v = self.get(key)
        if isinstance(v, (tuple, list)):
            es = v
        else:
            es = []
            self.set(key, es)
        #
        if value not in es:
            es.append(value)

    def append_element(self, key, value):
        v = self.get(key)
        if isinstance(v, (tuple, list)):
            es = v
        else:
            es = []
            self.set(key, es)
        #
        es.append(value)

    def _unfold_quote_(self, key, keys_all):
        value = self.get(key)
        if isinstance(value, six.string_types):
            if fnmatch.filter([value], '$*'):
                v_k = value[1:].lstrip()
                if fnmatch.filter([v_k], '.*'):
                    _ = v_k.split('.')
                    c_2 = len([i for i in _ if i == ''])
                    k_p_2 = '.'.join(key.split('.')[:-c_2])
                    if k_p_2:
                        k_2 = '{}.{}'.format(k_p_2, '.'.join(_[c_2:]))
                    else:
                        k_2 = '.'.join(_[c_2:])
                else:
                    k_2 = v_k
                #
                if k_2 not in keys_all:
                    raise KeyError('key="{}" is non-exists'.format(k_2))
                # need use copy
                self.set(key, copy.deepcopy(self.get(k_2)))
            elif fnmatch.filter([value], '\\$*'):
                self.set(key, value.replace('\\$', '$'))

    def _unfold_inherit_and_override_(self, key, keys_all):
        # etc. $: <key-path>
        if fnmatch.filter([key], '*$'):
            value = self.get(key)
            if fnmatch.filter([value], '.*'):
                key_inherit = CttBase.get_absolute_key(value, key)
            else:
                key_inherit = value
            #
            if key_inherit not in keys_all:
                raise KeyError('key="{}" is non-exists'.format(key_inherit))
            #
            k = '.'.join(key.split('.')[:-1])
            inherit_dict = copy.deepcopy(
                self.get(key_inherit)
            )
            override_dict = copy.deepcopy(
                self.get(k)
            )
            override_dict.pop('$')
            inherit_dict.update(override_dict)
            self.set(k, inherit_dict)

    def get_key_is_exists(self, key):
        return key in self._get_all_keys_()

    def set_clear(self):
        self._value = collections.OrderedDict()

    def set_update(self, data):
        if isinstance(data, self.__class__):
            self._value.update(data.get_value())
        elif isinstance(data, dict):
            self._value.update(data)

    def update_from(self, content):
        if isinstance(content, self.__class__):
            for i_key in content._get_leaf_keys_():
                self.set(i_key, content.get(i_key))

    def get_str_as_yaml_style(self):
        return ctt_core.CttYamlBase.dump(
            self.value,
            indent=4,
            default_flow_style=False
        )

    def print_as_yaml_style(self):
        sys.stdout.write(
            self.get_str_as_yaml_style()+'\n'
        )

    def set_flatten(self):
        keys_all = self.get_keys()
        #
        for i_key in keys_all:
            i_value = self.get(i_key)
            if isinstance(i_value, dict) is False:
                self._unfold_inherit_and_override_(i_key, keys_all)
        #
        for i_key in keys_all:
            i_value = self.get(i_key)
            if isinstance(i_value, dict) is False:
                self._unfold_quote_(i_key, keys_all)
        #
        keys_all = self.get_keys()
        for i_key in keys_all:
            i_value = self.get(i_key)
            if isinstance(i_value, dict) is False:
                i_value = CttBase.unfold_fnc(
                    i_key,
                    keys_all=keys_all,
                    keys_exclude=self._unfold_excludes,
                    get_fnc=self.get
                )
                self.set(i_key, i_value)

    def get_is_empty(self):
        return not self._value

    def get_file_path(self):
        return self.__file_path

    def set_reload(self):
        if self.__file_path is not None:
            if os.path.isfile(self.__file_path):
                _ = ctt_core.CttFile(self.__file_path).read()
                if isinstance(_, dict):
                    self._value = _
                else:
                    self._value = collections.OrderedDict()

    def __str__(self):
        return json.dumps(
            self.value,
            indent=4
        )

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.__file_path
        )

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)