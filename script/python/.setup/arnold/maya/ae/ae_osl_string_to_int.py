# encoding=utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

from lxmaya import ma_ae


# build by lynxi
class osl_string_to_int(ma_ae.AbsNodeTemplate):
    def setup(self):
        self._create_dict = {}
        with self.scroll_layout():
            with self.layout('osl string to int', collapse=False):
                self.addControl('input')
                self.addControl('input_mapper')
                with self.layout('extra', collapse=False):
                    self.addControl('output_default')
                    self.addControl('output_maximum')

            self.addExtraControls()