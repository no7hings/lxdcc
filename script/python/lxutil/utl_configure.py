# coding:utf-8
import os

import lxbasic.objects as bsc_objects


class Root(object):
    main = '/'.join(
        os.path.dirname(__file__.replace('\\', '/')).split('/')[:-1]
    )
    icon = '{}/.icon'.format(main)
    data = '{}/.data'.format(main)
    #
    DATA = '{}/.data'.format(main)
    #
    UTILITY_DATA = '{}/utility'.format(DATA)
    MAYA_DATA = '{}/maya'.format(DATA)
    HOUDINI_DATA = '{}/houdini'.format(DATA)
    KATANA_DATA = '{}/katana'.format(DATA)


class _AbsData(object):
    ROOT = None
    @classmethod
    def get(cls, key):
        return '{}/{}.yml'.format(cls.ROOT, key)
    @classmethod
    def get_as_configure(cls, key):
        return bsc_objects.Configure(
            value=cls.get(key)
        )


class MainData(_AbsData):
    ROOT = Root.DATA
    @classmethod
    def get_directory(cls, key):
        return '{}/{}'.format(cls.ROOT, key)
    @classmethod
    def get_file(cls, file_name):
        return '{}/{}'.format(cls.ROOT, file_name)
    @classmethod
    def get_configure_file(cls, key):
        return '{}/{}.yml'.format(cls.ROOT, key)
    @classmethod
    def get_help_file(cls, key):
        return '{}/{}.md'.format(cls.ROOT, key)


class MayaToolkitData(_AbsData):
    ROOT = '{}/toolkit'.format(Root.MAYA_DATA)


class KatanaToolkitData(_AbsData):
    ROOT = '{}/toolkit'.format(Root.KATANA_DATA)


class UtilityMethodData(_AbsData):
    ROOT = '{}/method'.format(Root.UTILITY_DATA)


class MayaMenuData(_AbsData):
    ROOT = '{}/menu'.format(Root.MAYA_DATA)


class Port(object):
    VALIDATION_IGNORES = 'lx_validation_ignore'
    VALIDATION_CHECK_IGNORES = 'lx_validation_check_ignore'
    VALIDATION_REPAIR_IGNORES = 'lx_validation_repair_ignore'
    #
    GEOMETRY_UUIDS = 'lx_geometry_uuid'


class GeometryData(object):
    FACE_VERTICES = 'face_vertices'
    POINTS = 'points'


class DccMeshCheckStatus(object):
    NON_CHANGED = 'non-changed'
    #
    DELETION = 'deletion'
    ADDITION = 'addition'
    #
    NAME_CHANGED = 'name-changed'
    PATH_CHANGED = 'path-changed'
    PATH_EXCHANGED = 'path-exchanged'
    #
    FACE_VERTICES_CHANGED = 'face-vertices-changed'
    POINTS_CHANGED = 'points-changed'
    #
    GEOMETRY_CHANGED = 'geometry-changed'
    #
    ALL = [
        NON_CHANGED,
        #
        DELETION,
        ADDITION,
        #
        NAME_CHANGED,
        PATH_CHANGED,
        PATH_EXCHANGED,
        #
        FACE_VERTICES_CHANGED,
        POINTS_CHANGED,
        #
        GEOMETRY_CHANGED
    ]


class TextureTypes(object):
    # usd
    UsdPreviews = [
        'diffuse', 'ao',
        'metalness', 'specular', 'roughness',
        'coat', 'coat_roughness',
        'opacity',
        'normal', 'displacement',
    ]
    UsdPreviewMapper = {
        'albedo': 'diffuse'
    }
    All = [
        'diffuse', 'albedo', 'ao',
        'metalness', 'specular', 'roughness',
        'glossiness',
        'coat', 'coat_roughness',
        'normal', 'displacement', 'bump',
        #
        'transmission', 'opacity', 'translucency',
        'emission',
        'cavity',
        'mask'
    ]
    class Arnold(object):
        All = [
            'diffuse_color',
            'metalness',
            'specular', 'specular_roughness',
            'coat', 'coat_roughness',
            'transmission', 'opacity',
            'emission',
            'normal', 'displacement',
        ]
        Mapper = {
            'albedo': 'diffuse_color',
            'roughness': 'specular_roughness'
        }


if __name__ == '__main__':
    pass
