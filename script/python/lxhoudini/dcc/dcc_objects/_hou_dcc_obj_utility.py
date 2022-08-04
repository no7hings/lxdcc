# coding:utf-8
import os

import re
# noinspection PyUnresolvedReferences
import hou

import types

from lxbasic import bsc_core

from lxutil import utl_core, utl_abstract

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxhoudini import hou_core

from lxhoudini.dcc.dcc_objects import _hou_dcc_obj_os

from lxutil_gui.qt import utl_gui_qt_core


__all__ = [
    'Scene',
    'Selection',
]


class Scene(utl_abstract.AbsDccScene):
    REFERENCE_FILE_CLASS = _hou_dcc_obj_os.OsFile
    def __init__(self):
        super(Scene, self).__init__()
    @property
    def type(self):
        return 'scene'
    @property
    def path(self):
        return hou.hipFile.path()
    @property
    def name(self):
        return hou.hipFile.name()
    @property
    def icon(self):
        return utl_core.FileIcon.get_houdini()
    @classmethod
    def get_houdini_absolutely_path_with_path(cls, path):
        path_ = path
        if '$' in path_:
            # noinspection RegExpRedundantEscape
            re_pattern = re.compile(r'[\$](.*?)[\/]', re.S)
            results = re.findall(re_pattern, path_)
            for environ_key in results:
                variant = '${}'.format(environ_key)
                if environ_key in os.environ:
                    environ_value = os.environ[environ_key]
                    path_ = path_.replace(variant, environ_value)
                else:
                    utl_core.Log.set_warning_trace('Variant "{}" in "{}" is Not Available.'.format(variant, path_))
        return path_

    def get_reference_files(self):
        pass

    def get_frame_range(self):
        return hou.playbar.frameRange()

    def set_frame_range(self, start_frame, end_frame):
        hou.playbar.setFrameRange(start_frame, end_frame)
        hou.playbar.setPlaybackRange(start_frame, end_frame)
        hou.setFrame(start_frame)

    def _test(self):
        self.get_reference_files()
    @classmethod
    def get_current_file_path(cls):
        return hou.hipFile.path()
    @classmethod
    def get_scene_is_dirty(cls):
        return hou.hipFile.hasUnsavedChanges()
    @classmethod
    def set_file_new(cls):
        hou.hipFile.clear(suppress_save_prompt=True)
    @classmethod
    def set_new_file_create_with_dialog_(cls, file_path):
        hou.hipFile.clear(suppress_save_prompt=False)
    @classmethod
    def set_file_new_with_dialog(cls, file_path, post_method=None):
        def pos_method_run_fnc_():
            if isinstance(post_method, (types.FunctionType, types.MethodType)):
                post_method(file_path)

        def yes_fnc_():
            hou.hipFile.save()
            #
            hou.hipFile.clear(suppress_save_prompt=True)
            #
            f = utl_dcc_objects.OsFile(file_path)
            f.set_directory_create()
            #
            pos_method_run_fnc_()
            #
            hou.hipFile.setName(file_path)
        #
        def no_fnc_():
            hou.hipFile.clear(suppress_save_prompt=True)
            #
            f = utl_dcc_objects.OsFile(file_path)
            f.set_directory_create()
            #
            pos_method_run_fnc_()
            #
            hou.hipFile.setName(file_path)
        #
        if cls.get_scene_is_dirty() is True:
            w = utl_core.DialogWindow.set_create(
                label='New',
                content=u'Scene has been modified, Do you want to save change to "{}"'.format(
                    cls.get_current_file_path()
                ),
                window_size=(480, 160),
                #
                yes_method=yes_fnc_,
                no_method=no_fnc_,
                #
                yes_label='Save and new',
                no_label='Don\'t save and new'
            )
        else:
            no_fnc_()
    @classmethod
    def set_file_open_with_dialog(cls, file_path):
        pass
    @classmethod
    def set_file_save_to(cls, file_path):
        hou.hipFile.save(file_path)
        utl_core.Log.set_module_result_trace(
            'scene save',
            u'file="{}"'.format(file_path)
        )
    @classmethod
    def set_file_save_with_dialog(cls):
        if cls.get_scene_is_dirty():
            if cls.get_is_default():
                f = utl_gui_qt_core.QtWidgets.QFileDialog()
                s = f.getSaveFileName(
                    utl_gui_qt_core.QtHoudiniMtd.get_main_window(),
                    caption='Save File',
                    dir=hou.hipFile.path(),
                    filter="Houdini Files (*.hip, *.hipnc)"
                )
                if s:
                    _ = s[0]
                    cls.set_file_save_to(_)
            else:
                pass
    @classmethod
    def get_default_file_path(cls):
        # /home/dongchangbao/untitled.hip
        user_directory_path = bsc_core.SystemMtd.get_user_directory_path()
        return '{}/untitled.hip'.format(user_directory_path)
    @classmethod
    def get_is_default(cls):
        return cls.get_current_file_path() == cls.get_default_file_path()
    @classmethod
    def set_file_open(cls, file_path):
        hou.hipFile.load(file_path)


class Selection(object):
    def __init__(self, *args):
        self._paths = args[0]
    @classmethod
    def _get_current_network_edit_(cls):
        for i in hou.ui.currentPaneTabs():
            if isinstance(i, hou.NetworkEditor):
                return i

    def set_all_select(self):
        [hou.node(i).setSelected(True) for i in self._paths]
        path = self._paths[-1]
        if hou.node(path) is not None:
            network_editor = self._get_current_network_edit_()
            if network_editor is not None:
                hou_node = hou.node(path)
                network_editor.setCurrentNode(hou_node)
                network_editor.homeToSelection()
    @classmethod
    def set_clear(cls):
        hou.clearAllSelected()
    @classmethod
    def get_selected_geos(cls):
        def add_fnc_(obj_):
            _path = obj_.path()
            if _path not in paths:
                paths.append(_path)
                lis.append(obj_)

        def sub_fnc_(obj_):
            _type_string = obj_.type().nameWithCategory()
            if _type_string == 'Object/geo':
                add_fnc_(obj_)
            elif _type_string == 'Object/instance':
                _obj = obj_.parm('instancepath').evalAsNode()
                if _obj is not None:
                    if _obj.type().nameWithCategory() == 'Object/geo':
                        add_fnc_(_obj)
            else:
                geo_objs = hou_core.HoudiniBasic.get_descendants(i, include=['Object/geo', 'Object/instance'])
                [sub_fnc_(_i) for _i in geo_objs]

        _ = hou.selectedNodes()
        paths = []
        lis = []
        for i in _:
            sub_fnc_(i)

        return lis
    @classmethod
    def get_selected_alembics(cls):
        def add_fnc_(obj_):
            _path = obj_.path()
            if _path not in paths:
                paths.append(_path)
                lis.append(obj_)

        paths = []
        lis = []
        geos = cls.get_selected_geos()
        for geo in geos:
            alembics = hou_core.HoudiniBasic.get_descendants(geo, include='Sop/alembic')
            [add_fnc_(i) for i in alembics]
        return lis
