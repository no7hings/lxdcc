# coding:utf-8
from __future__ import print_function

import six

import os

import re

import glob

import platform

import fnmatch

import parse

import collections

import copy

import json

import yaml


def yaml_ordered_load(stream, Loader=yaml.SafeLoader, object_pairs_hook=collections.OrderedDict):
    class _Cls(Loader):
        pass
    # noinspection PyArgumentList
    def _fnc(loader_, node_):
        loader_.flatten_mapping(node_)
        return object_pairs_hook(loader_.construct_pairs(node_))
    # noinspection PyUnresolvedReferences
    _Cls.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _fnc)
    return yaml.load(stream, _Cls)


def yaml_ordered_dump(data, stream=None, Dumper=yaml.SafeDumper, object_pairs_hook=collections.OrderedDict, **kwargs):
    class _Cls(Dumper):
        pass
    # noinspection PyUnresolvedReferences
    def _fnc(dumper_, data_):
        return dumper_.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data_.items())

    _Cls.add_representer(object_pairs_hook, _fnc)
    return yaml.dump(data, stream, _Cls, **kwargs)


class MtdBasic(object):
    REF_RE_PATTERN = r'[<](.*?)[>]'
    KEY_RE_PATTERN = r'[{](.*?)[}]'
    @classmethod
    def _get_keys_by_parse_pattern_(cls, pattern):
        lis_0 = re.findall(re.compile(cls.KEY_RE_PATTERN, re.S), pattern)
        lis_1 = list(set(lis_0))
        lis_1.sort(key=lis_0.index)
        return lis_1
    @classmethod
    def _set_pattern_update_(cls, pattern, format_variant):
        if pattern is not None:
            keys = cls._get_keys_by_parse_pattern_(pattern)
            s = pattern
            if keys:
                for key in keys:
                    if key in format_variant:
                        v = format_variant[key]
                        if v is not None:
                            s = s.replace('{{{}}}'.format(key), format_variant[key])
            return s
        return pattern
    @classmethod
    def _get_scheme_raw_(cls, file_path):
        if os.path.exists(file_path):
            ext = os.path.splitext(file_path)[-1]
            if ext in ['.json']:
                with open(file_path) as j:
                    return json.load(j, object_pairs_hook=collections.OrderedDict)
            elif ext in ['.yml']:
                with open(file_path) as y:
                    return yaml_ordered_load(y)
            else:
                raise TypeError(
                    'file-ext: "{}" is Non-available'.format(ext)
                )
        else:
            raise TypeError(
                u'file="{}" is Non-exists'.format(file_path)
            )
    @classmethod
    def _get_match_patterns_(cls, variant, dic):
        def _rcs_fnc(v_):
            if isinstance(v_, six.string_types):
                _r = v_
                _ks = re.findall(re.compile(cls.REF_RE_PATTERN, re.S), v_)
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
        return _rcs_fnc(variant)


class VersionKey(object):
    ZFILL_COUNT = 3
    FNMATCH_PATTERN = 'v{}'.format('[0-9]'*ZFILL_COUNT)
    def __init__(self, text):
        self.set_validation(text)
        #
        self._text = text
        self._number = int(text[-self.ZFILL_COUNT:])
    @classmethod
    def set_validation(cls, text):
        if not fnmatch.filter([text], cls.FNMATCH_PATTERN):
            raise TypeError('version: "{}" is Non-match "{}"'.format(text, cls.FNMATCH_PATTERN))
    @property
    def number(self):
        return self._number

    def __str__(self):
        return self._text

    def __iadd__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError()
        self._number += int(other)
        self._text = 'v{}'.format(str(self._number).zfill(self.ZFILL_COUNT))
        return self

    def __isub__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError()
        if self._number >= other:
            self._number -= int(other)
        else:
            self._number = 0
        self._text = 'v{}'.format(str(self._number).zfill(self.ZFILL_COUNT))
        return self


class Matcher(MtdBasic):
    RSV_TASK_VERSION_CLASS = VersionKey
    def __init__(self, pattern, format_variant=None):
        self._orig_parameter = format_variant
        self._rsv_pattern = self._current_pattern = pattern
        self.set_variant_update(format_variant)
        #
        self._keys = self._get_keys_by_parse_pattern_(self._rsv_pattern)
        self._results = []
        self._matches = []
    @classmethod
    def _get_glob_pattern_by_parse_pattern_(cls, pattern):
        if pattern is not None:
            keys = cls._get_keys_by_parse_pattern_(pattern)
            s = pattern
            if keys:
                for key in keys:
                    s = s.replace('{{{}}}'.format(key), '*')
            return s
        return pattern
    @classmethod
    def _str_to_number_embedded_args_(cls, string):
        pieces = re.compile(r'(\d+)').split(unicode(string))
        pieces[1::2] = map(int, pieces[1::2])
        return pieces
    @classmethod
    def _get_results_(cls, pattern, trim):
        glob_pattern = cls._get_glob_pattern_by_parse_pattern_(pattern)
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
    #
    @property
    def keys(self):
        return self._keys

    def get_results(self, trim=None):
        return self._get_results_(self._current_pattern, trim)

    def _get_matches_(self, orig_pattern, current_pattern, trim):
        results = self._get_results_(current_pattern, trim)
        #
        lis = []
        for i_result in results:
            p = parse.parse(
                orig_pattern, i_result
            )
            if p:
                lis.append((i_result, p.named))
        return lis

    def set_variant_update(self, format_variant):
        if isinstance(format_variant, dict):
            self._current_pattern = self._set_pattern_update_(self._current_pattern, format_variant)

    def get_matches(self, trim=None):
        return self._get_matches_(self._rsv_pattern, self._current_pattern, trim)
    @property
    def orig(self):
        return self._rsv_pattern

    def get_latest(self):
        matches = self.get_matches(trim=(-1, None))
        if matches:
            result, parameters = matches[-1]
            return result

    def get_next(self):
        matches = self.get_matches(trim=(-1, None))
        if matches:
            result, parameters = matches[-1]
            if 'version' in parameters:
                version = parameters['version']
                rsv_version = self.RSV_TASK_VERSION_CLASS(version)
                rsv_version += 1
                parameters['version'] = str(rsv_version)
                return self._set_pattern_update_(self._rsv_pattern, parameters)

    def get_current(self):
        return self._current_pattern

    def __str__(self):
        return self._rsv_pattern


