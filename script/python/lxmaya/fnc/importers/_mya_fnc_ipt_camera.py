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


class CameraAbcImporter(utl_fnc_obj_abs.AbsDccExporter):
    OPTION = dict(
        namespace=':'
    )
    PLUG_NAME = 'AbcImport'
    OBJ_PATHSEP = ma_configure.Util.OBJ_PATHSEP
    def __init__(self, file_path, root=None, option=None):
        super(CameraAbcImporter, self).__init__(file_path, root, option)

    def set_run(self):
        cmds.loadPlugin(self.PLUG_NAME, quiet=1)
        #
        namespace_temporary = 'alembic_import_{}'.format(utl_core.System.get_time_tag())
        root_mya_path = bsc_core.DccPathDagOpt(self._root).set_translate_to(
            self.OBJ_PATHSEP
        ).get_value()
        group = mya_dcc_objects.Group(root_mya_path)
        group.set_dag_components_create()
        #
        cmds.file(
            self._file_path,
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
        for obj in objs:
            utl_core.Log.set_module_result_trace(
                'camera-alembic-import',
                u'obj="{}"'.format(obj.path)
            )
            if obj.type == 'transform':
                path_src = obj.path
                if len(path_src.split('|')) == 2:
                    target_obj_path = '{}|{}'.format(
                        root_mya_path,  bsc_core.DccPathDagMtd.get_dag_name_with_namespace_clear(obj.name)
                    )
                    obj_tgt = mya_dcc_objects.Node(target_obj_path)
                    if obj_tgt.get_is_exists() is True:
                        obj_tgt.set_delete()
                    #
                    obj.set_parent_path(root_mya_path)
            #
            obj._set_path_update_()
            dcc_dag_path = bsc_core.DccPathDagOpt(obj.path).set_namespace_clear_to()
            self._results.append(dcc_dag_path.path)
        #
        namespace_obj.set_delete()
        return self._results
