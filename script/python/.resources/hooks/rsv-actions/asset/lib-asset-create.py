# coding:utf-8
from lxbasic import bsc_configure
#
from lxutil import utl_core


def main(session):
    def yes_method():
        import lxgui_fnc.methods as gui_fnc_methods
        if session.get_is_system_matched('linux-python'):
            gui_fnc_methods.LibAssetCreateBatch(
                project=project,
                assets=[
                    asset
                ],
                option=dict(
                    create_task=True,
                    # create_shotgun=True,
                    copy_src_file=True
                )
            ).set_run()
        elif session.get_is_system_matched('*-maya'):
            gui_fnc_methods.LibAssetCreateBatch(
                project=project,
                assets=[
                    asset
                ],
                option=dict(
                    create_task=True,
                    # create_shotgun=True,
                    copy_src_file=True
                )
            ).set_run()
    #
    rsv_entity = session.rsv_obj
    #
    project = rsv_entity.get('project')
    asset = rsv_entity.get('asset')
    #
    if project not in ['lib']:
        #
        dialog = utl_core.DialogWindow.set_create(
            'LIB Asset Create',
            content='Create this Asset in "LIB", press "Yes" to Continue...',
            yes_method=yes_method,
            status=bsc_configure.GuiStatus.Warning
        )
    else:
        dialog = utl_core.DialogWindow.set_create(
            'LIB Asset Create',
            content='Project "LIB" is not Support...',
            status=bsc_configure.GuiStatus.Error
        )

main(session)
