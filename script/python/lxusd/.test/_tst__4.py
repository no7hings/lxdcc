# coding:utf-8
from lxutil import utl_core

from lxbasic import bsc_core

from lxusd import usd_setup, usd_core

usd_setup.UsdSetup.build_environ()

import lxusd.fnc.exporters as usd_fnc_exporter

color_scheme = 'asset_color'

f_src = '/l/prod/cgm/publish/assets/chr/td_test/mod/modeling/td_test.mod.modeling.v056/cache/usd/geo/hi.usd'

f_tgt = '/l/prod/cgm/publish/assets/chr/td_test/mod/modeling/td_test.mod.modeling.v056/cache/usd/geo_extra/user_property.usd'

s = usd_core.UsdStageOpt._set_file_open_(f_src)

usd_fnc_exporter.GeometryLookPropertyExporter(
    option=dict(
        file=f_tgt,
        location='/master',
        #
        stage_src=s,
        #
        asset_name='nn_4y',
        #
        color_seed=5,
        #
        color_scheme=color_scheme,
        #
        with_object_color=True,
        with_group_color=True,
        with_asset_color=True,
        with_shell_color=True,
        #
        # with_uv_map=True,
        #
        # with_display_color=True
    )
).set_run()


