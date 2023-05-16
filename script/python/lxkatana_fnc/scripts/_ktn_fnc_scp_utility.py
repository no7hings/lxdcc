# coding:utf-8


def get_asset_scene_src_file_path(rsv_version):
    return rsv_version.get_rsv_unit(
        keyword='asset-katana-scene-src-file'
    ).get_result(version=rsv_version.get('version'))


def set_asset_workspace_create(rsv_task_properties, use_preview_look_pass=True):
    raise RuntimeError('this method is removed')


def set_asset_cfx_look_workspace_create(rsv_task_properties):
    raise RuntimeError('this method is removed')


def set_work_look_ass_import(rsv_task_properties):
    from lxutil import utl_core
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxresolver.operators as rsv_operators
    #
    import lxkatana.fnc.importers as ktn_fnc_importers
    #
    work_look_ass_file_path = rsv_operators.RsvAssetLookQuery(rsv_task_properties).get_ass_work_file()
    #
    work_look_ass_file_obj = utl_dcc_objects.OsFile(work_look_ass_file_path)
    if work_look_ass_file_obj.get_is_exists() is True:
        ktn_fnc_importers.LookAssImporter(
            option=dict(
                file=work_look_ass_file_path,
                location='/root/materials',
            ),
        ).set_run()
    else:
        utl_core.Log.set_module_warning_trace(
            'work-look-ass-import',
            'file="{}" is non-exists'.format(work_look_ass_file_path)
        )
