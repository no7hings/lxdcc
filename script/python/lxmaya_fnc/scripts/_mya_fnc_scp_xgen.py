# coding:utf-8


def set_xgen_export_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxshotgun_fnc.scripts as stg_fnc_scripts
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.map_to_current(any_scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
    if rsv_task_properties:
        rsv_version = resolver.get_rsv_task_version(**rsv_task_properties.value)
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
                'maya-scene-export',
                'start'
            )
            #
            with_hair_xgen = option_opt.get('with_hair_xgen') or False
            if with_hair_xgen is True:
                set_asset_xgen_export(rsv_version)


def set_asset_xgen_export(rsv_version):
    import lxmaya.dcc.dcc_objects as mya_dcc_objects

    import lxmaya.fnc.exporters as mya_fnc_exporters

    root = '/master'

    scene_file_unit = rsv_version.get_rsv_unit(keyword='asset-maya-scene-file')
    scene_file_path = scene_file_unit.get_result(version=rsv_version.get('version'))

    mya_dcc_objects.Scene.set_file_open(scene_file_path)

    project_directory_path = rsv_version.get_directory_path()

    xgen_collection_directory_unit = rsv_version.get_rsv_unit(keyword='asset-geometry-xgen-collection-dir')
    xgen_collection_directory_path = xgen_collection_directory_unit.get_result(version=rsv_version.get('version'))

    grow_mesh_directory_unit = rsv_version.get_rsv_unit(keyword='asset-geometry-xgen-glow-dir')
    grow_mesh_directory_path = grow_mesh_directory_unit.get_result(version=rsv_version.get('version'))

    location = '{}/hair'.format(root)

    mya_fnc_exporters.XgenExporter(
        option=dict(
            xgen_project_directory=project_directory_path,
            xgen_collection_directory=xgen_collection_directory_path,
            grow_mesh_directory=grow_mesh_directory_path,
            #
            location=location,
            #
            with_xgen_collection=True, with_grow_mesh_abc=True,
        )
    ).set_run()


