# coding:utf-8
from __future__ import division

import sys

import os

import collections

import yaml

import json

import six

import xmlrpclib

import getpass

import time

import datetime

import platform

import re

import fnmatch

import zipfile

import subprocess

import parse

import uuid

import math

import hashlib

import struct

import gzip

import copy

import glob

import threading

import socket

import itertools

import functools

import urllib

# import scandir

from lxbasic import bsc_configure

import shutil

import multiprocessing

THREAD_MAXIMUM = threading.Semaphore(1024)

SP_THREAD_MAXIMUM = threading.Semaphore(
    multiprocessing.cpu_count()-4
)

CPU_COUNT = multiprocessing.cpu_count()


class PyThread(threading.Thread):
    def __init__(self, fnc, *args, **kwargs):
        threading.Thread.__init__(self)
        self._fnc = fnc
        self._args = args
        self._kwargs = kwargs
    #
    def run(self):
        THREAD_MAXIMUM.acquire()
        self._fnc(*self._args, **self._kwargs)
        THREAD_MAXIMUM.release()


class PlatformMtd(object):
    @staticmethod
    def get_is_linux():
        return platform.system() == 'Linux'
    @staticmethod
    def get_is_windows():
        return platform.system() == 'Windows'
    @staticmethod
    def get_current():
        if platform.system() == 'Windows':
            return bsc_configure.Platform.Windows
        elif platform.system() == 'Linux':
            return bsc_configure.Platform.Linux


class ApplicationMtd(object):
    @classmethod
    def get_is_maya(cls):
        _ = os.environ.get('MAYA_APP_DIR')
        if _:
            return True
        return False
    @classmethod
    def get_is_houdini(cls):
        _ = os.environ.get('HIP')
        if _:
            return True
        return False
    @classmethod
    def get_is_katana(cls):
        _ = os.environ.get('KATANA_ROOT')
        if _:
            return True
        return False
    @classmethod
    def get_is_lynxi(cls):
        _ = os.environ.get('LYNXI_ROOT')
        if _:
            return True
        return False
    @classmethod
    def get_is_nuke(cls):
        pass
    @classmethod
    def get_is_clarisse(cls):
        _ = os.environ.get('IX_PYTHON2HOME')
        if _:
            return True
        return False
    @classmethod
    def get_is_dcc(cls):
        for i_fnc in [
            cls.get_is_maya,
            cls.get_is_houdini,
            cls.get_is_katana,
            cls.get_is_clarisse,
            cls.get_is_lynxi
        ]:
            if i_fnc() is True:
                return True
        return False
    @classmethod
    def get_current(cls):
        for i_fnc, i_app in [
            (cls.get_is_maya, bsc_configure.Application.Maya),
            (cls.get_is_houdini, bsc_configure.Application.Houdini),
            (cls.get_is_katana, bsc_configure.Application.Katana),
            (cls.get_is_clarisse, bsc_configure.Application.Clarisse),
            (cls.get_is_lynxi, bsc_configure.Application.Lynxi)
        ]:
            if i_fnc() is True:
                return i_app
        return bsc_configure.Application.Python
    @classmethod
    def test(cls):
        subprocess.check_output(
            ['', '-v'], shell=True
        ).strip()


class TimeMtd(object):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    #
    TIME_TAG_FORMAT = '%Y_%m%d_%H%M_%S_%f'
    DATA_TAG_FORMAT = '%Y_%m%d'
    @classmethod
    def get_time(cls):
        timestamp = time.time()
        return time.strftime(
            cls.TIME_FORMAT,
            time.localtime(timestamp)
        )
    @classmethod
    def get_timestamp(cls):
        return time.time()
    @classmethod
    def get_year(cls):
        return time.localtime().tm_year
    @classmethod
    def get_minute(cls):
        return time.localtime().tm_min
    @classmethod
    def get_second(cls):
        return time.localtime().tm_sec
    #
    @classmethod
    def get_time_tag(cls):
        return datetime.datetime.now().strftime(
            cls.TIME_TAG_FORMAT
        )
    @classmethod
    def get_date_tag(cls):
        timestamp = time.time()
        return time.strftime(
            cls.DATA_TAG_FORMAT,
            time.localtime(timestamp)
        )


