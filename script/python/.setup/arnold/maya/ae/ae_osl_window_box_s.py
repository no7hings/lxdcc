# encoding=utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

from lxmaya import ma_ae


class osl_window_box_s(ma_ae.AbsNodeTemplate):
    def setup(self):
        self._create_dict = {}
        #
        with self.scroll_layout():
            with self.layout('Attribute(s)', collapse=False):
                self.addControl('space', enumerateOption='x|-x|y|-y|z|-z')
                self.addControl('filename', useAsFileName=True)
                self.addControl('texture_flip')
                self.addControl('texture_flop')
                self.addControl('room_depth')
                self.addControl('width_overscan')
                self.addControl('height_overscan')
                self.addControl('midground_depth')
                self.addControl('midground_offset_x')
                self.addControl('midground_offset_y')
                self.addControl('add')
                self.addControl('multiply')
                self.addControl('curtains_enable')
                self.addControl('midground_enable')

            #
            self.addExtraControls()