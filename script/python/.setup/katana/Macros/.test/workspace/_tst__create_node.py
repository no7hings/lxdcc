# coding:utf-8
import lxkatana

lxkatana.set_reload()

from Katana import KatanaFile

import lxkatana.scripts as ktn_scripts


for i in [
    '_Wsp/VariantPropertiesOpt',
    '_Wsp/VariantRegister',
    '_Wsp/VariantSet',
    '_Wsp/VariantSetGroup',
    #
    '_Wsp/UpstreamMerge',
    '_Wsp/TurntableRotateOpt',
    '_Wsp/Turntable',
    '_Wsp/CameraPropertiesOpt',
    '_Wsp/CameraCopyOpt',
    '_Wsp/CameraListOpt',
    '_Wsp/RenderPropertiesOpt',
    '_Wsp/RenderResolutionOpt',
    '_Wsp/UserDataOpt',
    '_Wsp/LookPropertiesOpt',
    '_Wsp/Aov',
    '_Wsp/Aovs',
    '_Wsp/AovGroup',
    '_Wsp/ColorCheckerAttachFitOpt',
    '_Wsp/ColorChecker',

    '_Wsp/Material',
    '_Wsp/MaterialGroup',
    '_Wsp/MaterialAssign',
    '_Wsp/MaterialAssignGroup',
    '_Wsp/GeometryPropertiesAssign',
    '_Wsp/GeometryPropertiesAssignGroup',
    '_Wsp/UtilityLookProperties',
    '_Wsp/Aovs',
    '_Wsp/UtilityMaterials',
    #
    '_Wsp/AssetGeometry',
    '_Wsp/Geometry',
    '_Wsp/AssetCamera',
    '_Wsp/UtilityCamera',
    '_Wsp/Camera',
    '_Wsp/AssetLightRig',
    '_Wsp/LightRig',
    '_Wsp/UtilityLight',
    '_Wsp/Quality',
    '_Wsp/Layer',
    #
    '_Wsp/Space',
    #
    '_Wsp/GeometrySpace',
    '_Wsp/CameraSpace',
    '_Wsp/LookSpace',
    '_Wsp/LightSpace',
    '_Wsp/QualitySpace',
    '_Wsp/LayerSpace',
    #
    '_Wsp/Workspace',
    '_Wsp/RenderLayer',
    # user
    '_Wsp_Usr/MaterialGroup',
    '_Wsp_Usr/MaterialAssignGroup',
    '_Wsp_Usr/GeometryPropertiesAssignGroup',
    #
    '_Wsp_Usr/GeometrySpace',
    '_Wsp_Usr/CameraSpace',
    '_Wsp_Usr/LookSpace',
    '_Wsp_Usr/LightSpace',
    '_Wsp_Usr/QualitySpace',
    '_Wsp_Usr/LayerSpace',
]:
    i_f = '/data/e/myworkspace/td/lynxi/script/python/.setup/katana/Macros/{}.yml'.format(i)
    i_m = ktn_scripts.ScpMacro(i_f)
    # if i_m.get_is_changed() is True:
    KatanaFile.New()
    i_m.build()
    i_m.save()
