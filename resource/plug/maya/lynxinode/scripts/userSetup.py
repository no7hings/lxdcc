# encoding=utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


def get_is_ui_mode():
    return not cmds.about(batch=1)


#
def register():
    # AE Template
    from lxCommand.template import aeTemplate
    cmds.evalDeferred(aeTemplate.setupAETemplate)
    print 'setup lynxinode "AETemplate" complete.'
    # Menu
    if get_is_ui_mode():
        from lxCommand.ui import menu
        cmds.evalDeferred(menu.set_menu_setup)
        print 'setup lynxinode "Menu" complete.'


#
if __name__ == '__main__':
    register()
