# coding:utf-8
import parse
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccValidationHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccValidationHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_shotgun_check(self, validator):
        import lxshotgun.objects as stg_objects
        #
        import lxshotgun.operators as stg_operators
        #
        check_group = 'Shotgun Check'
        #
        root = self._rsv_scene_properties.get('dcc.root')
        geometry_location = '/root/world/geo'
        #
        location = '{}{}'.format(geometry_location, root)
        #
        stg_connector = stg_objects.StgConnector()
        sgt_task_query = stg_connector.get_stg_task_query(**self._rsv_scene_properties.value)
        if sgt_task_query is not None:
            stg_task_opt = stg_operators.StgTaskOpt(sgt_task_query)
            status = stg_task_opt.get_stg_status()
            if status in ['omt', 'hld']:
                validator.set_obj_error_register(
                    location,
                    check_group=check_group,
                    check_status=validator.CheckStatus.Warning,
                    description='"shotgun-task" is "omit" or "hold"'
                )
        else:
            validator.set_obj_error_register(
                location,
                check_group=check_group,
                check_status=validator.CheckStatus.Warning,
                description='"shotgun-task" is "non-exists"'
            )

    def set_katana_geometry_topology_check(self, validator):
        from lxutil import utl_configure
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        import lxkatana.fnc.comparers as ktn_fnc_comparers
        #
        check_group = 'Geometry Topology Check'
        #
        root = self._rsv_scene_properties.get('dcc.root')
        sub_root = '{}/hi'.format(root)
        #
        geometry_location = '/root/world/geo'
        #
        location = '{}{}'.format(geometry_location, root)
        sub_location = '{}{}'.format(geometry_location, sub_root)
        #
        obj_scene = ktn_dcc_objects.Scene()
        obj_scene.set_load_by_root(
            ktn_obj='asset_geometries_merge',
            root=sub_location,
        )
        dcc_obj_universe = obj_scene.universe

        dcc_location = dcc_obj_universe.get_obj(location)
        if dcc_location is None:
            validator.set_obj_error_register(
                location,
                check_group=check_group,
                check_status=validator.CheckStatus.Warning,
                description='"asset root" "{}" is non-exists'.format(location)
            )
            return False
        #
        rsv_entity = self._rsv_task.get_rsv_entity()
        model_rsv_task = rsv_entity.get_rsv_task(
            step='mod', task='modeling'
        )
        model_geometry_usd_hi_file_rsv_unit = model_rsv_task.get_rsv_unit(
            keyword='asset-geometry-usd-hi-file'
        )
        latest_model_geometry_usd_hi_file_path = model_geometry_usd_hi_file_rsv_unit.get_result(
            version='latest', extend_variants=dict(var='hi')
        )
        if latest_model_geometry_usd_hi_file_path is None:
            validator.set_obj_error_register(
                location,
                check_group=check_group,
                check_status=validator.CheckStatus.Warning,
                description='"geometry usd-file" from "model" is non-exists'
            )
            return False
        #
        katana_workspace = ktn_dcc_objects.AssetWorkspace()
        scene_file_path = ktn_dcc_objects.Scene.get_current_file_path()
        scene_usd_file_path = katana_workspace.get_geometry_uv_map_usd_source_file()
        if scene_usd_file_path is None:
            validator.set_obj_error_register(
                location,
                check_group=check_group,
                check_status=validator.CheckStatus.Warning,
                description='"geometry usd-file for uv-map" from "scene" is non-exists'
            )
            return False
        #
        fnc_geometry_comparer = ktn_fnc_comparers.GeometryComparer(
            scene_file_path, sub_root
        )
        warning_es = [
            utl_configure.DccMeshCheckStatus.ADDITION,
            utl_configure.DccMeshCheckStatus.DELETION,
            utl_configure.DccMeshCheckStatus.PATH_CHANGED,
            utl_configure.DccMeshCheckStatus.PATH_EXCHANGED,
        ]
        error_ds = [
            utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED,
        ]
        results = fnc_geometry_comparer.get_results()
        for i_src_gmt_path, i_tgt_gmt_path, i_description in results:
            obj_path = '{}{}'.format(location, i_src_gmt_path)
            for j_e in warning_es:
                if j_e in i_description:
                    validator.set_obj_error_register(
                        obj_path,
                        check_group=check_group,
                        check_status=validator.CheckStatus.Warning,
                        description='"mesh" is "{}"'.format(i_description)
                    )
            #
            for j_e in error_ds:
                if j_e in i_description:
                    validator.set_obj_error_register(
                        obj_path,
                        check_group=check_group,
                        check_status=validator.CheckStatus.Error,
                        description='"mesh" is "{}"'.format(i_description)
                    )

    def set_katana_geometry_uv_map_check(self, validator):
        from lxusd import usd_configure, usd_core
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects

        check_group = 'Geometry UV-map Check'
        #
        root = self._rsv_scene_properties.get('dcc.root')
        sub_root = '{}/hi'.format(root)
        #
        geometry_location = '/root/world/geo'
        #
        location = '{}{}'.format(geometry_location, root)
        sub_location = '{}{}'.format(geometry_location, sub_root)
        #
        katana_workspace = ktn_dcc_objects.AssetWorkspace()
        scene_usd_file_path = katana_workspace.get_geometry_uv_map_usd_source_file()
        if scene_usd_file_path is None:
            validator.set_obj_error_register(
                location,
                check_group=check_group,
                check_status=validator.CheckStatus.Warning,
                description='"geometry usd-file for uv-map" from "scene" is non-exists'
            )
            return False

        s = usd_core.UsdStageOpt(scene_usd_file_path)
        for i_usd_prim in s.usd_instance.TraverseAll():
            i_usd_prim_type_name = i_usd_prim.GetTypeName()
            if i_usd_prim_type_name == usd_configure.ObjType.MESH:
                i_mesh_opt = usd_core.UsdGeometryMeshOpt(i_usd_prim)
                i_uv_map_names = i_mesh_opt.get_uv_map_names()
                i_mesh_location = '{}/{}'.format(geometry_location, i_mesh_opt.get_path())
                if not 'st' in i_uv_map_names:
                    validator.set_obj_error_register(
                        i_mesh_location,
                        check_group=check_group,
                        check_status=validator.CheckStatus.Warning,
                        description='"mesh default uv-map name" "map1 / st" is non-exists'
                    )

                i_face_vertex_indices = i_mesh_opt.get_face_vertex_indices()
                j_uv_map_names_warning = []
                j_uv_map_names_error = []
                for j_uv_map_name in i_uv_map_names:
                    j_uv_map_indices = i_mesh_opt.get_uv_map_indices(j_uv_map_name)
                    if j_uv_map_indices:
                        if len(i_face_vertex_indices) != len(j_uv_map_indices):
                            j_uv_map_names_error.append(j_uv_map_name)
                    else:
                        j_uv_map_names_warning.append(j_uv_map_name)
                #
                if j_uv_map_names_warning:
                    validator.set_obj_error_register(
                        i_mesh_location,
                        check_group=check_group,
                        check_status=validator.CheckStatus.Warning,
                        description='"mesh uv-map" in "{}" is empty'.format(
                            ', '.join(map(lambda x: '"{}"'.format(x), j_uv_map_names_warning))
                        )
                    )
                #
                if j_uv_map_names_error:
                    validator.set_obj_error_register(
                        i_mesh_location,
                        check_group=check_group,
                        check_status=validator.CheckStatus.Error,
                        description='"mesh uv-map" in "{}" has non-data vertices'.format(
                            ', '.join(map(lambda x: '"{}"'.format(x), j_uv_map_names_error))
                        )
                    )

    def set_katana_texture_check(self, validator):
        from lxbasic import bsc_core
        #
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        from lxutil import utl_core

        root = self._rsv_scene_properties.get('dcc.root')

        check_group = 'Texture Check'
        #
        dcc_texture_references = ktn_dcc_objects.TextureReferences()
        location = root
        dcc_workspace = ktn_dcc_objects.AssetWorkspace()
        dcc_shaders = dcc_workspace.get_all_dcc_geometry_shader_by_location(location)
        dcc_objs = dcc_texture_references.get_objs(
            include_paths=[i.path for i in dcc_shaders]
        )
        if dcc_objs:
            check_dict = {}
            with utl_core.gui_progress(maximum=len(dcc_objs)) as g_p:
                for i_obj in dcc_objs:
                    g_p.set_update()
                    #
                    file_paths_0 = []
                    file_paths_1 = []
                    file_paths_2 = []
                    file_paths_3 = []
                    file_paths_4 = []
                    file_paths_5 = []
                    i_check_results = [
                        file_paths_0, file_paths_1, file_paths_2, file_paths_3, file_paths_4, file_paths_5
                    ]
                    for j_port_path, j_file_path in i_obj.reference_raw.items():
                        j_texture = utl_dcc_objects.OsTexture(j_file_path)
                        j_texture_tiles = j_texture.get_exists_files_()
                        if j_file_path in check_dict:
                            j_check_results = check_dict[j_file_path]
                        else:
                            j_check_results = [True]*6
                            check_dict[j_file_path] = j_check_results
                            # check exists
                            if not j_texture_tiles:
                                j_check_results[0] = False
                            else:
                                if j_texture.get_ext_is_tx() is False:
                                    j_check_results[1] = False
                                #
                                if j_texture.get_is_exists_as_tx() is False:
                                    j_check_results[2] = False
                                #
                                if bsc_core.TextOpt(j_file_path).get_is_contain_chinese() is True:
                                    j_check_results[3] = False
                                #
                                if bsc_core.TextOpt(j_file_path).get_is_contain_space() is True:
                                    j_check_results[4] = False
                                #
                                if bsc_core.SystemMtd.get_is_linux():
                                    if not j_texture.path.startswith('/l'):
                                        j_check_results[5] = False
                                elif bsc_core.SystemMtd.get_is_windows():
                                    if not j_texture.path.lower().startswith('l:'):
                                        j_check_results[5] = False
                        #
                        for index, k_check_result in enumerate(j_check_results):
                            if k_check_result is False:
                                i_check_results[index].append(j_file_path)
                    #
                    if file_paths_0:
                        validator.set_obj_files_error_register(
                            i_obj.path,
                            file_paths=file_paths_0,
                            description='"texture" is "non-exists"',
                            check_group=check_group,
                            check_status=validator.CheckStatus.Warning
                        )
                    #
                    if file_paths_1:
                        validator.set_obj_files_error_register(
                            i_obj.path,
                            file_paths=file_paths_1,
                            description='"node" is not path to "texture-tx"',
                            check_group=check_group,
                            check_status=validator.CheckStatus.Warning
                        )
                    #
                    if file_paths_2:
                        validator.set_obj_files_error_register(
                            i_obj.path,
                            file_paths=file_paths_2,
                            description='"texture-tx" is "changed / non-exists"',
                            check_group=check_group,
                            check_status=validator.CheckStatus.Warning
                        )
                    #
                    if file_paths_3:
                        validator.set_obj_files_error_register(
                            i_obj.path,
                            file_paths=file_paths_3,
                            description='"texture-path / name" is contain "chinese"',
                            check_group=check_group,
                            check_status=validator.CheckStatus.Warning
                        )
                    #
                    if file_paths_4:
                        validator.set_obj_files_error_register(
                            i_obj.path,
                            file_paths=file_paths_4,
                            description='"texture-path / name" is contain "space"',
                            check_group=check_group,
                            check_status=validator.CheckStatus.Warning
                        )
                    #
                    if file_paths_5:
                        validator.set_obj_files_error_register(
                            i_obj.path,
                            file_paths=file_paths_4,
                            description='"texture-root" must be "/l" or "l:"',
                            check_group=check_group,
                            check_status=validator.CheckStatus.Error
                        )

    def set_katana_texture_workspace_check(self, validator):
        from lxbasic import bsc_core
        #
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        from lxutil import utl_core

        root = self._rsv_scene_properties.get('dcc.root')

        rsv_project = self._rsv_task.get_rsv_project()

        ks = [
            'asset-work-texture-src-dir',
            'asset-work-texture-tx-dir'
        ]

        check_p_opt_list = []
        for i_k in ks:
            i_p = rsv_project.get_pattern(
                i_k
            )
            i_check_p = i_p + '/{extra}'
            i_check_p_opt = bsc_core.ParsePatternOpt(
                i_check_p
            )
            i_check_p_opt.set_update(
                **dict(root=rsv_project.get('root'))
            )
            check_p_opt_list.append(i_check_p_opt)

        check_group = 'Texture Workspace Check'
        #
        dcc_texture_references = ktn_dcc_objects.TextureReferences()
        location = root

        dcc_workspace = ktn_dcc_objects.AssetWorkspace()
        dcc_shaders = dcc_workspace.get_all_dcc_geometry_shader_by_location(location)
        dcc_objs = dcc_texture_references.get_objs(
            include_paths=[i.path for i in dcc_shaders]
        )
        if dcc_objs:
            check_dict = {}
            with utl_core.gui_progress(maximum=len(dcc_objs)) as g_p:
                for i_obj in dcc_objs:
                    g_p.set_update()
                    #
                    file_paths_0 = []
                    i_check_results = [
                        file_paths_0
                    ]
                    for j_port_path, j_file_path in i_obj.reference_raw.items():
                        j_texture = utl_dcc_objects.OsTexture(j_file_path)
                        j_texture_tiles = j_texture.get_exists_files_()
                        if j_file_path in check_dict:
                            j_check_results = check_dict[j_file_path]
                        else:
                            j_check_results = [True] * 5
                            check_dict[j_file_path] = j_check_results
                            if j_texture_tiles:
                                is_passed = False
                                for i_check_p_opt in check_p_opt_list:
                                    if i_check_p_opt.get_variants(j_file_path):
                                        is_passed = True
                                        break
                                #
                                if is_passed is False:
                                    j_check_results[0] = False
                        #
                        for index, k_check_result in enumerate(j_check_results):
                            if k_check_result is False:
                                i_check_results[index].append(j_file_path)
                    #
                    if file_paths_0:
                        validator.set_obj_files_error_register(
                            i_obj.path,
                            file_paths=file_paths_0,
                            description='"texture" is not in "workspace"',
                            check_group=check_group,
                            check_status=validator.CheckStatus.Warning
                        )

    def set_katana_scene_check(self, validator):
        def yes_fnc_():
            ktn_dcc_objects.Scene.set_file_save()
        #
        from lxutil import utl_core

        from lxkatana import ktn_core
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects

        from lxutil_gui.qt import utl_gui_qt_core
        #
        check_group = 'Scene Check'
        #
        root = self._rsv_scene_properties.get('dcc.root')
        geometry_location = '/root/world/geo'
        #
        location = '{}{}'.format(geometry_location, root)
        #
        if ktn_core._get_is_ui_mode_() is True:
            file_path = ktn_dcc_objects.Scene.get_current_file_path()
            if ktn_dcc_objects.Scene.get_scene_is_dirty():
                w = utl_core.DialogWindow.set_create(
                    label='Save',
                    content=u'Scene has been modified, Do you want to save changed to "{}"'.format(
                        ktn_dcc_objects.Scene.get_current_file_path()
                    ),
                    window_size=(480, 160),
                    #
                    yes_method=yes_fnc_,
                    #
                    yes_label='Save',
                    no_label='Don\'t save',
                    #
                    status=utl_core.DialogWindow.ValidatorStatus.Warning,
                    #
                    parent=utl_gui_qt_core.QtDccMtd.get_active_window()
                )
                #
                if not w.get_result():
                    validator.set_obj_files_error_register(
                        location,
                        [file_path],
                        description=u'scene has modifier to save',
                        check_group=check_group,
                        check_status=validator.CheckStatus.Error,
                    )
