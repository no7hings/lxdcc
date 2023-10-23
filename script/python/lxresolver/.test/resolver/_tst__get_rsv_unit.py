# coding:utf-8
if __name__ == '__main__':
    from lxbasic import bsc_core

    from lxutil import utl_core

    import lxresolver.commands as rsv_commands

    bsc_core.Log.RESULT_ENABLE = False

    r = rsv_commands.get_resolver()

    for i_project, i_asset, i_step, i_task in [
        # ('cgm', 'td_test', 'mod', 'modeling'),
        ('nsa_dev', 'td_test', 'mod', 'modeling'),
        ('nsa_dev', 'momo', 'mod', 'modeling'),
        # ('nsa_dev', 'dl_creatures', 'cpt', 'concept'),
    ]:
        i_rsv_project = r.get_rsv_project(project=i_project)

        i_rsv_task = i_rsv_project.get_rsv_task(asset=i_asset, step=i_step, task=i_task)

        i_rsv_unit = i_rsv_task.get_rsv_unit(
            keyword='{branch}-user-task-dir'
        )

        print i_rsv_unit.properties

        print i_rsv_unit.get_result(
            extend_variants=dict(artist='dongchangbao')
        )

