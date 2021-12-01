# coding:utf-8
import os

import glob


class Data(object):
    ROOT = os.path.dirname(__file__.replace('\\', '/'))
    DATA_PATH = '{}/.data'.format(ROOT)
    RESOLVER_BASIC_CONFIGURE_PATH = '{}/resolver-basic.yml'.format(DATA_PATH)
    @classmethod
    def get_project_configure_path(cls, project):
        return '{}/.data/resolver-{}.yml'.format(cls.ROOT, project)
    #
    GEOMETRY_USD_CONFIGURE_PATH = '{}/set-usd-configure.yml'.format(DATA_PATH)
    #
    ENTITIES_CONFIGURE_PATH = '{}/entities-configure.yml'.format(DATA_PATH)
    #
    ASSET_CONFIGURE_PATH = '{}/asset-configure.yml'.format(DATA_PATH)


class Key(object):
    KEYWORD = 'keyword'
    ROOT = 'root'
    PROJECT = 'project'
    WORKSPACE = 'workspace'
    TYPE = 'type'
    ASSET = 'asset'
    SHOT = 'shot'
    VERSION = 'version'


class Version(object):
    LATEST = 'latest'
    NEW = 'new'
    ALL = 'all'


class Platform(object):
    WINDOWS = 'windows'
    LINUX = 'linux'
    ALL = [
        WINDOWS,
        LINUX
    ]


class Application(object):
    MAYA = 'maya'
    HOUDINI = 'houdini'
    KATANA = 'katana'
    NUKE = 'nuke'
    ALL = [
        MAYA,
        HOUDINI,
        KATANA,
        NUKE
    ]
    PATHSEP_DICT = {
        MAYA: '|',
        HOUDINI: '/',
        KATANA: '/',
        NUKE: '/'
    }
    @classmethod
    def get_pathsep(cls, application):
        return cls.PATHSEP_DICT[application]


class Branch(object):
    KEY = 'branch'
    #
    ASSET = 'asset'
    SHOT = 'shot'
    ALL = [
        ASSET,
        SHOT
    ]


class Step(object):
    KEY = 'step'


class Task(object):
    KEY = 'task'


