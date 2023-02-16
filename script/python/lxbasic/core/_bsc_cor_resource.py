# coding:utf-8
from lxbasic.core._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_environ, _bsc_cor_storage


class RscFileMtd(object):
    CACHE = {}
    CACHE_ALL = {}
    ENVIRON_KEY = 'LYNXI_RESOURCES'
    @classmethod
    def get_search_directories(cls):
        return _bsc_cor_environ.EnvironMtd.get_as_array(
            cls.ENVIRON_KEY
        )
    @classmethod
    def get(cls, key):
        """
        :param key: str, etc. "rsv-task-batchers/asset/gen-model-export-extra" or "*/gen-model-export-extra"
        :return: str(path)
        """
        if key in cls.CACHE:
            return cls.CACHE[key]
        else:
            for i_path in cls.get_search_directories():
                i_path_opt = _bsc_cor_storage.StgPathOpt(i_path)
                if i_path_opt.get_is_exists() is True:
                    i_glob_pattern = '{}/{}'.format(i_path_opt.path, key)
                    i_results = _bsc_cor_storage.StgExtraMtd.get_paths_by_fnmatch_pattern(
                        i_glob_pattern
                    )
                    if i_results:
                        # use first result
                        value = i_results[0]
                        cls.CACHE[key] = value
                        return value
    @classmethod
    def get_all(cls, key):
        for i_path in cls.get_search_directories():
            i_path_opt = _bsc_cor_storage.StgPathOpt(i_path)
            if i_path_opt.get_is_exists() is True:
                i_glob_pattern = '{}/{}'.format(i_path_opt.path, key)
                i_results = _bsc_cor_storage.StgExtraMtd.get_paths_by_fnmatch_pattern(
                    i_glob_pattern
                )
                return i_results


class RscIconFileMtd(object):
    BRANCH = 'icons'
    ICON_KEY_PATTERN = r'[@](.*?)[@]'
    @classmethod
    def get(cls, key):
        return RscFileMtd.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )
    @classmethod
    def get_(cls, key):
        _ = re.findall(
            re.compile(cls.ICON_KEY_PATTERN, re.S), key
        )
        if _:
            cls.get(_)