class SystemMtd(TimeMtd):
    Platform = bsc_configure.Platform
    Application = bsc_configure.Application
    @classmethod
    def get_host(cls):
        return socket.gethostname()
    @classmethod
    def get_user_name(cls):
        return getpass.getuser()
    @staticmethod
    def get_is_linux():
        return platform.system() == 'Linux'
    @staticmethod
    def get_is_windows():
        return platform.system() == 'Windows'
    @staticmethod
    def get_platform():
        if platform.system() == 'Windows':
            return 'windows'
        elif platform.system() == 'Linux':
            return 'linux'
    #
    @classmethod
    def get_application(cls):
        return ApplicationMtd.get_current()
    #
    @classmethod
    def get_home_directory(cls):
        if cls.get_is_windows():
            return os.environ.get('HOMEPATH')
        elif cls.get_is_linux():
            return os.environ.get('HOME')
        else:
            raise SystemError()
    #
    @classmethod
    def get_system_includes(cls, system_keys):
        lis = []
        for i_system_key in system_keys:
            i_results = fnmatch.filter(
                bsc_configure.System.All, i_system_key
            ) or []
            for j_system in i_results:
                if j_system not in lis:
                    lis.append(j_system)
        return lis
    @classmethod
    def get_current(cls):
        return '{}-{}'.format(
            cls.get_platform(),
            cls.get_application()
        )
    @classmethod
    def get_is_matched(cls, system_keys):
        return cls.get_current() in cls.get_system_includes(system_keys)
    #
    @classmethod
    def get(cls, key):
        dic = {
            'user': cls.get_user_name,
            'host': cls.get_host,
            'time_tag': TimeMtd.get_time_tag
        }
        if key in dic:
            return dic[key]()
    @classmethod
    def get_group_id(cls, group_name):
        import grp
        return grp.getgrnam(group_name).gr_gid
    @classmethod
    def trace(cls, text):
        return sys.stdout.write(text+'\n')
    @classmethod
    def trace_error(cls, text):
        return sys.stderr.write(text+'\n')


