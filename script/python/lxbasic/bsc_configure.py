# coding:utf-8
import os

import enum

import getpass

import time


class Data(object):
    ROOT = os.path.dirname(__file__.replace('\\', '/'))


class Root(object):
    MAIN = '/'.join(
        os.path.dirname(__file__.replace('\\', '/')).split('/')[:-2]
    )
    BIN = '{}/bin'.format(MAIN)
    PYTHON = '{}/python'.format(MAIN)


class UserDirectory(object):
    user_name = getpass.getuser()
    WINDOWS = '{}/{}/.lynxi'.format(
        os.environ.get('HOMEDRIVE', 'c:'),
        os.environ.get('HOMEPATH', '/temp')
    ).replace('\\', '/')
    LINUX = '{}/.lynxi'.format(
        os.environ.get('HOME', '/temp')
    )


class LogDirectory(object):
    date_tag = time.strftime('%Y_%m%d', time.localtime(time.time()))
    WINDOWS = '{}/log/{}.log'.format(UserDirectory.WINDOWS, date_tag)
    LINUX = '{}/log/{}.log'.format(UserDirectory.LINUX, date_tag)


class CacheDirectory(object):
    WINDOWS = '{}/cache'.format(UserDirectory.WINDOWS)
    LINUX = '{}/cache'.format(UserDirectory.LINUX)


class HookDirectory(object):
    WINDOWS = '{}/hook'.format(UserDirectory.WINDOWS)
    LINUX = '{}/hook'.format(UserDirectory.LINUX)


class TemporaryDirectory(object):
    WINDOWS = '{}/temporary'.format(UserDirectory.WINDOWS)
    LINUX = '{}/temporary'.format(UserDirectory.LINUX)


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


class ShowStatus(enum.IntEnum):
    Started = 0
    Loading = 1
    Waiting = 2
    Finished = 3
    Completed = 4
    Failed = 5
    Stopped = 6


class ValidatorStatus(enum.IntEnum):
    Normal = 0x20
    Warning = 0x21
    Error = 0x22
    Correct = 0x23
    Ignore = 0x24
    Locked = 0x25


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
        #
        Lynxi
    ]


class System(object):
    All = []
    for i_p in Platform.All:
        for i_a in Application.All:
            All.append('{}-{}'.format(i_p, i_a))


if __name__ == '__main__':
    print System.All
