# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    r = rsv_commands.get_resolver()

    rsv_project = r.get_rsv_project(project='cgm')

    rsv_task = rsv_project.get_rsv_task(asset='nn_14y_test', step='srf', task='surfacing')

    rsv_unit = rsv_task.get_rsv_unit(keyword='asset-work-maya-scene-src-file')

    print rsv_unit.get_rsv_versions()

