# coding:utf-8
from lxresolver.objects import _rsv_obj_callback

from lxresolver.objects import _rsv_obj_utility


def get_resolver():
    _ = _rsv_obj_callback.__dict__['RESOLVER']
    if _ is None:
        _ = _rsv_obj_utility.Resolver()
        _rsv_obj_callback.__dict__['RESOLVER'] = _
    return _


def get_task_properties_by_work_scene_src_file_path(file_path):
    resolver = get_resolver()
    task_properties = resolver.get_task_properties_by_work_scene_src_file_path(file_path)
    _rsv_obj_callback.__dict__['TASK_PROPERTIES'] = task_properties
    return task_properties


def get_task_properties_by_scene_src_file_path(file_path):
    resolver = get_resolver()
    task_properties = resolver.get_task_properties_by_scene_src_file_path(file_path)
    _rsv_obj_callback.__dict__['TASK_PROPERTIES'] = task_properties
    return task_properties
