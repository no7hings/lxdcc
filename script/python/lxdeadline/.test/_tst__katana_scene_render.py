# coding:utf-8
if __name__ == '__main__':
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    from lxdeadline import ddl_core
    #
    import lxdeadline.methods as ddl_methods
    #
    utl_core.Environ.set_td_enable(True)
    #
    resolver = rsv_commands.get_resolver()
    #
    any_scene_file_path = '/l/prod/cjd/publish/assets/chr/huayao/srf/srf_cfxshading/huayao.srf.srf_cfxshading.v005/scene/huayao.katana'
    render_katana_file_path = '/l/prod/cjd/publish/assets/chr/huayao/srf/srf_cfxshading/huayao.srf.srf_cfxshading.v005/render/katana/huayao.katana'
    #
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
    #
    katana_look_checker_export = ddl_methods.DdlRsvTaskRender(
        method_option=ddl_core.DdlRsvTaskRenderOption.get_katana_scene_render(rsv_task_properties),
        script_option='file={}&render_file={}&quality=R2&frame=1+2&renderer=default__renderer&td_enable=True'.format(
            any_scene_file_path,
            render_katana_file_path
        ),
    )
    katana_look_checker_export.set_run_with_deadline()
