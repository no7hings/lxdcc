# coding:utf-8
from lxbasic import bsc_core


class ScpTextureResourceData(object):
    def __init__(self, directory_path):
        self._directory_path = directory_path

    def get_data(self):
        dict_ = {}
        directory_opt = bsc_core.StgDirectoryOpt(self._directory_path)

        texture_paths = directory_opt.get_all_file_paths(include_exts=['.tx'])

        p = bsc_core.PtnParseOpt(
            '{name}.{key}'
        )

        for i_texture_path in texture_paths:
            i_texture_opt = bsc_core.StgFileOpt(i_texture_path)
            i_name_base = i_texture_opt.name_base
            i_variants = p.get_variants(i_name_base)
            if i_variants:
                i_key = i_variants['key']
                dict_[i_key] = i_texture_opt.get_path()

        return dict_
