# coding:utf-8
import os

import enum

import getpass

import time


class Root(object):
    Main = '/'.join(
        os.path.dirname(__file__.replace('\\', '/')).split('/')[:-3]
    )
    Bin = '{}/bin'.format(Main)
    Python = '{}/python'.format(Main)
    Configure = '{}/configure'.format(Main)
    Execute = '{}/execute'.format(Main)


class ColorSpace(object):
    SRGB = 'sRGB'
    LINEAR = 'linear'
    RAW = 'raw'


class Status(enum.IntEnum):
    Unknown = 0
    Started = 1
    Running = 2
    Waiting = 3
    Completed = 4
    Suspended = 5
    Failed = 6
    Stopped = 7
    Error = 8
    Killed = 9
    Finished = 10


class SubProcessStatus(enum.EnumMeta):
    """
    0 正常结束
    1 sleep
    2 子进程不存在
    -15 kill
    None 在运行
    """
    Unknown = 2
    # sleep
    Failed = 1
    Completed = 0
    Running = None
    # kill
    Stopped = 5
    Error = -15


class Platform(object):
    Windows = 'windows'
    Linux = 'linux'
    #
    All = [
        Windows,
        Linux
    ]


class Application(object):
    Python = 'python'
    #
    Maya = 'maya'
    Houdini = 'houdini'
    Katana = 'katana'
    Nuke = 'nuke'
    Clarisse = 'clarisse'
    #
    Lynxi = 'lynxi'
    #
    All = [
        Python,
        #
        Maya,
        Houdini,
        Katana,
        Nuke,
        Clarisse,
        #
        Lynxi
    ]


class System(object):
    All = []
    for i_p in Platform.All:
        for i_a in Application.All:
            All.append('{}-{}'.format(i_p, i_a))


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