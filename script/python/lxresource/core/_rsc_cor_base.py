# coding:utf-8
import os

import platform

import glob

import re

import lxlog.core as log_core

import lxcontent.objects as ctt_objects


class Resource(object):
    """
print Resource.get('icons/file/file.svg')
print Resource.get('icons/file/folder.svg')
    """
    CACHE = {}

    ENVIRON_KEY = 'PAPER_EXTEND_RESOURCES'

    @classmethod
    def __find_all_roots(cls):
        if cls.ENVIRON_KEY in os.environ:
            _ = os.environ[cls.ENVIRON_KEY]
            if _:
                return _.split(os.pathsep)
        return []

    @classmethod
    def __find_all_results(cls, p):
        _ = glob.glob(p) or []
        if _:
            if platform.system() == 'Windows':
                _ = [i.replace('\\', '/') for i in _]
        return _

    @classmethod
    def __find_all_files(cls, path, ext_includes=None):
        def rcs_fnc_(path_):
            _results = os.listdir(path_) or []
            for _i_name in _results:
                _i_path = '{}/{}'.format(path_, _i_name)
                if os.path.isfile(_i_path):
                    if isinstance(ext_includes, (set, tuple, list)):
                        _i_name_base, _i_ext = os.path.splitext(_i_name)
                        if _i_ext not in ext_includes:
                            continue
                    #
                    set_.add(_i_path)
                elif os.path.isdir(_i_path):
                    rcs_fnc_(_i_path)

        set_ = set()
        if os.path.isdir(path):
            rcs_fnc_(path)

        if set_:
            list_ = list(set_)
            list_.sort()
            return list_
        return []

    @classmethod
    def __find_all_directories(cls, path):
        def rcs_fnc_(path_):
            _results = os.listdir(path_) or []
            for _i_name in _results:
                _i_path = '{}/{}'.format(path_, _i_name)
                if os.path.isdir(_i_path):
                    set_.add(_i_path)
                    rcs_fnc_(_i_path)

        set_ = set()
        if os.path.isdir(path):
            rcs_fnc_(path)

        if set_:
            list_ = list(set_)
            list_.sort()
            return list_
        return []

    @classmethod
    def get(cls, key, search_paths=None):
        """
        :param key: str
        :param search_paths: list
        :return: str(path)
        """
        if key in cls.CACHE:
            return cls.CACHE[key]

        if isinstance(search_paths, (tuple, list)):
            paths = search_paths
        else:
            paths = cls.__find_all_roots()
        #
        for i_path_root in paths:
            if os.path.isdir(i_path_root) is True:
                i_p = '{}/{}'.format(i_path_root, key)
                i_results = cls.__find_all_results(i_p)
                if i_results:
                    # use first result
                    value = i_results[0]
                    cls.CACHE[key] = value
                    return value

    @classmethod
    def get_all(cls, key):
        for i_path_root in cls.__find_all_roots():
            if os.path.isdir(i_path_root) is True:
                i_p = '{}/{}'.format(i_path_root, key)
                return cls.__find_all_results(i_p)

    @classmethod
    def find_all_file_keys_at(cls, branch, key, ext_includes):
        set_ = set()
        for i_path_root in cls.__find_all_roots():
            i_path_branch = '{}/{}'.format(i_path_root, branch)
            i_path_sub = '{}/{}/{}'.format(i_path_root, branch, key)
            if os.path.isdir(i_path_sub) is True:
                i_all_file_path = cls.__find_all_files(i_path_sub, ext_includes)
                set_.update(map(lambda x: os.path.splitext(x[len(i_path_branch)+1:])[0], i_all_file_path))
        if set_:
            list_ = list(set_)
            list_.sort()
            return list_
        return []

    @classmethod
    def find_all_directory_keys_at(cls, branch, key):
        set_ = set()
        for i_path_root in cls.__find_all_roots():
            i_path_branch = '{}/{}'.format(i_path_root, branch)
            i_path_sub = '{}/{}/{}'.format(i_path_root, branch, key)
            if os.path.isdir(i_path_sub) is True:
                i_all_directory_paths = cls.__find_all_directories(i_path_sub)
                set_.update(map(lambda x: os.path.splitext(x[len(i_path_branch)+1:])[0], i_all_directory_paths))
        if set_:
            list_ = list(set_)
            list_.sort()
            return list_
        return []


class RscIcon(object):
    BRANCH = 'icons'
    ICON_KEY_PATTERN = r'[@](.*?)[@]'

    @classmethod
    def get(cls, key):
        return Resource.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )

    @classmethod
    def get_(cls, key):
        _ = re.findall(
            re.compile(cls.ICON_KEY_PATTERN, re.S), key
        )
        if _:
            cls.get(_)

    @classmethod
    def find_all_keys_at(cls, group_name):
        return Resource.find_all_file_keys_at(
            cls.BRANCH, group_name, ext_includes={'.png', '.svg'}
        )


class RscHook(object):
    BRANCH = 'hooks'

    @classmethod
    def get_yaml(cls, key, search_paths=None):
        return Resource.get(
            '{}/{}.yml'.format(cls.BRANCH, key), search_paths
        )

    @classmethod
    def get_python(cls, key, search_paths=None):
        return Resource.get(
            '{}/{}.py'.format(cls.BRANCH, key), search_paths
        )

    @classmethod
    def get_shell(cls, key, search_paths=None):
        if platform.system() == 'Linux':
            return Resource.get(
                '{}.sh'.format(key), search_paths
            )
        elif platform.system() == 'Windows':
            return cls.get(
                '{}.bat'.format(key)
            )

    @classmethod
    def get_args(cls, key):
        yaml_file_path = cls.get_yaml(key)
        if yaml_file_path:
            configure = ctt_objects.Configure(value=yaml_file_path)
            type_ = configure.get('option.type')
            if type_:
                python_file_path = cls.get_python(key)
                shell_file_path = cls.get_shell(key)
                return type_, key, configure, yaml_file_path, python_file_path, shell_file_path

            log_core.Log.trace_warning(
                'hook file is not valid: "{}"'.format(yaml_file_path)
            )
            return None
        log_core.Log.trace_error(
            'hook file is found: "{}"'.format(key)
        )
        return None
