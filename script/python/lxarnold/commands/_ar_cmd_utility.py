# coding:utf-8
from lxarnold.dcc.dcc_objects import _ar_dcc_obj_utility, _ar_dcc_obj_callback


def get_scene():
    scene = _ar_dcc_obj_utility.Scene()
    _ar_dcc_obj_callback.__dict__['SCENE'] = scene
    return scene


def set_scene_load_from_dot_ass(file_path, root=None, root_lstrip=None):
    scene = _ar_dcc_obj_utility.Scene()
    scene.set_load_from_dot_ass(file_path, root=root, root_lstrip=root_lstrip)
    _ar_dcc_obj_callback.__dict__['SCENE'] = scene
    return scene


def set_scene_load_from_dot_mtlx(file_path, root=None, root_lstrip=None):
    scene = _ar_dcc_obj_utility.Scene()
    scene.set_load_from_dot_mtlx(file_path, root=root, root_lstrip=root_lstrip)
    _ar_dcc_obj_callback.__dict__['SCENE'] = scene
    return scene
