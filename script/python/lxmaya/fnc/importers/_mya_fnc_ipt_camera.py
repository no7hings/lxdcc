# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

import copy

import os

from lxmaya import ma_configure

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_operators as mya_dcc_operators

from lxmaya.fnc import mya_fnc_obj_core

import lxusd.dcc.dcc_operators as usd_dcc_operators

from lxusd import usd_configure, usd_core

from lxutil import utl_core

from lxutil.fnc import utl_fnc_obj_abs

from lxbasic import bsc_core


class CameraAbcImporter(
    utl_fnc_obj_abs.AbsFncOptionMethod
):
    OPTION = dict(
        file='',
        location='',
        namespace=':',
        camera_resolution=(2048, 2048)
    )
    PLUG_NAME = 'AbcImport'
    OBJ_PATHSEP = ma_configure.Util.OBJ_PATHSEP
    def __init__(self, option=None):
        super(CameraAbcImporter, self).__init__(option)

    def set_run(self):
        cmds.loadPlugin(self.PLUG_NAME, quiet=1)
        #
        file_path = self.get('file')
        location = self.get('location')
        #
        namespace_temporary = 'alembic_import_{}'.format(utl_core.System.get_time_tag())
        mya_location = bsc_core.DccPathDagOpt(location).set_translate_to(
            self.OBJ_PATHSEP
        ).get_value()
        group = mya_dcc_objects.Group(mya_location)
        group.set_dag_components_create()
        #
        cmds.file(
            file_path,
            i=1,
            options='v=0;',
            type='Alembic',
            ra=1,
            mergeNamespacesOnClash=1,
            namespace=namespace_temporary,
            preserveReferences=1
        )
        #
        namespace_obj = mya_dcc_objects.Namespace(namespace_temporary)
        self._results = []
        objs = namespace_obj.get_objs()
        for i_obj in objs:
            utl_core.Log.set_module_result_trace(
                'alembic import',
                u'obj="{}"'.format(i_obj.path)
            )
            if i_obj.type_name == 'transform':
                path_src = i_obj.path
                if len(path_src.split('|')) == 2:
                    i_children = i_obj.get_children()
                    for j_child in i_children:
                        if j_child.type_name == 'camera':
                            j_camera = mya_dcc_objects.Camera(j_child.path)
                            j_camera.set_display_()
                    #
                    target_obj_path = '{}|{}'.format(
                        mya_location,  bsc_core.DccPathDagMtd.get_dag_name_with_namespace_clear(i_obj.name)
                    )
                    obj_tgt = mya_dcc_objects.Node(target_obj_path)
                    if obj_tgt.get_is_exists() is True:
                        obj_tgt.set_delete()
                    #
                    i_obj.set_parent_path(mya_location)
            #
            i_obj._set_path_update_()
            dcc_dag_path = bsc_core.DccPathDagOpt(i_obj.path).set_namespace_clear_to()
            self._results.append(dcc_dag_path.path)
        #
        namespace_obj.set_delete()
        return self._results
