# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    r = rsv_commands.get_resolver()

    rsv_project = r.get_rsv_project(project='cjd')

    print rsv_project.get_rsv_resource(asset='sce_td_test')
