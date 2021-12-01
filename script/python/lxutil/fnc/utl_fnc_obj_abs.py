# coding:utf-8
import copy

from lxbasic import bsc_core

import lxobj.core_objects as core_objects

import lxresolver.commands as rsv_commands

import lxresolver.operators as rsv_operators

from lxutil import utl_configure, utl_core

import lxbasic.objects as bsc_objects


class AbsExporter(object):
    OPTION = dict()
    def __init__(self, option=None):
        self._option = copy.deepcopy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                if k in self.OPTION:
                    self._option[k] = v
        #
        self._results = []

    def set_run(self):
        raise NotImplementedError()

    def get_results(self):
        return self._results


class AbsDccExporter(object):
    OPTION = dict()
    def __init__(self, file_path, root=None, option=None):
        #
        self._file_path = file_path
        #
        self._root = root
        if root is not None:
            self._root_dag_path = core_objects.ObjDagPath(root)
        else:
            self._root_dag_path = None
        #
        self._option = copy.copy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                if k in self.OPTION:
                    self._option[k] = v
        #
        self._results = []

    def set_run(self):
        raise NotImplementedError()

    def get_results(self):
        return self._results


class AbsDccImporter(object):
    pass


class AbsFncDccMeshMatcher(object):
    FNC_DCC_MESH_CLASS = None
    #
    SRC_DCC_CACHE = bsc_objects.Content(value=dict())
    @classmethod
    def _set_geometry_cache_(cls, src_path, tgt_path):
        if cls.FNC_DCC_MESH_CLASS is not None:
            cls.SRC_DCC_CACHE.set(
                '{}.geometry'.format(src_path),
                cls.FNC_DCC_MESH_CLASS(tgt_path).get_geometry()
            )
    @classmethod
    def _set_look_cache_(cls, src_path, tgt_path):
        if cls.FNC_DCC_MESH_CLASS is not None:
            cls.SRC_DCC_CACHE.set(
                '{}.look'.format(src_path),
                cls.FNC_DCC_MESH_CLASS(tgt_path).get_look()
            )
    @classmethod
    def _get_geometry_cache_(cls, src_path):
        return cls.SRC_DCC_CACHE.get(
            '{}.geometry'.format(src_path)
        )
    @classmethod
    def _get_look_cache_(cls, src_path):
        return cls.SRC_DCC_CACHE.get(
            '{}.look'.format(src_path)
        )

    def __init__(self, src_path, src_data, tgt_data):
        self._src_path = src_path
        self._src_data = src_data
        self._tgt_data = tgt_data
        #
        self._src_paths = self._src_data.get_branch_keys('property.path')
        self._src_face_vertices_uuid = self._src_data.get('face-vertices.path.{}'.format(self._src_path))
        self._src_points_uuid = self._src_data.get('points.path.{}'.format(self._src_path))
        #
        self._tgt_paths = self._tgt_data.get_branch_keys('property.path')
        self._tgt_face_vertices_uuids = self._tgt_data.get_branch_keys('face-vertices.uuid')
        self._tgt_points_uuids = self._tgt_data.get_branch_keys('points.uuid')

    def __get_path_exchanged_(self):
        tgt_path = self._src_path
        #
        output_path = tgt_path
        check_statuses = [
            utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED,
            utl_configure.DccMeshCheckStatus.POINTS_CHANGED
        ]
        #
        tgt_face_vertices_uuid_has_matched = self._src_face_vertices_uuid in self._tgt_face_vertices_uuids
        tgt_points_uuid_has_matched = self._src_points_uuid in self._tgt_points_uuids
        tgt_uuid_has_matched_condition = tgt_face_vertices_uuid_has_matched, tgt_points_uuid_has_matched
        if tgt_uuid_has_matched_condition == (True, True):
            tgt_face_vertices_uuid = self._src_face_vertices_uuid
            tgt_points_uuid = self._src_points_uuid
            tgt_paths_in_face_vertices = self._tgt_data.get(
                'face-vertices.uuid.{}'.format(tgt_face_vertices_uuid)
            ) or []
            tgt_paths_in_points = self._tgt_data.get(
                'points.uuid.{}'.format(tgt_points_uuid)
            ) or []
            uuid_matched_tgt_paths = bsc_core.ListMtd.get_intersection(
                tgt_paths_in_face_vertices,
                tgt_paths_in_points
            )
            if uuid_matched_tgt_paths:
                output_path = uuid_matched_tgt_paths[0]
                check_statuses = [
                    utl_configure.DccMeshCheckStatus.PATH_EXCHANGED
                ]
        elif tgt_uuid_has_matched_condition == (True, False):
            tgt_face_vertices_uuid = self._src_face_vertices_uuid
            tgt_paths_in_face_vertices = self._tgt_data.get(
                'face-vertices.uuid.{}'.format(tgt_face_vertices_uuid)
            ) or []
            uuid_matched_tgt_paths = tgt_paths_in_face_vertices
            if uuid_matched_tgt_paths:
                output_path = uuid_matched_tgt_paths[0]
                check_statuses = [
                    utl_configure.DccMeshCheckStatus.PATH_EXCHANGED,
                    utl_configure.DccMeshCheckStatus.POINTS_CHANGED
                ]
        elif tgt_uuid_has_matched_condition == (False, True):
            tgt_points_uuid = self._src_points_uuid
            tgt_paths_in_points = self._tgt_data.get(
                'points.uuid.{}'.format(tgt_points_uuid)
            ) or []
            uuid_matched_tgt_paths = tgt_paths_in_points
            if uuid_matched_tgt_paths:
                output_path = uuid_matched_tgt_paths[0]
                check_statuses = [
                    utl_configure.DccMeshCheckStatus.PATH_EXCHANGED,
                    utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED
                ]
        elif tgt_uuid_has_matched_condition == (False, False):
            output_path = tgt_path
            check_statuses = [
                utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED,
                utl_configure.DccMeshCheckStatus.POINTS_CHANGED
            ]
        #
        self._set_geometry_cache_(self._src_path, output_path)
        self._set_look_cache_(self._src_path, output_path)
        return output_path, check_statuses

    def __get_path_changed_(self):
        output_path = self._src_path
        check_statuses = [utl_configure.DccMeshCheckStatus.DELETION]
        #
        tgt_face_vertices_uuid_has_matched = self._src_face_vertices_uuid in self._tgt_face_vertices_uuids
        tgt_points_uuid_has_matched = self._src_points_uuid in self._tgt_points_uuids
        tgt_uuid_has_matched_condition = tgt_face_vertices_uuid_has_matched, tgt_points_uuid_has_matched
        if tgt_uuid_has_matched_condition == (True, True):
            tgt_face_vertices_uuid = self._src_face_vertices_uuid
            tgt_points_uuid = self._src_points_uuid
            #
            tgt_paths_in_face_vertices = self._tgt_data.get(
                'face-vertices.uuid.{}'.format(tgt_face_vertices_uuid)
            ) or []
            tgt_paths_in_points = self._tgt_data.get(
                'points.uuid.{}'.format(tgt_points_uuid)
            ) or []
            uuid_matched_tgt_paths = bsc_core.ListMtd.get_addition(
                bsc_core.ListMtd.get_intersection(tgt_paths_in_face_vertices, tgt_paths_in_points) or [],
                self._src_paths
            ) or []
            if uuid_matched_tgt_paths:
                output_path = uuid_matched_tgt_paths[0]
                check_statuses = [
                    utl_configure.DccMeshCheckStatus.PATH_CHANGED
                ]
        elif tgt_uuid_has_matched_condition == (True, False):
            tgt_face_vertices_uuid = self._src_face_vertices_uuid
            tgt_paths_in_face_vertices = self._tgt_data.get(
                'face-vertices.uuid.{}'.format(tgt_face_vertices_uuid)
            ) or []
            uuid_matched_tgt_paths = bsc_core.ListMtd.get_addition(
                tgt_paths_in_face_vertices,
                self._src_paths
            ) or []
            if uuid_matched_tgt_paths:
                output_path = uuid_matched_tgt_paths[0]
                check_statuses = [
                    utl_configure.DccMeshCheckStatus.PATH_CHANGED,
                    utl_configure.DccMeshCheckStatus.POINTS_CHANGED
                ]
        elif tgt_uuid_has_matched_condition == (False, True):
            tgt_points_uuid = self._src_points_uuid
            tgt_paths_in_points = self._tgt_data.get(
                'points.uuid.{}'.format(tgt_points_uuid)
            ) or []
            uuid_matched_tgt_paths = bsc_core.ListMtd.get_addition(
                tgt_paths_in_points,
                self._src_paths
            ) or []
            if uuid_matched_tgt_paths:
                output_path = uuid_matched_tgt_paths[0]
                check_statuses = [
                    utl_configure.DccMeshCheckStatus.PATH_CHANGED,
                    utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED
                ]
        elif tgt_uuid_has_matched_condition == (False, False):
            output_path = self._src_path
            check_statuses = [utl_configure.DccMeshCheckStatus.DELETION]
        return output_path, check_statuses

    def get(self):
        find_path_match = self._src_path in self._tgt_paths
        if find_path_match is True:
            tgt_path = self._src_path
            #
            output_path = tgt_path
            check_statuses = [
                utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED,
                utl_configure.DccMeshCheckStatus.POINTS_CHANGED
            ]
            #
            tgt_face_vertices_uuid = self._tgt_data.get(
                'face-vertices.path.{}'.format(tgt_path)
            )
            tgt_points_uuid = self._tgt_data.get('points.path.{}'.format(tgt_path))
            #
            tgt_face_vertices_match = self._src_face_vertices_uuid == tgt_face_vertices_uuid
            tgt_points_match = self._src_points_uuid == tgt_points_uuid
            tgt_match_condition = tgt_face_vertices_match, tgt_points_match
            #
            if tgt_match_condition == (True, True):
                check_statuses = [utl_configure.DccMeshCheckStatus.NON_CHANGED]
            elif tgt_match_condition == (True, False):
                check_statuses = [utl_configure.DccMeshCheckStatus.POINTS_CHANGED]
            elif tgt_match_condition == (False, True):
                check_statuses = [utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED]
            elif tgt_match_condition == (False, False):
                output_path, check_statuses = self.__get_path_exchanged_()
        else:
            output_path, check_statuses = self.__get_path_changed_()
        #
        check_statuses.sort(key=utl_configure.DccMeshCheckStatus.ALL.index)
        return output_path, '+'.join(check_statuses)


