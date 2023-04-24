# coding:utf-8


def set_look_preview_export_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.map_to_current(any_scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
    if rsv_task_properties:
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            project = rsv_task_properties.get('project')
            application = rsv_task_properties.get('application')
            if application == 'maya':
                create_option = option


def set_asset_look_properties_usd_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators

    import lxutil.fnc.importers as utl_fnc_importers

    import lxarnold.fnc.exporters as and_fnc_exporters

    rsv_asset_look_query = rsv_operators.RsvAssetLookQuery(
        rsv_task_properties
    )
    rsv_asset_usd_query = rsv_operators.RsvAssetUsdQuery(
        rsv_task_properties
    )
    #
    dcc_root = rsv_task_properties['dcc.root']
    version = rsv_task_properties['version']
    #
    look_ass_file_path = rsv_asset_look_query.get_ass_file(
        version=version
    )
    #
    look_properties_usd_file_path = rsv_asset_usd_query.get_look_properties_file(
        version=version, look_pass='default'
    )
    #
    and_fnc_exporters.LookPropertiesUsdExporter(
        file_path=look_properties_usd_file_path,
        root=dcc_root,
        option=dict(
            ass_file=look_ass_file_path
        )
    ).set_run()
    #
    look_yml__surface_anm__file_path = rsv_asset_look_query.get_yml_surface_anm_file()
    if look_yml__surface_anm__file_path is not None:
        look_pass_names = utl_fnc_importers.LookYamlImporter(
            option=dict(
                file=look_yml__surface_anm__file_path,
                root=dcc_root
            )
        ).get_look_pass_names()
        for i_look_pass_name in look_pass_names:
            if i_look_pass_name not in ['default']:
                i_look_ass_sub_file_path = rsv_asset_look_query.get_ass_sub_file(
                    version=version, look_pass=i_look_pass_name
                )
                #
                i_look_properties_usd_file_path = rsv_asset_usd_query.get_look_properties_file(
                    version=version, look_pass=i_look_pass_name
                )
                #
                and_fnc_exporters.LookPropertiesUsdExporter(
                    file_path=i_look_properties_usd_file_path,
                    root=dcc_root,
                    option=dict(
                        ass_file=i_look_ass_sub_file_path
                    )
                ).set_run()
