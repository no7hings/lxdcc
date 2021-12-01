# coding:utf-8
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.cmds as cmds

from lxobj import core_objects

from lxmaya import ma_configure

import lxmaya.dcc.dcc_objects as mya_dcc_objects

from lxutil import utl_core


class AttributeTranslator(object):
    def __init__(self, root_src, root_tgt):
        root_src_dag_path = core_objects.ObjDagPath(root_src)
        self._mya_root_src_dag_path = root_src_dag_path.set_translate_to(ma_configure.Util.OBJ_PATHSEP)
        self._mya_root_src_path = self._mya_root_src_dag_path.path

        root_tgt_dag_path = core_objects.ObjDagPath(root_tgt)
        self._mya_root_tgt_dag_path = root_tgt_dag_path.set_translate_to(ma_configure.Util.OBJ_PATHSEP)
        self._mya_root_tgt_path = self._mya_root_tgt_dag_path.path

    def set_uv_translate(self, clear_history=False):
        lis = []
        src_root = mya_dcc_objects.Group(self._mya_root_src_dag_path.path)
        src_mesh_obj_paths = src_root.get_all_shape_paths(include_obj_type=['mesh'])
        for src_mesh_obj_path in src_mesh_obj_paths:
            rlt_path = src_mesh_obj_path[len(self._mya_root_src_path):]
            tgt_mesh_obj_path = self._mya_root_tgt_path + rlt_path
            if mya_dcc_objects.Node(tgt_mesh_obj_path).get_is_exists() is True:
                lis.append((src_mesh_obj_path, tgt_mesh_obj_path))
        #
        for src_obj_path, tgt_obj_path in lis:
            _ = cmds.transferAttributes(
                src_obj_path, tgt_obj_path, transferUVs=2
            )
            if clear_history is True:
                cmds.delete(tgt_obj_path, constructionHistory=1)
            #
            utl_core.Log.set_module_result_trace(
                'mesh-uv-translate',
                u'obj="{}"'.format(tgt_obj_path)
            )

    def set_look_translate(self):
        pass
