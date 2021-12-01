# coding:utf-8


def get_rsv_assets_opt():
    import lxresolver.commands as rsv_commands
    #
    import lxresolver.operators as rsv_operators
    #
    import lxhoudini.dcc.dcc_objects as hou_dcc_objects
    #
    work_source_file_path = hou_dcc_objects.Scene.get_current_file_path()
    resolver = rsv_commands.get_resolver()
    task_properties = resolver.get_task_properties_by_work_scene_src_file_path(file_path=work_source_file_path)
    #
    rsv_assets_opt = rsv_operators.RsvAssetsOpt(task_properties)
    return rsv_assets_opt


def get_rsv_asset_names(role='*'):
    rsv_assets_opt = get_rsv_assets_opt()
    if rsv_assets_opt:
        return rsv_assets_opt.get_names(role=role)
