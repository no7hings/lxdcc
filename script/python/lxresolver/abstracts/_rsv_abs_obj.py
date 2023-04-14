# coding:utf-8
from __future__ import print_function

import six

import itertools

import functools

import os

import re

import glob

import platform

import fnmatch

import parse

import collections

import copy

import json

import threading

from lxbasic import bsc_core

from lxbasic.abstracts import _bsc_abs_obj

import lxbasic.objects as bsc_objects

import lxuniverse.abstracts as unr_abstracts

from lxresolver import rsv_configure, rsv_core

THREAD_MAXIMUM = threading.Semaphore(1024)


class MtdBasic(object):
    PATTERN_REF_RE_PATTERN = r'[<](.*?)[>]'
    PATTERN_KEY_RE_PATTERN = r'[{](.*?)[}]'
    #
    VERSION_ZFILL_COUNT = 3
    VERSION_FNMATCH_PATTERN = 'v{}'.format('[0-9]' * VERSION_ZFILL_COUNT)
    #
    URL_PATTERN = 'url://resolver?{parameters}'
    URL_PARAMETERS_PATTERN = '{key}={value}'
    @classmethod
    def _set_pattern_update_(cls, parse_pattern, **format_variant):
        if parse_pattern is not None:
            keys = cls._get_keys_by_parse_pattern_(parse_pattern)
            s = parse_pattern
            if keys:
                for key in keys:
                    if key in format_variant:
                        v = format_variant[key]
                        if v is not None and v != '*':
                            s = s.replace('{{{}}}'.format(key), format_variant[key])
            return s
        return parse_pattern
    @classmethod
    def _get_scheme_raw_(cls, file_path):
        if os.path.exists(file_path):
            ext = os.path.splitext(file_path)[-1]
            if ext in ['.json']:
                with open(file_path) as j:
                    return json.load(j, object_pairs_hook=collections.OrderedDict)
            elif ext in ['.yml']:
                with open(file_path) as y:
                    return bsc_core.OrderedYamlMtd.set_load(y)
            else:
                raise TypeError(
                    'ext: "{}" is not available'.format(ext)
                )
        else:
            raise TypeError(
                'file="{}" is Non-exists'.format(file_path)
            )
    @classmethod
    def _get_rsv_pattern_real_value_(cls, value, dic):
        def _rcs_fnc(v_):
            if isinstance(v_, six.string_types):
                _r = v_
                _ks = re.findall(re.compile(cls.PATTERN_REF_RE_PATTERN, re.S), v_)
                if _ks:
                    for _k in set(_ks):
                        if _k not in dic:
                            raise KeyError(u'keyword: "{}" is non-registered'.format(_k))
                        _v = dic[_k]
                        #
                        _v = _rcs_fnc(_v)
                        #
                        _r = _r.replace(u'<{}>'.format(_k), _v)
                return _r
            return v_
        return _rcs_fnc(value)
    @classmethod
    def set_version_validation(cls, text):
        if not fnmatch.filter([text], cls.VERSION_FNMATCH_PATTERN):
            raise TypeError('version: "{}" is Non-match "{}"'.format(text, cls.VERSION_FNMATCH_PATTERN))
    @classmethod
    def _get_parameter_by_url_(cls, url):
        dic = {}
        p = parse.parse(
            cls.URL_PATTERN, url
        )
        if p:
            parameters = p['parameters']
            results = parameters.split('&')
            for result in results:
                if result:
                    key, value = result.split('=')
                    dic[key] = value
            if 'file' in dic:
                k = dic['file']
                keyword = '{}-file'.format(k)
                dic['keyword'] = keyword
        else:
            raise TypeError(u'url: "{}" is Non-available')
        return dic
    @classmethod
    def _get_rsv_task_unit_obj_path_(cls, **kwargs):
        keys = [
            'project',
            #
            'role', 'sequence',
            #
            'asset', 'shot',
            #
            'step',
            'task',
            #
            'workspace',
            #
            'version',
            #
            'unit',
        ]
        return '/' + '/'.join([kwargs[key] for key in keys if key in kwargs])
    @classmethod
    def _str_to_number_embedded_args_(cls, string):
        pieces = re.compile(r'(\d+)').split(unicode(string))
        pieces[1::2] = map(int, pieces[1::2])
        return pieces
    @classmethod
    def _get_fnmatch_pattern_by_parse_pattern_(cls, pattern):
        keys = cls._get_keys_by_parse_pattern_(pattern)
        s = pattern
        if keys:
            for i_key in keys:
                s = s.replace('{{{}}}'.format(i_key), '*')
            return True, s
        return False, s
    @classmethod
    def _update_fnmatch_pattern_by_parse_pattern_(cls, parse_pattern, **kwargs):
        keys = cls._get_keys_by_parse_pattern_(parse_pattern)
        s = parse_pattern
        if keys:
            for i_key in keys:
                if i_key in kwargs:
                    s = s.replace('{{{}}}'.format(i_key), kwargs[i_key])
                else:
                    s = s.replace('{{{}}}'.format(i_key), '*')
            return s
        return s
    @classmethod
    def _get_keys_by_parse_pattern_(cls, pattern):
        lis_0 = re.findall(re.compile(cls.PATTERN_KEY_RE_PATTERN, re.S), pattern)
        lis_1 = list(set(lis_0))
        lis_1.sort(key=lis_0.index)
        return lis_1
    @classmethod
    def _get_stg_paths_by_parse_pattern_(cls, pattern, trim=None):
        if pattern is not None:
            enable, glob_pattern = cls._get_fnmatch_pattern_by_parse_pattern_(pattern)
            if enable is True:
                _ = glob.glob(glob_pattern) or []
                if _:
                    # sort by number
                    _.sort(key=lambda x: cls._str_to_number_embedded_args_(x))
                    if trim is not None:
                        _ = _[trim[0]:trim[1]]
                    # fix windows path
                    if platform.system() == 'Windows':
                        _ = [i.replace('\\', '/') for i in _]
                return _
            else:
                return [glob_pattern]
        return []
    @classmethod
    def _set_name_check_(cls, rsv_type, name):
        _ = re.findall(
            r'[^a-zA-Z0-9_]',
            name
        )
        if _:
            if rsv_core.TRACE_WARNING_ENABLE is True:
                bsc_core.LogMtd.trace_method_warning(
                    'name check',
                    u'{}-name="{}" is not available'.format(rsv_type, name)
                )
            return False
        return True
    @classmethod
    def _set_rsv_obj_sort_(cls, rsv_objs):
        list_ = []
        paths = []
        obj_dic = {}
        for rsv_obj in rsv_objs:
            path = rsv_obj.path
            paths.append(path)
            obj_dic[path] = rsv_obj
        #
        paths.sort(key=lambda x: cls._str_to_number_embedded_args_(x))
        for path in paths:
            list_.append(
                obj_dic[path]
            )
        # print(paths)
        return list_


class RsvThread(threading.Thread):
    def __init__(self, fnc, *args, **kwargs):
        super(RsvThread, self).__init__()
        self._fnc = fnc
        self._args = args
        self._kwargs = kwargs
        #
        self._data = None
    #
    def set_data(self, data):
        self._data = data
    #
    def get_data(self):
        return self._data
    #
    def run(self):
        THREAD_MAXIMUM.acquire()
        self.set_data(
            self._fnc(*self._args, **self._kwargs)
        )
        THREAD_MAXIMUM.release()


class RsvSceneProperties(object):
    def __init__(self, rsv_project, dict_):
        pass


class RawOpt(object):
    PATHSEP = '.'
    PATTERN_REF_RE_PATTERN = r'[<](.*?)[>]'
    def __init__(self, dict_):
        self._dict = dict_
        self._keys_exclude = []

    def get_all_keys(self):
        def rcs_fnc_(k_, v_):
            for _k, _v in v_.items():
                if k_ is not None:
                    _key = '{}.{}'.format(k_, _k)
                else:
                    _key = _k
                #
                lis.append(_key)
                if isinstance(_v, dict):
                    rcs_fnc_(_key, _v)
        #
        lis = []
        rcs_fnc_(None, self._dict)
        return lis

    def get_keys(self, pattern=None):
        _ = self.get_all_keys()
        if pattern is not None:
            return fnmatch.filter(_, pattern)
        return _

    def get(self, key_path, default_value=None):
        ks = key_path.split(self.PATHSEP)
        v = self._dict
        for k in ks:
            if isinstance(v, dict):
                if k in v:
                    v = v[k]
                else:
                    return default_value
            else:
                return default_value
        return v

    def set(self, key_path, value):
        ks = key_path.split(self.PATHSEP)
        v = self._dict
        #
        maximum = len(ks) - 1
        for seq, k in enumerate(ks):
            if seq == maximum:
                v[k] = value
            else:
                if k not in v:
                    v[k] = collections.OrderedDict()
                #
                v = v[k]

    def unfold_value(self, value):
        def rcs_fnc_(v_):
            if isinstance(v_, six.string_types):
                _r = v_
                _ks = re.findall(re.compile(self.PATTERN_REF_RE_PATTERN, re.S), v_)
                if _ks:
                    for _k in set(_ks):
                        if _k not in self._dict:
                            raise KeyError(u'keyword: "{}" is non-registered'.format(_k))
                        #
                        _v = self._dict[_k]
                        #
                        _v = rcs_fnc_(_v)
                        #
                        _r = _r.replace(u'<{}>'.format(_k), _v)
                return _r
            return v_
        return rcs_fnc_(value)

    def get_content_as_unfold(self, key):
        c = bsc_objects.Configure(value=collections.OrderedDict())
        keys = self.get_keys('{}.*'.format(key))
        for i_key in keys:
            i_value = self.get_as_unfold(i_key)
            i_key_ = i_key[len(key)+1:]
            c.set(i_key_, i_value)
        return c

    def get_as_unfold(self, key):
        keys_all = self.get_all_keys()
        return _bsc_abs_obj._ContentMtd.unfold_fnc(
            key, keys_all, self._keys_exclude, self.get
        )


# <rev-version>
class AbsRsvVersionKey(object):
    VERSION_ZFILL_COUNT = 3
    VERSION_FNMATCH_PATTERN = 'v{}'.format('[0-9]'*VERSION_ZFILL_COUNT)
    def __init__(self, text):
        MtdBasic.set_version_validation(text)
        #
        self._text = text
        self._number = int(text[-self.VERSION_ZFILL_COUNT:])
    @property
    def number(self):
        return self._number

    def __str__(self):
        return self._text

    def __iadd__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError()
        self._number += int(other)
        self._text = 'v{}'.format(str(self._number).zfill(self.VERSION_ZFILL_COUNT))
        return self

    def __isub__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError()
        if self._number >= other:
            self._number -= int(other)
        else:
            self._number = 0
        self._text = 'v{}'.format(str(self._number).zfill(self.VERSION_ZFILL_COUNT))
        return self


class AbsRsvPattern(object):
    def __init__(self, raw):
        self._raw = raw
    @property
    def raw(self):
        return self._raw

    def set_update(self, **kwargs):
        return MtdBasic._set_pattern_update_(
            self._raw, **kwargs
        )

    def set_update_to(self, **kwargs):
        self._raw = MtdBasic._set_pattern_update_(
            self._raw, **kwargs
        )

    def get_results(self):
        return MtdBasic._get_stg_paths_by_parse_pattern_(
            self._raw
        )

    def __str__(self):
        return '{}(raw="{}")'.format(
            self.__class__.__name__,
            self._raw
        )

    def __repr__(self):
        return self.__str__()


class AbsRsvPropertiesDef(object):
    PROPERTIES_CLASS = None
    def _set_rsv_properties_def_init_(self):
        pass

    def get_properties(self, file_path):
        pass


