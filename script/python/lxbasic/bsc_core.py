# coding:utf-8
import sys

import os

import collections

import yaml

import json

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

from lxbasic import bsc_configure

import shutil

THREAD_MAXIMUM = threading.Semaphore(1024)


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


class OrderedYamlMtd(object):
    @classmethod
    def set_dump(cls, raw, stream=None, Dumper=yaml.SafeDumper, object_pairs_hook=collections.OrderedDict, **kwargs):
        class _Cls(Dumper):
            pass
        # noinspection PyUnresolvedReferences
        def _fnc(dumper_, data_):
            return dumper_.represent_mapping(
                yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                data_.items(),
            )

        _Cls.add_representer(object_pairs_hook, _fnc)
        return yaml.dump(raw, stream, _Cls, **kwargs)
    @classmethod
    def set_load(cls, stream, Loader=yaml.SafeLoader, object_pairs_hook=collections.OrderedDict):
        class _Cls(Loader):
            pass
        # noinspection PyArgumentList
        def _fnc(loader_, node_):
            loader_.flatten_mapping(node_)
            return object_pairs_hook(loader_.construct_pairs(node_))
        # noinspection PyUnresolvedReferences
        _Cls.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _fnc)
        return yaml.load(stream, _Cls)


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
    def get_is_dcc(cls):
        for i_fnc in [
            cls.get_is_maya,
            cls.get_is_houdini,
            cls.get_is_katana,
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


class SystemMtd(object):
    TIME_FORMAT = u'%Y-%m-%d %H:%M:%S'
    TIME_TAG_FORMAT = u'%Y_%m%d_%H%M_%S_%f'
    DATA_TAG_FORMAT = u'%Y_%m%d'
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
    @classmethod
    def get_application(cls):
        return ApplicationMtd.get_current()
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
    def get_minute(cls):
        return time.localtime().tm_min
    @classmethod
    def get_second(cls):
        return time.localtime().tm_sec
    @classmethod
    def get_time_tag(cls):
        return datetime.datetime.now().strftime(cls.TIME_TAG_FORMAT)
    @classmethod
    def get_batch_tag(cls):
        pass
    @classmethod
    def get_date_tag(cls):
        timestamp = time.time()
        return time.strftime(
            cls.DATA_TAG_FORMAT,
            time.localtime(timestamp)
        )
    @classmethod
    def set_directory_open(cls, path):
        if cls.get_is_windows():
            cmd = u'explorer "{}"'.format(path.replace('/', '\\'))
            # subprocess.Popen(cmd, shell=True)
        elif cls.get_is_linux():
            cmd = u'nautilus "{}"'.format(path)
            # subprocess.Popen(cmd, shell=True)
        else:
            raise SystemError()

        t_0 = threading.Thread(
            target=functools.partial(SubProcessMtd.set_run_with_result, cmd)
        )
        t_0.start()
    @classmethod
    def set_file_open(cls, path):
        if cls.get_is_windows():
            cmd = u'explorer /select,"{}"'.format(path.replace('/', '\\'))
            # subprocess.Popen(cmd, shell=True)

        elif cls.get_is_linux():
            cmd = u'nautilus "{}" --select'.format(path)
            # subprocess.Popen(cmd, shell=True)
        else:
            raise SystemError()

        t_0 = threading.Thread(
            target=functools.partial(SubProcessMtd.set_run_with_result, cmd)
        )
        t_0.start()
    @classmethod
    def get_user_directory_path(cls):
        if cls.get_is_windows():
            return os.environ.get('HOMEPATH')
        elif cls.get_is_linux():
            return os.environ.get('HOME')
        else:
            raise SystemError()
    #
    @classmethod
    def get_temporary_directory_path(cls, create=False):
        date_tag = cls.get_date_tag()
        if cls.get_is_windows():
            _ = '{}/temporary/{}'.format(bsc_configure.UserDirectory.WINDOWS, date_tag)
        elif cls.get_is_linux():
            _ = '{}/temporary/{}'.format(bsc_configure.UserDirectory.LINUX, date_tag)
        else:
            raise SystemError()
        if create:
            StoragePathMtd.set_directory_create(_)
        return _
    @classmethod
    def get_debug_directory_path(cls, tag=None, create=False):
        date_tag = cls.get_date_tag()
        if cls.get_is_windows():
            root = bsc_configure.UserDirectory.WINDOWS
            _ = '{}/debug/{}'.format(root, date_tag)
        elif cls.get_is_linux():
            _ = '{}/debug/{}'.format(bsc_configure.UserDirectory.LINUX, date_tag)
        else:
            raise SystemError()
        if tag is not None:
            _ = '{}/{}'.format(_, tag)
        if create:
            StoragePathMtd.set_directory_create(_)
        return _
    @classmethod
    def get_temporary_file_path(cls, ext):
        directory_path = cls.get_temporary_directory_path()
        return '{}/{}{}'.format(directory_path, UuidMtd.get_new(), ext)
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
    def get_user_session_directory_path(cls, create=False):
        date_tag = cls.get_date_tag()
        if cls.get_is_windows():
            _ = '{}/.session/{}'.format(bsc_configure.UserDirectory.WINDOWS, date_tag)
        elif cls.get_is_linux():
            _ = '{}/.session/{}'.format(bsc_configure.UserDirectory.LINUX, date_tag)
        else:
            raise SystemError()
        if create:
            StoragePathMtd.set_directory_create(_)
        return _
    @classmethod
    def get_user_session_file_path(cls, unique_id=None):
        directory_path = cls.get_user_session_directory_path()
        if unique_id is None:
            unique_id = UuidMtd.get_new()
        return '{}/{}.yml'.format(directory_path, unique_id)
    #
    GAIN_DICT = {
        'user': get_user_name,
        'time_tag': get_time_tag
    }
    #
    @classmethod
    def get(cls, key):
        dic = {
            'user': cls.get_user_name,
            'time_tag': cls.get_time_tag
        }
        if key in dic:
            return dic[key]()


class StoragePathMtd(object):
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
        if StoragePathMtd.get_path_is_linux(path):
            src_root = path[:2]
            _ = '/ifs/data/cgdata' + path[len(src_root):]
            return _
    @classmethod
    def set_map_to_windows(cls, path):
        path = cls.set_pathsep_cleanup(path)
        if StoragePathMtd.get_path_is_linux(path):
            src_root = path[:2]
            src_root_name = src_root[-1]
            tgt_root = src_root_name + ':'
            _ = tgt_root + path[len(src_root):]
            return _
        return path
    @classmethod
    def set_map_to_linux(cls, path):
        path = cls.set_pathsep_cleanup(path)
        if StoragePathMtd.get_path_is_windows(path):
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
            _mode_list = ['d', 'r', 'w', 'x', 'r', 'w', 'x', 'r', 'w', 'x']
            _mode_str = bin(st_mode_)[-10:]
            _result = ''
            for _idx, _flg in enumerate(_mode_str):
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
                user = pwd.getpwuid(uid)[0]
                return user
        return None
    @classmethod
    def get_group(cls, path):
        # noinspection PyBroadException
        if os.path.exists(path) is True:
            stat_info = os.stat(path)
            gid = stat_info.st_gid
            if SystemMtd.get_is_linux():
                import grp
                group = grp.getgrgid(gid)[0]
                return group
        return None
    @classmethod
    def set_directory_create(cls, directory_path):
        if os.path.isdir(directory_path) is False:
            os.makedirs(directory_path)
    @classmethod
    def get_relpath(cls, src_path, tgt_path):
        return os.path.relpath(src_path, tgt_path)
    @classmethod
    def get_path_is_exists(cls, path):
        return os.path.exists(path)
    @classmethod
    def get_file_realpath(cls, file_path_src, file_path_tgt):
        directory_path_src = os.path.dirname(file_path_src)
        return os.path.relpath(file_path_tgt, directory_path_src)


class StorageLinkMtd(object):
    @classmethod
    def set_link_to(cls, src_path, tgt_path):
        if os.path.exists(tgt_path) is False:
            tgt_dir_path = os.path.dirname(tgt_path)
            src_rel_path = os.path.relpath(src_path, tgt_dir_path)
            os.symlink(src_rel_path, tgt_path)
    @classmethod
    def get_is_link_source_to(cls, src_path, tgt_path):
        tgt_dir_path = os.path.dirname(tgt_path)
        src_rel_path = os.path.relpath(src_path, tgt_dir_path)
        if os.path.islink(tgt_path):
            orig_src_rel_path = os.readlink(tgt_path)
            return src_rel_path == orig_src_rel_path
        return False
    @classmethod
    def get_rel_path(cls, src_path, tgt_path):
        tgt_dir_path = os.path.dirname(tgt_path)
        return os.path.relpath(src_path, tgt_dir_path)


class StoragePathOpt(object):
    PATHSEP = '/'
    def __init__(self, path, cleanup=True):
        if cleanup is True:
            self._path = StoragePathMtd.set_pathsep_cleanup(path)
        else:
            self._path = path
        #
        if self.get_is_windows():
            self._root = self._path.split(self.PATHSEP)[0]
        elif self.get_is_linux():
            self._root = self.PATHSEP
        else:
            self._root = '/'

    def get_path(self):
        return self._path
    path = property(get_path)

    def get_root(self):
        return self._root
    root = property(get_root)
    @property
    def normcase_root(self):
        return os.path.normcase(self._root)
    @property
    def normcase_path(self):
        return os.path.normcase(self._path)

    def get_is_windows(self):
        return StoragePathMtd.get_path_is_windows(self.path)

    def get_is_linux(self):
        return StoragePathMtd.get_path_is_linux(self.path)

    def get_is_exists(self):
        return os.path.exists(self.path)

    def get_is_directory(self):
        return os.path.isdir(self.path)

    def get_is_file(self):
        return os.path.isfile(self.path)

    def set_open_in_system(self):
        if self.get_is_exists():
            if self.get_is_directory():
                SystemMtd.set_directory_open(self.path)
            elif self.get_is_file():
                SystemMtd.set_file_open(self.path)

    def get_modify_timestamp(self):
        return os.stat(self._path).st_mtime

    def get_access_timestamp(self):
        return os.stat(self._path).st_atime

    def get_is_same_timestamp_to(self, file_path):
        return str(self.get_modify_timestamp()) == str(self.__class__(file_path).get_modify_timestamp())

    def __str__(self):
        return self._path


class MultiplyPatternMtd(object):
    RE_UDIM_KEYS = [
        (r'<udim>', r'{}', 4),
    ]
    #
    RE_SEQUENCE_KEYS = [
        (r'#', r'{}', -1),
        # houdini
        (r'$F', r'\{}[^\d]', 4),
    ]
    # houdini
    for i in range(4):
        RE_SEQUENCE_KEYS.append(
            (r'$F0{}'.format(i+1), r'\{}', i+1)
        )
    # katana
    for i in range(4):
        RE_SEQUENCE_KEYS.append(
            (r'%0{}d'.format(i+1), r'{}', i+1)
        )
    #
    RE_MULTIPLY_KEYS = RE_UDIM_KEYS + RE_SEQUENCE_KEYS
    @classmethod
    def to_fnmatch_style(cls, pattern):
        re_keys = cls.RE_MULTIPLY_KEYS
        #
        new_name_base = pattern
        for i_k, i_f, i_c in re_keys:
            results = re.findall(i_f.format(i_k), pattern, re.IGNORECASE) or []
            if results:
                if i_c == -1:
                    i_count = len(results)
                    i_key = i_count * i_k
                else:
                    i_count = i_c
                    i_key = i_k
                #
                new_name_base = new_name_base.replace(i_key, '[0-9]'*i_count, 1)
        return new_name_base
    @classmethod
    def get_args(cls, pattern):
        re_keys = cls.RE_MULTIPLY_KEYS
        #
        key_args = []
        for i_k, i_f, i_c in re_keys:
            results = re.findall(i_f.format(i_k), pattern, re.IGNORECASE) or []
            if results:
                if i_c == -1:
                    i_count = len(results)
                    i_key = i_count * i_k
                else:
                    i_count = i_c
                    i_key = i_k
                #
                key_args.append(
                    (i_key, i_count)
                )
        return key_args
    @classmethod
    def get_is_valid(cls, pattern):
        re_keys = cls.RE_MULTIPLY_KEYS
        #
        for i_k, i_f, i_c in re_keys:
            results = re.findall(i_f.format(i_k), pattern, re.IGNORECASE) or []
            if results:
                return True
        return False


class FnmatchPatternMtd(object):
    @classmethod
    def to_re_style(cls, pattern):
        pattern_ = pattern
        args = MultiplyPatternMtd.get_args(pattern)
        for i, (i_key, i_count) in enumerate(args):
            pattern_ = pattern_.replace(
                i_key, r'[PATTERN-PLACEHOLDER-{}]'.format(i), 1
            )
        #
        re_pattern_ = fnmatch.translate(pattern_)
        for i, (i_key, i_count) in enumerate(args):
            re_pattern_ = re_pattern_.replace(
                r'[PATTERN-PLACEHOLDER-{}]'.format(i),
                r'(\d{{{}}})'.format(i_count)
            )
        return re_pattern_


class MultiplyFileNameMtd(object):
    @classmethod
    def get_match_args(cls, file_name, name_pattern):
        new_file_name = file_name
        args = MultiplyPatternMtd.get_args(
            name_pattern
        )
        re_pattern = FnmatchPatternMtd.to_re_style(name_pattern)
        numbers = re.findall(re_pattern, file_name)
        if numbers:
            if len(args) > 1:
                numbers = numbers[0]
            #
            for i, (i_key, i_count) in enumerate(args):
                new_file_name = new_file_name.replace(
                    numbers[i], i_key, 1
                )
            return new_file_name, map(int, numbers)


class DirectoryMtd(object):
    @classmethod
    def get_all_file_paths(cls, directory_path):
        def rcs_glob_fnc_(path_):
            _results = glob.glob(u'{}/*'.format(path_)) or []
            _results.sort()
            for _i_path in _results:
                if os.path.isfile(_i_path):
                    lis.append(_i_path)
                elif os.path.isdir(_i_path):
                    rcs_glob_fnc_(_i_path)
        #
        def rcs_os_fnc_(path_):
            _results = os.listdir(path_) or []
            _results.sort()
            for _i_name in _results:
                _i_path = '{}/{}'.format(path_, _i_name)
                if os.path.isfile(_i_path):
                    lis.append(_i_path)
                elif os.path.isdir(_i_path):
                    rcs_os_fnc_(_i_path)

        lis = []
        rcs_os_fnc_(directory_path)
        return lis
    @classmethod
    def get_file_relative_path(cls, directory_path, file_path):
        return os.path.relpath(file_path, directory_path)
    @classmethod
    def set_copy_to(cls, src_directory_path, tgt_directory_path):
        def copy_fnc_(src_file_path_, tgt_file_path_):
            shutil.copy2(src_file_path_, tgt_file_path_)
        #
        src_directory_path = src_directory_path
        file_paths = cls.get_all_file_paths(src_directory_path)
        #
        threads = []
        for i_src_file_path in file_paths:
            i_local_file_path = i_src_file_path[len(src_directory_path):]
            #
            i_tgt_file_path = tgt_directory_path + i_local_file_path
            if os.path.exists(i_tgt_file_path) is False:
                i_tgt_dir_path = os.path.dirname(i_tgt_file_path)
                if os.path.exists(i_tgt_dir_path) is False:
                    os.makedirs(i_tgt_dir_path)
                #
                i_thread = PyThread(
                    copy_fnc_, i_src_file_path, i_tgt_file_path
                )
                threads.append(i_thread)
                i_thread.start()
        #
        [i.join() for i in threads]


class MultiplyDirectoryMtd(object):
    @classmethod
    def get_all_multiply_file_dict(cls, directory_path, name_pattern):
        dic = collections.OrderedDict()
        _ = DirectoryMtd.get_all_file_paths(directory_path)
        for i_file_path in _:
            i_opt = StorageFileOpt(i_file_path)
            i_match_args = MultiplyFileNameMtd.get_match_args(
                i_opt.name, name_pattern
            )
            if i_match_args:
                i_pattern, i_numbers = i_match_args
                if len(i_numbers) == 1:
                    i_relative_path_dir_path = DirectoryMtd.get_file_relative_path(
                        directory_path, i_opt.directory_path
                    )
                    i_key = '{}/{}'.format(
                        i_relative_path_dir_path, i_pattern
                    )
                    dic.setdefault(
                        i_key, []
                    ).append(i_numbers[0])
        return dic


class EnvironMtd(object):
    TD_ENABLE_KEY = 'LYNXI_TD_ENABLE'
    DATA_PATH_KEY = 'LYNXI_DATA_PATH'
    #
    TEMPORARY_ROOT_KEY = 'LYNXI_TEMPORARY_ROOT'
    TEMPORARY_ROOT_DEFAULT = '/l/resource/temporary/.lynxi'
    #
    DATABASE_PATH_KEY = 'LYNXI_DATABASE_PATH'
    DATABASE_PATH_DEFAULT = '/l/resource/database/.lynxi'
    #
    SESSION_ROOT_KEY = 'LYNXI_SESSION_ROOT'
    SESSION_ROOT_DEFAULT = '/l/resource/temporary/.lynxi'
    #
    TRUE = 'true'
    FALSE = 'false'
    @classmethod
    def get_td_enable(cls):
        _ = cls.get(cls.TD_ENABLE_KEY)
        if _ == cls.TRUE:
            return True
        return False
    @classmethod
    def set_td_enable(cls, boolean):
        if boolean is True:
            cls.set(cls.TD_ENABLE_KEY, cls.TRUE)
        else:
            cls.set(cls.TD_ENABLE_KEY, cls.FALSE)
    @classmethod
    def get_temporary_root(cls):
        _ = cls.get(cls.TEMPORARY_ROOT_KEY)
        if _ is not None:
            return StoragePathMtd.set_map_to_platform(_)
        return StoragePathMtd.set_map_to_platform(cls.TEMPORARY_ROOT_DEFAULT)
    @classmethod
    def set_temporary_path(cls, path):
        cls.set(cls.TEMPORARY_ROOT_KEY, path)
    @classmethod
    def get_session_root(cls):
        _ = cls.get(cls.SESSION_ROOT_KEY)
        if _ is not None:
            return StoragePathMtd.set_map_to_platform(_)
        return StoragePathMtd.set_map_to_platform(cls.SESSION_ROOT_DEFAULT)
    @classmethod
    def get_database_path(cls):
        _ = cls.get(cls.DATABASE_PATH_KEY)
        if _ is not None:
            return StoragePathMtd.set_map_to_platform(_)
        return StoragePathMtd.set_map_to_platform(cls.DATABASE_PATH_DEFAULT)
    @classmethod
    def get_data_paths(cls):
        pass
    @classmethod
    def get(cls, key):
        return os.environ.get(key)
    @classmethod
    def set(cls, key, value):
        os.environ[key] = value
    @classmethod
    def set_add(cls, key, value):
        if key in os.environ:
            v = os.environ[key]
            if value not in v:
                os.environ[key] += os.pathsep + value
        else:
            os.environ[key] = value
    @classmethod
    def set_python_add(cls, path):
        python_paths = sys.path
        if path not in python_paths:
            sys.path.insert(0, path)


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
    @classmethod
    def get_save_region(cls, raw):
        _ = cls.get_hash_value(raw)
        return IntegerOpt(int(int(_, 16) / math.pow(2, 16))).set_encode_to_36()


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
    def get_by_file_path(cls, file_path):
        check_file_path = StoragePathMtd.set_map_to_linux(file_path)
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
    @classmethod
    def get_save_region(cls, unique_id):
        number = abs(uuid.UUID(unique_id).int)
        return IntegerOpt(number % 4096).set_encode_to_36()


class DatabaseMtd(object):
    @classmethod
    def get_key(cls, data):
        return HashMtd.get_hash_value(
            data, as_unique_id=True
        )
    @classmethod
    def _get_file_path_(cls, key, category):
        directory_path = EnvironMtd.get_database_path()
        region = UuidMtd.get_save_region(key)
        return '{}/{}/{}/{}'.format(directory_path, category, region, key)
    @classmethod
    def get_value(cls, key, category):
        file_path = cls._get_file_path_(key, category)
        gzip_file = GzipStorageFileOpt(file_path, '.yml')
        if gzip_file.get_is_exists() is True:
            return gzip_file.set_read()
    @classmethod
    def set_value(cls, key, value, force, category):
        file_path = cls._get_file_path_(key, category)
        gzip_file = GzipStorageFileOpt(file_path, '.yml')
        if gzip_file.get_is_exists() is False or force is True:
            gzip_file.set_write(value)
            return True


class DatabaseGeometryUvMapMtd(object):
    @classmethod
    def get_value(cls, key):
        return DatabaseMtd.get_value(
            key,
            category='geometry/uv-map'
        )
    @classmethod
    def set_value(cls, key, value, force):
        return DatabaseMtd.set_value(
            key,
            value,
            force,
            category='geometry/uv-map'
        )


class TemporaryThumbnailMtd(object):
    @classmethod
    def get_key(cls, file_path):
        return UuidMtd.get_by_file_path(file_path)
    @classmethod
    def get_file_path(cls, file_path, ext='.jpg'):
        directory_path = EnvironMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = UuidMtd.get_save_region(key)
        return '{}/.thumbnail/{}/{}{}'.format(
            directory_path, region, key, ext
        )


class TemporaryYamlMtd(object):
    @classmethod
    def get_key(cls, file_path):
        return UuidMtd.get_by_file_path(file_path)
    @classmethod
    def get_file_path(cls, file_path, tag):
        directory_path = EnvironMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = UuidMtd.get_save_region(key)
        return '{}/.yml/{}/{}/{}{}'.format(
            directory_path, tag, region, key, '.yml'
        )


class SessionYamlMtd(object):
    @classmethod
    def get_key(cls, **kwargs):
        return UuidMtd.get_by_string(
            KeywordArgumentsMtd.to_string(**kwargs)
        )
    @classmethod
    def get_file_path(cls, **kwargs):
        directory_path = EnvironMtd.get_session_root()
        key = cls.get_key(**kwargs)
        region = UuidMtd.get_save_region(key)
        return '{}/.session/option-hook/{}/{}{}'.format(
            directory_path, region, key, '.yml'
        )


class SubProcessMtd(object):
    if platform.system().lower() == 'windows':
        # noinspection PyUnresolvedReferences
        NO_WINDOW = subprocess.STARTUPINFO()
        NO_WINDOW.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    else:
        NO_WINDOW = None
    #
    ENVIRON_MARK = os.environ
    #
    def __init__(self):
        pass
    @classmethod
    def set_run_with_result_in_windows(cls, cmd, clear_environ=False):
        # must reload, output error
        import sys
        reload(sys)
        if hasattr(sys, 'setdefaultencoding'):
            sys.setdefaultencoding('utf-8')
        #
        cmd = cmd.replace("&", "^&")
        #
        if clear_environ is True:
            s_p = subprocess.Popen(
                cmd,
                shell=True,
                # close_fds=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=cls.NO_WINDOW,
                # env=cls.ENVIRON_MARK
            )
        else:
            s_p = subprocess.Popen(
                cmd,
                shell=True,
                # close_fds=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=cls.NO_WINDOW,
            )
        #
        while True:
            next_line = s_p.stdout.readline()
            #
            return_line = next_line
            if return_line == '' and s_p.poll() is not None:
                break
            #
            return_line = return_line.decode('gbk', 'ignore')
            print(return_line.rstrip())
        #
        return_code = s_p.wait()
        if return_code:
            ExceptionMtd.set_stack_print()
            #
            raise subprocess.CalledProcessError(
                return_code, s_p
            )
        #
        s_p.stdout.close()
    @classmethod
    def set_run_with_result_in_linux(cls, cmd, clear_environ=False):
        # must reload, output error
        import sys
        reload(sys)
        if hasattr(sys, 'setdefaultencoding'):
            sys.setdefaultencoding('utf-8')
        #
        if clear_environ is True:
            s_p = subprocess.Popen(
                cmd,
                shell=True,
                # close_fds=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=cls.NO_WINDOW,
                # env=cls.ENVIRON_MARK
            )
        else:
            s_p = subprocess.Popen(
                cmd,
                shell=True,
                # close_fds=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=cls.NO_WINDOW
            )
        #
        while True:
            next_line = s_p.stdout.readline()
            #
            return_line = next_line
            if return_line == '' and s_p.poll() is not None:
                break
            #
            return_line = return_line.decode('utf-8', 'ignore')
            return_line = return_line.replace(u'\u2018', "'").replace(u'\u2019', "'")
            print(return_line.rstrip())
        #
        return_code = s_p.wait()
        if return_code:
            ExceptionMtd.set_stack_print()
            #
            raise subprocess.CalledProcessError(
                return_code, s_p
            )
        #
        s_p.stdout.close()
    @classmethod
    def set_run_with_result(cls, cmd, clear_environ=False):
        if SystemMtd.get_is_windows():
            cls.set_run_with_result_in_windows(cmd, clear_environ)
        elif SystemMtd.get_is_linux():
            cls.set_run_with_result_in_linux(cmd, clear_environ)
    @classmethod
    def set_run(cls, cmd):
        _sp = subprocess.Popen(
            cmd,
            shell=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            startupinfo=cls.NO_WINDOW,
        )
        return _sp
    @classmethod
    def set_run_with_result_use_thread(cls, cmd):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.set_run_with_result,
                cmd=cmd
            )
        )
        t_0.start()


