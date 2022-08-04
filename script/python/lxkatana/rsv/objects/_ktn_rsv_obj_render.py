# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccRenderHookOpt(utl_rsv_obj_abstract.AbsRsvOHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccRenderHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def get_asset_render_file(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-katana-scene-file'
            keyword_1 = 'asset-katana-scene-src-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-katana-scene-file'
            keyword_1 = 'asset-output-katana-scene-src-file'
        else:
            raise TypeError()

        render_use_scene = self._hook_option_opt.get_as_boolean('render_use_scene')
        if render_use_scene is True:
            scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_0
            )
            scene_file_path = scene_file_rsv_unit.get_result(version=version)
            return scene_file_path
        else:
            render_us_scene_src = self._hook_option_opt.get_as_boolean('render_us_scene_src')
            if render_us_scene_src is True:
                scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
                    keyword=keyword_1
                )
                scene_src_file_path = scene_src_file_rsv_unit.get_result(version=version)
                return scene_src_file_path

    def get_asset_render_output_directory(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-katana-render-output-dir'
        elif workspace == 'output':
            keyword_0 = 'asset-output-katana-render-output-dir'
        else:
            raise TypeError()

        render_output_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        rsv_render_output_directory_path = render_output_directory_rsv_unit.get_result(
            version=version
        )
        return rsv_render_output_directory_path

    def set_asset_render_create(self):
        import collections
        #
        from lxbasic import bsc_core
        #
        from lxutil import utl_core

        from lxkatana import ktn_core
        #
        import lxsession.commands as ssn_commands
        #
        option_hook_key = self._hook_option_opt.get('option_hook_key')
        katana_render_hook_key = 'rsv-task-methods/asset/render/katana-render'
        movie_convert_hook_key = 'rsv-task-methods/asset/rv/movie-convert'
        image_convert_hook_key = 'rsv-task-methods/oiio/image-convert'
        #
        batch_file_path = self._hook_option_opt.get('batch_file')
        file_path = self._hook_option_opt.get('file')
        user = self._hook_option_opt.get('user')
        time_tag = self._hook_option_opt.get('time_tag')
        #
        td_enable = self._hook_option_opt.get_as_boolean('td_enable')
        rez_beta = self._hook_option_opt.get_as_boolean('rez_beta')
        #
        render_file_path = self.get_asset_render_file()

        render_settings_node_opt = ktn_core.NGObjOpt('render_settings')
        render_output_directory_path = render_settings_node_opt.get('lynxi_settings.render_output')
        #
        with_convert_movie = self._hook_option_opt.get_as_boolean('with_convert_movie')
        with_convert_image = self._hook_option_opt.get_as_boolean('with_convert_image')
        convert_extra_aovs = self._hook_option_opt.get_as_array('convert_extra_aovs')
        #
        variable_keys = [
            'camera',
            'layer',
            'light_pass',
            'look_pass',
            'quality'
        ]
        #
        variable_mapper = {
            'camera': 'cameras',
            'layer': 'layers',
            'light_pass': 'light_passes',
            'look_pass': 'look_passes',
            'quality': 'qualities',
        }
        variants_dic = collections.OrderedDict()
        for i_variable_key in variable_keys:
            variants_dic[i_variable_key] = self._hook_option_opt.get_as_array(
                variable_mapper[i_variable_key]
            )
        #
        combinations = bsc_core.VariablesMtd.get_all_combinations(
            variants_dic
        )
        with utl_core.log_progress(maximum=len(combinations), label='cmb-render-create') as l_p:
            for i_seq, i_variants in enumerate(combinations):
                l_p.set_update()
                #
                i_key_extend = '-'.join(
                    i_variants.values()
                )
                i_variable_name = '.'.join(
                    i_variants.values()
                )
                i_renderer = 'renderer__{}'.format(
                    '__'.join(['{}'.format(v) for k, v in i_variants.items()])
                )
                #
                i_camera = i_variants['camera']
                if i_camera in ['shot']:
                    i_render_frames = self._hook_option_opt.get('render_shot_frames')
                    i_render_frame_step = int(self._hook_option_opt.get_as_integer('render_shot_frame_step'))
                else:
                    i_render_frames = self._hook_option_opt.get('render_asset_frames')
                    i_render_frame_step = int(self._hook_option_opt.get_as_integer('render_asset_frame_step'))
                #
                if i_render_frame_step > 1:
                    render_frame_range = bsc_core.TextOpt(i_render_frames).to_frame_range()
                    i_render_frames_ = bsc_core.FrameRangeMtd.get(
                        render_frame_range, i_render_frame_step
                    )
                else:
                    i_render_frames_ = bsc_core.TextOpt(i_render_frames).to_frames()
                #
                i_katana_render_hook_option_opt = bsc_core.KeywordArgumentsOpt(
                    dict(
                        option_hook_key=katana_render_hook_key,
                        #
                        batch_file=batch_file_path,
                        # python option
                        file=file_path,
                        #
                        user=user, time_tag=time_tag,
                        #
                        td_enable=td_enable, rez_beta=rez_beta,
                        #
                        render_file=render_file_path,
                        render_output_directory=render_output_directory_path,
                        #
                        renderer=i_renderer,
                        #
                        render_frames=i_render_frames_,
                        #
                        option_hook_key_extend=[i_key_extend],
                        #
                        dependencies=[option_hook_key],
                    )
                )
                #
                i_katana_render_session = ssn_commands.set_option_hook_execute_by_deadline(
                    i_katana_render_hook_option_opt.to_string()
                )
                #
                i_katana_render_ddl_job_id = i_katana_render_session.get_ddl_job_id()
                if i_katana_render_ddl_job_id:
                    if with_convert_movie is True:
                        i_image_file_path_src = '{}/main/{}/beauty.####.exr'.format(
                            render_output_directory_path, i_variable_name
                        )
                        i_movie_file_path_tgt = '{}/main/{}.mov'.format(
                            render_output_directory_path,
                            i_variable_name
                        )
                        i_rv_movie_convert_hook_option_opt = bsc_core.KeywordArgumentsOpt(
                            option=dict(
                                option_hook_key=movie_convert_hook_key,
                                #
                                file=file_path,
                                #
                                user=user, time_tag=time_tag,
                                td_enable=td_enable, rez_beta=rez_beta,
                                #
                                image_file=i_image_file_path_src,
                                movie_file=i_movie_file_path_tgt,
                                #
                                start_frame=i_render_frames_[0],
                                end_frame=i_render_frames_[-1],
                                #
                                option_hook_key_extend=[i_key_extend],
                                dependencies=[option_hook_key],
                                dependent_ddl_job_id_extend=[i_katana_render_ddl_job_id],
                            )
                        )
                        ssn_commands.set_option_hook_execute_by_deadline(
                            i_rv_movie_convert_hook_option_opt.to_string()
                        )
                    #
                    if with_convert_image is True:
                        i_image_file_path_src = '{}/main/{}/beauty.{}.exr'.format(
                            render_output_directory_path,
                            i_variable_name,
                            str(i_render_frames_[0]).zfill(4)
                        )
                        i_image_file_path_tgt = '{}/main/{}.png'.format(
                            render_output_directory_path, i_variable_name
                        )
                        i_rv_movie_convert_hook_option_opt = bsc_core.KeywordArgumentsOpt(
                            option=dict(
                                option_hook_key=image_convert_hook_key,
                                #
                                file=file_path,
                                #
                                user=user, time_tag=time_tag,
                                td_enable=td_enable, rez_beta=rez_beta,
                                #
                                image_file=i_image_file_path_src,
                                output_image_file=i_image_file_path_tgt,
                                #
                                option_hook_key_extend=[i_key_extend],
                                dependencies=[option_hook_key],
                                dependent_ddl_job_id_extend=[i_katana_render_ddl_job_id],
                            )
                        )
                        ssn_commands.set_option_hook_execute_by_deadline(
                            i_rv_movie_convert_hook_option_opt.to_string()
                        )
