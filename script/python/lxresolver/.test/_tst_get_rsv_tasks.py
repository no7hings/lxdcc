# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    r = rsv_commands.get_resolver()

    rsv_project = r.get_rsv_project(project='cjd')

    rsv_tasks = rsv_project.get_rsv_tasks(branch='asset', role='chr', task='surfacing')
    lis = []
    for i_rsv_task in rsv_tasks:
        camera_abc_file_unit = i_rsv_task.get_rsv_unit(keyword='asset-camera-abc-file')
        camera_abc_file_path = camera_abc_file_unit.get_result()
        if camera_abc_file_path is not None:
            print i_rsv_task
            lis.append(i_rsv_task.properties.get('asset'))

    print lis

