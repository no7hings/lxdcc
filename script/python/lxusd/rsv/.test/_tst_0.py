# coding:utf-8
import lxmaya

lxmaya.set_reload()

import lxresolver.commands as rsv_commands

import lxusd.rsv.objects as usd_rsv_objects


usd_rsv_objects.RsvTaskOverrideUsdCreator(
    rsv_commands.get_resolver().get_rsv_task(
        project='cgm', asset='nn_14y_test', step='srf', task='surfacing'
    )
)._set_geometry_uv_map_create_()