class MultiProcessMtd(object):
    def set_run(self, cmd):
        pass


class KeywordArgumentsMtd(object):
    ARGUMENT_SEP = '&'
    @classmethod
    def to_string(cls, **kwargs):
        vars_ = []
        keys = kwargs.keys()
        keys.sort()
        for k in keys:
            v = kwargs[k]
            if isinstance(v, (tuple, list)):
                # must convert to str
                vars_.append('{}={}'.format(k, '+'.join(map(str, v))))
            else:
                vars_.append('{}={}'.format(k, v))
        return cls.ARGUMENT_SEP.join(vars_)


class KeywordArgumentsOpt(object):
    ARGUMENT_SEP = '&'
    def __init__(self, option, default_option=None):
        dic = collections.OrderedDict()
        if isinstance(default_option, (str, unicode)):
            self._set_update_by_string_(dic, default_option)
        elif isinstance(default_option, dict):
            dic.update(default_option)

        if isinstance(option, (str, unicode)):
            self._set_update_by_string_(dic, option)
        elif isinstance(option, dict):
            dic.update(option)
        else:
            raise TypeError()
        #
        self._option_dict = dic
        #
        self._string_dict = {
            'key': self.to_string()
        }
    @classmethod
    def _set_update_by_string_(cls, dic, option_string):
        ks = [i.lstrip().rstrip() for i in option_string.split(cls.ARGUMENT_SEP)]
        for k in ks:
            key, value = k.split('=')
            value = value.lstrip().rstrip()
            #
            value = cls._set_value_convert_by_string_(value)
            dic[key.lstrip().rstrip()] = value
    @classmethod
    def _set_value_convert_by_string_(cls, value_string):
        if isinstance(value_string, (str, unicode)):
            if value_string in ['None']:
                return None
            elif value_string in ['True', 'False']:
                return eval(value_string)
            elif value_string in ['true', 'false']:
                return [True, False][['true', 'false'].index(value_string)]
            elif value_string in ['()', '[]', '{}']:
                return eval(value_string)
            elif '+' in value_string:
                return value_string.split('+')
            else:
                return value_string

    def get_value(self):
        return self._option_dict
    value = property(get_value)

    def get(self, key, as_array=False):
        if key in self._option_dict:
            _ = self._option_dict[key]
            if as_array is True:
                if isinstance(_, list):
                    return _
                return [_]
            return self._option_dict[key]

    def pop(self, key):
        if key in self._option_dict:
            return self._option_dict.pop(
                key
            )

    def get_as(self, key, type_):
        pass

    def set(self, key, value):
        self._option_dict[key] = value

    def set_update(self, dic, override=True):
        if override is False:
            [dic.pop(k) for k in dic if k in self._option_dict]
        #
        self._option_dict.update(dic)

    def set_update_by_string(self, option):
        self._option_dict.update(
            self.__class__(option).get_value()
        )

    def get_key_is_exists(self, key):
        return key in self._option_dict

    def get_raw(self):
        return self._option_dict

    def to_option(self):
        return self.to_string()

    def to_string(self):
        return KeywordArgumentsMtd.to_string(
            **self._option_dict
        )

    def __str__(self):
        return json.dumps(
            self._option_dict,
            indent=4,
            skipkeys=True,
            sort_keys=True
        )


