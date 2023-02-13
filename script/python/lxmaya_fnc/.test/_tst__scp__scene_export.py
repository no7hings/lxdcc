# coding:utf-8
import lxmaya

lxmaya.set_reload()

option = 'create_scene_src=False&file=/l/prod/cgm_dev/publish/assets/chr/nn_14y/mod/modeling/nn_14y.mod.modeling.v001/scene/nn_14y.ma&hook_engine=maya&open_file=True&option_hook_key=rsv-task-methods/asset/maya/scene-export&project=cgm_dev&save_file=False&td_enable=True&time_tag=2022_0120_1901_23&user=dongchangbao&with_render_preview=False&with_scene=True&with_snapshot_preview=True&with_texture=False&with_texture_tx=True&start_index=0&end_index=0'

import lxmaya_fnc.scripts as mya_fnc_scripts


mya_fnc_scripts.set_scene_export_by_any_scene_file(option)