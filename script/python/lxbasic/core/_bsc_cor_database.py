# coding:utf-8
from ._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_environ, _bsc_cor_storage


class DtbFileMtd(object):
    @classmethod
    def get_key(cls, data):
        return HashMtd.get_hash_value(
            data, as_unique_id=True
        )
    @classmethod
    def _get_file_path_(cls, key, category):
        directory_path = _bsc_cor_environ.EnvironMtd.get_database_path()
        region = _bsc_cor_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/{}/{}/{}'.format(directory_path, category, region, key)
    @classmethod
    def get_value(cls, key, category):
        file_path = cls._get_file_path_(key, category)
        gzip_file = _bsc_cor_storage.StgGzipFileOpt(file_path, '.yml')
        if gzip_file.get_is_exists() is True:
            return gzip_file.set_read()
    @classmethod
    def set_value(cls, key, value, force, category):
        file_path = cls._get_file_path_(key, category)
        gzip_file = _bsc_cor_storage.StgGzipFileOpt(file_path, '.yml')
        if gzip_file.get_is_exists() is False or force is True:
            gzip_file.set_write(value)
            return True


class DtbGeometryUvMapFileMtd(object):
    @classmethod
    def get_value(cls, key):
        return DtbFileMtd.get_value(
            key,
            category='geometry/uv-map'
        )
    @classmethod
    def set_value(cls, key, value, force):
        return DtbFileMtd.set_value(
            key,
            value,
            force,
            category='geometry/uv-map'
        )
