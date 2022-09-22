# coding:utf-8
# noinspection PyUnresolvedReferences
from pxr import Usd, Sdf, Vt, UsdGeom, Gf

from lxbasic import bsc_core

from lxutil import utl_core

from lxutil.dcc import utl_dcc_opt_abs

import lxbasic.objects as bsc_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxusd.dcc.dcc_operators import _usd_dcc_opt_geometry


class SceneOpt(utl_dcc_opt_abs.AbsMeshComparerDef):
    def __init__(self, *args, **kwargs):
        self._stage = args[0]
    @property
    def stage(self):
        return self._stage

    def get_mesh_comparer_data(self, file_path):
        if file_path:
            yml_file_path = bsc_core.TemporaryYamlMtd.get_file_path(file_path, 'mesh-comparer')
            return self._get_mesh_data_content_(self._stage, file_path, yml_file_path)
        else:
            return bsc_objects.Content(value={})
    @classmethod
    def _get_mesh_data_content_(cls, stage, file_path, yml_file_path):
        yml_file = utl_dcc_objects.OsYamlFile(yml_file_path)
        if yml_file.get_is_exists() is True:
            if yml_file.set_read():
                utl_core.Log.set_module_result_trace(
                    'comparer-data read',
                    'cache="{}"'.format(yml_file_path)
                )
                return bsc_objects.Content(value=yml_file_path)
        #
        content_0 = bsc_objects.Content(value={})
        c = len([i for i in stage.TraverseAll()])
        if c:
            with utl_core.gui_progress(maximum=c) as g_p:
                for i_prim in stage.TraverseAll():
                    g_p.set_update()
                    i_obj_type_name = i_prim.GetTypeName()
                    if i_obj_type_name == 'Mesh':
                        i_mesh_obj_opt = _usd_dcc_opt_geometry.MeshOpt(i_prim)
                        i_dcc_obj_path = i_prim.GetPath().pathString
                        #
                        i_dcc_obj_name = i_prim.GetName()
                        i_face_vertices_uuid = i_mesh_obj_opt.get_face_vertices_as_uuid()
                        points_uuid = i_mesh_obj_opt.get_points_as_uuid()
                        cls._set_mesh_comparer_data_build_(
                            content_0,
                            i_dcc_obj_path,
                            i_dcc_obj_name, i_face_vertices_uuid, points_uuid
                        )
        #
        if content_0.value:
            utl_core.Log.set_module_result_trace(
                'comparer-data write',
                'cache="{}"'.format(yml_file_path)
            )
            yml_file.set_write(content_0.value)
        else:
            utl_core.Log.set_module_warning_trace(
                'comparer-data resolver',
                'file="{}" geometry is not found'.format(file_path)
            )

        #
        return content_0
