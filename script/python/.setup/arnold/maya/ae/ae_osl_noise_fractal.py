# encoding=utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

from lxmaya import ma_ae


class osl_noise_fractal(ma_ae.AbsNodeTemplate):
    def setup(self):
        self._create_dict = {}
        #
        with self.scroll_layout():
            with self.layout('Attribute(s)', collapse=False):
                self.addControl('octaves')
                self.addControl('distortion')
                self.addControl('value')
                self.addControl('gain')
                self.addControl('lacunarity')
                self.addControl('rotation')
                self.addControl('offset')
                self.addControl('scale')
                self.addControl('coord_space', enumerateOption='world|object|Pref|uv')
                self.addControl('position')
                self.addControl('frame')
                self.addControl('color1')
                self.addControl('color2')
                self.addControl('mode', enumerateOption='scalar|vector')
                self.addControl('turbulent_enable')
                self.addControl('clamp_enable')

            #
            self.addExtraControls()