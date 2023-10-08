# encoding=utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel
#
import lxCommand.cmds as ctomcmds
#
from lxCommand.template import nodeTemplate


#
class AEcurveToMeshExtraTemplate(nodeTemplate.attributeTemplate):

    def show_control_window_new(self, atr_path):
        tokens = atr_path.split('.')
        nodeName = tokens[0]
        cmds.button(
            'ctmeShowControlWindow', label='Show Control Window', backgroundColor=(1, .5, .25),
            command=self.show_control_window_command
        )

    def show_control_window_replace(self, atr_path):
        tokens = atr_path.split('.')
        nodeName = tokens[0]
        cmds.button(
            'ctmeShowControlWindow', edit=True,
            command=self.show_control_window_command
        )

    def show_control_window_command(self):
        pass
    #
    def setup(self):
        self.beginScrollLayout()
        self.beginLayout('Custom', collapse=False)
        self.addControl('baseAttachToGrowMeshEnable', label='Base Attach to Grow Mesh Enable')
        self.addControl('order', label='Order')
        self.addControl('radius', label='Radius')
        self.addControl('spin', label='Spin')
        self.addControl('twist', label='Twist')
        self.addControl('taper', label='Taper')
        self.endLayout()
        #
        self.beginLayout('Setting', collapse=False)
        self.addControl('uAutoDivisionEnable', label='U Auto Division Enable')
        self.addControl('uDivision', label='U Division')
        self.addControl('uUniformEnable', label='U Uniform Enable')
        self.addControl('uSmoothingEnable', label='U Smoothing Enable')
        self.addControl('uDegree', label='U Degree')
        self.addControl('uSample', label='U Sample')
        self.addControl('uStartIndex', label='U Start Index')
        self.addControl('uEndIndex', label='U End Index')
        self.addControl('vAutoDivisionEnable', label='U Auto Division Enable')
        self.addControl('vDivision', label='V Division')
        self.addControl('vUniformEnable', label='V Uniform Enable')
        self.addControl('vSmoothingEnable', label='V Smoothing Enable')
        self.addControl('vDegree', label='V Degree')
        self.addControl('vSample', label='V Sample')
        self.addControl('vStartIndex', label='V Start Index')
        self.addControl('vEndIndex', label='V End Index')
        self.endLayout()

        self.beginLayout('Extra', collapse=False)
        self.addControl('vTranslateUniformEnable', label='V Translate Uniform Enable')
        self.addControl('vTranslateExtraSmooth', label='V Translate Smooth')
        self.addControl('vTranslateExtraPoints', label='V Translate Points')
        self.addControl('vRotateUniformEnable', label='V Rotate Uniform Enable')
        self.addControl('vRotateExtraSmooth', label='V Rotate Smooth')
        self.addControl('vRotateExtraPoints', label='V Rotate Points')
        self.addControl('vScaleUniformEnable', label='V Scale Uniform Enable')
        self.addControl('vScaleExtraSmooth', label='V Scale Smooth')
        self.addControl('vScaleExtraPoints', label='V Scale Points')
        self.endLayout()

        mel.eval('AEdependNodeTemplate ' + self.nodeName)
        self.addExtraControls()
        #
        self.endScrollLayout()

