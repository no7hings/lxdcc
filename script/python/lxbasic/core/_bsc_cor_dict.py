# coding:utf-8
from ._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_raw

import lxcontent.core as ctt_core


CttYamlBase = ctt_core.CttYamlBase

CttYaml = ctt_core.CttYaml


class DictMtd(object):
    @classmethod
    def get_as_json_style(cls, dict_):
        return json.dumps(
            dict_,
            indent=4,
            skipkeys=True,
            sort_keys=True
        )

    @classmethod
    def get_as_yaml_style(cls, dict_):
        return CttYamlBase.dump(
            dict_,
            indent=4,
            default_flow_style=False
        )

    @classmethod
    def sort_key_to(cls, dict_):
        dict_1 = collections.OrderedDict()
        keys = dict_.keys()
        keys.sort()
        for i_key in keys:
            dict_1[i_key] = dict_[i_key]
        return dict_1

    @classmethod
    def sort_string_key_to(cls, dict_):
        dict_1 = collections.OrderedDict()
        keys = dict_.keys()
        keys = _bsc_cor_raw.RawTextsMtd.sort_by_number(keys)
        for i_key in keys:
            dict_1[i_key] = dict_[i_key]
        return dict_1

    @classmethod
    def sort_key_by_value_to(cls, dict_):
        value_to_key_dict = {v: k for k, v in dict_.items()}
        dict_1 = collections.OrderedDict()
        values = dict_.values()
        values.sort()
        for i_value in values:
            i_key = value_to_key_dict[i_value]
            dict_1[i_key] = i_value
        return dict_1

    @classmethod
    def deduplication_value_to(cls, dict_):
        dict_1 = {}
        for k, v_0 in dict_.items():
            v_1 = list(set(v_0))
            v_1.sort(key=v_0.index)
            dict_1[k] = v_1
        return dict_1


class DictOpt(object):
    PATHSEP = '.'

    def __init__(self, value):
        if not isinstance(value, dict):
            raise RuntimeError()

        self._value = value

    def get(self, key, default=None):
        ks = key.split(self.PATHSEP)
        if len(ks) == 1:
            return self._value.get(key, default)
        v_cur = self._value
        for i_k in ks:
            if isinstance(v_cur, dict):
                if i_k in v_cur:
                    v_cur = v_cur[i_k]
                else:
                    return default
            else:
                return default
        return v_cur

    def set(self, key, value):
        ks = key.split(self.PATHSEP)
        if len(ks) == 1:
            self._value[key] = value
        else:
            v_cur = self._value
            #
            maximum = len(ks)-1
            for seq, k in enumerate(ks):
                if seq == maximum:
                    v_cur[k] = value
                else:
                    if k not in v_cur:
                        v_cur[k] = collections.OrderedDict()
                    #
                    v_cur = v_cur[k]

    def to_dict(self):
        return self._value

    def __str__(self):
        return json.dumps(
            self._value,
            indent=4
        )
