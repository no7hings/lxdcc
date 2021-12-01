# coding:utf-8
import copy

import lxresolver.commands as rsv_commands

import lxusd.commands as usd_commands

import lxkatana.fnc.builders as ktn_fnc_builders


def set_asset_set_usd_import_(task_properties):
    resolver = rsv_commands.get_resolver()
    #
    branch = task_properties.get('branch')
    step = task_properties.get('step')
    if branch == 'asset' and step == 'srf':
        search_path = [
            ('set', 'registry')
        ]
        for step, task in search_path:
            _kwargs = copy.copy(task_properties.value)
            _kwargs['step'] = step
            _kwargs['task'] = task
            rsv_task = resolver.get_rsv_task(**_kwargs)
            set_usd_file = rsv_task.get_rsv_unit(
                keyword='asset-set-usd-file', workspace='publish'
            )
            set_usd_file_path = set_usd_file.get_result(version='latest')
            if set_usd_file_path is not None:
                ktn_fnc_builders.AssetWorkspaceBuilder().set_set_usd_import(set_usd_file_path)


def set_asset_work_set_usd_import(task_properties):
    results = usd_commands.set_asset_work_set_usda_create(task_properties)
    if results:
        work_set_usd_file_path = results[0]
        ktn_fnc_builders.AssetWorkspaceBuilder().set_set_usd_import(work_set_usd_file_path)
