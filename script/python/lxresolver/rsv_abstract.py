# coding:utf-8
from __future__ import print_function

import os

import re

import glob

import platform

import fnmatch

import parse

import collections

import copy

import json

from lxresolver import rsv_configure, rsv_core

from lxutil import utl_core

from lxbasic import bsc_core

from lxobj import obj_core, obj_abstract

import lxbasic.objects as bsc_objects

import threading

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
    def _set_pattern_update_(cls, raw, **format_variant):
        if raw is not None:
            keys = cls._get_keys_by_parse_pattern_(raw)
            s = raw
            if keys:
                for key in keys:
                    if key in format_variant:
                        v = format_variant[key]
                        if v is not None and v != '*':
                            s = s.replace('{{{}}}'.format(key), format_variant[key])
            return s
        return raw
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
                    'RsvProject-file-ext: "{}" is Non-available'.format(ext)
                )
        else:
            raise TypeError(
                'file="{}" is Non-exists'.format(file_path)
            )
    @classmethod
    def _get_rsv_pattern_real_value_(cls, value, dic):
        def _rcs_fnc(v_):
            if isinstance(v_, (str, unicode)):
                _r = v_
                _ks = re.findall(re.compile(cls.PATTERN_REF_RE_PATTERN, re.S), v_)
                if _ks:
                    for _k in set(_ks):
                        if _k not in dic:
                            raise KeyError(u'keyword: "{}" is Non-registered'.format(_k))
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
    def _get_rsv_obj_path_(cls, keys, variants):
        search_keys = [
            'project',
            #
            'role', 'sequence',
            #
            'asset', 'shot',
            #
            'step',
            'task',
            #
            # 'version'
        ]
        p_values = ['', ]
        #
        for key in keys:
            if key in search_keys:
                if key in variants:
                    p_values.append(variants[key])
                else:
                    raise KeyError('key: "{}" is Non-exists'.format(key))
        #
        return '/'.join(p_values)
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
            'version',
            #
            'workspace',
            # 'unit',
        ]
        return '/' + '/'.join([kwargs[key] for key in keys if key in kwargs])
    @classmethod
    def _str_to_number_embedded_args_(cls, string):
        pieces = re.compile(r'(\d+)').split(unicode(string))
        pieces[1::2] = map(int, pieces[1::2])
        return pieces
    @classmethod
    def _get_glob_pattern_by_parse_pattern_(cls, pattern):
        keys = cls._get_keys_by_parse_pattern_(pattern)
        s = pattern
        if keys:
            for key in keys:
                s = s.replace('{{{}}}'.format(key), '*')
            return True, s
        return False, s
    @classmethod
    def _get_keys_by_parse_pattern_(cls, pattern):
        lis_0 = re.findall(re.compile(cls.PATTERN_KEY_RE_PATTERN, re.S), pattern)
        lis_1 = list(set(lis_0))
        lis_1.sort(key=lis_0.index)
        return lis_1
    @classmethod
    def _get_stg_paths_by_parse_pattern_(cls, pattern, trim=None):
        if pattern is not None:
            enable, glob_pattern = cls._get_glob_pattern_by_parse_pattern_(pattern)
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
    def _set_name_check_(cls, type_, name):
        _ = re.findall(
            r'[^a-zA-Z0-9_]',
            name
        )
        if _:
            utl_core.Log.set_module_warning_trace(
                'name check',
                u'{}-name="{}" is not available'.format(type_, name)
            )
            return False
        return True
    @classmethod
    def _get_rsv_workspace_(cls, **kwargs):
        keyword = kwargs['keyword']
        ks = keyword.split('-')
        if ks[1] in ['work']:
            return 'work'
        elif ks[1] in ['output']:
            return 'output'
        return 'publish'
    @classmethod
    def _set_rsv_obj_sort_(cls, rsv_objs):
        lis = []
        paths = []
        obj_dic = {}
        for rsv_obj in rsv_objs:
            path = rsv_obj.path
            paths.append(path)
            obj_dic[path] = rsv_obj
        #
        paths.sort(key=lambda x: cls._str_to_number_embedded_args_(x))
        for path in paths:
            lis.append(
                obj_dic[path]
            )
        # print(paths)
        return lis


class _Thread(threading.Thread):
    def __init__(self, fnc, *args, **kwargs):
        super(_Thread, self).__init__()
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
        self.set_data(self._fnc(*self._args, **self._kwargs))
        THREAD_MAXIMUM.release()


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
    RSV_PATTERN_CLASS = None
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
    def __get_glob_pattern_by_parse_pattern_(self, pattern):
        key_glob_pattern_dic = self._rsv_project.get_value('key-glob-pattern')
        keys = MtdBasic._get_keys_by_parse_pattern_(pattern)
        s = pattern
        if keys:
            for key in keys:
                if key in key_glob_pattern_dic:
                    # _i = key_glob_pattern_dic[key]
                    # if isinstance(_i, (str, unicode)):
                    #     pass
                    # elif isinstance(_i, (tuple, list)):
                    #     pass
                    i_glob_pattern = key_glob_pattern_dic[key]
                else:
                    i_glob_pattern = '*'
                #
                s = s.replace('{{{}}}'.format(key), i_glob_pattern)
            return True, s
        return False, s
    #
    def __get_stg_paths_by_parse_pattern_(self, pattern, trim=None):
        if pattern is not None:
            enable, glob_pattern = self.__get_glob_pattern_by_parse_pattern_(pattern)
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

    def get_results(self, trim=None):
        lis = []
        for pattern in self._match_patterns:
            _, results = self.__get_stg_paths_by_parse_pattern_(pattern, trim)
            lis.extend(results)
            return lis

    def __get_matches_(self, trim):
        lis = []
        # print(self._match_patterns)
        for i_pattern in self._match_patterns:
            # print(i_pattern, 'AAA')
            enable, results = self.__get_stg_paths_by_parse_pattern_(i_pattern)
            if trim is not None:
                results = results[trim[0]:trim[1]]
            #
            for i_result in results:
                p = parse.parse(
                    self._parse_pattern, i_result
                )
                if p:
                    i_variants = p.named
                    lis.append(
                        (i_result, i_variants)
                    )
        #
        return lis#

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
                        if isinstance(v, (str, unicode)):
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
        return self.__get_matches_(trim)

    def __get_path_by_local_variants_(self, format_dict):
        pattern = self._orig_pattern
        # new_root = self._rsv_project._root_dict[self._match_variants['platform']]
        # format_dict['root'] = new_root
        # new_effect_root = self._rsv_project._root_effect_dict[self._match_variants['platform']]
        # format_dict['root_secondary'] = new_effect_root
        # new_user_name = utl_core.System.get_user_name()
        # format_dict['user'] = new_user_name
        new_result = pattern.format(**format_dict)
        return new_result

    def get_latest(self):
        matches = self.__get_matches_(trim=(-1, None))
        if matches:
            result, parameters = matches[-1]
            format_dict = copy.copy(self._match_variants)
            format_dict.update(parameters)
            return self.__get_path_by_local_variants_(format_dict)
    @classmethod
    def _get_properties_by_result_(cls, pattern, properties, result):
        # print('AAAA', pattern, result)
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