# <rev-pattern>
class AbsRsvMatcher(
    AbsRsvPropertiesDef
):
    PATTERN_REF_RE_PATTERN = r'[<](.*?)[>]'
    PATTERN_KEY_RE_PATTERN = r'[{](.*?)[}]'
    #
    RSV_MATCH_PATTERN_CLASS = None
    #
    RSV_VERSION_KEY_CLASS = None
    def __init__(self, rsv_obj, pattern, format_dict=None):
        self._set_rsv_properties_def_init_()
        #
        if isinstance(rsv_obj, AbsRsvProject):
            self._rsv_project = rsv_obj
        else:
            self._rsv_project = rsv_obj._rsv_project
        #
        self._match_variants = format_dict
        self._extend_variants = {}
        self._orig_pattern = pattern
        self._match_patterns = []
        #
        # print(format_dict['keyword'])
        #
        self._rsv_properties = self.PROPERTIES_CLASS(
            None,
            copy.copy(self._rsv_project.properties.value)
        )
        self.__set_rsv_variants_update_(format_dict)
        #
        self._results = []
        self._matches = []
    #
    def _matcher__get_fnmatch_pattern_by_parse_pattern_(self, pattern):
        dict_ = self._rsv_project.get_variant('variant-fnmatch-patterns')
        keys = MtdBasic._get_keys_by_parse_pattern_(pattern)
        s = pattern
        if keys:
            for i_key in keys:
                if i_key in dict_:
                    i_glob_pattern = dict_[i_key]
                    i_glob_pattern = MtdBasic._update_fnmatch_pattern_by_parse_pattern_(
                        i_glob_pattern, **self._match_variants
                    )
                else:
                    i_glob_pattern = '*'
                #
                s = s.replace('{{{}}}'.format(i_key), i_glob_pattern)
            return True, s
        if '*' in s:
            return True, s
        return False, s
    #
    def _matcher__get_stg_paths_by_parse_pattern_(self, pattern, trim=None):
        if pattern is not None:
            enable, glob_pattern = self._matcher__get_fnmatch_pattern_by_parse_pattern_(pattern)
            if enable is True:
                _ = glob.glob(glob_pattern) or []
                if _:
                    # sort by number
                    _.sort(key=lambda x: MtdBasic._str_to_number_embedded_args_(x))
                    if trim is not None:
                        _ = _[trim[0]:trim[1]]
                    # fix windows path
                    if platform.system() == 'Windows':
                        _ = [i.replace('\\', '/') for i in _]
                return True, _
            #
            if os.path.exists(glob_pattern):
                return False, [glob_pattern]
        return False, []

    def set_extend_variants(self, **kwargs):
        self._extend_variants = kwargs

    def get_results(self, trim=None):
        list_ = []
        for i_pattern in self._match_patterns:
            _, i_results = self._matcher__get_stg_paths_by_parse_pattern_(i_pattern, trim)
            list_.extend(i_results)
            return list_

    def _matcher__get_matches_(self, trim):
        list_ = []
        for i_pattern in self._match_patterns:
            i_enable, i_results = self._matcher__get_stg_paths_by_parse_pattern_(i_pattern)
            # print(i_pattern, i_results)
            # print('pattern is '.format(i_pattern))
            if trim is not None:
                i_results = i_results[trim[0]:trim[1]]
            #
            for j_result in i_results:
                j_p = parse.parse(
                    self._parse_pattern, j_result
                )
                if j_p:
                    j_variants = j_p.named
                    list_.append(
                        (j_result, j_variants)
                    )
        #
        return list_

    def __set_rsv_variants_update_(self, format_variant):
        if isinstance(format_variant, dict):
            for k, v in format_variant.items():
                if v is not None:
                    self._rsv_properties.set(k, v)
        #
        variants = self.__set_variants_completion_(self._rsv_properties.value)
        self._match_variants = variants
        #
        parse_variants = {
            'root': variants['root'],
        }
        #
        self._parse_pattern = MtdBasic._set_pattern_update_(
            self._orig_pattern, **parse_variants
        )
        #
        self._match_patterns = self.__get_match_patterns_(
            variants
        )
        # print(self._match_patterns)

    def __get_match_patterns_(self, variants):
        variants = self.__set_variants_completion_(variants)
        pattern = self._orig_pattern
        if pattern is not None:
            patterns = [
                pattern
            ]
            keys = MtdBasic._get_keys_by_parse_pattern_(pattern)
            if keys:
                for key in keys:
                    if key in variants:
                        v = variants[key]
                        if isinstance(v, six.string_types):
                            c = len(patterns)
                            for i_index in range(c):
                                if v != '*':
                                    patterns[i_index] = patterns[i_index].replace(u'{{{}}}'.format(key), v)
                        elif isinstance(v, (tuple, list)):
                            # update count
                            c = len(patterns)
                            v_c = len(v)
                            patterns *= v_c
                            for i_index in range(c):
                                for seq, i_v in enumerate(v):
                                    j_index = c*seq + i_index
                                    if i_v != '*':
                                        patterns[j_index] = patterns[j_index].replace(u'{{{}}}'.format(key), i_v)
            # print(patterns)
            return patterns

    def __set_variants_completion_(self, kwargs):
        root_choice = self._rsv_project._get_root_choice_(kwargs)
        root_cur = self._rsv_project._rsv_properties.get(root_choice)
        kwargs['root'] = root_cur
        return kwargs

    def get_matches(self, trim=None):
        return self._matcher__get_matches_(trim)

    def __get_path_by_local_variants_(self, format_dict):
        pattern = self._orig_pattern
        keys = MtdBasic._get_keys_by_parse_pattern_(pattern)
        for i in keys:
            if i not in format_dict:
                raise RuntimeError(
                    bsc_core.LogMtd.trace_method_error(
                        'path resolver',
                        'key "{}" in pattern "{}" is not value assigned'.format(
                            i,
                            pattern
                        )
                    )
                )
        new_result = pattern.format(**format_dict)
        return new_result

    def get_latest(self):
        matches = self._matcher__get_matches_(trim=(-1, None))
        if matches:
            result, parameters = matches[-1]
            format_dict = copy.copy(self._match_variants)
            format_dict.update(parameters)
            return self.__get_path_by_local_variants_(format_dict)
    @classmethod
    def _get_properties_by_result_(cls, pattern, properties, result):
        p = parse.parse(
            pattern, result
        )
        if p:
            dic = copy.copy(properties.value)
            dic.update(p.named)
            return cls.PROPERTIES_CLASS(None, dic)

    def get_properties_by_result(self, result):
        return self._get_properties_by_result_(
            self._parse_pattern,
            self._rsv_properties,
            result
        )

    def _get_project_properties_by_default_(self, result):
        properties_ = copy.copy(self._rsv_properties)
        properties_.set('project', '*')
        pattern = self._parse_pattern
        pattern = pattern.replace('default', '{project}')
        return self._get_properties_by_result_(
            pattern,
            properties_,
            result
        )
    @classmethod
    def _get_variants_by_result_(cls, pattern, properties, result):
        p = parse.parse(
            pattern, result
        )
        if p:
            variants = collections.OrderedDict()
            variants.update(p.named)
            return variants

    def get_new(self):
        matches = self.get_matches(trim=(-1, None))
        format_dict = copy.copy(self._match_variants)
        if matches:
            result, parameters = matches[-1]
            format_dict.update(parameters)
            if 'version' in format_dict:
                version = format_dict['version']
                rsv_version_key = self.RSV_VERSION_KEY_CLASS(version)
                rsv_version_key += 1
                format_dict['version'] = str(rsv_version_key)
                return self.__get_path_by_local_variants_(format_dict)
        else:
            format_dict['version'] = 'v001'
            return self.__get_path_by_local_variants_(format_dict)

    def get_current(self):
        format_dict = copy.copy(self._match_variants)
        return self.__get_path_by_local_variants_(format_dict)
    @classmethod
    def _set_rsv_version_key_create_(cls, version):
        return cls.RSV_VERSION_KEY_CLASS(version)

    def __str__(self):
        return '{}(pattern="{}")'.format(
            self.__class__.__name__,
            self._orig_pattern
        )


class AbsRsvDef(object):
    PATHSEP = '/'
    #
    Platforms = rsv_configure.Platforms
    Applications = rsv_configure.Applications
    VariantCategories = rsv_configure.VariantCategories
    VariantTypes = rsv_configure.VariantTypes
    VariantsKeys = rsv_configure.VariantsKeys
    Branches = rsv_configure.Branches
    WorkspaceKeys = rsv_configure.WorkspaceKeys
    WorkspaceMatchKeys = rsv_configure.WorkspaceMatchKeys


class AbsRsvObjDef(object):
    PATHSEP = '/'
    def _set_obj_def_init_(self):
        self._rsv_properties = None
        self._rsv_path = None
        self._rsv_matcher = None

    def _set_rsv_obj_def_init_(self, properties):
        self._rsv_path = properties.get('path')
        self._keyword = properties.get('keyword')
        self._pattern = properties.get('pattern')
        self._rsv_properties = properties
    @property
    def rsv_matcher(self):
        return self._rsv_matcher
    @property
    def properties(self):
        return self._rsv_properties

    def get(self, key):
        return self._rsv_properties.get(key)

    def set(self, key, value):
        self._rsv_properties.set(key, value)
    @property
    def type(self):
        return self.properties.get('type')
    @property
    def type_name(self):
        return self.type

    def get_name(self):
        return bsc_core.DccPathDagMtd.get_dag_name(self._rsv_path, pathsep=self.PATHSEP)
    name = property(get_name)
    @property
    def pattern(self):
        return self._pattern

    def _get_stack_key_(self):
        return self._rsv_path

    def get_path_args(self):
        types = [
            'project',
            #
            'role', 'sequence',
            #
            'asset', 'shot',
            #
            'step',
            'task'
        ]
        keys = MtdBasic._get_keys_by_parse_pattern_(self._pattern)
        dic = collections.OrderedDict()
        # dic['root'] = ''
        for i_type in types:
            if i_type in keys:
                i_name = self._rsv_properties.get(i_type)
                dic[i_name] = i_type
        return dic


class AbsRsvObj(
    AbsRsvDef,
    AbsRsvObjDef,
    AbsRsvPropertiesDef,
    unr_abstracts.AbsObjDagDef,
    # gui
    unr_abstracts.AbsObjGuiDef
):
    @classmethod
    def _completion_kwargs_from_parent_(cls, rsv_parent, kwargs):
        # do not override this keys
        for k, v in rsv_parent.properties.get_value().items():
            if k not in cls.VariantTypes.VariableTypes:
                kwargs[k] = v
    #
    def __init__(self, *args, **kwargs):
        self._set_rsv_properties_def_init_()
        self._set_obj_def_init_()
        #
        rsv_project = args[0]
        #
        self._rsv_project = rsv_project
        #
        self._set_rsv_obj_def_init_(
            self.PROPERTIES_CLASS(self, bsc_core.DictMtd.sort_key_to(kwargs))
        )
        self._set_obj_dag_def_init_(self._rsv_path)
        self._set_obj_gui_def_init_()
        #
        self._rsv_matcher = self._rsv_project._project__create_rsv_matcher_(
            self._rsv_properties.value
        )
        if self.type_name in self.VariantTypes.Trunks:
            self.set_gui_menu_raw(
                [
                    ('{}-directory'.format(self.type_name),),
                    ('Open Directory', 'file/folder', (self._get_source_directory_is_enable_, self._open_source_directory_open_, False)),
                ]
            )
        elif self.type_name in self.VariantTypes.Branches:
            self.set_gui_menu_raw(
                [
                    [
                        'Open Directory', 'file/folder',
                        [
                            ('{}-directory'.format(self.type_name),),
                            ('Source', 'file/folder',
                             (self._get_source_directory_is_enable_, self._open_source_directory_open_, False)),
                            ('User', 'file/folder',
                             (self._get_user_directory_is_enable_, self._open_user_directory_open_, False)),
                            ('Release', 'file/folder',
                             (self._get_release_directory_is_enable_, self._open_release_directory_open_, False)),
                            ('Temporary', 'file/folder',
                             (self._get_temporary_directory_is_enable_, self._open_temporary_directory_open_, False)),
                        ]
                    ]
                ]
            )
        #
        self.set_description(
            u'\n'.join([u'{} : {}'.format(k, v) for k, v in bsc_core.DictMtd.sort_key_to(kwargs).items()])
        )

    def get_rsv_project(self):
        return self._rsv_project

    def _get_valid_rsv_pattern_(self, **kwargs):
        rsv_type = self.type_name
        if rsv_type in self.VariantTypes.Trunks:
            key = '{type}-dir'.format(**kwargs)
            return self._rsv_project.get_pattern(key)
        elif rsv_type in self.VariantTypes.Branches:
            key = '{branch}-{workspace_key}-{type}-dir'.format(**kwargs)
            return self._rsv_project.get_pattern(key)
        return self._pattern
    # source
    def _get_source_directory_path_(self):
        kwargs = copy.copy(self.properties.value)
        kwargs['workspace'] = self.rsv_project.get_workspace_source()
        kwargs['workspace_key'] = self.WorkspaceKeys.Source
        p = self._get_valid_rsv_pattern_(**kwargs)
        return MtdBasic._set_pattern_update_(p, **kwargs)

    def _get_source_directory_is_enable_(self):
        directory_path = self._get_source_directory_path_()
        return bsc_core.StgDirectoryOpt(directory_path).get_is_exists()

    def _open_source_directory_open_(self):
        directory_path = self._get_source_directory_path_()
        bsc_core.StgDirectoryOpt(directory_path).set_open_in_system()
    # user
    def _get_user_directory_path_(self):
        kwargs = copy.copy(self.properties.value)
        kwargs['workspace'] = self.rsv_project.get_workspace_user()
        kwargs['workspace_key'] = self.WorkspaceKeys.User
        kwargs['artist'] = bsc_core.SystemMtd.get_user_name()
        p = self._get_valid_rsv_pattern_(**kwargs)
        return MtdBasic._set_pattern_update_(p, **kwargs)

    def _get_user_directory_is_enable_(self):
        directory_path = self._get_user_directory_path_()
        return bsc_core.StgDirectoryOpt(directory_path).get_is_exists()

    def _open_user_directory_open_(self):
        directory_path = self._get_user_directory_path_()
        bsc_core.StgDirectoryOpt(directory_path).set_open_in_system()
    # release
    def _get_release_directory_path_(self):
        kwargs = copy.copy(self.properties.value)
        kwargs['workspace'] = self.rsv_project.get_workspace_release()
        kwargs['workspace_key'] = self.WorkspaceKeys.Release
        p = self._get_valid_rsv_pattern_(**kwargs)
        return MtdBasic._set_pattern_update_(p, **kwargs)

    def _get_release_directory_is_enable_(self):
        directory_path = self._get_release_directory_path_()
        return bsc_core.StgDirectoryOpt(directory_path).get_is_exists()

    def _open_release_directory_open_(self):
        directory_path = self._get_release_directory_path_()
        bsc_core.StgDirectoryOpt(directory_path).set_open_in_system()
    # temporary
    def _get_temporary_directory_path_(self):
        kwargs = copy.copy(self.properties.value)
        kwargs['workspace'] = self.rsv_project.get_workspace_temporary()
        kwargs['workspace_key'] = self.WorkspaceKeys.Temporary
        p = self._get_valid_rsv_pattern_(**kwargs)
        return MtdBasic._set_pattern_update_(p, **kwargs)

    def _get_temporary_directory_is_enable_(self):
        directory_path = self._get_temporary_directory_path_()
        return bsc_core.StgDirectoryOpt(directory_path).get_is_exists()

    def _open_temporary_directory_open_(self):
        directory_path = self._get_temporary_directory_path_()
        bsc_core.StgDirectoryOpt(directory_path).set_open_in_system()
    @property
    def rsv_project(self):
        return self._rsv_project
    @property
    def icon(self):
        return bsc_core.RscIconFileMtd.get('file/folder')

    def _set_dag_create_(self, path):
        return self.rsv_project._project__get_rsv_obj_(path)

    def _get_child_paths_(self, *args, **kwargs):
        return self.rsv_project._project__get_rsv_obj_child_paths_(self._rsv_path)

    def get_descendants(self):
        return self.rsv_project._project__get_rsv_objs_(regex='{}/*'.format(self.path))

    def _set_child_create_(self, path):
        return self.rsv_project._project__get_rsv_obj_(path)

    def get_location(self):
        return self.properties.get('result')

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type,
            self.path
        )

    def __repr__(self):
        return self.__str__()


