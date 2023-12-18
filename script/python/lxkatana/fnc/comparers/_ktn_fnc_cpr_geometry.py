# coding:utf-8
from lxutil.fnc import utl_fnc_obj_abs


class FncDccMeshMatcher(utl_fnc_obj_abs.AbsFncDccMeshMatcher):
    FNC_DCC_MESH_CLS = None
    def __init__(self, *args, **kwargs):
        super(FncDccMeshMatcher, self).__init__(*args, **kwargs)


class FncGeometryComparer(utl_fnc_obj_abs.AbsFncDccGeometryComparer):
    DCC_SCENE_CLS = None
    DCC_SCENE_OPT_CLS = None
    #
    FNC_DCC_MESH_MATCHER_CLS = FncDccMeshMatcher
    FNC_USD_MESH_REPAIRER_CLS = None
    #
    RSV_KEYWORD = 'asset-geometry-usd-payload-file'
    DCC_NAMESPACE = 'usd'
    def __init__(self, *args):
        super(FncGeometryComparer, self).__init__(*args)

    def update_target_fnc(self):
        import lxbasic.core as bsc_core

        import lxkatana.core as ktn_core

        import lxusd.dcc.dcc_objects as usd_dcc_objects
        #
        import lxusd.dcc.dcc_operators as usd_dcc_operators

        import lxkatana.scripts as ktn_scripts
        #
        w_s = ktn_core.WorkspaceSetting()
        opt = w_s.get_current_look_output_opt_force()
        if opt is None:
            return False
        #
        s = ktn_scripts.ScpLookOutput(opt)
        #
        usd_file_path = s.get_geometry_uv_map_usd_source_file()
        if usd_file_path is not None:
            location = self._location
            #
            time_tag = bsc_core.StgFileOpt(usd_file_path).get_modify_time_tag()
            #
            self._dcc_scene_tgt = usd_dcc_objects.Scene()
            if time_tag in utl_fnc_obj_abs.AbsFncDccGeometryComparer.CACHE:
                self._dcc_universe_tgt = utl_fnc_obj_abs.AbsFncDccGeometryComparer.CACHE[time_tag]
            else:
                self._dcc_scene_tgt.load_from_dot_usd(usd_file_path, location)
                self._dcc_universe_tgt = self._dcc_scene_tgt.universe
                utl_fnc_obj_abs.AbsFncDccGeometryComparer.CACHE[time_tag] = self._dcc_universe_tgt
            #
            self._scene_usd_scene_opt = usd_dcc_operators.SceneOpt(self._dcc_scene_tgt.usd_stage, self.DCC_NAMESPACE)
            self._dcc_comparer_data_tgt = self._scene_usd_scene_opt.get_mesh_comparer_data(usd_file_path)
            self._dcc_geometries_tgt = []
            mesh_type = self._dcc_universe_tgt.get_obj_type('Mesh')
            if mesh_type is not None:
                self._dcc_geometries_tgt = mesh_type.get_objs()
