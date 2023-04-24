# coding:utf-8
import threading

from lxbasic import bsc_core

from lxkatana import ktn_core


class ScpWorkspaceCreate(object):
    """
# coding:utf-8
import lxkatana

lxkatana.set_reload()

from lxkatana import ktn_core

import lxkatana.scripts as ktn_scripts

ktn_scripts.ScpWorkspaceCreate.new()
    """
    KEY = 'workspace'
    def __init__(self, obj_opt):
        self._obj_opt = obj_opt
    @classmethod
    def load_geometry_auto(cls):
        g_ns = ktn_core.NGObjsMtd.find_nodes_by_port_filters(
            type_name='Group', filters=[('type', 'in', {'AssetGeometry_Wsp'})]
        )
        if g_ns:
            g_n = g_ns[0]
            g_n_opt = ktn_core.NGObjOpt(g_n)
            g_n_opt.set(
                'parameters.usd_variant.mode', 'override'
            )
            g_n_opt.execute_port(
                'parameters.usd.tools', index=1
            )
    @classmethod
    def load_look_auto(cls):
        m_gs = ktn_core.NGObjsMtd.find_nodes_by_port_filters(
            type_name='GroupMerge',
            filters=[('user.type', 'in', {'MaterialGroup_Wsp', 'MaterialGroup_Wsp_Usr'})]
        )
        if m_gs:
            m_g = m_gs[0]
            ktn_core.NGObjOpt(m_g).execute_port('user.parameters.ass.tools', index=0)
            ktn_core.NGObjOpt(m_g).execute_port('user.parameters.ass.tools', index=1)
        #
        ma_gs = ktn_core.NGObjsMtd.find_nodes_by_port_filters(
            type_name='GroupStack',
            filters=[('user.type', 'in', {'MaterialAssignGroup_Wsp', 'MaterialAssignGroup_Wsp_Usr'})]
        )
        if ma_gs:
            ms_g = ma_gs[0]
            ktn_core.NGObjOpt(ms_g).execute_port('user.parameters.ass.tools', index=0)
            ktn_core.NGObjOpt(ms_g).execute_port('user.parameters.ass.tools', index=1)
        #
        gpa_gs = ktn_core.NGObjsMtd.find_nodes_by_port_filters(
            type_name='GroupStack',
            filters=[('user.type', 'in', {'GeometryPropertiesAssignGroup_Wsp', 'GeometryPropertiesAssignGroup_Wsp_Usr'})]
        )
        if gpa_gs:
            gpa_g = gpa_gs[0]
            ktn_core.NGObjOpt(gpa_g).execute_port('user.parameters.ass.tools', index=0)
            ktn_core.NGObjOpt(gpa_g).execute_port('user.parameters.ass.tools', index=1)
    @classmethod
    def new(cls):
        def post_fnc_():
            bsc_core.LogMtd.ENABLE = False
            s = ScpWorkspaceCreate(obj_opt)
            s.load_geometry_auto()
            s.load_look_auto()
            bsc_core.LogMtd.ENABLE = True
        #
        ktn_obj, i_create = ktn_core.NGObjOpt._get_create_args_(
            '/rootNode/workspace', 'Workspace_Wsp'
        )
        if i_create is True:
            obj_opt = ktn_core.NGObjOpt(ktn_obj)
            obj_opt.execute_port(
                'workspace.tools', index=0
            )
            #
            # timer = threading.Timer(.25, post_fnc_)
            # timer.start()
            post_fnc_()