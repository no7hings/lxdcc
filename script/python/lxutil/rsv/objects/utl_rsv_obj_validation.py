# coding:utf-8
import parse
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccValidationHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccValidationHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)
    @classmethod
    def _set_dcc_texture_check_(cls, validation_checker, check_group, dcc_objs):
        from lxbasic import bsc_core
        #
        from lxutil import utl_core
        #
        import lxutil.dcc.dcc_objects as utl_dcc_objects

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
                        j_check_results = [True] * 6
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
                    validation_checker.set_node_files_result_register(
                        i_obj.path,
                        file_paths_0,
                        description='"texture" is "non-exists"',
                        check_group=check_group,
                        check_status=validation_checker.CheckStatus.Warning
                    )
                #
                if file_paths_1:
                    validation_checker.set_node_files_result_register(
                        i_obj.path,
                        file_paths_1,
                        description='"node" is not path to "texture-tx"',
                        check_group=check_group,
                        check_status=validation_checker.CheckStatus.Warning
                    )
                #
                if file_paths_2:
                    validation_checker.set_node_files_result_register(
                        i_obj.path,
                        file_paths_2,
                        description='"texture-tx" is "changed / non-exists"',
                        check_group=check_group,
                        check_status=validation_checker.CheckStatus.Warning
                    )
                #
                if file_paths_3:
                    validation_checker.set_node_files_result_register(
                        i_obj.path,
                        file_paths_3,
                        description='"texture-path / name" is contain "chinese"',
                        check_group=check_group,
                        check_status=validation_checker.CheckStatus.Warning
                    )
                #
                if file_paths_4:
                    validation_checker.set_node_files_result_register(
                        i_obj.path,
                        file_paths_4,
                        description='"texture-path / name" is contain "space"',
                        check_group=check_group,
                        check_status=validation_checker.CheckStatus.Warning
                    )
                #
                if file_paths_5:
                    validation_checker.set_node_files_result_register(
                        i_obj.path,
                        file_paths_5,
                        description='"texture-root" must be "/l" or "l:"',
                        check_group=check_group,
                        check_status=validation_checker.CheckStatus.Error
                    )

    def _set_dcc_texture_workspace_check_(self, validation_checker, check_group, dcc_objs):
        from lxbasic import bsc_core

        from lxutil import utl_core
        #
        import lxutil.dcc.dcc_objects as utl_dcc_objects

        rsv_project = self._rsv_task.get_rsv_project()

        file_keywords = [
            'asset-work-texture-src-dir',
            'asset-work-texture-tx-dir'
        ]

        check_pattern_opts = []
        for i_k in file_keywords:
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
            check_pattern_opts.append(i_check_p_opt)

        check_dict = {}
        with utl_core.gui_progress(maximum=len(dcc_objs)) as g_p:
            for i_obj in dcc_objs:
                g_p.set_update()
                #
                file_paths_0 = []
                file_paths_1 = []
                i_check_results = [
                    file_paths_0, file_paths_1
                ]
                for j_port_path, j_file_path in i_obj.reference_raw.items():
                    j_texture = utl_dcc_objects.OsTexture(j_file_path)
                    j_texture_tiles = j_texture.get_exists_files_()
                    if j_file_path in check_dict:
                        j_check_results = check_dict[j_file_path]
                    else:
                        j_check_results = [True] * 2
                        check_dict[j_file_path] = j_check_results
                        if j_texture_tiles:
                            is_passed = False
                            for i_check_p_opt in check_pattern_opts:
                                if i_check_p_opt.get_variants(j_file_path) is not None:
                                    is_passed = True
                                    break
                            #
                            if is_passed is False:
                                j_check_results[0] = False
                            else:
                                if j_texture.get_is_writeable() is True:
                                    j_check_results[1] = False
                    #
                    for index, k_check_result in enumerate(j_check_results):
                        if k_check_result is False:
                            i_check_results[index].append(j_file_path)
                #
                if file_paths_0:
                    validation_checker.set_node_files_result_register(
                        i_obj.path,
                        file_paths_0,
                        description='"texture" is not in "workspace"',
                        check_group=check_group,
                        check_status=validation_checker.CheckStatus.Warning
                    )
                if file_paths_1:
                    validation_checker.set_node_files_result_register(
                        i_obj.path,
                        file_paths_1,
                        description='"texture" in "workspace" is not "locked"',
                        check_group=check_group,
                        check_status=validation_checker.CheckStatus.Warning
                    )

    def set_shotgun_check(self, validation_checker):
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
                validation_checker.set_node_result_register(
                    location,
                    check_group=check_group,
                    check_status=validation_checker.CheckStatus.Warning,
                    description='"shotgun-task" is "omit" or "hold"'
                )
        else:
            validation_checker.set_node_result_register(
                location,
                check_group=check_group,
                check_status=validation_checker.CheckStatus.Warning,
                description='"shotgun-task" is "non-exists"'
            )
    # maya
    def set_maya_scene_check(self, validation_checker):
        def yes_fnc_():
            mya_dcc_objects.Scene.set_file_save()

        from lxbasic import bsc_core
        #
        from lxutil import utl_core

        from lxmaya import ma_core
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects

        from lxutil_gui.qt import utl_gui_qt_core
        #
        check_group = 'Scene Check'
        #
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')
        #
        location = bsc_core.DccPathDagOpt(root).set_translate_to(pathsep).to_string()
        #
        if ma_core._get_is_ui_mode_() is True:
            file_path = mya_dcc_objects.Scene.get_current_file_path()
            if mya_dcc_objects.Scene.get_scene_is_dirty():
                w = utl_core.DialogWindow.set_create(
                    label='Save',
                    content=u'scene has been modified, do you want to save changed to "{}"'.format(
                        mya_dcc_objects.Scene.get_current_file_path()
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
                    validation_checker.set_node_files_result_register(
                        location,
                        [file_path],
                        description=u'scene has modifier to save...',
                        check_group=check_group,
                        check_status=validation_checker.CheckStatus.Warning,
                    )

    def set_maya_geometry_check(self, validation_checker):
        from lxbasic import bsc_core

        from lxutil import utl_core
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects

        import lxmaya.dcc.dcc_operators as mya_dcc_operators
        #
        check_group = 'Geometry Check'
        #
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')
        #
        location = bsc_core.DccPathDagOpt(root).set_translate_to(pathsep).to_string()
        #
        dcc_location = mya_dcc_objects.Group(location)
        #
        sub_location = '{}|hi'.format(location)
        sub_dc_location = mya_dcc_objects.Group(sub_location)
        #
        if sub_dc_location.get_is_exists() is False:
            validation_checker.set_node_result_register(
                sub_location,
                check_group=check_group,
                check_status=validation_checker.CheckStatus.Warning,
                description='"asset sub root" "{}" is non-exists'.format(sub_location)
            )
            return False

        geometry_paths = sub_dc_location.get_all_shape_paths(include_obj_type=['mesh'])
        if geometry_paths:
            with utl_core.gui_progress(maximum=len(geometry_paths)) as g_p:
                for seq, i_geometry_path in enumerate(geometry_paths):
                    g_p.set_update()
                    #
                    i_mesh = mya_dcc_objects.Mesh(i_geometry_path)
                    i_mesh_opt = mya_dcc_operators.MeshOpt(i_mesh)
                    i_mesh_location = i_mesh.path
                    i_uv_map_names = i_mesh_opt.get_uv_map_names()
                    if not 'map1' in i_uv_map_names:
                        validation_checker.set_node_result_register(
                            i_mesh_location,
                            check_group=check_group,
                            check_status=validation_checker.CheckStatus.Warning,
                            description='"mesh default uv-map name" "map1" is non-exists'
                        )
                    else:
                        index = i_mesh_opt.get_default_uv_map_index()
                        if index > 0:
                            validation_checker.set_node_result_register(
                                i_mesh_location,
                                check_group=check_group,
                                check_status=validation_checker.CheckStatus.Warning,
                                description='"mesh default uv-map name" "map1" is not first index'
                            )
                    #
                    i_face_vertex_indices = i_mesh_opt.get_face_vertex_indices()
                    for j_uv_map_name in i_uv_map_names:
                        j_uv_map_face_vertex_indices = i_mesh_opt.get_uv_map_face_vertex_indices(j_uv_map_name)
                        if j_uv_map_face_vertex_indices:
                            if len(i_face_vertex_indices) != len(j_uv_map_face_vertex_indices):
                                j_uv_map_error_comps = i_mesh_opt.get_uv_map_error_comp_names(j_uv_map_name)
                                if j_uv_map_error_comps:
                                    validation_checker.set_node_components_result_register(
                                        i_mesh_location,
                                        ['{}.{}'.format(i_geometry_path, i) for i in j_uv_map_error_comps],
                                        check_group=check_group,
                                        check_status=validation_checker.CheckStatus.Error,
                                        description='"mesh uv-map" in "{}" has non-data vertices'.format(j_uv_map_name)
                                    )
                        else:
                            validation_checker.set_node_result_register(
                                i_mesh_location,
                                check_group=check_group,
                                check_status=validation_checker.CheckStatus.Warning,
                                description='"mesh uv-map" in "{}" is non-data'.format(j_uv_map_name)
                            )

    def set_maya_geometry_topology_check(self, validation_checker):
        from lxbasic import bsc_core
        #
        from lxutil import utl_configure
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        import lxmaya.fnc.comparers as mya_fnc_comparers
        #
        check_group = 'Geometry Topology Check'
        #
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')
        #
        location = bsc_core.DccPathDagOpt(root).set_translate_to(pathsep).to_string()
        #
        dcc_location = mya_dcc_objects.Node(location)
        # use utility pathsep
        sub_location = '{}/hi'.format(root)
        #
        if dcc_location.get_is_exists() is False:
            validation_checker.set_node_result_register(
                location,
                check_group=check_group,
                check_status=validation_checker.CheckStatus.Warning,
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
            validation_checker.set_node_result_register(
                location,
                check_group=check_group,
                check_status=validation_checker.CheckStatus.Warning,
                description='"geometry usd-file" from "model" is non-exists'
            )
            return False
        #
        work_scene_src_file_path = mya_dcc_objects.Scene.get_current_file_path()
        fnc_geometry_comparer = mya_fnc_comparers.GeometryComparer(
            work_scene_src_file_path, sub_location
        )
        fnc_geometry_comparer._set_model_geometry_usd_hi_file_path_(
            latest_model_geometry_usd_hi_file_path
        )
        warning_es = [
            utl_configure.DccMeshCheckStatus.ADDITION,
            utl_configure.DccMeshCheckStatus.DELETION,
            utl_configure.DccMeshCheckStatus.PATH_CHANGED,
        ]
        error_ds = [
            utl_configure.DccMeshCheckStatus.PATH_EXCHANGED,
            utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED,
        ]
        results = fnc_geometry_comparer.get_results()
        for i_src_gmt_path, i_tgt_gmt_path, i_description in results:
            i_dcc_path = bsc_core.DccPathDagOpt(i_src_gmt_path).set_translate_to(pathsep).to_string()
            for j_e in warning_es:
                if j_e in i_description:
                    validation_checker.set_node_result_register(
                        i_dcc_path,
                        check_group=check_group,
                        check_status=validation_checker.CheckStatus.Warning,
                        description='"mesh" is "{}"'.format(i_description)
                    )
            #
            for j_e in error_ds:
                if j_e in i_description:
                    validation_checker.set_node_result_register(
                        i_dcc_path,
                        check_group=check_group,
                        check_status=validation_checker.CheckStatus.Error,
                        description='"mesh" is "{}"'.format(i_description)
                    )

    def set_maya_look_check(self, validation_checker):
        from lxbasic import bsc_core

        from lxutil import utl_core
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects

        import lxmaya.dcc.dcc_operators as mya_dcc_operators
        #
        check_group = 'Look Check'
        #
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')
        #
        location = bsc_core.DccPathDagOpt(root).set_translate_to(pathsep).to_string()
        #
        dcc_location = mya_dcc_objects.Group(location)
        #
        sub_location = '{}|hi'.format(location)
        sub_dcc_location = mya_dcc_objects.Group(sub_location)
        if sub_dcc_location.get_is_exists() is False:
            validation_checker.set_node_result_register(
                sub_location,
                check_group=check_group,
                check_status=validation_checker.CheckStatus.Warning,
                description='"asset sub root" "{}" is non-exists'.format(sub_location)
            )
            return False

        geometry_paths = sub_dcc_location.get_all_shape_paths(include_obj_type=['mesh'])
        if geometry_paths:
            with utl_core.gui_progress(maximum=len(geometry_paths)) as g_p:
                for seq, i_geometry_path in enumerate(geometry_paths):
                    g_p.set_update()
                    #
                    i_mesh = mya_dcc_objects.Mesh(i_geometry_path)
                    i_mesh_location = i_mesh.path
                    #
                    look_obj_opt = mya_dcc_operators.MeshLookOpt(i_mesh)
                    i_components = look_obj_opt.get_face_assign_comp_names()
                    if i_components:
                        validation_checker.set_node_components_result_register(
                            i_mesh_location,
                            ['{}.{}'.format(i_geometry_path, i) for i in i_components],
                            check_group=check_group,
                            check_status=validation_checker.CheckStatus.Error,
                            description='"mesh" "material-assign" has components (faces ) '
                        )

    def set_maya_texture_check(self, validation_checker):
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        import lxmaya.dcc.dcc_operators as mya_dcc_operators
        #
        from lxbasic import bsc_core

        check_group = 'Texture Check'
        #
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')
        #
        location = bsc_core.DccPathDagOpt(root).set_translate_to(pathsep).to_string()
        dcc_location = mya_dcc_objects.Group(location)
        #
        sub_location = '{}|hi'.format(location)
        sub_dcc_location = mya_dcc_objects.Group(sub_location)
        #
        if sub_dcc_location.get_is_exists() is True:
            objs = sub_dcc_location.get_descendants()
            #
            objs_look_opt = mya_dcc_operators.ObjsLookOpt(objs)
            includes = objs_look_opt.get_texture_reference_paths()
            #
            if includes:
                dcc_objs = mya_dcc_objects.TextureReferences._get_objs_(includes)
                self._set_dcc_texture_check_(validation_checker, check_group, dcc_objs)

    def set_maya_texture_workspace_check(self, validation_checker):
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        import lxmaya.dcc.dcc_operators as mya_dcc_operators
        #
        from lxbasic import bsc_core

        check_group = 'Texture Workspace Check'
        #
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')
        #
        location = bsc_core.DccPathDagOpt(root).set_translate_to(pathsep).to_string()
        dcc_location = mya_dcc_objects.Group(location)
        #
        sub_location = '{}|hi'.format(location)
        sub_dcc_location = mya_dcc_objects.Group(sub_location)
        #
        if sub_dcc_location.get_is_exists() is True:
            objs = sub_dcc_location.get_descendants()
            #
            objs_look_opt = mya_dcc_operators.ObjsLookOpt(objs)
            includes = objs_look_opt.get_texture_reference_paths()
            #
            if includes:
                dcc_objs = mya_dcc_objects.TextureReferences._get_objs_(includes)
                self._set_dcc_texture_workspace_check_(
                    validation_checker, check_group,
                    dcc_objs
                )
    # katana
    def set_katana_scene_check(self, validation_checker):
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
        ktn_workspace = ktn_dcc_objects.AssetWorkspace()
        geometry_scheme = ktn_workspace.get_geometry_scheme()
        geometry_location = '/root/world/geo'
        if geometry_scheme == 'asset':
            root = self._rsv_scene_properties.get('dcc.root')
            location = '{}{}'.format(geometry_location, root)
        elif geometry_scheme == 'shot':
            root = '/assets'
            location = '{}{}'.format(geometry_location, root)
        else:
            raise NotImplementedError()
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
                    validation_checker.set_node_files_result_register(
                        location,
                        [file_path],
                        description=u'scene has modifier to save',
                        check_group=check_group,
                        check_status=validation_checker.CheckStatus.Warning,
                    )
    #
    def set_katana_geometry_check(self, validation_checker):
        from lxusd import usd_configure, usd_core
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        check_group = 'Geometry Check'
        #
        geometry_location = '/root/world/geo'
        #
        ktn_workspace = ktn_dcc_objects.AssetWorkspace()
        geometry_scheme = ktn_workspace.get_geometry_scheme()
        if geometry_scheme == 'asset':
            root = self._rsv_scene_properties.get('dcc.root')
            sub_root = '{}/hi'.format(root)
            #
            location = '{}{}'.format(geometry_location, root)
            sub_location = '{}{}'.format(geometry_location, sub_root)
            scene_usd_file_path = ktn_workspace.get_geometry_uv_map_usd_source_file()
            if scene_usd_file_path is None:
                validation_checker.set_node_result_register(
                    location,
                    check_group=check_group,
                    check_status=validation_checker.CheckStatus.Warning,
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
                        validation_checker.set_node_result_register(
                            i_mesh_location,
                            check_group=check_group,
                            check_status=validation_checker.CheckStatus.Warning,
                            description='"mesh default uv-map name" "map1 / st" is non-exists'
                        )
                    #
                    i_face_vertex_indices = i_mesh_opt.get_face_vertex_indices()
                    for j_uv_map_name in i_uv_map_names:
                        j_uv_map_face_vertex_indices = i_mesh_opt.get_uv_map_face_vertex_indices(j_uv_map_name)
                        if j_uv_map_face_vertex_indices:
                            if len(i_face_vertex_indices) != len(j_uv_map_face_vertex_indices):
                                validation_checker.set_node_result_register(
                                    i_mesh_location,
                                    check_group=check_group,
                                    check_status=validation_checker.CheckStatus.Error,
                                    description='"mesh uv-map" in "{}" has non-data vertices'.format(j_uv_map_name)
                                )
                        else:
                            validation_checker.set_node_result_register(
                                i_mesh_location,
                                check_group=check_group,
                                check_status=validation_checker.CheckStatus.Warning,
                                description='"mesh uv-map" in "{}" is non-data'.format(j_uv_map_name)
                            )

    def set_katana_geometry_topology_check(self, validation_checker):
        from lxutil import utl_configure
        #
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        #
        import lxkatana.fnc.comparers as ktn_fnc_comparers
        #
        check_group = 'Geometry Topology Check'
        #
        ktn_workspace = ktn_dcc_objects.AssetWorkspace()
        geometry_scheme = ktn_workspace.get_geometry_scheme()
        geometry_location = '/root/world/geo'
        if geometry_scheme == 'asset':
            root = self._rsv_scene_properties.get('dcc.root')
            sub_root = '{}/hi'.format(root)
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
                validation_checker.set_node_result_register(
                    location,
                    check_group=check_group,
                    check_status=validation_checker.CheckStatus.Warning,
                    description='"asset root" "{}" is non-exists'.format(dcc_location)
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
                validation_checker.set_node_result_register(
                    location,
                    check_group=check_group,
                    check_status=validation_checker.CheckStatus.Warning,
                    description='"geometry usd-file" from "model" is non-exists'
                )
                return False
            scene_file_path = ktn_dcc_objects.Scene.get_current_file_path()
            scene_usd_file_path = ktn_workspace.get_geometry_uv_map_usd_source_file()
            if scene_usd_file_path is None:
                validation_checker.set_node_result_register(
                    location,
                    check_group=check_group,
                    check_status=validation_checker.CheckStatus.Warning,
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
                i_dcc_path = '{}{}'.format(location, i_src_gmt_path)
                for j_e in warning_es:
                    if j_e in i_description:
                        validation_checker.set_node_result_register(
                            i_dcc_path,
                            check_group=check_group,
                            check_status=validation_checker.CheckStatus.Warning,
                            description='"mesh" is "{}"'.format(i_description)
                        )
                #
                for j_e in error_ds:
                    if j_e in i_description:
                        validation_checker.set_node_result_register(
                            i_dcc_path,
                            check_group=check_group,
                            check_status=validation_checker.CheckStatus.Error,
                            description='"mesh" is "{}"'.format(i_description)
                        )

    def set_katana_look_check(self, validation_checker):
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects

        check_group = 'Look Check'
        ktn_workspace = ktn_dcc_objects.AssetWorkspace()
        geometry_scheme = ktn_workspace.get_geometry_scheme()
        geometry_location = '/root/world/geo'
        if geometry_scheme == 'asset':
            root = self._rsv_scene_properties.get('dcc.root')
            location = '{}{}'.format(geometry_location, root)
        elif geometry_scheme == 'shot':
            root = '/assets'
            location = '{}{}'.format(geometry_location, root)
        else:
            raise NotImplementedError()

        dcc_workspace = ktn_dcc_objects.AssetWorkspace()

        error_args = dcc_workspace.get_non_material_geometry_args(location)
        for i_pass_name, i_dcc_path in error_args:
            validation_checker.set_node_result_register(
                i_dcc_path,
                check_group=check_group,
                check_status=validation_checker.CheckStatus.Warning,
                description='"geometry" in look-pass "{}" is non "material-assign" ( maybe assign at group )'.format(
                    i_pass_name
                )
            )

    def set_katana_texture_check(self, validation_checker):
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects

        check_group = 'Texture Check'
        ktn_workspace = ktn_dcc_objects.AssetWorkspace()
        geometry_scheme = ktn_workspace.get_geometry_scheme()
        geometry_location = '/root/world/geo'
        if geometry_scheme == 'asset':
            root = self._rsv_scene_properties.get('dcc.root')
            location = '{}{}'.format(geometry_location, root)
        elif geometry_scheme == 'shot':
            root = '/assets'
            location = '{}{}'.format(geometry_location, root)
        else:
            raise NotImplementedError()
        #
        dcc_texture_references = ktn_dcc_objects.TextureReferences()

        dcc_workspace = ktn_dcc_objects.AssetWorkspace()
        dcc_shaders = dcc_workspace.get_all_dcc_geometry_shader_by_location(location)
        dcc_objs = dcc_texture_references.get_objs(
            include_paths=[i.path for i in dcc_shaders]
        )
        if dcc_objs:
            self._set_dcc_texture_check_(validation_checker, check_group, dcc_objs)

    def set_katana_texture_workspace_check(self, validation_checker):
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects

        check_group = 'Texture Workspace Check'
        ktn_workspace = ktn_dcc_objects.AssetWorkspace()
        geometry_scheme = ktn_workspace.get_geometry_scheme()
        geometry_location = '/root/world/geo'
        if geometry_scheme == 'asset':
            root = self._rsv_scene_properties.get('dcc.root')
            location = '{}{}'.format(geometry_location, root)
        elif geometry_scheme == 'shot':
            root = '/assets'
            location = '{}{}'.format(geometry_location, root)
        else:
            raise NotImplementedError()
        #
        dcc_texture_references = ktn_dcc_objects.TextureReferences()

        dcc_workspace = ktn_dcc_objects.AssetWorkspace()
        dcc_shaders = dcc_workspace.get_all_dcc_geometry_shader_by_location(location)
        dcc_objs = dcc_texture_references.get_objs(
            include_paths=[i.path for i in dcc_shaders]
        )
        if dcc_objs:
            self._set_dcc_texture_workspace_check_(
                validation_checker, check_group,
                dcc_objs
            )
