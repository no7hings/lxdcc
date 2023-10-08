# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

from lxutil.scripts import _utl_scp_video

from lxsession import ssn_core

import lxsession.commands as ssn_commands


class ScpGeneralPublish(object):
    VERSION_NAME_PATTERN = '{project}.{resource}.{task}.{version}'
    def __init__(self, window, session, rsv_task, version_properties, options):
        self._window = window
        self._session = session
        self._rsv_task = rsv_task
        self._version_properties = version_properties
        self._options = options

        self._version_name = self.VERSION_NAME_PATTERN.format(
            **self._version_properties.get_value()
        )
        self._review_mov_file_path = None

        self._maya_scene_src_file_paths = []
        self._katana_scene_src_file_paths = []

    def create_or_unlock_version_directory_fnc(self):
        directory_path = self._options.get('version_directory')
        if bsc_core.StgDirectoryOpt(directory_path).get_is_exists() is False:
            bsc_core.StgPathPermissionMtd.create_directory(
                directory_path
            )

    def pre_fnc(self):
        self.create_or_unlock_version_directory_fnc()

    def get_scene_src_file_path(self):
        keyword = '{branch}-maya-scene-src-file'
        rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        return rsv_unit.get_result(
            version=self._version_properties.get('version')
        )

    def collection_review_fnc(self):
        self._review_mov_file_path = None
        #
        file_paths = self._options['review']
        movie_file_path = None
        if file_paths:
            movie_file_path = _utl_scp_video.ScpVideo.comp_movie(
                file_paths
            )
        #
        if movie_file_path:
            version = self._version_properties.get('version')
            review_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword='{branch}-review-file'
            )
            review_file_path = review_file_rsv_unit.get_result(
                version=version
            )
            #
            bsc_core.StgPathPermissionMtd.copy_to_file(
                movie_file_path, review_file_path
            )
            self._review_mov_file_path = movie_file_path

    def collection_scene_src_fnc(self):
        self._maya_scene_src_file_paths = []
        self._katana_scene_src_file_paths = []
        #
        count_dict = {}
        file_paths = self._options.get('extra.scene')
        if file_paths:
            version = self._version_properties.get('version')
            with self._window.gui_progressing(maximum=len(file_paths), label='export scene') as g_p:
                for i_index, i_file_path in enumerate(file_paths):
                    g_p.set_update()
                    i_file_opt = bsc_core.StgFileOpt(i_file_path)
                    if i_file_opt.get_is_file():
                        i_ext = i_file_opt.get_ext()
                        if i_ext in count_dict:
                            i_c = len(count_dict[i_ext])
                        else:
                            i_c = 0

                        if i_ext == '.ma':
                            i_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
                                keyword='{branch}-maya-scene-src-file'
                            )
                        elif i_ext == '.katana':
                            i_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
                                keyword='{branch}-katana-scene-src-file'
                            )
                        else:
                            raise RuntimeError()
                        #
                        i_scene_src_file_path_tgt = i_scene_src_file_rsv_unit.get_result(
                            version=version
                        )
                        if i_c > 0:
                            i_scene_src_file_path_opt_tgt = bsc_core.StgFileOpt(
                                i_scene_src_file_path_tgt
                            )
                            i_scene_src_file_path_tgt = '{}.{}{}'.format(
                                i_scene_src_file_path_opt_tgt.get_path_base(),
                                i_c,
                                i_scene_src_file_path_opt_tgt.get_ext()
                            )
                        #
                        if i_ext == '.ma':
                            self._maya_scene_src_file_paths.append(i_scene_src_file_path_tgt)
                        elif i_ext == '.katana':
                            self._katana_scene_src_file_paths.append(i_scene_src_file_path_tgt)
                        #
                        count_dict.setdefault(
                            i_ext, []
                        ).append(i_file_path)
                        if i_file_opt.get_is_readable() is False:
                            bsc_core.StgPathPermissionMtd.unlock(i_file_path)
                        #
                        i_file_opt.set_copy_to_file(
                            i_scene_src_file_path_tgt
                        )

    def collection_image_fnc(self):
        file_paths = self._options.get('extra.image')
        if file_paths:
            version = self._version_properties.get('version')
            image_directory_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword='{branch}-image-dir'
            )
            image_directory_path = image_directory_rsv_unit.get_result(
                version=version
            )
            with self._window.gui_progressing(maximum=len(file_paths), label='export image') as g_p:
                for i_index, i_file_path in enumerate(file_paths):
                    g_p.set_update()
                    i_file_tile_paths = bsc_core.StgFileMultiplyMtd.get_exists_unit_paths(i_file_path)
                    for j_file_path in i_file_tile_paths:
                        j_file_opt = bsc_core.StgFileOpt(j_file_path)
                        j_file_path_tgt = '{}/{}'.format(
                            image_directory_path, j_file_opt.get_name()
                        )
                        if j_file_opt.get_is_readable() is False:
                            bsc_core.StgPathPermissionMtd.unlock(j_file_path)
                        #
                        j_file_opt.set_copy_to_file(
                            j_file_path_tgt
                        )

    def farm_process_fnc(self):
        file_path = self.get_scene_src_file_path()
        #
        extra_data = dict(
            user=bsc_core.SystemMtd.get_user_name(),
            #
            version_type=self._options['version_type'],
            version_status='pub',
            description=self._options['description'],
            notice=self._options['notice'],
        )
        #
        extra_key = ssn_core.SsnHookFileMtd.set_extra_data_save(extra_data)
        #
        option_opt = bsc_core.ArgDictStringOpt(
            option=dict(
                option_hook_key='rsv-task-batchers/asset/gen-any-export-build',
                # choice_scheme='asset-maya-create-and-publish',
                choice_scheme='asset-maya-publish',
                #
                file=file_path,
                #
                extra_key=extra_key,
                maya_scene_srcs=self._maya_scene_src_file_paths,
                katana_scene_srcs=self._katana_scene_src_file_paths,
                movie_file=self._review_mov_file_path,
                # settings for any export
                with_scene=self._options.get('process.settings.with_scene'),
                #
                with_render_texture=self._options.get('process.settings.with_render_texture'),
                with_preview_texture=self._options.get('process.settings.with_preview_texture'),
                #
                with_look_yml=self._options.get('process.settings.with_look_yml'),
                #
                with_camera_abc=self._options.get('process.settings.with_camera_abc'),
                with_camera_usd=self._options.get('process.settings.with_camera_usd'),
                #
                td_enable=self._session.get_is_td_enable(),
                rez_beta=self._session.get_is_beta_enable(),
            )
        )
        #
        ssn_commands.set_option_hook_execute_by_deadline(
            option=option_opt.to_string()
        )

    @utl_core.Modifier.exception_catch
    def execute(self):
        fncs = [
            self.pre_fnc,
            self.collection_review_fnc,
            self.collection_scene_src_fnc,
            self.collection_image_fnc,
            #
            self.farm_process_fnc,
        ]
        with self._window.gui_progressing(maximum=len(fncs), label='execute publish process') as g_p:
            for i_fnc in fncs:
                g_p.set_update()
                i_fnc()
        #
        self._window.show_message(
            'publish process is complected',
            self._window.ValidatorStatus.Correct
        )


