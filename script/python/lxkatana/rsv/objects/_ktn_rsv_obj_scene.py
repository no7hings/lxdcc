# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvScene(utl_rsv_obj_abstract.AbsRsvObj):
    def __init__(self, rsv_scene_properties):
        super(RsvScene, self).__init__(rsv_scene_properties)

    def set_scene_src_create(self):
        pass

    def set_scene_create(self):
        pass
