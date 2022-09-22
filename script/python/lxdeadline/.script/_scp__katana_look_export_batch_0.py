# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

import lxresolver.commands as rsv_commands

import lxsession.commands as ssn_commands

assets = [
    # 'shrubs_a',
    # 'shrubs_b',
    # 'shrubs_c',
    'chrysanthemum_a',
    'chrysanthemum_b',
    'chrysanthemum_c',
    # 'kite_tree',
    # 'xiangzhang_tree_b',
    # 'xiangzhang_tree_b',
    # 'xiangzhang_tree_c',
    # 'xiangzhang_tree_d',
    # 'xiangzhang_tree_e',
    # 'xiangzhang_tree_f',
    # 'xiangzhang_tree_g'
]

resolver = rsv_commands.get_resolver()

rsv_project = resolver.get_rsv_project(project='cgm')

user = utl_core.System.get_user_name()
time_tag = utl_core.System.get_time_tag()

for i_asset in assets:
    i_rsv_task = rsv_project.get_rsv_task(asset=i_asset, task='surfacing')
    i_file_rsv_unit = i_rsv_task.get_rsv_unit(keyword='asset-katana-scene-src-file')
    i_file_path = i_file_rsv_unit.get_result(version='latest')
    if i_file_path:
        i_option_opt = bsc_core.KeywordArgumentsOpt(
            option=dict(
                option_hook_key='rsv-task-methods/asset/katana/gen-look-export',
                #
                file=i_file_path,
                user=bsc_core.SystemMtd.get_user_name(),
                #
                choice_scheme='asset-katana-publish',
                #
                with_texture_tx=True,
                with_look_ass=True,
                #
                # td_enable=True,
                rez_beta=True,
            )
        )
        #
        ssn_commands.set_option_hook_execute_by_deadline(
            option=i_option_opt.to_string()
        )

