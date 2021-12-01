# coding:utf-8
from lxusd.dcc.dcc_objects import _usd_dcc_obj_callback, _usd_dcc_obj_utility


def set_scene_load_from_dot_abc(file_path, root=None):
    scene = _usd_dcc_obj_utility.Scene()
    scene.set_load_from_dot_abc(file_path, root=root)
    _usd_dcc_obj_callback.__dict__['SCENE'] = scene
    _usd_dcc_obj_callback.__dict__['USD_STAGE'] = scene.usd_stage
    return scene


def set_scene_load_from_dot_usd(file_path, root=None):
    scene = _usd_dcc_obj_utility.Scene()
    scene.set_load_from_dot_usd(file_path, root)
    _usd_dcc_obj_callback.__dict__['SCENE'] = scene
    _usd_dcc_obj_callback.__dict__['USD_STAGE'] = scene.usd_stage
    return scene


def set_scene_load_from_file(file_path, root=None):
    scene = _usd_dcc_obj_utility.Scene()
    scene.set_load_from_file(file_path, root=root)
    _usd_dcc_obj_callback.__dict__['SCENE'] = scene
    _usd_dcc_obj_callback.__dict__['USD_STAGE'] = scene.usd_stage
    return scene
