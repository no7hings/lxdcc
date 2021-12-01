# coding:utf-8
import lxarnold.fnc.exporters as and_fnc_exporters

f = '/l/prod/cjd/publish/assets/chr/laohu_xiao/srf/surfacing/laohu_xiao.srf.surfacing.v038/cache/ass/laohu_xiao.ass'

f_0 = '/data/f/arnold_usd_export/test_1.properties.usda'

e = and_fnc_exporters.LookPropertiesUsdExporter(
    file_path=f_0,
    root='/master',
    option=dict(
        ass_file=f
    )
)

e.set_run()
