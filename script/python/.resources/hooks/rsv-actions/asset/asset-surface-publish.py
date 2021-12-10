# coding:utf-8
from lxbasic import bsc_configure
#
from lxutil import utl_core


def main(session):
    def yes_method():
        import lxgui.fnc.methods as gui_fnc_methods
        #
        gui_fnc_methods.AssetBatcher(
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
    utl_core.DialogWindow.set_create(
        'Publish Asset Surface',
        content=(
            'publish asset surface:\n'
            '"{}",\n'
            'press "Yes" to continue...'
        ).format(asset),
        yes_method=yes_method
    )


# noinspection PyUnresolvedReferences
main(session)
