# coding:utf-8
import lxresolver.commands as rsv_commands

import lxmaya.dcc.dcc_objects as mya_dcc_objects


class RsvApplication(object):
    def __init__(self):
        self._resolver = rsv_commands.get_resolver()
        self._scene_file_path = mya_dcc_objects.Scene.get_current_file_path()

    def get_rsv_task(self):
        print self._resolver.get_rsv_task_by_work_file_path(
            self._scene_file_path
        )

    def get_rsv_task_properties(self):
        pass
