# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract

from lxbasic import bsc_core
#
from lxutil import utl_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects
#
import lxmaya.fnc.exporters as mya_fnc_exporters


class RsvDccCameraHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccCameraHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_camera_main_abc_export(self):
        key = 'camera main abc export'
        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        pathsep = rsv_scene_properties.get('dcc.pathsep')
        #
        location = '/camera_grp'
        #
        mya_location = bsc_core.DccPathDagOpt(location).set_translate_to(
            pathsep=pathsep
        ).to_string()
        mya_group = mya_dcc_objects.Group(
            mya_location
        )
        if mya_group.get_is_exists() is True:
            if workspace == 'publish':
                keyword = 'asset-camera-main-abc-file'
            else:
                raise RuntimeError(
                    utl_core.Log.set_module_error_trace(
                        key,
                        u'workspace="{}" is not available'.format(workspace)
                    )
                )
            #
            camera_main_abc_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword
            )
            camera_main_abc_file_path = camera_main_abc_file_rsv_unit.get_result(
                version=version
            )
            frame_range = self._hook_option_opt.get('camera_main_frame_range', as_array=True)
            #
            mya_fnc_exporters.CameraAbcExport(
                dict(
                    file=camera_main_abc_file_path,
                    location='/camera_grp',
                    frame=frame_range,
                )
            ).set_run()
        else:
            raise RuntimeError(
                utl_core.Log.set_module_error_trace(
                    key,
                    u'obj="{}" is non-exists'.format(mya_group.path)
                )
            )
