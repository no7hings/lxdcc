# coding:utf-8
from lxbasic import bsc_core
#
from lxresolver import rsv_configure
#
import lxresolver.commands as rsv_commands
#
import lxshotgun.objects as stg_objects
#
r = rsv_commands.get_resolver()

branch = 'asset'

rsv_project = r.get_rsv_project(project='lib')

stg_connector = stg_objects.StgConnector()

print stg_connector.get_stg_task(
    project='lib', asset='yellow_fabric', step='srf', task='surfacing'
)

