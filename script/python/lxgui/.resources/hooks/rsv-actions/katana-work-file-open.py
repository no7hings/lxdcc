# coding:utf-8
from lxutil import utl_core

file_path = session.rsv_unit.get_result(
    version='latest'
)
if file_path:
    project = session.variants['project']

    launcher = utl_core.KatanaLauncher(
        project=project
    )
    launcher.set_file_open(file_path)
