# coding:utf-8
import os

from lxscheme.scm_objects import _scm_obj_utility


class Root(object):
    main = '/'.join(
        os.path.dirname(__file__.replace('\\', '/')).split('/')
    )
    icon = '{}/.icon'.format(main)
    data = '{}/.data'.format(main)


class Data(object):
    ROOT = os.path.dirname(__file__.replace('\\', '/'))
    DATA_ROOT = '{}/.data'.format(ROOT)


class Scheme(object):
    STEPS = _scm_obj_utility.FileScheme(
        '{}/step_configures.yml'.format(Root.data)
    )
    CHECKER_CONFIGURES = _scm_obj_utility.FileScheme(
        '{}/checker_configures.yml'.format(Root.data)
    )
    EXPORTERS_CONFIGURE_PATH = '{}/exporters_configure.yml'.format(Root.data)
    EXPORTER_CONFIGURES = _scm_obj_utility.FileScheme(
        '{}/exporters_configure.yml'.format(Root.data)
    )


class Look(object):
    HAIR_TYPES = [
        'xgmDescription'
    ]
    GEOMETRY_TYPES = [
        'mesh'
    ]
    # key
    NAME = 'name'
    POINTS_UUID = 'points_uuid'
    FACE_VERTICES_UUID = 'face_vertices_uuid'
    #
    SEARCH_ORDER = [
        POINTS_UUID,
        FACE_VERTICES_UUID,
        NAME,
    ]
    # value
    TYPE = 'type'
    PATH = 'path'
    MATERIAL_ASSIGNS = 'material_assigns'
    PROPERTIES = 'properties'
    VISIBILITIES = 'visibilities'

    UV_MAPS = 'uv_maps'