class AbsFncUsdMeshRepairer(object):
    FNC_USD_MESH_CLASS = None
    def __init__(self, src_usd_prim, tgt_path, check_statuses):
        self._src_usd_prim = src_usd_prim
        self._src_path = src_usd_prim.GetPath().pathString
        self._tgt_path = tgt_path
        self._check_statuses = check_statuses
    @classmethod
    def set_delete(cls, tgt_path):
        cls.FNC_USD_MESH_CLASS.set_delete(tgt_path)
    @classmethod
    def set_remove(cls, tgt_path):
        cls.FNC_USD_MESH_CLASS.set_remove(tgt_path)

    def set_run(self):
        # 1
        if self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED,
                    utl_configure.DccMeshCheckStatus.POINTS_CHANGED
                ]
        ):
            self.FNC_USD_MESH_CLASS(self._src_usd_prim).set_replace()
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED
                ]
        ):
            self.FNC_USD_MESH_CLASS(self._src_usd_prim).set_replace()
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.POINTS_CHANGED
                ]
        ):
            self.FNC_USD_MESH_CLASS(self._src_usd_prim).set_points()
        # 2
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.DELETION
                ]
        ):
            self.FNC_USD_MESH_CLASS(self._src_usd_prim).set_create()
        #
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.PATH_CHANGED
                ]
        ):
            self.FNC_USD_MESH_CLASS(self._src_usd_prim).set_repath_to(self._tgt_path)
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.PATH_CHANGED,
                    utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED
                ]
        ):
            self.FNC_USD_MESH_CLASS(self._src_usd_prim).set_repath_to(self._tgt_path)
            self.FNC_USD_MESH_CLASS(self._src_usd_prim).set_replace(
                keep_materials=True,
                keep_properties=True,
                keep_visibilities=True,
                transfer_uv_maps=True
            )
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.PATH_CHANGED,
                    utl_configure.DccMeshCheckStatus.POINTS_CHANGED
                ]
        ):
            self.FNC_USD_MESH_CLASS(self._src_usd_prim).set_repath_to(self._tgt_path)
            self.FNC_USD_MESH_CLASS(self._src_usd_prim).set_points()
        # 3
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.PATH_EXCHANGED
                ]
        ):
            geometry = AbsFncDccMeshMatcher._get_geometry_cache_(self._src_path)
            look = AbsFncDccMeshMatcher._get_look_cache_(self._src_path)
            self.FNC_USD_MESH_CLASS(self._src_usd_prim).set_exchange(
                geometry, look
            )
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.PATH_EXCHANGED,
                    utl_configure.DccMeshCheckStatus.POINTS_CHANGED
                ]
        ):
            geometry = AbsFncDccMeshMatcher._get_geometry_cache_(self._src_path)
            look = AbsFncDccMeshMatcher._get_look_cache_(self._src_path)
            self.FNC_USD_MESH_CLASS(self._src_usd_prim).set_exchange(
                geometry, look
            )
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.PATH_EXCHANGED,
                    utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED
                ]
        ):
            geometry = AbsFncDccMeshMatcher._get_geometry_cache_(self._src_path)
            look = AbsFncDccMeshMatcher._get_look_cache_(self._src_path)
            self.FNC_USD_MESH_CLASS(self._src_usd_prim).set_exchange(
                geometry, look
            )


