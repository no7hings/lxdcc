# coding:utf-8

def main(session):
    def yes_method_0():
        def yes_method_1():
            import lxdeadline.objects as ddl_objects
            #
            import lxdeadline.methods as ddl_methods
            #
            method_query = ddl_objects.DdlMethodQuery(
                key='lib-asset-pull', extend_option_kwargs=dict(configure=_project_tgt)
            )
            #
            method = ddl_methods.DdlMethodRunner(
                method_option=method_query.get_method_option(),
                script_option=method_query.get_script_option(
                    project=_project_tgt,
                    assets=[_asset_tgt],
                    #
                    with_system_create=True,
                    with_system_permission_create=True,
                    #
                    with_shotgun_create=True,
                    with_file_copy=True,
                    with_surface_publish=True,
                    #
                    user=bsc_core.SystemMtd.get_user_name(), time_tag=bsc_core.SystemMtd.get_time_tag(),
                    td_enable=True
                )
            )
            #
            method.set_run_with_deadline()
        #
        _kwargs = w.get_option_as_kwargs()
        _project_tgt = _kwargs['project']
        _asset_tgt = asset_src
        #
        _rsv_asset_tgt = resolver.get_rsv_entity(
            project=_project_tgt, asset=asset_src
        )
        if _rsv_asset_tgt is not None:
            utl_core.DialogWindow.set_create(
                window_title,
                content=(
                    'asset:\n'
                    '"{}"\n'
                    'asset is already exists\n'
                    'do you want to override exists...'
                ).format(
                    _asset_tgt
                ),
                yes_method=yes_method_1,
                yes_label='Override',
                no_label='Don\'t Override',
                status=bsc_configure.GuiStatus.Warning,
                use_exec=False
            )
        else:
            yes_method_1()
    #
    def get_projects():
        lis = []
        shotgun_connector = session.get_shotgun_connector()
        for stg_project_query in shotgun_connector.get_stg_project_queries():
            if stg_project_query.get('sg_studio') in ['CG']:
                name = stg_project_query.get('tank_name')
                if name:
                    lis.append(name)
        #
        lis.sort()
        return lis
    #
    from lxbasic import bsc_configure, bsc_core
    #
    from lxutil import utl_core
    #
    import lxutil_gui.proxy.widgets as prx_widgets

    import lxresolver.commands as rsv_commands
    #
    import lxgui.fnc.methods as gui_fnc_methods
    #
    resolver = rsv_commands.get_resolver()
    #
    rsv_entity = session.rsv_obj
    #
    project = rsv_entity.get('project')
    asset_src = rsv_entity.get('asset')
    #
    window_title = 'Pull Asset from "LIB"'
    if project in ['lib']:
        w = utl_core.DialogWindow.set_create(
            window_title,
            content=(
                'asset:\n'
                '"{}"\n'
                'select a project and press "Yes" to continue...'.format(
                    asset_src
                )
            ),
            yes_method=yes_method_0,
            show=False,
            use_exec=False
        )
        w.set_option_group_enable()
        #
        p = w._option_node.set_port_add(
            prx_widgets.PrxChoosePort(
                'project', 'Project'
            )
        )
        projects = ['shl', 'cjd']
        p.set(values=projects)
        #
        w.set_window_show()
    else:
        utl_core.DialogWindow.set_create(
            window_title,
            content='project "{}" is not support...'.format(project),
            status=bsc_configure.GuiStatus.Error
        )


# noinspection PyUnresolvedReferences
main(session)

