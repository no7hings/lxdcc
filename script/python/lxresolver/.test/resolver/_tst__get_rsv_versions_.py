# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    r = rsv_commands.get_resolver()

    rsv_project = r.get_rsv_project(project='lib')

    rsv_task = rsv_project.get_rsv_task(asset='ast_cjd_didi', workspace='publish', step='srf', task='srf_anishading')

    print rsv_task.get_rsv_versions()

