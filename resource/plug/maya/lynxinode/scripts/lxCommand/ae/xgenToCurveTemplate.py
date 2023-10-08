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
class AExgenToCurveTemplate(nodeTemplate.attributeTemplate):
    def setup(self):
        self.beginScrollLayout()
        #
        self.addExtraControls()
        #
        self.endScrollLayout()

