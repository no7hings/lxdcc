# coding:utf-8
import lxshotgun_fnc.scripts as stg_fnc_scripts

option = 'create_shotgun_task=True&create_shotgun_version=True&file=/l/prod/cgm_dev/publish/assets/chr/nn_14y/mod/modeling/nn_14y.mod.modeling.v001/scene/nn_14y.ma&hook_engine=shotgun&option_hook_key=rsv-task-methods/asset/shotgun/version-register&project=cgm_dev&td_enable=True&time_tag=2022_0121_1118_05&user=dongchangbao&start_index=<STARTFRAME>&end_index=<ENDFRAME>'

stg_fnc_scripts.set_shotgun_create_by_any_scene_file(
    option
)