class ScriptArgumentsOpt(object):
    PATTERN = r'[\[](.*?)[\]]'
    def __init__(self, arguments):
        self._arguments = re.findall(re.compile(self.PATTERN, re.S), arguments) or []

    def get_value(self):
        return self._arguments
    value = property(get_value)


class _OrderedYaml(object):
    @classmethod
    def set_dump(cls, raw, stream=None, Dumper=yaml.SafeDumper, object_pairs_hook=collections.OrderedDict, **kwargs):
        class _Cls(Dumper):
            pass
        # noinspection PyUnresolvedReferences
        def _fnc(dumper_, data_):
            return dumper_.represent_mapping(
                yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                data_.items(),
            )
        #
        _Cls.add_representer(object_pairs_hook, _fnc)
        return yaml.dump(raw, stream, _Cls, **kwargs)
    @classmethod
    def set_load(cls, stream, Loader=yaml.SafeLoader, object_pairs_hook=collections.OrderedDict):
        class _Cls(Loader):
            pass
        # noinspection PyArgumentList
        def _fnc(loader_, node_):
            loader_.flatten_mapping(node_)
            return object_pairs_hook(loader_.construct_pairs(node_))
        # noinspection PyUnresolvedReferences
        _Cls.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _fnc)
        return yaml.load(stream, _Cls)


class StorageFileOpt(StoragePathOpt):
    def __init__(self, file_path, file_type=None):
        super(StorageFileOpt, self).__init__(file_path)
        self._file_type = file_type

    def get_directory_path(self):
        return os.path.dirname(self.path)
    directory_path = property(get_directory_path)

    def get_type(self):
        return self.ext
    type = property(get_type)
    @property
    def path_base(self):
        return os.path.splitext(self.path)[0]

    def get_name(self):
        return os.path.basename(self.path)
    name = property(get_name)
    @property
    def name_base(self):
        return os.path.splitext(os.path.basename(self.path))[0]

    def get_ext(self):
        if self._file_type is not None:
            return self._file_type
        return os.path.splitext(self.path)[-1]
    ext = property(get_ext)

    def get_is_match_name_pattern(self, name_pattern):
        _ = fnmatch.filter([self.name], name_pattern)
        if _:
            return True
        return False

    def set_write(self, raw):
        directory = os.path.dirname(self.path)
        if os.path.isdir(directory) is False:
            os.makedirs(directory)
        if self.ext in ['.json']:
            with open(self.path, 'w') as j:
                json.dump(
                    raw,
                    j,
                    indent=4
                )
        elif self.ext in ['.yml']:
            with open(self.path, 'w') as y:
                _OrderedYaml.set_dump(
                    raw,
                    y,
                    indent=4,
                    default_flow_style=False,
                )
        else:
            with open(self.path, 'w') as f:
                f.write(raw)

    def set_read(self):
        if os.path.exists(self.path):
            if self.get_ext() in ['.json']:
                with open(self.path) as j:
                    raw = json.load(j, object_pairs_hook=collections.OrderedDict)
                    j.close()
                    return raw
            elif self.get_ext() in ['.yml']:
                with open(self.path) as y:
                    raw = _OrderedYaml.set_load(y)
                    y.close()
                    return raw
            else:
                with open(self.path) as f:
                    raw = f.read()
                    f.close()
                    return raw


class GzipStorageFileOpt(StorageFileOpt):
    def __init__(self, *args, **kwargs):
        super(GzipStorageFileOpt, self).__init__(*args, **kwargs)

    def set_read(self):
        if self.get_is_file() is True:
            with gzip.GzipFile(
                    mode='rb',
                    fileobj=open(self.path, 'rb')
            ) as g:
                if self.get_ext() in ['.yml']:
                    raw = _OrderedYaml.set_load(g)
                    g.close()
                    return raw

    def set_write(self, raw):
        if os.path.isdir(self.directory_path) is False:
            os.makedirs(self.directory_path)
        # noinspection PyArgumentEqualDefault
        with gzip.GzipFile(
            filename=self.name + self.ext,
            mode='wb',
            compresslevel=9,
            fileobj=open(self.path, 'wb')
        ) as g:
            if self.get_ext() in ['.yml']:
                _OrderedYaml.set_dump(
                    raw,
                    g,
                    indent=4,
                    default_flow_style=False,
                )


class DirectoryOpt(object):
    def __init__(self, directory_path):
        self._path = directory_path

    def get_path(self):
        return self._path
    path = property(get_path)

    def set_open(self):
        if os.path.exists(self.path):
            if SystemMtd.get_is_windows():
                os.startfile(
                    self.path.replace(u'/', os.sep)
                )
            elif SystemMtd.get_is_linux():
                subprocess.Popen(
                    u'nautilus "{}" --select'.format(self.path),
                    shell=True
                )

    def get_is_exists(self):
        return os.path.exists(self.path)


class ZipFileOpt(StorageFileOpt):
    def __init__(self, file_path):
        self._file_path = file_path

    def get_path(self):
        return self._file_path
    path = property(get_path)

    def get_element_names(self):
        file_path = self.get_path()
        if self.get_is_exists() is True:
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path) as z:
                    return z.namelist()
        # else:
        #     from unrar import rarfile
        #     if rarfile.is_rarfile(file_path):
        #         with rarfile.RarFile(file_path) as r:
        #             return r.namelist()
        return []

    def set_element_extract_to(self, element_name, element_file_path):
        if self.get_is_exists() is True:
            if zipfile.is_zipfile(self.path):
                with zipfile.ZipFile(self.path) as z:
                    directory_path = os.path.dirname(element_file_path)
                    f = z.extract(element_name, directory_path)
                    os.rename(f, element_file_path)
        # else:
        #     from unrar import rarfile
        #     if rarfile.is_rarfile(self.path):
        #         with rarfile.RarFile(self.path) as r:
        #             directory_path = os.path.dirname(element_file_path)
        #             f = r.extract(element_name, directory_path)
        #             os.rename(f, element_file_path)


class TimestampOpt(object):
    TIME_FORMAT = u'%Y-%m-%d %H:%M:%S'
    TIME_TAG_FORMAT = u'%Y_%m%d_%H%M_%S'
    def __init__(self, timestamp):
        self._timestamp = timestamp
    @property
    def timestamp(self):
        return self._timestamp

    def get(self):
        return time.strftime(
            self.TIME_FORMAT,
            time.localtime(self._timestamp)
        )

    def get_as_tag(self):
        return time.strftime(
            self.TIME_TAG_FORMAT,
            time.localtime(self._timestamp)
        )


class TimestampMtd(object):
    @classmethod
    def to_string(cls, pattern, timestamp):
        return time.strftime(
            pattern,
            time.localtime(timestamp)
        )


class IntegerMtd(object):
    @classmethod
    def get_file_size_prettify(cls, value):
        string = value
        #
        dv = 1024
        lis = [(dv ** 4, 'T'), (dv ** 3, 'G'), (dv ** 2, 'M'), (dv ** 1, 'K')]
        #
        for i in lis:
            s = abs(value) / i[0]
            if s:
                string = str(round(float(value) / float(i[0]), 2)) + i[1]
                break
        #
        return str(string)
    @classmethod
    def get_prettify(cls, value):
        string = value
        #
        dv = 1000
        lis = [(dv ** 4, 'T'), (dv ** 3, 'B'), (dv ** 2, 'M'), (dv ** 1, 'K')]
        #
        if value >= dv:
            for i in lis:
                s = int(abs(value)) / i[0]
                if s:
                    string = str(round(float(value) / float(i[0]), 2)) + i[1]
                    break
        else:
            string = value
        #
        return str(string)
    @classmethod
    def get_prettify_(cls, value, mode):
        if mode == 0:
            return cls.get_prettify(value)
        else:
            return cls.get_file_size_prettify(value)
    @classmethod
    def byte_to_gb(cls, value):
        dv = 1024.0
        return float(value)/dv ** 3
    @classmethod
    def frame_to_time(cls, frame, fps=24):
        second = int(frame) / fps
        h = second / 3600
        m = second / 60 - 60 * h
        s = second - 3600 * h - 60 * m
        return h, m, s
    @classmethod
    def frame_to_time_prettify(cls, frame, fps=24):
        h, m, s = cls.frame_to_time(frame, fps)
        return '%s:%s:%s' % (str(h).zfill(2), str(m).zfill(2), str(s).zfill(2))
    @classmethod
    def second_to_time(cls, second):
        h = int(second/3600)
        m = int(second/60-60*h)
        s = int(second-3600*h-60*m)
        return h, m, s
    @classmethod
    def second_to_time_prettify(cls, second):
        h, m, s = cls.second_to_time(int(second))
        return '%s:%s:%s' % (str(h).zfill(2), str(m).zfill(2), str(s).zfill(2))
    @classmethod
    def second_to_minute(cls, second):
        dv = 60.0
        return float(second)/dv ** 1
    @classmethod
    def second_to_hours(cls, second):
        dv = 60.0
        return float(second)/dv ** 2
    @classmethod
    def microsecond_to_second(cls, microsecond):
        dv = 1000.0
        return float(microsecond) / dv ** 2
    @classmethod
    def microsecond_to_hours(cls, microsecond):
        return cls.second_to_hours(
            cls.microsecond_to_second(microsecond)
        )


