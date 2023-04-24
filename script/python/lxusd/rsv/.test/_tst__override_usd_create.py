# coding:utf-8
import lxresolver.commands as rsv_commands

import lxusd.rsv.objects as rsv_objects

resolver = rsv_commands.get_resolver()


rsv_task = resolver.get_rsv_task(
    project='nsa_dev', asset='td_test', task='surface'
)


rsv_objects.RsvTaskOverrideUsdCreator(
    rsv_task
).create_all_source_geometry_uv_map_over()

