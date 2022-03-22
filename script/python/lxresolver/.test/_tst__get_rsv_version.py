# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    r = rsv_commands.get_resolver()

    rsv_project = r.get_rsv_project(project='lib')

    rsv_version = rsv_project.get_rsv_task_versions(
        asset='ast_cjd_didi',
        workspace='publish',
        # step='srf',
        task='srf_anishading',
        version='v00*'
    )

    print rsv_version