class AbsFncDccGeometryComparer(object):
    DCC_SCENE_CLASS = None
    DCC_SCENE_OPT_CLASS = None
    #
    OPTION = dict()
    #
    FNC_DCC_MESH_MATCHER_CLASS = None
    FNC_USD_MESH_REPAIRER_CLASS = None
    def __init__(self, file_path, root=None, option=None):
        self._scene_file_path = file_path
        self._root = root
        #
        self._cache_directory = bsc_core.EnvironMtd.get_temporary_path()
        self._resolver = rsv_commands.get_resolver()
        #
        self._option = copy.deepcopy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                if k in self.OPTION:
                    self._option[k] = v
        #
        self._task_properties = self._resolver.get_task_properties_by_any_scene_file_path(
            file_path=file_path
        )
        if self._task_properties is not None:
            step = self._task_properties.get('step')
            if step in ['mod', 'srf', 'rig']:
                self._set_model_geometry_usd_hi_file_path_(
                    rsv_operators.RsvAssetGeometryQuery(
                        self._task_properties
                    ).get_usd_hi_file(
                        step='mod', task='modeling', version='latest'
                    )
                )
            else:
                raise TypeError()
        else:
            raise TypeError()
        #
        self._set_model_dcc_objs_init_()
        self._set_scene_dcc_obj_init_()
        #
        self._results = []

    def _set_model_geometry_usd_hi_file_path_(self, file_path):
        self._model_geometry_usd_hi_file_path = file_path

    def _set_model_dcc_objs_init_(self):
        import lxusd.dcc.dcc_objects as usd_dcc_objects
        #
        import lxusd.dcc.dcc_operators as usd_dcc_operators
        #
        self._model_dcc_obj_scene = usd_dcc_objects.Scene()
        self._model_dcc_obj_universe = self._model_dcc_obj_scene.universe
        self._model_usd_scene_opt = usd_dcc_operators.SceneOpt(self._model_dcc_obj_scene.usd_stage)
        self._model_dcc_mesh_comparer_data = bsc_objects.Content(
            value={}
        )
        #
        self._model_dcc_geometries = []

    def _set_model_dcc_objs_update_(self):
        import lxusd.dcc.dcc_operators as usd_dcc_operators
        usd_file_path = self._model_geometry_usd_hi_file_path
        root = self._root
        if usd_file_path is not None:
            self._model_dcc_obj_scene.set_load_from_dot_usd(usd_file_path, root)
            self._model_dcc_obj_universe = self._model_dcc_obj_scene.universe
            self._model_usd_scene_opt = usd_dcc_operators.SceneOpt(self._model_dcc_obj_scene.usd_stage)
            self._model_dcc_mesh_comparer_data = self._model_usd_scene_opt.get_mesh_comparer_data(
                usd_file_path
            )
            #
            self._model_dcc_geometries = []
            mesh_type = self._model_dcc_obj_universe.get_obj_type('Mesh')
            if mesh_type is not None:
                self._model_dcc_geometries = mesh_type.get_objs()

    def _set_scene_dcc_obj_init_(self):
        import lxusd.dcc.dcc_objects as usd_dcc_objects
        #
        import lxusd.dcc.dcc_operators as usd_dcc_operators
        #
        self._scene_dcc_obj_scene = usd_dcc_objects.Scene()
        self._scene_dcc_obj_universe = self._scene_dcc_obj_scene.universe
        self._scene_dcc_stage_opt = usd_dcc_operators.SceneOpt(self._scene_dcc_obj_scene.usd_stage)
        self._scene_dcc_mesh_comparer_data = bsc_objects.Content(
            value={}
        )
        #
        self._scene_dcc_geometries = []

    def _set_scene_dcc_objs_update_(self):
        scene_file_path = self._scene_file_path
        root = self._root
        #
        self._scene_dcc_obj_scene = self.DCC_SCENE_CLASS()
        self._scene_dcc_obj_scene.set_load_by_root(root, include_obj_type=['mesh'])
        self._scene_dcc_obj_universe = self._scene_dcc_obj_scene.universe
        self._scene_dcc_stage_opt = self.DCC_SCENE_OPT_CLASS(self._scene_dcc_obj_universe)
        self._scene_dcc_mesh_comparer_data = self._scene_dcc_stage_opt.get_mesh_comparer_data(scene_file_path)
        #
        self._scene_dcc_geometries = []
        mesh_type = self._scene_dcc_obj_universe.get_obj_type('mesh')
        if mesh_type is not None:
            self._scene_dcc_geometries = mesh_type.get_objs()
    # geometry in model
    def get_model_dcc_geometry(self, dcc_geometry_path):
        return self._model_dcc_obj_universe.get_obj(dcc_geometry_path)
    # geometry in scene
    def get_scene_dcc_geometry(self, dcc_geometry_path):
        return self._scene_dcc_obj_universe.get_obj(dcc_geometry_path)

    def get_matched_mesh(self, src_path):
        src_data = self._model_dcc_mesh_comparer_data
        tgt_data = self._scene_dcc_mesh_comparer_data
        return self.FNC_DCC_MESH_MATCHER_CLASS(
            src_path, src_data, tgt_data
        ).get()

    def set_mesh_repair(self, src_path, tgt_path, check_statuses):
        src_usd_prim = self._model_dcc_obj_scene.usd_stage.GetPrimAtPath(src_path)
        if src_usd_prim.IsValid() is True:
            self.FNC_USD_MESH_REPAIRER_CLASS(
                src_usd_prim, tgt_path, check_statuses
            ).set_run()
        else:
            if check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.ADDITION
                ]
            ):
                self.FNC_USD_MESH_REPAIRER_CLASS.set_delete(tgt_path)

    def set_run(self):
        self._results = []
        #
        methods = [
            self._set_model_dcc_objs_update_,
            self._set_scene_dcc_objs_update_
        ]
        if methods:
            gp = utl_core.GuiProgressesRunner(maximum=len(methods))
            for method in methods:
                gp.set_update()
                method()
            #
            gp.set_stop()
        #
        src_dcc_geometries = self._model_dcc_geometries
        tgt_dcc_geometries = self._scene_dcc_geometries
        #
        if src_dcc_geometries:
            gp = utl_core.GuiProgressesRunner(maximum=len(src_dcc_geometries))
            for i_src_geometry in src_dcc_geometries:
                gp.set_update()
                if i_src_geometry.type_name == 'Mesh':
                    i_src_mesh_path = i_src_geometry.path
                    #
                    i_mesh_path, i_check_statuses = self.get_matched_mesh(src_path=i_src_mesh_path)
                    self._results.append(
                        (i_mesh_path, i_check_statuses)
                    )
            #
            gp.set_stop()
        #
        src_dcc_paths = [i.path for i in src_dcc_geometries]
        tgt_dcc_paths = [i.path for i in tgt_dcc_geometries]
        addition_geometry_paths = list(set(tgt_dcc_paths)-set(src_dcc_paths))
        for i_tgt_geometry_path in addition_geometry_paths:
            self._results.append(
                (i_tgt_geometry_path, utl_configure.DccMeshCheckStatus.ADDITION)
            )
        return self._results

    def get_results(self):
        lis = []
        #
        methods = [
            self._set_model_dcc_objs_update_,
            self._set_scene_dcc_objs_update_
        ]
        if methods:
            gp = utl_core.GuiProgressesRunner(maximum=len(methods))
            for method in methods:
                gp.set_update()
                method()
            #
            gp.set_stop()
        #
        src_dcc_geometries = self._model_dcc_geometries
        tgt_dcc_geometries = self._scene_dcc_geometries
        #
        dcc_geometry_paths = []
        if src_dcc_geometries:
            gp = utl_core.GuiProgressesRunner(maximum=len(src_dcc_geometries))
            for i_src_geometry in src_dcc_geometries:
                gp.set_update()
                if i_src_geometry.type_name == 'Mesh':
                    i_src_mesh_path = i_src_geometry.path
                    #
                    i_tgt_mesh_path, i_check_statuses = self.get_matched_mesh(src_path=i_src_mesh_path)
                    lis.append(
                        (i_src_mesh_path, i_tgt_mesh_path, i_check_statuses)
                    )
                    dcc_geometry_paths.append(i_tgt_mesh_path)
            #
            gp.set_stop()
        # addition
        src_dcc_geometry_paths = [i.path for i in src_dcc_geometries]
        tgt_dcc_geometry_paths = [i.path for i in tgt_dcc_geometries]
        addition_geometry_paths = list(set(tgt_dcc_geometry_paths) - set(src_dcc_geometry_paths) - set(dcc_geometry_paths))
        for i_tgt_geometry_path in addition_geometry_paths:
            lis.append(
                (i_tgt_geometry_path, i_tgt_geometry_path, utl_configure.DccMeshCheckStatus.ADDITION)
            )
        return lis


class AbsFncOptionMethod(object):
    OPTION = dict()
    def __init__(self, option):
        self._option = copy.copy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                self._option[k] = v

    def get_option(self):
        return self._option
    option = property(get_option)
