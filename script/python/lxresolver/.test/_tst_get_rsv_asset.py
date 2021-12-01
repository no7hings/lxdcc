# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    r = rsv_commands.get_resolver()

    rsv_project = r.get_rsv_project(project='cjd')

    # print rsv_project.get_rsv_entity(asset='sce_td_test')
    # print rsv_project.get_rsv_tasks(asset='sce_td_test', task='modeling')
    # print rsv_project.get_rsv_task(asset='sce_td_test', task='modeling')

    rsv_task = rsv_project.get_rsv_task(asset='huayao', task='groom')

    rsv_unit = rsv_task.get_rsv_unit(keyword='asset-geometry-xgen-file')

    print rsv_unit.get_latest_results()

    rsv_unit = rsv_task.get_rsv_unit(keyword='asset-geometry-xgen-grow-file')

    print rsv_unit.get_latest_results()
