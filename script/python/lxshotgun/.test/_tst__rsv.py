# coding:utf-8
import lxresolver.commands as rsv_commands

import lxshotgun.rsv.scripts as stg_rsv_scripts

resolver = rsv_commands.get_resolver()

rsv_task = resolver.get_rsv_task(
    project='nsa_dev',
    asset='td_test',
    task='surfacing'
)

print rsv_task


print stg_rsv_scripts.RsvShotgunHookOpt.get_new_registry_file_data_fnc(
    rsv_task, version='v004'
)

print stg_rsv_scripts.RsvShotgunHookOpt.get_new_registry_info_data_fnc(
    user='dongchangbao'
)
