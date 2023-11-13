# coding:utf-8
import lxresource.core as rsc_core

from lxbasic.core import _bsc_cor_utility, _bsc_cor_storage


class StgPathMapper(object):
    PATHSEP = '/'
    #
    MAPPER = _bsc_cor_storage.StgPathMapDict(
        _bsc_cor_storage.StgFileOpt(
            rsc_core.RscConfigure.get_yaml('storage/path-mapper')
        ).set_read()
    )

    @classmethod
    def map_to_current(cls, path):
        if path is not None:
            if _bsc_cor_utility.SystemMtd.get_is_windows():
                return cls.map_to_windows(path)
            elif _bsc_cor_utility.SystemMtd.get_is_linux():
                return cls.map_to_linux(path)
            return _bsc_cor_storage.StgPathOpt(path).__str__()
        return path

    @classmethod
    def map_to_windows(cls, path):
        # clear first
        path = _bsc_cor_storage.StgPathOpt(path).__str__()
        if _bsc_cor_storage.StorageMtd.get_path_is_linux(path):
            mapper_dict = cls.MAPPER._windows_dict
            for i_root_src, i_root_tgt in mapper_dict.items():
                if path == i_root_src:
                    return i_root_tgt
                elif path.startswith(i_root_src+cls.PATHSEP):
                    return i_root_tgt+path[len(i_root_src):]
            return path
        return path

    @classmethod
    def map_to_linux(cls, path):
        """
print Path.map_to_linux(
    'l:/a'
)
        :param path:
        :return:
        """
        # clear first
        path = _bsc_cor_storage.StgPathOpt(path).__str__()
        if _bsc_cor_storage.StorageMtd.get_path_is_windows(path):
            mapper_dict = cls.MAPPER._linux_dict
            for i_root_src, i_root_tgt in mapper_dict.items():
                if path == i_root_src:
                    return i_root_tgt
                elif path.startswith(i_root_src+cls.PATHSEP):
                    return i_root_tgt+path[len(i_root_src):]
            return path
        return path


class StgEnvPathMapper(object):
    MAPPER = _bsc_cor_storage.StgEnvPathMapDict(
        _bsc_cor_storage.StgFileOpt(
            rsc_core.RscConfigure.get_yaml('storage/path-environment-mapper')
        ).set_read()
    )

    @classmethod
    def map_to_path(cls, path, pattern='[KEY]'):
        """
        print(
            PathEnv.map_to_path(
                '[PAPER_PRODUCTION_ROOT]/nsa_dev/assets/chr/td_test/user/team.srf/extend/look/klf/v001/all.json',
                pattern='[KEY]'
            )
        )
        print(
            PathEnv.map_to_path(
                '${PAPER_PRODUCTION_ROOT}/nsa_dev/assets/chr/td_test/user/team.srf/extend/look/klf/v001/all.json',
                pattern='${KEY}'
            )
        )
        :param path:
        :param pattern:
        :return:
        """
        path = _bsc_cor_storage.StgPathOpt(path).__str__()
        mapper_dict = cls.MAPPER._env_dict
        for i_env_key, i_root in mapper_dict.items():
            i_string = pattern.replace('KEY', i_env_key)
            if path == i_string:
                return i_root
            elif path.startswith(i_string+'/'):
                return i_root+path[len(i_string):]
        return path

    @classmethod
    def map_to_env(cls, path, pattern='[KEY]'):
        """
        print(
            PathEnv.map_to_env(
                '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/look/klf/v001/all.json',
                pattern='[KEY]'
            ),
        )
        print(
            PathEnv.map_to_env(
                '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/look/klf/v001/all.json',
                pattern='${KEY}'
            )
        )
        :param path:
        :param pattern:
        :return:
        """
        path = _bsc_cor_storage.StgPathOpt(path).__str__()
        mapper_dict = cls.MAPPER._path_dict
        for i_root, i_env_key in mapper_dict.items():
            i_string = pattern.replace('KEY', i_env_key)
            if path == i_root:
                return i_string
            elif path.startswith(i_root+'/'):
                return i_string+path[len(i_root):]
        return path
