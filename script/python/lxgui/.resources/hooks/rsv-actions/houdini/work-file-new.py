# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects
#
import lxhoudini.dcc.dcc_objects as hou_dcc_objects


def post_method_fnc_(file_path_):
    # noinspection PyUnresolvedReferences
    import hou
    f = utl_dcc_objects.OsFile(file_path_)
    cmd = "set -g {0}={1}".format('HIP', f.directory.path)
    hou.hscript(cmd)


file_path = session.rsv_unit.get_result(
    version='new'
)
file_ = utl_dcc_objects.OsFile(file_path)
if file_.get_is_exists() is False:
    hou_dcc_objects.Scene.set_file_new_with_dialog(
        file_path,
        post_method_fnc_
    )
