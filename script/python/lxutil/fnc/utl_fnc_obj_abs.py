# coding:utf-8
import copy

import os

import glob

from lxbasic import bsc_core

import lxresolver.commands as rsv_commands

import lxresolver.operators as rsv_operators

from lxutil import utl_configure, utl_core

import lxutil.objects as utl_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxcontent.objects as ctt_objects


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
            self._root_dat_opt = bsc_core.DccPathDagOpt(root)
        else:
            self._root_dat_opt = None
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
    FNC_DCC_MESH_CLS = None
    #
    SRC_DCC_CACHE = ctt_objects.Content(value=dict())

    @classmethod
    def _set_geometry_cache_(cls, src_path, tgt_path):
        if cls.FNC_DCC_MESH_CLS is not None:
            cls.SRC_DCC_CACHE.set(
                '{}.geometry'.format(src_path),
                cls.FNC_DCC_MESH_CLS(tgt_path).get_geometry()
            )

    @classmethod
    def _set_look_cache_(cls, src_path, tgt_path):
        if cls.FNC_DCC_MESH_CLS is not None:
            cls.SRC_DCC_CACHE.set(
                '{}.look'.format(src_path),
                cls.FNC_DCC_MESH_CLS(tgt_path).get_look()
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
            uuid_matched_tgt_paths = bsc_core.RawListMtd.get_intersection(
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
            #
            uuid_matched_tgt_paths = bsc_core.RawListMtd.get_addition(
                bsc_core.RawListMtd.get_intersection(tgt_paths_in_face_vertices, tgt_paths_in_points) or [],
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
            uuid_matched_tgt_paths = bsc_core.RawListMtd.get_addition(
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
            uuid_matched_tgt_paths = bsc_core.RawListMtd.get_addition(
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
    FNC_USD_MESH_CLS = None

    def __init__(self, src_usd_prim, tgt_path, check_statuses):
        self._src_usd_prim = src_usd_prim
        self._src_path = src_usd_prim.GetPath().pathString
        self._tgt_path = tgt_path
        self._check_statuses = check_statuses

    @classmethod
    def set_delete(cls, tgt_path):
        cls.FNC_USD_MESH_CLS.set_delete(tgt_path)

    @classmethod
    def set_remove(cls, tgt_path):
        cls.FNC_USD_MESH_CLS.set_remove(tgt_path)

    def set_run(self):
        # 1
        if self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED,
                    utl_configure.DccMeshCheckStatus.POINTS_CHANGED
                ]
        ):
            self.FNC_USD_MESH_CLS(self._src_usd_prim).set_replace()
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED
                ]
        ):
            self.FNC_USD_MESH_CLS(self._src_usd_prim).set_replace()
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.POINTS_CHANGED
                ]
        ):
            self.FNC_USD_MESH_CLS(self._src_usd_prim).set_points()
        # 2
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.DELETION
                ]
        ):
            self.FNC_USD_MESH_CLS(self._src_usd_prim).set_create()
        #
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.PATH_CHANGED
                ]
        ):
            self.FNC_USD_MESH_CLS(self._src_usd_prim).set_repath_to(self._tgt_path)
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.PATH_CHANGED,
                    utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED
                ]
        ):
            self.FNC_USD_MESH_CLS(self._src_usd_prim).set_repath_to(self._tgt_path)
            self.FNC_USD_MESH_CLS(self._src_usd_prim).set_replace(
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
            self.FNC_USD_MESH_CLS(self._src_usd_prim).set_repath_to(self._tgt_path)
            self.FNC_USD_MESH_CLS(self._src_usd_prim).set_points()
        # 3
        elif self._check_statuses == '+'.join(
                [
                    utl_configure.DccMeshCheckStatus.PATH_EXCHANGED
                ]
        ):
            geometry = AbsFncDccMeshMatcher._get_geometry_cache_(self._src_path)
            look = AbsFncDccMeshMatcher._get_look_cache_(self._src_path)
            self.FNC_USD_MESH_CLS(self._src_usd_prim).set_exchange(
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
            self.FNC_USD_MESH_CLS(self._src_usd_prim).set_exchange(
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
            self.FNC_USD_MESH_CLS(self._src_usd_prim).set_exchange(
                geometry, look
            )


class AbsFncDccGeometryComparer(object):
    DCC_SCENE_CLS = None
    DCC_SCENE_OPT_CLS = None
    #
    OPTION = dict()
    #
    FNC_DCC_MESH_MATCHER_CLS = None
    FNC_USD_MESH_REPAIRER_CLS = None
    #
    CACHE = {}
    #
    RSV_KEYWORD = 'asset-geometry-usd-payload-file'
    DCC_NAMESPACE = 'usd'

    def __init__(self, file_path, location=None, location_source=None):
        self._file_path = file_path
        self._location = location
        self._location_source = location_source
        #
        self._cache_directory = bsc_core.EnvironMtd.get_temporary_root()
        self._resolver = rsv_commands.get_resolver()
        #
        self._rsv_scene_properties = self._resolver.get_rsv_scene_properties_by_any_scene_file_path(
            file_path=file_path
        )
        if self._rsv_scene_properties is not None:
            step = self._rsv_scene_properties.get('step')
            if step in ['mod', 'srf', 'rig', 'grm']:
                keyword = self.RSV_KEYWORD
                rsv_resource = self._resolver.get_rsv_resource(
                    **self._rsv_scene_properties.get_value()
                )
                rsv_model_task = rsv_resource.get_rsv_task(
                    step='mod', task='modeling'
                )
                if rsv_model_task is not None:
                    rsv_unit = rsv_model_task.get_rsv_unit(
                        keyword=keyword
                    )
                    result = rsv_unit.get_result()
                    if result:
                        self.set_source_file(result)
            else:
                raise TypeError()
        else:
            raise TypeError()
        #
        self.init_source_fnc()
        self.init_target_fnc()
        #
        self._results = []

    def set_source_file(self, file_path):
        self._source_file_path = file_path

    def init_source_fnc(self):
        import lxusd.dcc.dcc_objects as usd_dcc_objects
        #
        import lxusd.dcc.dcc_operators as usd_dcc_operators

        #
        self._dcc_scene_src = usd_dcc_objects.Scene()
        self._dcc_universe_src = self._dcc_scene_src.universe
        self._dcc_stage_opt_src = usd_dcc_operators.SceneOpt(self._dcc_scene_src.usd_stage, self.DCC_NAMESPACE)
        self._dcc_comparer_data_src = ctt_objects.Content(
            value={}
        )
        #
        self._dcc_geometries_src = []

    def init_target_fnc(self):
        import lxusd.dcc.dcc_objects as usd_dcc_objects
        #
        import lxusd.dcc.dcc_operators as usd_dcc_operators

        #
        self._dcc_scene_tgt = usd_dcc_objects.Scene()
        self._dcc_universe_tgt = self._dcc_scene_tgt.universe
        self._dcc_stage_opt_tgt = usd_dcc_operators.SceneOpt(self._dcc_scene_tgt.usd_stage, self.DCC_NAMESPACE)
        self._dcc_comparer_data_tgt = ctt_objects.Content(
            value={}
        )
        #
        self._dcc_geometries_tgt = []

    #
    def update_source_fnc(self):
        import lxusd.dcc.dcc_objects as usd_dcc_objects
        #
        import lxusd.dcc.dcc_operators as usd_dcc_operators

        #
        usd_file_path = self._source_file_path
        if usd_file_path is not None:
            time_tag = bsc_core.StgFileOpt(usd_file_path).get_modify_time_tag()
            if time_tag in AbsFncDccGeometryComparer.CACHE:
                self._dcc_universe_src = AbsFncDccGeometryComparer.CACHE[time_tag]
            else:
                self._dcc_scene_src = usd_dcc_objects.Scene()
                self._dcc_scene_src.load_from_dot_usd(
                    usd_file_path,
                    self._location,
                    self._location_source
                )
                self._dcc_universe_src = self._dcc_scene_src.universe
                AbsFncDccGeometryComparer.CACHE[time_tag] = self._dcc_universe_src
            #
            self._dcc_stage_opt_src = usd_dcc_operators.SceneOpt(self._dcc_scene_src.usd_stage, self.DCC_NAMESPACE)
            self._dcc_comparer_data_src = self._dcc_stage_opt_src.get_mesh_comparer_data(
                usd_file_path
            )
            #
            self._dcc_geometries_src = []
            mesh_type = self._dcc_universe_src.get_obj_type('Mesh')
            if mesh_type is not None:
                self._dcc_geometries_src = mesh_type.get_objs()

    def update_target_fnc(self):
        scene_file_path = self._file_path
        location = self._location
        #
        self._dcc_scene_tgt = self.DCC_SCENE_CLS()
        self._dcc_scene_tgt.load_from_location(location, include_obj_type=['mesh'])
        self._dcc_universe_tgt = self._dcc_scene_tgt.universe
        self._dcc_stage_opt_tgt = self.DCC_SCENE_OPT_CLS(self._dcc_universe_tgt)
        self._dcc_comparer_data_tgt = self._dcc_stage_opt_tgt.get_mesh_comparer_data(scene_file_path)
        #
        self._dcc_geometries_tgt = []
        mesh_type = self._dcc_universe_tgt.get_obj_type('mesh')
        if mesh_type is not None:
            self._dcc_geometries_tgt = mesh_type.get_objs()

    #
    def get_geometry_src(self, dcc_geometry_path):
        return self._dcc_universe_src.get_obj(dcc_geometry_path)

    def get_geometry_tgt(self, dcc_geometry_path):
        return self._dcc_universe_tgt.get_obj(dcc_geometry_path)

    #
    def get_matched_mesh(self, src_path):
        src_data = self._dcc_comparer_data_src
        tgt_data = self._dcc_comparer_data_tgt
        return self.FNC_DCC_MESH_MATCHER_CLS(
            src_path, src_data, tgt_data
        ).get()

    #
    def repair_mesh(self, src_path, tgt_path, check_statuses):
        src_usd_prim = self._dcc_scene_src.usd_stage.GetPrimAtPath(src_path)
        if src_usd_prim.IsValid() is True:
            self.FNC_USD_MESH_REPAIRER_CLS(
                src_usd_prim, tgt_path, check_statuses
            ).set_run()
        else:
            if check_statuses == '+'.join(
                    [
                        utl_configure.DccMeshCheckStatus.ADDITION
                    ]
            ):
                self.FNC_USD_MESH_REPAIRER_CLS.set_delete(tgt_path)

    def set_run(self):
        self._results = []
        #
        methods = [
            self.update_source_fnc,
            self.update_target_fnc
        ]
        if methods:
            with bsc_core.LogProcessContext.create(
                maximum=len(methods), label='execute geometry-comparer method'
            ) as g_p:
                for method in methods:
                    g_p.set_update()
                    method()
        #
        src_dcc_geometries = self._dcc_geometries_src
        tgt_dcc_geometries = self._dcc_geometries_tgt
        #
        if src_dcc_geometries:
            with bsc_core.LogProcessContext.create(
                maximum=len(src_dcc_geometries), label='gain geometry-comparer result'
            ) as g_p:
                for i_src_geometry in src_dcc_geometries:
                    g_p.set_update()
                    if i_src_geometry.type_name == 'Mesh':
                        i_src_mesh_path = i_src_geometry.path
                        #
                        i_mesh_path, i_check_statuses = self.get_matched_mesh(src_path=i_src_mesh_path)
                        self._results.append(
                            (i_mesh_path, i_check_statuses)
                        )
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
            self.update_source_fnc,
            self.update_target_fnc
        ]
        if methods:
            with bsc_core.LogProcessContext.create(
                maximum=len(methods), label='execute geometry-comparer method'
            ) as g_p:
                for method in methods:
                    g_p.set_update()
                    method()
        #
        dcc_geometries_src = self._dcc_geometries_src
        dcc_geometries_tgt = self._dcc_geometries_tgt
        #
        dcc_geometry_paths = []
        if dcc_geometries_src:
            with bsc_core.LogProcessContext.create(
                maximum=len(dcc_geometries_src), label='gain geometry-comparer result'
            ) as g_p:
                for i_src_geometry in dcc_geometries_src:
                    g_p.set_update()
                    if i_src_geometry.type_name == 'Mesh':
                        i_src_mesh_path = i_src_geometry.path
                        #
                        i_tgt_mesh_path, i_check_statuses = self.get_matched_mesh(src_path=i_src_mesh_path)
                        lis.append(
                            (i_src_mesh_path, i_tgt_mesh_path, i_check_statuses)
                        )
                        dcc_geometry_paths.append(i_tgt_mesh_path)
        # addition
        dcc_geometry_paths_src = [i.path for i in dcc_geometries_src]
        dcc_geometry_paths_tgt = [i.path for i in dcc_geometries_tgt]
        addition_geometry_paths = list(set(dcc_geometry_paths_tgt)-set(dcc_geometry_paths_src)-set(dcc_geometry_paths))
        for i_tgt_geometry_path in addition_geometry_paths:
            lis.append(
                (i_tgt_geometry_path, i_tgt_geometry_path, utl_configure.DccMeshCheckStatus.ADDITION)
            )
        return lis


class AbsFncOptionBase(object):
    OPTION = dict()

    def __init__(self, option=None):
        self._option = copy.copy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                self._option[k] = v

    def get_option(self):
        return self._option

    option = property(get_option)

    def get(self, key):
        return self._option.get(key)


class AbsDotXgenDef(object):
    @classmethod
    def _get_xgen_collection_file_paths_(cls, maya_scene_file_path):
        d = os.path.splitext(maya_scene_file_path)[0]
        glob_pattern = '{}__*.xgen'.format(d)
        return glob.glob(glob_pattern) or []

    @classmethod
    def _get_xgen_collection_names_(cls, maya_scene_file_path):
        file_paths = cls._get_xgen_collection_file_paths_(maya_scene_file_path)
        return [cls._get_xgen_collection_name_(i) for i in file_paths]

    @classmethod
    def _get_xgen_collection_name_(cls, xgen_collection_file_path):
        """
        :param xgen_collection_file_path: str()
        :return:
        """
        file_opt = bsc_core.StgFileOpt(xgen_collection_file_path)
        file_name_base = file_opt.name_base
        return file_name_base.split('__')[-1]

    @classmethod
    def copy_xgen_collection_files_fnc(cls, file_path_src, file_path_tgt):
        """
        :param file_path_src: str("maya_scene_file_path")
        :param file_path_tgt:
        :return:
        """
        file_paths_src = cls._get_xgen_collection_file_paths_(file_path_src)
        file_opt_tgt = bsc_core.StgFileOpt(file_path_tgt)
        file_name_base_tgt = file_opt_tgt.name_base
        file_directory_path_tgt = file_opt_tgt.directory_path
        replace_list = []
        #
        for i_file_path_src in file_paths_src:
            i_file_opt_src = bsc_core.StgFileOpt(i_file_path_src)
            i_file_name_src = i_file_opt_src.name
            i_xgen_collection_name = cls._get_xgen_collection_name_(i_file_path_src)
            i_file_name_tgt = '{}__{}.xgen'.format(file_name_base_tgt, i_xgen_collection_name)
            i_xgen_collection_file_path_tgt = '{}/{}'.format(file_directory_path_tgt, i_file_name_tgt)
            utl_dcc_objects.OsFile(i_file_path_src).set_copy_to_file(i_xgen_collection_file_path_tgt)
            #
            cls._set_xgen_collection_file_repair_(i_xgen_collection_file_path_tgt)
            #
            replace_list.append(
                (i_file_name_src, i_file_name_tgt)
            )
        #
        if replace_list:
            if os.path.isfile(file_path_tgt):
                with open(file_path_tgt) as f_r:
                    d = f_r.read()
                    for i in replace_list:
                        s, t = i
                        d = d.replace(
                            r'setAttr ".xfn" -type "string" "{}";'.format(s),
                            r'setAttr ".xfn" -type "string" "{}";'.format(t)
                        )
                        d = d.replace(
                            r'"xgFileName" " -type \"string\" \"{}\""'.format(s),
                            r'"xgFileName" " -type \"string\" \"{}\""'.format(t)
                        )
                    with open(file_path_tgt, 'w') as f_w:
                        f_w.write(d)

    @classmethod
    def _set_xgen_collection_file_repath_(
            cls, xgen_collection_file_path, xgen_project_directory_path, xgen_collection_directory_path,
            xgen_collection_name
            ):
        dot_xgen_file_reader = utl_objects.DotXgenFileReader(xgen_collection_file_path)
        dot_xgen_file_reader.set_project_directory_repath(xgen_project_directory_path)
        dot_xgen_file_reader.set_collection_directory_repath(
            xgen_collection_directory_path, xgen_collection_name
        )
        #
        dot_xgen_file_reader.set_save()

    @classmethod
    def _set_xgen_collection_file_repair_(cls, xgen_collection_file_path):
        i_dot_xgen_reader = utl_objects.DotXgenFileReader(xgen_collection_file_path)
        i_dot_xgen_reader.set_repair()
        i_dot_xgen_reader.set_save()


class AbsUsdGeometryComparer(AbsFncOptionBase):
    OPTION = dict(
        file_src='',
        file_tgt='',
        location=''
    )
    FNC_DCC_MESH_MATCHER_CLS = None

    def __init__(self, option):
        super(AbsUsdGeometryComparer, self).__init__(option)

    @classmethod
    def _get_data_(cls, file_path, location):
        import lxusd.dcc.dcc_objects as usd_dcc_objects

        import lxusd.dcc.dcc_operators as usd_dcc_operators

        if file_path is not None:
            scene = usd_dcc_objects.Scene()
            scene.load_from_dot_usd(
                file_path,
                location
            )
            universe = scene.universe
            stage_opt = usd_dcc_operators.SceneOpt(scene.usd_stage, 'usd')
            comparer_data = stage_opt.get_mesh_comparer_data(
                file_path
            )
            #
            geometries = []
            mesh_type = universe.get_obj_type('Mesh')
            if mesh_type is not None:
                geometries = mesh_type.get_objs()
            #
            return geometries, comparer_data

    def __gain_data_fnc_(self, file_path, location):
        self._comparer_data.append(
            self._get_data_(file_path, location)
        )

    def __gain_result_fnc_(self):
        objs_src, data_src = self._comparer_data[0]
        objs_tgt, data_tgt = self._comparer_data[1]
        #
        if objs_src:
            with bsc_core.LogProcessContext.create(maximum=len(objs_src), label='comparer geometry by data') as g_p:
                for i_obj_src in objs_src:
                    if i_obj_src.type_name == 'Mesh':
                        i_path_src = i_obj_src.path

                        i_mesh_matcher = self.FNC_DCC_MESH_MATCHER_CLS(
                            i_path_src, data_src, data_tgt
                        )
                        i_path_tgt, i_check_statuses = i_mesh_matcher.get()

                        self._comparer_results.append(
                            (i_path_src, i_path_tgt, i_check_statuses)
                        )
                    #
                    g_p.set_update()
        # addition
        paths_src = [i.path for i in objs_src]
        paths_tgt = [i.path for i in objs_tgt]
        #
        path_addition = list(
            set(paths_tgt)-set(paths_src)
        )
        for i_path_tgt in path_addition:
            self._comparer_results.append(
                (i_path_tgt, i_path_tgt, utl_configure.DccMeshCheckStatus.ADDITION)
            )

    def __get_results_(self):
        self._comparer_data = []
        self._comparer_results = []
        #
        ms = [
            # gain source data
            (self.__gain_data_fnc_, (self.get('file_src'), self.get('location'))),
            # gain target data
            (self.__gain_data_fnc_, (self.get('file_tgt'), self.get('location'))),
            # comparer
            (self.__gain_result_fnc_, ())
        ]
        if ms:
            with bsc_core.LogProcessContext.create(maximum=len(ms), label='execute geometry-comparer method') as g_p:
                for i_method, i_args in ms:
                    g_p.set_update()
                    i_method(*i_args)
        return self._comparer_results

    def get_results(self, check_status_includes=None):
        results = self.__get_results_()
        if check_status_includes is not None:
            list_ = []
            for i_path_src, i_path_tgt, i_check_status in results:
                for j_e in check_status_includes:
                    if j_e in i_check_status:
                        list_.append(
                            (i_path_src, i_path_tgt, i_check_status)
                        )
            return list_
        return results


class AbsFncRenderTextureExportDef(object):
    KEY = 'texture export'

    @classmethod
    def copy_and_repath_as_base_link_fnc(
            cls,
            directory_path_bsc, directory_path_dst,
            #
            dcc_objs,
            # file name auto replace " " to "_"
            fix_name_blank,
            #
            with_reference=False,
            ignore_missing_texture=False,
            remove_expression=False,
            use_environ_map=False,
            repath_fnc=None,
            # copy option
            #   copy source file, etc. use ".tx", auto copy ".exr"
            copy_source=False,
            copy_source_scheme='separate',
            target_extension='.tx',
    ):
        if dcc_objs:
            copy_cache = []
            index_mapper = {}
            # use for file with same name, etc. "/temp/a/a.exr", "/temp/b/a.exr"
            index_query = {}
            with bsc_core.LogProcessContext.create_as_bar(maximum=len(dcc_objs), label=cls.KEY) as l_p:
                for i_dcc_obj in dcc_objs:
                    l_p.set_update()
                    # dpt to dst, file path can be is multiply
                    for j_port_path, j_texture_path_dpt in i_dcc_obj.reference_raw.items():
                        # map path to current platform
                        j_texture_path_dpt = utl_core.Path.map_to_current(j_texture_path_dpt)
                        j_texture_dpt = utl_dcc_objects.OsTexture(j_texture_path_dpt)
                        if j_texture_dpt.get_exists_unit_paths() is False:
                            bsc_core.Log.trace_method_warning(
                                cls.KEY,
                                'file="{}" is non exists'.format(j_texture_path_dpt)
                            )
                            continue
                        # fix name overlay
                        if j_texture_path_dpt in index_query:
                            j_index = index_query[j_texture_path_dpt]
                        else:
                            j_key = j_texture_dpt.name
                            if j_key in index_mapper:
                                j_index = index_mapper[j_key]+1
                            else:
                                j_index = 0
                            #
                            index_mapper[j_key] = j_index
                            index_query[j_texture_path_dpt] = j_index
                        #
                        index_mapper[j_key] = j_index
                        #
                        j_directory_path_dst = '{}/v{}'.format(directory_path_dst, j_index)
                        # get dst
                        if copy_source is True:
                            j_texture_path_dst_src, j_texture_path_dst_tgt = j_texture_dpt.get_target_file_path_as_src(
                                directory_path_dst=j_directory_path_dst,
                                #
                                scheme=copy_source_scheme,
                                target_extension=target_extension,
                                #
                                fix_name_blank=fix_name_blank
                            )
                            ext = j_texture_dpt.ext
                            if ext == target_extension:
                                j_texture_path_dst = j_texture_path_dst_tgt
                            else:
                                j_texture_path_dst = j_texture_path_dst_src
                        else:
                            j_texture_path_dst = j_texture_dpt.get_target_file_path(
                                j_directory_path_dst,
                                fix_name_blank=fix_name_blank
                            )
                        # ignore when dpt ( departure ) same to dst ( destination )
                        if j_texture_path_dpt != j_texture_path_dst:
                            # do copy
                            j_file_units_dpt = j_texture_dpt.get_exists_units()
                            if j_file_units_dpt:
                                for k_file_unit_dpt in j_file_units_dpt:
                                    k_file_tile_path = k_file_unit_dpt.path
                                    if k_file_tile_path not in copy_cache:
                                        copy_cache.append(k_file_tile_path)
                                        #
                                        if copy_source is True:
                                            k_file_unit_dpt.copy_unit_as_base_link_with_src(
                                                directory_path_bsc=directory_path_bsc,
                                                directory_path_dst=j_directory_path_dst,
                                                #
                                                scheme=copy_source_scheme,
                                                target_extension=target_extension,
                                                #
                                                fix_name_blank=fix_name_blank,
                                                replace=True
                                            )
                                        else:
                                            k_file_unit_dpt.copy_unit_as_base_link(
                                                directory_path_bsc=directory_path_bsc,
                                                directory_path_dst=j_directory_path_dst,
                                                #
                                                fix_name_blank=fix_name_blank,
                                                replace=True
                                            )
                            else:
                                bsc_core.Log.trace_method_warning(
                                    'texture search',
                                    u'file="{}" is Non-exists'.format(j_texture_path_dpt)
                                )
                                continue
                            # do repath
                            j_texture_dst = utl_dcc_objects.OsTexture(j_texture_path_dst)
                            if j_texture_dst.get_exists_units():
                                # environ map
                                if use_environ_map is True:
                                    # noinspection PyArgumentEqualDefault
                                    j_texture_path_dst_new = utl_core.PathEnv.map_to_env(
                                        j_texture_path_dst, pattern='[KEY]'
                                    )
                                    if j_texture_path_dst_new != j_texture_path_dst:
                                        j_texture_path_dst = j_texture_path_dst_new
                                #
                                repath_fnc(
                                    i_dcc_obj,
                                    j_port_path,
                                    j_texture_path_dst,
                                    remove_expression,
                                )
                                bsc_core.Log.trace_method_result(
                                    cls.KEY,
                                    u'"{}" >> "{}"'.format(j_texture_path_dpt, j_texture_path_dst)
                                )
                            else:
                                bsc_core.Log.trace_method_warning(
                                    cls.KEY,
                                    u'file="{}" is non-exists'.format(j_texture_path_dst)
                                )

    @classmethod
    def copy_and_repath_fnc(
            cls,
            directory_path_dst,
            #
            dcc_objs,
            # file name auto replace " " to "_"
            fix_name_blank,
            #
            with_reference=False,
            ignore_missing_texture=False,
            remove_expression=False,
            use_environ_map=False,
            repath_fnc=None,
            # copy option
            #   copy source file, etc. use ".tx", auto copy ".exr"
            copy_source=False,
            copy_source_scheme='separate',
            target_extension='.tx',
    ):
        copy_cache = []
        index_mapper = {}
        # use for file with same name, etc. "/temp/a/a.exr", "/temp/b/a.exr"
        index_query = {}
        with bsc_core.LogProcessContext.create_as_bar(maximum=len(dcc_objs), label=cls.KEY) as l_p:
            for i_dcc_obj in dcc_objs:
                l_p.set_update()
                # dpt to dst
                for j_port_path, j_texture_path_dpt in i_dcc_obj.reference_raw.items():
                    # map path to current platform
                    j_texture_path_dpt = utl_core.Path.map_to_current(j_texture_path_dpt)
                    j_texture_dpt = utl_dcc_objects.OsTexture(j_texture_path_dpt)
                    if j_texture_dpt.get_exists_units() is False:
                        bsc_core.Log.trace_method_warning(
                            cls.KEY,
                            'file="{}" is non exists'.format(j_texture_path_dpt)
                        )
                        continue
                    # fix name overlay
                    if j_texture_path_dpt in index_query:
                        j_index = index_query[j_texture_path_dpt]
                    else:
                        j_key = j_texture_dpt.name
                        if j_key in index_mapper:
                            j_index = index_mapper[j_key]+1
                        else:
                            j_index = 0
                        #
                        index_mapper[j_key] = j_index
                        index_query[j_texture_path_dpt] = j_index
                    #
                    index_mapper[j_key] = j_index
                    #
                    j_directory_path_dst = '{}/v{}'.format(directory_path_dst, j_index)
                    # get dst
                    if copy_source is True:
                        j_texture_path_dst_src, j_texture_path_dst_tgt = j_texture_dpt.get_target_file_path_as_src(
                            directory_path_dst=j_directory_path_dst,
                            #
                            scheme=copy_source_scheme,
                            target_extension=target_extension,
                            #
                            fix_name_blank=fix_name_blank
                        )
                        ext = j_texture_dpt.ext
                        if ext == target_extension:
                            j_texture_path_dst = j_texture_path_dst_tgt
                        else:
                            j_texture_path_dst = j_texture_path_dst_src
                    else:
                        j_texture_path_dst = j_texture_dpt.get_target_file_path(
                            j_directory_path_dst,
                            fix_name_blank=fix_name_blank
                        )
                    # ignore when dpt ( departure ) same to dst ( destination )
                    if j_texture_path_dpt != j_texture_path_dst:
                        # do copy
                        j_file_units_dpt = j_texture_dpt.get_exists_units()
                        if j_file_units_dpt:
                            for k_file_unit_dpt in j_file_units_dpt:
                                k_file_tile_path = k_file_unit_dpt.path
                                if k_file_tile_path not in copy_cache:
                                    copy_cache.append(k_file_tile_path)
                                    #
                                    if copy_source is True:
                                        k_file_unit_dpt.copy_unit_with_src(
                                            directory_path_dst=j_directory_path_dst,
                                            #
                                            scheme=copy_source_scheme,
                                            target_extension=target_extension,
                                            #
                                            fix_name_blank=fix_name_blank,
                                            replace=True
                                        )
                                    else:
                                        k_file_unit_dpt.copy_unit_to(
                                            directory_path_dst=j_directory_path_dst,
                                            #
                                            fix_name_blank=fix_name_blank,
                                            replace=True
                                        )
                        else:
                            bsc_core.Log.trace_method_warning(
                                'texture search',
                                u'file="{}" is Non-exists'.format(j_texture_path_dpt)
                            )
                            continue
                        # do repath
                        #
                        j_texture_dst = utl_dcc_objects.OsTexture(j_texture_path_dst)
                        if j_texture_dst.get_exists_units():
                            # environ map
                            if use_environ_map is True:
                                # noinspection PyArgumentEqualDefault
                                j_texture_path_dst_new = utl_core.PathEnv.map_to_env(
                                    j_texture_path_dst, pattern='[KEY]'
                                )
                                if j_texture_path_dst_new != j_texture_path_dst:
                                    j_texture_path_dst = j_texture_path_dst_new
                            #
                            repath_fnc(
                                i_dcc_obj,
                                j_port_path,
                                j_texture_path_dst,
                                remove_expression,
                            )
                            bsc_core.Log.trace_method_result(
                                'texture export',
                                u'"{}" >> "{}"'.format(j_texture_path_dpt, j_texture_path_dst)
                            )
                        else:
                            bsc_core.Log.trace_method_warning(
                                'texture export',
                                u'file="{}" is non-exists'.format(j_texture_path_dst)
                            )


if __name__ == '__main__':
    pass
