# coding:utf-8
if __name__ == '__main__':
    from lxutil import utl_core
    import lxresolver.commands as rsv_commands

    utl_core.Log.PRINT_ENABLE = False
    r = rsv_commands.get_resolver()

    rsv_project = r.get_rsv_project(project='cjd')

    rsv_tasks = rsv_project.get_rsv_tasks(branch='asset', asset='nn_*', task=['surfacing', 'modeling'])
    lis = []
    for i_rsv_task in rsv_tasks:
        print i_rsv_task.properties
        i_rsv_unit = i_rsv_task.get_rsv_unit(
            keyword='asset-maya-scene-file'
        )
        print i_rsv_unit.get_result(version='all')
        print i_rsv_unit.properties
        # camera_abc_file_unit = i_rsv_task.get_rsv_unit(keyword='asset-camera-persp-abc-file')
        # camera_abc_file_path = camera_abc_file_unit.get_result()
        # if camera_abc_file_path is not None:
        #     lis.append(i_rsv_task.properties.get('asset'))

    print lis

