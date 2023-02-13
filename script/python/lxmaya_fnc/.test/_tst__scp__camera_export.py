# coding:utf-8
import lxmaya

lxmaya.set_reload()

import lxmaya_fnc.scripts as mya_fnc_scripts

scene_src_file_path = '/l/prod/cjd/publish/assets/chr/laohu_xiao/srf/surfacing/laohu_xiao.srf.surfacing.v021/scene/laohu_xiao.katana'

mya_fnc_scripts.set_camera_create_by_any_scene_file(
    'file={}&with_camera_persp_abc=True'.format(scene_src_file_path)
)