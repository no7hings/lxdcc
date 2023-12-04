# coding:utf-8
import lxlog.core as log_core

import lxbasic.core as bsc_core

import lxcontent.core as ctt_core

from lxutil.dcc import utl_dcc_opt_abs

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxusd.dcc.dcc_operators import _usd_dcc_opt_geometry


class SceneOpt(utl_dcc_opt_abs.AbsMeshComparerDef):
    def __init__(self, stage, namespace=None):
        self._stage = stage
        if namespace is not None:
            self._namespace = namespace
        else:
            self._namespace = 'usd'

    @property
    def stage(self):
        return self._stage

    def get_mesh_comparer_data(self, file_path):
        if file_path:
            yml_file_path = bsc_core.StgTmpYamlMtd.get_file_path(
                file_path, 'mesh-comparer-{}'.format(self._namespace)
            )
            return self._get_mesh_data_content_(self._stage, file_path, yml_file_path)
        return ctt_core.Content(value={})

    @classmethod
    def _get_mesh_data_content_(cls, stage, file_path, yml_file_path):
        yml_file = utl_dcc_objects.OsYamlFile(yml_file_path)
        if yml_file.get_is_exists() is True:
            if yml_file.set_read():
                log_core.Log.trace_method_result(
                    'geometry-comparer data read',
                    'cache="{}", source="{}"'.format(yml_file_path, file_path)
                )
                return ctt_core.Content(value=yml_file_path)
        #
        content_0 = ctt_core.Content(value={})
        c = len([i for i in stage.TraverseAll()])
        if c:
            with bsc_core.LogProcessContext.create(maximum=c, label='gain geometry-comparer data') as g_p:
                for i_prim in stage.TraverseAll():
                    g_p.do_update()
                    i_obj_type_name = i_prim.GetTypeName()
                    if i_obj_type_name == 'Mesh':
                        i_mesh_obj_opt = _usd_dcc_opt_geometry.MeshOpt(i_prim)
                        i_dcc_obj_path = i_prim.GetPath().pathString
                        #
                        i_dcc_obj_name = i_prim.GetName()
                        i_face_vertices_uuid = i_mesh_obj_opt.get_face_vertices_as_uuid()
                        i_points_uuid = i_mesh_obj_opt.get_points_as_uuid()
                        cls._set_mesh_comparer_data_build_(
                            content_0,
                            i_dcc_obj_path,
                            i_dcc_obj_name, i_face_vertices_uuid, i_points_uuid
                        )
        #
        if content_0.value:
            log_core.Log.trace_method_result(
                'geometry comparer-data write',
                'cache="{}", source="{}"'.format(yml_file_path, file_path)
            )
            yml_file.set_write(content_0.value)
        else:
            log_core.Log.trace_method_warning(
                'geometry comparer-data resolver',
                'file="{}" geometry is not found'.format(file_path)
            )

        #
        return content_0
