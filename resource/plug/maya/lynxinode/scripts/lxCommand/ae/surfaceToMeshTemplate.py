# encoding=utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel
#
from lxCommand.template import nodeTemplate


#
class AEsurfaceToMeshTemplate(nodeTemplate.attributeTemplate):
    def set_auto_u_division_enable_swap(self):
        enable = cmds.getAttr(self.nodeName + '.autoUDivisionEnable')
        if enable is True:
            cmds.setAttr(self.nodeName + '.uDivision', lock=1)
        else:
            cmds.setAttr(self.nodeName + '.uDivision', lock=0)

    def set_auto_v_division_enable_swap(self):
        enable = cmds.getAttr(self.nodeName + '.autoVDivisionEnable')
        if enable is True:
            cmds.setAttr(self.nodeName + '.vDivision', lock=1)
        else:
            cmds.setAttr(self.nodeName + '.vDivision', lock=0)
    #
    def setup(self):
        self.beginScrollLayout()
        #
        self.beginLayout('Custom', collapse=False)
        self.addControl('uUniformEnable', label='U-uniform Enable')
        self.addControl('vUniformEnable', label='V-uniform Enable')
        self.addSeparator()
        self.addControl('uDivision', label='U-division')
        self.addControl('vDivision', label='V-division')
        self.endLayout()
        #
        mel.eval('AEdependNodeTemplate ' + self.nodeName)
        self.addExtraControls()
        #
        self.endScrollLayout()

