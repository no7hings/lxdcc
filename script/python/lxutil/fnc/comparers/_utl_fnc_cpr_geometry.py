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
    def __init__(self, *args, **kwargs):
        super(GeometryComparer, self).__init__(*args, **kwargs)

    def _set_scene_dcc_objs_update_(self):
        import lxusd.dcc.dcc_objects as usd_dcc_objects
        #
        import lxusd.dcc.dcc_operators as usd_dcc_operators
        #
        import lxresolver.operators as rsv_operators
        #
        asset_query = rsv_operators.RsvAssetGeometryQuery(self._task_properties)
        geometry_usd_hi_file_path = asset_query.get_usd_hi_file()
        if geometry_usd_hi_file_path is not None:
            root = self._root
            #
            self._scene_dcc_obj_scene = usd_dcc_objects.Scene()
            self._scene_dcc_obj_scene.set_load_from_dot_usd(geometry_usd_hi_file_path, root)
            self._scene_dcc_obj_universe = self._scene_dcc_obj_scene.universe
            self._scene_usd_scene_opt = usd_dcc_operators.SceneOpt(self._scene_dcc_obj_scene.usd_stage)
            self._scene_dcc_mesh_comparer_data = self._scene_usd_scene_opt.get_mesh_comparer_data(geometry_usd_hi_file_path)
            self._scene_dcc_geometries = []
            mesh_type = self._scene_dcc_obj_universe.get_obj_type('Mesh')
            if mesh_type is not None:
                self._scene_dcc_geometries = mesh_type.get_objs()
