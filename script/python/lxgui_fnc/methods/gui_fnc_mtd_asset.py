# coding:utf-8
# coding:utf-8
import copy
#
from lxbasic import bsc_core
#
from lxutil import utl_configure
#
import lxresolver.commands as rsv_commands
#
import lxresolver.methods as rsv_methods
#
import lxshotgun.objects as stg_objects
#
import lxshotgun.methods as stg_methods
#
import lxdeadline.objects as ddl_objects
#
import lxdeadline.methods as ddl_methods
#
import lxutil.dcc.dcc_objects as utl_dcc_objects
#
import lxutil.fnc.exporters as utl_fnc_exporters


class LibAssetCreateBatch(object):
    SHOTGUN_TEMPLATE_CONFIGURE = utl_configure.MainData.get_as_configure(
        'shotgun/template'
    )
    OPTION = dict(
        create_task=False,
        create_shotgun=False,
        copy_src_file=False
    )
    def __init__(self, project, assets, option=None):
        self._project_src = project
        self._assets_src = assets
        #
        self._project_tgt = 'lib'
        #
        self._user = bsc_core.SystemMtd.get_user_name()
        self._time_tag = bsc_core.SystemMtd.get_time_tag()
        #
        self._option = option
        #
        self._resolver = rsv_commands.get_resolver()

    def _get_asset_tgt_(self, i_asset_src):
        return 'ast_{}_{}'.format(self._project_src, i_asset_src)

    def set_run(self):
        for i_asset_src in self._assets_src:
            self._set_i_rsv_asset_run_(i_asset_src)

    def _set_i_rsv_asset_run_(self, i_asset_src):
        i_rsv_asset_src = self._resolver.get_rsv_entity(
            project=self._project_src,
            workspace='work',
            asset=i_asset_src
        )
        create_task = self._option.get('create_task') or False
        create_shotgun = self._option.get('create_shotgun') or False
        copy_src_file = self._option.get('copy_src_file') or False
        #
        if i_rsv_asset_src is not None:
            i_role_tgt = i_rsv_asset_src.get('role')
            i_asset_tgt = self._get_asset_tgt_(i_asset_src)
            #
            if create_task is True:
                self._set_i_rsv_asset_build_(i_rsv_asset_src, i_role_tgt, i_asset_tgt)
            #
            i_rsv_asset_tgt = self._resolver.get_rsv_entity(
                project=self._project_tgt,
                workspace='work',
                role=i_role_tgt,
                asset=i_asset_tgt
            )
            #
            if copy_src_file is True:
                i_rsv_tasks_tgt = i_rsv_asset_tgt.get_rsv_tasks()
                for j_rsv_task_tgt in i_rsv_tasks_tgt:
                    j_rsv_task_src = i_rsv_asset_src.get_rsv_task(
                        step=j_rsv_task_tgt.get('step'), task=j_rsv_task_tgt.get('task')
                    )
                    if j_rsv_task_src is not None and j_rsv_task_tgt is not None:
                        self._set_j_rsv_task_copy_(j_rsv_task_src, j_rsv_task_tgt)
            #
            if create_shotgun is True:
                self._set_i_rsv_asset_shotgun_build_(i_rsv_asset_src, i_rsv_asset_tgt)

    def _set_i_rsv_asset_build_(self, i_asset_src, i_role_tgt, i_asset_tgt):
        i_asset_kwargs_tgt = dict(
            project=self._project_tgt,
            role=i_role_tgt,
            asset=i_asset_tgt
        )
        task_keys = self.SHOTGUN_TEMPLATE_CONFIGURE.get(
            'task-templates.{}.task-keys'.format(i_role_tgt)
        )
        if task_keys is None:
            task_keys = self.SHOTGUN_TEMPLATE_CONFIGURE.get(
                'task-templates.default.task-keys'
            )
        #
        for j_task_key in task_keys:
            j_task_kwargs = copy.copy(i_asset_kwargs_tgt)
            step, task = j_task_key.split('/')
            j_task_kwargs['step'] = step
            j_task_kwargs['task'] = task
            #
            rsv_methods.RsvPermissionMtd.set_entity_task_create(
                **j_task_kwargs
            )

    def _set_i_rsv_asset_shotgun_build_(self, i_rsv_asset_src, i_rsv_asset_tgt):
        self._stg_connector = stg_objects.StgConnector()
        #
        stg_methods.StgTaskMtd.set_asset_create(
            project=self._project_tgt,
            role=i_rsv_asset_tgt.get('role'),
            asset=i_rsv_asset_tgt.get('asset'),
        )
        i_rsv_task_src = i_rsv_asset_src.get_rsv_task(step='srf', task='surfacing')
        i_rsv_task_unit_src = i_rsv_task_src.get_rsv_unit(
            keyword='asset-preview-mov-file'
        )
        preview_file_path = i_rsv_task_unit_src.get_result()
        if preview_file_path:
            i_stg_asset_query_tgt = self._stg_connector.get_stg_entity_query(
                project=self._project_tgt, asset=i_rsv_asset_tgt.get('asset')
            )
            thumbnail_file_path = bsc_core.VedioOpt(preview_file_path).get_thumbnail(ext='.png', block=True)
            if thumbnail_file_path:
                i_stg_asset_query_tgt.set_upload(
                    'image', thumbnail_file_path
                )

    def _set_j_rsv_task_copy_(self, j_rsv_task_src, j_rsv_task_tgt):
        # self._set_j_rsv_task_dir_build_(j_rsv_task_src, j_rsv_task_tgt)
        #
        self._set_j_rsv_task_work_scene_file_copy_(j_rsv_task_src, j_rsv_task_tgt)
        self._set_j_rsv_task_scene_file_copy_(j_rsv_task_src, j_rsv_task_tgt)
        #
        self._set_j_rsv_task_file_copy_(j_rsv_task_src, j_rsv_task_tgt)
        self._set_j_rsv_task_files_build_(j_rsv_task_src, j_rsv_task_tgt)

    def _set_j_rsv_task_work_scene_file_copy_(self, j_rsv_task_src, j_rsv_task_tgt):
        for k_keyword in [
            'asset-work-maya-scene-src-file',
            'asset-work-houdini-scene-src-file',
            'asset-work-katana-scene-src-file',
            'asset-work-nuke-scene-src-file',
        ]:
            self._set_k_rsv_unit_scene_file_copy_(j_rsv_task_src, j_rsv_task_tgt, k_keyword)

    def _set_j_rsv_task_scene_file_copy_(self, j_rsv_task_src, j_rsv_task_tgt):
        for k_keyword in [
            'asset-maya-scene-src-file', 'asset-katana-scene-src-file', 'asset-houdini-scene-src-file', 'asset-nuke-scene-src-file',
            #
            'asset-maya-scene-file', 'asset-katana-scene-file', 'asset-houdini-scene-file', 'asset-nuke-scene-file',
        ]:
            self._set_k_rsv_unit_scene_file_copy_(j_rsv_task_src, j_rsv_task_tgt, k_keyword)

    def _set_k_rsv_unit_scene_file_copy_(self, j_rsv_task_src, j_rsv_task_tgt, k_keyword):
        rsv_unit_file_src = j_rsv_task_src.get_rsv_unit(
            keyword=k_keyword
        )
        rsv_unit_file_tgt = j_rsv_task_tgt.get_rsv_unit(
            keyword=k_keyword
        )
        file_path_src = rsv_unit_file_src.get_result(version='latest')
        file_path_tgt = rsv_unit_file_tgt.get_result(version='v001')
        if file_path_src:
            file_src = utl_dcc_objects.OsFile(file_path_src)
            if file_src.ext in ['.ma']:
                utl_fnc_exporters.DotMaExport(
                    option=dict(
                        file_path_src=file_path_src,
                        file_path_tgt=file_path_tgt
                    )
                ).set_run()
            else:
                file_src.set_copy_to_file(
                    file_path_tgt
                )

    def _set_j_rsv_task_file_copy_(self, j_rsv_task_src, j_rsv_task_tgt):
        for k_keyword in [
            'asset-review-file',
            #
            'asset-geometry-usd-hi-file',
            #
            'asset-look-ass-file', 'asset-look-klf-file',
        ]:
            self._set_k_rsv_unit_file_build_(j_rsv_task_src, j_rsv_task_tgt, k_keyword)

    def _set_j_rsv_task_files_build_(self, j_rsv_task_src, j_rsv_task_tgt):
        for k_keyword in [
            'asset-geometry-xgen-file',
            'asset-geometry-xgen-grow-file',
        ]:
            self._set_k_rsv_unit_files_build_(j_rsv_task_src, j_rsv_task_tgt, k_keyword)

    def _set_j_rsv_task_dir_build_(self, j_rsv_task_src, j_rsv_task_tgt):
        for k_keyword in [
            'asset-texture-tgt-dir',
        ]:
            self._set_k_rsv_unit_dir_build_(j_rsv_task_src, j_rsv_task_tgt, k_keyword)

    def _set_k_rsv_unit_file_build_(self, j_rsv_task_src, j_rsv_task_tgt, k_keyword):
        rsv_unit_file_src = j_rsv_task_src.get_rsv_unit(
            keyword=k_keyword
        )
        rsv_unit_file_tgt = j_rsv_task_tgt.get_rsv_unit(
            keyword=k_keyword
        )
        file_path_src = rsv_unit_file_src.get_result(version='latest')
        file_path_tgt = rsv_unit_file_tgt.get_result(version='v001')
        if file_path_src:
            utl_dcc_objects.OsFile(file_path_src).set_copy_to_file(
                file_path_tgt
            )

    def _set_k_rsv_unit_files_build_(self, j_rsv_task_src, j_rsv_task_tgt, k_keyword):
        rsv_unit_file_src = j_rsv_task_src.get_rsv_unit(
            keyword=k_keyword
        )
        rsv_unit_file_tgt = j_rsv_task_tgt.get_rsv_unit(
            keyword=k_keyword
        )
        src_file_paths = rsv_unit_file_src.get_results(version='latest')
        for i_file_path_src in src_file_paths:
            i_extend_variants = rsv_unit_file_src.get_extend_variants(i_file_path_src)
            i_file_path_tgt = rsv_unit_file_tgt.get_result(version='v001', extend_variants=i_extend_variants)
            utl_dcc_objects.OsFile(i_file_path_src).set_copy_to_file(
                i_file_path_tgt
            )

    def _set_k_rsv_unit_dir_build_(self, j_rsv_task_src, j_rsv_task_tgt, k_keyword):
        k_rsv_unit_dir_src = j_rsv_task_src.get_rsv_unit(
            keyword=k_keyword
        )
        k_rsv_unit_dir_tgt = j_rsv_task_tgt.get_rsv_unit(
            keyword=k_keyword
        )
        k_rsv_unit_dir_path_src = k_rsv_unit_dir_src.get_result(version='latest')
        k_rsv_unit_dir_path_tgt = k_rsv_unit_dir_tgt.get_result(version='v001')
        if k_rsv_unit_dir_path_src:
            k_rsv_unit_dir = utl_dcc_objects.OsDirectory_(k_rsv_unit_dir_path_src)
            k_rsv_unit_dir.set_copy_to_directory(
                k_rsv_unit_dir_path_tgt
            )

    def _set_j_rsv_task_shotgun_build_(self, j_rsv_task_src, j_rsv_task_tgt):
        pass


