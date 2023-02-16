# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

import lxsession.commands as ssn_commands

utl_core.Environ.set_add(
    bsc_core.RscFileMtd.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)

user = bsc_core.SystemMtd.get_user_name()

for i_file_path in [
    # '/l/prod/cgm/work/assets/chr/ext_andy/srf/surfacing/maya/scenes/ext_andy.srf.surfacing.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_ben/srf/surfacing/maya/scenes/ext_ben.srf.surfacing.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_burk/srf/surfacing/maya/scenes/ext_burk.srf.surfacing.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_erzi/srf/surfacing/maya/scenes/ext_erzi.srf.surfacing.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_fuzzy/srf/surfacing/maya/scenes/ext_fuzzy.srf.surfacing.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_johnny/srf/surfacing/maya/scenes/ext_johnny.srf.surfacing.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_luo/srf/surfacing/maya/scenes/ext_luo.srf.surfacing.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_mannequin/srf/surfacing/maya/scenes/ext_mannequin.srf.surfacing.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_mike/srf/surfacing/maya/scenes/ext_mike.srf.surfacing.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_owl_a/srf/surfacing/maya/scenes/ext_owl_a.srf.surfacing.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_proketeriat/srf/surfacing/maya/scenes/ext_proketeriat.srf.surfacing.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_suraj/srf/surfacing/maya/scenes/ext_suraj.srf.surfacing.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_woodpecker/srf/surfacing/maya/scenes/ext_woodpecker.srf.surfacing.v001.ma'
]:
    j_option_opt = bsc_core.ArgDictStringOpt(
        option=dict(
            option_hook_key='rsv-task-batchers/asset/maya/surface-export',
            #
            file=i_file_path,
            user=bsc_core.SystemMtd.get_user_name(),
            #
            # td_enable=True,
            rez_beta=True,
        )
    )
    #
    ssn_commands.set_option_hook_execute_by_deadline(
        option=j_option_opt.to_string()
    )
