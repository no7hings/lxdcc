# coding:utf-8
import copy
#
import fnmatch

import os

import parse

import lxbasic.core as bsc_core
#
from lxutil import utl_configure
#
import lxresolver.commands as rsv_commands
#
import lxresolver.scripts as rsv_scripts

import lxwarp.shotgun.core as wrp_stg_core

import lxshotgun.scripts as stg_scripts
#
import lxutil.dcc.dcc_objects as utl_dcc_objects
#
import lxutil.fnc.exporters as utl_fnc_exporters


class ScpAssetBatcher(object):
    OPTION = dict(
        surface_publish=False,
        surface_katana_publish=False,
        surface_katana_render=False
    )

    def __init__(self, project, assets, option=None):
        self._project_tgt = project
        self._assets_tgt = assets
        #
        self._option = option
        #
        self._user = bsc_core.SystemMtd.get_user_name()
        self._time_tag = bsc_core.TimeMtd.get_time_tag()
        #
        self._td_enable = True
        #
        self._resolver = rsv_commands.get_resolver()

    def set_run(self):
        surface_katana_render = self._option.get('surface_katana_render') or False
        surface_publish = self._option.get('surface_publish') or False

        if self._assets_tgt:
            with bsc_core.LogProcessContext.create(maximum=len(self._assets_tgt), label='execute batch') as g_p:
                for i_asset_tgt in self._assets_tgt:
                    g_p.do_update()
                    #
                    i_rsv_asset_tgt = self._resolver.get_rsv_resource(
                        project=self._project_tgt,
                        workspace='publish',
                        asset=i_asset_tgt
                    )
                    if i_rsv_asset_tgt is not None:
                        if surface_katana_render is True:
                            self._set_i_rsv_asset_surface_katana_render_(i_rsv_asset_tgt)
                        if surface_publish is True:
                            self._set_i_rsv_asset_surface_publish_(i_rsv_asset_tgt)

    @classmethod
    def _set_i_rsv_asset_surface_publish_(cls, i_rsv_asset_tgt, user=None, time_tag=None):
        raise RuntimeError(
            'this method is removed'
        )

    def _set_i_rsv_asset_surface_katana_render_(self, i_rsv_asset_tgt):
        raise RuntimeError(
            'this method is removed'
        )


