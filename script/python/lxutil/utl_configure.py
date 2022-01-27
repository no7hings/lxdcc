# coding:utf-8
import os

import enum

import jinja2

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


class UtilityToolData(_AbsData):
    ROOT = '{}/tool'.format(Root.UTILITY_DATA)


class UtilityToolkitData(_AbsData):
    ROOT = '{}/toolkit'.format(Root.UTILITY_DATA)


class UtilityProductData(_AbsData):
    ROOT = '{}/product'.format(Root.UTILITY_DATA)


class MayaToolkitData(_AbsData):
    ROOT = '{}/toolkit'.format(Root.MAYA_DATA)


class KatanaToolkitData(_AbsData):
    ROOT = '{}/toolkit'.format(Root.KATANA_DATA)


class UtilityMethodData(_AbsData):
    ROOT = '{}/method'.format(Root.UTILITY_DATA)


class MayaMenuData(_AbsData):
    ROOT = '{}/menu'.format(Root.MAYA_DATA)


class Data(object):
    ROOT = os.path.dirname(__file__.replace('\\', '/'))
    DATA_PATH = '{}/.data'.format(ROOT)
    #
    LOOK_SYSTEM_WORKSPACE_CONFIGURE_PATH = '{}/look-system-workspace-configure.yml'.format(DATA_PATH)
    #
    PATH_MAPPER_CONFIGURE_PATH = '{}/path-mapper-configure.yml'.format(DATA_PATH)
    #
    UTILITY_ROOT = '{}/utility'.format(ROOT)
    MAYA_ROOT = '{}/maya'.format(ROOT)
    HOUDINI_ROOT = '{}/houdini'.format(ROOT)
    KATANA_ROOT = '{}/katana'.format(ROOT)


class Port(object):
    VALIDATION_IGNORES = 'lx_validation_ignore'
    VALIDATION_CHECK_IGNORES = 'lx_validation_check_ignore'
    VALIDATION_REPAIR_IGNORES = 'lx_validation_repair_ignore'
    #
    GEOMETRY_UUIDS = 'lx_geometry_uuid'


class GeometryData(object):
    FACE_VERTICES = 'face_vertices'
    POINTS = 'points'


class GuiSize(object):
    item_height = 20


class App(object):
    HOUDINI = 'houdini'
    MAYA = 'maya'


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


class DccMeshCheckStatus_(enum.IntEnum):
    NonChanged = 0
    Deletion = 1
    Addition = 2
    #
    NameChanged = 3
    PathChanged = 4
    PathExchanged = 5
    #
    FaceVerticesChanged = 6
    PointsChanged = 7
    #
    GeometryChanged = 8


class GuiSectorChartMode(enum.IntEnum):
    Completion = 0
    Error = 1


class EnvironKey(object):
    SOURCE_PATHS = 'LYNXI_SOURCE_PATHS'


class Jinja(object):
    ROOT = MainData.get_directory('jinja')
    #
    MAIN = jinja2.Environment(
        loader=jinja2.FileSystemLoader(ROOT)
    )
    USDA = jinja2.Environment(
        loader=jinja2.FileSystemLoader('{}/usda'.format(ROOT))
    )
    XARC = jinja2.Environment(
        loader=jinja2.FileSystemLoader('{}/xarc'.format(ROOT))
    )
    ARNOLD = jinja2.Environment(
        loader=jinja2.FileSystemLoader('{}/arnold'.format(ROOT))
    )
    @classmethod
    def get_template(cls, key):
        return cls.MAIN.get_template(
            '{}.j2'.format(key)
        )
    @classmethod
    def get_configure(cls, key):
        return bsc_objects.Configure(
            value='{}/{}.yml'.format(cls.ROOT, key)
        )


class Hook(object):
    HOST = 'localhost'
    PORT = 9527


class Session(object):
    pass


if __name__ == '__main__':
    print UtilityProductData.get_as_configure('texture-tx-convert')
