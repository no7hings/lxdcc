# coding:utf-8
from lxbasic import bsc_core

from lxarnold import and_setup

s = and_setup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019')
s.set_run()
# xgen lib
s._set_environ_add_('LD_LIBRARY_PATH', '/l/packages/pg/prod/maya/2019.2/platform-linux/Application/plug-ins/xgen/lib')
s._set_environ_add_('LD_LIBRARY_PATH', '/l/packages/pg/prod/maya/2019.2/platform-linux/Application/lib')

bsc_core.EnvironMtd.set(
    'OCIO', '/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'
)

if __name__ == '__main__':
    from lxarnold import and_core

    from lxbasic import bsc_core

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    # utl_dcc_objects.OsTexture._create_unit_exr_as_acescg_(
    #     '/l/resource/library/texture/all/surface/rough_concrete_ogioE0/v0001/texture/test/src/rough_concrete_ogioE0.displacement.lin_srgb.exr',
    #     '/l/resource/library/texture/all/surface/rough_concrete_ogioE0/v0001/texture/test/acescg/rough_concrete_ogioE0.displacement.exr',
    # )

    # utl_dcc_objects.OsTexture._convert_unit_format_(
    #     '/l/resource/library/texture/all/surface/rough_concrete_ogioE0/v0001/texture/test/test.roughness.exr',
    #     '/l/resource/library/texture/all/surface/rough_concrete_ogioE0/v0001/texture/test/test2.acescg.roughness.exr',
    #     'Utility - Linear - sRGB',
    #     'ACES - ACEScg'
    # )

    directory_path_src = '/l/resource/library/texture/all/surface/rough_concrete_ogioE0/v0001/texture/original/src'
    directory_path_tgt = '/l/resource/library/texture/all/surface/rough_concrete_ogioE0/v0001/texture/acescg/src'

    bsc_core.StgDirectoryOpt_(directory_path_tgt).set_create()

    d_original_src_opt = bsc_core.StgDirectoryOpt(directory_path_src)
    d_acescg_src_opt = bsc_core.StgDirectoryOpt(directory_path_tgt)
    d_acescg_src_opt.set_create()

    jpg_file_paths = d_original_src_opt.get_all_file_paths(
        include_exts=['.jpg']
    )
    jpg_file_path_mapper = bsc_core.StorageBaseMtd.to_file_deduplication_mapper(jpg_file_paths)
    exr_file_paths = d_original_src_opt.get_all_file_paths(
        include_exts=['.exr']
    )
    exr_file_path_mapper = bsc_core.StorageBaseMtd.to_file_deduplication_mapper(exr_file_paths)

    for k, v in jpg_file_path_mapper.items():
        if k in exr_file_path_mapper:
            i_file_path_src = exr_file_path_mapper[k]
        else:
            i_file_path_src = v
        #
        i_file_opt_src = bsc_core.StgFileOpt(i_file_path_src)
        i_file_path_tgt = '{}/{}.exr'.format(directory_path_tgt, i_file_opt_src.name_base)
        #
        utl_dcc_objects.OsTexture._create_unit_exr_as_acescg_(
            i_file_path_src,
            i_file_path_tgt,
        )
