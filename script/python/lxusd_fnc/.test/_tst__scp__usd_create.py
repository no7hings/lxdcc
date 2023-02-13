# coding:utf-8
import lxusd_fnc.scripts as usd_fnc_scripts

option = 'file=/l/prod/cgm_dev/publish/assets/chr/nn_14y/mod/modeling/nn_14y.mod.modeling.v001/scene/nn_14y.ma&hook_engine=usd&option_hook_key=rsv-task-methods/asset/usd/usd-create&project=cgm_dev&td_enable=True&time_tag=2022_0121_1454_59&user=dongchangbao&with_component_usd=True&start_index=0&end_index=0'

usd_fnc_scripts.set_usd_create_by_any_scene_file(
    option
)
