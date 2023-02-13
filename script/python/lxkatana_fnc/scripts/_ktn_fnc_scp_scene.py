# coding:utf-8
from lxkatana_fnc.scripts import _ktn_fnc_scp_utility, _ktn_fnc_scp_texture


def set_scene_new(file_path):
    print file_path, 'AAAAA'


# scene export
def set_scene_export_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    import lxshotgun_fnc.scripts as stg_fnc_scripts
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.set_map_to_platform(any_scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
    if rsv_task_properties:
        application = rsv_task_properties.get('application')
        rsv_version = resolver.get_rsv_task_version(**rsv_task_properties.value)
        if application != 'katana':
            any_scene_file_path = _ktn_fnc_scp_utility.get_asset_scene_src_file_path(rsv_version)
            rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
        #
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        rsv_version.set('user', user)
        rsv_version.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            stg_fnc_scripts.set_version_log_module_result_trace(
                rsv_task_properties,
                'katana-scene-export',
                'start'
            )
            #
            create_scene_src = option_opt.get('create_scene_src') or False
            if create_scene_src is True:
                ktn_dcc_objects.Scene.set_file_new()
                set_asset_scene_src_create(rsv_task_properties)
            #
            scene_src_file = utl_dcc_objects.OsFile(any_scene_file_path)
            if scene_src_file.get_is_exists() is True:
                if create_scene_src is False:
                    ktn_dcc_objects.Scene.set_file_open(any_scene_file_path)
                # texture
                with_texture = option_opt.get('with_texture') or False
                if with_texture is True:
                    _ktn_fnc_scp_texture.set_asset_texture_export(rsv_task_properties)
                else:
                    # texture-tx
                    with_texture_tx = option_opt.get('with_texture_tx') or False
                    if with_texture_tx is True:
                        _ktn_fnc_scp_texture.set_asset_texture_tx_export(rsv_task_properties)
                # scene
                with_scene = option_opt.get('with_scene') or False
                if with_scene is True:
                    set_asset_scene_export(rsv_task_properties)
                #
                stg_fnc_scripts.set_version_log_module_result_trace(
                    rsv_task_properties,
                    'katana-scene-export',
                    'complete'
                )
            else:
                utl_core.Log.set_module_warning_trace(
                    'katana-scene-export-script-run',
                    u'file="{}" is non-exists'.format(any_scene_file_path)
                )
    else:
        utl_core.Log.set_module_warning_trace(
            'katana-scene-export-script-run',
            u'file="{}" is not available'.format(any_scene_file_path)
        )


def set_asset_scene_src_create(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    import lxkatana.fnc.importers as ktn_fnc_importers
    #
    version = rsv_task_properties.get('version')
    #
    any_scene_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_katana_src_file(
        version=version
    )
    ktn_dcc_objects.Scene.set_file_save_to(any_scene_file_path)
    result = _ktn_fnc_scp_utility.set_asset_workspace_create(
        rsv_task_properties
    )
    if result is True:
        ktn_dcc_objects.Scene.set_file_save_to(any_scene_file_path)
        ktn_fnc_importers.LookAssImporter._set_pst_run_()
        ktn_dcc_objects.Scene.set_file_save()


def set_asset_scene_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    version = rsv_task_properties.get('version')
    root = rsv_task_properties.get('dcc.root')
    #
    scene_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_file(
        version=version
    )
    if scene_file_path:
        ktn_dcc_objects.Scene.set_file_save_to(scene_file_path)
        return scene_file_path
