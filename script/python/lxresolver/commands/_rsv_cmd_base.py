# coding:utf-8
from lxresolver.objects import _rsv_obj_main, _rsv_obj_cache


def get_resolver():
    _ = _rsv_obj_cache.__dict__['RSV_ROOT']
    if _ is not None:
        return _
    _ = _rsv_obj_main.RsvRoot()
    _rsv_obj_cache.__dict__['RSV_ROOT'] = _
    return _
