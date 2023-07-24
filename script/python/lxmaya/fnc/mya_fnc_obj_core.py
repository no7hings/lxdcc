# coding:utf-8
from lxbasic import bsc_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_operators as mya_dcc_operators

import lxusd.dcc.dcc_operators as usd_dcc_operators


class FncUsdObj(object):
    OBJ_PATHSEP = '|'
    def __init__(self, usd_prim, location=None):
        self._usd_prim = usd_prim
        self._usd_stage = usd_prim.GetStage()
        #
        self._dcc_path = usd_prim.GetPath().pathString
        self._usd_path = self._dcc_path
        self._usd_path_dag_opt = bsc_core.DccPathDagOpt(self._usd_path)
        self._mya_path_dag_opt = self._usd_path_dag_opt.translate_to(self.OBJ_PATHSEP)
        #
        if location is not None:
            location_path_dag_opt = bsc_core.DccPathDagOpt(location)
            mya_root = location_path_dag_opt.translate_to(self.OBJ_PATHSEP)
            self._mya_path_dag_opt.set_parent_path(mya_root.path)

    def __str__(self):
        return '{}(path="{}")'.format(
            self.__class__.__name__,
            self._usd_path
        )

    def set_customize_ports_create(self, port_match_patterns):
        pass


class FncUsdTransform(FncUsdObj):
    def __init__(self, usd_prim, location=None):
        super(FncUsdTransform, self).__init__(usd_prim, location)

    def set_create(self):
        mya_transform = mya_dcc_objects.Transform(self._mya_path_dag_opt.get_value())
        if mya_transform.get_is_exists() is False:
            usd_transform_opt = usd_dcc_operators.TransformOpt(self._usd_prim)
            matrix = usd_transform_opt.get_matrix()
            #
            mya_transform_opt = mya_dcc_operators.TransformOpt(mya_transform)
            if mya_transform_opt.set_create() is True:
                mya_transform_opt.set_matrix(matrix)


