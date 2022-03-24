# coding:utf-8
from lxutil import utl_core

print utl_core.AppLauncher(
    project='default',
    application='maya'
).get_run_cmd('')

# rez-env mtoa-4.2.1.1 maya-2019.2 mgear usd aces-1.2 nxt pg_zsPyBase pg_publish pgPvt lxdcc tl_rigsystem pg_production_lib pgmaya xgenPipe-0.1 pgusd xpuCache tk_framework_pg_maya tk_app_pg_multi_publish2