class AbsRsvObjDef(object):
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
    @property
    def name(self):
        return obj_core.DccPathDagMtd.get_dag_name(self._rsv_path, pathsep='/')
    @property
    def pattern(self):
        return self._pattern

    def _get_stack_key_(self):
        return self._rsv_path

    def get_path_args(self):
        search_keys = [
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
        for key in search_keys:
            if key in keys:
                value = self._rsv_properties.get(key)
                dic[key] = value
        return dic


class AbsRsvObj(
    AbsRsvObjDef,
    AbsRsvPropertiesDef,
    obj_abstract.AbsObjDagDef,
    # gui
    obj_abstract.AbsObjGuiDef
):
    def __init__(self, *args, **kwargs):
        self._set_rsv_properties_def_init_()
        self._set_obj_def_init_()
        #
        rsv_project = args[0]
        #
        self._rsv_project = rsv_project
        #
        self._set_rsv_obj_def_init_(
            self.PROPERTIES_CLASS(self, bsc_core.DictMtd.set_key_sort_to(kwargs))
        )
        self._set_obj_dag_def_init_(self._rsv_path)
        self._set_obj_gui_def_init_()
        #
        self._rsv_matcher = self._rsv_project._project__set_rsv_matcher_create_(
            self._rsv_properties.value
        )
        #
        self.set_gui_menu_raw(
            [
                ('{}-directory'.format(self.type_name), ),
                ('Open Work Directory', 'file/folder', (self._get_work_directory_is_enable_, self._set_work_directory_open_, False)),
                ('Open Publish Directory', 'file/folder', (self._get_publish_directory_is_enable_, self._set_publish_directory_open_, False)),
                ('Open Output Directory', 'file/folder', (self._get_output_directory_is_enable_, self._set_output_directory_open_, False)),
            ]
        )

        self.set_description(
            u'\n'.join([u'{} : {}'.format(k, v) for k, v in bsc_core.DictMtd.set_key_sort_to(kwargs).items()])
        )

    def __get_src_directory_path_(self):
        kwargs = copy.copy(self.properties.value)
        kwargs['workspace'] = self.rsv_project.get_workspace_src()
        return self._pattern.format(**kwargs)

    def _get_work_directory_is_enable_(self):
        directory_path = self.__get_src_directory_path_()
        return bsc_core.DirectoryOpt(directory_path).get_is_exists()

    def _set_work_directory_open_(self):
        directory_path = self.__get_src_directory_path_()
        bsc_core.DirectoryOpt(directory_path).set_open()

    def _get_publish_directory_path_(self):
        kwargs = copy.copy(self.properties.value)
        kwargs['workspace'] = self.rsv_project.get_workspace_release()
        return self._pattern.format(**kwargs)

    def _get_output_directory_path_(self):
        kwargs = copy.copy(self.properties.value)
        kwargs['workspace'] = self.rsv_project.get_workspace_pre_release()
        return self._pattern.format(**kwargs)

    def _get_publish_directory_is_enable_(self):
        directory_path = self._get_publish_directory_path_()
        return bsc_core.DirectoryOpt(directory_path).get_is_exists()

    def _set_publish_directory_open_(self):
        directory_path = self._get_publish_directory_path_()
        bsc_core.DirectoryOpt(directory_path).set_open()

    def _get_output_directory_is_enable_(self):
        directory_path = self._get_output_directory_path_()
        return bsc_core.DirectoryOpt(directory_path).get_is_exists()

    def _set_output_directory_open_(self):
        directory_path = self._get_output_directory_path_()
        bsc_core.DirectoryOpt(directory_path).set_open()
    @property
    def rsv_project(self):
        return self._rsv_project
    @property
    def icon(self):
        return utl_core.Icon.get('file/folder')

    def _set_dag_create_(self, path):
        return self.rsv_project._project__get_rsv_obj_(path)

    def _get_child_paths_(self, *args, **kwargs):
        return self.rsv_project._project__get_rsv_obj_child_paths_(self._rsv_path)

    def get_descendants(self):
        return self.rsv_project._project__get_rsv_objs_(regex='{}/*'.format(self.path))

    def _set_child_create_(self, path):
        return self.rsv_project._project__get_rsv_obj_(path)

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type,
            self.path
        )

    def __repr__(self):
        return self.__str__()


class AbsRsvDef(object):
    RSV_PATTERN_CLASS = None
    def _set_rsv_def_init_(self):
        self._raw = collections.OrderedDict()
        self._includes_dict = collections.OrderedDict()
        self._patterns_dict = collections.OrderedDict()
        #
        self._pattern_keys_dict = {}

    def _get_rsv_obj_create_kwargs_(self, obj_path, input_variants, extend_keys=None):
        keyword = input_variants['keyword']
        output_variants = collections.OrderedDict()
        pattern = self.get_pattern(keyword)
        keys = MtdBasic._get_keys_by_parse_pattern_(pattern)
        #
        if isinstance(extend_keys, (tuple, list)):
            keys.extend(list(extend_keys))
        #
        for key in keys:
            if key in input_variants:
                output_variants[key] = input_variants[key]
        #
        output_variants['path'] = obj_path
        output_variants['keyword'] = keyword
        output_variants['pattern'] = pattern
        return output_variants

    def _get_rsv_obj_path_(self, variants):
        keyword = variants['keyword']
        pattern = self.get_pattern(keyword)
        keys = MtdBasic._get_keys_by_parse_pattern_(pattern)
        return MtdBasic._get_rsv_obj_path_(keys, variants)

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

    def get_rsv_pattern(self, keyword):
        return self.RSV_PATTERN_CLASS(self.get_pattern(keyword))

    def get_include(self, keyword):
        if keyword in self._includes_dict:
            return self._includes_dict[keyword]
        return []

    def get_value(self, keyword):
        if keyword not in self._raw:
            raise KeyError(u'keyword: "{}" is Non-registered'.format(keyword))
        return self._raw[keyword]

    def get_pattern_keys(self, pattern):
        if pattern in self._pattern_keys_dict:
            return self._pattern_keys_dict[pattern]
        keys = MtdBasic._get_keys_by_parse_pattern_(pattern)
        self._pattern_keys_dict[pattern] = keys
        return keys


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
        kwargs['workspace'] = MtdBasic._get_rsv_workspace_(**kwargs)
        if extend_variants is not None:
            kwargs.update(extend_variants)
        #
        if version == rsv_configure.Version.LATEST:
            kwargs['version'] = '*'
            rsv_matcher = self.rsv_project._set_rsv_matcher_create_(
                self._pattern,
                kwargs
            )
            return rsv_matcher.get_latest()
        elif version == rsv_configure.Version.NEW:
            kwargs['version'] = '*'
            rsv_matcher = self.rsv_project._set_rsv_matcher_create_(
                self._pattern,
                kwargs
            )
            return rsv_matcher.get_new()
        elif version == rsv_configure.Version.ALL:
            kwargs['version'] = '*'
            rsv_matcher = self.rsv_project._set_rsv_matcher_create_(
                self._pattern,
                kwargs
            )
            return rsv_matcher.get_results(trim=trim)
        #
        kwargs['version'] = version
        rsv_matcher = self.rsv_project._set_rsv_matcher_create_(
            self._pattern,
            kwargs
        )
        return rsv_matcher.get_current()

    def get_exists_result(self, *args, **kwargs):
        result = self.get_result(*args, **kwargs)
        if result:
            if isinstance(result, (str, unicode)):
                if bsc_core.StoragePathMtd.get_path_is_exists(result):
                    return result
            elif isinstance(result, (tuple, list)):
                return result

    def get_results(self, version=None, check_exists=False, trim=None):
        kwargs = copy.copy(self.properties.value)
        if version is None:
            version = self.properties.get('version')
        #
        kwargs['workspace'] = MtdBasic._get_rsv_workspace_(**kwargs)
        if version == rsv_configure.Version.LATEST:
            version = self.get_latest_version()
        elif version == rsv_configure.Version.NEW:
            version = self.get_new_version()
        #
        if version is not None:
            kwargs['version'] = version
            kwargs['workspace'] = MtdBasic._get_rsv_workspace_(**kwargs)
            rsv_matcher = self.rsv_project._set_rsv_matcher_create_(
                self._pattern,
                kwargs
            )
            results = rsv_matcher.get_results(trim=trim)
            if check_exists is True:
                return self._set_exists_results_filter_(results)
            return results
        return []

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
            kwargs['workspace'] = MtdBasic._get_rsv_workspace_(**kwargs)
            rsv_matcher = self.rsv_project._set_rsv_matcher_create_(
                self._pattern,
                kwargs
            )
            return rsv_matcher.get_results()

    def get_extend_variants(self, file_path):
        variants = self._rsv_properties.value
        pattern = self._pattern
        rsv_matcher = self._rsv_project._set_rsv_matcher_create_(
            pattern,
            dict(
                type='unit',
                workspace='publish'
            )
        )
        cur_variants = rsv_matcher.get_properties_by_result(result=file_path)
        return {k: v for k, v in cur_variants.items() if k not in variants}

    def get_properties_by_result(self, file_path, override_variants=None):
        kwargs = copy.copy(self.properties.value)
        kwargs['workspace'] = MtdBasic._get_rsv_workspace_(**kwargs)
        if override_variants is not None:
            kwargs.update(override_variants)
        #
        rsv_matcher = self.rsv_project._set_rsv_matcher_create_(
            self._pattern,
            kwargs
        )
        file_properties = rsv_matcher.get_properties_by_result(
            result=file_path
        )
        return file_properties

    def get_latest_version(self):
        kwargs = copy.copy(self.properties.value)
        kwargs['version'] = '*'
        kwargs['workspace'] = MtdBasic._get_rsv_workspace_(**kwargs)
        rsv_matcher = self.rsv_project._set_rsv_matcher_create_(
            self._pattern,
            kwargs
        )
        matches = rsv_matcher.get_matches(trim=(-1, None))
        if matches:
            result, variants = matches[-1]
            version = variants['version']
            return version

    def get_new_version(self):
        version = self.get_latest_version()
        if version is not None:
            rsv_version_key = self._rsv_matcher._set_rsv_version_key_create_(version)
            rsv_version_key += 1
            return str(rsv_version_key)
        return 'v001'

    def get_rsv_version(self, **kwargs):
        rsv_version = self.rsv_project._project__get_rsv_unit_version_(
            rsv_obj=self,
            **kwargs
        )
        return rsv_version

    def get_rsv_versions(self):
        lis = []
        results = self.get_result(version='all')
        for i_result in results:
            i_properties = self.get_properties_by_result(i_result)
            i_properties.set('keyword', self.get('keyword'))
            i_rsv_version = self.get_rsv_version(**i_properties.value)
            lis.append(i_rsv_version)
        return lis