class StorageMtd(object):
    PATHSEP = '/'
    @classmethod
    def get_path_is_windows(cls, path):
        return fnmatch.filter([path.lower()], '[a-zA-Z]:*') != []
    @classmethod
    def get_path_is_linux(cls, path):
        return fnmatch.filter([path.lower()], '/*') != []
    @classmethod
    def get_root(cls, path):
        if cls.get_path_is_windows(path):
            return path.split(cls.PATHSEP)[0]
        elif cls.get_path_is_linux(path):
            return cls.PATHSEP
    @classmethod
    def set_map_to_platform(cls, path):
        if path is not None:
            if SystemMtd.get_is_windows():
                return cls.set_map_to_windows(path)
            elif SystemMtd.get_is_linux():
                return cls.set_map_to_linux(path)
            return cls.set_pathsep_cleanup(path)
        return path
    @classmethod
    def set_map_to_nas(cls, path):
        path = cls.set_pathsep_cleanup(path)
        if StorageMtd.get_path_is_linux(path):
            src_root = path[:2]
            if src_root == '/l':
                _ = '/ifs/data/cgdata' + path[len(src_root):]
                return _
            elif src_root == '/t':
                _ = '/hwshare001' + path[len(src_root):]
                return _
            else:
                return path
    @classmethod
    def set_map_to_windows(cls, path):
        path = cls.set_pathsep_cleanup(path)
        if StorageMtd.get_path_is_linux(path):
            src_root = path[:2]
            src_root_name = src_root[-1]
            tgt_root = src_root_name + ':'
            _ = tgt_root + path[len(src_root):]
            return _
        return path
    @classmethod
    def set_map_to_linux(cls, path):
        path = cls.set_pathsep_cleanup(path)
        if StorageMtd.get_path_is_windows(path):
            src_root = path[:2]
            src_root_name = src_root[0]
            tgt_root = '/' + src_root_name.lower()
            _ = tgt_root + path[len(src_root):]
            return _
        return path
    @classmethod
    def set_pathsep_convert(cls, path):
        lis = []
        for i in path:
            i_r = repr(i)
            i_r_s = i_r.split("'")[1]
            i_r_s_c = len(i_r_s)
            if i_r_s_c == 1:
                lis.append(i)
            elif i_r_s_c == 2:
                if i_r_s == '\\\\':
                    lis.append('/')
                else:
                    lis.append('/' + i_r_s[-1])
            else:
                #
                if i_r_s in ['\\x07']:
                    lis.append('/a')
                elif i_r_s in ['\\x08']:
                    lis.append('/b')
                # hex
                elif i_r_s.startswith('\\x'):
                    hex_str = '0' + i_r_s[1:]
                    lis.append('/' + str(int(oct(int(hex_str, 16)))))
                # unicode
                elif i_r_s.startswith('\\u'):
                    lis.append(i_r_s)
        #
        return ''.join(lis).decode('unicode_escape')
    @classmethod
    def set_pathsep_cleanup(cls, path):
        path_ = cls.set_pathsep_convert(path)
        #
        _ = path_.split(cls.PATHSEP)
        new_path = cls.PATHSEP.join([i for i in _ if i])
        # etc: '/data/f/'
        if path_.endswith(cls.PATHSEP):
            new_path += '/'
        if path_.startswith(cls.PATHSEP):
            return cls.PATHSEP + new_path
        return new_path
    @classmethod
    def get_permission(cls, path):
        def get_str_fnc_(st_mode_):
            _mode_list = [
                #
                'd',
                # user
                # read, write, execute
                'r', 'w', 'x',
                # group
                'r', 'w', 'x',
                # other
                'r', 'w', 'x'
            ]
            print st_mode_
            _mode_b = bin(st_mode_)[-10:]
            _result = ''
            for _idx, _flg in enumerate(_mode_b):
                if _flg == '1':
                    _result += _mode_list[_idx]
                else:
                    _result += '-'
            return _result
        #
        if os.path.exists(path) is True:
            s = os.stat(path)
            return get_str_fnc_(s.st_mode)
    @classmethod
    def get_user(cls, path):
        # noinspection PyBroadException
        if os.path.exists(path) is True:
            s = os.stat(path)
            uid = s.st_uid
            if SystemMtd.get_is_linux():
                import pwd
                try:
                    user = pwd.getpwuid(uid)[0]
                    return user
                except KeyError:
                    return 'unknown'
        return 'unknown'
    @classmethod
    def get_group_name(cls, path):
        # noinspection PyBroadException
        if os.path.exists(path) is True:
            stat_info = os.stat(path)
            gid = stat_info.st_gid
            if SystemMtd.get_is_linux():
                import grp
                group_name = grp.getgrgid(gid)[0]
                return group_name
        return None
    @classmethod
    def create_directory(cls, directory_path):
        if os.path.isdir(directory_path) is False:
            os.makedirs(directory_path)
    @classmethod
    def get_relpath(cls, path_src, path_tgt):
        return os.path.relpath(path_src, path_tgt)
    @classmethod
    def get_is_exists(cls, path):
        return os.path.exists(path)
    @classmethod
    def get_file_realpath(cls, file_path_src, file_path_tgt):
        directory_path_src = os.path.dirname(file_path_src)
        return os.path.relpath(file_path_tgt, directory_path_src)
    @classmethod
    def get_is_readable(cls, path):
        return os.access(path, os.R_OK)
    @classmethod
    def get_is_writeable(cls, path):
        return os.access(path, os.W_OK)
    @classmethod
    def get_file_name_search_dict(cls, directory_paths):
        def rcs_fnc_(path_):
            _results = glob.glob(u'{}/*'.format(path_)) or []
            # _results.sort()
            for _i_path in _results:
                if os.path.isfile(_i_path):
                    _i_directory_path = os.path.dirname(_i_path)
                    _i_name = os.path.basename(_i_path)
                    _i_name_base, _i_ext = os.path.splitext(_i_name)
                    #
                    _i_name_base_key = _i_name_base
                    _i_ext_key = _i_ext
                    #
                    if _i_name_base_key in dict_:
                        _i_ext_search_dict = dict_[_i_name_base_key]
                    else:
                        _i_ext_search_dict = {}
                        dict_[_i_name_base_key] = _i_ext_search_dict
                    #
                    if _i_ext_key in _i_ext_search_dict:
                        _i_matches = _i_ext_search_dict[_i_ext_key]
                    else:
                        _i_matches = []
                        _i_ext_search_dict[_i_ext_key] = _i_matches
                    #
                    _i_matches.append(
                        (_i_directory_path, _i_name_base, _i_ext)
                    )
                elif os.path.isdir(_i_path):
                    rcs_fnc_(_i_path)

        dict_ = {}
        [rcs_fnc_(i) for i in directory_paths]
        return dict_
    @classmethod
    def get_file_args(cls, file_path):
        directory_path = os.path.dirname(file_path)
        base = os.path.basename(file_path)
        name_base, ext = os.path.splitext(base)
        return directory_path, name_base, ext
    @classmethod
    def to_file_deduplication_mapper(cls, file_paths):
        dict_ = {}
        for i_path in file_paths:
            i_path_base = os.path.splitext(i_path)[0]
            dict_[i_path_base] = i_path
        return dict_
    @classmethod
    def deduplication_files_by_formats(cls, file_paths, formats):
        list_ = []
        dict_ = {}
        set_ = set()
        for i_file_path in file_paths:
            i_path_base, i_ext = os.path.splitext(i_file_path)
            i_format = i_ext[1:]
            set_.add(i_format)
            dict_.setdefault(i_path_base, []).append(i_format)
        #
        fs = [i for i in formats]
        [fs.append(i) for i in set_ if i not in fs]
        #
        for k, v in dict_.items():
            v.sort(key=fs.index)
            list_.append('{}.{}'.format(k, v[0]))
        return list_