class AbsScpLibFileDef(object):
    @classmethod
    def _set_j_rsv_task_copy_(cls, j_rsv_task_src, j_rsv_task_tgt):
        cls._set_j_rsv_task_scene_file_copy_(j_rsv_task_src, j_rsv_task_tgt)
        cls._set_j_rsv_task_work_scene_src_file_link_(j_rsv_task_src, j_rsv_task_tgt)
        #
        cls._set_j_rsv_task_file_copy_(j_rsv_task_src, j_rsv_task_tgt)
        cls._set_j_rsv_task_files_copy_(j_rsv_task_src, j_rsv_task_tgt)

    @classmethod
    def _set_j_rsv_task_work_scene_src_file_copy_(cls, j_rsv_task_src, j_rsv_task_tgt):
        for k_keyword in [
            'asset-source-maya-scene-src-file',
            'asset-source-houdini-scene-src-file',
            'asset-source-katana-scene-src-file',
            'asset-source-nuke-scene-src-file',
        ]:
            cls._set_k_rsv_unit_scene_file_copy_(j_rsv_task_src, j_rsv_task_tgt, k_keyword)

    @classmethod
    def _set_j_rsv_task_work_scene_src_file_link_(cls, j_rsv_task_src, j_rsv_task_tgt):
        for k_keywords in [
            ('asset-maya-scene-file', 'asset-source-maya-scene-src-file'),
            ('asset-katana-scene-file', 'asset-source-katana-scene-src-file'),
            ('asset-houdini-scene-file', 'asset-source-houdini-scene-src-file'),
            ('asset-nuke-scene-file', 'asset-source-nuke-scene-src-file'),
        ]:
            cls._set_k_rsv_unit_scene_file_link_to_(j_rsv_task_src, j_rsv_task_tgt, k_keywords)

    @classmethod
    def _set_j_rsv_task_scene_file_copy_(cls, j_rsv_task_src, j_rsv_task_tgt):
        for k_keyword in [
            'asset-maya-scene-src-file',
            'asset-katana-scene-src-file',
            'asset-houdini-scene-src-file',
            'asset-nuke-scene-src-file',
            #
            'asset-maya-scene-file',
            'asset-katana-scene-file',
            'asset-houdini-scene-file',
            'asset-nuke-scene-file',
        ]:
            cls._set_k_rsv_unit_scene_file_copy_(j_rsv_task_src, j_rsv_task_tgt, k_keyword)

    @classmethod
    def _set_k_rsv_unit_scene_file_copy_(cls, j_rsv_task_src, j_rsv_task_tgt, k_keyword):
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
                utl_fnc_exporters.DotMaExporter(
                    option=dict(
                        file_path_src=file_path_src,
                        file_path_tgt=file_path_tgt
                    )
                ).set_run()
            else:
                file_src.set_copy_to_file(
                    file_path_tgt
                )

    @classmethod
    def _set_j_rsv_task_file_copy_(cls, j_rsv_task_src, j_rsv_task_tgt):
        for k_keyword in [
            'asset-review-file',
            #
            'asset-geometry-usd-hi-file',
            #
            'asset-look-ass-file', 'asset-look-klf-file',
        ]:
            cls._set_k_rsv_unit_file_copy_(j_rsv_task_src, j_rsv_task_tgt, k_keyword)

    @classmethod
    def _set_j_rsv_task_files_copy_(cls, j_rsv_task_src, j_rsv_task_tgt):
        for k_keyword in [
            'asset-geometry-xgen-file',
            'asset-geometry-xgen-grow-mesh-file',
        ]:
            cls._set_k_rsv_unit_files_copy_(j_rsv_task_src, j_rsv_task_tgt, k_keyword)

    @classmethod
    def _set_j_rsv_task_directory_copy_(cls, j_rsv_task_src, j_rsv_task_tgt):
        for k_keyword in [
            'asset-texture-dir',
        ]:
            cls._set_k_rsv_unit_directory_copy_(j_rsv_task_src, j_rsv_task_tgt, k_keyword)

    @classmethod
    def _set_k_rsv_unit_file_copy_(cls, j_rsv_task_src, j_rsv_task_tgt, k_keyword):
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

    @classmethod
    def _set_k_rsv_unit_files_copy_(cls, j_rsv_task_src, j_rsv_task_tgt, k_keyword):
        rsv_unit_file_src = j_rsv_task_src.get_rsv_unit(
            keyword=k_keyword
        )
        rsv_unit_file_tgt = j_rsv_task_tgt.get_rsv_unit(
            keyword=k_keyword
        )
        src_file_paths = rsv_unit_file_src.get_results(version='latest')
        for i_file_path_src in src_file_paths:
            i_extend_variants = rsv_unit_file_src.get_extend_variants(i_file_path_src)
            i_file_path_tgt = rsv_unit_file_tgt.get_result(version='v001', variants_extend=i_extend_variants)
            utl_dcc_objects.OsFile(i_file_path_src).set_copy_to_file(
                i_file_path_tgt
            )

    @classmethod
    def _set_k_rsv_unit_directory_copy_(cls, j_rsv_task_src, j_rsv_task_tgt, k_keyword):
        k_rsv_unit_dir_src = j_rsv_task_src.get_rsv_unit(
            keyword=k_keyword
        )
        k_rsv_unit_dir_tgt = j_rsv_task_tgt.get_rsv_unit(
            keyword=k_keyword
        )
        k_rsv_unit_dir_path_src = k_rsv_unit_dir_src.get_result(version='latest')
        k_rsv_unit_dir_path_tgt = k_rsv_unit_dir_tgt.get_result(version='v001')
        if k_rsv_unit_dir_path_src:
            k_rsv_unit_dir = utl_dcc_objects.StgDirectory(k_rsv_unit_dir_path_src)
            k_rsv_unit_dir.set_copy_to_directory(
                k_rsv_unit_dir_path_tgt
            )

    @classmethod
    def _set_k_rsv_unit_scene_file_link_to_(cls, j_rsv_task_src, j_rsv_task_tgt, k_keywords):
        k_keyword_src, k_keyword_tgt = k_keywords
        rsv_unit_file_src = j_rsv_task_src.get_rsv_unit(
            keyword=k_keyword_src
        )
        rsv_unit_file_tgt = j_rsv_task_tgt.get_rsv_unit(
            keyword=k_keyword_tgt
        )
        file_path_src = rsv_unit_file_src.get_result(version='latest')
        file_path_tgt = rsv_unit_file_tgt.get_result(version='v001')
        if file_path_src:
            utl_dcc_objects.OsFile(file_path_src).link_to(
                file_path_tgt, replace=True
            )


