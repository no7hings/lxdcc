# coding:utf-8
if __name__ == '__main__':
    from lxutil import utl_core

    import lxresolver.commands as rsv_commands

    utl_core.Log.TRACE_RESULT_ENABLE = False

    r = rsv_commands.get_resolver()

    for i_project, i_asset, i_step, i_task in [
        ('cgm', 'td_test', 'mod', 'modeling'),
        ('nsa_dev', 'td_test', 'mod', 'modeling'),
        ('nsa_dev', 'momo', 'mod', 'modeling'),
    ]:
        i_rsv_project = r.get_rsv_project(project=i_project)

        i_rsv_task = i_rsv_project.get_rsv_task(asset=i_asset, step=i_step, task=i_task)

        i_rsv_unit = i_rsv_task.get_rsv_unit(
            keyword='{branch}-maya-scene-src-file'
        )

        print i_rsv_unit.properties

        print i_rsv_unit.get_result(version='latest')
        print i_rsv_unit.get_result(version='all')
        print i_rsv_unit.get_result(version='new')
        print i_rsv_unit.get_result(version='v002')

