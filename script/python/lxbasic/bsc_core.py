# coding:utf-8
from lxbasic.core import *


if __name__ == '__main__':
    pass
    # print RawTextOpt('user_data_int').to_rgb_(
    #     s_p=10, v_p=10
    # )
    #
    # os.environ['LYNXI_CONFIGURES'] = '/data/e/myworkspace/td/lynxi/script/configure'
    # print CfgFileMtd.get_yaml('storage/path-mapper')
    # print CfgFileMtd.get_yaml('session/deadline/submiter')
    # print CfgFileMtd.get_yaml('session/deadline/rsv-task-submiter')
    # print CfgFileMtd.get_yaml('katana/node-graph/asset-texture-resource')
    #
    # print CfgFileMtd.get_yaml('colorspace/aces-color')
    #
    # print CfgFileMtd.get_yaml('arnold/node')
    # print CfgFileMtd.get_yaml('arnold/convert')
    #
    # print CfgFileMtd.get_yaml('clarisse/gui/menu')
    #
    # print CfgFileMtd.get_yaml('database/library/resource-basic')
    #
    # print CfgFileMtd.get_yaml('storage/asset-system-workspace')

    # print RawTextMtd.to_integer(
    #     'merge'
    # )
    # print RawTextOpt('abc').to_rgb_()
    #
    # print RscFileMtd.get(
    #     'lua-scripts'
    # )
    # print RawTextOpt(
    #     '1001-1120:5'
    # ).to_frames()

    # print StgPathPermissionBaseMtd.get_mode(
    #     'r-x', 'r-x', 'r-x'
    # )
    # StgPathPermissionMtd.lock_all_directories(
    #     '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/texture/main/v002'
    # )
    # print StgPathPermissionMtd.change_owner('/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/texture/main/v002')

    # StgPathPermissionMtd.change_owner(
    #     '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/texture'
    # )
    # StgPathPermissionMtd.unlock_all_files(
    #     '/job/PLE/bundle/thirdparty/lxdcc_rsc/master-8/script/python/.resources/icons'
    # )
    #
    # print RawTextMtd.to_integer('geometry')
    # print RawTextOpt(
    #     'dreambae'
    # ).to_rgb_0()
    # print RawTextOpt(
    #     'dreambae_nightare'
    # ).to_rgb_0()
    # print RawTextMtd.to_integer(
    #     'l_out_eye_001_hishape'
    # )
    # StgPathPermissionMtd.create_directory(
    #     '/production/library/resource', 777
    # )
    # print ImgFileOpt(
    #     '/production/library/resource/all/atlas/sword_fern_pjvef2/v0001/image/preview.png'
    # ).get_thumbnail(ext='.png')

    # print RscFileMtd.get(
    #     'asset/library/geometry_sphere.usda'
    # )
    # print SystemMtd.get_environment()
    # StgRarFileOpt(
    #     '/l/temp/zeqi/tex/test/DirtWipes 016.rar'
    # ).extract_all_elements_to(
    #     '/l/temp/zeqi/tex/test'
    # )
    for i in [
        'DirtAWipes007',
        'Dirt007AWipes',
        'tube coral_v2 2'
    ]:
        print RawTextMtd.clear_up_to(i)
        print i, RawTextMtd.split_any_to(i)
    # p = '/production/library/resource/all/imperfection/{resource_name}/v001/texture/original/src/{resource_name}.mask.jpg'
    # p_o = PtnParseOpt(p)
    # for i in p_o.get_matches():
    #     i_f_src = i['result']
    #     i_f_o_src = StgFileOpt(i_f_src)
    #     i_n = i_f_o_src.get_name().replace('mask', 'roughness')
    #     i_f_tgt = '{}/{}'.format(i_f_o_src.get_directory_path(), i_n)
    #     ImgFileOpt.r_to_rgb(
    #         i_f_src,
    #         i_f_tgt
    #     )
