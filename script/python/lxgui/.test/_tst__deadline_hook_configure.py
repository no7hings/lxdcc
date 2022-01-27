# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

utl_core.Environ.set_add(
    utl_core.Resources.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)

option = bsc_core.KeywordArgumentsMtd.to_string(
    **dict(
        # hook option
        option_hook_key='rsv-task-methods/asset/maya/geometry-export',
        # task option
        project='lib', asset='ast_cjd_didi', step='srf', task='srf_anishading', version='v003',
        batch_file='/l/prod/lib/publish/assets/chr/ast_cjd_didi/srf/srf_anishading/ast_cjd_didi.srf.srf_anishading.v003/scene/ast_cjd_didi.ma',
        # user+time_tag
        user='dongchangbao', time_tag='2022_0104_1942_52',
        # python option
        file='/l/prod/lib/publish/assets/chr/ast_cjd_didi/srf/srf_anishading/ast_cjd_didi.srf.srf_anishading.v003/scene/ast_cjd_didi.ma',
        td_enable=True,
    )
)

import lxsession.commands as ssn_commands

session, fnc = ssn_commands.get_option_hook_args(
    option
)
