# coding:utf-8
import lxmaya

lxmaya.set_reload()

import lxmaya_fnc.scripts as mya_fnc_scripts

scene_src_file_path = '/l/prod/cjd/publish/assets/chr/qunzhongnan_c/srf/srf_anishading/qunzhongnan_c.srf.srf_anishading.v005/scene/qunzhongnan_c.katana'

mya_fnc_scripts.set_camera_create_by_any_scene_file(
    'file={}&with_camera_persp_abc=True'.format(scene_src_file_path)
)