class AbsRsvUnit(
    AbsRsvObj
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvUnit, self).__init__(*args, **kwargs)

    def get_result(self, version=None, extend_variants=None, trim=None):
        kwargs = copy.copy(self.properties.value)
        if version is None:
            version = rsv_configure.Version.LATEST
        #
        kwargs['workspace'] = self._rsv_project._project__guess_workspace_extra_(**kwargs)
        if extend_variants is not None:
            kwargs.update(extend_variants)
        #
        if version == rsv_configure.Version.LATEST:
            kwargs['version'] = '*'
            rsv_matcher = self.rsv_project._create_rsv_matcher_(
                self._pattern,
                kwargs
            )
            return rsv_matcher.get_latest()
        elif version == rsv_configure.Version.NEW:
            kwargs['version'] = '*'
            rsv_matcher = self.rsv_project._create_rsv_matcher_(
                self._pattern,
                kwargs
            )
            return rsv_matcher.get_new()
        elif version == rsv_configure.Version.ALL:
            kwargs['version'] = '*'
            rsv_matcher = self.rsv_project._create_rsv_matcher_(
                self._pattern,
                kwargs
            )
            return rsv_matcher.get_results(trim=trim)
        #
        kwargs['version'] = version
        rsv_matcher = self.rsv_project._create_rsv_matcher_(
            self._pattern,
            kwargs
        )
        return rsv_matcher.get_current()

    def get_exists_result(self, *args, **kwargs):
        result = self.get_result(*args, **kwargs)
        if result:
            if isinstance(result, six.string_types):
                if bsc_core.StorageMtd.get_is_exists(result):
                    return result
            elif isinstance(result, (tuple, list)):
                return result

    def get_results(self, version=None, check_exists=False, trim=None):
        kwargs = copy.copy(self.properties.value)
        if version is None:
            version = self.properties.get('version')
        #
        kwargs['workspace'] = self._rsv_project._project__guess_workspace_extra_(**kwargs)
        if version == rsv_configure.Version.LATEST:
            version = self.get_latest_version()
        elif version == rsv_configure.Version.NEW:
            version = self.get_new_version()
        #
        if version is not None:
            kwargs['version'] = version
            kwargs['workspace'] = self._rsv_project._project__guess_workspace_extra_(**kwargs)
            rsv_matcher = self.rsv_project._create_rsv_matcher_(
                self._pattern,
                kwargs
            )
            results = rsv_matcher.get_results(trim=trim)
            if check_exists is True:
                return self._set_exists_results_filter_(results)
            return results
        return []

    def get_exists_results(self, *args, **kwargs):
        kwargs['check_exists'] = True
        return self.get_results(*args, **kwargs)

    def get_other_result(self, **kwargs):
        pass
    #
    def _set_exists_results_filter_(self, results):
        keyword = self.properties.get('keyword')
        if keyword.endswith('-file'):
            return [i for i in results if os.path.isfile(i)]
        elif keyword.endswith('-dir'):
            return [i for i in results if os.path.isdir(i)]
    #
    def _get_results_(self):
        pass

    def get_latest_results(self):
        kwargs = copy.copy(self.properties.value)
        version = self.get_latest_version()
        if version is not None:
            kwargs['version'] = version
            kwargs['workspace'] = self._rsv_project._project__guess_workspace_extra_(**kwargs)
            rsv_matcher = self.rsv_project._create_rsv_matcher_(
                self._pattern,
                kwargs
            )
            return rsv_matcher.get_results()

    def get_extend_variants(self, file_path):
        variants = self._rsv_properties.value
        pattern = self._pattern
        rsv_matcher = self._rsv_project._create_rsv_matcher_(
            pattern,
            dict(
                type='unit',
                workspace=self._rsv_project.get_workspace_release()
            )
        )
        cur_variants = rsv_matcher.get_properties_by_result(result=file_path)
        return {k: v for k, v in cur_variants.items() if k not in variants}

    def get_properties_by_result(self, file_path, override_variants=None):
        kwargs = copy.copy(self.properties.value)
        kwargs['workspace'] = self._rsv_project._project__guess_workspace_extra_(**kwargs)
        if override_variants is not None:
            kwargs.update(override_variants)
        #
        rsv_matcher = self.rsv_project._create_rsv_matcher_(
            self._pattern,
            kwargs
        )
        file_properties = rsv_matcher.get_properties_by_result(
            result=file_path
        )
        return file_properties

    def get_properties(self, file_path, override_variants=None):
        # old method , do not delete or rename
        return self.get_properties_by_result(file_path, override_variants)

    def get_latest_version(self, extend_variants=None):
        kwargs = copy.copy(self.properties.value)
        kwargs['version'] = '*'
        kwargs['workspace'] = self._rsv_project._project__guess_workspace_extra_(**kwargs)
        #
        if extend_variants is not None:
            kwargs.update(extend_variants)
        #
        rsv_matcher = self.rsv_project._create_rsv_matcher_(
            self._pattern,
            kwargs
        )
        matches = rsv_matcher.get_matches(trim=(-1, None))
        if matches:
            result, variants = matches[-1]
            version = variants['version']
            return version

    def get_new_version(self, extend_variants=None):
        version = self.get_latest_version(extend_variants)
        if version is not None:
            rsv_version_key = self._rsv_matcher._set_rsv_version_key_create_(version)
            rsv_version_key += 1
            return str(rsv_version_key)
        return 'v001'

    def get_all_exists_matches(self, extend_variants=None):
        kwargs = copy.copy(self.properties.value)
        kwargs['version'] = '*'
        kwargs['workspace'] = self._rsv_project._project__guess_workspace_extra_(**kwargs)
        #
        if extend_variants is not None:
            kwargs.update(extend_variants)
        #
        rsv_matcher = self.rsv_project._create_rsv_matcher_(
            self._pattern,
            kwargs
        )
        return rsv_matcher.get_matches()

    def get_all_exists_results(self, extend_variants=None):
        matches = self.get_all_exists_matches(extend_variants)
        list_ = []
        if matches:
            for i in matches:
                i_result, i_variants = i
                list_.append(i_result)
        return list_

    def get_all_exists_versions(self, extend_variants=None):
        matches = self.get_all_exists_matches(extend_variants)
        list_ = []
        if matches:
            for i in matches:
                i_result, i_variants = i
                list_.append(i_variants['version'])
        return list_

    def get_rsv_version(self, **kwargs):
        rsv_version = self.rsv_project._project__get_rsv_unit_version_(
            rsv_obj=self,
            **kwargs
        )
        return rsv_version

    def get_rsv_versions(self, trim=None):
        list_ = []
        results = self.get_result(version='all', trim=trim)
        for i_result in results:
            i_properties = self.get_properties_by_result(i_result)
            i_properties.set('keyword', self.get('keyword'))
            i_rsv_version = self.get_rsv_version(**i_properties.value)
            list_.append(i_rsv_version)
        return list_

    def get_rsv_task(self):
        return self.get_parent().get_parent()

    def get_rsv_step(self):
        return self.get_parent().get_parent().get_parent()

    def get_rsv_resource(self):
        return self.get_parent().get_parent().get_parent().get_parent()


class AbsRsvUnitVersion(
    AbsRsvObj
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvUnitVersion, self).__init__(*args, **kwargs)
        self.set_gui_menu_raw(
            [
                ('{}-directory'.format(self.type_name), ),
                ('Open Directory', 'file/folder', (True, self._open_source_directory_open_, False)),
            ]
        )

        self._result = None

    def get_rsv_unit(self):
        return self.get_parent()

    def _set_directory_open_(self):
        if self._result:
            bsc_core.StgPathOpt(self._result).set_open_in_system()


class AbsRsvTaskVersion(
    AbsRsvObj
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvTaskVersion, self).__init__(*args, **kwargs)

    def get_rsv_task(self):
        return self.get_parent()
    # unit
    def get_rsv_unit(self, **kwargs):
        return self.rsv_project._project__get_rsv_unit_(
            rsv_obj=self,
            **kwargs
        )

    def get_directory_path(self):
        return self.properties.get('result')


# <rsv-task>
class AbsRsvTask(
    AbsRsvObj
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvTask, self).__init__(*args, **kwargs)
        # self.set_gui_menu_raw_extend(
        #     [
        #         (),
        #         [
        #             'Open Work-scene-src-directory', 'file/folder',
        #             self.get_work_scene_src_directory_open_menu_raw()
        #         ]
        #     ]
        # )
    @property
    def icon(self):
        return bsc_core.RscIconFileMtd.get('file/file')

    def get_work_scene_src_directory_open_menu_raw(self):
        def add_fnc_(application_):
            def get_directory_is_exists_fnc_():
                return bsc_core.StgDirectoryOpt(_directory_path).get_is_exists()

            def set_directory_open_fnc_():
                bsc_core.StgDirectoryOpt(_directory_path).set_open_in_system()
            #
            _branch = self.properties.get('branch')
            _keyword = '{}-work-{}-scene-src-dir'.format(_branch, application_)
            _rsv_unit = self.get_rsv_unit(keyword=_keyword)
            _directory_path = _rsv_unit.get_result()
            list_.append(
                (application_, 'application/{}'.format(application_), (get_directory_is_exists_fnc_, set_directory_open_fnc_, False))
            )

        list_ = []
        for application in self.Applications.DCCS:
            add_fnc_(application)
        return list_

    def get_directory_path(self):
        return self.properties.get('result')
    # todo: remove old fnc, use "get_rsv_scene_properties_by_any_scene_file_path"
    def get_properties_by_work_scene_src_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            key_format='{branch}-source-{application}-scene-src-file',
            override_variants=dict(workspace=self._rsv_project.get_workspace_source()),
            file_path_keys=['any_scene_file', 'work_scene_src_file', 'work_source_file']
        )

    def get_properties_by_scene_src_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            key_format='{branch}-{application}-scene-src-file',
            override_variants=dict(workspace=self._rsv_project.get_workspace_release()),
            file_path_keys=['any_scene_file', 'scene_src_file', 'source_file']
        )
    #
    def get_properties_by_scene_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            key_format='{branch}-{application}-scene-file',
            override_variants=dict(workspace=self._rsv_project.get_workspace_release()),
            file_path_keys=['any_scene_file', 'scene_file']
        )

    def get_properties_by_output_scene_src_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            key_format='{branch}-temporary-{application}-scene-src-file',
            override_variants=dict(workspace=self._rsv_project.get_workspace_temporary()),
            file_path_keys=['any_scene_file', 'output_scene_src_file']
        )

    def get_properties_by_output_scene_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            key_format='{branch}-temporary-{application}-scene-file',
            override_variants=dict(workspace=self._rsv_project.get_workspace_temporary()),
            file_path_keys=['any_scene_file', 'output_scene_file']
        )
    #
    def _get_properties_by_scene_file_path_(self, file_path, key_format, override_variants, file_path_keys):
        if file_path is not None:
            branch = self.properties.get('branch')
            for i_application in self.Applications.DCCS:
                keyword = key_format.format(
                    **dict(branch=branch, application=i_application)
                )
                rsv_task_unit = self.get_rsv_unit(
                    keyword=keyword,
                    application=i_application
                )
                task_unit_properties = rsv_task_unit.get_properties_by_result(file_path, override_variants)
                if task_unit_properties:
                    task_unit_properties.set('application', i_application)
                    task_unit_properties.set('user', bsc_core.SystemMtd.get_user_name())
                    task_unit_properties.set('time', bsc_core.TimeMtd.get_time())
                    task_unit_properties.set('time_tag', bsc_core.TimeMtd.get_time_tag())
                    for i_file_path_key in file_path_keys:
                        task_unit_properties.set(i_file_path_key, file_path)
                    #
                    task_unit_properties.set('option.scheme', self._rsv_project.get_workspace_release())
                    task_unit_properties.set('option.version', task_unit_properties.get('version'))
                    #
                    task_unit_properties.set('dcc.root', '/master')
                    task_unit_properties.set('dcc.root_name', 'master')
                    task_unit_properties.set('dcc.sub_root', '/master/hi')
                    #
                    task_unit_properties.set('dcc.pathsep', self.Applications.get_pathsep(i_application))
                    return task_unit_properties
    #
    def get_rsv_scene_properties_by_any_scene_file_path(self, file_path):
        if file_path is not None:
            branch = self.properties.get('branch')
            for i_application in self.Applications.DCCS:
                for j_keyword_format, scene_type in [
                    # source
                    ('{branch}-source-{application}-scene-src-file', 'source-scene-src'),
                    ('{branch}-user-{application}-scene-src-file', 'user-scene-src'),
                    # release
                    ('{branch}-{application}-scene-src-file', 'release-scene-src'),
                    ('{branch}-{application}-scene-file', 'release-scene'),
                    # temporary
                    ('{branch}-temporary-{application}-scene-src-file', 'temporary-scene-src'),
                    ('{branch}-temporary-{application}-scene-file', 'temporary-scene'),
                ]:
                    j_keyword = j_keyword_format.format(
                        **dict(branch=branch, application=i_application)
                    )
                    if self._rsv_project.get_has_pattern(j_keyword):
                        j_rsv_unit = self.get_rsv_unit(
                            keyword=j_keyword,
                            application=i_application
                        )
                        j_rsv_scene_properties = j_rsv_unit.get_properties_by_result(file_path)
                        if j_rsv_scene_properties:
                            j_rsv_scene_properties.set('keyword', j_keyword)
                            j_rsv_scene_properties.set('scene_type', scene_type)
                            #
                            j_rsv_scene_properties.set('branch', branch)
                            j_rsv_scene_properties.set('resource', j_rsv_scene_properties.get(branch))
                            j_rsv_scene_properties.set('application', i_application)
                            #
                            j_rsv_scene_properties.set('extra.file', file_path)
                            j_rsv_scene_properties.set('extra.user', bsc_core.SystemMtd.get_user_name())
                            j_rsv_scene_properties.set('extra.time_tag', bsc_core.TimeMtd.get_time_tag())
                            #
                            j_rsv_scene_properties.set(
                                'dcc', self._rsv_project.get_dcc_data(i_application)
                            )
                            return j_rsv_scene_properties
    # tag
    def get_rsv_tag(self):
        return self.get_parent().get_parent().get_parent()
    # entity
    def get_rsv_resource(self):
        return self.get_parent().get_parent()
    # step
    def get_rsv_step(self):
        return self.get_parent()
    # version
    def get_rsv_version(self, **kwargs):
        return self.rsv_project._project__get_rsv_task_version_(
            rsv_obj=self,
            **kwargs
        )

    def get_rsv_versions(self, **kwargs):
        kwargs_over = self.properties.get_copy_value()
        kwargs_over.update(kwargs)
        return self._rsv_project._project__get_rsv_task_versions_(
            **kwargs_over
        )
    # unit
    def get_rsv_unit(self, **kwargs):
        return self.rsv_project._project__get_rsv_unit_(
            rsv_obj=self,
            **kwargs
        )

    def get_rsv_scene_properties(self):
        properties = self.PROPERTIES_CLASS(
            self, self.properties.get_copy_value()
        )
        properties.set(
            'user', bsc_core.SystemMtd.get_user_name()
        )
        return properties

    def create_directory(self, workspace_key):
        variants = self.properties.get_copy_value()
        variants['workspace_key'] = workspace_key
        keyword = '{branch}-{workspace_key}-task-dir'.format(
            **variants
        )
        rsv_unit = self.get_rsv_unit(keyword=keyword)
        directory_path = rsv_unit.get_result()

        bsc_core.StgPathPermissionMtd.create_directory(
            directory_path
        )


# <rsv-step>
class AbsRsvStep(
    AbsRsvObj
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvStep, self).__init__(*args, **kwargs)

    def get_rsv_unit(self, **kwargs):
        return self.rsv_project._project__get_rsv_unit_(
            rsv_obj=self,
            **kwargs
        )

    def get_directory_path(self):
        return self.properties.get('result')

    def get_source_directory_path(self):
        keyword = self._rsv_project._get_step_keyword_(
            self.properties.get('branch'),
            self.WorkspaceKeys.Source
        )
        return self.get_rsv_unit(
            workspace=self._rsv_project.get_workspace_source(),
            keyword=keyword
        ).get_result()

    def get_rsv_tasks(self, **kwargs):
        self._completion_kwargs_from_parent_(self, kwargs)
        return self._rsv_project._project__get_rsv_tasks_(
            **kwargs
        )

    def get_rsv_task(self, **kwargs):
        rsv_obj = self.rsv_project._project__get_rsv_task_(
            rsv_obj=self,
            **kwargs
        )
        return rsv_obj


