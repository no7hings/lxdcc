# coding:utf-8


def main(session):
    def get_asset_tgt(asset_src_):
        return gui_fnc_methods.LibAssetPusher._get_lib_asset_(project_src, asset_src_)

    def yes_method_0():
        def run_method_1(assets_tgt_):
            import lxdeadline.objects as ddl_objects
            #
            import lxdeadline.methods as ddl_methods
            #
            method_query = ddl_objects.DdlMethodQuery(
                key='lib-assets-push', extend_option_kwargs=dict(configure=_project_tgt)
            )
            #
            method = ddl_methods.DdlMethodRunner(
                method_option=method_query.get_method_option(),
                script_option=method_query.get_script_option(
                    project=project_src,
                    assets=assets_tgt_,
                    #
                    with_system_create=True,
                    with_system_permission_create=False,
                    #
                    with_shotgun_create=True,
                    with_file_copy=True,
                    with_surface_publish=True,
                    #
                    batch_key='assets',
                    #
                    user=bsc_core.SystemMtd.get_user_name(), time_tag=bsc_core.SystemMtd.get_time_tag(),
                    td_enable=True
                )
            )
            #
            method.set_run_with_deadline()

        def yes_method_1():
            _assets = assets_src
            # print _assets
            run_method_1(_assets)

        def no_method_1():
            _assets = [_i for _i in assets_src if _i not in _exists_assets_src]
            # print _assets
            run_method_1(_assets)

        _project_tgt = 'lib'

        _exists_assets_src = []
        for _i_asset_src in assets_src:
            _i_asset_tgt = get_asset_tgt(_i_asset_src)
            _i_rsv_asset_tgt = resolver.get_rsv_entity(project=_project_tgt, asset=_i_asset_tgt)
            if _i_rsv_asset_tgt is not None:
                _exists_assets_src.append(_i_asset_src)
        #
        if _exists_assets_src:
            _w = utl_core.DialogWindow.set_create(
                window_title,
                content=(
                    '{} asset(s) is already exists:\n'
                    '{}\n'
                    'do you want to override exists...'
                ).format(
                    len(_exists_assets_src),
                    ',\n'.join(map(lambda x: 'from "{}" to "{}"'.format(x, get_asset_tgt(x)), _exists_assets_src))
                ),
                window_size=window_size,
                yes_label='Override',
                no_label='Don\'t Override',
                yes_method=yes_method_1,
                no_method=no_method_1,
                status=bsc_configure.GuiStatus.Warning,
                use_exec=False
                # show=False
            )
            _w.set_window_show()
        else:
            yes_method_1()
    #
    from lxbasic import bsc_core

    from lxutil import utl_core

    from lxbasic import bsc_configure

    import lxresolver.commands as rsv_commands

    import lxgui.fnc.methods as gui_fnc_methods

    resolver = rsv_commands.get_resolver()

    rsv_asset = session.rsv_obj
    #
    project_src = rsv_asset.get('project')

    window_title = 'Push Asset(s) to "LIB"'
    window_size = 480, 480
    #
    if project_src not in ['lib']:
        tree_item = rsv_asset.get_obj_gui()
        tree_view = tree_item.get_view()

        all_items = tree_view.get_all_items()

        assets_src = []
        for i_item in all_items:
            i_rsv_obj = i_item.get_gui_dcc_obj(namespace='resolver')
            if i_rsv_obj:
                if i_rsv_obj.type_name == 'asset':
                    if i_item.get_is_checked() and i_item.get_is_hidden(ancestors=True) is False:
                        assets_src.append(i_rsv_obj.name)
        #
        if assets_src:
            utl_core.DialogWindow.set_create(
                window_title,
                content=(
                    '{} asset(s) is checked:\n'
                    '{}\n'
                    'press "Yes" to continue...'
                ).format(
                    len(assets_src),
                    ',\n'.join(map(lambda x: 'from "{}" to "{}"'.format(x, get_asset_tgt(x)), assets_src))
                ),
                yes_method=yes_method_0,
                window_size=window_size,
                status=bsc_configure.GuiStatus.Warning,
                use_exec=False
            )
        else:
            utl_core.DialogWindow.set_create(
                'Push Asset(s) to "LIB"',
                content='no asset(s) has checked',
                status=bsc_configure.GuiStatus.Error
            )
    else:
        utl_core.DialogWindow.set_create(
            'Push Asset(s) to "LIB"',
            content='project "LIB" is not support...',
            status=bsc_configure.GuiStatus.Error
        )


# noinspection PyUnresolvedReferences
main(session)