class ScpAssetSurfacePublish(object):
    def __init__(self, window, session, scene_file_path, validation_info_file, rsv_task, rsv_scene_properties, options):
        self._window = window
        self._session = session
        self._scene_file_path = scene_file_path
        self._validation_info_file = validation_info_file
        self._rsv_task = rsv_task
        self._rsv_scene_properties = rsv_scene_properties
        self._options = options

    def collection_review_fnc(self):
        self._review_mov_file_path = None
        #
        file_paths = self._options['review']
        if file_paths:
            movie_file_path = _utl_scp_video.ScpVideo.comp_movie(
                file_paths
            )
            self._review_mov_file_path = movie_file_path

    def farm_process_fnc(self):
        version_type = self._options['version_type']
        scene_file_path = self._scene_file_path

        user = bsc_core.SystemMtd.get_user_name()

        extra_data = dict(
            user=user,
            #
            version_type=self._options['version_type'],
            version_status='pub',
            #
            notice=self._options['notice'],
            description=self._options['description'],
        )

        extra_key = ssn_core.SsnHookFileMtd.set_extra_data_save(extra_data)

        application = self._rsv_scene_properties.get('application')
        if application == 'katana':
            choice_scheme = 'asset-katana-publish'
        elif application == 'maya':
            choice_scheme = 'asset-maya-publish'
        else:
            raise RuntimeError()

        option_opt = bsc_core.ArgDictStringOpt(
            option=dict(
                option_hook_key='rsv-task-batchers/asset/gen-surface-export',
                #
                file=scene_file_path,
                #
                extra_key=extra_key,
                #
                choice_scheme=choice_scheme,
                #
                version_type=version_type,
                movie_file=self._review_mov_file_path,
                #
                validation_info_file=self._validation_info_file,
                #
                with_workspace_texture_lock=self._options['process.settings.with_workspace_texture_lock'],
                #
                user=user,
                #
                td_enable=self._session.get_is_td_enable(),
                rez_beta=self._session.get_is_beta_enable(),
                #
                localhost_enable=self._options['process.deadline.scheme'] == 'localhost'
            )
        )
        #
        ssn_commands.set_option_hook_execute_by_deadline(
            option=option_opt.to_string()
        )
    @utl_core.Modifier.exception_catch
    def execute(self):
        fncs = [
            self.collection_review_fnc,
            #
            self.farm_process_fnc,
        ]
        with self._window.gui_progressing(maximum=len(fncs), label='execute publish process') as g_p:
            for i_fnc in fncs:
                g_p.set_update()
                i_fnc()
        #
        self._window.show_message(
            'publish process is complected',
            self._window.ValidatorStatus.Correct
        )