class IntegerOpt(object):
    def __init__(self, raw):
        self._value = raw

    def set_encode_to_36(self):
        number = self._value
        num_str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if number == 0:
            return '0'

        base36 = []
        while number != 0:
            number, i = divmod(number, 36)
            base36.append(num_str[i])

        return ''.join(reversed(base36))


class TextMtd(object):
    def set_text_join(self):
        pass
    @classmethod
    def to_number_embedded_args(cls, string):
        pieces = re.compile(r'(\d+)').split(unicode(string))
        pieces[1::2] = map(int, pieces[1::2])
        return pieces
    @classmethod
    def to_glob_pattern(cls, string):
        return re.sub(r'(\d)', '[0-9]', string)


class DictMtd(object):
    @classmethod
    def get_as_json_style(cls, dict_):
        return json.dumps(
            dict_,
            indent=4,
            skipkeys=True,
            sort_keys=True
        )
    @classmethod
    def get_as_yaml_style(cls, dict_):
        return OrderedYamlMtd.set_dump(
            dict_,
            indent=4,
            default_flow_style=False
        )
    @classmethod
    def set_key_sort_to(cls, dict_):
        dic = collections.OrderedDict()
        keys = dict_.keys()
        keys.sort()
        for i_key in keys:
            dic[i_key] = dict_[i_key]
        return dic


class StrUnderlineOpt(object):
    def __init__(self, string):
        self._string = string

    def to_prettify(self, capitalize=True):
        if capitalize is True:
            return ' '.join([i.capitalize() for i in self._string.split('_')])
        return ' '.join([i.lower() for i in self._string.split('_')])

    def to_camelcase(self):
        return re.sub(r'_(\w)', lambda x: x.group(1).upper(), self._string)


class DccPathDagMtd(object):
    @classmethod
    def get_dag_args(cls, path, pathsep='/'):
        """
        :param path: str(<obj-path>)
        :param pathsep:
        :return: list[str(<obj-name>), ...]
        """
        if pathsep is None:
            raise TypeError()
        # is <root-obj>, etc: "/"
        if path == pathsep:
            return [pathsep, ]
        # is <obj>, etc: "/obj"
        return path.split(pathsep)
    @classmethod
    def get_dag_name(cls, path, pathsep='/'):
        """
        :param path:
        :param pathsep:
        :return:
        """
        # is <root-obj>, etc: "/"
        if path == pathsep:
            return pathsep
        # is <obj>, etc: "/obj"
        return cls.get_dag_args(path, pathsep)[-1]
    @classmethod
    def get_dag_parent(cls, path, pathsep='/'):
        """
        :param path:
        :param pathsep:
        :return:
        """
        dag_args = cls.get_dag_args(path, pathsep)
        # windows file-path-root etc: "D:/directory"
        if ':' in dag_args[0]:
            if len(dag_args) == 1:
                return None
            else:
                return pathsep.join(dag_args[:-1])
        else:
            if len(dag_args) == 1:
                return None
            elif len(dag_args) == 2:
                return pathsep
            else:
                return pathsep.join(dag_args[:-1])
    @classmethod
    def get_dag_component_paths(cls, path, pathsep='/'):
        """
        :param path:
        :param pathsep:
        :return: list[str(<obj-path>)]
        """
        def _rcs_fnc(lis_, path_):
            if path_ is not None:
                lis_.append(path_)
                _parent_path = cls.get_dag_parent(path_, pathsep)
                if _parent_path:
                    _rcs_fnc(lis_, _parent_path)

        lis = []
        _rcs_fnc(lis, path)
        return lis
    @classmethod
    def get_dag_name_with_namespace_clear(cls, name, namespacesep=':'):
        return name.split(namespacesep)[-1]
    @classmethod
    def get_dag_path_with_namespace_clear(cls, path, pathsep='/', namespacesep=':'):
        dag_args = cls.get_dag_args(path, pathsep)
        lis = []
        for i in dag_args:
            lis.append(cls.get_dag_name_with_namespace_clear(i, namespacesep))
        return cls.get_dag_path(lis, pathsep)
    @classmethod
    def get_dag_path_lstrip(cls, path, lstrip=None):
        if lstrip is not None:
            if path.startswith(lstrip):
                return path[len(lstrip):]
            elif lstrip.startswith(path):
                return ''
            return path
        return path
    @classmethod
    def get_dag_path(cls, dag_args, pathsep='/'):
        return pathsep.join(dag_args)
    @classmethod
    def get_dag_pathsep_replace(cls, path, pathsep_src='/', pathsep_tgt='/'):
        if path == pathsep_src:
            return pathsep_tgt
        return pathsep_tgt.join(cls.get_dag_args(path, pathsep=pathsep_src))
    @classmethod
    def get_dag_children(cls, path, paths, pathsep='/'):
        lis = []
        for i_path in paths:
            # r'/shl/chr/test_0/[^/]*'
            _ = re.match(
                r'{0}{1}[^{1}]*'.format(path, pathsep), i_path
            )
            if _ is not None:
                if _.group() == i_path:
                    lis.append(i_path)
        return lis


class DccPathDagOpt(object):
    def __init__(self, path):
        self._pathsep = path[0]
        self._path = path

    def get_name(self):
        return DccPathDagMtd.get_dag_name(
            path=self._path, pathsep=self._pathsep
        )
    name = property(get_name)

    def set_name(self, name):
        self._path = self._pathsep.join(
            [self.get_parent_path(), name]
        )

    def get_pathsep(self):
        return self._pathsep
    pathsep = property(get_pathsep)

    def get_path(self):
        return self._path
    path = property(get_path)

    def get_value(self):
        return self._path
    value = property(get_value)

    def get_root(self):
        return self.__class__(self.pathsep)

    def get_is_root(self):
        return self.path == self.pathsep

    def get_parent_path(self):
        return DccPathDagMtd.get_dag_parent(
            path=self._path, pathsep=self._pathsep
        )

    def set_parent_path(self, path):
        # noinspection PyAugmentAssignment
        self._path = path + self._path

    def get_ancestor_paths(self):
        return self.get_component_paths()[1:]

    def get_parent(self):
        _ = self.get_parent_path()
        if _:
            return self.__class__(
                self.get_parent_path()
            )

    def get_component_paths(self):
        return DccPathDagMtd.get_dag_component_paths(
            path=self._path, pathsep=self._pathsep
        )

    def get_components(self):
        return [self.__class__(i) for i in self.get_component_paths()]

    def set_translate_to(self, pathsep='/'):
        return self.__class__(
            DccPathDagMtd.get_dag_pathsep_replace(
                self.path,
                pathsep_src=self.pathsep,
                pathsep_tgt=pathsep
            )
        )

    def set_namespace_clear_to(self):
        return self.__class__(
            DccPathDagMtd.get_dag_path_with_namespace_clear(
                self.path,
                pathsep=self.pathsep,
                # namespacesep=':',
            )
        )

    def get_name_namespace(self, namespacesep=':'):
        name = self.get_name()
        _ = name.split(namespacesep)
        # print _
        return namespacesep.join(_[:-1])

    def __str__(self):
        return self._path

    def __repr__(self):
        return self.__str__()

    def to_string(self):
        return self._path


class AtrPathMtd(object):
    @classmethod
    def get_atr_path(cls, obj_path, port_path, port_pathsep='.'):
        return port_pathsep.join([obj_path, port_path])


class DccAttrPathOpt(object):
    def __init__(self, atr_path, port_pathsep='.'):
        self._path = atr_path
        self._port_pathsep = port_pathsep
        _ = self._path.split(self._port_pathsep)
        self._obj_path = _[0]
        self._port_path = self._port_pathsep.join(_[1:])
    @property
    def path(self):
        return self._path
    @property
    def obj_path(self):
        return self._obj_path
    @property
    def port_path(self):
        return self._port_path

    def to_args(self):
        return self._obj_path, self._port_path


class TextsMtd(object):
    @classmethod
    def set_sort_to(cls, texts):
        _ = texts
        _.sort(key=lambda x: TextMtd.to_number_embedded_args(x))
        return _


class ParsePatternMtd(object):
    RE_PATTERN = r'[{](.*?)[}]'
    @classmethod
    def get_keys(cls, pattern):
        lis_0 = re.findall(re.compile(cls.RE_PATTERN, re.S), pattern)
        lis_1 = list(set(lis_0))
        lis_1.sort(key=lis_0.index)
        return lis_1
    @classmethod
    def set_update(cls, pattern, **kwargs):
        if pattern is not None:
            keys = cls.get_keys(pattern)
            s = pattern
            if keys:
                for i_key in keys:
                    if i_key in kwargs:
                        v = kwargs[i_key]
                        if v is not None and v != '*':
                            s = s.replace('{{{}}}'.format(i_key), kwargs[i_key])
            return s
        return pattern


class TextsOpt(object):
    def __init__(self, raw):
        self._raw = raw

    def set_sort_to(self):
        _ = self._raw
        _.sort(key=lambda x: TextMtd.to_number_embedded_args(x))
        return _


class ColorMtd(object):
    @classmethod
    def rgb2hex(cls, r, g, b):
        return hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)
    @classmethod
    def hex2rgb(cls, hex_color, maximum=255):
        hex_color = int(hex_color, base=16) if isinstance(hex_color, str) else hex_color
        r, g, b = ((hex_color >> 16) & 0xff, (hex_color >> 8) & 0xff, hex_color & 0xff)
        if maximum == 255:
            return r, g, b
        elif maximum == 1.0:
            return round(float(r) / float(255), 4), round(float(g) / float(255), 4), round(float(b) / float(255), 4)
    @classmethod
    def hsv2rgb(cls, h, s, v, maximum=255):
        h = float(h % 360.0)
        s = float(max(min(s, 1.0), 0.0))
        v = float(max(min(v, 1.0), 0.0))
        #
        c = v * s
        x = c * (1 - abs((h / 60.0) % 2 - 1))
        m = v - c
        if 0 <= h < 60:
            r_, g_, b_ = c, x, 0
        elif 60 <= h < 120:
            r_, g_, b_ = x, c, 0
        elif 120 <= h < 180:
            r_, g_, b_ = 0, c, x
        elif 180 <= h < 240:
            r_, g_, b_ = 0, x, c
        elif 240 <= h < 300:
            r_, g_, b_ = x, 0, c
        else:
            r_, g_, b_ = c, 0, x
        #
        if maximum == 255:
            r, g, b = int(round((r_ + m) * maximum)), int(round((g_ + m) * maximum)), int(round((b_ + m) * maximum))
        else:
            r, g, b = float((r_ + m)), float((g_ + m)), float((b_ + m))
        return r, g, b
    @classmethod
    def rgb_to_hsv(cls, r, g, b, maximum=255):
        r, g, b = r/255.0, g/255.0, b/255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        m = mx - mn
        #
        h = 0.0
        if mx == mn:
            h = 0.0
        elif mx == r:
            if g >= b:
                h = ((g - b) / m) * 60
            else:
                h = ((g - b) / m) * 60 + 360
        elif mx == g:
            h = ((b - r) / m) * 60 + 120
        elif mx == b:
            h = ((r - g) / m) * 60 + 240
        #
        if mx == 0:
            s = 0.0
        else:
            s = m / mx
        v = mx
        h_ = h
        s_ = s
        v_ = v
        return h_, s_, v_
    @classmethod
    def get_complementary_rgb(cls, r, g, b, maximum=255):
        return abs(255-r), abs(255-g), abs(255-b)
    @classmethod
    def set_rgb_offset(cls, rgb, hsv_offset):
        r, g, b = rgb


