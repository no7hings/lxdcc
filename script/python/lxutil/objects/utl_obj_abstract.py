# coding:utf-8
import six

import fnmatch

import parse

import collections

import json

import re

from lxbasic import bsc_core

from lxutil import utl_core


class AbsContent(object):
    DEFAULT_VALUE = collections.OrderedDict()
    PATHSEP = None
    VARIANT_RE_PATTERN = r'[<](.*?)[>]'
    def __init__(self, key=None, value=None):
        self._key = key
        if isinstance(value, six.string_types):
            _ = utl_core.File.set_read(value)
            if isinstance(_, dict):
                self._value = _
            else:
                raise TypeError()
        elif isinstance(value, dict):
            self._value = value
        else:
            raise TypeError()

    def set_save_to(self, file_path):
        utl_core.File.set_write(file_path, self._value)
    @property
    def key(self):
        return self._key
    @property
    def value(self):
        return self._value
    @classmethod
    def _to_key_path_(cls, key):
        return '/' + key.replace('.', '/')

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
        _rcs_fnc(self._key, self._value)
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
        _rcs_fnc(self._key, self._value)
        return lis

    def get_keys(self, regex=None):
        _ = self._get_all_keys_()
        if regex is not None:
            return fnmatch.filter(_, regex)
        return _

    def get_key_as_paths(self):
        keys = self.get_keys()
        return [self._to_key_path_(i) for i in keys]

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
        if isinstance(value, dict) is True:
            return self.__class__(
                key, value
            )

    def _set_content_create_(self, key, value):
        if isinstance(value, dict) is False:
            raise TypeError()
        return self.__class__(
            key, value
        )

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

    def set_element_add(self, key, value):
        v = self.get(key)
        if isinstance(v, (tuple, list)):
            es = v
        else:
            es = []
            self.set(key, es)
        #
        if value not in es:
            es.append(value)

    def _set_value_unfold_(self, key, keys):
        def _rcs_fnc(key_, value_):
            if isinstance(value_, six.string_types):
                _value_unfold = value_
                _var_keys = re.findall(re.compile(self.VARIANT_RE_PATTERN, re.S), _value_unfold)
                if _var_keys:
                    for _var_key in set(_var_keys):
                        # catch value
                        if fnmatch.filter([_var_key], '*.key'):
                            _ = _var_key.split('.')
                            _c = len([i for i in _ if i == ''])
                            _ks = key_.split('.')
                            _v = _ks[-_c]
                        elif fnmatch.filter([_var_key], '.*'):
                            # etc key=nodes.asset.name, _var_key=<.label>, result=nodes.asset.label
                            _ = _var_key.split('.')
                            _c = len([i for i in _ if i == ''])
                            __k = '{}.{}'.format('.'.join(key_.split('.')[:-_c]), '.'.join(_[_c:]))
                            if __k not in keys:
                                raise TypeError('key: "{}" is Non-exists'.format(__k))
                            _v = self.get(__k)
                            #
                            _v = _rcs_fnc(__k, _v)
                        else:
                            if _var_key not in keys:
                                raise TypeError('key: "{}" is Non-exists'.format(_var_key))
                            _v = self.get(_var_key)
                            #
                            _v = _rcs_fnc(_var_key, _v)
                        #
                        if isinstance(_v, six.string_types):
                            _value_unfold = _value_unfold.replace('<{}>'.format(_var_key), _v)
                        elif isinstance(_v, (int, float, bool)):
                            _value_unfold = _value_unfold.replace('<{}>'.format(_var_key), str(_v))
                # etc: =0+1
                if fnmatch.filter([_value_unfold], '=*'):
                    cmd = _value_unfold[1:]
                    _value_unfold = eval(cmd)
                return _value_unfold
            elif isinstance(value_, (tuple, list)):
                return [_rcs_fnc(key_, _i) for _i in value_]
            return value_
        value = self.get(key)
        return _rcs_fnc(key, value)

    def set_clear(self):
        self._value = collections.OrderedDict()

    def __str__(self):
        return json.dumps(
            self.value,
            indent=4
        )

    def set_print_as_yaml_style(self):
        print bsc_core.OrderedYamlMtd.set_dump(
            self.value,
            indent=4,
            default_flow_style=False
        )


class AbsConfigure(AbsContent):
    PATHSEP = None
    def __init__(self, key, value):
        super(AbsConfigure, self).__init__(key, value)

    def set_flatten(self):
        keys = self.get_keys()
        for key in keys:
            value = self.get(key)
            if isinstance(value, dict) is False:
                value = self._set_value_unfold_(key, keys)
                self.set(key, value)


class AbsFileReader(object):
    SEP = '\n'
    LINE_MATCHER_CLS = None
    PROPERTIES_CLASS = None
    def __init__(self, file_path):
        self._file_path = file_path
        self._set_line_raw_update_()

    def _set_line_raw_update_(self):
        self._lines = []
        if self._file_path is not None:
            with open(self._file_path) as f:
                raw = f.read()
                sep = self.SEP
                self._lines = self._get_lines_(raw, sep)
    @classmethod
    def _get_lines_(cls, raw, sep):
        return [r'{}{}'.format(i, sep) for i in raw.split(sep)]
    @property
    def file_path(self):
        return self._file_path
    @property
    def lines(self):
        return self._lines
    @classmethod
    def _get_matches_(cls, pattern, lines):
        lis = []
        pattern_0 = cls.LINE_MATCHER_CLS(pattern)
        lines = fnmatch.filter(
            lines, pattern_0.pattern
        )
        for line in lines:
            p = parse.parse(
                pattern_0.format, line
            )
            if p:
                variants = p.named
                lis.append((line, variants))
        #
        return lis
