# coding:utf-8
import sys

import os

from ..core import base as bsc_cor_base


class EnvBaseMtd(object):
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
    def get_is_beta_enable(cls):
        _ = cls.get('REZ_BETA')
        if _ == '1':
            return True
        return False

    #
    @classmethod
    def get_temporary_root(cls):
        _ = cls.get(cls.TEMPORARY_ROOT_KEY)
        if _ is not None:
            return bsc_cor_base.StgBasePathMapMtd.map_to_current(_)
        return bsc_cor_base.StgBasePathMapMtd.map_to_current(cls.TEMPORARY_ROOT_DEFAULT)

    @classmethod
    def set_temporary_path(cls, path):
        cls.set(cls.TEMPORARY_ROOT_KEY, path)

    @classmethod
    def get_session_root(cls):
        _ = cls.get(cls.SESSION_ROOT_KEY)
        if _ is not None:
            return bsc_cor_base.StgBasePathMapMtd.map_to_current(_)
        return bsc_cor_base.StgBasePathMapMtd.map_to_current(cls.SESSION_ROOT_DEFAULT)

    @classmethod
    def get_database_path(cls):
        _ = cls.get(cls.DATABASE_PATH_KEY)
        if _ is not None:
            return bsc_cor_base.StgBasePathMapMtd.map_to_current(_)
        return bsc_cor_base.StgBasePathMapMtd.map_to_current(cls.DATABASE_PATH_DEFAULT)

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
    def append(cls, key, value):
        if key in os.environ:
            v = os.environ[key]
            if value not in v:
                os.environ[key] += os.pathsep+value
        else:
            os.environ[key] = value

    @classmethod
    def set_python_add(cls, path):
        python_paths = sys.path
        if path not in python_paths:
            sys.path.insert(0, path)

    @classmethod
    def get_qt_thread_enable(cls):
        if bsc_cor_base.SysApplicationMtd.get_is_maya():
            return False
        return True

    @classmethod
    def append_lua_path(cls, path):
        key = 'LUA_PATH'
        value = cls.get(key)
        if value:
            if path not in value:
                value += path+';'
                cls.set(key, value)

    @classmethod
    def find_all_executes(cls, name):
        _ = cls.get_as_array('PATH')
        list_ = []
        for i in _:
            i_f = '{}/{}'.format(i, name)
            if os.path.isfile(i_f):
                list_.append(i_f)
        return list_

    @classmethod
    def find_execute(cls, name):
        _ = cls.get_as_array('PATH')
        for i in _:
            i_f = '{}/{}'.format(i, name)
            if os.path.isfile(i_f):
                return i_f


class EnvContentOpt(object):
    def __init__(self, environs):
        self.__raw = environs

    def set(self, key, value):
        self.__raw[key] = value

    def append(self, key, value):
        if key in self.__raw:
            v = self.__raw[key]
            if value not in v:
                self.__raw[key] += os.pathsep+value
        else:
            self.__raw[key] = value

    def prepend(self, key, value):
        if key in self.__raw:
            v = self.__raw[key]
            if value not in v:
                self.__raw[key] = value+os.pathsep+self.__raw[key]
        else:
            self.__raw[key] = value


class EnvExtraMtd(EnvBaseMtd):
    SCHEME_KEY = 'LYNXI_SCHEME'
    BETA_ENABLE_KEY = 'LYNXI_BETA_ENABLE'
    TD_ENABLE_KEY = 'LYNXI_TD_ENABLE'
    LOG_ROOT_KEY = 'LYNXI_LOG_ROOT'

    @classmethod
    def get_scheme(cls):
        return cls.get(cls.SCHEME_KEY)

    @classmethod
    def get_beta_enable(cls):
        _ = cls.get(cls.BETA_ENABLE_KEY)
        if str(_).lower() == cls.TRUE:
            return True
        return False

    @classmethod
    def set_beta_enable(cls, boolean):
        if boolean is True:
            cls.set(cls.BETA_ENABLE_KEY, cls.TRUE)
        else:
            cls.set(cls.BETA_ENABLE_KEY, cls.FALSE)

    @classmethod
    def get_is_td_enable(cls):
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