class ColorSpaceMtd(object):
    SRGB_TO_ACCESCG_MATRIX = [
        [0.613132422390542, 0.339538015799666, 0.047416696048269],
        [0.070124380833917, 0.916394011313573, 0.013451523958235],
        [0.020587657528185, 0.109574571610682, 0.869785404035327]
    ]
    ACCESCG_TO_SRGB_MATRIX = [
        [1.704858676289160, -0.621716021885330, -0.083299371729057],
        [-0.130076824208823, 1.140735774822504, -0.010559801677511],
        [-0.023964072927574, -0.128975508299318, 1.153014018916862]
    ]
    @classmethod
    def srgb_to_accescg(cls, rgb):
        matrix = cls.SRGB_TO_ACCESCG_MATRIX
        v_out = [
            matrix[0][0] * rgb[0] + matrix[0][1] * rgb[1] + matrix[0][2] * rgb[2],
            matrix[1][0] * rgb[0] + matrix[1][1] * rgb[1] + matrix[1][2] * rgb[2],
            matrix[2][0] * rgb[0] + matrix[2][1] * rgb[1] + matrix[2][2] * rgb[2]
        ]
        if len(rgb) > 3:
            v_out += rgb[3::]
        return v_out
    @classmethod
    def accescg_to_srgb(cls, rgb):
        matrix = cls.ACCESCG_TO_SRGB_MATRIX
        v_out = [
            matrix[0][0] * rgb[0] + matrix[0][1] * rgb[1] + matrix[0][2] * rgb[2],
            matrix[1][0] * rgb[0] + matrix[1][1] * rgb[1] + matrix[1][2] * rgb[2],
            matrix[2][0] * rgb[0] + matrix[2][1] * rgb[1] + matrix[2][2] * rgb[2]
        ]
        if len(rgb) > 3:
            v_out += rgb[3::]
        return v_out


class TextOpt(object):
    def __init__(self, raw):
        self._raw = raw

    def get_is_contain_chinese(self):
        check_str = self._raw
        if isinstance(check_str, str):
            check_str = check_str.decode('utf-8')
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def get_is_contain_space(self):
        return ' ' in self._raw

    def to_rgb(self, maximum=255):
        string = self._raw
        if string:
            _ = [str(ord(i)) for seq, i in enumerate(string)]
            _.reverse()
            a = int(''.join(_))
            h = float(a % 25600)/100.0
            s = float(50 + a % 50)/100.0
            v = float(50 + (a+h) % 50)/100.0
            return ColorMtd.hsv2rgb(h, s, v, maximum)
        return 0, 0, 0

    def to_rgb_(self, maximum=255):
        pass

    def set_clear_to(self):
        return re.sub(
            ur'[^\u4e00-\u9fa5a-zA-Z0-9]', '_', self._raw
        )

    def get_filter_by_pattern(self, pattern):
        return fnmatch.filter([self._raw], pattern)

    def to_frames(self):
        lis = []
        s = self._raw
        texts = [i.strip() for i in s.split(',')]
        for i in texts:
            if '-' in i:
                i_start_frame, i_end_frame = [j.strip() for j in i.split('-')]
                lis.extend(list(range(int(i_start_frame), int(i_end_frame)+1)))
            else:
                lis.append(int(i))
        if lis:
            lis_ = list(set(lis))
            lis_.sort()
            return lis_
        return lis

    def to_frame_range(self):
        frames = self.to_frames()
        return min(frames), max(frames)


class ValueMtd(object):
    @classmethod
    def step_to(cls, value, delta, step, valueRange):
        min0, max0 = valueRange
        min1, max1 = min0 + step, max0 - step
        if value < min1:
            if 0 < delta:
                value += step
            else:
                value = min0
        elif min1 <= value <= max1:
            value += [-step, step][delta > 0]
        elif max1 < value:
            if delta < 0:
                value -= step
            else:
                value = max0
        return value
    @classmethod
    def map_to(cls, value, sourceValueRange, targetValueRange):
        assert isinstance(sourceValueRange, (tuple, list)), 'Argument Error, "sourceValueRange" Must "tuple" or "list".'
        assert isinstance(targetValueRange, (tuple, list)), 'Argument Error, "targetValueRange" Must "tuple" or "list".'

        min0, max0 = sourceValueRange
        min1, max1 = targetValueRange
        #
        if max0 - min0 > 0:
            percent = float(value - min0) / float(max0 - min0)
            #
            value_ = (max1 - min1) * percent + min1
            return value_
        else:
            return min1
    @classmethod
    def get_percent_prettify(cls, value, maximum, round_count=3):
        round_range = 100
        if maximum > 0:
            percent = round(float(value) / float(maximum), round_count) * round_range
        else:
            if value > 0:
                percent = float(u'inf')
            elif value < 0:
                percent = float('-inf')
            else:
                percent = 0
        return percent


class VedioOpt(object):
    """
ffmpeg version 3.4.7 Copyright (c) 2000-2019 the FFmpeg developers
  built with gcc 4.8.5 (GCC) 20150623 (Red Hat 4.8.5-39)
  configuration: --prefix=/usr --bindir=/usr/bin --datadir=/usr/share/ffmpeg --docdir=/usr/share/doc/ffmpeg --incdir=/usr/include/ffmpeg --libdir=/usr/lib64 --mandir=/usr/share/man --arch=x86_64 --optflags='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic' --extra-ldflags='-Wl,-z,relro ' --extra-cflags=' ' --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc --enable-version3 --enable-bzlib --disable-crystalhd --enable-fontconfig --enable-gcrypt --enable-gnutls --enable-ladspa --enable-libass --enable-libbluray --enable-libcdio --enable-libdrm --enable-indev=jack --enable-libfreetype --enable-libfribidi --enable-libgsm --enable-libmp3lame --enable-nvenc --enable-openal --enable-opencl --enable-opengl --enable-libopenjpeg --enable-libopus --disable-encoder=libopus --enable-libpulse --enable-librsvg --enable-libsoxr --enable-libspeex --enable-libtheora --enable-libvorbis --enable-libv4l2 --enable-libvidstab --enable-libx264 --enable-libx265 --enable-libxvid --enable-libzvbi --enable-avfilter --enable-avresample --enable-postproc --enable-pthreads --disable-static --enable-shared --enable-gpl --disable-debug --disable-stripping --shlibdir=/usr/lib64 --enable-libmfx --enable-runtime-cpudetect
  libavutil      55. 78.100 / 55. 78.100
  libavcodec     57.107.100 / 57.107.100
  libavformat    57. 83.100 / 57. 83.100
  libavdevice    57. 10.100 / 57. 10.100
  libavfilter     6.107.100 /  6.107.100
  libavresample   3.  7.  0 /  3.  7.  0
  libswscale      4.  8.100 /  4.  8.100
  libswresample   2.  9.100 /  2.  9.100
  libpostproc    54.  7.100 / 54.  7.100
Hyper fast Audio and Video encoder
usage: ffmpeg [options] [[infile options] -i infile]... {[outfile options] outfile}...

Getting help:
    -h      -- print basic options
    -h long -- print more options
    -h full -- print all options (including all format and codec specific options, very long)
    -h type=name -- print all options for the named decoder/encoder/demuxer/muxer/filter
    See man ffmpeg for detailed description of the options.

Print help / information / capabilities:
-L                  show license
-h topic            show help
-? topic            show help
-help topic         show help
--help topic        show help
-version            show version
-buildconf          show build configuration
-formats            show available formats
-muxers             show available muxers
-demuxers           show available demuxers
-devices            show available devices
-codecs             show available codecs
-decoders           show available decoders
-encoders           show available encoders
-bsfs               show available bit stream filters
-protocols          show available protocols
-filters            show available filters
-pix_fmts           show available pixel formats
-layouts            show standard channel layouts
-sample_fmts        show available audio sample formats
-colors             show available color names
-opencl_bench       run benchmark on all OpenCL devices and show results
-sources device     list sources of the input device
-sinks device       list sinks of the output device
-hwaccels           show available HW acceleration methods

Global options (affect whole program instead of just one file:
-loglevel loglevel  set logging level
-v loglevel         set logging level
-report             generate a report
-max_alloc bytes    set maximum size of a single allocated block
-opencl_options     set OpenCL environment options
-y                  overwrite output files
-n                  never overwrite output files
-ignore_unknown     Ignore unknown stream types
-filter_threads     number of non-complex filter threads
-filter_complex_threads  number of threads for -filter_complex
-stats              print progress report during encoding
-max_error_rate ratio of errors (0.0: no errors, 1.0: 100% error  maximum error rate
-bits_per_raw_sample number  set the number of bits per raw sample
-vol volume         change audio volume (256=normal)

Per-file main options:
-f fmt              force format
-c codec            codec name
-codec codec        codec name
-pre preset         preset name
-map_metadata outfile[,metadata]:infile[,metadata]  set metadata information of outfile from infile
-t duration         record or transcode "duration" seconds of audio/video
-to time_stop       record or transcode stop time
-fs limit_size      set the limit file size in bytes
-ss time_off        set the start time offset
-sseof time_off     set the start time offset relative to EOF
-seek_timestamp     enable/disable seeking by timestamp with -ss
-timestamp time     set the recording timestamp ('now' to set the current time)
-metadata string=string  add metadata
-program title=string:st=number...  add program with specified streams
-target type        specify target file type ("vcd", "svcd", "dvd", "dv" or "dv50" with optional prefixes "pal-", "ntsc-" or "film-")
-apad               audio pad
-frames number      set the number of frames to output
-filter filter_graph  set stream filtergraph
-filter_script filename  read stream filtergraph description from a file
-reinit_filter      reinit filtergraph on input parameter changes
-discard            discard
-disposition        disposition

Video options:
-vframes number     set the number of video frames to output
-r rate             set frame rate (Hz value, fraction or abbreviation)
-s size             set frame size (WxH or abbreviation)
-aspect aspect      set aspect ratio (4:3, 16:9 or 1.3333, 1.7777)
-bits_per_raw_sample number  set the number of bits per raw sample
-vn                 disable video
-vcodec codec       force video codec ('copy' to copy stream)
-timecode hh:mm:ss[:;.]ff  set initial TimeCode value.
-pass n             select the pass number (1 to 3)
-vf filter_graph    set video filters
-ab bitrate         audio bitrate (please use -b:a)
-b bitrate          video bitrate (please use -b:v)
-dn                 disable data

Audio options:
-aframes number     set the number of audio frames to output
-aq quality         set audio quality (codec-specific)
-ar rate            set audio sampling rate (in Hz)
-ac channels        set number of audio channels
-an                 disable audio
-acodec codec       force audio codec ('copy' to copy stream)
-vol volume         change audio volume (256=normal)
-af filter_graph    set audio filters

Subtitle options:
-s size             set frame size (WxH or abbreviation)
-sn                 disable subtitle
-scodec codec       force subtitle codec ('copy' to copy stream)
-stag fourcc/tag    force subtitle tag/fourcc
-fix_sub_duration   fix subtitles duration
-canvas_size size   set canvas size (WxH or abbreviation)
-spre preset        set the subtitle options to the indicated preset

    """
    def __init__(self, file_path):
        self._file_path = file_path
    @property
    def path(self):
        return self._file_path
    #
    def get_thumbnail_file_path(self, ext='.jpg'):
        return TemporaryThumbnailMtd.get_file_path(self._file_path, ext=ext)
    #
    def get_thumbnail(self, width=128, ext='.jpg', block=False):
        thumbnail_file_path = self.get_thumbnail_file_path(ext=ext)
        if os.path.exists(self._file_path):
            if os.path.exists(thumbnail_file_path) is False:
                directory_path = os.path.dirname(thumbnail_file_path)
                if os.path.exists(directory_path) is False:
                    os.makedirs(directory_path)
                #
                cmd_args = [
                    Bin.get_ffmpeg(),
                    u'-i "{}"'.format(self.path),
                    '-vf scale={}:-1'.format(width),
                    '-vframes 1',
                    '"{}"'.format(thumbnail_file_path)
                ]
                #
                if block is True:
                    SubProcessMtd.set_run_with_result(
                        ' '.join(cmd_args)
                    )
                else:
                    SubProcessMtd.set_run(
                        ' '.join(cmd_args)
                    )
        return thumbnail_file_path

    def get_thumbnail_create_args(self, width=128, ext='.jpg'):
        thumbnail_file_path = self.get_thumbnail_file_path(ext=ext)
        if os.path.exists(thumbnail_file_path) is False:
            if os.path.exists(self._file_path):
                directory_path = os.path.dirname(thumbnail_file_path)
                if os.path.exists(directory_path) is False:
                    os.makedirs(directory_path)
                #
                cmd_args = [
                    Bin.get_ffmpeg(),
                    u'-i "{}"'.format(self.path),
                    '-vf scale={}:-1'.format(width),
                    '-vframes 1',
                    '-n',
                    '"{}"'.format(thumbnail_file_path)
                ]
                return thumbnail_file_path, ' '.join(cmd_args)
        return thumbnail_file_path, None

    def set_convert_to(self):
        pass

    def set_mov_create_from(self, image_file_path, width=1024, fps=24, block=False):
        if StoragePathOpt(self.path).get_is_exists() is False:
            cmd_args = [
                Bin.get_ffmpeg(),
                '-i "{}"'.format(image_file_path),
                '-r {}'.format(fps),
                '-f mov',
                '-vf scale={}:-1'.format(width),
                '-vcodec h264',
                '-n',
                '"{}"'.format(self.path)
            ]
            cmd = ' '.join(cmd_args)
            if block is True:
                SubProcessMtd.set_run_with_result(
                    cmd
                )
            else:
                SubProcessMtd.set_run(
                    cmd
                )

    def get_size(self):
        cmd_args = [
            Bin.get_ffmpeg(),
            u'-i "{}"'.format(self.path),
        ]
        cmd = ' '.join(cmd_args)
        SubProcessMtd.set_run_with_result(
            cmd
        )


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


