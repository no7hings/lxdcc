# coding:utf-8


def main(session):
    def yes_method_0():
        import lxdeadline.objects as ddl_objects
        #
        import lxdeadline.methods as ddl_methods
        #
        method_query = ddl_objects.DdlMethodQuery(
            key='lib-asset-push', extend_option_kwargs=dict(configure='lib')
        )
        #
        method = ddl_methods.DdlMethodRunner(
            method_option=method_query.get_method_option(),
            script_option=method_query.get_script_option(
                project=project,
                assets=[asset_src],
                #
                with_system_create=True,
                with_system_permission_create=False,
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
    from lxbasic import bsc_configure, bsc_core
    #
    from lxutil import utl_core
    #
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
    window_title = 'Push Asset to "LIB"'
    #
    if project not in ['lib']:
        #
        asset_tgt = gui_fnc_methods.LibAssetPusher._get_lib_asset_(
            project, asset_src
        )
        lib_rsv_asset = resolver.get_rsv_entity(
            project='lib',
            asset=asset_tgt
        )
        if lib_rsv_asset is None:
            content = (
                'asset:\n'
                'from "{}" to "{}"\n'
                'press "Yes" to continue...'
            ).format(
                asset_src, asset_tgt
            )
            status = bsc_configure.GuiStatus.Normal
        else:
            content = (
                'asset is already exists:\n'
                'from "{}" to "{}"\n'
                'press "Yes" to continue...'
            ).format(
                asset_src, asset_tgt
            )
            status = bsc_configure.GuiStatus.Warning
        #
        utl_core.DialogWindow.set_create(
            window_title,
            content=content,
            yes_method=yes_method_0,
            status=status
        )
    else:
        utl_core.DialogWindow.set_create(
            window_title,
            content='project "{}" is not support...'.format(project),
            status=bsc_configure.GuiStatus.Error
        )


# noinspection PyUnresolvedReferences
main(session)