class AbsRsvUnitVersion(
    AbsRsvObj
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvUnitVersion, self).__init__(*args, **kwargs)
        self.set_gui_menu_raw(
            [
                ('{}-directory'.format(self.type_name), ),
                ('Open Directory', 'file/folder', (True, self._set_work_directory_open_, False)),
            ]
        )

        self._result = None

    def get_rsv_unit(self):
        return self.get_parent()

    def _set_directory_open_(self):
        if self._result:
            bsc_core.StoragePathOpt(self._result).set_open_in_system()


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
        keyword = '{}-version-dir'.format(self.get('branch'))
        rsv_unit = self.get_rsv_unit(keyword=keyword)
        return rsv_unit.get_result()


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

    def get_work_scene_src_directory_open_menu_raw(self):
        def add_fnc_(application_):
            def get_directory_is_exists_fnc_():
                return bsc_core.DirectoryOpt(_directory_path).get_is_exists()

            def set_directory_open_fnc_():
                bsc_core.DirectoryOpt(_directory_path).set_open()
            #
            _branch = self.properties.get('branch')
            _keyword = '{}-work-{}-scene-src-dir'.format(_branch, application_)
            _rsv_unit = self.get_rsv_unit(keyword=_keyword)
            _directory_path = _rsv_unit.get_result()
            lis.append(
                (application_, 'application/{}'.format(application_), (get_directory_is_exists_fnc_, set_directory_open_fnc_, False))
            )

        lis = []
        for application in rsv_configure.Application.ALL:
            add_fnc_(application)
        return lis

    def get_directory_path(self):
        keyword = '{}-version-dir'.format(self.properties.get('branch'))
        rsv_unit = self.get_rsv_unit(keyword=keyword)
        return rsv_unit.get_result()

    def get_properties_by_work_scene_src_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            key_format='{branch}-work-{application}-scene-src-file',
            override_variants=dict(workspace='work'),
            file_path_keys=['any_scene_file', 'work_scene_src_file', 'work_source_file']
        )

    def get_properties_by_scene_src_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            key_format='{branch}-{application}-scene-src-file',
            override_variants=dict(workspace='publish'),
            file_path_keys=['any_scene_file', 'scene_src_file', 'source_file']
        )
    #
    def get_properties_by_scene_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            key_format='{branch}-{application}-scene-file',
            override_variants=dict(workspace='publish'),
            file_path_keys=['any_scene_file', 'scene_file']
        )

    def get_properties_by_output_scene_src_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            key_format='{branch}-output-{application}-scene-src-file',
            override_variants=dict(workspace='output'),
            file_path_keys=['any_scene_file', 'output_scene_src_file']
        )

    def get_properties_by_output_scene_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            key_format='{branch}-output-{application}-scene-file',
            override_variants=dict(workspace='output'),
            file_path_keys=['any_scene_file', 'output_scene_file']
        )
    #
    def _get_properties_by_scene_file_path_(self, file_path, key_format, override_variants, file_path_keys):
        if file_path is not None:
            branch = self.properties.get('branch')
            for application in rsv_configure.Application.ALL:
                keyword = key_format.format(
                    **dict(branch=branch, application=application)
                )
                rsv_task_unit = self.get_rsv_unit(
                    keyword=keyword,
                    application=application
                )
                task_unit_properties = rsv_task_unit.get_properties_by_result(file_path, override_variants)
                if task_unit_properties:
                    task_unit_properties.set('application', application)
                    task_unit_properties.set('user', utl_core.System.get_user_name())
                    task_unit_properties.set('time', utl_core.System.get_time())
                    task_unit_properties.set('time_tag', utl_core.System.get_time_tag())
                    for i_file_path_key in file_path_keys:
                        task_unit_properties.set(i_file_path_key, file_path)
                    #
                    task_unit_properties.set('option.scheme', 'publish')
                    task_unit_properties.set('option.version', task_unit_properties.get('version'))
                    #
                    task_unit_properties.set('dcc.root', '/master')
                    task_unit_properties.set('dcc.root_name', 'master')
                    task_unit_properties.set('dcc.sub_root', '/master/hi')
                    #
                    task_unit_properties.set('dcc.pathsep', rsv_configure.Application.get_pathsep(application))
                    return task_unit_properties
    #
    def get_rsv_scene_properties_by_any_scene_file_path(self, file_path):
        if file_path is not None:
            branch = self.properties.get('branch')
            for i_application in rsv_configure.Application.ALL:
                for j_keyword_format, scene_type in [
                    ('{branch}-work-{application}-scene-src-file', 'work-scene-src'),
                    #
                    ('{branch}-{application}-scene-src-file', 'scene-src'),
                    ('{branch}-{application}-scene-file', 'scene-src'),
                    #
                    ('{branch}-output-{application}-scene-src-file', 'output-scene-src'),
                    ('{branch}-output-{application}-scene-file', 'output-scene'),
                ]:
                    j_keyword = j_keyword_format.format(
                        **dict(branch=branch, application=i_application)
                    )
                    if self.get_rsv_project().get_has_pattern(j_keyword):
                        j_rsv_unit = self.get_rsv_unit(
                            keyword=j_keyword,
                            application=i_application
                        )
                        j_rsv_properties = j_rsv_unit.get_properties_by_result(file_path)
                        if j_rsv_properties:
                            j_rsv_properties.set('keyword', j_keyword)
                            j_rsv_properties.set('scene_type', scene_type)

                            j_rsv_properties.set('branch', branch)
                            j_rsv_properties.set('application', i_application)
                            #
                            j_rsv_properties.set('extra.file', file_path)
                            j_rsv_properties.set('extra.user', utl_core.System.get_user_name())
                            j_rsv_properties.set('extra.time_tag', utl_core.System.get_time_tag())
                            #
                            j_rsv_properties.set('dcc.root', '/master')
                            j_rsv_properties.set('dcc.root_name', 'master')
                            j_rsv_properties.set('dcc.sub_root', '/master/hi')
                            #
                            j_rsv_properties.set('dcc.pathsep', rsv_configure.Application.get_pathsep(i_application))
                            return j_rsv_properties
    # ================================================================================================================ #
    def get_rsv_project(self):
        return self._rsv_project
    # tag
    def get_rsv_tag(self):
        return self.get_parent().get_parent().get_parent()
    # entity
    def get_rsv_entity(self):
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

    def get_rsv_versions(self):
        return self._rsv_project._project__get_rsv_task_versions_(
            **self.properties.value
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
            'user', utl_core.System.get_user_name()
        )
        return properties


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
        keyword = '{}-step-dir'.format(self.properties.get('branch'))
        rsv_unit = self.get_rsv_unit(keyword=keyword)
        return rsv_unit.get_result()

    def get_work_directory_path(self):
        keyword = '{}-work-step-dir'.format(self.properties.get('branch'))
        rsv_unit = self.get_rsv_unit(keyword=keyword)
        return rsv_unit.get_result()

    def get_rsv_tasks(self, **kwargs):
        kwargs.update(self._rsv_properties.value)
        return self._rsv_project._project__get_rsv_tasks_(
            **kwargs
        )

    def get_rsv_task(self, **kwargs):
        rsv_obj = self.rsv_project._project__get_rsv_task_(
            rsv_obj=self,
            **kwargs
        )
        return rsv_obj


class AbsRsvEntity(
    AbsRsvObj
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvEntity, self).__init__(*args, **kwargs)

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

    def get_rsv_steps(self):
        return self._rsv_project._project__get_rsv_steps_(
            **self._rsv_properties.value
        )

    def get_rsv_tasks(self, **kwargs):
        kwargs.update(self._rsv_properties.value)
        return self._rsv_project._project__get_rsv_tasks_(
            **kwargs
        )

    def get_rsv_unit(self, **kwargs):
        return self.rsv_project._project__get_rsv_unit_(
            rsv_obj=self,
            **kwargs
        )


class AbsRsvTag(
    AbsRsvObj
):
    def __init__(self, *args, **kwargs):
        super(AbsRsvTag, self).__init__(*args, **kwargs)

    def get_rsv_entity(self, **kwargs):
        """
        :param kwargs: asset: str(<asset-name>) / shot: str(<shot-name>)
        :return: instance(<rsv-entity>)
        """
        rsv_obj = self._rsv_project._project__get_rsv_entity_(
            rsv_obj=self,
            **kwargs
        )
        return rsv_obj

    def get_rsv_entities(self):
        return self._rsv_project._project__get_rsv_entities_(
            **self._rsv_properties.value
        )

    def get_rsv_steps(self):
        return self._rsv_project._project__get_rsv_steps_(
            **self._rsv_properties.value
        )

    def get_rsv_tasks(self, **kwargs):
        kwargs.update(self._rsv_properties.value)
        return self._rsv_project._project__get_rsv_tasks_(
            **kwargs
        )


