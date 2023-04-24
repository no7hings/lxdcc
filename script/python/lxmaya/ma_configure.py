# coding:utf-8
import enum


class Util(object):
    OBJ_PATHSEP = '|'
    PORT_PATHSEP = '.'
    NAMESPACE_PATHSEP = ':'
    #
    MESH_TYPE = 'mesh'
    CURVE_TYPE = 'nurbsCurve'
    TRANSFORM_TYPE = 'transform'
    FILE_TYPE_NAME = 'file'
    MATERIAL_TYPE = 'shadingEngine'
    #
    XGEN_PALETTE = 'xgmPalette'
    XGEN_DESCRIPTION = 'xgmDescription'
    XGEN_SPLINE_GUIDE = 'xgmSplineGuide'


class Types(enum.EnumMeta):
    Mesh = 'mesh'
    Curve = 'nurbsCurve'
    Transform = 'transform'
    File = 'file'
    Material = 'shadingEngine'
    #
    XgenPalette = 'xgmPalette'
    XgenDescription = 'xgmDescription'
    XgenSplineGuide = 'xgmSplineGuide'


class ApiTypes(object):
    Transform = 'kTransform'
    TransformPlugin = 'kPluginTransformNode'
    #
    Transforms = {
        Transform,
        TransformPlugin
    }


class XGen(object):
    PATH_IGNORE_DICT = {
        'RandomGenerator': {
            'pointDir': ('usePoints', 'false')
        },
        'SplinePrimitive': {
            'cacheFileName': ('useCache', 'false'),
            'regionMap': ('regionMask', ['0.0', '0'])
        },
        'ClumpingFXModule': {
            'controlMapDir': [('useControlMaps', '0'), ('controlMask', ['0.0', '0'])]
        },
        'NoiseFXModule': {
            'bakeDir': ('mode', '0')
        }
    }
