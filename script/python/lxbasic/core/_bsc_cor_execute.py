# coding:utf-8
from _bsc_cor_utility import *

from lxbasic.core import _bsc_cor_environ


class Executes(object):
    @classmethod
    def oiiotool(cls):
        if SystemMtd.get_is_windows():
            name = 'oiiotool.exe'
            _ = _bsc_cor_environ.EnvironMtd.find_execute(name)
            if _:
                return name
            return '{}/windows/oiiotool.exe'.format(bsc_configure.Root.Execute)
        elif SystemMtd.get_is_linux():
            name = 'oiiotool'
            _ = _bsc_cor_environ.EnvironMtd.find_execute(name)
            if _:
                return name
            return '{}/linux/oiiotool'.format(bsc_configure.Root.Execute)

    @classmethod
    def oslc(cls):
        if SystemMtd.get_is_windows():
            name = 'oslc.exe'
            _ = _bsc_cor_environ.EnvironMtd.find_execute(name)
            if _:
                return name
            return '{}/windows/oslc.exe'.format(bsc_configure.Root.Execute)
        elif SystemMtd.get_is_linux():
            name = 'oslc'
            _ = _bsc_cor_environ.EnvironMtd.find_execute(name)
            if _:
                return name
            return '{}/linux/oslc'.format(bsc_configure.Root.Execute)

    @classmethod
    def oslinfo(cls):
        if SystemMtd.get_is_windows():
            name = 'oslinfo.exe'
            _ = _bsc_cor_environ.EnvironMtd.find_execute(name)
            if _:
                return name
            return '{}/windows/oslinfo.exe'.format(bsc_configure.Root.Execute)
        elif SystemMtd.get_is_linux():
            name = 'oslinfo'
            _ = _bsc_cor_environ.EnvironMtd.find_execute(name)
            if _:
                return name
            return '{}/linux/oslinfo'.format(bsc_configure.Root.Execute)

    @classmethod
    def ffmpeg(cls):
        if SystemMtd.get_is_windows():
            return 'l:/packages/pg/third_party/app/ffmpeg/4.4.0/platform-windows/bin/ffmpeg.exe'
        elif SystemMtd.get_is_linux():
            return '/l/packages/pg/third_party/app/ffmpeg/4.4.0/platform-linux/bin/ffmpeg'