class HashMtd(object):
    @classmethod
    def get_pack_format(cls, max_value):
        o = 'q'
        if max_value < 128:
            o = 'b'
        elif max_value < 32768:
            o = 'h'
        elif max_value < 4294967296:
            o = 'i'
        return o
    @classmethod
    def get_hash_value(cls, raw, as_unique_id=False):
        s = hashlib.md5(
            str(raw)
        ).hexdigest()
        if as_unique_id is True:
            return UuidMtd.get_by_hash_value(s)
        return s.upper()
    @classmethod
    def get_hash_value_(cls, raw, as_unique_id=False):
        raw_str = str(raw)
        pack_array = [ord(i) for i in raw_str]
        #
        s = hashlib.md5(
            struct.pack('%s%s' % (len(pack_array), cls.get_pack_format(max(pack_array))), *pack_array)
        ).hexdigest()
        if as_unique_id is True:
            return UuidMtd.get_by_hash_value(s)
        return s.upper()


class UuidMtd(object):
    BASIC = '4908BDB4-911F-3DCE-904E-96E4792E75F1'
    VERSION = 3.0
    @classmethod
    def get_new(cls):
        return str(uuid.uuid1()).upper()
    @classmethod
    def get_by_string(cls, string):
        return str(uuid.uuid3(uuid.UUID(cls.BASIC), str(string))).upper()
    @classmethod
    def get_by_hash_value(cls, hash_value):
        return cls.get_by_string(hash_value)
    @classmethod
    def get_by_file(cls, file_path):
        check_file_path = StorageMtd.set_map_to_linux(file_path)
        if os.path.isfile(file_path):
            timestamp = os.stat(file_path).st_mtime
            size = os.path.getsize(file_path)
            f = check_file_path.encode('utf-8')
            return str(
                uuid.uuid3(
                    uuid.UUID(cls.BASIC),
                    'file={}&timestamp={}&size={}&version={}'.format(f, timestamp, size, cls.VERSION)
                )
            ).upper()
        return str(
            uuid.uuid3(
                uuid.UUID(cls.BASIC),
                'file={}&version={}'.format(file_path, cls.VERSION))
        ).upper()