# <rsv-project>
class AbsRsvProject(
    AbsRsvObjDef,
    AbsRsvDef,
    obj_abstract.AbsObjGuiDef,
    obj_abstract.AbsObjDagDef,
):
    RSV_MATCHER_CLASS = None
    #
    RSV_OBJ_STACK_CLASS = None
    #
    RSV_TAG_CLASS = None
    RSV_ENTITY_CLASS = None
    RSV_STEP_CLASS = None
    RSV_TASK_CLASS = None
    RSV_TASK_VERSION_CLASS = None
    #
    RSV_UNIT_CLASS = None
    RSV_UNIT_VERSION_CLASS = None

    PROPERTIES_CLASS = None
    def __init__(self, *args, **kwargs):
        self._set_obj_def_init_()
        self._set_rsv_def_init_()
        #
        resolver = args[0]
        #
        self._resolver = resolver
        self._rsv_obj_stack = self.RSV_OBJ_STACK_CLASS()
        #
        self._set_rsv_obj_def_init_(
            self.PROPERTIES_CLASS(self, bsc_core.DictMtd.set_key_sort_to(kwargs))
        )
        self._set_obj_dag_def_init_(self._rsv_path)
        self._set_obj_gui_def_init_()
        #
        self._root_dict = {}
        self._root_effect_dict = {}
        self._root_step_choice = None
        self._root_configure = bsc_objects.Configure(value=collections.OrderedDict())
        #
        self._rsv_matcher = self._set_rsv_matcher_create_(
            self._pattern,
            self._rsv_properties.value
        )
        #
        self._raw = copy.copy(self._resolver._raw)
        #
        file_path = rsv_configure.Data.get_project_configure_path(
            self.get(rsv_configure.Key.PROJECT)
        )
        if file_path:
            if os.path.exists(file_path) is False:
                file_path = rsv_configure.Data.get_project_configure_path(
                    project='default'
                )
        #
        self._raw.update(
            MtdBasic._get_scheme_raw_(os.path.abspath(file_path))
        )
        #
        self._configure = bsc_objects.Configure(value=self._raw)
        self._root_choices = self._configure.get('root-choices')
        self._root_step_choice = self._configure.get_content(
            'root-step-choice'
        )
        #
        self._includes_dict = collections.OrderedDict()
        self._patterns_dict = collections.OrderedDict()
        #
        self._set_root_dict_update_()
        self._set_includes_dict_update_(self._raw)
        # file-pattern(s) gain
        self._set_patterns_dict_update_(self._raw)
    @property
    def resolver(self):
        return self._resolver
    @property
    def pathsep(self):
        return '/'
    @property
    def path(self):
        return self._rsv_path
    @property
    def icon(self):
        return utl_core.Icon.get('file/folder')

    def get_workspace_src(self):
        return self.get_value('workspace-src')

    def _get_root_choice_(self, kwargs):
        root_choice = self._root_step_choice
        if root_choice:
            if 'workspace' in kwargs and 'step' in kwargs:
                root_choice = self._root_step_choice.get(
                    '{}.{}'.format(kwargs['workspace'], kwargs['step'])
                )
                if root_choice is not None:
                    return root_choice
        return 'root_primary'

    def __set_match_kwargs_completion_(self, kwargs):
        # workspace
        if 'workspace' in kwargs:
            workspace = kwargs['workspace']
            # convert other workspace to "work"
            if workspace not in [
                'work',
                'publish',
                # 'output'
            ]:
                kwargs['workspace'] = self.get_workspace_src()
        else:
            kwargs['workspace'] = self.get_workspace_src()
        # root_choice
        root_choice = self._get_root_choice_(kwargs)
        kwargs['root_choice'] = root_choice
        # root
        root_cur = self._rsv_properties.get(root_choice)
        kwargs['root'] = root_cur

    def get_workspace_release(self):
        return self.get_value('workspace-release')

    def get_workspace_pre_release(self):
        return self.get_value('workspace-pre-release')

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
        return self._resolver

    def get_directory_path(self):
        keyword = 'project-dir'
        rsv_pattern = self.RSV_PATTERN_CLASS(
            self.get_pattern(keyword)
        )
        return rsv_pattern.set_update(**self.properties.value)

    def _set_root_dict_update_(self):
        self._root_dict['windows'] = self._raw['project-root-windows-dir']
        self._root_dict['linux'] = self._raw['project-root-linux-dir']

        self._root_effect_dict['windows'] = self._raw['project-root_secondary-windows-dir']
        self._root_effect_dict['linux'] = self._raw['project-root_secondary-linux-dir']

        for i_root_choice in self._root_choices:
            for j_platform in ['windows', 'linux']:
                self._root_configure.set(
                    '{}.{}'.format(i_root_choice, j_platform),
                    self._raw['project-{}-{}-dir'.format(i_root_choice, j_platform)]
                )

    def _set_root_properties_update_(self, platform_):
        if platform_ == 'windows':
            self._rsv_properties.set('root', self._root_dict['windows'])
            self._rsv_properties.set('root_secondary', self._root_effect_dict['windows'])
        elif platform_ == 'linux':
            self._rsv_properties.set('root', self._root_dict['linux'])
            self._rsv_properties.set('root_secondary', self._root_effect_dict['linux'])

        for i_root_choice in self._root_choices:
            self._rsv_properties.set(
                i_root_choice,
                self._root_configure.get('{}.{}'.format(i_root_choice, platform_))
            )

    def _set_includes_dict_update_(self, raw):
        for k, v in raw.items():
            if isinstance(v, (tuple, list)):
                self._includes_dict[k] = [MtdBasic._get_rsv_pattern_real_value_(i, raw) for i in v]

    def _set_patterns_dict_update_(self, raw):
        for k, v in raw.items():
            if isinstance(v, (str, unicode)):
                pattern = MtdBasic._get_rsv_pattern_real_value_(v, raw)
                self._patterns_dict[k] = pattern

    def set_override_load(self, file_path):
        raw = MtdBasic._get_scheme_raw_(file_path)
        self._raw.update(raw)
        self._set_includes_dict_update_(raw)
        self._set_patterns_dict_update_(raw)

    def get_patterns(self, regex=None):
        if regex is not None:
            return [self.get_pattern(i) for i in self.get_keywords(regex)]
        return self._patterns_dict.values()

    def get_url(self, keyword, **kwargs):
        pattern = self.get_pattern(keyword)
        # find-order
        keys = MtdBasic._get_keys_by_parse_pattern_(pattern)
        main_keys = self.get_include(u'include-key-main')
        for key in keys:
            if key in main_keys and key not in kwargs:
                raise KeyError(u'keyword: "{}" is Non-assigned'.format(key))
        _ = u''.join([MtdBasic.URL_PARAMETERS_PATTERN.format(**dict(key=key, value=kwargs[key])) for key in keys if key in kwargs])
        return MtdBasic.URL_PATTERN.format(**dict(keyword=keyword, parameters=_))
    #
    def get_platform(self):
        return
    #
    def get_root(self):
        return
    @classmethod
    def _get_rsv_branch_(cls, **kwargs):
        if 'branch' in kwargs:
            return kwargs['branch']
        elif 'sequence' in kwargs:
            return 'shot'
        elif 'shot' in kwargs:
            return 'shot'
        elif 'role' in kwargs:
            return 'asset'
        elif 'asset' in kwargs:
            return 'asset'
        #
        elif 'keyword' in kwargs:
            keyword = kwargs['keyword']
            if fnmatch.filter([keyword], 'asset-*'):
                return 'asset'
            elif fnmatch.filter([keyword], 'shot-*'):
                return 'shot'
            else:
                raise TypeError()
        else:
            raise TypeError()
    @classmethod
    def _get_rsv_branch_0_(cls, **kwargs):
        if 'branch' in kwargs:
            return kwargs['branch']
        elif 'sequence' in kwargs:
            return 'shot'
        elif 'shot' in kwargs:
            return 'shot'
        elif 'role' in kwargs:
            return 'asset'
        elif 'asset' in kwargs:
            return 'asset'
    #
    def _project__set_rsv_matcher_create_(self, kwargs):
        self.__set_match_kwargs_completion_(kwargs)
        #
        pattern = kwargs['pattern']
        return self.RSV_MATCHER_CLASS(
            self,
            pattern,
            kwargs
        )

    def _set_rsv_matcher_create_(self, pattern, variants_override):
        return self.RSV_MATCHER_CLASS(
            self,
            pattern,
            variants_override
        )
    # tag
    def _project__get_rsv_tags_(self, **kwargs):
        lis = []
        #
        branch = kwargs['branch']
        if branch == 'asset':
            type_ = 'role'
        elif branch == 'shot':
            type_ = 'sequence'
        else:
            raise TypeError()
        #
        keyword = '{}-{}-dir'.format(branch, type_)
        kwargs['keyword'] = keyword
        kwargs['pattern'] = self.get_pattern(keyword=keyword)
        rsv_matcher = self._project__set_rsv_matcher_create_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        for i_match in matches:
            _, i_variants = i_match
            i_kwargs = copy.copy(kwargs)
            i_kwargs.update(i_variants)
            i_rsv_tag = self.get_rsv_tag(**i_kwargs)
            if i_rsv_tag is not None:
                if i_rsv_tag not in lis:
                    lis.append(i_rsv_tag)
        return lis

    def _project__get_rsv_tag_(self, rsv_obj, **kwargs):
        kwargs_ = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_[k] = v
        #
        kwargs_.update(kwargs)
        #
        branch = self._get_rsv_branch_(**kwargs_)
        if branch == 'asset':
            type_ = 'role'
        elif branch == 'shot':
            type_ = 'sequence'
        else:
            raise TypeError()
        #
        if type_ in kwargs_:
            name = kwargs_[type_]
        else:
            name = '*'
            # raise KeyError()
        #
        if MtdBasic._set_name_check_(type_, name) is False:
            return None
        # type
        kwargs_['type'] = type_
        keyword = '{}-{}-dir'.format(branch, type_)
        kwargs_['keyword'] = keyword
        # branch
        kwargs_['branch'] = branch
        # asset/shot
        kwargs_[type_] = name
        #
        obj_path = self._get_rsv_obj_path_(kwargs_)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        #
        variants = self._get_rsv_obj_create_kwargs_(
            obj_path,
            kwargs_,
            extend_keys=['type', 'branch']
        )
        return self._project__set_rsv_tag_create_(**variants)

    def _project__set_rsv_tag_create_(self, **kwargs):
        rsv_matcher = self._project__set_rsv_matcher_create_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            result, variants = matches[-1]
            self.__set_create_kwargs_completion_(kwargs, result, variants)
            rsv_obj = self.RSV_TAG_CLASS(self, **kwargs)
            self._project__set_rsv_obj_add_(rsv_obj)
            return rsv_obj

    def get_rsv_tags(self, **kwargs):
        branch = self._get_rsv_branch_0_(**kwargs)
        if branch is not None:
            kwargs['branch'] = branch
            return self._project__get_rsv_tags_(**kwargs)
        else:
            lis = []
            for branch in rsv_configure.Branch.ALL:
                kwargs['branch'] = branch
                lis.extend(
                    self._project__get_rsv_tags_(**kwargs)
                )
            return lis

    def get_rsv_tag(self, **kwargs):
        rsv_obj = self._project__get_rsv_tag_(
            rsv_obj=self, **kwargs
        )
        return rsv_obj
    # entity
    def _tag__get_rev_entity_(self, **kwargs):
        rsv_tag = self.get_rsv_tag(**kwargs)
        if rsv_tag:
            return rsv_tag.get_rsv_entity(**kwargs)

    def _project__get_rsv_entities_(self, **kwargs):
        lis = []
        branch = kwargs['branch']
        keyword = '{}-dir'.format(branch)
        kwargs['keyword'] = keyword
        kwargs['pattern'] = self.get_pattern(keyword=keyword)
        rsv_matcher = self._project__set_rsv_matcher_create_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        for i_match in matches:
            _, i_variants = i_match
            i_kwargs = copy.copy(kwargs)
            i_kwargs.update(i_variants)
            rsv_entity = self._tag__get_rev_entity_(**i_kwargs)
            if rsv_entity is not None:
                if rsv_entity not in lis:
                    lis.append(rsv_entity)
        return lis
    #
    def _project__get_rsv_entity_(self, rsv_obj, **kwargs):
        kwargs_ = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_[k] = v
        #
        kwargs_.update(kwargs)
        #
        branch = self._get_rsv_branch_(**kwargs_)
        type_ = branch
        if type_ in kwargs_:
            name = kwargs_[type_]
        else:
            raise KeyError()
        #
        if MtdBasic._set_name_check_(type_, name) is False:
            return None
        # type
        kwargs_['type'] = type_
        keyword = '{}-dir'.format(type_)
        kwargs_['keyword'] = keyword
        # branch
        kwargs_['branch'] = branch
        # asset/shot
        kwargs_[type_] = name
        #
        obj_path = self._get_rsv_obj_path_(kwargs_)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        variants = self._get_rsv_obj_create_kwargs_(
            obj_path,
            kwargs_,
            extend_keys=['type', 'branch']
        )
        return self._project__set_rsv_entity_create_(**variants)
    #
    def _project__set_rsv_entity_create_(self, **kwargs):
        rsv_matcher = self._project__set_rsv_matcher_create_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            result, variants = matches[-1]
            self.__set_create_kwargs_completion_(kwargs, result, variants)
            rsv_obj = self.RSV_ENTITY_CLASS(self, **kwargs)
            self._project__set_rsv_obj_add_(rsv_obj)
            return rsv_obj
    #
    def get_rsv_entities(self, **kwargs):
        branch = self._get_rsv_branch_0_(**kwargs)
        if branch is not None:
            kwargs['branch'] = branch
            return self._project__get_rsv_entities_(**kwargs)
        else:
            lis = []
            for branch in rsv_configure.Branch.ALL:
                kwargs['branch'] = branch
                lis.extend(
                    self._project__get_rsv_entities_(**kwargs)
                )
            return lis
    #
    def get_rsv_entity(self, **kwargs):
        if 'role' in kwargs or 'sequence' in kwargs:
            return self._tag__get_rev_entity_(**kwargs)
        else:
            _ = self.get_rsv_entities(**kwargs)
            if _:
                return _[-1]
    # step
    def _entity__get_rsv_step_(self, **kwargs):
        rsv_entity = self.get_rsv_entity(**kwargs)
        if rsv_entity is not None:
            return rsv_entity.get_rsv_step(**kwargs)

    def _project__get_rsv_steps_(self, **kwargs):
        lis = []
        branch = kwargs['branch']
        keyword = '{}-step-dir'.format(branch)
        kwargs['keyword'] = keyword
        kwargs['pattern'] = self.get_pattern(keyword=keyword)
        rsv_matcher = self._project__set_rsv_matcher_create_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        for i_match in matches:
            _, i_variants = i_match
            i_kwargs = copy.copy(kwargs)
            i_kwargs.update(i_variants)
            rsv_step = self._entity__get_rsv_step_(**i_kwargs)
            if rsv_step is not None:
                if rsv_step not in lis:
                    lis.append(rsv_step)
        return lis
    #
    def _project__get_rsv_step_(self, rsv_obj, **kwargs):
        kwargs_ = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_[k] = v
        #
        kwargs_.update(kwargs)
        #
        type_ = 'step'
        branch = self._get_rsv_branch_(**kwargs_)
        keyword = '{}-{}-dir'.format(branch, type_)
        #
        if type_ in kwargs_:
            name = kwargs_[type_]
            step_include_names = self.get_include(u'include-{}-{}'.format(branch, type_)) or []
            if step_include_names:
                if name not in step_include_names:
                    return
        else:
            raise KeyError()
        #
        kwargs_['type'] = type_
        kwargs_['keyword'] = keyword
        kwargs_[type_] = name
        #
        obj_path = self._get_rsv_obj_path_(kwargs_)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        variants = self._get_rsv_obj_create_kwargs_(
            obj_path,
            kwargs_,
            extend_keys=['type', 'branch']
        )
        return self._project__set_rsv_step_create_(**variants)
    #
    def _project__set_rsv_step_create_(self, **kwargs):
        rsv_matcher = self._project__set_rsv_matcher_create_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            result, variants = matches[-1]
            self.__set_create_kwargs_completion_(kwargs, result, variants)
            rsv_obj = self.RSV_STEP_CLASS(self, **kwargs)
            self._project__set_rsv_obj_add_(rsv_obj)
            return rsv_obj
    #
    def get_rsv_steps(self, **kwargs):
        branch = self._get_rsv_branch_0_(**kwargs)
        if branch is not None:
            kwargs['branch'] = branch
            return self._project__get_rsv_steps_(**kwargs)
        else:
            lis = []
            for branch in rsv_configure.Branch.ALL:
                kwargs['branch'] = branch
                lis.extend(
                    self._project__get_rsv_steps_(**kwargs)
                )
            return lis
    #
    def get_rsv_step(self, **kwargs):
        if 'asset' in kwargs or 'shot' in kwargs:
            return self._entity__get_rsv_step_(**kwargs)
        _ = self.get_rsv_steps(**kwargs)
        if _:
            return _[-1]
    # task
    def _step__get_rsv_task_(self, **kwargs):
        rsv_step = self.get_rsv_step(**kwargs)
        if rsv_step is not None:
            return rsv_step.get_rsv_task(**kwargs)

    def _project__get_rsv_tasks_(self, **kwargs):
        lis = []
        #
        branch = kwargs['branch']
        keyword = '{}-task-dir'.format(branch)
        kwargs['keyword'] = keyword
        kwargs['pattern'] = self.get_pattern(keyword=keyword)
        rsv_matcher = self._project__set_rsv_matcher_create_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        for i_match in matches:
            _, i_variants = i_match
            i_kwargs = copy.copy(kwargs)
            i_kwargs.update(i_variants)
            rsv_task = self._step__get_rsv_task_(**i_kwargs)
            if rsv_task is not None:
                if rsv_task not in lis:
                    lis.append(rsv_task)
        return lis

    def _project__get_rsv_task_(self, rsv_obj, **kwargs):
        kwargs_ = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_[k] = v
        #
        kwargs_.update(kwargs)
        #
        type_ = 'task'
        branch = self._get_rsv_branch_(**kwargs_)
        keyword = '{}-{}-dir'.format(branch, type_)
        #
        if type_ in kwargs_:
            name = kwargs_[type_]
        else:
            raise KeyError()
        #
        if MtdBasic._set_name_check_(type_, name) is False:
            return None
        #
        kwargs_['type'] = type_
        kwargs_['keyword'] = keyword
        kwargs_[type_] = name
        #
        obj_path = self._get_rsv_obj_path_(kwargs_)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        variants = self._get_rsv_obj_create_kwargs_(
            obj_path,
            kwargs_,
            extend_keys=['type', 'branch']
        )
        return self._project__set_rsv_task_create_(**variants)
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
        branch = self._get_rsv_branch_0_(**kwargs)
        if branch is not None:
            kwargs['branch'] = branch
            return self._project__get_rsv_tasks_(**kwargs)
        else:
            lis = []
            for branch in rsv_configure.Branch.ALL:
                kwargs['branch'] = branch
                lis.extend(
                    self._project__get_rsv_tasks_(**kwargs)
                )
            return lis
    #
    def _project__set_rsv_task_create_(self, **kwargs):
        rsv_matcher = self._project__set_rsv_matcher_create_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            result, variants = matches[-1]
            self.__set_create_kwargs_completion_(kwargs, result, variants)
            rsv_obj = self.RSV_TASK_CLASS(self, **kwargs)
            self._project__set_rsv_obj_add_(rsv_obj)
            return rsv_obj
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
        branch = self._get_rsv_branch_0_(**kwargs)
        if branch is not None:
            kwargs['branch'] = branch
            return self._project__get_rsv_task_versions_(**kwargs)
        else:
            lis = []
            for branch in rsv_configure.Branch.ALL:
                kwargs['branch'] = branch
                lis.extend(
                    self._project__get_rsv_task_versions_(**kwargs)
                )
            return lis

    def _task__get_rsv_version_(self, **kwargs):
        rsv_task = self.get_rsv_task(**kwargs)
        if rsv_task is not None:
            return rsv_task.get_rsv_version(**kwargs)

    def _project__get_rsv_task_versions_(self, **kwargs):
        lis = []
        #
        branch = kwargs['branch']
        keyword = '{}-version-dir'.format(branch)
        kwargs['keyword'] = keyword
        kwargs['pattern'] = self.get_pattern(keyword=keyword)
        rsv_matcher = self._project__set_rsv_matcher_create_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        for i_match in matches:
            _, i_variants = i_match
            i_kwargs = copy.copy(kwargs)
            i_kwargs.update(i_variants)
            #
            rsv_version = self._task__get_rsv_version_(**i_kwargs)
            if rsv_version is not None:
                if rsv_version not in lis:
                    lis.append(rsv_version)
        return lis

    def _project__get_rsv_task_version_(self, rsv_obj, **kwargs):
        kwargs_ = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_[k] = v
        #
        kwargs_.update(kwargs)
        #
        type_ = 'version'
        branch = self._get_rsv_branch_(**kwargs_)
        keyword = '{}-{}-dir'.format(branch, type_)
        #
        if type_ in kwargs_:
            name = kwargs_[type_]
        else:
            raise KeyError()
        #
        if MtdBasic._set_name_check_(type_, name) is False:
            return None
        #
        kwargs_['type'] = type_
        kwargs_['keyword'] = keyword
        kwargs_[type_] = name
        version = kwargs_['version']
        #
        obj_path = self._get_rsv_obj_path_(kwargs_)
        obj_path = '{}/{}'.format(obj_path, version)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        #
        variants = self._get_rsv_obj_create_kwargs_(
            obj_path,
            kwargs_,
            extend_keys=['type', 'branch']
        )
        return self._project__set_rsv_task_version_create_(**variants)

    def _project__set_rsv_task_version_create_(self, **kwargs):
        rsv_matcher = self._project__set_rsv_matcher_create_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            result, variants = matches[-1]
            self.__set_create_kwargs_completion_(kwargs, result, variants)
            rsv_obj = self.RSV_TASK_VERSION_CLASS(self, **kwargs)
            self._project__set_rsv_obj_add_(rsv_obj)
            return rsv_obj
    # unit
    def get_rsv_unit(self, **kwargs):
        rsv_task = self.get_rsv_task(**kwargs)
        if rsv_task is not None:
            return rsv_task.get_rsv_unit(**kwargs)

    def _project__get_rsv_unit_(self, rsv_obj, **kwargs):
        kwargs_ = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_[k] = v
        #
        kwargs_.update(kwargs)
        #
        type_ = 'unit'
        kwargs_['type'] = type_
        # keyword = kwargs_['keyword']
        keyword = self.__set_keyword_completion_(kwargs_)
        if 'platform' not in kwargs_:
            kwargs_['platform'] = bsc_core.SystemMtd.get_platform()
        #
        if 'version' not in kwargs_:
            kwargs_['version'] = rsv_configure.Version.LATEST
        #
        obj_path = self._get_rsv_obj_path_(kwargs_)
        obj_path = '{}/{}'.format(obj_path, keyword)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        variants = self._get_rsv_obj_create_kwargs_(
            obj_path,
            kwargs_,
            extend_keys=['type', 'branch', 'platform', 'application', 'keyword']
        )
        return self._project__set_rsv_unit_create_(**variants)
    @staticmethod
    def __set_keyword_completion_(kwargs):
        """
        etc: keyword = '{branch}-component-usd-file'
        :param kwargs:
        :return:
        """
        keyword = kwargs.pop('keyword')
        # noinspection PyStatementEffect
        keyword = keyword.format(**kwargs)
        kwargs['keyword'] = keyword
        return keyword

    def _project__set_rsv_unit_create_(self, **kwargs):
        rsv_obj = self.RSV_UNIT_CLASS(self, **kwargs)
        self._project__set_rsv_obj_add_(rsv_obj)
        return rsv_obj

    def _project__get_rsv_unit_version_(self, rsv_obj, **kwargs):
        kwargs_ = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_[k] = v
        #
        kwargs_.update(kwargs)
        #
        type_ = 'version'
        keyword = rsv_obj.get('keyword')
        #
        if type_ in kwargs_:
            name = kwargs_[type_]
        else:
            raise KeyError()
        #
        if MtdBasic._set_name_check_(type_, name) is False:
            return None
        #
        kwargs_['type'] = type_
        kwargs_['keyword'] = keyword
        kwargs_[type_] = name
        version = kwargs_['version']
        #
        obj_path = self._get_rsv_obj_path_(kwargs_)
        obj_path = '{}/{}/{}'.format(obj_path, keyword, version)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        variants = self._get_rsv_obj_create_kwargs_(
            obj_path,
            kwargs_,
            extend_keys=['type', 'branch']
        )
        return self._project__set_rsv_unit_version_create_(**variants)

    def _project__set_rsv_unit_version_create_(self, **kwargs):
        rsv_matcher = self._project__set_rsv_matcher_create_(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            result, variants = matches[-1]
            self.__set_create_kwargs_completion_(kwargs, result, variants)
            rsv_obj = self.RSV_UNIT_VERSION_CLASS(self, **kwargs)
            self._project__set_rsv_obj_add_(rsv_obj)
            return rsv_obj
    @staticmethod
    def __set_create_kwargs_completion_(kwargs, result, variants):
        update = bsc_core.TimeMtd.to_prettify_by_timestamp(
            bsc_core.StorageFileOpt(
                result
            ).get_modify_timestamp(),
            language=1
        )
        user = bsc_core.StoragePathOpt(
            result
        ).get_user()
        kwargs['result'] = result
        kwargs['update'] = update
        kwargs['user'] = user
        kwargs.update(variants)

    def _unit__get_rsv_version_(self, **kwargs):
        rsv_task = self.get_rsv_task(**kwargs)
        if rsv_task is not None:
            return rsv_task.get_rsv_version(**kwargs)

    def _get_rsv_obj_exists_(self, rsv_obj_path):
        return self._rsv_obj_stack.get_object_exists(rsv_obj_path)

    def _project__set_rsv_obj_add_(self, rsv_obj):
        self._rsv_obj_stack.set_object_add(rsv_obj)
        utl_core.Log.set_module_result_trace(
            'resolver',
            u'{}="{}"'.format(rsv_obj.type, rsv_obj.path)
        )

    def _project__get_rsv_obj_(self, path):
        if path == '/':
            return self._resolver
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
            for i_branch in rsv_configure.Branch.ALL:
                i_pattern = self.get_pattern(keyword='{}-dir'.format(i_branch))
                i_pattern_ = '{}/{{extra}}'.format(i_pattern)

                i_rsv_matcher = self._set_rsv_matcher_create_(
                    i_pattern_, variants_override
                )
                i_properties = i_rsv_matcher.get_properties_by_result(result=file_path)
                if i_properties:
                    i_properties.set('branch', i_branch)
                    # i_properties.set('workspace', 'work')
                    i_rsv_entity = self.get_rsv_entity(**i_properties.value)
                    return i_rsv_entity
    # rsv-step
    def get_rsv_step_work_file_path(self, file_path):
        return self._project__get_rsv_step_by_file_path_(
            file_path,
            variants_override=dict(workspace='work')
        )

    def get_rsv_step_file_path(self, file_path):
        return self._project__get_rsv_step_by_file_path_(
            file_path,
            variants_override=dict(workspace='publish')
        )

    def _project__get_rsv_step_by_file_path_(self, file_path, variants_override):
        if file_path is not None:
            for i_branch in rsv_configure.Branch.ALL:
                i_pattern = self.get_pattern(keyword='{}-step-dir'.format(i_branch))
                i_pattern_ = '{}/{{extra}}'.format(i_pattern)
                i_rsv_matcher = self._set_rsv_matcher_create_(
                    i_pattern_, variants_override
                )
                i_properties = i_rsv_matcher.get_properties_by_result(result=file_path)
                if i_properties:
                    i_properties.set('branch', i_branch)
                    # i_properties.set('workspace', 'work')
                    i_rsv_step = self.get_rsv_step(**i_properties.value)
                    return i_rsv_step
    # scene
    def _project__get_rsv_task_by_file_path_(self, file_path, variants_override):
        if file_path is not None:
            for i_branch in rsv_configure.Branch.ALL:
                i_pattern = self.get_pattern(keyword='{}-task-dir'.format(i_branch))
                i_pattern_ = '{}/{{extra}}'.format(i_pattern)
                i_rsv_matcher = self._set_rsv_matcher_create_(
                    i_pattern_, variants_override
                )
                i_properties = i_rsv_matcher.get_properties_by_result(result=file_path)
                if i_properties:
                    i_properties.set('branch', i_branch)
                    i_rsv_task = self.get_rsv_task(**i_properties.value)
                    i_rsv_task.set('workspace', variants_override['workspace'])
                    return i_rsv_task

    def _project__get_rsv_version_by_file_path_(self, file_path, variants_override):
        rsv_task = self._project__get_rsv_task_by_file_path_(file_path, variants_override)
        if rsv_task is not None:
            pass
    # work
    def get_rsv_task_by_work_file_path(self, file_path):
        return self._project__get_rsv_task_by_file_path_(
            file_path,
            variants_override=dict(workspace='work')
        )
    # publish
    def get_rsv_task_by_file_path(self, file_path):
        return self._project__get_rsv_task_by_file_path_(
            file_path,
            variants_override=dict(workspace='publish')
        )
    # output
    def get_rsv_task_by_output_file_path(self, file_path):
        return self._project__get_rsv_task_by_file_path_(
            file_path,
            variants_override=dict(workspace='output')
        )

    def get_rsv_task_by_any_file_path(self, file_path):
        for i_workspace in ['work', 'publish', 'output']:
            rsv_task = self._project__get_rsv_task_by_file_path_(
                file_path,
                variants_override=dict(workspace=i_workspace)
            )
            if rsv_task is not None:
                return rsv_task
        return None

    def get_rsv_version_by_any_file_path(self, file_path):
        for i_workspace in ['work', 'publish']:
            rsv_version = self._project__get_rsv_version_by_file_path_(
                file_path,
                variants_override=dict(workspace=i_workspace)
            )
            if rsv_version is not None:
                return rsv_version
        return None

    def get_folders(self):
        pass

    def get_rsv_obj_by_path(self, rsv_obj_type_name, rsv_obj_path):
        keyword_dict = {
            'project': 'project-dir'
        }

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
    AbsRsvDef,
    obj_abstract.AbsObjGuiDef,
    obj_abstract.AbsObjDagDef,
):
    FILE_PATH = None
    #
    OBJ_UNIVERSE_CLASS = None
    #
    RSV_PROJECT_STACK_CLASS = None
    RSV_PROJECT_CLASS = None
    def __init__(self):
        self._set_rsv_def_init_()
        self._set_obj_dag_def_init_('/')
        self._set_obj_gui_def_init_()
        #
        self._rsv_project_stack = self.RSV_PROJECT_STACK_CLASS()
        self._obj_universe = self.OBJ_UNIVERSE_CLASS()
        #
        self._raw = MtdBasic._get_scheme_raw_(os.path.abspath(self.FILE_PATH))
        #
        self._patterns_dict = collections.OrderedDict()
        self._includes_dict = collections.OrderedDict()
        #
        self._set_includes_dict_update_(self._raw)
        self._set_patterns_dict_update_(self._raw)
        #
        pattern = rsv_configure.Data.get_project_configure_path('{project}')
        results = MtdBasic._get_stg_paths_by_parse_pattern_(pattern)
        if results:
            for result in results:
                p = parse.parse(
                    pattern, result
                )
                if p:
                    project = p['project']
                    if not project == 'basic':
                        self.get_rsv_project(project=project)
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
        return utl_core.Icon.get('file/root')

    def _set_dag_create_(self, path):
        if path == self.path:
            return self

    def _get_child_paths_(self, *args, **kwargs):
        return self._rsv_project_stack.get_keys()

    def _set_child_create_(self, path):
        return self._rsv_project_stack.get_object(path)
    @property
    def include_dict(self):
        return self._includes_dict
    @property
    def pattern_dict(self):
        return self._patterns_dict

    def _set_includes_dict_update_(self, raw):
        for k, v in raw.items():
            if isinstance(v, (tuple, list)):
                self._includes_dict[k] = [MtdBasic._get_rsv_pattern_real_value_(i, raw) for i in v]

    def _set_patterns_dict_update_(self, raw):
        for k, v in raw.items():
            if isinstance(v, (str, unicode)):
                pattern = MtdBasic._get_rsv_pattern_real_value_(v, raw)
                self._patterns_dict[k] = pattern
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

    def get_rsv_project(self, **kwargs):
        return self._get_rsv_project_(self, **kwargs)

    def get_rsv_project_is_exists(self, **kwargs):
        return

    def _get_rsv_project_(self, rsv_obj, **kwargs):
        kwargs_ = collections.OrderedDict()
        kwargs_.update(kwargs)
        type_ = 'project'
        if type_ in kwargs_:
            name = kwargs_[type_]
        else:
            raise KeyError()
        #
        kwargs_['type'] = type_
        kwargs_[type_] = name
        keyword = '{}-dir'.format(type_)
        kwargs_['keyword'] = keyword
        #
        obj_path = self._get_rsv_obj_path_(kwargs_)
        if self._rsv_project_stack.get_object_exists(obj_path) is True:
            rsv_project = self._rsv_project_stack.get_object(obj_path)
            if 'platform' in kwargs_:
                rsv_project._set_root_properties_update_(kwargs_['platform'])
            else:
                platform_ = self.get_platform()
                rsv_project._set_root_properties_update_(platform_)
            return rsv_project
        #
        variants = self._get_rsv_obj_create_kwargs_(
            obj_path,
            kwargs_,
            extend_keys=['type']
        )
        return self._root__set_rsv_project_create_(**variants)

    def _root__set_rsv_project_create_(self, **kwargs):
        rsv_obj = self.RSV_PROJECT_CLASS(self, **kwargs)
        rsv_obj._set_root_properties_update_(platform_=self.get_platform())
        obj_type = rsv_obj.type
        obj_path = rsv_obj.path
        self._rsv_project_stack.set_object_add(rsv_obj)
        utl_core.Log.set_module_result_trace(
            'resolver',
            u'{}="{}"'.format(obj_type, obj_path)
        )
        return rsv_obj
    # scene
    def get_rsv_project_by_file_path(self, file_path):
        return self._resolver__get_rsv_project_by_file_path_(file_path)

    def _resolver__get_rsv_project_by_file_path_(self, file_path):
        rsv_projects = self.get_rsv_projects()
        for i_rsv_project in rsv_projects:
            for j_platform in rsv_configure.Platform.ALL:
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
                    j_rsv_matcher = i_rsv_project._set_rsv_matcher_create_(
                        j_pattern_, j_variants
                    )
                    j_project_rsv_properties = j_rsv_matcher.get_properties_by_result(file_path)
                    if j_project_rsv_properties:
                        i_rsv_project.properties.set('platform', j_platform)
                        i_rsv_project.properties.set('root', j_root)
                        return i_rsv_project
        #
        return self._resolver__get_rsv_project_use_default_(file_path)
    # = rsv_project.get_rsv_entities
    def get_rsv_entities(self, **kwargs):
        kwargs_ = self._get_rsv_kwargs_(**kwargs)
        if kwargs_:
            rsv_project = self.get_rsv_project(**kwargs_)
            if rsv_project:
                return rsv_project.get_rsv_entities(**kwargs_)
    # = rsv_project.get_rsv_entity
    def get_rsv_entity(self, **kwargs):
        kwargs_ = self._get_rsv_kwargs_(**kwargs)
        if kwargs_:
            rsv_project = self.get_rsv_project(**kwargs_)
            if rsv_project:
                return rsv_project.get_rsv_entity(**kwargs_)
    #
    def get_rsv_step(self, **kwargs):
        kwargs_ = self._get_rsv_kwargs_(**kwargs)
        if kwargs_:
            rsv_project = self.get_rsv_project(**kwargs_)
            if rsv_project:
                return rsv_project.get_rsv_step(**kwargs_)
    # = rsv_project.get_rsv_task
    def get_rsv_task(self, **kwargs):
        kwargs_ = self._get_rsv_kwargs_(**kwargs)
        if kwargs_:
            rsv_project = self.get_rsv_project(**kwargs_)
            if rsv_project:
                return rsv_project.get_rsv_task(**kwargs_)

    def get_rsv_tasks(self, **kwargs):
        kwargs_ = self._get_rsv_kwargs_(**kwargs)
        if kwargs_:
            rsv_project = self.get_rsv_project(**kwargs_)
            if rsv_project:
                return rsv_project.get_rsv_tasks(**kwargs_)

    def get_rsv_task_by_file_path(self, file_path):
        rsv_project = self.get_rsv_project_by_file_path(file_path)
        if rsv_project is not None:
            return rsv_project.get_rsv_task_by_file_path(
                file_path
            )
        else:
            utl_core.Log.set_module_warning_trace(
                'project-resolver',
                u'file="{}" is not available'.format(file_path)
            )
        return None

    def get_rsv_task_by_work_file_path(self, file_path):
        rsv_project = self.get_rsv_project_by_file_path(file_path)
        if rsv_project is not None:
            return rsv_project.get_rsv_task_by_work_file_path(
                file_path
            )
        else:
            utl_core.Log.set_module_warning_trace(
                'project-resolver',
                u'file="{}" is not available'.format(file_path)
            )
        return None

    def get_rsv_task_by_any_file_path(self, file_path):
        rsv_project = self.get_rsv_project_by_file_path(file_path)
        if rsv_project is not None:
            return rsv_project.get_rsv_task_by_any_file_path(
                file_path
            )
        else:
            utl_core.Log.set_module_warning_trace(
                'project-resolver',
                u'file="{}" is not available'.format(file_path)
            )
        return None

    def get_rsv_task_version(self, **kwargs):
        kwargs_ = self._get_rsv_kwargs_(**kwargs)
        if kwargs_:
            rsv_project = self.get_rsv_project(**kwargs_)
            if rsv_project:
                return rsv_project.get_rsv_task_version(**kwargs_)
    # = rsv_project.get_rsv_unit
    def get_rsv_unit(self, **kwargs):
        kwargs_ = self._get_rsv_kwargs_(**kwargs)
        if kwargs_:
            rsv_project = self.get_rsv_project(**kwargs_)
            if rsv_project:
                return rsv_project.get_rsv_unit(**kwargs_)
    #
    def _resolver__get_rsv_project_use_default_(self, file_path):
        rsv_project = self.get_rsv_project(project='default')
        for i_platform in rsv_configure.Platform.ALL:
            i_root = rsv_project.get_pattern('project-root-{}-dir'.format(i_platform))
            i_glob_pattern = '{}/*'.format(i_root)
            i_results = fnmatch.filter([file_path.lower()], i_glob_pattern)
            if i_results:
                j_variants = {'root': i_root}
                i_pattern = rsv_project.get_pattern('project-dir')
                i_pattern_ = '{}/{{extra}}'.format(i_pattern)
                i_rsv_matcher = rsv_project._set_rsv_matcher_create_(
                    i_pattern_, j_variants
                )
                i_project_properties = i_rsv_matcher._get_project_properties_by_default_(file_path)
                i_project = i_project_properties.get('project')
                utl_core.Log.set_module_result_trace(
                    'resolver project create',
                    'project-name="{}", create use "default"'.format(i_project)
                )
                return self.get_rsv_project(project=i_project)
    # rsv-project
    def get_rsv_project_by_work_scene_src_file_path(self, file_path):
        return self._resolver__get_rsv_project_by_file_path_(file_path)

    def get_rsv_project_by_scene_src_file_path(self, file_path):
        return self._resolver__get_rsv_project_by_file_path_(file_path)
    # rsv-step
    def get_rsv_step_by_work_scene_src_file_path(self, file_path):
        rsv_project = self.get_rsv_project_by_work_scene_src_file_path(file_path)
        if rsv_project is not None:
            return rsv_project.get_rsv_step_work_file_path(file_path)
        else:
            utl_core.Log.set_module_warning_trace(
                'project-resolver',
                u'file="{}" is not available'.format(file_path)
            )
        return None

    def get_rsv_step_by_scene_src_file_path(self, file_path):
        rsv_project = self.get_rsv_project_by_scene_src_file_path(file_path)
        if rsv_project is not None:
            return rsv_project.get_rsv_step_file_path(file_path)
        else:
            utl_core.Log.set_module_warning_trace(
                'project-resolver',
                u'file="{}" is not available'.format(file_path)
            )
        return None
    # rsv-task
    def get_rsv_task_by_work_scene_src_file_path(self, file_path):
        rsv_project = self.get_rsv_project_by_work_scene_src_file_path(file_path)
        if rsv_project is not None:
            return rsv_project.get_rsv_task_by_work_file_path(file_path)
        else:
            utl_core.Log.set_module_warning_trace(
                'project-resolver',
                u'file="{}" is not available'.format(file_path)
            )
        return None

    def get_rsv_task_by_scene_src_file_path(self, file_path):
        rsv_project = self.get_rsv_project_by_scene_src_file_path(file_path)
        if rsv_project is not None:
            return rsv_project.get_rsv_task_by_file_path(file_path)
        else:
            utl_core.Log.set_module_warning_trace(
                'project-resolver',
                u'file="{}" is not available'.format(file_path)
            )
        return None

    def get_task_properties_by_work_scene_src_file_path(self, file_path):
        _ = self._get_rsv_task_properties_by_work_scene_src_file_path_(file_path)
        if _ is not None:
            return _
        else:
            utl_core.Log.set_module_warning_trace(
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
            utl_core.Log.set_module_warning_trace(
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
    def get_task_properties_by_source_file_path(self, file_path):
        return self.get_task_properties_by_scene_src_file_path(file_path)
    #
    def get_rsv_task_by_scene_file_path(self, file_path):
        rsv_project = self.get_rsv_project_by_file_path(file_path)
        if rsv_project is not None:
            return rsv_project.get_rsv_task_by_file_path(file_path)
        else:
            utl_core.Log.set_module_warning_trace(
                'project-resolver',
                u'file="{}" is not available'.format(file_path)
            )
        return None
    #
    def get_task_properties_by_scene_file_path(self, file_path):
        _ = self._get_rsv_task_properties_by_scene_file_path_(file_path)
        if _ is not None:
            return _
        else:
            utl_core.Log.set_module_warning_trace(
                'scene-file-resolver',
                u'file="{}" is not available'.format(file_path)
            )
        return None
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
    def _get_task_properties_by_work_user_scene_src_file_path_(self, file_path):
        rsv_task = self.get_rsv_task_by_work_scene_src_file_path(file_path)
        if rsv_task is not None:
            return rsv_task.get_properties_by_work_scene_src_file_path(file_path)
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
            result = method(bsc_core.StoragePathOpt(file_path).get_path())
            if result is not None:
                # print(';'.join(['{}={}'.format(k, v) for k, v in result.value.items() if isinstance(v, (str, unicode))]))
                return result
    @classmethod
    def get_path_args(cls):
        dic = collections.OrderedDict()
        # dic['root'] = ''
        return dic
    #
    def get_rsv_entity_step_directory_paths(self, **kwargs):
        lis = []
        if 'role' in kwargs:
            branch = 'asset'
        elif 'sequence' in kwargs:
            branch = 'shot'
        else:
            raise TypeError()
        #
        project = kwargs['project']
        rsv_project = self.get_rsv_project(project=project)
        keywords = [
            '{}-step-dir'.format(branch),
            '{}-work-step-dir'.format(branch),
            '{}-output-step-dir'.format(branch),
        ]
        #
        for i_keyword in keywords:
            i_kwargs = rsv_project.properties.copy_value
            i_kwargs.update(kwargs)
            rsv_pattern = rsv_project.get_rsv_pattern(i_keyword)
            workspace = MtdBasic._get_rsv_workspace_(keyword=i_keyword)
            i_kwargs['workspace'] = workspace
            result = rsv_pattern.set_update(**i_kwargs)
            lis.append(result)
        return lis

    def get_rsv_entity_task_directory_paths(self, **kwargs):
        lis = []
        if 'role' in kwargs:
            branch = 'asset'
        elif 'sequence' in kwargs:
            branch = 'shot'
        else:
            raise TypeError()
        #
        project = kwargs['project']
        rsv_project = self.get_rsv_project(project=project)
        keywords = [
            '{}-task-dir'.format(branch),
            '{}-work-task-dir'.format(branch),
            '{}-output-task-dir'.format(branch),
        ]
        #
        for i_keyword in keywords:
            i_kwargs = rsv_project.properties.copy_value
            i_kwargs.update(kwargs)
            rsv_pattern = rsv_project.get_rsv_pattern(i_keyword)
            workspace = MtdBasic._get_rsv_workspace_(keyword=i_keyword)
            i_kwargs['workspace'] = workspace
            result = rsv_pattern.set_update(**i_kwargs)
            lis.append(result)
        return lis

    def get_rsv_scene_properties_by_any_scene_file_path(self, file_path):
        rsv_task = self.get_rsv_task_by_any_file_path(file_path)
        if rsv_task is not None:
            return rsv_task.get_rsv_scene_properties_by_any_scene_file_path(file_path)

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type,
            self.path
        )

    def __repr__(self):
        return self.__str__()
