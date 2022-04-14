# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxresolver.commands as rsv_commands

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


def set_surface_light_rig_update_(task_properties):
    import copy
    #
    resolver = rsv_commands.get_resolver()
    branch = task_properties.get('branch')
    step = task_properties.get('step')
    if branch == 'asset' and step == 'srf':
        node_dcc_obj = ktn_dcc_objects.AssetWorkspace().set_light_rig_update()

        _kwargs = copy.copy(task_properties)

        rsv_task = resolver.get_rsv_task(**task_properties.value)

        render_dir = rsv_task.get_rsv_unit(
            keyword='asset-work-render-dir',
            workspace='output'
        )
        render_dir_path = render_dir.get_result()
        node_dcc_obj.get_port('user.Output_Path').set(render_dir_path)
        utl_dcc_objects.OsDirectory_(render_dir_path).set_create()
