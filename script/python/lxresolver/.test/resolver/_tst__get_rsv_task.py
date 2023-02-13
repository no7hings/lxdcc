# coding:utf-8
if __name__ == '__main__':
    from lxutil import utl_core

    import lxresolver.commands as rsv_commands

    utl_core.Log.TRACE_RESULT_ENABLE = False

    r = rsv_commands.get_resolver()

    for i_project, i_asset in [
        ('cgm', 'td_test'),
        ('nsa_dev', 'td_test'),
        ('nsa_dev', 'momo'),
    ]:
        i_rsv_project = r.get_rsv_project(project=i_project)

        i_rsv_asset = i_rsv_project.get_rsv_resource(asset=i_asset)
        print i_rsv_asset

        i_rsv_task = i_rsv_asset.get_rsv_task(step='mod', task='modeling')
        print i_rsv_task

        print i_rsv_task._get_user_directory_path_()
