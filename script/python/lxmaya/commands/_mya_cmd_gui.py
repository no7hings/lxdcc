# coding:utf-8
from lxmaya_gui.panel.pnl_widgets import _mya_pnl_wgt_checker

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_utility

from lxshotgun_gui.panel.pnl_widgets import _stg_pnl_wgt_validation


# noinspection PyUnusedLocal
def get_validation_window():
    w = _mya_pnl_wdt_checker.SceneCheckerToolPanel()
    return w


def get_validation_main_widget():
    w = get_validation_window()
    return w.get_main_widget()


def get_validation_central_widget():
    w = get_validation_window()
    return w.get_central_widget()


def get_shotgun_validation_window():
    file_path = _mya_dcc_obj_utility.SceneFile.get_current_file_path()
    w = _stg_pnl_wgt_validation.SceneCheckerToolPanel(file_path)
    return w

