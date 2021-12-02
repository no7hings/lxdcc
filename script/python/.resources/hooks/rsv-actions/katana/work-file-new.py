# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects
#
import lxkatana.dcc.dcc_objects as ktn_dcc_objects


def post_method_fnc_(file_path_):
    pass


rsv_task = session.rsv_obj
#
rsv_unit = rsv_task.get_rsv_unit(
    keyword='{branch}-work-maya-scene-src-file'.format(
        **session.variants
    )
)
#
file_path = rsv_unit.get_result(
    version='new'
)
file_ = utl_dcc_objects.OsFile(file_path)
if file_.get_is_exists() is False:
    ktn_dcc_objects.Scene.set_file_new_with_dialog(
        file_path,
        post_method_fnc_
    )
