# coding:utf-8
from lxbasic.core import *


if __name__ == '__main__':
    # print RawTextOpt('user_data_int').to_rgb_(
    #     s_p=10, v_p=10
    # )
    #
    if __name__ == '__main__':
        import os

        # os.environ['LYNXI_CONFIGURES'] = '/data/e/myworkspace/td/lynxi/script/configure'
        print CfgFileMtd.get_yaml('storage/path-mapper')
        print CfgFileMtd.get_yaml('session/deadline/submiter')
        print CfgFileMtd.get_yaml('session/deadline/rsv-task-submiter')
        print CfgFileMtd.get_yaml('katana/node-graph/asset-texture-resource')

        print CfgFileMtd.get_yaml('colorspace/aces-color')

        print CfgFileMtd.get_yaml('arnold/node')
        print CfgFileMtd.get_yaml('arnold/convert')

