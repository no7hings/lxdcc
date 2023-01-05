# coding:utf-8
from lxbasic import bsc_core

from lxarnold import and_setup

import lxutil.dcc.dcc_objects as utl_dcc_objects


class TextureConvertScript(object):
    def __init__(self):
        pass
    @staticmethod
    def setup():
        # arnold
        s = and_setup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019')
        s.set_run()
        # xgen lib
        s._set_environ_add_(
            'LD_LIBRARY_PATH', '/l/packages/pg/prod/maya/2019.2/platform-linux/Application/plug-ins/xgen/lib'
        )
        s._set_environ_add_(
            'LD_LIBRARY_PATH', '/l/packages/pg/prod/maya/2019.2/platform-linux/Application/lib'
        )
        # ocio
        bsc_core.EnvironMtd.set(
            'OCIO', '/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'
        )
    @staticmethod
    def to_acescg_exr(directory_path_src, directory_path_tgt):
        bsc_core.DirectoryOpt(directory_path_tgt).set_create()
        #
        directory_opt_src = bsc_core.StorageDirectoryOpt(directory_path_src)
        directory_opt_tgt = bsc_core.StorageDirectoryOpt(directory_path_tgt)
        directory_opt_tgt.set_create()
        #
        jpg_file_paths_src = directory_opt_src.get_all_file_paths(
            include_exts=['.jpg']
        )
        jpg_file_path_mapper_src = bsc_core.StoragePathMtd.to_deduplication_mapper(jpg_file_paths_src)
        exr_file_paths = directory_opt_src.get_all_file_paths(
            include_exts=['.exr']
        )
        exr_file_path_mapper_src = bsc_core.StoragePathMtd.to_deduplication_mapper(exr_file_paths)
        jpg_file_path_mapper_src.update(exr_file_path_mapper_src)
        #
        for k, v in jpg_file_path_mapper_src.items():
            i_file_path_src = v
            #
            i_file_opt_src = bsc_core.StorageFileOpt(i_file_path_src)
            i_file_path_tgt = '{}/{}.exr'.format(directory_path_tgt, i_file_opt_src.name_base)
            #
            utl_dcc_objects.OsTexture._convert_unit_format_as_acescg_(
                i_file_path_src,
                i_file_path_tgt,
            )
    @staticmethod
    def to_acescg_tx(directory_path_src, directory_path_tgt):
        bsc_core.DirectoryOpt(directory_path_tgt).set_create()
        #
        directory_opt_src = bsc_core.StorageDirectoryOpt(directory_path_src)
        directory_opt_tgt = bsc_core.StorageDirectoryOpt(directory_path_tgt)
        directory_opt_tgt.set_create()
        #
        jpg_file_paths_src = directory_opt_src.get_all_file_paths(
            include_exts=['.jpg']
        )
        jpg_file_path_mapper_src = bsc_core.StoragePathMtd.to_deduplication_mapper(jpg_file_paths_src)
        exr_file_paths = directory_opt_src.get_all_file_paths(
            include_exts=['.exr']
        )
        exr_file_path_mapper_src = bsc_core.StoragePathMtd.to_deduplication_mapper(exr_file_paths)
        jpg_file_path_mapper_src.update(exr_file_path_mapper_src)
        #
        for k, v in jpg_file_path_mapper_src.items():
            i_file_path_src = v
            #
            i_file_opt_src = bsc_core.StorageFileOpt(i_file_path_src)
            i_file_path_tgt = '{}/{}.tx'.format(directory_path_tgt, i_file_opt_src.name_base)

            utl_dcc_objects.OsTexture._create_unit_tx_as_acescg_(
                i_file_path_src,
                i_file_path_tgt,
            )


if __name__ == '__main__':
    scp = TextureConvertScript()

    scp.setup()

    d = '/l/resource/library/texture/all/surface/rough_concrete_sbqkmjp0/v0001/texture'

    # scp.to_acescg_exr(
    #     '{}/original/src'.format(d),
    #     '{}/acescg/src'.format(d)
    # )

    scp.to_acescg_tx(
        '{}/acescg/src'.format(d),
        '{}/acescg/tx'.format(d)
    )


