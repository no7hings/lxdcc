# coding:utf-8
import lxbasic.core as bsc_core


class ScpTextureResourceData(object):
    TextureTypes = bsc_core.BscTextureTypes

    def __init__(self, directory_path):
        self._directory_path = directory_path

    def get_data(self):
        dict_ = {}
        directory_opt = bsc_core.StgDirectoryOpt(self._directory_path)
        texture_paths = directory_opt.get_all_file_paths(ext_includes=['.tx'])

        name_p_opt = bsc_core.PtnParseOpt(
            '{name}.{key}'
        )

        for i_texture_path in texture_paths:
            i_texture_opt = bsc_core.StgFileOpt(i_texture_path)
            i_name_base = i_texture_opt.name_base
            i_variants = name_p_opt.get_variants(i_name_base)
            if i_variants:
                i_key = i_variants['key']
                if i_key in self.TextureTypes.Arnold.Mapper:
                    i_key = self.TextureTypes.Arnold.Mapper[i_key]
                #
                if i_key in self.TextureTypes.Arnold.All:
                    dict_[i_key] = i_texture_opt.get_path()

        return dict_


if __name__ == '__main__':
    print ScpTextureResourceData(
        '/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/tx'
    ).get_data()
