# coding:utf-8
if __name__ == '__main__':
    from lxutil import utl_core
    #
    from lxdeadline import ddl_core
    #
    import lxdeadline.methods as ddl_methods
    #
    import lxresolver.commands as rsv_commands

    resolver = rsv_commands.get_resolver()
    #
    utl_core.Environ.set_td_enable(True)
    #
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(
        file_path='/l/prod/cjd/publish/assets/chr/td_test/srf/surfacing/td_test.srf.surfacing.v060/scene/td_test.ma'
    )
