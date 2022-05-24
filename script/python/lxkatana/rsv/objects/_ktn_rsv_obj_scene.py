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

