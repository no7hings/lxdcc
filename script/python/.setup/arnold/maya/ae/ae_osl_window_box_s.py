# encoding=utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

from lxmaya import ma_ae


# build by lynxi
class osl_window_box_s(ma_ae.AbsNodeTemplate):
    def setup(self):
        self._create_dict = {}
        with self.scroll_layout():
            with self.layout('osl window box s', collapse=False):
                with self.layout('texture', collapse=False):
                    self.addControl('filename', useAsFileName=True)
                    self.addControl('udim_maximum')
                    self.addControl('texture_flip')
                    self.addControl('texture_flop')
                with self.layout('basic', collapse=False):
                    self.addControl('space', enumerateOption='x|-x|y|-y|z|-z')
                    self.addControl('rotation_x')
                    self.addControl('rotation_y')
                    self.addControl('rotation_z')
                with self.layout('extra', collapse=False):
                    self.addControl('depth')
                    self.addControl('overscan_left')
                    self.addControl('overscan_right')
                    self.addControl('overscan_top')
                    self.addControl('overscan_bottom')
                    self.addControl('contract_back')
                    self.addControl('curtains_enable')
                    self.addControl('middle_enable')
                    self.addControl('middle_depth')
                    self.addControl('middle_offset_x')
                    self.addControl('middle_offset_y')

            self.addExtraControls()