class FncUsdMesh(FncUsdObj):
    def __init__(self, usd_prim, location=None):
        super(FncUsdMesh, self).__init__(usd_prim, location)
        #
        self._usd_transform_path_dag_opt = self._usd_path_dag_opt.get_parent()
        self._usd_group_path_dag_opt = self._usd_transform_path_dag_opt.get_parent()
        #
        self._mya_transform_path_dag_opt = self._mya_path_dag_opt.get_parent()
        self._mya_group_path_dag_opt = self._mya_transform_path_dag_opt.get_parent()

    def set_repath_to(self, tgt_path):
        self.set_group_create()
        #
        tgt_path_dag_opt = bsc_core.DccPathDagOpt(tgt_path)
        tgt_mya_path_dag_opt = tgt_path_dag_opt.translate_to(self.OBJ_PATHSEP)
        tgt_mya_mesh = mya_dcc_objects.Mesh(tgt_mya_path_dag_opt.get_value())
        #
        if tgt_mya_mesh.get_is_exists() is True:
            tgt_mya_transform = tgt_mya_mesh.transform
            tgt_mya_transform.set_repath(self._mya_transform_path_dag_opt.get_value())

    def set_group_create(self):
        mya_group = mya_dcc_objects.Group(self._mya_group_path_dag_opt.get_value())
        if mya_group.get_is_exists() is False:
            usd_paths = self._usd_group_path_dag_opt.get_component_paths()
            if usd_paths:
                usd_paths.reverse()
                for i_usd_path in usd_paths:
                    if i_usd_path != '/':
                        FncUsdTransform(
                            self._usd_stage.GetPrimAtPath(i_usd_path)
                        ).set_create()

    def set_transform_create(self):
        mya_transform = mya_dcc_objects.Transform(self._mya_transform_path_dag_opt.get_value())
        if mya_transform.get_is_exists() is False:
            FncUsdTransform(
                self._usd_stage.GetPrimAtPath(self._usd_transform_path_dag_opt.get_value())
            ).set_create()

    def set_create(self, with_group=True, with_transform=True):
        if with_group is True:
            self.set_group_create()
        #
        if with_transform is True:
            self.set_transform_create()
        #
        mya_mesh = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
        if mya_mesh.get_is_exists() is False:
            usd_mesh_opt = usd_dcc_operators.MeshOpt(self._usd_prim)
            face_vertices = usd_mesh_opt.get_face_vertices()
            points = usd_mesh_opt.get_points()
            #
            mya_mesh_opt = mya_dcc_operators.MeshOpt(mya_mesh)
            is_create = mya_mesh_opt.set_create(
                face_vertices=face_vertices, points=points
            )
            if is_create is True:
                uv_maps = usd_mesh_opt.get_uv_maps()
                mya_mesh_opt.set_uv_maps(uv_maps)
                #
                mya_mesh_look_opt = mya_dcc_operators.MeshLookOpt(mya_mesh)
                mya_mesh_look_opt.set_default_material_assign()

    def set_replace(self):
        old_mya_mesh = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
        if old_mya_mesh.get_is_exists() is True:
            old_mya_mesh_opt = mya_dcc_operators.MeshOpt(old_mya_mesh)
            old_face_vertices_uuid = old_mya_mesh_opt.get_face_vertices_as_uuid()
            #
            geometry = FncDccMesh(self._dcc_path).get_geometry()
            look = FncDccMesh(self._dcc_path).get_look()
            #
            old_mya_transform = old_mya_mesh.transform
            old_mya_transform.set_visible(False)
            old_mya_transform.set_parent_path(self.OBJ_PATHSEP)
            # instance after
            mya_mesh = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
            if mya_mesh.get_is_exists() is False:
                self.set_transform_create()
                #
                usd_mesh_opt = usd_dcc_operators.MeshOpt(self._usd_prim)
                face_vertices_uuid = usd_mesh_opt.get_face_vertices_as_uuid()
                face_vertices = usd_mesh_opt.get_face_vertices()
                points = usd_mesh_opt.get_points()
                #
                mya_mesh_opt = mya_dcc_operators.MeshOpt(mya_mesh)
                mya_mesh_look_opt = mya_dcc_operators.MeshLookOpt(mya_mesh)
                is_create = mya_mesh_opt.set_create(
                    face_vertices=face_vertices, points=points
                )
                #
                if is_create is True:
                    if face_vertices_uuid == old_face_vertices_uuid:
                        uv_maps = geometry['uv_maps']
                        mya_mesh_opt.set_uv_maps(uv_maps)
                    else:
                        old_mya_mesh._update_path_()
                        old_mya_mesh.set_uv_maps_transfer_to(mya_mesh.path, clear_history=True)
                    #
                    material_assigns = look['material_assigns']
                    properties = look['properties']
                    visibilities = look['visibilities']
                    #
                    mya_mesh_look_opt.set_material_assigns(material_assigns)
                    mya_mesh_look_opt.set_properties(properties)
                    mya_mesh_look_opt.set_visibilities(visibilities)
            #
            old_mya_transform._update_path_()
            old_mya_transform.set_delete()

    def set_exchange(self, geometry, look):
        old_mya_mesh = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
        if old_mya_mesh.get_is_exists() is True:
            old_mya_mesh_opt = mya_dcc_operators.MeshOpt(old_mya_mesh)
            old_face_vertices_uuid = old_mya_mesh_opt.get_face_vertices_as_uuid()
            #
            old_mya_transform = old_mya_mesh.transform
            old_mya_transform.set_visible(False)
            old_mya_transform.set_parent_path(self.OBJ_PATHSEP)
            #
            mya_mesh = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
            if mya_mesh.get_is_exists() is False:
                self.set_transform_create()
                #
                usd_mesh_opt = usd_dcc_operators.MeshOpt(self._usd_prim)
                face_vertices_uuid = usd_mesh_opt.get_face_vertices_as_uuid()
                #
                face_vertices = usd_mesh_opt.get_face_vertices()
                points = usd_mesh_opt.get_points()
                #
                mya_mesh_opt = mya_dcc_operators.MeshOpt(mya_mesh)
                is_create = mya_mesh_opt.set_create(
                    face_vertices=face_vertices, points=points
                )
                if is_create is True:
                    old_face_vertices_uuid = geometry['face_vertices_uuid']
                    if face_vertices_uuid == old_face_vertices_uuid:
                        uv_maps = geometry['uv_maps']
                        mya_mesh_opt.set_uv_maps(uv_maps)
                    else:
                        old_mya_mesh._update_path_()
                        old_mya_mesh.set_uv_maps_transfer_to(mya_mesh.path, clear_history=True)

                    mya_mesh_look_opt = mya_dcc_operators.MeshLookOpt(mya_mesh)
                    #
                    material_assigns = look['material_assigns']
                    properties = look['properties']
                    visibilities = look['visibilities']
                    #
                    mya_mesh_look_opt.set_material_assigns(material_assigns)
                    mya_mesh_look_opt.set_properties(properties)
                    mya_mesh_look_opt.set_visibilities(visibilities)
                #
                old_mya_transform._update_path_()
                old_mya_transform.set_delete()

    def set_points(self):
        mya_mesh = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
        if mya_mesh.get_is_exists() is True:
            usd_mesh_opt = usd_dcc_operators.MeshOpt(self._usd_prim)
            #
            mya_mesh_opt = mya_dcc_operators.MeshOpt(mya_mesh)
            points = usd_mesh_opt.get_points()
            mya_mesh_opt.set_points(points)

    def set_uv_maps(self):
        mya_mesh = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
        if mya_mesh.get_is_exists() is True:
            usd_mesh_opt = usd_dcc_operators.MeshOpt(self._usd_prim)
            #
            mya_mesh_opt = mya_dcc_operators.MeshOpt(mya_mesh)
            uv_maps = usd_mesh_opt.get_uv_maps()
            mya_mesh_opt.set_uv_maps(uv_maps)
    @classmethod
    def set_delete(cls, tgt_path):
        mesh_dcc_path_dag_opt = bsc_core.DccPathDagOpt(tgt_path)
        transform_dcc_path_dag_opt = mesh_dcc_path_dag_opt.get_parent()
        transform_mya_path_dag_opt = transform_dcc_path_dag_opt.translate_to(cls.OBJ_PATHSEP)
        mya_dcc_objects.Node(transform_mya_path_dag_opt.get_value()).set_delete()
    @classmethod
    def set_remove(cls, tgt_path):
        mesh_dcc_path_dag_opt = bsc_core.DccPathDagOpt(tgt_path)
        transform_dcc_path_dag_opt = mesh_dcc_path_dag_opt.get_parent()
        transform_mya_path_dag_opt = transform_dcc_path_dag_opt.translate_to(cls.OBJ_PATHSEP)
        mya_dcc_objects.Node(transform_mya_path_dag_opt.get_value()).set_to_world()


