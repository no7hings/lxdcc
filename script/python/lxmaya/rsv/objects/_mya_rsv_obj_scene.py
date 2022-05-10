# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract

from lxbasic import bsc_core

from lxmaya import ma_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.fnc.exporters as mya_fnc_exporters


class RsvDccSceneHookOpt(utl_rsv_obj_abstract.AbsRsvOHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccSceneHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_scene_export(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-maya-scene-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-maya-scene-file'
        else:
            raise TypeError()
        #
        maya_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        maya_scene_file_path = maya_scene_file_rsv_unit.get_result(version=version)
        mya_fnc_exporters.SceneExporter(
            option=dict(
                file=maya_scene_file_path,
                location=root,
                #
                with_xgen_collection=True,
                with_set=True,
                #
                ext_extras=self._hook_option_opt.get('ext_extras', as_array=True)
            )
        ).set_run()
        return maya_scene_file_path

    def set_asset_root_property_refresh(self):
        task = self._rsv_scene_properties.get('task')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')

        mya_root_dag_opt = bsc_core.DccPathDagOpt(root).set_translate_to(
            pathsep='|'
        )
        mya_root = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if mya_root.get_is_exists() is True:
            ma_core.CmdObjOpt(mya_root.path).set_customize_attribute_create(
                'pg_{}_version'.format(task),
                version
            )


class RsvDccShotSceneHookOpt(utl_rsv_obj_abstract.AbsRsvOHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccShotSceneHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_shot_scene_open(self):
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        asset_shot = self._hook_option_opt.get('shot')
        #
        if workspace == 'publish':
            keyword_1 = 'asset-shot-maya-scene-file'
        elif workspace == 'output':
            keyword_1 = 'asset-output-shot-maya-scene-file'
        else:
            raise TypeError()
        #
        asset_shot_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        asset_shot_scene_file_path = asset_shot_scene_file_rsv_unit.get_exists_result(
            version=version,
            extend_variants=dict(
                asset_shot=asset_shot
            )
        )
        if asset_shot_scene_file_path is not None:
            mya_dcc_objects.Scene.set_file_open(
                asset_shot_scene_file_path
            )
        else:
            raise RuntimeError()

    def set_asset_shot_scene_src_copy(self):
        asset_shot = self._hook_option_opt.get('shot')
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-shot-maya-scene-src-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-shot-maya-scene-src-file'
        else:
            raise TypeError()
        #
        rsv_project = self._rsv_task.get_rsv_project()
        rsv_shot = rsv_project.get_rsv_entity(
            shot=asset_shot
        )
        #
        shot_scene_file_rsv_unit = rsv_shot.get_available_rsv_unit(
            task=['final_layout', 'animation', 'blocking', 'rough_layout'],
            keyword='shot-maya-scene-file',
        )
        shot_scene_file_path = shot_scene_file_rsv_unit.get_result(
            version='latest',
        )
        #
        asset_shot_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        asset_shot_scene_src_file_path = asset_shot_scene_src_file_rsv_unit.get_result(
            version=version,
            extend_variants=dict(
                asset_shot=asset_shot
            )
        )
        #
        utl_dcc_objects.OsFile(
            shot_scene_file_path
        ).set_copy_to_file(
            asset_shot_scene_src_file_path
        )

    def set_asset_shot_scene_export(self):
        asset_shot = self._hook_option_opt.get('shot')
        shot_asset = self._hook_option_opt.get('shot_asset')
        #
        workspace = self._rsv_scene_properties.get('workspace')
        version = self._rsv_scene_properties.get('version')
        #
        if workspace == 'publish':
            keyword_0 = 'asset-shot-maya-scene-src-file'
            keyword_1 = 'asset-shot-maya-scene-file'
            keyword_2 = 'asset-maya-scene-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-shot-maya-scene-src-file'
            keyword_1 = 'asset-output-shot-maya-scene-file'
            keyword_2 = 'asset-output-maya-scene-file'
        else:
            raise TypeError()
        #
        asset_shot_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        asset_shot_scene_src_file_path = asset_shot_scene_src_file_rsv_unit.get_exists_result(
            version=version,
            extend_variants=dict(
                asset_shot=asset_shot
            )
        )
        if asset_shot_scene_src_file_path:
            mya_dcc_objects.Scene.set_file_open(asset_shot_scene_src_file_path)
            #
            asset_maya_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_2
            )
            asset_maya_scene_file_path = asset_maya_scene_file_rsv_unit.get_exists_result(
                version=version
            )
            if asset_maya_scene_file_path:
                self._set_shot_asset_rig_replace_(shot_asset, asset_maya_scene_file_path)
            else:
                raise RuntimeError()
            #
            asset_shot_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_1
            )
            asset_shot_scene_file_path = asset_shot_scene_file_rsv_unit.get_result(
                version=version,
                extend_variants=dict(
                    asset_shot=asset_shot
                )
            )
            mya_dcc_objects.Scene.set_file_save_to(
                asset_shot_scene_file_path
            )
        else:
            raise RuntimeError()
    @classmethod
    def _set_shot_asset_rig_replace_(cls, namespace, file_path):
        reference_dict = mya_dcc_objects.References().get_reference_dict()
        if namespace in reference_dict:
            obj = reference_dict[namespace][0]
            obj.set_replace(file_path)
    @classmethod
    def get_shot_asset_dict(cls):
        dict_ = {}
        r = cls.get_resolver()
        reference_raw = mya_dcc_objects.References().get_reference_raw()
        for i_obj, i_namespace, i_file_path in reference_raw:
            i_rsv_task = r.get_rsv_task_by_any_file_path(
                i_file_path
            )
            i_root = i_obj.get_content_obj_paths()[0]
            if i_rsv_task is not None:
                dict_[i_root] = i_namespace, i_rsv_task
        return dict_