class Bin(object):
    @classmethod
    def get_oiiotool(cls):
        if SystemMtd.get_is_windows():
            return '{}/windows/oiiotool.exe'.format(bsc_configure.Root.BIN)
        elif SystemMtd.get_is_linux():
            return '{}/linux/oiiotool'.format(bsc_configure.Root.BIN)
    @classmethod
    def get_oslinfo(cls):
        if SystemMtd.get_is_windows():
            return '{}/windows/oslinfo.exe'.format(bsc_configure.Root.BIN)
        elif SystemMtd.get_is_linux():
            return '{}/linux/oslinfo'.format(bsc_configure.Root.BIN)
    @classmethod
    def get_oslc(cls):
        if SystemMtd.get_is_windows():
            return '{}/windows/oslc.exe'.format(bsc_configure.Root.BIN)
        elif SystemMtd.get_is_linux():
            return '{}/linux/oslc'.format(bsc_configure.Root.BIN)
    @classmethod
    def get_ffmpeg(cls):
        if SystemMtd.get_is_windows():
            return 'l:/packages/pg/third_party/app/ffmpeg/4.4.0/platform-windows/bin/ffmpeg.exe'.format(bsc_configure.Root.BIN)
        elif SystemMtd.get_is_linux():
            return 'ffmpeg'.format(bsc_configure.Root.BIN)


class ExceptionMtd(object):
    @classmethod
    def set_print(cls):
        import traceback
        #
        traceback.print_exc()
    @classmethod
    def set_stack_print(cls):
        import sys
        #
        import traceback
        #
        exc_type, exc_value, exc_stack = sys.exc_info()
        exc_texts = []
        # value = '{}: "{}"'.format(exc_type.__name__, exc_value.message)
        for seq, stk in enumerate(traceback.extract_tb(exc_stack)):
            i_file_path, i_line, i_fnc, i_fnc_line = stk
            exc_texts.append(
                '    file "{}" line {} in {}\n        {}'.format(i_file_path, i_line, i_fnc, i_fnc_line)
            )
        if exc_texts:
            sys.stdout.write('\n'.join(exc_texts)+'\n')
    @classmethod
    def get_stack(cls):
        import sys
        #
        import traceback
        #
        exc_type, exc_value, exc_stack = sys.exc_info()
        exc_texts = []
        # value = '{}: "{}"'.format(exc_type.__name__, exc_value.message)
        for seq, stk in enumerate(traceback.extract_tb(exc_stack)):
            i_file_path, i_line, i_fnc, i_fnc_line = stk
            exc_texts.append(
                u'    file "{}" line {} in {}\n        {}'.format(i_file_path, i_line, i_fnc, i_fnc_line)
            )
        return '\n'.join(exc_texts)
    @classmethod
    def get_stack_(cls):
        import sys
        #
        import traceback

        exc_texts = []
        exc_type, exc_value, exc_stack = sys.exc_info()
        if exc_type:
            value = '{}: "{}"'.format(exc_type.__name__, exc_value.message)
            for seq, stk in enumerate(traceback.extract_tb(exc_stack)):
                i_file_path, i_line, i_fnc, i_fnc_line = stk
                exc_texts.append(
                    '{indent}file "{file}" line {line} in {fnc}\n{indent}{indent}{fnc_line}'.format(
                        **dict(
                            indent='    ',
                            file=i_file_path,
                            line=i_line,
                            fnc=i_fnc,
                            fnc_line=i_fnc_line
                        )
                    )
                )
            #
            exc_texts.append(value)
        return '\n'.join(exc_texts)