class Test(object):
    ROOT = os.path.abspath('../../bin')


class OiioImageOpt(object):
    """
    oiiotool -- simple image processing operations
    OpenImageIO-Arnold 2.2.1 http://www.openimageio.org
    Usage:  oiiotool [filename|command]...

    Important usage tips:
      * The oiiotool command line is processed in order, LEFT to
        RIGHT.
      * The command line consists of image NAMES ('image.tif') and
        COMMANDS ('--over'). Commands start with dashes (one or two
        dashes are equivalent). Some commands have required arguments
        which must follow on the command line. For example, the '-o'
        command is followed by a filename.
      * oiiotool is STACK-based: naming an image pushes it on the
        stack, and most commands pop the top image (or sometimes more
        than one image), perform a calculation, and push the result
        image back on the stack. For example, the '--over' command pops
        the top two images off the stack, composites them, then pushes
        the result back onto the stack.
      * Some commands allow one or more optional MODIFIERS in the
        form 'name=value', which are appended directly to the command
        itself (no spaces), separated by colons ':'. For example,
           oiiotool in.tif --text:x=100:y=200:color=1,0,0 "Hello" -o out.tif
      * Using numerical wildcards will run the whole command line
        on each of several sequentially-named files, for example:
           oiiotool fg.#.tif bg.#.tif -over -o comp.#.tif
        See the manual for info about subranges, number of digits,
        etc.
      * Command line arguments containing substrings enclosed in
        braces {} are replaced by evaluating their contents as
        expressions. Simple math is allowed as well as retrieving
        metadata such as {TOP.'foo:bar'}, {IMG[0].filename}, or
        {FRAME_NUMBER/24.0}.

    Options (general):
        --help                        Print help message
        -v                            Verbose status messages
        -q                            Quiet mode (turn verbose off)
        -n                            No saved output (dry run)
        -a                            Do operations on all subimages/miplevels
        --debug                       Debug mode
        --runstats                    Print runtime statistics
        --info                        Print resolution and basic info on all inputs, detailed metadata if -v is also used (options: format=xml:verbose=1)
        --echo TEXT                   Echo message to console (options: newline=0)
        --metamatch REGEX             Which metadata is printed with -info -v
        --no-metamatch REGEX          Which metadata is excluded with -info -v
        --stats                       Print pixel statistics on all inputs
        --dumpdata                    Print all pixel data values (options: empty=0)
        --hash                        Print SHA-1 hash of each input image
        --colorcount COLORLIST        Count of how many pixels have the given color (argument: color;color;...) (options: eps=color)
        --rangecheck MIN MAX          Count of how many pixels are outside the min/max color range (each is a comma-separated color value list)
        --no-clobber                  Do not overwrite existing files
        --threads N                   Number of threads (default 0 == #cores)
        --frames FRAMERANGE           Frame range for '#' or printf-style wildcards
        --framepadding NDIGITS        Frame number padding digits (ignored when using printf-style wildcards)
        --views VIEWNAMES             Views for %V/%v wildcards (comma-separated, defaults to "left,right")
        --wildcardoff                 Disable numeric wildcard expansion for subsequent command line arguments
        --wildcardon                  Enable numeric wildcard expansion for subsequent command line arguments
        --evaloff                     Disable {expression} evaluation for subsequent command line arguments
        --evalon                      Enable {expression} evaluation for subsequent command line arguments
        --no-autopremult              Turn off automatic premultiplication of images with unassociated alpha
        --autopremult                 Turn on automatic premultiplication of images with unassociated alpha
        --autoorient                  Automatically --reorient all images upon input
        --autocc                      Automatically color convert based on filename
        --noautocc                    Turn off automatic color conversion
        --native                      Keep native pixel data type (bypass cache if necessary)
        --cache MB                    ImageCache size (in MB: default=4096)
        --autotile TILESIZE           Autotile enable for cached images (the argument is the tile size, default 0 means no autotile)
        --metamerge                   Always merge metadata of all inputs into output
    Commands that read images:
        -i FILENAME                   Input file (options: now=, printinfo=, autocc=, type=, ch=)
        --iconfig NAME VALUE          Sets input config attribute (options: type=...)
    Commands that write images:
        -o FILENAME                   Output the current image to the named file
        -otex FILENAME                Output the current image as a texture
        -oenv FILENAME                Output the current image as a latlong env map
        -obump FILENAME               Output the current bump texture map as a 6 channels texture including the first and second moment of the bump slopes (options: bumpformat=height|normal|auto)
    Options that affect subsequent image output:
        -d TYPE                       '-d TYPE' sets the output data format of all channels, '-d CHAN=TYPE' overrides a single named channel (multiple -d args are allowed). Data types include: uint8, sint8, uint10, uint12, uint16, sint16, uint32, sint32, half, float, double
        --scanline                    Output scanline images
        --tile WIDTH HEIGHT           Output tiled images with this tile size
        --compression NAME            Set the compression method (in the form "name" or "name:quality")
        --dither                      Add dither to 8-bit output
        --planarconfig CONFIG         Force planarconfig (contig, separate, default)
        --adjust-time                 Adjust file times to match DateTime metadata
        --noautocrop                  Do not automatically crop images whose formats don't support separate pixel data and full/display windows
        --autotrim                    Automatically trim black borders upon output to file formats that support separate pixel data and full/display windows
    Options that change current image metadata (but not pixel values):
        --attrib NAME VALUE           Sets metadata attribute (options: type=...)
        --sattrib NAME VALUE          Sets string metadata attribute
        --eraseattrib REGEX           Erase attributes matching regex
        --caption TEXT                Sets caption (ImageDescription metadata)
        --keyword KEYWORD             Add a keyword
        --clear-keywords              Clear all keywords
        --nosoftwareattrib            Do not write command line into Exif:ImageHistory, Software metadata attributes
        --sansattrib                  Write command line into Software & ImageHistory but remove --sattrib and --attrib options
        --orientation ORIENT          Set the assumed orientation
        --orientcw                    Rotate orientation metadata 90 deg clockwise
        --orientccw                   Rotate orientation metadata 90 deg counter-clockwise
        --orient180                   Rotate orientation metadata 180 deg
        --origin +X+Y                 Set the pixel data window origin (e.g. +20+10, -16-16)
        --originoffset +X+Y           Offset the pixel data window origin from its current position (e.g. +20+10, -16-16)
        --fullsize GEOM               Set the display window (e.g., 1920x1080, 1024x768+100+0, -20-30)
        --fullpixels                  Set the 'full' image range to be the pixel data window
        --chnames NAMELIST            Set the channel names (comma-separated)
    Options that affect subsequent actions:
        --fail THRESH                 Failure threshold difference (0.000001)
        --failpercent PCNT            Allow this percentage of failures in diff (0)
        --hardfail THRESH             Fail diff if any one pixel exceeds this error (infinity)
        --warn THRESH                 Warning threshold difference (0.00001)
        --warnpercent PCNT            Allow this percentage of warnings in diff (0)
        --hardwarn THRESH             Warn if any one pixel difference exceeds this error (infinity)
    Actions:
        --create GEOM NCHANS          Create a blank image
        --pattern NAME GEOM NCHANS    Create a patterned image. Pattern name choices: black, constant, fill, checker, noise
        --kernel NAME GEOM            Create a centered convolution kernel
        --capture                     Capture an image (options: camera=%d)
        --diff                        Print report on the difference of two images (modified by --fail, --failpercent, --hardfail, --warn, --warnpercent --hardwarn)
        --pdiff                       Print report on the perceptual difference of two images (modified by --fail, --failpercent, --hardfail, --warn, --warnpercent --hardwarn)
        --add                         Add two images
        --addc VAL                    Add to all channels a scalar or per-channel constants (e.g.: 0.5 or 1,1.25,0.5)
        --sub                         Subtract two images
        --subc VAL                    Subtract from all channels a scalar or per-channel constants (e.g.: 0.5 or 1,1.25,0.5)
        --mul                         Multiply two images
        --mulc VAL                    Multiply the image values by a scalar or per-channel constants (e.g.: 0.5 or 1,1.25,0.5)
        --div                         Divide first image by second image
        --divc VAL                    Divide the image values by a scalar or per-channel constants (e.g.: 0.5 or 1,1.25,0.5)
        --mad                         Multiply two images, add a third
        --invert                      Take the color inverse (subtract from 1)
        --abs                         Take the absolute value of the image pixels
        --absdiff                     Absolute difference between two images
        --absdiffc VAL                Absolute difference versus a scalar or per-channel constant (e.g.: 0.5 or 1,1.25,0.5)
        --powc VAL                    Raise the image values to a scalar or per-channel power (e.g.: 2.2 or 2.2,2.2,2.2,1.0)
        --noise                       Add noise to an image (options: type=gaussian:mean=0:stddev=0.1, type=uniform:min=0:max=0.1, type=salt:value=0:portion=0.1, seed=0
        --chsum                       Turn into 1-channel image by summing channels (options: weight=r,g,...)
        --colormap MAPNAME            Color map based on channel 0 (arg: "inferno", "viridis", "magma", "turbo", "plasma", "blue-red", "spectrum", "heat", or comma-separated list of RGB triples)
        --crop GEOM                   Set pixel data resolution and offset, cropping or padding if necessary (WxH+X+Y or xmin,ymin,xmax,ymax)
        --croptofull                  Crop or pad to make pixel data region match the "full" region
        --trim                        Crop to the minimal ROI containing nonzero pixel values
        --cut GEOM                    Cut out the ROI and reposition to the origin (WxH+X+Y or xmin,ymin,xmax,ymax)
        --paste +X+Y                  Paste fg over bg at the given position (e.g., +100+50; '-' or 'auto' indicates using the data window position as-is; options: all=%d, mergeroi=%d)
        --mosaic WxH                  Assemble images into a mosaic (arg: WxH; options: pad=0)
        --over                        'Over' composite of two images
        --zover                       Depth composite two images with Z channels (options: zeroisinf=%d)
        --deepmerge                   Merge/composite two deep images
        --deepholdout                 Hold out one deep image by another
        --histogram BINSxHEIGHT CHAN  Histogram one channel (options: cumulative=0)
        --rotate90                    Rotate the image 90 degrees clockwise
        --rotate180                   Rotate the image 180 degrees
        --rotate270                   Rotate the image 270 degrees clockwise (or 90 degrees CCW)
        --flip                        Flip the image vertically (top<->bottom)
        --flop                        Flop the image horizontally (left<->right)
        --reorient                    Rotate and/or flop the image to transform the pixels to match the Orientation metadata
        --transpose                   Transpose the image
        --cshift +X+Y                 Circular shift the image (e.g.: +20-10)
        --resample GEOM               Resample (640x480, 50%) (options: interp=0)
        --resize GEOM                 Resize (640x480, 50%) (options: filter=%s)
        --fit GEOM                    Resize to fit within a window size (options: filter=%s, pad=%d, exact=%d)
        --pixelaspect ASPECT          Scale up the image's width or height to match the given pixel aspect ratio (options: filter=%s)
        --rotate DEGREES              Rotate pixels (degrees clockwise) around the center of the display window (options: filter=%s, center=%f,%f, recompute_roi=%d
        --warp MATRIX                 Warp pixels (argument is a 3x3 matrix, separated by commas) (options: filter=%s, recompute_roi=%d)
        --convolve                    Convolve with a kernel
        --blur WxH                    Blur the image (options: kernel=name)
        --median WxH                  Median filter the image
        --dilate WxH                  Dilate (area maximum) the image
        --erode WxH                   Erode (area minimum) the image
        --unsharp                     Unsharp mask (options: kernel=gaussian, width=3, contrast=1, threshold=0)
        --laplacian                   Laplacian filter the image
        --fft                         Take the FFT of the image
        --ifft                        Take the inverse FFT of the image
        --polar                       Convert complex (real,imag) to polar (amplitude,phase)
        --unpolar                     Convert polar (amplitude,phase) to complex (real,imag)
        --fixnan STRATEGY             Fix NaN/Inf values in the image (choices: none, black, box3, error)
        --fillholes                   Fill in holes (where alpha is not 1)
        --max                         Pixel-by-pixel max of two images
        --maxc VAL                    Max all values with a scalar or per-channel constants (e.g.: 0.5 or 1,1.25,0.5)
        --min                         Pixel-by-pixel min of two images
        --minc VAL                    Min all values with a scalar or per-channel constants (e.g.: 0.5 or 1,1.25,0.5)
        --clamp                       Clamp values (options: min=..., max=..., clampalpha=0)
        --contrast                    Remap values (options: black=0..., white=1..., sthresh=0.5..., scontrast=1.0..., gamma=1, clamp=0|1)
        --rangecompress               Compress the range of pixel values with a log scale (options: luma=0|1)
        --rangeexpand                 Un-rangecompress pixel values back to a linear scale (options: luma=0|1)
        --line X1,Y1,X2,Y2,...        Render a poly-line (options: color=)
        --box X1,Y1,X2,Y2             Render a box (options: color=)
        --fill GEOM                   Fill a region (options: color=)
        --text TEXT                   Render text into the current image (options: x=, y=, size=, color=)
    Manipulating channels or subimages:
        --ch CHANLIST                 Select or shuffle channels (e.g., "R,G,B", "B,G,R", "2,3,4")
        --chappend                    Append the channels of the last two images
        --unmip                       Discard all but the top level of a MIPmap
        --selectmip MIPLEVEL          Select just one MIP level (0 = highest res)
        --subimage SUBIMAGEINDEX      Select just one subimage (by index or name)
        --sisplit                     Split the top image's subimges into separate images
        --siappend                    Append the last two images into one multi-subimage image
        --siappendall                 Append all images on the stack into a single multi-subimage image
        --deepen                      Deepen normal 2D image to deep
        --flatten                     Flatten deep image to non-deep
    Image stack manipulation:
        --dup                         Duplicate the current image (push a copy onto the stack)
        --swap                        Swap the top two images on the stack.
        --pop                         Throw away the current image
        --label %s                    Label the top image
    Color management:
        --colorconfig FILENAME        Explicitly specify an OCIO configuration file
        --iscolorspace COLORSPACE     Set the assumed color space (without altering pixels)
        --tocolorspace COLORSPACE     Convert the current image's pixels to a named color space
        --colorconvert SRC DST        Convert pixels from 'src' to 'dst' color space (options: key=, value=, unpremult=, strict=)
        --ccmatrix MATRIXVALS         Color convert pixels with a 3x3 or 4x4 matrix (options: unpremult=,transpose=)
        --ociolook LOOK               Apply the named OCIO look (options: from=, to=, inverse=, key=, value=, unpremult=)
        --ociodisplay DISPLAY VIEW    Apply the named OCIO display and view (options: from=, looks=, key=, value=, unpremult=)
        --ociofiletransform FILENAME  Apply the named OCIO filetransform (options: inverse=, unpremult=)
        --unpremult                   Divide all color channels of the current image by the alpha to "un-premultiply"
        --premult                     Multiply all color channels of the current image by the alpha

    Input formats supported: bmp, cineon, dds, dpx, fits, hdr, ico, iff, jpeg, null, openexr, png, pnm, psd, rla, sgi, socket, softimage, targa, tiff, zfile
    Output formats supported: bmp, dpx, fits, hdr, ico, iff, jpeg, null, openexr, png, pnm, rla, sgi, socket, targa, tiff, zfile
    Color configuration: built-in
    Known color spaces: "linear", "default", "rgb", "RGB", "sRGB", "Rec709"
    No OpenColorIO support was enabled at build time.
    Filters available: box, triangle, gaussian, sharp-gaussian, catmull-rom, blackman-harris, sinc, lanczos3, radial-lanczos3, nuke-lanczos6, mitchell, bspline, disk, cubic, keys, simon, rifman
    Dependent libraries: jpeglib 9.2, null 1.0, IlmBase , libpng 1.6.29, LIBTIFF Version 4.0.8
    OIIO 2.2.1 built sse2,sse3,ssse3,sse41,sse42, running on 12 cores 62.7GB sse2,sse3,ssse3,sse41,sse42,avx,avx2,fma,f16c,popcnt,rdrand
    Full OIIO documentation can be found at
        https://openimageio.readthedocs.io
    """
    #
    INFO_PATTERN = '{path} : {width} x {height}, {channel_count} channel, {type} {format}'
    #
    BIT_DICT = {
        'uint8': 8, 'uint10': 10, 'uint12': 12, 'uint16': 16, 'uint32': 32,
        'sint8': 8, 'sint16': 16, 'sint32': 32,
        'half': 16, 'float': 32, 'double': 64
    }
    TYPE_DICT = {
        'uint8': 'uint', 'uint10': 'uint', 'uint12': 'uint', 'uint16': 'uint', 'uint32': 'uint',
        'sint16': 'sint', 'sint8': 'sint', 'sint32': 'sint',
        'half': 'half',  'float': 'float', 'double': 'double'
    }
    @classmethod
    def _get_info_(cls, file_path):
        cmd_args = [
            Bin.get_oiiotool(),
            '--info:verbose=1 "{}"'.format(file_path),
        ]
        p = SubProcessMtd.set_run(' '.join(cmd_args))
        _ = p.stdout.readlines()
        if _:
            p = parse.parse(cls.INFO_PATTERN, _[0])
            if p:
                return p.named
    @classmethod
    def _get_metadata_(cls, file_path):
        cmd_args = [
            Bin.get_oiiotool(),
            '--info:verbose=1 "{}"'.format(file_path),
        ]
        p = SubProcessMtd.set_run(' '.join(cmd_args))
        _ = p.stdout.readlines()
        print _
    #
    def __init__(self, file_path):
        if os.path.isfile(file_path):
            self._file_path = file_path
            self._info = self._get_info_(self._file_path)
        else:
            raise OSError()
    @property
    def info(self):
        return self._info
    #
    @property
    def path(self):
        return self._file_path
    @property
    def size(self):
        return int(self._info['width']), int(self._info['height'])
    @property
    def bit(self):
        return self.BIT_DICT[self._info['type']]
    @property
    def type(self):
        return self.TYPE_DICT[self._info['type']]
    @property
    def format(self):
        return self

    def set_convert_to(self, output_file_path):
        if os.path.exists(self.path):
            if SystemMtd.get_is_windows():
                pass
            elif SystemMtd.get_is_linux():
                if os.path.exists(output_file_path) is False:
                    subprocess.Popen(
                        u'ffmpeg -framerate 1 -i "{}" -c:v libx264 -r 30 -pix_fmt yuv420p "{}"'.format(
                            self.path, output_file_path
                        ),
                        shell=True
                    )

    def get_metadata(self):
        pass

    def __str__(self):
        return 'image(path="{}", width={}, height={})'.format(
            self._file_path,
            self._info['width'], self._info['height']
        )


