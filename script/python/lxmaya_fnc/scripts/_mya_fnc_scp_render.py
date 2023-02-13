# coding:utf-8
import sys
from lxmaya_fnc.scripts import _mya_fnc_scp_utility


def set_render_scene_create_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxresolver.commands as rsv_commands
    #
    import lxshotgun_fnc.scripts as stg_fnc_scripts
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    scene_src_file_path = option_opt.get('file')
    scene_src_file_path = utl_core.Path.set_map_to_platform(scene_src_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_src_file_path)
    if rsv_task_properties:
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            step = rsv_task_properties.get('step')
            if step in ['mod', 'srf']:
                pass


def set_asset_render_scene_create(rsv_task_properties):
    pass
