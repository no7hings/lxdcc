# coding:utf-8
from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

import lxresolver.commands as rsv_commands

r = rsv_commands.get_resolver()

rsv_project = r.get_rsv_project(
    project='nsa_dev'
)
if rsv_project is not None:
    rsv_task = rsv_project.get_rsv_task(
        asset='surface_workspace',
        step='srf',
        task='surface'
    )
    if rsv_task is not None:
        keyword = 'asset-source-katana-scene-src-file'
        rsv_unit = rsv_task.get_rsv_unit(
            keyword=keyword
        )
        # print rsv_unit.pattern
        results = rsv_unit.get_result(
            version='all',
            extend_variants=dict(task_extra='surface')
        )
        print results
        # print rsv_unit.get_result(version='new', extend_variants=dict(task_extra='surface'))