class AssetTaskFileGain(object):
    ASSET_PATH_PATTERN = (
        '/l/prod/{project}/{workspace}/assets/{role}/{asset}/'
    )
    TASK_KEY = (
        '{step}/{task}/'
    )
    VERSION_KEY = (
        '{asset}.{step}.{task}.{version}/'
    )
    FILE_PATH_PATTERN_ABC = (
        ASSET_PATH_PATTERN + TASK_KEY + VERSION_KEY +
        'cache/abc/hi.abc'
    )
    FILE_PATH_PATTERN_ASS = (
        ASSET_PATH_PATTERN + TASK_KEY + VERSION_KEY +
        'cache/ass/hi.ass'
    )
    FILE_PATH_PATTERN_XGN = (
        ASSET_PATH_PATTERN + TASK_KEY + VERSION_KEY +
        'scene/{asset}_{xgen_collection}.xgen'
    )
    FILE_PATH_PATTERN_KLF = (
        ASSET_PATH_PATTERN + TASK_KEY + VERSION_KEY +
        'look/klf/{asset}.klf'
    )
    FILE_PATH_PATTERN_KTN = (
        ASSET_PATH_PATTERN + TASK_KEY + VERSION_KEY +
        'katana/{asset}.katana'
    )
    WORKSPACE_PUBLISH = 'publish'
    def __init__(self, project, asset, step, task, workspace=None):
        # project
        self._project = project
        # asset
        if isinstance(asset, six.string_types):
            self._assets = [asset]
        elif isinstance(asset, (tuple, list)):
            self._assets = asset
        else:
            raise TypeError()
        if workspace is None:
            self._workspace = 'publish'
        else:
            self._workspace = workspace
        # step
        self._step = step
        self._task = task

    def _get_assets_file_paths_(self, pattern_inputs):
        asset_dict = collections.OrderedDict()
        for asset in self._assets:
            file_paths = []
            format_variant = {
                'workspace': self._workspace,
                'project': self._project,
                'asset': asset,
            }
            file_pattern_src = Matcher(self.ASSET_PATH_PATTERN, format_variant=format_variant)
            asset_matches = file_pattern_src.get_matches()
            if asset_matches:
                asset_result, asset_variants = asset_matches[-1]
                input_file_paths = []
                output_file_paths = []
                if isinstance(pattern_inputs, six.string_types):
                    pattern_inputs = [pattern_inputs]
                elif isinstance(pattern_inputs, (tuple, list)):
                    pattern_inputs = pattern_inputs
                #
                for input_pattern, step, task, output_patterns in pattern_inputs:
                    input_variant = copy.deepcopy(asset_variants)
                    input_variant.update(
                        {
                            'step': step,
                            'task': task,
                        }
                    )
                    input_file_pattern = Matcher(input_pattern, input_variant)
                    input_file_matches = input_file_pattern.get_matches(trim=(-5, None))
                    if input_file_matches:
                        input_file_match = input_file_matches[-1]
                        input_file_result, input_file_variants = input_file_match
                        if output_patterns is not None:
                            for output_pattern in output_patterns:
                                output_file_pattern = Matcher(output_pattern, format_variant=input_file_variants)
                                output_file_paths.append(output_file_pattern.get_current())
                        #
                        input_file_paths.append(input_file_result)
                    else:
                        input_file_paths.append(None)
                file_paths.append((tuple(input_file_paths), tuple(output_file_paths)))
            else:
                print('asset: "{}" is Non-valid'.format(asset))
            asset_dict[asset] = file_paths
        return asset_dict

    def get_look_file_export_args(self):
        pattern_inputs = [
            (self.FILE_PATH_PATTERN_ABC, 'srf', 'surfacing', None),
            (self.FILE_PATH_PATTERN_XGN, 'grm', 'groom', None),
            (self.FILE_PATH_PATTERN_ASS, 'srf', 'surfacing', (self.FILE_PATH_PATTERN_KLF, self.FILE_PATH_PATTERN_KTN)),
        ]
        return self._get_assets_file_paths_(pattern_inputs)