class FncDccMesh(object):
    OBJ_PATHSEP = '|'
    def __init__(self, dcc_path):
        self._dcc_path_dag_opt = bsc_core.DccPathDagOpt(dcc_path)
        self._mya_path_dag_opt = self._dcc_path_dag_opt.translate_to(self.OBJ_PATHSEP)
        self._maya_mesh = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
        #
        self._mya_mesh_opt = mya_dcc_operators.MeshOpt(self._maya_mesh)
        self._mya_mesh_look_opt = mya_dcc_operators.MeshLookOpt(self._maya_mesh)

    def get_geometry(self):
        if self._maya_mesh.get_is_exists() is True:
            return dict(
                face_vertices=self._mya_mesh_opt.get_face_vertices(),
                face_vertices_uuid=self._mya_mesh_opt.get_face_vertices_as_uuid(),
                points=self._mya_mesh_opt.get_points(),
                uv_maps=self._mya_mesh_opt.get_uv_maps()

            )
        return {}

    def get_look(self):
        if self._maya_mesh.get_is_exists() is True:
            return dict(
                material_assigns=self._mya_mesh_look_opt.get_material_assigns(),
                properties=self._mya_mesh_look_opt.get_properties(),
                visibilities=self._mya_mesh_look_opt.get_visibilities()
            )
        return {}
