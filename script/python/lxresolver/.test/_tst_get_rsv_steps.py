# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    r = rsv_commands.get_resolver()

    rsv_project = r.get_rsv_project(project='lib')

    print rsv_project

    rsv_steps = rsv_project.get_rsv_steps(workspace='work', role=['chr', 'prp'])