class AbsRsvResource(
    AbsRsvObj
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvResource, self).__init__(*args, **kwargs)
    @property
    def icon(self):
        return bsc_core.RscIconFileMtd.get('resolver/asset')

    def get_rsv_steps(self, **kwargs):
        self._completion_kwargs_from_parent_(self, kwargs)
        return self._rsv_project._project__get_rsv_steps_(
            **kwargs
        )

    def get_rsv_step(self, **kwargs):
        """
        :param kwargs: step: str(<step-name>)
        :return: instance(<rsv-step>)
        """
        rsv_obj = self.rsv_project._project__get_rsv_step_(
            rsv_obj=self,
            **kwargs
        )
        return rsv_obj

    def get_rsv_task(self, **kwargs):
        rsv_step = self.get_rsv_step(**kwargs)
        if rsv_step is not None:
            return rsv_step.get_rsv_task(**kwargs)

    def get_rsv_tasks(self, **kwargs):
        self._completion_kwargs_from_parent_(self, kwargs)
        return self._rsv_project._project__get_rsv_tasks_(
            **kwargs
        )

    def get_rsv_unit(self, **kwargs):
        """
        :param kwargs:
            task: str
            keyword: str
        :return:
        """
        return self.rsv_project._project__get_rsv_unit_(
            rsv_obj=self,
            **kwargs
        )

    def get_available_rsv_unit(self, **kwargs):
        """
        :param kwargs:
            task: str / [str, ...]
            keyword: str
        :return:
        """
        rsv_tasks = self.get_rsv_tasks(**kwargs)
        keyword = kwargs['keyword']
        for i_rsv_task in rsv_tasks:
            i_rsv_unit = i_rsv_task.get_rsv_unit(keyword=keyword)
            if i_rsv_unit.get_result(version='latest'):
                return i_rsv_unit


class AbsRsvTag(
    AbsRsvObj
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvTag, self).__init__(*args, **kwargs)

    def get_rsv_resources(self, **kwargs):
        self._rsv_project._project__completion_kwargs_from_parent_(
            self.VariantCategories.Resource, self, kwargs
        )
        return self._rsv_project._project__get_rsv_resources_(
            **kwargs
        )

    def get_rsv_resource(self, **kwargs):
        """
        :param kwargs: asset: str(<asset-name>) / shot: str(<shot-name>)
        :return: instance(<rsv-entity>)
        """
        rsv_obj = self._rsv_project._project__get_rsv_resource_(
            rsv_obj=self,
            **kwargs
        )
        return rsv_obj

    def get_rsv_steps(self, **kwargs):
        self._completion_kwargs_from_parent_(self, kwargs)
        return self._rsv_project._project__get_rsv_steps_(
            **kwargs
        )

    def get_rsv_tasks(self, **kwargs):
        self._completion_kwargs_from_parent_(self, kwargs)
        return self._rsv_project._project__get_rsv_tasks_(
            **kwargs
        )


class AbsRsvExtraDef(AbsRsvDef):
    RSV_MATCH_PATTERN_CLASS = None
    @classmethod
    def _guess_branch_0_(cls, **kwargs):
        if 'branch' in kwargs:
            return kwargs['branch']
        elif 'sequence' in kwargs:
            if 'shot' in kwargs:
                return cls.Branches.Shot
            return cls.Branches.Sequence
        elif 'shot' in kwargs:
            return cls.Branches.Shot
        elif 'role' in kwargs:
            return cls.Branches.Asset
        elif 'asset' in kwargs:
            return cls.Branches.Asset
    @classmethod
    def _guess_branch_(cls, **kwargs):
        if 'branch' in kwargs:
            return kwargs['branch']
        elif 'sequence' in kwargs:
            if 'shot' in kwargs:
                return cls.Branches.Shot
            return cls.Branches.Sequence
        elif 'shot' in kwargs:
            return cls.Branches.Shot
        elif 'role' in kwargs:
            return cls.Branches.Asset
        elif 'asset' in kwargs:
            return cls.Branches.Asset
        raise RuntimeError(
            'argument key "branch" must definition in kwargs'
        )
    @classmethod
    def _get_step_keyword_(cls, branch, workspace_key):
        return '{}-{}-step-dir'.format(branch, workspace_key)
    @classmethod
    def _get_task_keyword_(cls, branch, workspace_key):
        return '{}-{}-task-dir'.format(branch, workspace_key)
    @classmethod
    def _read_raw_(cls, file_path):
        if os.path.exists(file_path):
            ext = os.path.splitext(file_path)[-1]
            if ext in ['.json']:
                with open(file_path) as j:
                    return json.load(j, object_pairs_hook=collections.OrderedDict)
            elif ext in ['.yml']:
                with open(file_path) as y:
                    return bsc_core.OrderedYamlMtd.set_load(y)
            else:
                raise TypeError(
                    'ext: "{}" is not available'.format(ext)
                )
        else:
            raise TypeError(
                'file="{}" is not found'.format(file_path)
            )
    @classmethod
    def _get_raw_opt_(cls, raw):
        return RawOpt(raw)
    @staticmethod
    def _completion_keyword_by_variants_(variants):
        """
        etc: keyword = '{branch}-component-usd-file'
        :param variants:
        :return:
        """
        keyword = variants.pop('keyword')
        # noinspection PyStatementEffect
        keyword = keyword.format(**variants)
        variants['keyword'] = keyword
        return keyword

    def init_rsv_extra(self, raw):
        self._raw = raw
        self._raw_opt = RawOpt(self._raw)
    #
    def _set_rsv_def_init_(self):
        self._raw = collections.OrderedDict()
        #
        self._patterns_dict = collections.OrderedDict()

    def _update_all_patterns_(self):
        file_keys = self._raw_opt.get_keys(pattern='*-file')
        directory_keys = self._raw_opt.get_keys(pattern='*-dir')
        for i_key in file_keys+directory_keys:
            self._patterns_dict[i_key] = self._raw_opt.unfold_value(self._raw_opt.get(i_key))

    def _get_rsv_obj_create_kwargs_(self, obj_path, kwargs_src, extend_keys=None):
        keyword = kwargs_src['keyword']
        kwargs_tgt = collections.OrderedDict()
        pattern = self.get_pattern(keyword)
        keys = MtdBasic._get_keys_by_parse_pattern_(pattern)
        #
        if isinstance(extend_keys, (tuple, list)):
            keys.extend(list(extend_keys))
        #
        for i_key in keys:
            if i_key in kwargs_src:
                kwargs_tgt[i_key] = kwargs_src[i_key]
        #
        kwargs_tgt['path'] = obj_path
        kwargs_tgt['keyword'] = keyword
        kwargs_tgt['pattern'] = pattern
        return kwargs_tgt

    def _get_main_rsv_obj_path__(self, variants):
        search_keys = self._raw_opt.get('path-main-keys')
        #
        p_values = ['', ]
        for i_key in search_keys:
            if i_key in variants:
                p_values.append(variants[i_key])
        return self.PATHSEP.join(p_values)

    def _get_path_keys_(self, rsv_category):
        return self._raw_opt.get('path-{}-keys'.format(rsv_category))

    def _get_main_rsv_path_(self, rsv_category, variants):
        search_keys = self._raw_opt.get('path-{}-keys'.format(rsv_category))
        #
        p_values = ['', ]
        for i_key in search_keys:
            if i_key in variants:
                p_values.append(variants[i_key])
        #
        return self.PATHSEP.join(p_values)

    def _get_version_rsv_path_(self, main_path, variants):
        search_keys_extend = self._raw_opt.get('path-version-keys_extend')
        #
        p_values = ['', ]
        for i_key in search_keys_extend:
            if i_key in variants:
                p_values.append(variants[i_key])
            else:
                raise KeyError('key: "{}" is non-exists'.format(i_key))
        #
        return main_path + self.PATHSEP.join(p_values)

    def _get_unit_rsv_path_(self, main_path, variants):
        search_keys_extend = self._raw_opt.get('path-unit-keys_extend')
        #
        p_values = ['', ]
        for i_key in search_keys_extend:
            if i_key in variants:
                p_values.append(variants[i_key])
            else:
                raise KeyError('key: "{}" is non-exists'.format(i_key))
        #
        return main_path + self.PATHSEP.join(p_values)

    def _copy_variants_as_branches_(self, variants):
        kwargs_copy = {}
        search_keys = self._raw_opt.get('path-main-keys')
        for i_key in search_keys:
            if i_key in variants:
                kwargs_copy[i_key] = variants[i_key]
        #
        keys_extend = ['branch', 'workspace']
        for i_key in keys_extend:
            if i_key in variants:
                kwargs_copy[i_key] = variants[i_key]
        return kwargs_copy

    def _completion_branch_rsv_create_kwargs_(self, rsv_category, rsv_type, kwargs, result, kwargs_extend):
        rsv_path = self._get_main_rsv_path_(rsv_category, kwargs)
        kwargs['category'] = rsv_category
        kwargs['type'] = rsv_type
        kwargs['path'] = rsv_path
        user = bsc_core.StgPathOpt(result).get_user()
        #
        kwargs['result'] = result
        if bsc_core.StgFileOpt(result).get_is_exists() is True:
            update = bsc_core.TimePrettifyMtd.to_prettify_by_timestamp(
                bsc_core.StgFileOpt(
                    result
                ).get_modify_timestamp(),
                language=1
            )
        else:
            update = 'non-exists'
        #
        kwargs['update'] = update
        kwargs['user'] = user
        #
        kwargs.update(kwargs_extend)
    @staticmethod
    def _completion_rsv_obj_create_kwargs_(kwargs, result, variants):
        update = bsc_core.TimePrettifyMtd.to_prettify_by_timestamp(
            bsc_core.StgFileOpt(
                result
            ).get_modify_timestamp(),
            language=1
        )
        user = bsc_core.StgPathOpt(
            result
        ).get_user()
        #
        kwargs['result'] = result
        kwargs['update'] = update
        kwargs['user'] = user
        kwargs.update(variants)

    def _set_obj_parameters_completes_(self, kwargs, parent_parameters, extend_keys=None):
        keyword = kwargs['keyword']
        pattern = self.get_pattern(keyword)
        keys = MtdBasic._get_keys_by_parse_pattern_(pattern)
        if isinstance(extend_keys, (str, list)):
            keys += list(extend_keys)
        for key in keys:
            if key in kwargs:
                if key in parent_parameters:
                    if kwargs[key] == '*':
                        kwargs[key] = parent_parameters[key]
            else:
                if key in parent_parameters:
                    kwargs[key] = parent_parameters[key]

    def get_keywords(self, regex=None):
        _ = self._patterns_dict.keys()
        if regex is not None:
            return fnmatch.filter(_, regex)
        return _

    def get_has_pattern(self, keyword):
        return keyword in self._patterns_dict

    def get_pattern(self, keyword):
        if keyword not in self._patterns_dict:
            raise KeyError(u'keyword: "{}" is Non-registered'.format(keyword))
        return self._patterns_dict[keyword]
    # todo: remove this method
    def get_value(self, key):
        return self._raw_opt.get(key)

    def get_rsv_pattern(self, keyword):
        return self.RSV_MATCH_PATTERN_CLASS(self.get_pattern(keyword))

    def get_variant(self, keyword):
        if keyword not in self._raw:
            raise KeyError(u'keyword: "{}" is Non-registered'.format(keyword))
        return self._raw[keyword]


