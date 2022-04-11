# coding:utf-8
from lxbasic import bsc_core

from lxsession.objects import ssn_obj_eng_abs


class SsnRsvApplication(ssn_obj_eng_abs.AbsSsnRsvApplication):
    def __init__(self):
        super(SsnRsvApplication, self).__init__()

    def _get_any_scene_file_path_(self):
        return bsc_core.EnvironMtd.get(
            'RSV_SCENE_FILE'
        )
