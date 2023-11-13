# coding:utf-8
from lxutil.core import *


if __name__ == '__main__':
    print ctt_objects.Configure(
        value=bsc_core.StgFileOpt(
            bsc_core.RscConfigure.get_yaml('storage/path-mapper')
        ).set_read()
    )
    print(
        bsc_core.StgEnvPathMapper.map_to_path(
            '[PAPER_PRODUCTION_ROOT]/nsa_dev/assets/chr/td_test/user/team.srf/extend/look/klf/v001/all.json',
            pattern='[KEY]'
        )
    )
    print(
        bsc_core.StgEnvPathMapper.map_to_env(
            '/production/shows',
            pattern='[KEY]'
        )
    )
