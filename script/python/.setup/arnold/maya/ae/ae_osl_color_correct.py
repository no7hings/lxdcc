# encoding=utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

from lxmaya import ma_ae


# build by lynxi
class osl_color_correct(ma_ae.AbsNodeTemplate):
    def setup(self):
        self._create_dict = {}
        with self.scroll_layout():
            with self.layout('osl color correct', collapse=False):
                self.addControl('input')
                self.addControl('rgb_over')
                self.addControl('h_offset')
                self.addControl('s_offset')
                self.addControl('v_offset')
                self.addControl('scale')

            self.addExtraControls()