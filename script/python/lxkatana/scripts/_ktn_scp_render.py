# coding:utf-8
import copy

from lxbasic import bsc_core

from lxkatana import ktn_core

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

from lxkatana.scripts import _ktn_scp_macro_extra


class ScpRenderLayer(object):
    VERSION_KEY = 'render_version'
    def __init__(self, obj_opt):
        self._obj_opt = obj_opt

        i_scp = _ktn_scp_macro_extra.ScpWspRenderLayer(self._obj_opt._ktn_obj)
        self._variant = i_scp.get_variants()
        self._variant.pop(self.VERSION_KEY)
    @classmethod
    def _to_render_layer_(cls, opt_opt):
        parent_opt = opt_opt.get_parent_opt()
        if parent_opt.get('type') == 'RenderLayer_Wsp':
            return parent_opt
    @classmethod
    def _get_real_version_(cls, version, pattern_opt, version_key):
        if version == 'new':
            return pattern_opt.get_new_version(version_key=version_key)
        elif version == 'latest':
            return pattern_opt.get_latest_version(version_key=version_key)
        else:
            return version

    def get_render_version(self, default_render_version):
        render_version_mode = self._obj_opt.get('parameters.render.version.mode')
        directory_p = self._obj_opt.get('parameters.render.output.directory')
        directory_p_opt = bsc_core.PtnParseOpt(directory_p)
        # check is valid
        if directory_p_opt.get_keys():
            directory_p_opt.set_update(**self._variant)
            #
            if render_version_mode == 'default':
                version = self._get_real_version_(default_render_version, directory_p_opt, self.VERSION_KEY)
            elif render_version_mode == 'new':
                version = directory_p_opt.get_new_version(version_key=self.VERSION_KEY)
            elif render_version_mode == 'latest':
                version = directory_p_opt.get_latest_version(version_key=self.VERSION_KEY)
            elif render_version_mode == 'customize':
                version = self._obj_opt.get('parameters.render.version.customize')
            else:
                raise RuntimeError()
            return version
        return default_render_version

    def get_render_output_directory(self, default_render_version):
        directory_p = self._obj_opt.get('parameters.render.output.directory')
        directory_p_opt = bsc_core.PtnParseOpt(directory_p)
        # check is valid
        if directory_p_opt.get_keys():
            directory_p_opt.set_update(**self._variant)
            version_kwargs = {}
            render_version = self.get_render_version(default_render_version)
            version_kwargs[self.VERSION_KEY] = render_version
            directory_p_opt.set_update(**version_kwargs)
            return directory_p_opt.get_value()
        else:
            return directory_p_opt.get_value()

    def get_latest_render_output_image(self):
        directory_p = self._obj_opt.get('parameters.render.output.directory')
        directory_p_opt = bsc_core.PtnParseOpt(directory_p)
        # check is valid
        if directory_p_opt.get_keys():
            directory_p_opt.set_update(**self._variant)
            results = directory_p_opt.get_match_results(sort=True)
            if results:
                directory = results[-1]
                variant = copy.copy(self._variant)
                image_sub_p = self._obj_opt.get('parameters.render.output.builtin.image_pattern')
                image_file_p = bsc_core.PtnParseOpt('{}{}'.format(directory, image_sub_p))
                variant.update(dict(aov='primary'))
                image_file_p.set_update(**variant)
                return image_file_p.get_value()

    def get_render_output_directory_key(self):
        directory_p = self._obj_opt.get('parameters.render.output.directory')
        directory_p_opt = bsc_core.PtnParseOpt(directory_p)
        directory_p_opt.set_update(**self._variant)
        return directory_p_opt.get_value()

    def get_render_frames(self, default_render_frames):
        render_frames_mode = self._obj_opt.get('parameters.render.frames.mode')
        if render_frames_mode == 'default':
            render_frames_string = default_render_frames
        elif render_frames_mode == 'customize':
            render_frames_string = self._obj_opt.get('parameters.render.frames.customize')
        else:
            raise RuntimeError()
        return render_frames_string


