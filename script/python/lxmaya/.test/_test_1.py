# coding:utf-8
import xgenm.xgGlobal as xgg

de = xgg.DescriptionEditor
active = de.getAttr(self.name, "active")
if active == "true":
    value = de.getAttr(self.name, "exportDir")
    de.setAttr(self.name, "exportDir", str(value))
    de.setAttr(self.name, "exportCurves", "true")
    #
    # Need to fill in the export faces to correct value
    #

    de.setAttr(self.name, "exportFaces", "")
    setProgressInfo(maya.stringTable['y_xgAnimWiresFXModuleTab.kAnimWireExportClumpingGuidesProgress'])
    cmd = 'xgmNullRender -percent 0 "' + de.currentDescription() + '"'
    mel.eval(cmd)
    value = de.getAttr(self.name, "_fullExportDir")
    cmd = 'source "' + str(value) + '"'
    mel.eval(cmd)
    de.setAttr(self.name, "exportCurves", "false")
    de.setAttr(self.name, "exportFaces", "")
else:
    xg.XGWarning(1, maya.stringTable['y_xgAnimWiresFXModuleTab.kTheModuleHasToBeActiveWarning'])