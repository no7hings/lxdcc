# coding:utf-8


class Util(object):
    OBJ_PATHSEP = '|'
    PORT_PATHSEP = '.'
    NAMESPACE_PATHSEP = ':'
    #
    MESH_TYPE = 'mesh'
    TRANSFORM_TYPE = 'transform'
    FILE_TYPE_NAME = 'file'
    MATERIAL_TYPE = 'shadingEngine'
    #
    XGEN_DESCRIPTION = 'xgmDescription'
    XGEN_SPLINE_GUIDE = 'xgmSplineGuide'
    #
    XGEN_PALETTE = 'xgmPalette'


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
