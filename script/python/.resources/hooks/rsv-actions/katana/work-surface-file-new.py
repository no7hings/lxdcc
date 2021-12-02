# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects
#
import lxkatana.dcc.dcc_objects as ktn_dcc_objects
#


def post_method_fnc_(file_path_):
    import lxresolver.commands as rsv_commands
    #
    import lxkatana.fnc.creators as ktn_fnc_creators
    #
    from lxkatana import commands
    #
    ktn_fnc_creators.LookWorkspaceCreator().set_run()
    task_properties = rsv_commands.get_resolver().get_task_properties_by_any_scene_file_path(
        file_path_
    )
    if task_properties:
        commands.set_asset_work_set_usd_import(task_properties)


file_path = session.rsv_unit.get_result(
    version='new'
)
file_ = utl_dcc_objects.OsFile(file_path)
if file_.get_is_exists() is False:
    ktn_dcc_objects.Scene.set_file_new_with_dialog(
        file_path,
        post_method_fnc_
    )
