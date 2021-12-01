# coding:utf-8
import os

import json

import yaml

import re

import fnmatch


class AbsContentDef(object):
    PATHSEP = '.'
    def _set_content_def_init_(self, key, value):
        self._key = key
        self._raw = value
    @property
    def key(self):
        return self._key
    @property
    def value(self):
        return self._raw

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
        _rcs_fnc(self._key, self._raw)
        return lis

    def _get_keys_(self, regex=None):
        _ = self._get_all_keys_()
        if regex is not None:
            return fnmatch.filter(_, regex)
        return _

    def get_keys(self, regex=None):
        _ = self._get_keys_(regex)
        if _:
            _.sort()
        return _

    def get(self, key_path, default_value=None):
        keys = key_path.split(self.PATHSEP)
        value = self.value
        for key in keys:
            if isinstance(value, dict):
                if key in value:
                    # noinspection PyUnresolvedReferences
                    value = value[key]
                else:
                    return default_value
            else:
                return default_value
        return value

    def set_variant_convert(self, variant):
        re_pattern = re.compile(r'[<](.*?)[>]', re.S)
        if isinstance(variant, (str, unicode)):
            s = variant
            keys = re.findall(re_pattern, variant)
            if keys:
                for i in set(keys):
                    v = self.get(i)
                    if v is None:
                        raise TypeError('key: "{}" is Non-exists'.format(i))
                    v = self.set_variant_convert(v)
                    if isinstance(v, (str, unicode)):
                        s = s.replace('<{}>'.format(i), v)
                    elif isinstance(v, (tuple, list)):
                        return None
            return s
        elif isinstance(variant, (tuple, list)):
            lis = []
            for i in variant:
                keys = re.findall(re_pattern, i)
                if keys:
                    v = self.get(keys[0])
                    if v:
                        index = variant.index(i)
                        if isinstance(v, list):
                            v.reverse()
                            [lis.insert(index, self.set_variant_convert(i)) for i in v]
                        elif isinstance(v, (str, unicode)):
                            lis.append(self.set_variant_convert(v))
                else:
                    lis.append(i)
            return lis
        return variant

    def __str__(self):
        return json.dumps(
            self.value,
            indent=4
        )


class AbsSchemeFileLoader(AbsContentDef):
    CONTENT_CLASS = None
    def __init__(self, *args):
        self._file_path = args[0]
        #
        key = None
        value = self._get_file_raw_(self._file_path)
        self._set_content_def_init_(key, value)
    @classmethod
    def _get_file_raw_(cls, file_path):
        if os.path.exists(file_path):
            ext = os.path.splitext(file_path)[-1]
            if ext in ['.json']:
                with open(file_path) as j:
                    return json.load(j)
            elif ext in ['.yml']:
                with open(file_path) as y:
                    return yaml.load(y)
            else:
                raise TypeError(
                    'Scheme-file-ext: "{}" is Non-available'.format(ext)
                )
        else:
            raise TypeError(
                'Scheme-file-path: "{}" is Non-exists'.format(file_path)
            )

    def set_layer_load(self, file_scheme):
        def _rcs_fnc(old_raw_, new_raw_):
            if isinstance(old_raw_, dict):
                for _k, _v in new_raw_.items():
                    if _k in old_raw_:
                        if isinstance(_v, dict):
                            _old_raw = old_raw_[_k]
                            _new_raw = new_raw_[_k]
                            _rcs_fnc(_old_raw, _new_raw)
                        else:
                            if isinstance(old_raw_, dict):
                                old_raw_[_k] = _v
                    else:
                        old_raw_[_k] = _v

        old_raw = self.value
        new_raw = file_scheme.value
        _rcs_fnc(old_raw, new_raw)

    def get_content(self, key_path, default_value=None):
        key = key_path.split(self.PATHSEP)[-1]
        value = self.get(key_path, default_value)
        return self.CONTENT_CLASS(
            key, value
        )

    def _set_content_create_(self, key, value):
        return self.CONTENT_CLASS(
            key, value
        )

    def __str__(self):
        return json.dumps(
            self.value,
            indent=4
        )
