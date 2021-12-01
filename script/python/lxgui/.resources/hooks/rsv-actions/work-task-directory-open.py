# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects
#
dir_path = session.rsv_unit.get_result(
    version='latest'
)
#
if dir_path:
    utl_dcc_objects.OsDirectory_(dir_path).set_open()
