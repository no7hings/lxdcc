# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects

# t_0 = utl_dcc_objects.OsTexture(
#     '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/v001/bl_xiz_f.diff_clr.<udim>.exr'
# )
#
# print t_0._get_path_args_as_ext_tgt_(
#     t_0.path, '.tx'
# )
#
# t_1 = utl_dcc_objects.OsTexture(
#     '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/v001/bl_xiz_f.diff_clr.<udim>.tx'
# )
#
# print t_1._get_path_args_as_ext_tgt_(
#     t_1.path, '.tx'
# )

# print utl_dcc_objects.OsTexture(
#     '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/v001/bl_xiz_f.diff_clr.<udim>.exr'
# ).get_args_as_ext_tgt(
#     '.tx'
# )
#
# print utl_dcc_objects.OsTexture(
#     '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/v001/bl_xiz_f.diff_clr.<udim>.tx'
# ).get_args_as_ext_tgt(
#     '.tx'
# )
#
#
# print utl_dcc_objects.OsTexture(
#     '/l/temp/td/dongchangbao/tx_convert_test/exr/jiguang_cloth_mask.1001.1001.exr'
# ).get_args_as_ext_tgt(
#     '.tx'
# )
#
# print utl_dcc_objects.OsTexture(
#     '/l/temp/td/dongchangbao/tx_convert_test/exr/jiguang_cloth_mask.<udim>.####.exr'
# ).get_args_as_ext_tgt(
#     '.tx'
# )
#
# print utl_dcc_objects.OsTexture(
#     '/l/temp/td/dongchangbao/tx_convert_test/tx_1/jiguang_cloth_mask.1001.1002.tx'
# ).get_args_as_ext_tgt(
#     '.tx'
# )
#
#
# print utl_dcc_objects.OsTexture(
#     '/l/temp/td/dongchangbao/tx_convert_test/tx_1/jiguang_cloth_mask.<udim>.####.tx'
# ).get_args_as_ext_tgt(
#     '.tx'
# )
#


# utl_dcc_objects.OsTexture(
#     '/l/temp/td/dongchangbao/texture_base_test/exr/jiguang_cloth_mask.1001.1001.exr'
# ).set_unit_copy_as_src(
#     directory_path_src='/l/temp/td/dongchangbao/texture_base_test/base',
#     directory_path_tgt='/l/temp/td/dongchangbao/texture_base_test/tgt'
# )

# utl_dcc_objects.OsTexture(
#     '/l/temp/td/dongchangbao/texture_base_test/exr_0/jiguang_cloth_mask.1001.1001.exr'
# ).set_unit_copy_as_src(
#     directory_path_src='/l/temp/td/dongchangbao/texture_base_test/base',
#     directory_path_tgt='/l/temp/td/dongchangbao/texture_base_test/tgt'
# )
#
# utl_dcc_objects.OsTexture(
#     '/l/temp/td/dongchangbao/texture_base_test/exr/jiguang_cloth_mask.<udim>.####.exr'
# ).set_copy_as_src(
#     directory_path_src='/l/temp/td/dongchangbao/texture_base_test/base',
#     directory_path_tgt='/l/temp/td/dongchangbao/texture_base_test/tgt'
# )

# utl_dcc_objects.OsTexture(
#     '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/src/bl_xiz_f.diff_clr.<udim>.exr'
# ).get_args_as_ext_tgt_by_directory_args(
#     '.tx',
#     (
#         '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/src',
#         '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/tx'
#     )
# )
#
# utl_dcc_objects.OsTexture(
#     '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/tx/bl_xiz_f.diff_clr.<udim>.tx'
# ).get_args_as_ext_tgt_by_directory_args(
#     '.tx',
#     (
#         '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/src',
#         '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/tx'
#     )
# )

# print utl_dcc_objects.OsTexture(
#     '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/tx/bl_xiz_f.metal.<udim>.tx'
# ).get_args_as_ext_tgt_by_directory_args(
#     '.tx',
#     (
#         '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/src',
#         '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/tx'
#     )
# )

print utl_dcc_objects.OsTexture(
    '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/src/nn4y_eye.normal.1001.exr'
).get_args_as_tx_by_directory_args(
    ('/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/src', '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/tx')
)