# <rsv-project>
class AbsRsvProject(
    AbsRsvObjDef,
    AbsRsvExtraDef,
    unr_abstracts.AbsObjGuiDef,
    unr_abstracts.AbsObjDagDef,
):
    RSV_MATCHER_CLASS = None
    #
    RSV_OBJ_STACK_CLASS = None
    #
    RSV_TAG_CLASS = None
    RSV_RESOURCE_CLASS = None
    RSV_STEP_CLASS = None
    RSV_TASK_CLASS = None
    RSV_TASK_VERSION_CLASS = None
    #
    RSV_UNIT_CLASS = None
    RSV_UNIT_VERSION_CLASS = None
    #
    RSV_APP_DEFAULT_CLASS = None
    RSV_APP_NEW_CLASS = None
    #
    PROPERTIES_CLASS = None
    def __init__(self, *args, **kwargs):
        self._set_obj_def_init_()
        self._set_rsv_def_init_()
        #
        project_root, project_raw = args[:2]
        #
        self._rsv_root = project_root
        self._project_raw = project_raw
        #
        self._rsv_obj_stack = self.RSV_OBJ_STACK_CLASS()
        #
        self._set_rsv_obj_def_init_(
            self.PROPERTIES_CLASS(self, bsc_core.DictMtd.sort_key_to(kwargs))
        )
        self._set_obj_dag_def_init_(self._rsv_path)
        self._set_obj_gui_def_init_()
        #
        self._root_dict = collections.OrderedDict()
        self._root_step_choice = None
        self._root_configure = bsc_objects.Configure(value=collections.OrderedDict())
        #
        self._static_variant_configure = bsc_objects.Configure(value=collections.OrderedDict())
        #
        self._rsv_matcher = self._create_rsv_matcher_(
            self._pattern,
            self._rsv_properties.value
        )
        #
        raw = copy.copy(self._rsv_root._raw)
        raw.update(project_raw)
        self.init_rsv_extra(raw)
        #
        self._configure = bsc_objects.Configure(value=self._raw)
        self._root_choices = self._configure.get('root-choices')
        self._root_step_choice = self._configure.get_content(
            'root-step-choice'
        )
        #
        self._project_update_all_static_variants_()
        self._project_update_all_roots_()
        #
        self._update_all_patterns_()
        #
        self._workspace_key_mapper = {}

    def _project__completion_kwargs_from_parent_(self, rsv_category, rsv_parent, kwargs):
        path_keys = self._get_path_keys_(rsv_category)
        # do not override this keys
        for k, v in rsv_parent.properties.get_value().items():
            if k in path_keys:
                kwargs[k] = v

    def _project_update_all_roots_(self):
        self._root_dict[self.Platforms.Windows] = self._raw_opt.get_as_unfold('project-root-windows-dir')
        self._root_dict[self.Platforms.Linux] = self._raw_opt.get_as_unfold('project-root-linux-dir')

        for i_index, i_root_choice in enumerate(self._root_choices):
            for j_platform in self.Platforms.All:
                if i_index == 0:
                    self._root_configure.set(
                        'root.{}'.format(i_root_choice, j_platform),
                        self._raw['project-{}-{}-dir'.format(i_root_choice, j_platform)]
                    )
                #
                self._root_configure.set(
                    '{}.{}'.format(i_root_choice, j_platform),
                    self._raw['project-{}-{}-dir'.format(i_root_choice, j_platform)]
                )

    def _project_update_all_static_variants_(self):
        for i_variant_type_key in self.VariantsKeys.All:
            i_variant_type_key_extra = '{}_extra'.format(i_variant_type_key)
            i_extras = self._raw_opt.get(i_variant_type_key_extra)
            i_variants = self._raw_opt.get(i_variant_type_key)
            if isinstance(i_variants, dict):
                for j_variant_name_key, j_value in i_variants.items():
                    j_key = '{}.{}'.format(
                        i_variant_type_key, j_variant_name_key
                    )
                    self._static_variant_configure.set(
                        j_key,
                        j_value
                    )
                    if i_extras:
                        for k_seq, k_extra in enumerate(i_extras):
                            k_key = '{}.{}'.format(
                                i_variant_type_key_extra,
                                k_extra.format(**dict(key=j_variant_name_key))
                            )
                            k_value = k_extra.format(**dict(key=j_value))
                            self._static_variant_configure.set(
                                k_key,
                                k_value
                            )

    def _project_update_roots_to_properties_(self, platform_):
        for i_index, i_root_choice in enumerate(self._root_choices):
            if i_index == 0:
                self._rsv_properties.set(
                    'root',
                    self._root_configure.get('root.{}'.format(i_root_choice, platform_))
                )
            #
            self._rsv_properties.set(
                i_root_choice,
                self._root_configure.get('{}.{}'.format(i_root_choice, platform_))
            )

    def _project_update_static_variants_to_properties_(self):
        self._rsv_properties.set_update(
            self._static_variant_configure.get_value()
        )
    @classmethod
    def _project_get_branch_extra_(cls, **kwargs):
        if 'branch' in kwargs:
            return kwargs['branch']
        elif 'sequence' in kwargs:
            if 'shot' in kwargs:
                return cls.Branches.Shot
            return cls.Branches.Sequence
        elif 'shot' in kwargs:
            return cls.Branches.Shot
        elif 'role' in kwargs:
            return cls.Branches.Asset
        elif 'asset' in kwargs:
            return cls.Branches.Asset
        #
        elif 'keyword' in kwargs:
            keyword = kwargs['keyword']
            if fnmatch.filter([keyword], 'asset-*'):
                return cls.Branches.Asset
            elif fnmatch.filter([keyword], 'shot-*'):
                return cls.Branches.Shot
            raise RuntimeError()
        raise RuntimeError()

    def _project_get_workspace_key_mapper_(self):
        if not self._workspace_key_mapper:
            self._workspace_key_mapper = {v: k for k, v in self.properties.get(self.VariantsKeys.Workspaces).items()}
        return self._workspace_key_mapper

    def _project__get_workspace_key_by_variants_(self, variants):
        if 'workspace_key' in variants:
            return variants['workspace_key']
        elif 'workspace' in variants:
            workspace = variants['workspace']
            workspace_key_mapper = self._project_get_workspace_key_mapper_()
            if workspace in workspace_key_mapper:
                return workspace_key_mapper[workspace]
        return self.WorkspaceKeys.Source

    def _project_get_workspace_(self, **kwargs):
        if 'workspace_key' in kwargs:
            return self.get_workspace(kwargs['workspace_key'])
        elif 'workspace' in kwargs:
            return kwargs['workspace']
        return self.get_workspace_source()

    def _project_update_workspace_variants_(self, variants):
        workspace_key = self._project__get_workspace_key_by_variants_(variants)
        variants['workspace_key'] = workspace_key
        workspace = self._project_get_workspace_(**variants)
        variants['workspace'] = workspace
        return workspace_key, workspace

    def _project__guess_workspace_extra_(self, **kwargs):
        keyword = kwargs['keyword']
        ks = keyword.split('-')
        key = ks[1]
        if key in self.WorkspaceMatchKeys.Sources:
            return self.get_workspace_source()
        elif key in self.WorkspaceMatchKeys.Users:
            return self.get_workspace_user()
        elif key in self.WorkspaceMatchKeys.Releases:
            return self.get_workspace_release()
        elif key in self.WorkspaceMatchKeys.Temporaries:
            return self.get_workspace_temporary()
        return self.get_workspace_release()

    def _project_get_search_patterns_(self, branch, rsv_type):
        key = '{}-{}-search-patterns'.format(branch, rsv_type)
        return collections.OrderedDict(
            [(k, self._raw_opt.unfold_value(v)) for k, v in (self._raw_opt.get(key) or {}).items()]
        )
    @property
    def resolver(self):
        return self._rsv_root
    @property
    def pathsep(self):
        return '/'
    @property
    def path(self):
        return self._rsv_path
    @property
    def icon(self):
        return bsc_core.RscIconFileMtd.get('resolver/project')

    def get_workspaces(self):
        return self._rsv_properties.get(
            self.VariantsKeys.Workspaces
        ).values()

    def get_workspace(self, workspace_key):
        return self._rsv_properties.get(
            '{}.{}'.format(self.VariantsKeys.Workspaces, workspace_key)
        )
    # etc. "work"
    def get_workspace_source(self):
        return self._rsv_properties.get(
            '{}.{}'.format(self.VariantsKeys.Workspaces, self.WorkspaceKeys.Source)
        )
    #
    def get_workspace_user(self):
        return self._rsv_properties.get(
            '{}.{}'.format(self.VariantsKeys.Workspaces, self.WorkspaceKeys.User)
        )
    # etc. "publish"
    def get_workspace_release(self):
        return self._rsv_properties.get(
            '{}.{}'.format(self.VariantsKeys.Workspaces, self.WorkspaceKeys.Release)
        )
    # etc. "output"
    def get_workspace_temporary(self):
        return self._rsv_properties.get(
            '{}.{}'.format(self.VariantsKeys.Workspaces, self.WorkspaceKeys.Temporary)
        )

    def get_roles(self):
        return self._rsv_properties.get(
            self.VariantsKeys.Roles
        ).values()

    def get_tags(self, branch):
        if branch == self.Branches.Asset:
            return self.get_roles()
        elif branch == self.Branches.Sequence:
            return []
        elif branch == self.Branches.Shot:
            return []
        else:
            raise RuntimeError()

    def get_asset_steps(self, with_extra=False):
        if with_extra is True:
            return self._rsv_properties.get(
                self.VariantsKeys.AssetSteps
            ).values() + (self._rsv_properties.get(
                '{}_extra'.format(
                    self.VariantsKeys.AssetSteps
                )
            ) or {}).values()
        return self._rsv_properties.get(
            self.VariantsKeys.AssetSteps
        ).values()

    def get_sequence_steps(self, with_extra=False):
        if with_extra is True:
            return self._rsv_properties.get(
                self.VariantsKeys.SequenceSteps
            ).values() + (self._rsv_properties.get(
                '{}_extra'.format(
                    self.VariantsKeys.SequenceSteps
                )
            ) or {}).values()
        return self._rsv_properties.get(
            self.VariantsKeys.SequenceSteps
        ).values()

    def get_shot_steps(self, with_extra=False):
        if with_extra is True:
            return self._rsv_properties.get(
                self.VariantsKeys.ShotSteps
            ).values() + (self._rsv_properties.get(
                '{}_extra'.format(
                    self.VariantsKeys.ShotSteps
                )
            ) or {}).values()
        return self._rsv_properties.get(
            self.VariantsKeys.ShotSteps
        ).values()

    def get_steps(self, branch, with_extra=False):
        if branch == self.Branches.Asset:
            return self.get_asset_steps(with_extra=with_extra)
        elif branch == self.Branches.Sequence:
            return self.get_sequence_steps(with_extra=with_extra)
        elif branch == self.Branches.Shot:
            return self.get_shot_steps(with_extra=with_extra)
        else:
            raise RuntimeError()

    def _get_root_choice_(self, variants):
        root_choice = self._root_step_choice
        if root_choice:
            if 'workspace' in variants and 'step' in variants:
                workspace_key = self._project__get_workspace_key_by_variants_(variants)
                root_choice = self._root_step_choice.get(
                    '{}.{}'.format(workspace_key, variants['step'])
                )
                if root_choice is not None:
                    return root_choice
        return 'root_primary'

    def _set_dag_create_(self, path):
        if path == self._rsv_path:
            return self
        return self._project__get_rsv_obj_(path)

    def _get_child_paths_(self, *args, **kwargs):
        return self._project__get_rsv_obj_child_paths_(self._rsv_path)

    def _set_child_create_(self, path):
        return self._project__get_rsv_obj_(path)

    def get_descendants(self):
        return self._rsv_obj_stack.get_objects()

    def get_parent(self):
        return self._rsv_root

    def get_directory_path(self):
        keyword = 'project-dir'
        rsv_pattern = self.RSV_MATCH_PATTERN_CLASS(
            self.get_pattern(keyword)
        )
        return rsv_pattern.set_update(**self.properties.value)

    def get_patterns(self, regex=None):
        if regex is not None:
            return [self.get_pattern(i) for i in self.get_keywords(regex)]
        return self._patterns_dict.values()

    def get_url(self, keyword, **kwargs):
        pass
    #
    def get_platform(self):
        return
    #
    def get_root(self):
        return

    def _completion_rsv_match_kwargs_(self, kwargs):
        # workspace
        if 'workspace' in kwargs:
            workspace = kwargs['workspace']
            # convert other workspace to "work"
            if workspace not in [
                self.get_workspace_source(),
                self.get_workspace_release(),
                # self.get_workspace_temporary()
            ]:
                kwargs['workspace'] = self.get_workspace_source()
        else:
            kwargs['workspace'] = self.get_workspace_source()
        # root_choice
        root_choice = self._get_root_choice_(kwargs)
        kwargs['root_choice'] = root_choice
        # root
        root_cur = self._rsv_properties.get(root_choice)
        kwargs['root'] = root_cur
    #
    def _project__create_rsv_matcher_(self, kwargs):
        self._completion_rsv_match_kwargs_(kwargs)
        #
        pattern = kwargs['pattern']
        return self.RSV_MATCHER_CLASS(
            self,
            pattern,
            kwargs
        )

    def _completion_rsv_match_main_kwargs_(self, kwargs):
        # root_choice
        root_choice = self._get_root_choice_(kwargs)
        kwargs['root_choice'] = root_choice
        # root
        root_cur = self._rsv_properties.get(root_choice)
        kwargs['root'] = root_cur

    def _project__create_main_rsv_matcher_(self, kwargs):
        self._completion_rsv_match_main_kwargs_(kwargs)
        #
        pattern = kwargs['pattern']
        return self.RSV_MATCHER_CLASS(
            self,
            pattern,
            kwargs
        )

    def _create_rsv_matcher_(self, pattern, variants_override):
        return self.RSV_MATCHER_CLASS(
            self,
            pattern,
            variants_override
        )
    # tag
    def _project__get_rsv_tags_(self, **kwargs):
        list_ = []
        #
        branch = kwargs['branch']
        if branch == self.Branches.Asset:
            rsv_type = self.VariantTypes.Role
        elif branch == self.Branches.Shot:
            rsv_type = self.VariantTypes.Sequence
        else:
            raise TypeError()
        #
        keyword = '{}-dir'.format(rsv_type)
        kwargs['keyword'] = keyword
        kwargs['pattern'] = self.get_pattern(keyword=keyword)
        rsv_matcher = self._project__create_main_rsv_matcher_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        for i_m in matches:
            _, i_variants = i_m
            i_kwargs = copy.copy(kwargs)
            i_kwargs.update(i_variants)
            i_rsv_tag = self.get_rsv_tag(**i_kwargs)
            if i_rsv_tag is not None:
                if i_rsv_tag not in list_:
                    list_.append(i_rsv_tag)
        return list_

    def _project__get_rsv_tag_(self, rsv_obj, **kwargs):
        kwargs_over = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_over[k] = v
        #
        kwargs_over.update(kwargs)
        #
        branch = self._guess_branch_(**kwargs_over)
        if branch == self.Branches.Asset:
            rsv_type = self.VariantTypes.Role
        elif branch == self.Branches.Shot:
            rsv_type = self.VariantTypes.Sequence
        else:
            raise TypeError()
        #
        if rsv_type in kwargs_over:
            name = kwargs_over[rsv_type]
            name_includes = self.get_tags(branch)
            if name_includes:
                if name not in name_includes:
                    return
        else:
            name = '*'
        #
        if MtdBasic._set_name_check_(rsv_type, name) is False:
            return None
        # type
        kwargs_over['type'] = rsv_type
        keyword = '{}-dir'.format(rsv_type)
        kwargs_over['keyword'] = keyword
        # branch
        kwargs_over['branch'] = branch
        # asset/shot
        kwargs_over[rsv_type] = name
        #
        obj_path = self._get_main_rsv_path_(self.VariantCategories.Tag, kwargs_over)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        #
        variants = self._get_rsv_obj_create_kwargs_(
            obj_path,
            kwargs_over,
            extend_keys=['type', 'branch']
        )
        return self._project__set_rsv_tag_create_(**variants)

    def _project__set_rsv_tag_create_(self, **kwargs):
        rsv_matcher = self._project__create_main_rsv_matcher_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            result, variants = matches[-1]
            self._completion_rsv_obj_create_kwargs_(kwargs, result, variants)
            rsv_obj = self.RSV_TAG_CLASS(self, **kwargs)
            self._project__set_rsv_obj_add_(rsv_obj)
            return rsv_obj

    def get_rsv_tags(self, **kwargs):
        branch = self._guess_branch_0_(**kwargs)
        if branch is not None:
            kwargs['branch'] = branch
            return self._project__get_rsv_tags_(**kwargs)
        else:
            list_ = []
            for i_branch in self.Branches.Mains:
                kwargs['branch'] = i_branch
                list_.extend(
                    self._project__get_rsv_tags_(**kwargs)
                )
            return list_

    def get_rsv_tag(self, **kwargs):
        rsv_obj = self._project__get_rsv_tag_(
            rsv_obj=self, **kwargs
        )
        return rsv_obj
    # resource
    def _tag__get_rev_resource_(self, **kwargs):
        rsv_tag = self.get_rsv_tag(**kwargs)
        if rsv_tag:
            return rsv_tag.get_rsv_resource(**kwargs)

    def _project__get_rsv_resources_(self, **kwargs):
        list_ = []
        kwargs_over = copy.copy(kwargs)
        branch = kwargs_over['branch']
        keyword = '{}-dir'.format(branch)
        kwargs_over['keyword'] = keyword
        kwargs_over['pattern'] = self.get_pattern(keyword=keyword)
        rsv_matcher = self._project__create_main_rsv_matcher_(
            kwargs_over
        )
        matches = rsv_matcher.get_matches()
        for i_m in matches:
            _, i_variants = i_m
            i_kwargs_over = copy.copy(kwargs_over)
            i_kwargs_over.update(i_variants)
            i_rsv_resource = self._tag__get_rev_resource_(**i_kwargs_over)
            if i_rsv_resource is not None:
                if i_rsv_resource not in list_:
                    list_.append(i_rsv_resource)
        return list_
    #
    def _project__get_rsv_resource_(self, rsv_obj, **kwargs):
        kwargs_over = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_over[k] = v
        #
        kwargs_over.update(kwargs)
        #
        branch = self._guess_branch_(**kwargs_over)
        rsv_type = branch
        if rsv_type in kwargs_over:
            name = kwargs_over[rsv_type]
        else:
            raise KeyError()
        #
        if MtdBasic._set_name_check_(rsv_type, name) is False:
            return None
        # type
        kwargs_over['type'] = rsv_type
        keyword = '{}-dir'.format(rsv_type)
        kwargs_over['keyword'] = keyword
        # branch
        kwargs_over['branch'] = branch
        # asset/shot
        kwargs_over[branch] = name
        #
        obj_path = self._get_main_rsv_path_(self.VariantCategories.Resource, kwargs_over)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        variants = self._get_rsv_obj_create_kwargs_(
            obj_path,
            kwargs_over,
            extend_keys=['type', 'branch']
        )
        return self._project__set_rsv_resource_create_(**variants)
    #
    def _project__set_rsv_resource_create_(self, **kwargs):
        rsv_matcher = self._project__create_main_rsv_matcher_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            result, variants = matches[-1]
            self._completion_rsv_obj_create_kwargs_(kwargs, result, variants)
            rsv_obj = self.RSV_RESOURCE_CLASS(self, **kwargs)
            self._project__set_rsv_obj_add_(rsv_obj)
            return rsv_obj
    #
    def get_rsv_resources(self, **kwargs):
        branch = self._guess_branch_0_(**kwargs)
        if branch is not None:
            kwargs['branch'] = branch
            list_ = []
            if self.VariantTypes.Role in kwargs or self.VariantTypes.Sequence in kwargs:
                rsv_tag = self.get_rsv_tag(**kwargs)
                list_.extend(
                    rsv_tag.get_rsv_resources(**kwargs)
                )
            else:
                rsv_tags = self.get_rsv_tags(**kwargs)
                for i_rsv_tag in rsv_tags:
                    list_.extend(
                        i_rsv_tag.get_rsv_resources(**kwargs)
                    )
            return list_
        else:
            list_ = []
            for i_branch in self.Branches.Mains:
                kwargs['branch'] = i_branch
                i_rsv_tags = self.get_rsv_tags(branch=i_branch)
                for j_rsv_tag in i_rsv_tags:
                    list_.extend(j_rsv_tag.get_rsv_resources())
            return list_
    #
    def get_rsv_resource(self, **kwargs):
        if self.VariantTypes.Role in kwargs or self.VariantTypes.Sequence in kwargs:
            return self._tag__get_rev_resource_(**kwargs)
        else:
            _ = self.get_rsv_resources(**kwargs)
            if _:
                return _[-1]
    # step
    def _resource__get_rsv_step_(self, **kwargs):
        rsv_resource = self.get_rsv_resource(**kwargs)
        if rsv_resource is not None:
            return rsv_resource.get_rsv_step(**kwargs)

    def _project__get_rsv_steps_(self, **kwargs):
        list_ = []
        #
        rsv_type = self.VariantTypes.Step
        branch = self._guess_branch_(**kwargs)
        search_patterns = self._project_get_search_patterns_(branch, rsv_type)
        for i_workspace_key, i_pattern_args in search_patterns.items():
            i_kwargs_over = copy.copy(kwargs)
            i_kwargs_over['pattern'] = i_pattern_args
            i_kwargs_over['workspace'] = self.get_workspace(i_workspace_key)
            i_rsv_matcher = self._project__create_main_rsv_matcher_(
                i_kwargs_over
            )
            i_matches = i_rsv_matcher.get_matches()
            for j_match in i_matches:
                j_result, j_variants = j_match
                j_kwargs_over = self._copy_variants_as_branches_(i_kwargs_over)
                j_kwargs_over.update(j_variants)
                j_kwargs_over['resolver_workspace_key'] = i_workspace_key
                j_kwargs_over['resolver_pattern'] = i_pattern_args
                j_kwargs_over['resolver_result'] = j_result
                j_rsv_step = self._resource__get_rsv_step_(**j_kwargs_over)
                if j_rsv_step is not None:
                    if j_rsv_step not in list_:
                        list_.append(j_rsv_step)
        return list_
    #
    def _project__get_rsv_step_(self, rsv_obj, **kwargs):
        kwargs_over = self._copy_variants_as_branches_(
            rsv_obj.properties.get_value()
        )
        #
        kwargs_over.update(kwargs)
        #
        rsv_type = self.VariantTypes.Step
        rsv_category = self.VariantCategories.Step
        kwargs_over['type'] = rsv_type
        if rsv_type in kwargs_over:
            name = kwargs_over[rsv_type]
            kwargs_over[rsv_type] = name
            #
            branch = self._guess_branch_(**kwargs_over)
            name_includes = self.get_steps(
                branch, with_extra=True
            )
            if name_includes:
                if name not in name_includes:
                    return
        else:
            raise KeyError()
        #
        obj_path = self._get_main_rsv_path_(rsv_category, kwargs_over)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        return self._project__create_rsv_step_auto_(**kwargs_over)

    def _project__create_rsv_step_auto_(self, **kwargs):
        if 'resolver_result' in kwargs:
            return self._project__create_rsv_step_(**kwargs)
        return self._project__search_rsv_step_(**kwargs)

    def _project__search_rsv_step_(self, **kwargs):
        rsv_type = self.VariantTypes.Step
        branch = self._guess_branch_(**kwargs)
        search_patterns = self._project_get_search_patterns_(branch, rsv_type)
        for i_workspace_key, i_pattern_args in search_patterns.items():
            i_kwargs_over = copy.copy(kwargs)
            i_kwargs_over['pattern'] = i_pattern_args
            i_kwargs_over['workspace'] = self.get_workspace(i_workspace_key)
            i_rsv_matcher = self._project__create_main_rsv_matcher_(
                i_kwargs_over
            )
            i_matches = i_rsv_matcher.get_matches()
            for j_match in i_matches:
                j_result, j_variants = j_match
                j_kwargs_over = self._copy_variants_as_branches_(i_kwargs_over)
                j_kwargs_over.update(j_variants)
                j_kwargs_over['resolver_workspace_key'] = i_workspace_key
                j_kwargs_over['resolver_pattern'] = i_pattern_args
                j_kwargs_over['resolver_result'] = j_result
                j_rsv_step = self._project__create_rsv_step_(**j_kwargs_over)
                if j_rsv_step is not None:
                    return j_rsv_step
        return None

    def _project__create_rsv_step_(self, **kwargs):
        rsv_category = self.VariantCategories.Step
        rsv_type = self.VariantTypes.Step
        result = kwargs.pop('resolver_result')
        kwargs['workspace_key'] = kwargs.pop('resolver_workspace_key')
        kwargs['pattern'] = kwargs.pop('resolver_pattern')
        variants = dict()
        self._completion_branch_rsv_create_kwargs_(
            rsv_category, rsv_type,
            kwargs, result, variants
        )
        rsv_obj = self.RSV_STEP_CLASS(self, **kwargs)
        self._project__set_rsv_obj_add_(rsv_obj)
        return rsv_obj
    #
    def get_rsv_steps(self, **kwargs):
        branch = self._guess_branch_(**kwargs)
        if branch is not None:
            kwargs['branch'] = branch
            return self._project__get_rsv_steps_(**kwargs)
        else:
            list_ = []
            for i_branch in self.Branches.Mains:
                kwargs['branch'] = i_branch
                list_.extend(
                    self._project__get_rsv_steps_(**kwargs)
                )
            return list_
    #
    def get_rsv_step(self, **kwargs):
        if 'asset' in kwargs or 'shot' in kwargs:
            return self._resource__get_rsv_step_(**kwargs)
        #
        _ = self.get_rsv_steps(**kwargs)
        if _:
            return _[-1]
    # task
    def _step__get_rsv_task_(self, **kwargs):
        rsv_step = self.get_rsv_step(**kwargs)
        if rsv_step is not None:
            return rsv_step.get_rsv_task(**kwargs)

    def _project__get_rsv_tasks_(self, **kwargs):
        list_ = []
        #
        rsv_type = self.VariantTypes.Task
        branch = self._guess_branch_(**kwargs)
        search_patterns = self._project_get_search_patterns_(branch, rsv_type)
        for i_workspace_key, i_pattern in search_patterns.items():
            i_kwargs_over = copy.copy(kwargs)
            i_kwargs_over['pattern'] = i_pattern
            i_kwargs_over['workspace'] = self.get_workspace(i_workspace_key)
            i_rsv_matcher = self._project__create_main_rsv_matcher_(
                i_kwargs_over
            )
            i_matches = i_rsv_matcher.get_matches()
            for j_match in i_matches:
                j_result, j_variants = j_match
                j_kwargs_over = self._copy_variants_as_branches_(i_kwargs_over)
                j_kwargs_over.update(j_variants)
                j_kwargs_over['resolver_workspace_key'] = i_workspace_key
                j_kwargs_over['resolver_pattern'] = i_pattern
                j_kwargs_over['resolver_result'] = j_result
                j_rsv_task = self._step__get_rsv_task_(**j_kwargs_over)
                if j_rsv_task is not None:
                    if j_rsv_task not in list_:
                        list_.append(j_rsv_task)
        return list_

    def _project__get_rsv_task_(self, rsv_obj, **kwargs):
        rsv_category = self.VariantCategories.Task
        rsv_type = self.VariantTypes.Task
        #
        kwargs_over = self._copy_variants_as_branches_(
            rsv_obj.properties.get_value()
        )
        #
        kwargs_over.update(kwargs)
        #
        kwargs_over['type'] = rsv_type
        if rsv_type in kwargs_over:
            name = kwargs_over[rsv_type]
            kwargs_over[rsv_type] = name
        else:
            raise KeyError()
        obj_path = self._get_main_rsv_path_(rsv_category, kwargs_over)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        #
        return self._project__create_rsv_task_auto_(**kwargs_over)

    def _project__create_rsv_task_auto_(self, **kwargs):
        if 'resolver_result' in kwargs:
            return self._project__create_rsv_task_(**kwargs)
        return self._project__search_rsv_task_(**kwargs)

    def _project__search_rsv_task_(self, **kwargs):
        rsv_type = self.VariantTypes.Task
        branch = self._guess_branch_(**kwargs)
        search_patterns = self._project_get_search_patterns_(branch, rsv_type)
        for i_workspace_key, i_pattern_args in search_patterns.items():
            i_kwargs_over = copy.copy(kwargs)
            i_kwargs_over['pattern'] = i_pattern_args
            i_kwargs_over['workspace'] = self.get_workspace(i_workspace_key)
            i_rsv_matcher = self._project__create_main_rsv_matcher_(
                i_kwargs_over
            )
            i_matches = i_rsv_matcher.get_matches()
            for j_match in i_matches:
                j_result, j_variants = j_match
                j_kwargs_over = self._copy_variants_as_branches_(i_kwargs_over)
                j_kwargs_over.update(j_variants)
                j_kwargs_over['resolver_workspace_key'] = i_workspace_key
                j_kwargs_over['resolver_pattern'] = i_pattern_args
                j_kwargs_over['resolver_result'] = j_result
                j_rsv_task = self._project__create_rsv_task_(**j_kwargs_over)
                if j_rsv_task is not None:
                    return j_rsv_task
        return None

    def _project__create_rsv_task_(self, **kwargs):
        rsv_category = self.VariantCategories.Task
        rsv_type = self.VariantTypes.Task
        result = kwargs.pop('resolver_result')
        kwargs['workspace_key'] = kwargs.pop('resolver_workspace_key')
        kwargs['pattern'] = kwargs.pop('resolver_pattern')
        variants = dict()
        self._completion_branch_rsv_create_kwargs_(
            rsv_category, rsv_type,
            kwargs, result, variants
        )
        rsv_obj = self.RSV_TASK_CLASS(self, **kwargs)
        self._project__set_rsv_obj_add_(rsv_obj)
        return rsv_obj
    #
    def _project__set_rsv_task_create_(self, **kwargs):
        rsv_matcher = self._project__create_main_rsv_matcher_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            result, variants = matches[-1]
            self._completion_rsv_obj_create_kwargs_(kwargs, result, variants)
            rsv_obj = self.RSV_TASK_CLASS(self, **kwargs)
            self._project__set_rsv_obj_add_(rsv_obj)
            return rsv_obj
    #
    def get_rsv_task(self, **kwargs):
        if 'step' in kwargs:
            return self._step__get_rsv_task_(**kwargs)
        #
        _ = self.get_rsv_tasks(**kwargs)
        if _:
            return _[-1]
    #
    def get_rsv_tasks(self, **kwargs):
        branch = self._guess_branch_(**kwargs)
        if branch is not None:
            kwargs['branch'] = branch
            return self._project__get_rsv_tasks_(**kwargs)
        else:
            list_ = []
            for i_branch in self.Branches.Mains:
                kwargs['branch'] = i_branch
                list_.extend(
                    self._project__get_rsv_tasks_(**kwargs)
                )
            return list_
    # task version
    def get_rsv_task_version(self, **kwargs):
        if 'version' in kwargs:
            return self._task__get_rsv_version_(**kwargs)
        #
        _ = self.get_rsv_task_versions(**kwargs)
        if _:
            return _[-1]
    #
    def get_rsv_task_versions(self, **kwargs):
        branch = self._guess_branch_(**kwargs)
        if branch is not None:
            kwargs['branch'] = branch
            return self._project__get_rsv_task_versions_(**kwargs)
        else:
            list_ = []
            for i_branch in self.Branches.Mains:
                kwargs['branch'] = i_branch
                list_.extend(
                    self._project__get_rsv_task_versions_(**kwargs)
                )
            return list_

    def _task__get_rsv_version_(self, **kwargs):
        rsv_task = self.get_rsv_task(**kwargs)
        if rsv_task is not None:
            return rsv_task.get_rsv_version(**kwargs)

    def _project__get_rsv_task_versions_(self, **kwargs):
        list_ = []
        #
        rsv_type = self.VariantTypes.Version
        branch = self._guess_branch_(**kwargs)
        #
        workspace_key, workspace = self._project_update_workspace_variants_(kwargs)
        #
        keyword = '{}-{}-{}-dir'.format(branch, workspace_key, rsv_type)
        kwargs['keyword'] = keyword
        kwargs['pattern'] = self.get_pattern(keyword=keyword)
        rsv_matcher = self._project__create_main_rsv_matcher_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        for i_m in matches:
            _, i_variants = i_m
            i_kwargs = copy.copy(kwargs)
            i_kwargs.update(i_variants)
            #
            i_rsv_version = self._task__get_rsv_version_(**i_kwargs)
            if i_rsv_version is not None:
                if i_rsv_version not in list_:
                    list_.append(i_rsv_version)
        return list_

    def _project__get_rsv_task_version_(self, rsv_obj, **kwargs):
        kwargs_over = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_over[k] = v
        #
        kwargs_over.update(kwargs)
        #
        rsv_type = self.VariantTypes.Version
        branch = self._guess_branch_(**kwargs_over)
        #
        workspace_key, workspace = self._project_update_workspace_variants_(kwargs)
        keyword = '{}-{}-{}-dir'.format(branch, workspace_key, rsv_type)
        if rsv_type in kwargs_over:
            name = kwargs_over[rsv_type]
        else:
            raise KeyError()
        #
        if MtdBasic._set_name_check_(rsv_type, name) is False:
            return None
        #
        kwargs_over['type'] = rsv_type
        kwargs_over['keyword'] = keyword
        kwargs_over[rsv_type] = name
        #
        obj_path = self._get_version_rsv_path_(rsv_obj.path, kwargs_over)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        #
        variants = self._get_rsv_obj_create_kwargs_(
            obj_path,
            kwargs_over,
            extend_keys=['type', 'branch']
        )
        return self._project__set_rsv_task_version_create_(**variants)

    def _project__set_rsv_task_version_create_(self, **kwargs):
        rsv_matcher = self._project__create_main_rsv_matcher_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            result, variants = matches[-1]
            self._completion_rsv_obj_create_kwargs_(kwargs, result, variants)
            rsv_obj = self.RSV_TASK_VERSION_CLASS(self, **kwargs)
            self._project__set_rsv_obj_add_(rsv_obj)
            return rsv_obj
    # unit
    def get_rsv_task_unit(self, **kwargs):
        rsv_task = self.get_rsv_task(**kwargs)
        if rsv_task is not None:
            return rsv_task.get_rsv_unit(**kwargs)

    def get_rsv_unit(self, **kwargs):
        return self._project__get_rsv_unit_(
            self, **kwargs
        )

    def _project__get_rsv_unit_(self, rsv_obj, **kwargs):
        kwargs_over = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_over[k] = v
        #
        kwargs_over.update(kwargs)
        #
        rsv_type = 'unit'
        kwargs_over['type'] = rsv_type
        keyword = self._completion_keyword_by_variants_(kwargs_over)
        kwargs_over['keyword'] = keyword
        if 'platform' not in kwargs_over:
            kwargs_over['platform'] = bsc_core.SystemMtd.get_platform()
        #
        if 'version' not in kwargs_over:
            kwargs_over['version'] = rsv_configure.Version.LATEST
        #
        workspace = self._project__guess_workspace_extra_(**kwargs_over)
        kwargs_over['workspace'] = workspace
        workspace_key = self._project__get_workspace_key_by_variants_(kwargs_over)
        kwargs_over['workspace_key'] = workspace_key
        obj_path = self._get_unit_rsv_path_(rsv_obj.path, kwargs_over)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        #
        variants = self._get_rsv_obj_create_kwargs_(
            obj_path,
            kwargs_over,
            extend_keys=['type', 'platform', 'application', 'branch', 'workspace', 'workspace_key', 'keyword']
        )
        return self._project__set_rsv_unit_create_(**variants)

    def _project__set_rsv_unit_create_(self, **kwargs):
        rsv_obj = self.RSV_UNIT_CLASS(self, **kwargs)
        self._project__set_rsv_obj_add_(rsv_obj)
        return rsv_obj

    def _project__get_rsv_unit_version_(self, rsv_obj, **kwargs):
        kwargs_over = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_over[k] = v
        #
        kwargs_over.update(kwargs)
        #
        rsv_type = 'version'
        keyword = rsv_obj.get('keyword')
        #
        if rsv_type in kwargs_over:
            name = kwargs_over[rsv_type]
        else:
            raise KeyError()
        #
        if MtdBasic._set_name_check_(rsv_type, name) is False:
            return None
        #
        kwargs_over['type'] = rsv_type
        kwargs_over['keyword'] = keyword
        kwargs_over[rsv_type] = name
        #
        obj_path = self._get_version_rsv_path_(rsv_obj.path, kwargs_over)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        #
        variants = self._get_rsv_obj_create_kwargs_(
            obj_path,
            kwargs_over,
            extend_keys=['type', 'branch']
        )
        return self._project__set_rsv_unit_version_create_(**variants)

    def _project__set_rsv_unit_version_create_(self, **kwargs):
        rsv_matcher = self._project__create_rsv_matcher_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            result, variants = matches[-1]
            self._completion_rsv_obj_create_kwargs_(kwargs, result, variants)
            rsv_obj = self.RSV_UNIT_VERSION_CLASS(self, **kwargs)
            self._project__set_rsv_obj_add_(rsv_obj)
            return rsv_obj

    def _unit__get_rsv_version_(self, **kwargs):
        rsv_task = self.get_rsv_task(**kwargs)
        if rsv_task is not None:
            return rsv_task.get_rsv_version(**kwargs)
    # app
    def get_rsv_app(self, application):
        configure = bsc_objects.Configure(value=self.get_package_data())
        scheme = configure.get('scheme')
        if scheme == 'default':
            return self.RSV_APP_DEFAULT_CLASS(
                rsv_project=self,
                application=application,
                configure=configure
            )
        elif scheme == 'new':
            return self.RSV_APP_NEW_CLASS(
                rsv_project=self,
                application=application,
                configure=configure
            )

    def get_framework_scheme(self):
        return self._raw_opt.get('schemes.framework')

    def get_package_data(self):
        return self._raw_opt.get('package-data')

    def get_storage_scheme(self):
        return self._raw_opt.get('schemes.storage')

    def get_dcc_data(self, application):
        app_data = self._raw_opt.get_content_as_unfold(
            'dcc-data.{}'.format(application)
        )
        extend_data = self._raw_opt.get('dcc-data.extend') or {}
        for k, v in extend_data.items():
            app_data.set(
                k, v.format(**app_data.value)
            )
        app_extend_data = self._raw_opt.get('dcc-data.{}-extend'.format(application)) or {}
        for k, v in app_extend_data.items():
            app_data.set(
                k, v.format(**app_data.value)
            )
        return app_data.get_value()

    def _get_rsv_obj_exists_(self, rsv_obj_path):
        return self._rsv_obj_stack.get_object_exists(rsv_obj_path)

    def _project__set_rsv_obj_add_(self, rsv_obj):
        self._rsv_obj_stack.set_object_add(rsv_obj)
        if rsv_core.TRACE_RESULT_ENABLE is True:

            bsc_core.LogMtd.trace_method_result(
                'resolver',
                u'{}="{}"'.format(rsv_obj.type, rsv_obj.path)
            )

    def _project__get_rsv_obj_(self, path):
        if path == '/':
            return self._rsv_root
        elif path == self.path:
            return self
        return self._rsv_obj_stack.get_object(path)

    def _project__get_rsv_objs_(self, regex=None):
        return self._rsv_obj_stack.get_objects(regex)

    def _project__get_rsv_obj_child_paths_(self, path):
        return bsc_core.DccPathDagMtd.get_dag_children(path, self._rsv_obj_stack.get_keys())

    def _project__get_rsv_obj_children_(self, path):
        child_paths = bsc_core.DccPathDagMtd.get_dag_children(path, self._rsv_obj_stack.get_keys())
        return [self._rsv_obj_stack.get_object(i) for i in child_paths]
    # gain by file-path
    def _project__get_rsv_entity_by_file_path_(self, file_path, variants_override):
        if file_path is not None:
            for i_branch in self.Branches.Mains:
                i_pattern = self.get_pattern(keyword='{}-dir'.format(i_branch))
                i_pattern_ = '{}/{{extra}}'.format(i_pattern)

                i_rsv_matcher = self._create_rsv_matcher_(
                    i_pattern_, variants_override
                )
                i_properties = i_rsv_matcher.get_properties_by_result(result=file_path)
                if i_properties:
                    i_properties.set('branch', i_branch)
                    i_rsv_entity = self.get_rsv_resource(**i_properties.value)
                    return i_rsv_entity

    def get_rsv_step_by_any_file_path(self, file_path):
        return self._project__get_rsv_step_by_any_file_path_(file_path)

    def _project__get_rsv_step_by_any_file_path_(self, file_path):
        if file_path is not None:
            rsv_type = self.VariantTypes.Step
            for i_branch in self.Branches.All:
                search_pattern = self._project_get_search_patterns_(i_branch, rsv_type)
                for j_workspace_key in self.WorkspaceKeys.All:
                    if j_workspace_key in search_pattern:
                        j_pattern = search_pattern[j_workspace_key]
                        if '{ext}' not in j_pattern:
                            j_pattern_extra = '{}/{{extra}}'.format(j_pattern)
                        else:
                            j_pattern_extra = j_pattern
                        #
                        j_rsv_matcher = self._create_rsv_matcher_(
                            j_pattern_extra, variants_override={}
                        )
                        j_properties = j_rsv_matcher.get_properties_by_result(result=file_path)
                        if j_properties:
                            j_kwargs_over = self._copy_variants_as_branches_(j_properties.get_value())
                            j_kwargs_over['resolver_workspace_key'] = j_workspace_key
                            j_kwargs_over['resolver_pattern'] = j_pattern
                            j_kwargs_over['resolver_result'] = file_path
                            i_rsv_step = self.get_rsv_step(**j_kwargs_over)
                            if i_rsv_step is not None:
                                return i_rsv_step
    # scene
    def _project__get_rsv_task_by_any_file_path_(self, file_path):
        if file_path is not None:
            rsv_type = self.VariantTypes.Task
            for i_branch in self.Branches.All:
                search_pattern = self._project_get_search_patterns_(i_branch, rsv_type)
                for j_workspace_key in self.WorkspaceKeys.All:
                    if j_workspace_key in search_pattern:
                        j_pattern = search_pattern[j_workspace_key]
                        if '{ext}' not in j_pattern:
                            j_pattern_extra = '{}/{{extra}}'.format(j_pattern)
                        else:
                            j_pattern_extra = j_pattern
                        j_rsv_matcher = self._create_rsv_matcher_(
                            j_pattern_extra, variants_override={}
                        )
                        j_properties = j_rsv_matcher.get_properties_by_result(result=file_path)
                        if j_properties:
                            j_kwargs_over = self._copy_variants_as_branches_(j_properties.get_value())
                            j_kwargs_over['resolver_workspace_key'] = j_workspace_key
                            j_kwargs_over['resolver_pattern'] = j_pattern
                            j_kwargs_over['resolver_result'] = file_path
                            i_rsv_task = self.get_rsv_task(**j_kwargs_over)
                            if i_rsv_task is not None:
                                return i_rsv_task
    # output
    def get_rsv_task_by_output_file_path(self, file_path):
        return self._project__get_rsv_task_by_any_file_path_(
            file_path,
            variants_override=dict(workspace=self.get_workspace_temporary())
        )

    def get_rsv_task_by_any_file_path(self, file_path):
        return self._project__get_rsv_task_by_any_file_path_(file_path)

    def get_rsv_version_by_any_file_path(self, file_path):
        pass

    def get_folders(self):
        pass

    def get_rsv_obj_by_path(self, rsv_obj_type_name, rsv_obj_path):
        keyword_dict = {
            'project': 'project-dir'
        }

    def set_gui_attribute_restore(self):
        for i in self._rsv_obj_stack.get_objects():
            i.set_obj_gui(None)

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type,
            self.path
        )

    def __repr__(self):
        return self.__str__()


