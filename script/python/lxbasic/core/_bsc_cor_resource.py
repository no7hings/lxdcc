# coding:utf-8
import os

from lxbasic.core._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_environ, _bsc_cor_storage


class RscFileMtd(object):
    CACHE = {}
    ENVIRON_KEY = 'PAPER_EXTEND_RESOURCES'

    @classmethod
    def get_search_directories(cls):
        return _bsc_cor_environ.EnvironMtd.get_as_array(
            cls.ENVIRON_KEY
        )

    @classmethod
    def get(cls, key, search_paths=None):
        """
        :param key: str
        :param search_paths: list
        :return: str(path)
        """
        if key in cls.CACHE:
            return cls.CACHE[key]
        else:
            if isinstance(search_paths, (tuple, list)):
                paths = search_paths
            else:
                paths = cls.get_search_directories()
            #
            for i_path in paths:
                i_path_opt = _bsc_cor_storage.StgPathOpt(i_path)
                i_path_opt.map_to_current()
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

    @classmethod
    def get_all_keys_at(cls, branch, key, ext_includes):
        set_ = set()
        for i_path_root in cls.get_search_directories():
            i_path_branch = '{}/{}'.format(i_path_root, branch)
            i_path = '{}/{}/{}'.format(i_path_root, branch, key)
            i_path_opt = _bsc_cor_storage.StgDirectoryOpt(i_path)
            if i_path_opt.get_is_directory() is True:
                all_file_paths = i_path_opt.get_all_file_paths(ext_includes)
                set_.update(map(lambda x: os.path.splitext(x[len(i_path_branch)+1:])[0], all_file_paths))
        list_ = list(set_)
        list_.sort()
        return list_


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

    @classmethod
    def get_all_keys_at(cls, key):
        return RscFileMtd.get_all_keys_at(
            cls.BRANCH, key, ext_includes={'.png', '.svg'}
        )


if __name__ == '__main__':
    print RscFileMtd.get('fonts/Arial.ttf')
