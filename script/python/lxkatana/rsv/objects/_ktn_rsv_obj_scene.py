# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvScene(utl_rsv_obj_abstract.AbsRsvOHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvScene, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_scene_src_create(self):
        pass

    def set_scene_create(self):
        pass
