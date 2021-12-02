# coding:utf-8
import lxmaya.dcc.dcc_objects as mya_dcc_objects
#
file_path = session.rsv_unit.get_result(
    version='latest'
)
if file_path:
    mya_dcc_objects.Scene.set_file_open_with_dialog(file_path)
