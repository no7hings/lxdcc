# coding:utf-8
from lxbasic import bsc_core

from lxsession.objects import ssn_obj_eng_abs


class RsvApplication(ssn_obj_eng_abs.AbsRsvApplication):
    def __init__(self):
        super(RsvApplication, self).__init__()

    def _get_any_scene_file_path_(self):
        return bsc_core.EnvironMtd.get(
            'RSV_SCENE_FILE'
        )
