# coding:utf-8
import collections

from lxbasic import bsc_configure, bsc_core


class RsvConfigureMtd(object):
    @classmethod
    def get_raw(cls, key):
        raw = collections.OrderedDict()
        for i_key in ['builtin', 'main', 'frame', 'project', 'storage']:
            i_file = bsc_core.CfgFileMtd.get_yaml('resolver/{}/{}'.format(key, i_key))
            if i_file is not None:
                i_raw = bsc_core.StgFileOpt(i_file).set_read() or {}
                raw.update(i_raw)
        return raw
    @classmethod
    def get_basic_raw(cls):
        return cls.get_raw('basic')
    @classmethod
    def get_default_raws(cls):
        list_ = []
        for i_key in ['default', 'new']:
            i_raw = cls.get_raw(i_key)
            list_.append(i_raw)
        return list_


class ResolverMtd(object):
    @classmethod
    def set_rsv_obj_sort(cls, rsv_objs):
        rsv_objs.sort(
            key=lambda x: bsc_core.RawTextMtd.to_number_embedded_args(x.path)
        )


class RsvBaseMtd(object):
    pass


if __name__ == '__main__':
    print RsvConfigureMtd.get_basic_raw()
