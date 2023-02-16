# coding:utf-8
import lxmaya

lxmaya.set_reload()

from lxbasic import bsc_core

from lxdeadline import ddl_core

import lxdeadline.objects as ddl_objects

import lxdeadline.methods as ddl_methods

import lxresolver.commands as rsv_commands


f = '/l/prod/lib/publish/assets/chr/ast_cjd_didi/srf/surfacing/ast_cjd_didi.srf.surfacing.v001/scene/ast_cjd_didi.ma'

r = rsv_commands.get_resolver()

rsv_task_properties = r.get_task_properties_by_any_scene_file_path(
    f
)

if rsv_task_properties:
    project = rsv_task_properties.get('project')
    asset = rsv_task_properties.get('asset')
    #
    look_preview_task = r.get_rsv_task(
        project=project, asset=asset, step='srf', task='srf_anishading'
    )
    #
    scene_src_maya_file_unit = look_preview_task.get_rsv_unit(
        keyword='asset-maya-scene-src-file'
    )
    scene_src_maya_file_path = scene_src_maya_file_unit.get_result(
        version='new'
    )

    maya_look_export_query = ddl_objects.DdlRsvTaskQuery(
        'maya-look-preview-export', rsv_task_properties
    )
    user = bsc_core.SystemMtd.get_user_name()
    time_tag = bsc_core.TimeMtd.get_time_tag()
    #
    maya_look_preview_export = ddl_methods.RsvTaskHookExecutor(
        method_option=maya_look_export_query.get_method_option(),
        script_option=maya_look_export_query.get_script_option(
            file=scene_src_maya_file_path,
            #
            create_scene_src=True,
            with_scene=True,
            with_work_scene_src=True,
            #
            user=user, time_tag=time_tag,
            #
            td_enable=True
        ),
        job_dependencies=ddl_core.DdlCacheMtd.get_ddl_job_ids(
            [
                # maya-scene
                ddl_objects.DdlRsvTaskQuery(
                    'maya-scene-export', rsv_task_properties
                ).get_method_option(),
            ]
        )
    )
    maya_look_preview_export.execute_with_deadline()