class AbsScpLibSystemDef(object):
    SHOTGUN_TEMPLATE_CONFIGURE = None

    @classmethod
    def _set_i_rsv_asset_system_create_(cls, i_project_tgt, i_role_tgt, i_asset_tgt):
        i_asset_kwargs_tgt = dict(
            project=i_project_tgt,
            role=i_role_tgt,
            asset=i_asset_tgt
        )
        task_keys = cls.SHOTGUN_TEMPLATE_CONFIGURE.get(
            'task-templates.{}.task-keys'.format(i_role_tgt)
        )
        if task_keys is None:
            task_keys = cls.SHOTGUN_TEMPLATE_CONFIGURE.get(
                'task-templates.default.task-keys'
            )
        #
        for j_task_key in task_keys:
            j_task_kwargs = copy.copy(i_asset_kwargs_tgt)
            step, task = j_task_key.split('/')
            j_task_kwargs['step'] = step
            j_task_kwargs['task'] = task
            #
            r = rsv_commands.get_resolver()
            #
            j_task_directory_paths = r.get_rsv_resource_task_directory_paths(**j_task_kwargs)
            for k_task_directory_path in j_task_directory_paths:
                k_task_directory = utl_dcc_objects.StgDirectory(k_task_directory_path)
                k_task_directory.set_create()

    @classmethod
    def _set_i_rsv_asset_system_permission_create_(cls, i_rsv_asset_tgt):
        i_rsv_tasks_tgt = i_rsv_asset_tgt.get_rsv_tasks()
        for j_rsv_task_tgt in i_rsv_tasks_tgt:
            j_task_kwargs = j_rsv_task_tgt.properties.value
            rsv_scripts.RsvPermissionMtd.set_create(
                **j_task_kwargs
            )


class AbsScpLibShotgunDef(object):
    @classmethod
    def _set_i_rsv_asset_shotgun_create_(cls, i_rsv_asset_tgt):
        stg_connector = wrp_stg_core.StgConnector()
        #
        project = i_rsv_asset_tgt.get('project')
        role = i_rsv_asset_tgt.get('role')
        asset = i_rsv_asset_tgt.get('asset')
        stg_scripts.StgScpTask.set_asset_create(
            project=project,
            role=role,
            asset=asset,
        )
        i_rsv_task_tgt = i_rsv_asset_tgt.get_rsv_task(step='srf', task='surfacing')
        if i_rsv_task_tgt is not None:
            i_rsv_task_unit_tgt = i_rsv_task_tgt.get_rsv_unit(
                keyword='asset-preview-mov-file'
            )
            i_move_file_path = i_rsv_task_unit_tgt.get_result()
            if i_move_file_path:
                i_stg_asset_query_tgt = stg_connector.get_stg_resource_query(
                    project=project, asset=asset
                )
                i_thumbnail_file_path = bsc_core.VdoFileOpt(i_move_file_path).get_thumbnail(block=True)
                if i_thumbnail_file_path:
                    i_stg_asset_query_tgt.set_upload(
                        'image', i_thumbnail_file_path
                    )
        else:
            bsc_core.Log.trace_method_warning(
                'shotgun entity create',
                'surface task in non-exists'
            )


class AbsScpLib(
    AbsScpLibFileDef,
    AbsScpLibSystemDef,
    AbsScpLibShotgunDef
):
    SHOTGUN_TEMPLATE_CONFIGURE = utl_configure.MainData.get_as_configure(
        'shotgun/template'
    )
    OPTION = dict(
        with_system_create=False,
        with_system_permission_create=False,
        #
        with_shotgun_create=False,
        #
        with_file_copy=False,
        #
        with_surface_publish=False,
    )

    @classmethod
    def _get_lib_asset_(cls, project, asset):
        if fnmatch.filter([asset], 'ast_*_*'):
            p = parse.parse(
                'ast_{project}_{asset}', asset
            )
            if p:
                asset = p.named['asset']
        #
        elif '__' in asset:
            if fnmatch.filter([asset], '[a-z][a-z][a-z0-9]__*'):
                asset = asset.split('__')[-1]
        return 'ast_{}_{}'.format(project, asset)


