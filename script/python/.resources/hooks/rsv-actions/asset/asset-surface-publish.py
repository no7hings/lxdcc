# coding:utf-8
from lxbasic import bsc_configure
#
from lxutil import utl_core


def main(session):
    def yes_method():
        import lxgui_fnc.methods as gui_fnc_methods
        #
        gui_fnc_methods.AssetBatch(
            project=project,
            assets=[
                asset,
            ],
            option=dict(
                surface_publish=True
            )
        ).set_run()
    #
    rsv_entity = session.rsv_obj
    #
    project = rsv_entity.get('project')
    asset = rsv_entity.get('asset')
    #
    dialog = utl_core.DialogWindow.set_create(
        'Asset-surface Publish',
        content='Surface Publish, press "Yes" to Continue...',
        yes_method=yes_method,
        status=bsc_configure.GuiStatus.Warning
    )


main(session)
