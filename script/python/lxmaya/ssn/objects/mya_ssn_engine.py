# coding:utf-8
import lxsession.abstracts as ssn_abstracts

import lxmaya.dcc.dcc_objects as mya_dcc_objects


class SsnRsvApplication(ssn_abstracts.AbsSsnRsvApplication):
    def __init__(self):
        super(SsnRsvApplication, self).__init__()

    def _get_any_scene_file_path_(self):
        return mya_dcc_objects.Scene.get_current_file_path()
