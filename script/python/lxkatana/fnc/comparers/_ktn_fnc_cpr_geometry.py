# coding:utf-8
from lxutil.fnc import utl_fnc_obj_abs


class FncDccMeshMatcher(utl_fnc_obj_abs.AbsFncDccMeshMatcher):
    FNC_DCC_MESH_CLASS = None
    def __init__(self, *args, **kwargs):
        super(FncDccMeshMatcher, self).__init__(*args, **kwargs)


class GeometryComparer(utl_fnc_obj_abs.AbsFncDccGeometryComparer):
    DCC_SCENE_CLASS = None
    DCC_SCENE_OPT_CLASS = None
    #
    FNC_DCC_MESH_MATCHER_CLASS = FncDccMeshMatcher
    FNC_USD_MESH_REPAIRER_CLASS = None
    #
    def __init__(self, *args):
        super(GeometryComparer, self).__init__(*args)

    def _set_scene_dcc_objs_update_(self):
        from lxbasic import bsc_core

        from lxkatana import ktn_core

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
            root = self._root
            #
            time_tag = bsc_core.StgFileOpt(usd_file_path).get_modify_time_tag()
            #
            self._scene_dcc_obj_scene = usd_dcc_objects.Scene()
            if time_tag in utl_fnc_obj_abs.AbsFncDccGeometryComparer.CACHE:
                self._scene_dcc_obj_universe = utl_fnc_obj_abs.AbsFncDccGeometryComparer.CACHE[time_tag]
            else:
                self._scene_dcc_obj_scene.set_load_from_dot_usd(usd_file_path, root)
                self._scene_dcc_obj_universe = self._scene_dcc_obj_scene.universe
                utl_fnc_obj_abs.AbsFncDccGeometryComparer.CACHE[time_tag] = self._scene_dcc_obj_universe
            #
            self._scene_usd_scene_opt = usd_dcc_operators.SceneOpt(self._scene_dcc_obj_scene.usd_stage)
            self._scene_dcc_mesh_comparer_data = self._scene_usd_scene_opt.get_mesh_comparer_data(usd_file_path)
            self._scene_dcc_geometries = []
            mesh_type = self._scene_dcc_obj_universe.get_obj_type('Mesh')
            if mesh_type is not None:
                self._scene_dcc_geometries = mesh_type.get_objs()
