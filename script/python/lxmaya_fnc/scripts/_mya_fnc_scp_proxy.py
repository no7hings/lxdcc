# coding:utf-8
import sys


def set_proxy_export_by_any_scene_file(option):
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
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    option_opt = bsc_core.ArgDictStringOpt(option, default_option='with_look_ass=True')
    #
    scene_src_file_path = option_opt.get('file')
    scene_src_file_path = utl_core.Path.map_to_current(scene_src_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_src_file_path)
    if rsv_task_properties:
        #
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        #
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        step = rsv_task_properties.get('step')
        task = rsv_task_properties.get('task')
        if branch == 'asset':
            if step in ['mod', 'srf']:
                if task in ['modeling', 'surfacing']:
                    scene_src_file_obj = utl_dcc_objects.OsFile(scene_src_file_path)
                    if scene_src_file_obj.get_is_exists() is True:
                        stg_fnc_scripts.set_version_log_module_result_trace(
                            rsv_task_properties,
                            'maya-proxy-export',
                            'start'
                        )
                        #
                        mya_dcc_objects.Scene.open_file(scene_src_file_path)
                        #
                        with_proxy_xarc = option_opt.get('with_proxy_xarc')
                        if with_proxy_xarc is True:
                            set_asset_proxy_export(rsv_task_properties)
                        #
                        stg_fnc_scripts.set_version_log_module_result_trace(
                            rsv_task_properties,
                            'maya-proxy-export',
                            'complete'
                        )
                    else:
                        bsc_core.Log.trace_method_warning(
                            'maya-look-export-script-run',
                            u'file="{}" is non-exists'.format(scene_src_file_path)
                        )
    else:
        bsc_core.Log.trace_method_warning(
            key,
            u'file="{}" is not available'.format(scene_src_file_path)
        )


def set_asset_proxy_export(rsv_task_properties):
    from lxbasic import bsc_core
    #
    import lxutil.fnc.exporters as utl_fnc_exporters
    #
    from lxmaya import ma_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxmaya.fnc.exporters as mya_fnc_exporters
    #
    resolver = rsv_commands.get_resolver()
    rsv_task = resolver.get_rsv_task(
        **rsv_task_properties.value
    )
    root = rsv_task_properties.get('dcc.root')
    asset = rsv_task.get('asset')
    version = rsv_task_properties.get('version')
    location = '{}/{}'.format(root, 'hi')
    mya_location = bsc_core.DccPathDagOpt(location).translate_to('|').get_value()
    #
    act = 'static'
    for i_look_pass in ['default']:
        i_name = '{}.{}.{}'.format(asset, i_look_pass, act)
        i_color = bsc_core.RawTextOpt(i_name).to_rgb(maximum=1)
        i_xarc_option = dict(
            name=i_name,
            color=i_color,
        )
        gpu_files = []
        ass_files = []
        #
        i_proxy_jpg_sub_file = rsv_task.get_rsv_unit(
            keyword='asset-proxy-jpg-sub-file',
        )
        i_proxy_jpg_sub_file_path = i_proxy_jpg_sub_file.get_result(
            version=version,
            extend_variants=dict(
                look_pass=i_look_pass
            )
        )
        #
        # mya_fnc_exporters.PreviewExporter(
        #     file_path=i_proxy_jpg_sub_file_path,
        #     root=location,
        #     option=dict(
        #         use_render=False,
        #         convert_to_dot_mov=False,
        #     )
        # ).set_run()
        #
        i_xarc_option['jpg_file'] = i_proxy_jpg_sub_file_path
        #
        i_proxy_gpu_act_file = rsv_task.get_rsv_unit(
            keyword='asset-proxy-gpu-sub-act-file'
        )
        i_proxy_gpu_act_file_path = i_proxy_gpu_act_file.get_result(
            version=version,
            extend_variants=dict(
                look_pass=i_look_pass,
                act=act
            )
        )
        mya_fnc_exporters.ProxyGpuExporter(
            option=dict(
                file=i_proxy_gpu_act_file_path,
                location=location
            )
        ).set_run()
        #
        gpu_files.append(i_proxy_gpu_act_file_path)
        #
        i_proxy_ass_var_file = rsv_task.get_rsv_unit(
            keyword='asset-proxy-ass-sub-act-file'
        )
        i_proxy_ass_var_file_path = i_proxy_ass_var_file.get_result(
            version=version,
            extend_variants=dict(
                look_pass=i_look_pass,
                act=act
            )
        )
        mya_fnc_exporters.ProxyAssExporter(
            option=dict(
                file=i_proxy_ass_var_file_path,
                location=location
            )
        ).set_run()
        #
        ass_files.append(i_proxy_ass_var_file_path)
        #
        for j_lod in range(2):
            j_proxy_gpu_act_lod_file = rsv_task.get_rsv_unit(
                keyword='asset-proxy-gpu-sub-act-lod-file'
            )
            j_proxy_gpu_act_lod_file_path = j_proxy_gpu_act_lod_file.get_result(
                version=version,
                extend_variants=dict(
                    look_pass=i_look_pass,
                    act=act,
                    lod=str(j_lod+1).zfill(2)
                )
            )
            #
            gpu_files.append(j_proxy_gpu_act_lod_file_path)
            #
            # ma_core.CmdMeshesOpt(mya_location).set_reduce_by(.5)
            #
            mya_fnc_exporters.ProxyGpuExporter(
                option=dict(
                    file=j_proxy_gpu_act_lod_file_path,
                    location=location
                )
            ).set_run()
            #
            j_proxy_ass_var_lod_file = rsv_task.get_rsv_unit(
                keyword='asset-proxy-ass-sub-act-lod-file'
            )
            j_proxy_ass_var_lod_file_path = j_proxy_ass_var_lod_file.get_result(
                version=version,
                extend_variants=dict(
                    look_pass=i_look_pass,
                    act=act,
                    lod=str(j_lod + 1).zfill(2)
                )
            )
            mya_fnc_exporters.ProxyAssExporter(
                option=dict(
                    file=j_proxy_ass_var_lod_file_path,
                    location=location
                )
            ).set_run()
            #
            ass_files.append(j_proxy_ass_var_lod_file_path)
        #
        i_proxy_xarc_sub_act_file = rsv_task.get_rsv_unit(
            keyword='asset-proxy-xarc-sub-act-file',
        )
        i_xarc_option['gpu_files'] = gpu_files
        i_xarc_option['ass_files'] = ass_files
        #
        i_proxy_xarc_sub_act_file_path = i_proxy_xarc_sub_act_file.get_result(
            version=version,
            extend_variants=dict(
                act=act,
                look_pass=i_look_pass
            )
        )
        i_xarc_option['file'] = i_proxy_xarc_sub_act_file_path
        #
        utl_fnc_exporters.DotXarcExporter(
            option=i_xarc_option
        ).set_run()
    