class CameraMtd(object):
    @classmethod
    def get_front_transformation(cls, geometry_args, angle, mode=0):
        _, (c_x, c_y, c_z), (w, h, d) = geometry_args

        if mode == 1:
            r = max(w, h)
        else:
            r = max(w, h)

        z_1 = r / math.tan(math.radians(angle))
        t_x, t_y, t_z = (c_x, c_y, z_1 - c_z)

        r_x, r_y, r_z = 0, 0, 0
        s_x, s_y, s_z = 1, 1, 1
        return (t_x, t_y, t_z), (r_x, r_y, r_z), (s_x, s_y, s_z)
    @classmethod
    def get_project_pos(cls, size, scale_percent, margin_percent, camera_fov, camera_screen_mode, render_resolution):
        # s = 1, x = y = -0
        # s = .5, x = y = -.25
        # s = .25, x = y = -.375
        # x = y = -(0.5 - s/2)
        # a/b=tan(camera_fov/2)
        b = (size/2)/math.tan(math.radians(camera_fov/2))
        x, y = 1, 1
        w, h = render_resolution
        if camera_screen_mode == 'horizontal':
            x, y = 1, h/w
        elif camera_screen_mode == 'vertical':
            x, y = w/h, 1
        s_s = min(x, y)
        s = scale_percent*s_s
        t_x, t_y, t_z = -(0.5*x-s/2)+margin_percent, -(0.5*y-s/2)+margin_percent, -b
        s_x, s_y, s_z = s, s, s
        return (t_x, t_y, t_z), (s_x, s_y, s_z)


HEXDIG = '0123456789ABCDEFabcdef'
HEXTOCHR = dict((a + b, chr(int(a + b, 16))) for a in HEXDIG for b in HEXDIG)


class SPathMtd(object):
    """
    from urllib quote and unquote
    """
    ALWAYS_SAFE = (
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        'abcdefghijklmnopqrstuvwxyz'
        '0123456789'
    )
    SAFE_MAP = {}
    SAFE_QUOTERS = {}
    for i, c in zip(xrange(256), str(bytearray(xrange(256)))):
        SAFE_MAP[c] = c if (i < 128 and c in ALWAYS_SAFE) else '%{:02X}'.format(i)
    #
    RE_ASCII = re.compile('([\x00-\x7f]+)')
    @classmethod
    def set_quote_to(cls, s, safe=''):
        # fastpath
        if not s:
            if s is None:
                raise TypeError('None object cannot be quoted')
            return s
        cache_key = (safe, cls.ALWAYS_SAFE)
        try:
            (quoter, safe) = cls.SAFE_QUOTERS[cache_key]
        except KeyError:
            safe_map = cls.SAFE_MAP.copy()
            safe_map.update([(c, c) for c in safe])
            quoter = safe_map.__getitem__
            safe = cls.ALWAYS_SAFE + safe
            cls.SAFE_QUOTERS[cache_key] = (quoter, safe)
        if not s.rstrip(safe):
            return s
        return ''.join(map(quoter, s))
    @classmethod
    def _get_is_unicode(cls, x):
        return isinstance(x, unicode)
    @classmethod
    def set_unquote_to(cls, s):
        """unquote('abc%20def') -> 'abc def'."""
        if cls._get_is_unicode(s):
            if '%' not in s:
                return s
            bits = cls.RE_ASCII.split(s)
            res = [bits[0]]
            append = res.append
            for i in range(1, len(bits), 2):
                append(cls.set_unquote_to(str(bits[i])).decode('latin1'))
                append(bits[i + 1])
            return ''.join(res)

        bits = s.split('%')
        # fastpath
        if len(bits) == 1:
            return s
        res = [bits[0]]
        append = res.append
        for item in bits[1:]:
            try:
                append(HEXTOCHR[item[:2]])
                append(item[2:])
            except KeyError:
                append('%')
                append(item)
        return ''.join(res)


if __name__ == '__main__':
    print UuidMtd.get_new()