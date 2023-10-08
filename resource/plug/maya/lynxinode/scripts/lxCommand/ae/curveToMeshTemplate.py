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
class AEcurveToMeshTemplate(nodeTemplate.attributeTemplate):
    @staticmethod
    def set_curve_select(nodeName):
        curve = ctomcmds.get_c2m_curve(nodeName)
        if curve:
            cmds.select(curve)
            ctomcmds.setAddToModelPanel(curve)
    #
    def set_curve_select_new(self, atr_path):
        tokens = atr_path.split('.')
        nodeName = tokens[0]
        cmds.button(
            'ctomSelCurveButton', label='Select Curve', backgroundColor=(1, .5, .25),
            command=lambda arg=None, x=nodeName: self.set_curve_select(x)
        )
    #
    def set_curve_select_replace(self, atr_path):
        tokens = atr_path.split('.')
        nodeName = tokens[0]
        cmds.button(
            'ctomSelCurveButton', edit=True,
            command=lambda arg=None, x=nodeName: self.set_curve_select(x)
        )
    @staticmethod
    def set_modify_reset(nodeName):
        ctomcmds.set_c2m_modify_reset(nodeName)
    #
    def set_modify_reset_new(self, atr_path):
        tokens = atr_path.split('.')
        nodeName = tokens[0]
        cmds.button(
            'ctomResetModifyButton', label='Reset Modify', backgroundColor=(1, 0, .25),
            command=lambda arg=None, x=nodeName: self.set_modify_reset(x)
        )
    #
    def set_modify_reset_replace(self, atr_path):
        tokens = atr_path.split('.')
        nodeName = tokens[0]
        cmds.button(
            'ctomResetModifyButton', edit=True,
            command=lambda arg=None, x=nodeName: self.set_modify_reset(x)
        )

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
        self.addControl('uniformEnable', label='Uniform Enable')
        self.addSeparator()
        self.addControl('baseAttachToMeshEnable', label='Base Attach-to-mesh Enable')
        self.addControl('order', label='Order')
        self.addSeparator()
        #
        self.addControl('autoUDivisionEnable', label='Auto U-division Enable', changeCommand=lambda *args: self.set_auto_u_division_enable_swap())
        self.addControl('autoVDivisionEnable', label='Auto V-division Enable', changeCommand=lambda *args: self.set_auto_v_division_enable_swap())
        self.addControl('uDivision', label='U-division')
        self.addControl('vDivision', label='V-division')
        self.addSeparator()
        #
        self.addControl('uSample', label='U-sample')
        self.addControl('vSample', label='V-sample')
        self.addSeparator()
        #
        self.addControl('width', label='Width')
        self.endLayout()
        #
        self.addCustom('set_curve_select', self.set_curve_select_new, self.set_curve_select_replace)
        #
        self.beginLayout('Modify', collapse=False)
        self.addControl('spin', label='Spin')
        self.addControl('twist', label='Twist')
        self.addControl('taper', label='Taper')
        self.addSeparator()
        self.addControl('archAttachCurveEnable', label='Arch Attach-to-curve Enable')
        self.addControl('arch', label='Arch')
        self.addSeparator()
        self.addControl('startIndex', label='Start-index')
        self.addControl('endIndex', label='End-index')
        self.endLayout()
        #
        self.addCustom('set_modify_reset', self.set_modify_reset_new, self.set_modify_reset_replace)
        #
        self.beginLayout('Extra', collapse=True)
        mel.eval('AEaddRampControl ' + self.nodeName + '.widthExtra')
        mel.eval('AEaddRampControl ' + self.nodeName + '.spinExtra')
        mel.eval('AEaddRampControl ' + self.nodeName + '.archExtra')
        self.endLayout()
        #
        self.beginLayout('Texture-coord', collapse=False)
        self.addControl('uTextureCoordTileWidth', label='U-texture-coord Tile-width')
        self.addControl('vTextureCoordTileWidth', label='V-texture-coord Tile-width')
        #
        mel.eval('AEdependNodeTemplate ' + self.nodeName)
        self.addExtraControls()
        #
        self.endScrollLayout()

