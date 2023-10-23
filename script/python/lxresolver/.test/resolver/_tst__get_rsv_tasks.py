# coding:utf-8
if __name__ == '__main__':
    from lxbasic import bsc_core

    from lxutil import utl_core

    import lxresolver.commands as rsv_commands

    bsc_core.Log.RESULT_ENABLE = False

    r = rsv_commands.get_resolver()

    for i_project, i_asset in [
        ('cgm', 'td_test'),
        ('nsa_dev', 'momo')
    ]:
        i_rsv_project = r.get_rsv_project(project=i_project)

        i_rsv_asset = i_rsv_project.get_rsv_resource(asset=i_asset)
        print i_rsv_asset

        i_rsv_tasks = i_rsv_asset.get_rsv_tasks()
        print i_rsv_tasks
        # print i_rsv_task.properties