class OiioTextureOpt(OiioImageOpt):
    def __init__(self, *args, **kwargs):
        super(OiioTextureOpt, self).__init__(*args, **kwargs)

    def get_is_srgb(self):
        bit = self.BIT_DICT[self._info['type']]
        type_ = self.TYPE_DICT[self._info['type']]
        return bit <= 16 and type_ in ('uint', 'sint')

    def get_is_linear(self):
        return not self.get_is_srgb()

    def get_color_space(self):
        if self.get_is_srgb():
            return bsc_configure.ColorSpace.SRGB
        else:
            return bsc_configure.ColorSpace.LINEAR


class OslShaderMtd(object):
    OBJ_PATTERN = 'shader "{name}"\n'
    PORT_PATTERN = '    "{name}" "{type}"\n'
    DEFAULT_VALUE_PATTERN = '		Default value: {value}\n'
    METADATA_PATTERN = '		metadata: {type} {name} = {value}\n'
    @classmethod
    def set_compile(cls, file_path):
        file_opt = StorageFileOpt(file_path)
        compile_file_path = '{}.oso'.format(file_opt.path_base)
        #
        cmd_args = [
            Bin.get_oslc(),
            '-o "{}" "{}"'.format(compile_file_path, file_opt.path),
        ]
        SubProcessMtd.set_run_with_result(' '.join(cmd_args))
    @classmethod
    def get_info(cls, file_path):
        dic = collections.OrderedDict()
        #
        file_opt = StorageFileOpt(file_path)
        compile_file_path = '{}.oso'.format(file_opt.path_base)
        #
        cmd_args = [
            Bin.get_oslinfo(),
            '-v "{}"'.format(compile_file_path),
        ]
        p = SubProcessMtd.set_run(' '.join(cmd_args))
        _ = p.stdout.readlines()
        if _:
            p = parse.parse(cls.OBJ_PATTERN, _[0])
            if p:
                dic.update(p.named)
            #
            ports_dict = collections.OrderedDict()
            dic['ports'] = ports_dict
            #
            i_port_dict = collections.OrderedDict()
            for i in _[1:]:
                i_p_0 = parse.parse(cls.PORT_PATTERN, i)
                if i_p_0:
                    i_port_dict = collections.OrderedDict()
                    i_name_0 = i_p_0.named['name']
                    i_type_0 = i_p_0.named['type']
                    i_assign_0 = 'input'
                    if i_type_0.startswith('output'):
                        i_type_0 = i_type_0.split(' ')[-1]
                        i_assign_0 = 'output'
                    #
                    i_port_dict['type'] = i_type_0
                    i_port_dict['assign'] = i_assign_0
                    i_port_dict['metadata'] = collections.OrderedDict()
                    ports_dict[i_name_0] = i_port_dict
                else:
                    i_p_1 = parse.parse(cls.DEFAULT_VALUE_PATTERN, i)
                    if i_p_1:
                        i_type = i_port_dict['type']
                        i_value_1 = i_p_1.named['value']
                        if i_type in ['int', 'float', 'string']:
                            i_value_1 = eval(i_value_1)
                        #
                        i_port_dict['value'] = i_value_1
                    else:
                        i_p_2 = parse.parse(cls.METADATA_PATTERN, i)
                        i_name_2 = i_p_2.named['name']
                        i_type_2 = i_p_2.named['type']
                        i_value_2 = i_p_2.named['value']
                        #
                        i_metadata_dict = collections.OrderedDict()
                        i_metadata_dict['type'] = i_type_2
                        if i_type_2 in ['int', 'float', 'string']:
                            i_value_2 = eval(i_value_2)
                        #
                        i_metadata_dict['value'] = i_value_2
                        i_port_dict['metadata'][i_name_2] = i_metadata_dict
        return dic


class ImageOpt(object):
    def __init__(self, file_path):
        self._file_path = file_path

    def get_thumbnail_file_path(self):
        return TemporaryThumbnailMtd.get_file_path(self._file_path)

    def get_thumbnail(self, width=128):
        thumbnail_file_path = self.get_thumbnail_file_path()
        if os.path.isfile(self._file_path):
            if os.path.exists(thumbnail_file_path) is False:
                directory_path = os.path.dirname(thumbnail_file_path)
                if os.path.exists(directory_path) is False:
                    os.makedirs(directory_path)
                #
                cmd_args = [
                    Bin.get_oiiotool(),
                    u'-i "{}"'.format(self._file_path),
                    '--resize {}x0'.format(width),
                    '-o "{}"'.format(thumbnail_file_path)
                ]
                SubProcessMtd.set_run(
                    ' '.join(cmd_args)
                )
        return thumbnail_file_path

    def get_jpg_file_path(self):
        path_base, ext = os.path.splitext(self._file_path)
        return '{}{}'.format(path_base, '.jpg')

    def get_jpg(self, width=1024):
        file_path = self._file_path
        #
        jpg_file_path = self.get_jpg_file_path()
        if os.path.isfile(file_path):
            directory_path = os.path.dirname(jpg_file_path)
            if os.path.exists(directory_path) is False:
                os.makedirs(directory_path)
            #
            data_time = TimestampMtd.to_string(
                '%Y:%m:%d %H:%M:%S', StorageFileOpt(file_path).get_modify_timestamp()
            )
            cmd_args = [
                Bin.get_oiiotool(),
                u'-i "{}"'.format(file_path),
                '--resize {}x0'.format(width),
                '--attrib:type=string DateTime "{}"'.format(data_time),
                '--adjust-time ',
                '--threads 1',
                u'-o "{}"'.format(jpg_file_path),
            ]
            s_p = SubProcessMtd.set_run(
                ' '.join(cmd_args)
            )
            return s_p


