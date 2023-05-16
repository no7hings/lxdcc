# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    r = rsv_commands.get_resolver()

    rsv_project = r.get_rsv_project(project='lib')

    print rsv_project

    rsv_tags = rsv_project.get_rsv_resource_groups(workspace='work', role=['gmt', 'sdr'])

    print rsv_project.get_rsv_resource_groups(role='ch*')

    # def test():
    #     for rsv_tag in rsv_tags:
    #         print rsv_tag.get_rsv_tasks()
    #
    # import cProfile
    #
    # cProfile.run("test()")
