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
    CONFIGURE = '{}/configure'.format(MAIN)
    EXECUTE = '{}/execute'.format(MAIN)

    @classmethod
    def get_configure_file(cls, key):
        return '{root}/{key}.yml'.format(**dict(root=Root.CONFIGURE, key=key))


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
    Unknown = -1
    Started = 0
    Loading = 1
    Waiting = 2
    Finished = 3
    Completed = 4
    Failed = 5
    Stopped = 6
    Killed = 7


class ValidatorStatus(enum.IntEnum):
    Normal = 0x20
    Correct = 0x21
    Warning = 0x22
    Error = 0x23
    Ignore = 0x24
    Locked = 0x25
    Active = 0x26
    Disable = 0x27


class ActionState(enum.IntEnum):
    Normal = 0x30
    Enable = 0x31
    Disable = 0x32
    #
    PressEnable = 0x41
    PressDisable = 0x42
    #
    ChooseEnable = 0x51
    ChooseDisable = 0x52


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


class Rgba(object):
    # 63+48=111
    # 127+48=175
    Red = 255, 0, 63, 255
    DarkRed = 159, 0, 63, 255
    LightRed = 255, 47, 111, 255
    Orange = 255, 127, 63, 255
    DarkOrange = 159, 95, 63, 255
    LightOrange = 255, 175, 111, 255
    Yellow = 255, 255, 63, 255
    DarkYellow = 159, 159, 63, 255
    LightYellow = 255, 255, 111, 255
    Green = 63, 255, 127, 255
    DarkGreen = 63, 159, 95, 255
    LightGreen = 111, 255, 175, 255
    Blue = 63, 127, 255, 255
    DarkBlue = 63, 95, 159, 255
    LightBlue = 111, 175, 255
    BabyBlue = 63, 255, 255, 255
    DarkBabyBlue = 63, 159, 159, 255
    LightBabyBlue = 111, 255, 255, 255
    Purple = 127, 127, 255, 255
    DarkPurple = 95, 95, 159, 255
    LightPurple = 175, 175, 255, 255
    Pink = 255, 127, 127, 255
    DarkPink = 159, 95, 79, 255
    LightPink = 255, 175, 175, 255
    Gray = 127, 127, 127, 255
    White = 255, 255, 255, 255
    Black = 0, 0, 0, 255
    Opacity = 0, 0, 0, 0

    All = [
        Red, DarkRed, LightRed,
        LightOrange, Orange, DarkOrange,
        LightYellow, Yellow, DarkYellow,
        LightGreen, Green, DarkGreen,
        LightBlue, Blue, DarkBlue,
        LightPurple, Purple, DarkPurple,
        LightPink, Pink, DarkPink,
        Gray, White, Black, Opacity
    ]


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


if __name__ == '__main__':
    print System.All
