# coding:utf-8
import lxkatana

lxkatana.set_reload()

from Katana import KatanaFile

import lxkatana.scripts as ktn_scripts


for i in [
    'VariantPropertiesOpt',
    'VariantRegister',
    'VariantSet',
    #
    'Turntable',
    'CameraPropertiesOpt',
    'RenderPropertiesOpt',
    'RenderResolutionOpt',
    'ColorCheckerCameraFitOpt',
    'UserDataOpt',
    'LookPropertiesOpt',
    'Aov',
    'AovGroup',
    'ColorChecker',
    'CameraListOpt',
    'UpstreamMerge',

    'Material',
    'MaterialGroup',
    'MaterialAssign',
    'MaterialAssignGroup',
    'GeometryPropertiesAssign',
    'GeometryPropertiesAssignGroup',
    'UtilityLookProperties',
    'UtilityAovs',
    'UtilityMaterials',
    'LightRig',
    #
    'UserMaterialGroup',
    'UserMaterialAssignGroup',
    'UserGeometryPropertiesAssignGroup',
    #
    'Geometry',
    'Camera',
    'Light',
    'Quality',
    'Layer',
    #
    'MaterialArea',
    'UtilityLight',
    #
    'Space',
    #
    'GeometrySpace',
    'CameraSpace',
    'LookSpace',
    'LightSpace',
    'QualitySpace',
    'LayerSpace',
    #
    'UserGeometrySpace',
    'UserCameraSpace',
    'UserLookSpace',
    'UserLightSpace',
    'UserQualitySpace',
    'UserLayerSpace',
]:
    KatanaFile.New()
    i_f = '/data/e/myworkspace/td/lynxi/script/python/.setup/katana/Macros/_Wsp/{}.yml'.format(i)
    i_m = ktn_scripts.ScpMacro(i_f)
    i_m.build()
    i_m.save()