class ScpAssetPusher(AbsScpLib):
    def __init__(self, project, assets, option=None):
        self._project_src = project
        self._assets_src = assets
        #
        self._project_tgt = 'lib'
        #
        self._user = bsc_core.SystemMtd.get_user_name()
        self._time_tag = bsc_core.TimeMtd.get_time_tag()
        #
        self._option = option
        #
        self._resolver = rsv_commands.get_resolver()

    def get_option(self):
        return self._option

    def set_run(self):
        for i_asset_src in self._assets_src:
            self._set_i_rsv_asset_run_(i_asset_src)

    def _set_i_rsv_asset_run_(self, i_asset_src):
        i_rsv_asset_src = self._resolver.get_rsv_resource(
            project=self._project_src,
            workspace='work',
            asset=i_asset_src
        )
        #
        if i_rsv_asset_src is not None:
            with_system_create = self._option.get('with_system_create') or False
            with_system_permission_create = self._option.get('with_system_permission_create') or False
            #
            with_shotgun_create = self._option.get('with_shotgun_create') or False
            with_file_copy = self._option.get('with_file_copy') or False
            with_surface_publish = self._option.get('with_surface_publish') or False
            #
            user = self._option.get('user') or bsc_core.SystemMtd.get_user_name()
            time_tag = self._option.get('time_tag') or bsc_core.TimeMtd.get_time_tag()
            #
            i_role_tgt = i_rsv_asset_src.get('role')
            i_asset_tgt = self._get_lib_asset_(
                self._project_src,
                i_asset_src
            )
            #
            if with_system_create is True:
                self._set_i_rsv_asset_system_create_(
                    self._project_tgt, i_role_tgt, i_asset_tgt
                )
            #
            i_rsv_asset_tgt = self._resolver.get_rsv_resource(
                project=self._project_tgt,
                workspace='work',
                role=i_role_tgt,
                asset=i_asset_tgt
            )
            if i_rsv_asset_tgt is not None:
                if with_file_copy is True:
                    i_rsv_tasks_tgt = i_rsv_asset_tgt.get_rsv_tasks()
                    for j_rsv_task_tgt in i_rsv_tasks_tgt:
                        j_rsv_task_src = i_rsv_asset_src.get_rsv_task(
                            step=j_rsv_task_tgt.get('step'), task=j_rsv_task_tgt.get('task')
                        )
                        if j_rsv_task_src is not None and j_rsv_task_tgt is not None:
                            self._set_j_rsv_task_copy_(j_rsv_task_src, j_rsv_task_tgt)
                #
                if with_system_permission_create is True:
                    self._set_i_rsv_asset_system_permission_create_(i_rsv_asset_tgt)
                #
                if with_shotgun_create is True:
                    self._set_i_rsv_asset_shotgun_create_(i_rsv_asset_tgt)
                # surface-publish
                if with_surface_publish is True:
                    ScpAssetBatcher._set_i_rsv_asset_surface_publish_(
                        i_rsv_asset_tgt,
                        user, time_tag
                    )


class ScpAssetPuller(AbsScpLib):
    def __init__(self, project, assets, option=None):
        self._project_src = 'lib'
        self._assets_src = assets
        #
        self._project_tgt = project
        #
        self._user = bsc_core.SystemMtd.get_user_name()
        self._time_tag = bsc_core.TimeMtd.get_time_tag()
        #
        self._option = option
        #
        self._resolver = rsv_commands.get_resolver()

    def set_run(self):
        for i_asset_src in self._assets_src:
            self._set_i_rsv_asset_run_(i_asset_src)

    def _set_i_rsv_asset_run_(self, i_asset_src):
        i_rsv_asset_src = self._resolver.get_rsv_resource(
            project=self._project_src,
            workspace='work',
            asset=i_asset_src
        )
        if i_rsv_asset_src is not None:
            with_system_create = self._option.get('with_system_create') or False
            with_system_permission_create = self._option.get('with_system_permission_create') or False
            #
            with_shotgun_create = self._option.get('with_shotgun_create') or False
            with_file_copy = self._option.get('with_file_copy') or False
            with_surface_publish = self._option.get('with_surface_publish') or False
            #
            user = self._option.get('user') or bsc_core.SystemMtd.get_user_name()
            time_tag = self._option.get('time_tag') or bsc_core.TimeMtd.get_time_tag()
            #
            i_role_tgt = i_rsv_asset_src.get('role')
            i_asset_tgt = i_asset_src
            if with_system_create is True:
                self._set_i_rsv_asset_system_create_(
                    self._project_tgt, i_role_tgt, i_asset_tgt
                )
            #
            i_rsv_asset_tgt = self._resolver.get_rsv_resource(
                project=self._project_tgt,
                workspace='work',
                role=i_role_tgt,
                asset=i_asset_tgt
            )
            if i_rsv_asset_tgt is not None:
                #
                if with_file_copy is True:
                    i_rsv_tasks_tgt = i_rsv_asset_tgt.get_rsv_tasks()
                    for j_rsv_task_tgt in i_rsv_tasks_tgt:
                        j_rsv_task_src = i_rsv_asset_src.get_rsv_task(
                            step=j_rsv_task_tgt.get('step'), task=j_rsv_task_tgt.get('task')
                        )
                        if j_rsv_task_src is not None and j_rsv_task_tgt is not None:
                            self._set_j_rsv_task_copy_(j_rsv_task_src, j_rsv_task_tgt)
                #
                if with_system_permission_create is True:
                    self._set_i_rsv_asset_system_permission_create_(i_rsv_asset_tgt)
                # shotgun-create
                if with_shotgun_create is True:
                    self._set_i_rsv_asset_shotgun_create_(i_rsv_asset_tgt)
                # surface-publish
                if with_surface_publish is True:
                    ScpAssetBatcher._set_i_rsv_asset_surface_publish_(
                        i_rsv_asset_tgt,
                        user, time_tag
                    )


if __name__ == '__main__':
    print AbsScpLib._get_lib_asset_(
        'cjd', 'ast_shl_cao_a'
    )