class AssetBatch(object):
    OPTION = dict(
        surface_publish=False,
        surface_render=False
    )
    def __init__(self, project, assets, option=None):
        self._project_tgt = project
        self._assets_tgt = assets
        #
        self._option = option
        #
        self._user = bsc_core.SystemMtd.get_user_name()
        self._time_tag = bsc_core.SystemMtd.get_time_tag()
        #
        self._td_enable = True
        #
        self._resolver = rsv_commands.get_resolver()

    def set_run(self):
        surface_render = self._option.get('surface_render') or False
        surface_publish = self._option.get('surface_publish') or False
        for i_asset_tgt in self._assets_tgt:
            i_rsv_asset_tgt = self._resolver.get_rsv_entity(
                project=self._project_tgt,
                workspace='publish',
                asset=i_asset_tgt
            )
            if i_rsv_asset_tgt is not None:
                if surface_render is True:
                    self._set_i_rsv_asset_surface_katana_render_(i_rsv_asset_tgt)
                if surface_publish is True:
                    self._set_i_rsv_asset_surface_publish_(i_rsv_asset_tgt)

    def _set_i_rsv_asset_surface_publish_(self, i_rsv_asset_tgt):
        import lxutil_fnc.scripts as utl_fnc_scripts
        #
        i_rsv_task = i_rsv_asset_tgt.get_rsv_task(step='srf', task='surfacing')
        if i_rsv_task:
            i_katana_scene_src_src_file_unit = i_rsv_task.get_rsv_unit(keyword='asset-katana-scene-src-file')
            i_katana_scene_src_src_file_path = i_katana_scene_src_src_file_unit.get_result(version='latest')
            if i_katana_scene_src_src_file_path:
                utl_fnc_scripts.set_fnc_methods_run_by_asset_katana_scene_src(
                    option='file={}'.format(i_katana_scene_src_src_file_path)
                )

    def _set_i_rsv_asset_surface_katana_render_(self, i_rsv_asset_tgt):
        i_rsv_task = i_rsv_asset_tgt.get_rsv_task(step='srf', task='surfacing')
        if i_rsv_task:
            i_katana_scene_src_file_unit = i_rsv_task.get_rsv_unit(keyword='asset-katana-scene-src-file')
            i_katana_scene_src_file_path = i_katana_scene_src_file_unit.get_result()
            #
            i_render_katana_scene_file_unit = i_rsv_task.get_rsv_unit(keyword='asset-render-katana-scene-file')
            i_render_katana_scene_file_path = i_render_katana_scene_file_unit.get_result()
            if i_render_katana_scene_file_path is None:
                if i_katana_scene_src_file_path:
                    i_rsv_task_properties = self._resolver.get_task_properties_by_any_scene_file_path(
                        file_path=i_katana_scene_src_file_path)
                    #
                    i_export_query = ddl_objects.DdlRsvTaskQuery(
                        'katana-render-export', i_rsv_task_properties
                    )
                    i_export = ddl_methods.DdlRsvTaskMethodRunner(
                        method_option=i_export_query.get_method_option(),
                        script_option=i_export_query.get_script_option(
                            file=i_katana_scene_src_file_path,
                            create_camera=True,
                            create_scene=True,
                            create_render=True,
                            #
                            with_shotgun_render=True,
                            width=1024, height=1024,
                            #
                            td_enable=self._td_enable,
                            #
                            user=self._user, time_tag=self._time_tag
                        )
                    )
                    i_export.set_run_with_deadline()
