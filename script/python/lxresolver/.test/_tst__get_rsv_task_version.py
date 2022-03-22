# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    r = rsv_commands.get_resolver()

    rsv_project = r.get_rsv_project(project='cgm')

    rsv_task = rsv_project.get_rsv_task(asset='nn_14y_test', step='srf', task='surfacing')

    print rsv_task.get_rsv_versions()

    print rsv_project.get_rsv_task_version(
        asset='nn_14y_test', step='srf', task='surfacing', version='v001'
    )
    print rsv_project.get_rsv_task_versions(
        asset='nn_14y_test', step='srf', task='surfacing'
    )

