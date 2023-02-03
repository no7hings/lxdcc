# coding:utf-8
from ._bsc_cor_utility import *


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
    def get_rez_beta(cls):
        _ = cls.get('REZ_BETA')
        if _ == '1':
            return True
        return False
    @classmethod
    def get_temporary_root(cls):
        _ = cls.get(cls.TEMPORARY_ROOT_KEY)
        if _ is not None:
            return StorageBaseMtd.set_map_to_platform(_)
        return StorageBaseMtd.set_map_to_platform(cls.TEMPORARY_ROOT_DEFAULT)
    @classmethod
    def set_temporary_path(cls, path):
        cls.set(cls.TEMPORARY_ROOT_KEY, path)
    @classmethod
    def get_session_root(cls):
        _ = cls.get(cls.SESSION_ROOT_KEY)
        if _ is not None:
            return StorageBaseMtd.set_map_to_platform(_)
        return StorageBaseMtd.set_map_to_platform(cls.SESSION_ROOT_DEFAULT)
    @classmethod
    def get_database_path(cls):
        _ = cls.get(cls.DATABASE_PATH_KEY)
        if _ is not None:
            return StorageBaseMtd.set_map_to_platform(_)
        return StorageBaseMtd.set_map_to_platform(cls.DATABASE_PATH_DEFAULT)
    @classmethod
    def get_data_paths(cls):
        pass
    @classmethod
    def get(cls, key):
        return os.environ.get(key)
    @classmethod
    def get_as_array(cls, key):
        if key in os.environ:
            _ = os.environ[key]
            if _:
                return _.split(os.pathsep)
        return []
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
    @classmethod
    def get_qt_thread_enable(cls):
        if ApplicationMtd.get_is_maya():
            return False
        return True


class EnvironsOpt(object):
    def __init__(self, environs):
        self._environs = environs

    def set(self, key, value):
        self._environs[key] = value

    def set_add(self, key, value):
        if key in self._environs:
            v = self._environs[key]
            if value not in v:
                self._environs[key] += os.pathsep + value
        else:
            self._environs[key] = value