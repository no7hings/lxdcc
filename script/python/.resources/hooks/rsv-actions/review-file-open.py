# coding:utf-8
from lxutil import utl_core
#
file_path = session.rsv_unit.get_result(
    version='latest'
)
#
if file_path:
    if session.platform == 'linux':
        # cmd = '/opt/rv/bin/rv "{}"'.format(file_path)
        # utl_core.SubProcessRunner.set_run(cmd)
        utl_core.RvLauncher().set_file_open(
            file_path
        )
