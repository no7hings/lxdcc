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
    # print CfgFileMtd.get_yaml('database/library/basic')
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

    # StgPathPermissionMtd.change_mode(
    #     '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/texture', '775'
    # )
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
    ps = ['/cgm', '/cjd', '/shl', '/cg7', '/lib', '/lib_bck', '/nsa_dev', '/tnt', '/']
    print DccPathDagMtd.get_dag_sibling_names(
        '/cgm', ps
    )
