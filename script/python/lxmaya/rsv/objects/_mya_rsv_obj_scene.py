# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccSceneHookOpt(utl_rsv_obj_abstract.AbsRsvOHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccSceneHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_scene_export(self):
        import lxutil.dcc.dcc_objects as utl_dcc_objects

        import lxmaya.fnc.exporters as mya_fnc_exporters
        #
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
        maya_scene_src_file_path = self._hook_option_opt.get('file')
        maya_scene_file_path = maya_scene_file_rsv_unit.get_result(version=version)
        mya_fnc_exporters.SceneExporter(
            file_path=maya_scene_file_path,
            root=root,
            option=dict(
                with_xgen_collection=True,
                with_set=True
            )
        ).set_run()
        #
        ext_extras = self._hook_option_opt.get('ext_extras', as_array=True)
        if ext_extras:
            file_src = utl_dcc_objects.OsFile(maya_scene_src_file_path)
            file_tgt = utl_dcc_objects.OsFile(maya_scene_file_path)
            for i_ext in ext_extras:
                i_src = '{}.{}'.format(file_src.path_base, i_ext)
                i_tgt = '{}.{}'.format(file_tgt.path_base, i_ext)
                utl_dcc_objects.OsFile(i_src).set_copy_to_file(i_tgt)
        return maya_scene_file_path

    def set_root_property_refresh(self):
        from lxbasic import bsc_core

        from lxmaya import ma_core
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        workspace = self._rsv_scene_properties.get('workspace')
        task = self._rsv_scene_properties.get('task')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')

        mya_root_dat_opt = bsc_core.DccPathDagOpt(root).set_translate_to(
            pathsep='|'
        )
        mya_root = mya_dcc_objects.Group(
            mya_root_dat_opt.get_value()
        )
        if mya_root.get_is_exists() is True:
            ma_core.CmdObjOpt(mya_root.path).set_customize_attribute_create(
                'pg_{}_version'.format(task),
                version
            )