# <resolver>
class AbsRsvRoot(
    AbsRsvExtraDef,
    unr_abstracts.AbsObjGuiDef,
    unr_abstracts.AbsObjDagDef,
):
    OBJ_UNIVERSE_CLASS = None
    #
    RSV_PROJECT_STACK_CLASS = None
    RSV_PROJECT_CLASS = None

    RSV_VERSION_KEY_CLASS = None
    def __init__(self):
        self._set_rsv_def_init_()
        self._set_obj_dag_def_init_('/')
        self._set_obj_gui_def_init_()
        #
        self._rsv_project_stack = self.RSV_PROJECT_STACK_CLASS()
        self._obj_universe = self.OBJ_UNIVERSE_CLASS()
        #
        raw = rsv_core.RsvConfigureMtd.get_basic_raw()
        self.init_rsv_extra(raw)
        #
        self._default_root_to_project_dict = {}
        #
        self._update_all_patterns_()
        self._update_all_projects_()

    def _update_all_projects_(self):
        default_raws = rsv_core.RsvConfigureMtd.get_default_raws()
        for i_raw in default_raws:
            i_project_raw_opt = self._get_raw_opt_(i_raw)
            key = i_project_raw_opt.get('key')
            if key is not None:
                projects = i_project_raw_opt.get('projects-include') or []
                for j_project in projects:
                    j_raw = copy.copy(i_raw)
                    j_project_raw_opt = self._get_raw_opt_(j_raw)
                    j_project_raw_opt.set('key', j_project)
                    self._create_rsv_project_(j_raw, project=j_project)
    @property
    def type(self):
        return 'resolver'
    @property
    def type_name(self):
        return self.type
    @property
    def pathsep(self):
        return '/'
    @property
    def path(self):
        return '/'
    @property
    def name(self):
        return ''
    @property
    def icon(self):
        return bsc_core.RscIconFileMtd.get('resolver/root')

    def _set_dag_create_(self, path):
        if path == self.path:
            return self

    def _get_child_paths_(self, *args, **kwargs):
        return self._rsv_project_stack.get_keys()

    def _set_child_create_(self, path):
        return self._rsv_project_stack.get_object(path)
    @property
    def pattern_dict(self):
        return self._patterns_dict
    @classmethod
    def get_platform(cls):
        if platform.system() == 'Windows':
            return 'windows'
        elif platform.system() == 'Linux':
            return 'linux'
    @classmethod
    def _get_rsv_kwargs_(cls, **kwargs):
        dic = {}
        # use url
        if 'url' in kwargs:
            url = kwargs['url']
            dic = MtdBasic._get_parameter_by_url_(url)
        elif 'file' in kwargs:
            dic = kwargs
            k = kwargs['file']
            keyword = '{}-file'.format(k)
            if fnmatch.filter([keyword], 'asset-*'):
                branch = 'asset'
            elif fnmatch.filter([keyword], 'shot-*'):
                branch = 'shot'
            else:
                raise TypeError()
            dic['branch'] = branch
        # use keyword
        elif 'keyword' in kwargs:
            dic = kwargs
            keyword = kwargs['keyword']
            if fnmatch.filter([keyword], 'asset-*'):
                branch = 'asset'
            elif fnmatch.filter([keyword], 'shot-*'):
                branch = 'shot'
            else:
                raise TypeError()
            dic['branch'] = branch
        else:
            dic = kwargs
        return dic

    def get_rsv_projects(self):
        return self._rsv_project_stack.get_objects()

    def get_rsv_project(self, *args, **kwargs):
        self._update_all_projects_()
        return self._get_exists_rsv_project_(*args, **kwargs)

    def get_rsv_project_is_exists(self, **kwargs):
        return

    def _create_rsv_project_(self, *args, **kwargs):
        kwargs_over = collections.OrderedDict()
        kwargs_over.update(kwargs)
        rsv_type = 'project'
        if rsv_type in kwargs_over:
            name = kwargs_over[rsv_type]
        else:
            raise KeyError()
        #
        kwargs_over['type'] = rsv_type
        kwargs_over[rsv_type] = name
        keyword = '{}-dir'.format(rsv_type)
        kwargs_over['keyword'] = keyword
        #
        obj_path = self._get_main_rsv_path_(self.VariantCategories.Project, kwargs_over)
        if self._rsv_project_stack.get_object_exists(obj_path) is True:
            rsv_project = self._rsv_project_stack.get_object(obj_path)
            if 'platform' in kwargs_over:
                rsv_project._project_update_roots_to_properties_(kwargs_over['platform'])
            else:
                rsv_project._project_update_roots_to_properties_(platform_=self.get_platform())
            #
            rsv_project._project_update_static_variants_to_properties_()
            return rsv_project
        #
        variants = self._get_rsv_obj_create_kwargs_(
            obj_path,
            kwargs_over,
            extend_keys=['type']
        )
        return self._root__set_rsv_project_create_(*args, **variants)

    def _get_exists_rsv_project_(self, **kwargs):
        kwargs_over = collections.OrderedDict()
        kwargs_over.update(kwargs)
        rsv_type = 'project'
        if rsv_type in kwargs_over:
            name = kwargs_over[rsv_type]
        else:
            raise KeyError()
        #
        kwargs_over['type'] = rsv_type
        kwargs_over[rsv_type] = name
        keyword = '{}-dir'.format(rsv_type)
        kwargs_over['keyword'] = keyword
        #
        obj_path = self._get_main_rsv_path_(self.VariantCategories.Project, kwargs_over)
        if self._rsv_project_stack.get_object_exists(obj_path) is True:
            rsv_project = self._rsv_project_stack.get_object(obj_path)
            if 'platform' in kwargs_over:
                rsv_project._project_update_roots_to_properties_(kwargs_over['platform'])
            else:
                rsv_project._project_update_roots_to_properties_(platform_=self.get_platform())
            #
            rsv_project._project_update_static_variants_to_properties_()
            return rsv_project
        #
        # project = kwargs['project']
        # #
        # default_project = self._rsv_project_stack.get_object('/default')
        # default_project_raw = copy.copy(default_project._raw)
        # default_project_raw['key'] = project
        # return self._create_rsv_project_(default_project_raw, project=project)

    def _root__set_rsv_project_create_(self, *args, **kwargs):
        rsv_project = self.RSV_PROJECT_CLASS(self, *args, **kwargs)
        rsv_project._project_update_roots_to_properties_(platform_=self.get_platform())
        rsv_project._project_update_static_variants_to_properties_()
        obj_type = rsv_project.type
        obj_path = rsv_project.path
        self._rsv_project_stack.set_object_add(rsv_project)
        if rsv_core.TRACE_RESULT_ENABLE is True:
            bsc_core.LogMtd.trace_method_result(
                'resolver',
                u'{}="{}"'.format(obj_type, obj_path)
            )
        return rsv_project
    # scene
    def get_rsv_project_by_any_file_path(self, file_path):
        return self._root__get_rsv_project_by_any_file_path_(file_path)

    def _root__get_rsv_project_by_any_file_path_(self, file_path):
        rsv_projects = self.get_rsv_projects()
        for i_rsv_project in rsv_projects:
            i_project = i_rsv_project.get('project')
            for j_platform in self.Platforms.All:
                j_root = i_rsv_project.get_pattern('project-root-{}-dir'.format(j_platform))
                j_glob_pattern = '{}/*'.format(j_root)
                j_results = fnmatch.filter([file_path.lower()], j_glob_pattern)
                if j_results:
                    j_variants = {'root': j_root}
                    j_keyword = 'project-dir'
                    j_pattern = i_rsv_project.get_pattern(j_keyword)
                    j_pattern_ = '{}/{{extra}}'.format(j_pattern)
                    j_variants['keyword'] = j_keyword
                    j_variants['pattern'] = j_pattern_
                    j_rsv_matcher = i_rsv_project._create_rsv_matcher_(
                        j_pattern_, j_variants
                    )
                    j_project_rsv_properties = j_rsv_matcher.get_properties_by_result(file_path)
                    if j_project_rsv_properties:
                        j_project = j_project_rsv_properties.get('project')
                        if j_project == i_project:
                            i_rsv_project.properties.set('platform', j_platform)
                            i_rsv_project.properties.set('root', j_root)
                            return i_rsv_project
        #
        return self._resolver__get_rsv_project_use_default_(file_path)
    # = rsv_project.get_rsv_resources
    def get_rsv_resources(self, **kwargs):
        kwargs_over = self._get_rsv_kwargs_(**kwargs)
        if kwargs_over:
            rsv_project = self.get_rsv_project(**kwargs_over)
            if rsv_project:
                return rsv_project.get_rsv_resources(**kwargs_over)
    # = rsv_project.get_rsv_resource
    def get_rsv_resource(self, **kwargs):
        kwargs_over = self._get_rsv_kwargs_(**kwargs)
        if kwargs_over:
            rsv_project = self.get_rsv_project(**kwargs_over)
            if rsv_project:
                return rsv_project.get_rsv_resource(**kwargs_over)
    #
    def get_rsv_step(self, **kwargs):
        kwargs_over = self._get_rsv_kwargs_(**kwargs)
        if kwargs_over:
            rsv_project = self.get_rsv_project(**kwargs_over)
            if rsv_project:
                return rsv_project.get_rsv_step(**kwargs_over)
    # = rsv_project.get_rsv_task
    def get_rsv_task(self, **kwargs):
        kwargs_over = self._get_rsv_kwargs_(**kwargs)
        if kwargs_over:
            rsv_project = self.get_rsv_project(**kwargs_over)
            if rsv_project:
                return rsv_project.get_rsv_task(**kwargs_over)

    def get_rsv_tasks(self, **kwargs):
        kwargs_over = self._get_rsv_kwargs_(**kwargs)
        if kwargs_over:
            rsv_project = self.get_rsv_project(**kwargs_over)
            if rsv_project:
                return rsv_project.get_rsv_tasks(**kwargs_over)

    def get_rsv_task_version(self, **kwargs):
        kwargs_over = self._get_rsv_kwargs_(**kwargs)
        if kwargs_over:
            rsv_project = self.get_rsv_project(**kwargs_over)
            if rsv_project:
                return rsv_project.get_rsv_task_version(**kwargs_over)
    # = rsv_project.get_rsv_unit
    def get_rsv_unit(self, **kwargs):
        kwargs_over = self._get_rsv_kwargs_(**kwargs)
        if kwargs_over:
            rsv_project = self.get_rsv_project(**kwargs_over)
            if rsv_project:
                return rsv_project.get_rsv_unit(**kwargs_over)
    #
    def get_result(self, **kwargs):
        rsv_unit = self.get_rsv_unit(**kwargs)
        return rsv_unit.get_result(
            version=kwargs['version'],
            extend_variants=kwargs
        )

    def get_rsv_step_by_any_file_path(self, file_path):
        rsv_project = self._root__get_rsv_project_by_any_file_path_(file_path)
        if rsv_project is not None:
            return rsv_project._project__get_rsv_step_by_any_file_path_(
                file_path
            )
        else:
            if rsv_core.TRACE_WARNING_ENABLE is True:
                bsc_core.LogMtd.trace_method_warning(
                    'project-resolver',
                    u'file="{}" is not available'.format(file_path)
                )
        return None

    def get_rsv_task_by_any_file_path(self, file_path):
        rsv_project = self._root__get_rsv_project_by_any_file_path_(file_path)
        if rsv_project is not None:
            return rsv_project._project__get_rsv_task_by_any_file_path_(
                file_path
            )
        else:
            if rsv_core.TRACE_WARNING_ENABLE is True:
                bsc_core.LogMtd.trace_method_warning(
                    'project-resolver',
                    u'file="{}" is not available'.format(file_path)
                )
        return None
    #
    def _resolver__get_rsv_project_use_default_(self, file_path):
        rsv_project = self.get_rsv_project(project='default')
        if rsv_project is not None:
            for i_platform in self.Platforms.All:
                i_root = rsv_project.get_pattern('project-root-{}-dir'.format(i_platform))
                i_glob_pattern = '{}/*'.format(i_root)
                i_results = fnmatch.filter([file_path.lower()], i_glob_pattern)
                if i_results:
                    i_variants = {'root': i_root}
                    i_pattern = rsv_project.get_pattern('project-dir')
                    i_pattern_ = '{}/{{extra}}'.format(i_pattern)
                    i_rsv_matcher = rsv_project._create_rsv_matcher_(
                        i_pattern_, i_variants
                    )
                    i_project_properties = i_rsv_matcher._get_project_properties_by_default_(file_path)
                    i_project = i_project_properties.get('project')
                    if rsv_core.TRACE_RESULT_ENABLE is True:
                        bsc_core.LogMtd.trace_method_result(
                            'resolver project create',
                            'project-name="{}", create use "default"'.format(i_project)
                        )
                    return self.get_rsv_project(project=i_project)

    def get_task_properties_by_work_scene_src_file_path(self, file_path):
        _ = self._get_rsv_task_properties_by_work_scene_src_file_path_(file_path)
        if _ is not None:
            return _
        else:
            if rsv_core.TRACE_WARNING_ENABLE is True:
                bsc_core.LogMtd.trace_method_warning(
                    'work-scene-src-file-resolver',
                    u'file="{}" is not available'.format(file_path)
                )
        return None
    #
    def _get_rsv_task_properties_by_work_scene_src_file_path_(self, file_path):
        rsv_task = self.get_rsv_task_by_any_file_path(file_path)
        if rsv_task is not None:
            return rsv_task.get_properties_by_work_scene_src_file_path(file_path)

    def get_task_properties_by_scene_src_file_path(self, file_path):
        _ = self._get_rsv_task_properties_by_scene_src_file_path_(file_path)
        if _ is not None:
            return _
        else:
            if rsv_core.TRACE_WARNING_ENABLE is True:
                bsc_core.LogMtd.trace_method_warning(
                    'scene-src-file-resolver',
                    u'file="{}" is not available'.format(file_path)
                )
        return None
    #
    def _get_rsv_task_properties_by_scene_src_file_path_(self, file_path):
        rsv_task = self.get_rsv_task_by_any_file_path(file_path)
        if rsv_task is not None:
            return rsv_task.get_properties_by_scene_src_file_path(file_path)
    #
    def _get_rsv_task_properties_by_scene_file_path_(self, file_path):
        rsv_task = self.get_rsv_task_by_any_file_path(file_path)
        if rsv_task is not None:
            return rsv_task.get_properties_by_scene_file_path(file_path)

    def _get_rsv_task_properties_by_output_scene_src_file_path_(self, file_path):
        rsv_task = self.get_rsv_task_by_any_file_path(file_path)
        if rsv_task is not None:
            return rsv_task.get_properties_by_output_scene_src_file_path(file_path)

    def _get_rsv_task_properties_by_output_scene_file_path_(self, file_path):
        rsv_task = self.get_rsv_task_by_any_file_path(file_path)
        if rsv_task is not None:
            return rsv_task.get_properties_by_output_scene_file_path(file_path)
    #
    def get_task_properties_by_any_scene_file_path(self, file_path):
        methods = [
            self._get_rsv_task_properties_by_work_scene_src_file_path_,
            self._get_rsv_task_properties_by_scene_src_file_path_,
            self._get_rsv_task_properties_by_scene_file_path_,
            self._get_rsv_task_properties_by_output_scene_src_file_path_,
            self._get_rsv_task_properties_by_output_scene_file_path_,
        ]
        for method in methods:
            # noinspection PyArgumentList
            result = method(bsc_core.StgPathOpt(file_path).get_path())
            if result is not None:
                # print(';'.join(['{}={}'.format(k, v) for k, v in result.value.items() if isinstance(v, six.string_types)]))
                return result
    @classmethod
    def get_path_args(cls):
        dic = collections.OrderedDict()
        return dic
    #
    def get_rsv_resource_step_directory_paths(self, **kwargs):
        list_ = []
        project = kwargs['project']
        rsv_project = self.get_rsv_project(project=project)
        branch = rsv_project._guess_branch_(**kwargs)
        keywords = [self._get_step_keyword_(branch, i) for i in self.WorkspaceKeys.Mains]
        for i_keyword in keywords:
            i_kwargs = rsv_project.properties.get_copy_value()
            i_kwargs.update(kwargs)
            i_rsv_pattern = rsv_project.get_rsv_pattern(i_keyword)
            i_workspace = rsv_project._project__guess_workspace_extra_(keyword=i_keyword)
            i_kwargs['workspace'] = i_workspace
            i_result = i_rsv_pattern.set_update(**i_kwargs)
            list_.append(i_result)
        return list_

    def get_rsv_resource_task_directory_paths(self, **kwargs):
        list_ = []
        project = kwargs['project']
        rsv_project = self.get_rsv_project(project=project)
        branch = rsv_project._guess_branch_(**kwargs)
        keywords = [self._get_task_keyword_(branch, i) for i in self.WorkspaceKeys.Mains]
        #
        for i_keyword in keywords:
            i_kwargs = rsv_project.properties.copy_value
            i_kwargs.update(kwargs)
            i_rsv_pattern = rsv_project.get_rsv_pattern(i_keyword)
            i_workspace = rsv_project._project__guess_workspace_extra_(keyword=i_keyword)
            i_kwargs['workspace'] = i_workspace
            i_result = i_rsv_pattern.set_update(**i_kwargs)
            list_.append(i_result)
        return list_

    def get_rsv_scene_properties_by_any_scene_file_path(self, file_path):
        rsv_task = self.get_rsv_task_by_any_file_path(file_path)
        if rsv_task is not None:
            return rsv_task.get_rsv_scene_properties_by_any_scene_file_path(file_path)

    def get_new_version_key(self, version):
        version_key = self.RSV_VERSION_KEY_CLASS(version)
        version_key += 1
        return version_key

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type,
            self.path
        )

    def __repr__(self):
        return self.__str__()
