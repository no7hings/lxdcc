# coding:utf-8
from .wrap import *

import lxlog.core as log_core

from ..core import _ktn_cor_node


class _AbsHotkey(object):
    KEY = 'hot key'


class HotKeyForNodeGraphLayout(_AbsHotkey):
    """
# coding:utf-8
import lxkatana
lxkatana.set_reload()

import lxkatana.core as ktn_core

ktn_core.HotKeyForNodeGraphLayout().register()
    """
    NAME = 'Node Graph Layout'
    ID = 'F4331532-D52B-11ED-8C7C-2CFDA1C062BB'
    HOT_KEY = 'Alt+L'

    @classmethod
    def release_fnc_(cls, ktn_gui):
        ss = NodegraphAPI.GetAllSelectedNodes()
        if ss:
            group = ktn_gui.getEnteredGroupNode()
            if group.getType() in {'NetworkMaterialCreate', 'ShadingGroup'}:
                ss_ = [i_s for i_s in ss if i_s.getParent() == group]
                _ktn_cor_node.NGGuiLayout(
                    ss_
                ).layout_shader_graph(
                    size=(320, 320)
                )

    def __init__(self):
        self._ktn_gui = App.Tabs.FindTopTab('Node Graph')

    def press_fnc(self, *args, **kwargs):
        pass

    def release_fnc(self, *args, **kwargs):
        ktn_gui = args[0]
        self.release_fnc_(ktn_gui)

    def register(self):
        log_core.Log.trace_method_result(
            self.KEY,
            'register: name is "{}", hot key is "{}"'.format(self.NAME, self.HOT_KEY)
        )
        self._ktn_gui.registerKeyboardShortcut(
            self.ID, self.NAME, self.HOT_KEY, self.press_fnc, self.release_fnc
        )


class HotKeyForNodeGraphPaste(_AbsHotkey):
    NAME = 'Node Graph Paste'
    ID = 'F4331532-D52B-11ED-8C7C-2CFDA1C062BC'
    HOT_KEY = 'Alt+V'

    @classmethod
    def release_fnc_(cls, ktn_gui):
        node = ktn_gui.getEnteredGroupNode()
        if node.getType() in {'NetworkMaterialCreate', 'ShadingGroup'}:
            import lxkatana.scripts as ktn_scripts

            ktn_scripts.ScpTextureBuilder(
                node
            ).do_paste()

    def __init__(self):
        self._ktn_gui = App.Tabs.FindTopTab('Node Graph')

    def press_fnc(self, *args, **kwargs):
        pass

    def release_fnc(self, *args, **kwargs):
        ktn_gui = args[0]
        self.release_fnc_(ktn_gui)

    def register(self):
        log_core.Log.trace_method_result(
            self.KEY,
            'register: name is "{}", hot key is "{}"'.format(self.NAME, self.HOT_KEY)
        )
        self._ktn_gui.registerKeyboardShortcut(
            self.ID, self.NAME, self.HOT_KEY, self.press_fnc, self.release_fnc
        )

