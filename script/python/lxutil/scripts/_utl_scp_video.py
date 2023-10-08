# coding:utf-8
from lxbasic import bsc_core

import lxutil.extra.methods as utl_etr_methods


class ScpVideo(object):
    @classmethod
    def comp_by_image(cls, file_path):
        user_directory_path = bsc_core.StgTmpBaseMtd.get_user_directory('vedio-converter')
        file_name = bsc_core.UuidMtd.generate_by_text(file_path)
        movie_file_path = '{}/{}.mov'.format(user_directory_path, file_name)
        utl_etr_methods.EtrRv.convert_to_mov(
            input=file_path,
            output=movie_file_path
        )
        return movie_file_path
    @classmethod
    def comp_movie(cls, file_paths):
        if len(file_paths) == 1:
            file_path = file_paths[0]
            file_opt = bsc_core.StgFileOpt(file_path)
            if file_opt.get_ext() == '.mov':
                return file_path
            else:
                return cls.comp_by_image(file_path)
        else:
            movie_file_paths = []
            for i_file_path in file_paths:
                i_file_opt = bsc_core.StgFileOpt(i_file_path)
                if i_file_opt.get_ext() == '.mov':
                    i_movie_file_path = i_file_path
                else:
                    i_movie_file_path = cls.comp_by_image(i_file_path)
                movie_file_paths.append(i_movie_file_path)
            #
            user_directory_path = bsc_core.StgTmpBaseMtd.get_user_directory('vedio-converter')
            file_name = bsc_core.UuidMtd.generate_by_text(
                ' '.join(movie_file_paths)
            )
            movie_file_path = '{}/{}.mov'.format(user_directory_path, file_name)
            utl_etr_methods.EtrRv.convert_to_mov(
                input=movie_file_paths,
                output=movie_file_path
            )
            return movie_file_path


if __name__ == '__main__':
    print ScpVideo.comp_movie(
        [
            '/production/shows/nsa_dev/assets/chr/nikki/user/work.wengmengdi/katana/render/surfacing/nikki.srf.surfacing.v001.asset__default__close_up__night01__custom__all.mov',
            '/production/shows/nsa_dev/assets/chr/nikki/user/work.wengmengdi/katana/render/surfacing/nikki.srf.surfacing.v001.asset__default__close_up__night01__custom__all/primary.####.exr'
        ]
    )