class ListMtd(object):
    @classmethod
    def set_grid_to(cls, array, column_count):
        lis_ = []
        count = len(array)
        row_count = int(count / column_count)
        for i in range(row_count + 1):
            _ = array[i*column_count:min((i + 1)*column_count, count)]
            if _:
                lis_.append(_)
        return lis_
    @classmethod
    def get_intersection(cls, a, b):
        _ = list(set(a) & set(b))
        _.sort(key=a.index)
        return _
    @classmethod
    def get_addition(cls, a, b):
        _ = list(set(a)-set(b))
        _.sort(key=a.index)
        return _
    @classmethod
    def get_deletion(cls, a, b):
        pass


class CoordMtd(object):
    @classmethod
    def get_region(cls, position, size):
        x, y = position
        width, height = size
        if 0 <= x < width / 2 and 0 <= y < height / 2:
            value = 0
        elif width / 2 <= x < width and 0 <= y < height / 2:
            value = 1
        elif 0 <= x < width / 2 and height / 2 <= y < height:
            value = 2
        else:
            value = 3
        return value
    @classmethod
    def set_region_to(cls, position, size, maximum_size, offset):
        x, y = position
        width, height = size
        maximum_w, maximum_h = maximum_size
        o_x, o_y = offset
        #
        region = cls.get_region(
            position=position,
            size=(maximum_w, maximum_h)
        )
        #
        if region == 0:
            x_ = x + o_x
            y_ = y + o_y
        elif region == 1:
            x_ = x - width - o_x
            y_ = y + o_y
        elif region == 2:
            x_ = x + o_x
            y_ = y - height - o_y
        else:
            x_ = x - width - o_x
            y_ = y - height - o_y
        #
        return x_, y_, region
    @classmethod
    def to_length(cls, position0, position1):
        x0, y0 = position0
        x1, y1 = position1
        return math.sqrt(((x0 - x1) ** 2) + ((y0 - y1) ** 2))
    @classmethod
    def to_angle(cls, position0, position1):
        x0, y0 = position0
        x1, y1 = position1
        #
        radian = 0.0
        #
        r0 = 0.0
        r90 = math.pi / 2.0
        r180 = math.pi
        r270 = 3.0 * math.pi / 2.0
        #
        if x0 == x1:
            if y0 < y1:
                radian = r0
            elif y0 > y1:
                radian = r180
        elif y0 == y1:
            if x0 < x1:
                radian = r90
            elif x0 > x1:
                radian = r270

        elif x0 < x1 and y0 < y1:
            radian = math.atan2((-x0 + x1), (-y0 + y1))
        elif x0 < x1 and y0 > y1:
            radian = r90 + math.atan2((y0 - y1), (-x0 + x1))
        elif x0 > x1 and y0 > y1:
            radian = r180 + math.atan2((x0 - x1), (y0 - y1))
        elif x0 > x1 and y0 < y1:
            radian = r270 + math.atan2((-y0 + y1), (x0 - x1))
        return radian * 180 / math.pi


class NestedArrayMtd(object):
    @classmethod
    def set_map_to(cls, nestedArray):
        """
        :param nestedArray: etc.[[1, 2], [1, 2]]
        :return: etc.[[1, 1], [1, 2], [2, 1], [2, 2]]
        """
        def rcsFnc_(index_):
            if index_ < count:
                _array = nestedArray[index_]
                for _i in _array:
                    c[index_] = _i
                    rcsFnc_(index_ + 1)
            else:
                lis.append(
                    copy.copy(c)
                )

        lis = []
        count = len(nestedArray)
        c = [None]*count
        rcsFnc_(0)
        return lis


class IntegerArrayMtd(object):
    @staticmethod
    def set_merge_to(array):
        lis = []
        #
        if array:
            if len(array) == 1:
                return array
            else:
                minimum, maximum = min(array), max(array)
                #
                start, end = None, None
                count = len(array)
                cur_index = 0
                #
                array.sort()
                for i_index in array:
                    if cur_index > 0:
                        pre = array[cur_index - 1]
                    else:
                        pre = None
                    #
                    if cur_index < (count - 1):
                        nex = array[cur_index + 1]
                    else:
                        nex = None
                    #
                    if pre is None and nex is not None:
                        start = minimum
                        if i_index - nex != -1:
                            lis.append(start)
                    elif pre is not None and nex is None:
                        end = maximum
                        if i_index - pre == 1:
                            lis.append((start, end))
                        else:
                            lis.append(end)
                    elif pre is not None and nex is not None:
                        if i_index - pre != 1 and i_index - nex != -1:
                            lis.append(i_index)
                        elif i_index - pre == 1 and i_index - nex != -1:
                            end = i_index
                            lis.append((start, end))
                        elif i_index - pre != 1 and i_index - nex == -1:
                            start = i_index
                    #
                    cur_index += 1
                #
        return lis


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
        exc_typ, exc_vlu, exc_stk = sys.exc_info()
        exc_txts = []
        # value = '{}: "{}"'.format(exc_typ.__name__, exc_vlu.message)
        for seq, stk in enumerate(traceback.extract_tb(exc_stk)):
            i_file_path, i_line, i_fnc, i_fnc_line = stk
            exc_txts.append(
                u'    file "{}" line {} in {}\n        {}'.format(i_file_path, i_line, i_fnc, i_fnc_line)
            )
        print exc_txts


class PointArrayOpt(object):
    def __init__(self, point_array):
        self._point_array = point_array

    def round_to(self, round_count=8):
        lis = []
        for i in self._point_array:
            x, y, z = i
            x_, y_, z_ = round(x, round_count), round(y, round_count), round(z, round_count)
            lis.append((x_, y_, z_))
        return lis


class GuiCacheMtd(object):
    CACHE = dict(
        window=None,
        button=None
    )
    @classmethod
    def get_active_window(cls):
        return cls.CACHE['window']
    @classmethod
    def set_active_window(cls, gui_prx):
        cls.CACHE['window'] = gui_prx
    @classmethod
    def get_active_button(cls):
        return cls.CACHE['button']
    @classmethod
    def set_active_button(cls, gui_prx):
        cls.CACHE['button'] = gui_prx


class SessionMtd(object):
    @classmethod
    def get_hook_abs_path(cls, src_key, tgt_key):
        """
        for i in ['../shotgun/shotgun-create', '../maya/geometry-export', '../maya/look-export']:
            print SessionMtd.get_hook_abs_path(
                'rsv-task-methods/asset/usd/usd-create', i
            )

        rsv-task-methods/asset/shotgun/shotgun-create
        rsv-task-methods/asset/maya/geometry-export
        rsv-task-methods/asset/maya/look-export

        :param src_key: str(<hook-key>)
        :param tgt_key: str(<hook-key>)
        :return: str(<hook-key>)
        """
        if fnmatch.filter([tgt_key], '.*'):
            s_0 = tgt_key.split('.')[-1].strip()
            c_0 = tgt_key.count('.')
            ss_1 = src_key.split('/')
            c_1 = len(ss_1)
            if c_0 < c_1:
                return '{}{}'.format('/'.join(ss_1[:-c_0]), s_0)
            elif c_0 == c_1:
                return s_0
            else:
                raise ValueError(
                    'count of sep "." out of range'
                )
        return tgt_key


class VariablesMtd(object):
    @classmethod
    def get_all_combinations(cls, variables):
        lis = []
        for i in itertools.product(*[[{k: i} for i in v] for k, v in variables.items()]):
            i_dic = collections.OrderedDict()
            for j_dic in i:
                i_dic.update(j_dic)
            lis.append(i_dic)
        return lis


class FrameRangeMtd(object):
    @classmethod
    def get(cls, frame_range, frame_step):
        start_frame, end_frame = frame_range
        start_frame, end_frame = int(start_frame), int(end_frame)
        frame_step = int(frame_step)
        # (1001, 1001), 1
        if start_frame == end_frame:
            return [start_frame]
        # (1001, 1002), 1
        elif start_frame < end_frame:
            frames = range(start_frame, end_frame+1)
            count = len(frames)
            # (1001, 1002), 2
            if count == frame_step:
                return [start_frame, end_frame]
            # (1001, 1010), 4
            elif count > frame_step:
                _ = [i for i in frames if not (i-1) % frame_step]
                if start_frame not in _:
                    _.insert(0, start_frame)
                if end_frame not in _:
                    _.append(end_frame)
                return _
            # (1001, 1002), 3
            else:
                return [start_frame]
        else:
            raise ValueError()


class ParsePatternOpt(object):
    def __init__(self, pattern):
        self._pattern = pattern
        self._fnmatch_pattern = self._get_fnmatch_pattern_(self._pattern)
    @classmethod
    def _get_fnmatch_pattern_(cls, variant):
        if variant is not None:
            re_pattern = re.compile(r'[{](.*?)[}]', re.S)
            #
            keys = re.findall(re_pattern, variant)
            s = variant
            if keys:
                for key in keys:
                    s = s.replace('{{{}}}'.format(key), '*')
            return s
        return variant
    @property
    def pattern(self):
        return self._pattern
    @property
    def fnmatch_pattern(self):
        return self._fnmatch_pattern


class TimeMtd(object):
    MONTH = [
        (u'01月', 'January'),
        (u'02月', 'February'),
        (u'03月', 'March'),
        (u'04月', 'April'),
        (u'05月', 'May'),
        (u'06月', 'June'),
        (u'07月', 'July'),
        (u'08月', 'August'),
        (u'09月', 'September'),
        (u'10月', 'October'),
        (u'11月', 'November'),
        (u'12月', 'December')
    ]
    WEEK = [
        (u'周一', 'Monday'),
        (u'周二', 'Tuesday'),
        (u'周三', 'Wednesday'),
        (u'周四', 'Thursday'),
        (u'周五', 'Friday'),
        (u'周六', 'Saturday'),
        (u'周天', 'Sunday'),
    ]
    @classmethod
    def to_prettify_by_timestamp(cls, timestamp, language=0):
        if isinstance(timestamp, float):
            return cls.to_prettify_by_timetuple(
                time.localtime(timestamp),
                language=language,
                )
    @classmethod
    def to_prettify_by_timetuple(cls, timetuple, language=0):
        year, month, day, hour, minute, second, week, dayCount, isDst = timetuple
        cur_timetuple = time.localtime(time.time())
        year_, month_, day_, hour_, minute_, second_, week_, dayCount_, isDst_ = cur_timetuple
        #
        monday = day - week
        monday_ = day_ - week_
        year_str = [u'{}年'.format(str(year).zfill(4)), str(year).zfill(4)][language]
        month_str = cls.MONTH[int(month) - 1][language]
        day_str = [u'{}日'.format(str(day).zfill(2)), str(day).zfill(2)][language]
        if cur_timetuple[:1] == timetuple[:1]:
            if cur_timetuple[:2] == timetuple[:2]:
                if monday_ == monday:
                    week_str = u'{0}'.format(cls.WEEK[int(week)][language])
                    if day_ == day:
                        time_str = [
                            u'{}点{}分{}秒'.format(str(hour).zfill(2), str(minute).zfill(2), str(second).zfill(2)),
                            '{}:{}:{}'.format(str(hour).zfill(2), str(minute).zfill(2), str(second).zfill(2))
                        ][language]
                        return time_str
                    elif day_ == day + 1:
                        sub_str = [u'昨天', 'Yesterday'][language]
                        return sub_str
                    return week_str
            #
            if language == 0:
                return u'{}{}'.format(month_str, day_str)
            return '{} {}'.format(day_str, month_str)
        #
        if language == 0:
            return u'{}{}'.format(year_str, month_str)
        return '{} {}'.format(month_str, year_str)


if __name__ == '__main__':
    print TextOpt('1001-1005, 2000,500, 500').to_frames()