class ScpRenderBuild(object):
    KEY = 'render build'
    def __init__(self, session):
        self._session = session
        self._hook_option_opt = self._session.option_opt
    @classmethod
    def _get_real_version_(cls, version, pattern_opt, version_key):
        if version == 'new':
            return pattern_opt.get_new_version(version_key=version_key)
        elif version == 'latest':
            return pattern_opt.get_latest_version(version_key=version_key)
        else:
            return version
    @ktn_core.Modifier.undo_run
    def refresh_all_render_layers_output(self, default_render_version='new'):
        key = 'render process'

        from lxkatana.scripts import _ktn_scp_macro_extra

        version_key = 'render_version'

        render_layers = ktn_core.NGObjsMtd.find_nodes_by_port_filters(
            type_name='Group', filters=[('type', 'in', {'RenderLayer_Wsp', 'RenderLayer_Wsp_Usr'})]
        )
        for i_render_layer in render_layers:
            i_obj_opt = ktn_core.NGObjOpt(i_render_layer)
            i_scp = _ktn_scp_macro_extra.ScpWspRenderLayer(i_render_layer)
            i_kwargs = i_scp.get_variants()
            i_kwargs.pop(version_key)
            i_render_version_mode = i_obj_opt.get('parameters.render.version.mode')
            i_directory_p = i_obj_opt.get('parameters.render.output.directory')
            i_directory_p_opt = bsc_core.PtnParseOpt(i_directory_p)
            # check is valid
            if i_directory_p_opt.get_keys():
                i_directory_p_opt.set_update(**i_kwargs)
                #
                i_version_kwargs = {}
                if i_render_version_mode == 'default':
                    i_version = self._get_real_version_(default_render_version, i_directory_p_opt, version_key)
                elif i_render_version_mode == 'new':
                    i_version = i_directory_p_opt.get_new_version(version_key=version_key)
                elif i_render_version_mode == 'latest':
                    i_version = i_directory_p_opt.get_latest_version(version_key=version_key)
                elif i_render_version_mode == 'customize':
                    i_version = i_obj_opt.get('parameters.render.version.customize')
                else:
                    raise RuntimeError()
                #
                i_version_kwargs[version_key] = i_version
                i_directory_p_opt.set_update(**i_version_kwargs)
                # check is valid
                if not i_directory_p_opt.get_keys():
                    i_result = i_directory_p_opt.get_value()
                    #
                    i_obj_opt.set('parameters.render.output.directory', i_result)
                    #
                    bsc_core.LogMtd.trace_method_result(
                        key,
                        'node: "{}"'.format(
                            i_obj_opt.get_path()
                        )
                    )
                    # create directory
                    bsc_core.StgPathPermissionMtd.create_directory(
                        i_result
                    )
                else:
                    bsc_core.LogMtd.trace_method_error(
                        key,
                        'node: "{}" is failed'.format(
                            i_obj_opt.get_path()
                        )
                    )
            else:
                bsc_core.LogMtd.trace_method_warning(
                    key,
                    'node: "{}" not any variant for convert, ignore'.format(
                        i_obj_opt.get_path()
                    )
                )
    @classmethod
    def _to_render_layer_(cls, opt_opt):
        parent_opt = opt_opt.get_parent_opt()
        if parent_opt.get('type') == 'RenderLayer_Wsp':
            return parent_opt

    def copy_file(self):
        from lxbasic import bsc_core
        #
        import lxbasic.extra.methods as bsc_etr_methods
        #
        file_path = self._hook_option_opt.get('file')

        render_file_path = bsc_core.StgFileOpt(
            file_path
        ).get_render_file_path()
        #
        bsc_core.StgPathPermissionMtd.copy_to_file(
            file_path,
            render_file_path
        )
        self._hook_option_opt.set(
            'render_file', render_file_path
        )

    def pre_process(self):
        render_file_path = self._hook_option_opt.get('render_file')

        ktn_dcc_objects.Scene.set_file_open(render_file_path)

        default_render_version = self._hook_option_opt.get('default_render_version')

        self.refresh_all_render_layers_output(
            default_render_version=default_render_version
        )

        ktn_dcc_objects.Scene.set_file_save()

    def build_render_job(self):
        render_file_path = self._hook_option_opt.get('render_file')
        ktn_dcc_objects.Scene.set_file_open(render_file_path)
        self._build_render_job_(
            hook_option_opt=self._hook_option_opt
        )
    @classmethod
    def _build_render_job_(cls, hook_option_opt):
        import lxsession.commands as ssn_commands

        auto_convert_mov = hook_option_opt.get_as_boolean('auto_convert_mov')

        default_render_frames = hook_option_opt.get('default_render_frames')

        render_nodes = hook_option_opt.get_as_array(
            'render_nodes'
        )
        option_hook_key = hook_option_opt.get('option_hook_key')
        batch_name = hook_option_opt.get('batch_name')
        batch_file_path = hook_option_opt.get('batch_file')
        file_path = hook_option_opt.get('file')
        render_file_path = hook_option_opt.get('render_file')
        user = hook_option_opt.get('user')
        time_tag = hook_option_opt.get('time_tag')
        td_enable = hook_option_opt.get('td_enable')
        rez_beta = hook_option_opt.get('rez_beta')
        #
        katana_render_hook_key = 'rsv-project-methods/katana/render'
        rv_video_comp_hook_key = 'rsv-project-methods/rv/video-comp'
        with bsc_core.LogProgress.create_as_bar(maximum=len(render_nodes), label=cls.KEY) as l_p:
            for i_render_node in render_nodes:
                l_p.set_update()
                if ktn_core.NGObjOpt._get_is_exists_(i_render_node) is True:
                    i_render_node_opt = ktn_core.NGObjOpt(i_render_node)
                    i_render_layer_opt = cls._to_render_layer_(i_render_node_opt)
                    if i_render_layer_opt is not None:
                        i_render_frames_mode = i_render_layer_opt.get('parameters.render.frames.mode')
                        if i_render_frames_mode == 'default':
                            i_render_frames_string = default_render_frames
                        elif i_render_frames_mode == 'customize':
                            i_render_frames_string = i_render_layer_opt.get('parameters.render.frames.customize')
                        else:
                            raise RuntimeError()
                    else:
                        i_render_frames_string = default_render_frames
                    #
                    i_render_output_image_file_path = ktn_core.SGStageOpt(
                        i_render_node_opt._ktn_obj
                    ).get(
                        '/root.renderSettings.outputs.primary.locationSettings.renderLocation'
                    )
                    #
                    i_render_output_directory_path = bsc_core.StgFileOpt(i_render_output_image_file_path).get_directory_path()
                    i_vedio_file_path = '{}/primary.mov'.format(i_render_output_directory_path)
                    #
                    i_render_frames = bsc_core.RawTextOpt(i_render_frames_string).to_frames()
                    #
                    i_katana_render_hook_option_opt = bsc_core.ArgDictStringOpt(
                        dict(
                            option_hook_key=katana_render_hook_key,
                            #
                            batch_name=batch_name,
                            #
                            batch_file=batch_file_path,
                            file=file_path,
                            #
                            user=user, time_tag=time_tag,
                            td_enable=td_enable, rez_beta=rez_beta,
                            #
                            render_file=render_file_path,
                            render_output_directory=i_render_output_directory_path,
                            render_node=i_render_node,
                            #
                            render_frames=i_render_frames,
                            #
                            option_hook_key_extend=[i_render_node, 'image'],
                            #
                            dependencies=[option_hook_key],
                        )
                    )
                    i_katana_render_session = ssn_commands.set_option_hook_execute_by_deadline(
                        i_katana_render_hook_option_opt.to_string()
                    )
                    #
                    if auto_convert_mov is True:
                        i_katana_render_ddl_job_id = i_katana_render_session.get_ddl_job_id()
                        i_rv_movie_convert_hook_option_opt = bsc_core.ArgDictStringOpt(
                            option=dict(
                                option_hook_key=rv_video_comp_hook_key,
                                #
                                batch_name=batch_name,
                                #
                                batch_file=batch_file_path,
                                file=file_path,
                                #
                                user=user, time_tag=time_tag,
                                td_enable=td_enable, rez_beta=rez_beta,
                                #
                                image_file=i_render_output_image_file_path,
                                video_file=i_vedio_file_path,
                                #
                                render_output_directory=i_render_output_directory_path,
                                #
                                start_frame=i_render_frames[0],
                                end_frame=i_render_frames[-1],
                                #
                                option_hook_key_extend=[i_render_node, 'video'],
                                #
                                dependencies=[option_hook_key],
                                #
                                dependent_ddl_job_id_extend=[i_katana_render_ddl_job_id]
                            )
                        )
                        ssn_commands.set_option_hook_execute_by_deadline(
                            i_rv_movie_convert_hook_option_opt.to_string()
                        )
                else:
                    bsc_core.LogMtd.trace_method_warning(
                        cls.KEY,
                        'render-node: "{}" is non-exists'.format(i_render_node)
                    )

    def execute(self):
        self.copy_file()
        self.pre_process()
        self.build_render_job()