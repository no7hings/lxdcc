# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccTextureHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccTextureHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def execute_render_texture_export(self):
        from lxbasic import bsc_core
        #
        import lxutil.dcc.dcc_operators as utl_dcc_operators
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        import lxmaya.fnc.exporters as mya_fnc_exporters
        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-texture-base-dir'
            keyword_1 = 'asset-texture-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-texture-base-dir'
            keyword_1 = 'asset-temporary-texture-dir'
        else:
            raise RuntimeError()
        #
        texture_src_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        texture_directory_path_src = texture_src_directory_rsv_unit.get_result(
            version=version
        )
        bsc_core.StgPathPermissionMtd.create_directory(texture_directory_path_src)
        #
        texture_tgt_directory_tgt_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        texture_directory_path_tgt = texture_tgt_directory_tgt_unit.get_result(
            version=version
        )
        bsc_core.StgPathPermissionMtd.create_directory(texture_directory_path_tgt)
        #
        # TODO remove orig directory
        mya_fnc_exporters.FncRenderTextureExporter(
            option=dict(
                directory_base=texture_directory_path_src,
                directory=texture_directory_path_tgt,
                #
                location=root,
                #
                fix_name_blank=True,
                with_reference=False,
                #
                use_environ_map=True,
                #
                copy_source=True,
            )
        ).execute()
