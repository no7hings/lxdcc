# encoding=utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

from lxmaya import ma_ae


# build by lynxi
class osl_file_path(ma_ae.AbsNodeTemplate):
    def setup(self):
        self._create_dict = {}
        with self.scroll_layout():
            with self.layout('osl file path', collapse=False):
                self.addControl('filename', useAsFileName=True)
                self.addControl('udim_enable')
                self.addControl('sequence_enable')

            self.addExtraControls()
