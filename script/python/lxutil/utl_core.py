# coding:utf-8
from lxutil.core import *


if __name__ == '__main__':
    # Log.set_trace('测试')
    # Log.set_result_trace('测试')
    # Log.set_module_result_trace('test', '测试', 'a')
    # with LogProgressRunner.create_as_bar(maximum=10, label='test') as l_p:
    #     for i in range(10):
    #         l_p.set_update()
    print ctt_objects.Configure(
        value=bsc_core.StgFileOpt(
            bsc_core.CfgFileMtd.get_yaml('storage/path-mapper')
        ).set_read()
    )
    print(
        PathEnv.map_to_path(
            '[PAPER_PRODUCTION_ROOT]/nsa_dev/assets/chr/td_test/user/team.srf/extend/look/klf/v001/all.json',
            pattern='[KEY]'
        )
    )
    print(
        PathEnv.map_to_env(
            '/production/shows',
            pattern='[KEY]'
        )
    )