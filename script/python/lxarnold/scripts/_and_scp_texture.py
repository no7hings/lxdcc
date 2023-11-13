# coding:utf-8
from lxbasic import bsc_core

from lxarnold import and_setup

import lxutil.dcc.dcc_objects as utl_dcc_objects


class ScpTextureCreate(object):
    def __init__(self):
        pass
    @staticmethod
    def setup():
        # arnold
        s = and_setup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019')
        s.set_run()
        # xgen lib
        s.add_environ_fnc(
            'LD_LIBRARY_PATH', '/l/packages/pg/prod/maya/2019.2/platform-linux/Application/plug-ins/xgen/lib'
        )
        s.add_environ_fnc(
            'LD_LIBRARY_PATH', '/l/packages/pg/prod/maya/2019.2/platform-linux/Application/lib'
        )
        # ocio
        bsc_core.EnvironMtd.set(
            'OCIO', '/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'
        )
    @classmethod
    def to_exr_by_directory_as_acescg(cls, directory_path_src, directory_path_tgt, formats=None, use_update_mode=True):
        bsc_core.StgDirectoryOptExtra(directory_path_tgt).set_create()
        #
        directory_opt_src = bsc_core.StgDirectoryOpt(directory_path_src)
        directory_opt_tgt = bsc_core.StgDirectoryOpt(directory_path_tgt)
        directory_opt_tgt.set_create()
        #
        file_paths_src = directory_opt_src.get_all_file_paths(
            ext_includes=map(lambda x: '.{}'.format(x), formats)
        )
        file_paths_src = bsc_core.StorageMtd.deduplication_files_by_formats(
            file_paths_src, formats
        )
        # bsc_core.FncThread()
        for i_index, i_file_path_src in enumerate(file_paths_src):
            i_file_opt_src = bsc_core.StgFileOpt(i_file_path_src)
            i_file_path_tgt = '{}/{}.exr'.format(directory_path_tgt, i_file_opt_src.name_base)

            bsc_core.TrdFunction.set_wait()
            bsc_core.TrdFunction.set_start(
                cls.to_exr_as_acescg, i_index,
                # args
                i_file_path_src, i_file_path_tgt,
                # kwargs
                use_update_mode=use_update_mode
            )
    @classmethod
    def to_exr_as_acescg(cls, file_path_src, file_path_tgt, use_update_mode=True):
        utl_dcc_objects.OsTexture._create_unit_exr_as_acescg_(
            file_path_src,
            file_path_tgt,
            use_update_mode=use_update_mode
        )
    #
    @classmethod
    def get_exr_create_data_by_directory(cls, directory_path_src, formats=None):
        list_ = []
        #
        directory_opt_src = bsc_core.StgDirectoryOpt(directory_path_src)
        #
        file_paths_src = directory_opt_src.get_all_file_paths(
            ext_includes=map(lambda x: '.{}'.format(x), formats)
        )
        file_paths_src = bsc_core.StorageMtd.deduplication_files_by_formats(
            file_paths_src, formats
        )
        for i_index, i_file_path_src in enumerate(file_paths_src):
            list_.append(i_file_path_src)
        return list_
    #
    @classmethod
    def get_exr_create_cmds_by_directory_as_acescg(cls, directory_path_src, directory_path_tgt, formats=None, use_update_mode=True):
        list_ = []
        bsc_core.StgDirectoryOptExtra(directory_path_tgt).set_create()
        #
        directory_opt_src = bsc_core.StgDirectoryOpt(directory_path_src)
        directory_opt_tgt = bsc_core.StgDirectoryOpt(directory_path_tgt)
        directory_opt_tgt.set_create()
        #
        file_paths_src = directory_opt_src.get_all_file_paths(
            ext_includes=map(lambda x: '.{}'.format(x), formats)
        )
        file_paths_src = bsc_core.StorageMtd.deduplication_files_by_formats(
            file_paths_src, formats
        )
        for i_index, i_file_path_src in enumerate(file_paths_src):
            i_file_opt_src = bsc_core.StgFileOpt(i_file_path_src)
            i_file_path_tgt = '{}/{}.exr'.format(directory_path_tgt, i_file_opt_src.name_base)
            list_.append(
                cls.get_exr_create_cmd_as_acescg(i_file_path_src, i_file_path_tgt, use_update_mode=use_update_mode)
            )
        return list_
    @classmethod
    def get_exr_create_cmd_as_acescg(cls, file_path_src, file_path_tgt, use_update_mode=True):
        return utl_dcc_objects.OsTexture._get_unit_exr_create_cmd_as_acescg_(
            file_path_src,
            file_path_tgt,
            use_update_mode=use_update_mode
        )
    # tx
    @classmethod
    def to_tx_by_directory_as_acescg(cls, directory_path_src, directory_path_tgt, formats=None, use_update_mode=True):
        bsc_core.StgDirectoryOptExtra(directory_path_tgt).set_create()
        #
        directory_opt_src = bsc_core.StgDirectoryOpt(directory_path_src)
        directory_opt_tgt = bsc_core.StgDirectoryOpt(directory_path_tgt)
        directory_opt_tgt.set_create()
        #
        file_paths_src = directory_opt_src.get_all_file_paths(
            ext_includes=map(lambda x: '.{}'.format(x), formats)
        )
        file_paths_src = bsc_core.StorageMtd.deduplication_files_by_formats(
            file_paths_src, formats
        )
        #
        for i_index, i_file_path_src in enumerate(file_paths_src):
            i_file_opt_src = bsc_core.StgFileOpt(i_file_path_src)
            i_file_path_tgt = '{}/{}.tx'.format(directory_path_tgt, i_file_opt_src.name_base)

            bsc_core.TrdFunction.set_wait()
            bsc_core.TrdFunction.set_start(
                cls.to_tx_as_acescg, i_index,
                # args
                i_file_path_src, i_file_path_tgt,
                # kwargs
                use_update_mode=use_update_mode
            )
    @classmethod
    def to_tx_as_acescg(cls, file_path_src, file_path_tgt, use_update_mode=True):
        utl_dcc_objects.OsTexture._create_unit_tx_as_acescg_(
            file_path_src,
            file_path_tgt,
            use_update_mode=use_update_mode
        )
    @classmethod
    def get_tx_create_cmds_by_directory_as_acescg(cls, directory_path_src, directory_path_tgt, formats=None, use_update_mode=True):
        list_ = []
        bsc_core.StgDirectoryOptExtra(directory_path_tgt).set_create()
        #
        directory_opt_src = bsc_core.StgDirectoryOpt(directory_path_src)
        directory_opt_tgt = bsc_core.StgDirectoryOpt(directory_path_tgt)
        directory_opt_tgt.set_create()
        #
        file_paths_src = directory_opt_src.get_all_file_paths(
            ext_includes=map(lambda x: '.{}'.format(x), formats)
        )
        file_paths_src = bsc_core.StorageMtd.deduplication_files_by_formats(
            file_paths_src, formats
        )
        #
        for i_index, i_file_path_src in enumerate(file_paths_src):
            i_file_opt_src = bsc_core.StgFileOpt(i_file_path_src)
            i_file_path_tgt = '{}/{}.tx'.format(directory_path_tgt, i_file_opt_src.name_base)
            list_.append(
                cls.get_tx_create_cmd_as_acescg(i_file_path_src, i_file_path_tgt, use_update_mode=use_update_mode)
            )
        return list_
    @classmethod
    def get_tx_create_cmd_as_acescg(cls, file_path_src, file_path_tgt, use_update_mode=True):
        return utl_dcc_objects.OsTexture._get_unit_tx_create_cmd_as_acescg_(
            file_path_src,
            file_path_tgt,
            use_update_mode=use_update_mode
        )


if __name__ == '__main__':
    scp = ScpTextureCreate()

    scp.setup()

    d = '/l/resource/library/texture/all/surface/fort_damaged_floor_te3maaeg/v0001/texture'

    cmds = scp.get_exr_create_cmds_by_directory_as_acescg(
        '{}/original/src'.format(d),
        '{}/acescg/src'.format(d),
        formats=['exr', 'tiff', 'png', 'jpg']
    )

    # d = '/l/resource/library/texture/all/surface/fort_damaged_floor_te3maaeg/v0001/texture/acescg'
    #
    # scp.to_tx_by_directory_as_acescg(
    #     '{}/src'.format(d),
    #     '{}/tx'.format(d),
    #     formats=['exr', 'tiff', 'png', 'jpg']
    # )

    # utl_dcc_objects.OsTexture._create_unit_tx_as_acescg_(
    #     '/l/resource/library/texture/all/surface/rough_concrete_sbqkmjp0/v0001/texture/acescg/src/rough_concrete_sbqkmjp0.albedo.exr',
    #     '/l/resource/library/texture/all/surface/rough_concrete_sbqkmjp0/v0001/texture/acescg/tx/rough_concrete_sbqkmjp0.albedo.tx',
    # )


