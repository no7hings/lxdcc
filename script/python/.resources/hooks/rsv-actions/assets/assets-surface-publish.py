# coding:utf-8


def main(session):
    def yes_method():
        import lxgui.fnc.methods as gui_fnc_methods
        #
        gui_fnc_methods.AssetBatcher(
            project=project,
            assets=assets,
            option=dict(
                surface_publish=True
            )
        ).set_run()

    from lxutil import utl_core

    from lxbasic import bsc_configure

    rsv_asset = session.rsv_obj
    #
    project = rsv_asset.get('project')
    #
    tree_item = rsv_asset.get_obj_gui()
    tree_view = tree_item.get_view()

    all_items = tree_view.get_all_items()

    assets = []
    for i_item in all_items:
        i_rsv_obj = i_item.get_gui_dcc_obj(namespace='resolver')
        if i_rsv_obj:
            if i_rsv_obj.type_name == 'asset':
                if i_item.get_is_checked() and i_item.get_is_hidden(ancestors=True) is False:
                    assets.append(i_rsv_obj.name)
    #
    if assets:
        utl_core.DialogWindow.set_create(
            'Publish Asset(s) Surface',
            content=(
                'publish asset(s) surface:\n'
                '{}\n'
                'press "Yes" to continue...'
            ).format(
                ',\n'.join(map(lambda x: '"{}"'.format(x), assets))
            ),
            yes_method=yes_method
        )
    else:
        utl_core.DialogWindow.set_create(
            'Publish Asset(s) Surface',
            content='no asset(s) has checked',
            status=bsc_configure.GuiStatus.Error
        )


# noinspection PyUnresolvedReferences
main(session)
