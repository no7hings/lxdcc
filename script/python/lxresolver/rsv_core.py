# coding:utf-8

from lxbasic import bsc_core


class ResolverMtd(object):
    @classmethod
    def set_rsv_obj_sort(cls, rsv_objs):
        rsv_objs.sort(key=lambda x: bsc_core.RawTextMtd.to_number_embedded_args(x.path))
