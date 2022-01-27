# coding:utf-8
from .. import utl_core


def get_validation_window():
    if utl_core._app__get_is_maya_():
        from lxmaya_gui.panel.pnl_widgets import _mya_pnl_wdt_checker
        return _mya_pnl_wdt_checker.SceneCheckerToolPanel()
    elif utl_core._app__get_is_houdini_():
        from lxhoudini_gui.panel.hou_pnl_widgets import _hou_pnl_wdt_checker
        return _hou_pnl_wdt_checker.SceneCheckerToolPanel()


def get_validation_main_widget():
    w = get_validation_window()
    return w.get_main_widget()


def get_validation_central_widget():
    w = get_validation_window()
    return w.get_central_widget()


def get_shotgun_validation_window():
    from lxshotgun_gui.panel.pnl_widgets import _stg_pnl_wgt_validation
    if utl_core._app__get_is_maya_():
        from lxmaya.dcc.dcc_objects import _mya_dcc_obj_utility
        work_source_file_path = _mya_dcc_obj_utility.SceneFile.get_current_file_path()
        return _stg_pnl_wgt_validation.SceneCheckerToolPanel(work_source_file_path)
    elif utl_core._app__get_is_houdini_():
        from lxhoudini.dcc.dcc_objects import _hou_dcc_obj_utility
        work_source_file_path = _hou_dcc_obj_utility.Scene().path
        return _stg_pnl_wgt_validation.SceneCheckerToolPanel(work_source_file_path)

