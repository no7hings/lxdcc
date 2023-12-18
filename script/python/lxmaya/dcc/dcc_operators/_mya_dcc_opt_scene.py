# coding:utf-8
import lxbasic.core as bsc_core

import lxcontent.core as ctt_core

from lxutil.dcc import utl_dcc_opt_abs

from lxmaya import ma_configure


class SceneOpt(utl_dcc_opt_abs.AbsMeshComparerDef):
    def __init__(self, *args, **kwargs):
        """
        stage is universe
        :param args:
        :param kwargs:
        """
        self._stage = args[0]

    @property
    def stage(self):
        return self._stage

    def get_mesh_data_content(self, directory_path, file_path):
        from lxmaya.dcc.dcc_objects import _mya_dcc_obj_geometry
        #
        from lxmaya.dcc.dcc_operators import _mya_dcc_opt_geometry

        #
        if file_path:
            yml_file_path = bsc_core.StgTmpYamlMtd.get_file_path(file_path, 'mesh-comparer')
            yml_file = bsc_core.StgFileOpt(yml_file_path)
            if yml_file.get_is_exists() is False:
                content_0 = ctt_core.Content(value={})
                content_0.set('file', file_path)
                dcc_objs = self._stage.get_objs()
                if dcc_objs:
                    bsc_core.Log.trace_method_result(
                        'comparer-data build',
                        'file="{}"'.format(file_path)
                    )
                    with bsc_core.LogProcessContext.create(maximum=len(dcc_objs), label='build comparer-data') as g_p:
                        for dcc_obj in dcc_objs:
                            g_p.do_update()
                            obj_type_name = dcc_obj.type.name
                            if obj_type_name == 'mesh':
                                dcc_path = dcc_obj.path
                                dcc_obj_name = dcc_obj.name
                                #
                                dcc_path_dag_opt = bsc_core.PthNodeOpt(dcc_path)
                                mya_path_dag_opt = dcc_path_dag_opt.translate_to(ma_configure.Util.OBJ_PATHSEP)
                                mya_obj_path = mya_path_dag_opt.path
                                mya_mesh = _mya_dcc_obj_geometry.Mesh(mya_obj_path)
                                mya_mesh_opt = _mya_dcc_opt_geometry.MeshOpt(mya_mesh)
                                #
                                content_0.set('name.{}'.format(dcc_obj_name), dcc_path)
                                content_0.set('name.{}'.format(dcc_path), dcc_obj_name)
                                #
                                face_vertices_uuid = mya_mesh_opt.get_face_vertices_as_uuid()
                                content_0.set('face_vertices_uuids.{}'.format(face_vertices_uuid), dcc_path)
                                content_0.set('face_vertices_uuids.{}'.format(dcc_path), face_vertices_uuid)
                                #
                                points_uuid = mya_mesh_opt.get_points_as_uuid()
                                content_0.set('points_uuids.{}'.format(points_uuid), dcc_path)
                                content_0.set('points_uuids.{}'.format(dcc_path), points_uuid)
                #
                return content_0
            else:
                return ctt_core.Content(value=yml_file_path)
        else:
            return ctt_core.Content(value={})

    #
    def get_mesh_comparer_data(self, file_path):
        if file_path:
            yml_file_path = bsc_core.StgTmpYamlMtd.get_file_path(file_path, 'mesh-comparer')
            return self._get_mesh_data_content_(self._stage, file_path, yml_file_path)
        else:
            return ctt_core.Content(value={})

    @classmethod
    def _get_mesh_data_content_(cls, stage, file_path, yml_file_path):
        from lxmaya.dcc.dcc_objects import _mya_dcc_obj_geometry
        #
        from lxmaya.dcc.dcc_operators import _mya_dcc_opt_geometry

        #
        yml_file = bsc_core.StgFileOpt(yml_file_path)
        if yml_file.get_is_exists() is True:
            return ctt_core.Content(value=yml_file_path)
        #
        content_0 = ctt_core.Content(value={})
        dcc_objs = stage.get_objs()
        if dcc_objs:
            with bsc_core.LogProcessContext.create(maximum=len(dcc_objs), label='gain build comparer-data') as g_p:
                for dcc_obj in dcc_objs:
                    g_p.do_update()
                    obj_type_name = dcc_obj.type.name
                    if obj_type_name == 'mesh':
                        dcc_path = dcc_obj.path
                        #
                        dcc_path_dag_opt = bsc_core.PthNodeOpt(dcc_path)
                        mya_path_dag_opt = dcc_path_dag_opt.translate_to(ma_configure.Util.OBJ_PATHSEP)
                        mya_obj_path = mya_path_dag_opt.path
                        mya_mesh = _mya_dcc_obj_geometry.Mesh(mya_obj_path)
                        mya_mesh_opt = _mya_dcc_opt_geometry.MeshOpt(mya_mesh)
                        #
                        dcc_obj_name = dcc_obj.name
                        face_vertices_uuid = mya_mesh_opt.get_face_vertices_as_uuid()
                        points_uuid = mya_mesh_opt.get_points_as_uuid()
                        cls._set_mesh_comparer_data_build_(
                            content_0,
                            dcc_path,
                            dcc_obj_name, face_vertices_uuid, points_uuid
                        )
        #
        return content_0
