# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccSceneHookOpt(utl_rsv_obj_abstract.AbsRsvOHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccSceneHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_scene_src_create(self):
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects

        import lxkatana.fnc.importers as ktn_fnc_importers

        import lxkatana.fnc.creators as ktn_fnc_creators
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-katana-scene-src-file'
            keyword_1 = 'asset-look-ass-file'
            keyword_2 = 'asset-look-ass-sub-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-katana-scene-src-file'
            keyword_1 = 'asset-output-look-ass-file'
            keyword_2 = 'asset-output-look-ass-sub-file'
        else:
            raise TypeError()

        scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_src_file_path = scene_src_file_rsv_unit.get_result(
            version=version
        )
        # save first
        ktn_dcc_objects.Scene.set_file_save_to(scene_src_file_path)

        ktn_fnc_creators.LookWorkspaceCreator().set_run()

        look_ass_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        look_ass_file_path = look_ass_file_rsv_unit.get_exists_result(
            version=version
        )
        if look_ass_file_path:
            ktn_fnc_importers.LookAssImporter(
                option=dict(
                    file=look_ass_file_path,
                    location='/root/materials',
                    look_pass='default'
                )
            ).set_run()

            look_ass_sub_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_2
            )
            look_ass_sub_file_paths = look_ass_sub_file_rsv_unit.get_results(
                version=version
            )
            for i_file_path in look_ass_sub_file_paths:
                i_properties = look_ass_sub_file_rsv_unit.get_properties_by_result(i_file_path)
                i_look_pass_name = i_properties.get('look_pass')
                ktn_fnc_importers.LookAssImporter(
                    option=dict(
                        file=i_file_path,
                        location='/root/materials',
                        look_pass=i_look_pass_name
                    )
                ).set_run()
        else:
            raise RuntimeError()

        ktn_dcc_objects.Scene.set_file_save_to(scene_src_file_path)
        return scene_src_file_path

    def set_asset_scene_export(self):
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = '{branch}-katana-scene-file'
        elif workspace == 'output':
            keyword_0 = '{branch}-output-katana-scene-file'
        else:
            raise TypeError()
        #
        scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_file_path = scene_file_rsv_unit.get_result(
            version=version
        )
        ktn_dcc_objects.Scene.set_file_save_to(scene_file_path)
        return scene_file_path

    def get_scene_src_file_path(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-katana-scene-src-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-katana-scene-src-file'
        else:
            raise TypeError()

        scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_src_file_path = scene_src_file_rsv_unit.get_result(
            version=version
        )
        return scene_src_file_path

    def set_asset_scene_create(self):
        import fnmatch

        from lxkatana import ktn_core

        import lxkatana.dcc.dcc_objects as ktn_dcc_objects

        import lxkatana.fnc.creators as ktn_fnc_creators
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-katana-scene-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-katana-scene-file'
        else:
            raise TypeError()

        katana_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        katana_scene_file_path = katana_scene_file_rsv_unit.get_result(version=version)

        render_file_path = katana_scene_file_path
        ktn_dcc_objects.Scene.set_file_save_to(render_file_path)
        # create workspace
        ktn_fnc_creators.LookWorkspaceCreator().set_run()
        #
        look_pass_names = self._hook_option_opt.get('look_passes')
        if 'white_disp' in look_pass_names:
            self.set_white_disp_create()

        if 'white_zbrush' in look_pass_names:
            self.set_white_zbrush_create()
        #
        shot_name = self._hook_option_opt.get('shot')
        if shot_name:
            shot_geometries_node_opt = ktn_core.NGObjOpt('shot__geometries')
            shot_paths = shot_geometries_node_opt.get_as_enumerate('options.shot')
            _ = fnmatch.filter(shot_paths, '*/{}'.format(shot_name))
            if _:
                shot_geometries_node_opt.set('options.shot', _[0])
            shot_geometries_node_opt.set_port_execute('usd.create')
        #
        render_arnold_aov_enable = self._hook_option_opt.get('render_arnold_aov_enable')
        qualities = self._hook_option_opt.get('qualities', as_array=True)
        for i_quality in qualities:
            i_quality_dcc_node = ktn_dcc_objects.Node('{}__quality'.format(i_quality))
            #
            i_quality_dcc_node.set('lynxi_variants.arnold.aov_enable', render_arnold_aov_enable)
        #
        render_override_enable = self._hook_option_opt.get('render_override_enable')
        if render_override_enable is True:
            render_override_percent = self._hook_option_opt.get('render_override_percent')
            #
            qualities = self._hook_option_opt.get('qualities', as_array=True)
            for i_quality in qualities:
                i_quality_dcc_node = ktn_dcc_objects.Node('{}__quality'.format(i_quality))
                #
                i_quality_dcc_node.set('lynxi_variants.percent', render_override_percent)
        #
        render_arnold_override_enable = self._hook_option_opt.get('render_arnold_override_enable')
        if render_arnold_override_enable is True:
            render_arnold_override_aa_sample = self._hook_option_opt.get('render_arnold_override_aa_sample')
            #
            qualities = self._hook_option_opt.get('qualities', as_array=True)
            for i_quality in qualities:
                i_quality_dcc_node = ktn_dcc_objects.Node('{}__quality'.format(i_quality))
                #
                i_quality_dcc_node.set('lynxi_variants.arnold_override_enable', True)
                i_quality_dcc_node.set('lynxi_variants.arnold_override.aa_sample', render_arnold_override_aa_sample)
        #
        render_settings_node_opt = ktn_core.NGObjOpt('render_settings')
        render_output_directory_path = self._hook_option_opt.get('render_output_directory')
        render_output_file_path = '{}/main/<camera>.<layer>.<light-pass>.<look-pass>.<quality>/<render-pass>.####.exr'.format(
            render_output_directory_path
        )
        render_settings_node_opt.set(
            'lynxi_settings.render_output', render_output_file_path
        )
        #
        renderer_node_opt = ktn_core.NGObjOpt('render_outputs')

        variable_keys = [
            'cameras',
            'layers',
            'light_passes',
            'look_passes',
            'qualities',
        ]
        for i_variable_key in variable_keys:
            renderer_node_opt.set(
                'lynxi_variants.{}'.format(i_variable_key),
                ', '.join(self._hook_option_opt.get(i_variable_key, as_array=True))
            )

        renderer_node_opt.set_port_execute('create')
        ktn_dcc_objects.Scene.set_file_save()

    def set_white_disp_create(self):
        import lxkatana.fnc.importers as ktn_fnc_importers

        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')

        if workspace == 'publish':
            keyword_0 = 'asset-look-ass-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-look-ass-file'
        else:
            raise TypeError()

        look_ass_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=keyword_0)
        look_ass_file_path = look_ass_file_rsv_unit.get_exists_result(version=version)
        if look_ass_file_path:
            ktn_fnc_importers.LookAssImporter(
                option=dict(
                    file=look_ass_file_path,
                    auto_white_disp_assign=True,
                    look_pass='white_disp'
                )
            ).set_run()

    def set_white_zbrush_create(self):
        import lxkatana.fnc.importers as ktn_fnc_importers

        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')

        if workspace == 'publish':
            keyword_0 = 'asset-look-ass-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-look-ass-file'
        else:
            raise TypeError()

        look_ass_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=keyword_0)
        look_ass_file_path = look_ass_file_rsv_unit.get_exists_result(version=version)
        if look_ass_file_path:
            ktn_fnc_importers.LookAssImporter(
                option=dict(
                    file=look_ass_file_path,
                    auto_white_zbrush_assign=True,
                    look_pass='white_zbrush'
                )
            ).set_run()

    def set_front_camera(self):
        pass
