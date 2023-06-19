# coding:utf-8
from ._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_raw


class OrderedYamlMtd(object):
    @classmethod
    def set_dump(cls, raw, stream=None, Dumper=yaml.SafeDumper, object_pairs_hook=collections.OrderedDict, **kwargs):
        class _Cls(Dumper):
            pass
        # noinspection PyUnresolvedReferences
        def _fnc(dumper_, data_):
            return dumper_.represent_mapping(
                yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                data_.items(),
            )

        _Cls.add_representer(object_pairs_hook, _fnc)
        return yaml.dump(raw, stream, _Cls, **kwargs)
    @classmethod
    def set_load(cls, stream, Loader=yaml.SafeLoader, object_pairs_hook=collections.OrderedDict):
        class _Cls(Loader):
            pass
        # noinspection PyArgumentList
        def _fnc(loader_, node_):
            loader_.flatten_mapping(node_)
            return object_pairs_hook(loader_.construct_pairs(node_))
        # noinspection PyUnresolvedReferences
        _Cls.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _fnc)
        return yaml.load(stream, _Cls)


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
        return OrderedYamlMtd.set_dump(
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
