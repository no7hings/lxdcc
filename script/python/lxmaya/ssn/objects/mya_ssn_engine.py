# coding:utf-8
from lxsession.objects import ssn_obj_eng_abs

import lxmaya.dcc.dcc_objects as mya_dcc_objects


class SsnRsvApplication(ssn_obj_eng_abs.AbsSsnRsvApplication):
    def __init__(self):
        super(SsnRsvApplication, self).__init__()

    def _get_any_scene_file_path_(self):
        return mya_dcc_objects.Scene.get_current_file_path()
