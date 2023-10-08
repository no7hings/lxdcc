# coding=utf-8
import os
#
import sys
# noinspection PyUnresolvedReferences
import shiboken2
# noinspection PyUnresolvedReferences
import maya.OpenMayaUI as openMayaUI
# noinspection PyUnresolvedReferences
from PySide2 import QtGui, QtCore, QtWidgets
#
DEFAULT_MENU_NAME = '&Lynxi Tool(s)'


#
def isMayaApp():
    data = os.environ.get(u'MAYA_APP_DIR')
    if data:
        return True
    return False


#
def get_qt_main_window():
    if isMayaApp():
        mainWindowPtr = openMayaUI.MQtUtil.mainWindow()
        if mainWindowPtr is not None:
            mainWindow = shiboken2.wrapInstance(long(mainWindowPtr), QtWidgets.QMainWindow)
            return mainWindow


#
def get_qt_menu_bar():
    w = get_qt_main_window()
    if w:
        children = w.children()
        for child in children:
            if type(child) == QtWidgets.QMenuBar:
                return child


#
def get_qt_menu():
    m_b = get_qt_menu_bar()
    if m_b:
        children = m_b.children()
        for child in children:
            if type(child) == QtWidgets.QMenu:
                menuTitle = child.title()
                if menuTitle.startswith(DEFAULT_MENU_NAME):
                    return child


#
def set_menu_setup():
    def set_mesh_create_by_curve_fnc_():
        import lxCommand.cmds as lxcmds
        lxcmds.set_mesh_create_by_curve_cmd()
    #
    def set_mesh_create_by_bonus_curve_fnc_():
        import lxCommand.cmds as lxcmds
        lxcmds.set_mesh_create_by_bonus_curve()
    #
    def set_surface_create_by_mesh_fnc_():
        import lxCommand.cmds as lxcmds
        lxcmds.set_surface_create_by_mesh_cmd()
    #
    def set_curve_create_by_xgen_guide_fnc_():
        import lxCommand.cmds as lxcmds
        lxcmds.set_curve_create_by_xgen_guide_cmd()
    #
    def set_mesh_create_by_xgen_guide_fnc_01_():
        import lxCommand.cmds as lxcmds
        lxcmds.set_mesh_create_by_xgen_guide_cmd_01()
    #
    def set_mesh_create_by_mesh_fnc_():
        import lxCommand.cmds as lxcmds
        lxcmds.set_mesh_create_by_mesh_cmd()
    #
    def set_mesh_create_by_xgen_guide_fnc_02_():
        import lxCommand.cmds as lxcmds
        lxcmds.set_mesh_create_by_xgen_guide_cmd_02()
    #
    def create_cylinder_mesh_by_curve_fnc_():
        from lxCommand import curve_to_mesh_extra_cmd
        curve_to_mesh_extra_cmd.C2meCommand().create_node_by_curves()

    def create_cylinder_mesh_by_guide_fnc_():
        from lxCommand import curve_to_mesh_extra_cmd
        curve_to_mesh_extra_cmd.C2meCommand().create_node_by_guides()
    #
    def set_mesh_create_by_surface_fnc_():
        import lxCommand.cmds as lxcmds
        lxcmds.set_mesh_create_by_surface_cmd()
    #
    def set_mesh_morph_by_uv_map_fnc_1_():
        import lxCommand.cmds as lxcmds
        lxcmds.set_mesh_morph_by_uv_map_cmd_01()

    def set_mesh_morph_by_uv_map_fnc_2_():
        import lxCommand.cmds as lxcmds
        lxcmds.set_mesh_morph_by_uv_map_cmd_02()

    def show_control_window_fnc_():
        from lxCommand import curve_to_mesh_extra_cmd
        curve_to_mesh_extra_cmd.C2meCommand().setup()
        curve_to_mesh_extra_cmd.C2meCommand().show_control_window()
    #
    raw = [
        ('curve', ),
        ('Create Curve(s) by Xgen-guide(s)', set_curve_create_by_xgen_guide_fnc_),
        ('surface', ),
        ('Create Surface(s) by Mesh(s)', set_surface_create_by_mesh_fnc_),
        ('plane mesh', ),
        ('Create Plane-mesh(s) by Curve(s)', set_mesh_create_by_curve_fnc_),
        ('Create Plane-mesh(s) by Xgen-guide(s) 01', set_mesh_create_by_xgen_guide_fnc_01_),
        ('Create Plane-mesh(s) by Surface(s)', set_mesh_create_by_surface_fnc_),
        ('Create Plane-mesh(s) by Mesh(s)', set_mesh_create_by_mesh_fnc_),
        (),
        ('Create mesh(s) by Xgen-guide(s) 02', set_mesh_create_by_xgen_guide_fnc_02_),
        ('cylinder mesh', ),
        ('Create Cylinder-mesh(s) by Curve(s)', create_cylinder_mesh_by_curve_fnc_),
        ('Create Cylinder-mesh(s) by Xgen-guide(s)', create_cylinder_mesh_by_guide_fnc_),
        ('command',),
        ('Morph Mesh(s) by Uv-map (keep-topology)', set_mesh_morph_by_uv_map_fnc_1_),
        ('Morph Mesh(s) by Uv-map', set_mesh_morph_by_uv_map_fnc_2_),
        ('window', ),
        ('Show Control Window', show_control_window_fnc_),
        ('extend', ),
        ('About', None)
    ]
    #
    m_b = get_qt_menu_bar()
    if m_b:
        d_m = get_qt_menu()
        if d_m is not None:
            d_m.deleteLater()
        #
        d_m = m_b.addMenu(DEFAULT_MENU_NAME)
        d_m.setTearOffEnabled(True)
        d_m.setWindowTitle(DEFAULT_MENU_NAME[1:])
        d_m.setObjectName(DEFAULT_MENU_NAME)
        #
        for i in raw:
            if i:
                if len(i) == 1:
                    s = d_m.addSeparator()
                    s.setText(i[0])
                else:
                    label, command = i
                    #
                    action = d_m.addAction(label)
                    if command is not None:
                        action.triggered.connect(command)
            else:
                d_m.addSeparator()
