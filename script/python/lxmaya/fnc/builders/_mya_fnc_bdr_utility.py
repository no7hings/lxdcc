# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from lxbasic import bsc_core

from lxutil import utl_core

from lxutil.fnc import utl_fnc_obj_abs

from lxmaya import ma_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_operators as mya_dcc_operators


class GeometryAlembicBlender(object):
    def __init__(self, src_root, tgt_root):
        self._src_root = bsc_core.DccPathDagOpt(src_root).set_translate_to('|').to_string()
        self._tgt_root = bsc_core.DccPathDagOpt(tgt_root).set_translate_to('|').to_string()

    def __set_meshes_blend_(self):
        self._set_mesh_connect_(
            self._get_mesh_dic_(mya_dcc_objects.Group(self._src_root).get_all_shape_paths(include_obj_type='mesh')),
            self._get_mesh_dic_(mya_dcc_objects.Group(self._tgt_root).get_all_shape_paths(include_obj_type='mesh'))
        )
        _ = '|'.join(self._src_root.split('|')[:2])
        if cmds.objExists(
            _
        ) is True:
            cmds.delete(_)
    @classmethod
    def _get_mesh_dic_(cls, mesh_paths):
        dic = {}
        for i_mesh_path in mesh_paths:
            mesh_opt = mya_dcc_operators.MeshOpt(mya_dcc_objects.Node(i_mesh_path))
            face_vertices_as_uuid = mesh_opt.get_face_vertices_as_uuid()
            dic.setdefault(
                face_vertices_as_uuid, []
            ).append(i_mesh_path)
        return dic
    @classmethod
    def _set_mesh_connect_(cls, src_dic, tgt_dic):
        for seq, (k, s_v) in enumerate(src_dic.items()):
            if k in tgt_dic:
                t_v = tgt_dic[k]
                s_p = s_v[0]
                t_p = t_v[0]
                cls._set_mesh_shape_blend_(seq, s_p, t_p)
    @classmethod
    def _set_blend_histories_clear_(cls, obj_path):
        _ = cmds.listConnections(obj_path, destination=0, source=1, type='tweak') or []
        [cmds.delete(i) for i in _ if cmds.objExists(i)]
    @classmethod
    def _set_shape_parent_(cls, src_shape_path, tgt_shape_path, blend_path):
        if cmds.objExists(src_shape_path) and cmds.objExists(tgt_shape_path):
            src_transform_path = cmds.listRelatives(src_shape_path, parent=1, fullPath=1)[0]
            tgt_transform_path = cmds.listRelatives(tgt_shape_path, parent=1, fullPath=1)[0]
            if src_transform_path != tgt_transform_path:
                tgt_shape_name = tgt_shape_path.split('|')[-1]
                new_shape_name = '{}_source'.format(tgt_shape_name)
                new_src_shape_path = '{}|{}'.format(src_transform_path, new_shape_name)
                #
                new_tgt_shape_path = '{}|{}'.format(tgt_transform_path, new_shape_name)
                cmds.rename(
                    src_shape_path, new_shape_name
                )
                cmds.parent(new_src_shape_path, tgt_transform_path, shape=1, add=1)
                cmds.setAttr('{}.intermediateObject'.format(new_tgt_shape_path), 1)
                cmds.delete(src_transform_path)
                cmds.connectAttr(
                    '{}.worldMesh[0]'.format(new_tgt_shape_path),
                    '{}.inputTarget[0].inputTargetGroup[0].inputTargetItem[6000].inputGeomTarget'.format(blend_path)
                )
    @classmethod
    def _set_mesh_shape_blend_(cls, seq, src_mesh_path, tgt_mesh_path):
        tgt_shape_name = src_mesh_path.split('|')[-1]
        bs = cmds.blendShape(
            src_mesh_path, tgt_mesh_path,
            name='{}_blend'.format(tgt_shape_name).format(seq),
            weight=(0, 1),
            origin='world',
            before=1
        )
        #
        if bs:
            cls._set_shape_parent_(src_mesh_path, tgt_mesh_path, bs[0])
            # for i_b in bs:
            #     cls._set_blend_histories_clear_(i_b)

    def set_run(self):
        self.__set_meshes_blend_()


class AssetBuilder(utl_fnc_obj_abs.AbsFncOptionMethod):
    VAR_NAMES = ['hi', 'shape']
    #
    OPTION = dict(
        project='',
        asset='',
        #
        geometry_option='step=mod&task=modeling',
        look_option='step=srf&task=surfacing',
        #
        with_model_geometry=False,
        with_model_act_geometry_dyn=False,
        with_model_act_geometry_dyn_connect=False,
        model_act_properties=[],
        #
        with_surface_cfx_geometry=False,
        #
        with_groom_geometry=False,
        with_groom_grow_geometry=False,
        #
        with_surface_geometry_uv_map=False,
        with_work_surface_geometry_uv_map=False,
        uv_map_face_vertices_contrast=False,
        #
        with_surface_look=False,
        with_surface_cfx_look=False,
        #
        with_surface_look_preview=False,
        with_work_surface_look_preview=False,
        #
        save_scene=False,
        #
        with_camera=False,
        with_light=False,
        #
        geometry_var_names=VAR_NAMES,
        #
        render_resolution=[2048, 2048]
    )
    def __init__(self, option=None):
        super(AssetBuilder, self).__init__(option)
    @classmethod
    def _set_geometry_build_by_usd_(cls, rsv_task, enable, geometry_var_names):
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        if enable is True:
            root = None
            if rsv_task:
                g_p = utl_core.GuiProgressesRunner(maximum=len(geometry_var_names))
                for var_name in geometry_var_names:
                    g_p.set_update()
                    #
                    keyword = 'asset-geometry-usd-{}-file'.format(var_name)
                    model_geometry_usd_hi_file = rsv_task.get_rsv_unit(keyword=keyword)
                    model_geometry_usd_hi_file_path = model_geometry_usd_hi_file.get_result(version='latest')
                    if model_geometry_usd_hi_file_path:
                        ipt = mya_fnc_importers.GeometryUsdImporter_(
                            file_path=model_geometry_usd_hi_file_path,
                            root=root
                        )
                        ipt.set_run()
                    else:
                        utl_core.Log.set_module_warning_trace(
                            'asset-build',
                            'unit="{}" is non-exists'.format(keyword)
                        )
                #
                g_p.set_stop()
    @classmethod
    def _set_model_act_geometry_dyn_build_(cls, rsv_task, with_model_act_geometry_dyn, model_act_properties, geometry_var_names):
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        from lxusd import usd_core
        #
        if with_model_act_geometry_dyn is True:
            dyn_sub_root = '/dyn/master/hi'
            if rsv_task:
                keyword = 'asset-geometry-abc-hi-dyn-file'
                model__act_abc_dyn__file = rsv_task.get_rsv_unit(keyword=keyword)
                model__act_abc_dyn__file_path = model__act_abc_dyn__file.get_result(version='latest')
                if model__act_abc_dyn__file_path:
                    mya_fnc_importers.GeometryAbcImporter(
                        file_path=model__act_abc_dyn__file_path,
                        root=dyn_sub_root,
                        option=dict(
                            hidden=True
                        )
                    ).set_run()
                #
                root = '/master'
                #
                keyword = 'asset-component-registry-usd-file'
                model_act__usd_registry__file = rsv_task.get_rsv_unit(keyword=keyword)
                model_act__usd_registry__file_path = model_act__usd_registry__file.get_result(version='latest')
                if model_act__usd_registry__file_path:
                    usd_stage_opt = usd_core.UsdStageOpt()
                    usd_stage_opt.set_sublayer_append(model_act__usd_registry__file_path)
                    usd_stage_opt.set_flatten()
                    usd_prim = usd_stage_opt.get_obj(root)
                    usd_prim_opt = usd_core.UsdPrimOpt(usd_prim)
                    customize_attributes = usd_prim_opt.get_customize_attributes(
                        includes=model_act_properties
                    )
                    #
                    ma_core.CmdObjOpt(
                        bsc_core.DccPathDagOpt(root).set_translate_to('|').to_string()
                    ).set_customize_attributes_create(customize_attributes)
    @classmethod
    def _set_model_act_geometry_dyn_connect_(cls, with_model_act_geometry_dyn_connect):
        GeometryAlembicBlender(
            '/dyn/master/hi', '/master/hi'
        ).set_run()
    @classmethod
    def _set_geometry_uv_map_build_by_usd_(cls, rsv_task, with_surface_geometry_uv_map, geometry_var_names, uv_map_face_vertices_contrast):
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        if with_surface_geometry_uv_map is True:
            root = None
            if rsv_task:
                g_p = utl_core.GuiProgressesRunner(maximum=len(geometry_var_names))
                for var_name in geometry_var_names[:1]:
                    g_p.set_update()
                    #
                    keyword = 'asset-geometry-usd-{}-file'.format(var_name)
                    surface_geometry_hi_file = rsv_task.get_rsv_unit(keyword=keyword)
                    surface_geometry_hi_file_path = surface_geometry_hi_file.get_result(version='latest')
                    if surface_geometry_hi_file_path:
                        ipt = mya_fnc_importers.GeometryUsdImporter_(
                            file_path=surface_geometry_hi_file_path,
                            root=root,
                        )
                        ipt.set_meshes_uv_maps_import_run(
                            uv_map_face_vertices_contrast
                        )
                    else:
                        utl_core.Log.set_module_warning_trace(
                            'asset-build',
                            'unit="{}" is non-exists'.format(keyword)
                        )
                #
                g_p.set_stop()
    @classmethod
    def _set_work_geometry_uv_map_build_by_usd_(cls, rsv_task, with_work_surface_geometry_uv_map, geometry_var_names, uv_map_face_vertices_contrast):
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        if with_work_surface_geometry_uv_map is True:
            root = None
            if rsv_task:
                g_p = utl_core.GuiProgressesRunner(maximum=len(geometry_var_names))
                for var_name in geometry_var_names[:1]:
                    g_p.set_update()
                    #
                    keyword = 'asset-work-geometry-usd-{}-file'.format(var_name)
                    work_surface_geometry_hi_file = rsv_task.get_rsv_unit(keyword=keyword)
                    work_surface_geometry_hi_file_path = work_surface_geometry_hi_file.get_result(version='latest')
                    if work_surface_geometry_hi_file_path:
                        ipt = mya_fnc_importers.GeometryUsdImporter_(
                            file_path=work_surface_geometry_hi_file_path,
                            root=root,
                        )
                        ipt.set_meshes_uv_maps_import_run(uv_map_face_vertices_contrast)
                    else:
                        utl_core.Log.set_module_warning_trace(
                            'asset-build',
                            'unit="{}" is non-exists'.format(keyword)
                        )
                #
                g_p.set_stop()
    @classmethod
    def _set_groom_geometry_build_(cls, rsv_task, with_groom_geometry, with_groom_grow_geometry):
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        if with_groom_geometry is True:
            if rsv_task:
                xgen_collection_directory_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-geometry-xgen-collection-dir')
                xgen_collection_directory_path = xgen_collection_directory_rsv_unit.get_exists_result()
                xgen_collection_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-geometry-xgen-file')
                xgen_collection_file_paths = xgen_collection_file_rsv_unit.get_latest_results()
                xgen_grow_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-geometry-xgen-grow-mesh-file')
                xgen_grow_file_paths = xgen_grow_file_rsv_unit.get_latest_results()
                if xgen_collection_file_paths:
                    if with_groom_grow_geometry is True:
                        option = dict(
                            # xgen
                            xgen_collection_file=xgen_collection_file_paths,
                            xgen_collection_directory=xgen_collection_directory_path,
                            xgen_location='/master/hair',
                            # grow
                            grow_file=xgen_grow_file_paths,
                            grow_location='/master/hair/hair_shape/hair_growMesh',
                        )
                    else:
                        option = dict(
                            # xgen
                            xgen_collection_file=xgen_collection_file_paths,
                            xgen_collection_directory=xgen_collection_directory_path,
                            xgen_location='/master/hair',
                        )
                    #
                    mya_fnc_importers.GeometryXgenImporter(
                        option=option
                    ).set_run()
    @classmethod
    def _set_look_build_by_ass_(cls, rsv_task, enable):
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        if enable is True:
            root = None
            if rsv_task:
                look_ass_file = rsv_task.get_rsv_unit(keyword='asset-look-ass-file')
                look_ass_file_path = look_ass_file.get_result(version='latest')
                if look_ass_file_path:
                    mya_fnc_importers.LookAssImporter(
                        option=dict(
                            file=look_ass_file_path,
                            location='/master',
                            look_pass='default',
                            name_join_time_tag=True,
                        )
                    ).set_run()
    @classmethod
    def _set_look_preview_build_by_yml_(cls, rsv_task, with_surface_look_preview):
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        if with_surface_look_preview is True:
            if rsv_task:
                look_yml_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-look-yml-file')
                look_yml_file_path = look_yml_file_rsv_unit.get_result(version='latest')
                if look_yml_file_path:
                    rsv_unit_properties = look_yml_file_rsv_unit.get_properties_by_result(look_yml_file_path)
                    version = rsv_unit_properties.get('version')
                    mya_fnc_importers.LookYamlImporter(
                        option=dict(
                            file=look_yml_file_path
                        )
                    ).set_run()
    @classmethod
    def _set_work_look_preview_build_by_yml_(cls, rsv_task, with_work_surface_look_preview):
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        if with_work_surface_look_preview is True:
            if rsv_task:
                look_yml_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-work-look-yml-file')
                work_look_yml_file_path = look_yml_file_rsv_unit.get_result(version='latest')
                if work_look_yml_file_path:
                    mya_fnc_importers.LookYamlImporter(
                        option=dict(
                            file=work_look_yml_file_path
                        )
                    ).set_run()
    @classmethod
    def _set_camera_build_by_abc_(cls, rsv_task, with_camera):
        import lxmaya.fnc.importers as mya_fnc_importers
        #
        if with_camera is True:
            if rsv_task is not None:
                camera_main_abc_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-camera-main-abc-file')
                camera_main_abc_file_path = camera_main_abc_file_rsv_unit.get_result(version='latest')
                if camera_main_abc_file_path:
                    mya_fnc_importers.CameraAbcImporter(
                        option=dict(
                            file=camera_main_abc_file_path,
                            location='/camera_grp'
                        )
                    ).set_run()
    @classmethod
    def _set_light_build_by_ass_(cls, rsv_task, with_light):
        if with_light is True:
            if rsv_task is not None:
                light_ass_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-light-ass-file')
                light_ass_file_path = light_ass_file_rsv_unit.get_result(version='latest')
                if light_ass_file_path:
                    light_ass_file_opt = bsc_core.StorageFileOpt(light_ass_file_path)
                    obj = mya_dcc_objects.Shape(light_ass_file_opt.name_base)
                    if obj.get_is_exists() is False:
                        obj = obj.set_create('aiStandIn')
                    #
                    atr_raw = dict(
                        dso=light_ass_file_path,
                        # mode=6
                    )
                    [obj.get_port(k).set(v) for k, v in atr_raw.items()]
    @classmethod
    def _set_scene_save_(cls, rsv_asset, save_scene):
        if save_scene is True:
            if rsv_asset is not None:
                user_directory_path = bsc_core.TemporaryMtd.get_user_directory('builder')
                # print user_directory_path
                file_path = '{}/{}.ma'.format(user_directory_path, '-'.join(rsv_asset.path.split('/')[1:]+[bsc_core.SystemMtd.get_time_tag()]))

                mya_dcc_objects.Scene.set_file_save_to(file_path)
    @classmethod
    def _set_render_(cls, render_resolution):
        mya_dcc_objects.Scene.set_render_resolution(
            *render_resolution
        )

    def set_run_with_window(self):
        import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets

        w = utl_pnl_widgets.FncPanel()

        w.set_window_show()

    def set_run(self):
        import lxresolver.commands as rsv_commands
        #
        with_model_geometry = self.get('with_model_geometry')
        with_model_act_geometry_dyn = self.get('with_model_act_geometry_dyn')
        with_model_act_geometry_dyn_connect = self.get('with_model_act_geometry_dyn_connect')
        model_act_properties = self.get('model_act_properties')
        #
        with_surface_cfx_geometry = self.get('with_surface_cfx_geometry')
        #
        with_groom_geometry = self.get('with_groom_geometry')
        with_groom_grow_geometry = self.get('with_groom_grow_geometry')
        #
        with_surface_geometry_uv_map = self.get('with_surface_geometry_uv_map')
        with_work_surface_geometry_uv_map = self.get('with_work_surface_geometry_uv_map')
        uv_map_face_vertices_contrast = self.get('uv_map_face_vertices_contrast')
        #
        with_surface_look = self.get('with_surface_look')
        with_surface_cfx_look = self.get('with_surface_cfx_look')
        #
        with_surface_look_preview = self.get('with_surface_look_preview')
        with_work_surface_look_preview = self.get('with_work_surface_look_preview')
        #
        with_camera = self.get('with_camera')
        with_light = self.get('with_light')
        #
        render_resolution = self.get('render_resolution')
        #
        save_scene = self.get('save_scene')
        #
        geometry_var_names = self.get('geometry_var_names')
        #
        project = self.get('project')
        asset = self.get('asset')
        #
        resolver = rsv_commands.get_resolver()
        rsv_project = resolver.get_rsv_project(project=project)
        #
        rsv_asset = rsv_project.get_rsv_entity(asset=asset)
        #
        model_rsv_task = rsv_project.get_rsv_task(asset=asset, step='mod', task='modeling')
        model_act_rsv_task = rsv_project.get_rsv_task(asset=asset, step='mod', task='mod_dynamic')
        groom_rsv_task = rsv_project.get_rsv_task(asset=asset, step='grm', task='groom')
        surface_rsv_task = rsv_project.get_rsv_task(asset=asset, step='srf', task='surfacing')
        surface_occ_rsv_task = rsv_project.get_rsv_task(asset=asset, step='srf', task='srf_anishading')
        surface_cfx_rsv_task = rsv_project.get_rsv_task(asset=asset, step='srf', task='srf_cfxshading')
        #
        camera_rsv_task = rsv_project.get_rsv_task(asset=asset, step='cam', task='camera')
        light_rsv_task = rsv_project.get_rsv_task(asset='lightrig', step='lgt', task='lighting')
        #
        method_args = [
            (self._set_geometry_build_by_usd_, (model_rsv_task, with_model_geometry, geometry_var_names)),
            (self._set_model_act_geometry_dyn_build_, (model_act_rsv_task, with_model_act_geometry_dyn, model_act_properties, geometry_var_names)),
            #
            (self._set_geometry_build_by_usd_, (surface_cfx_rsv_task, with_surface_cfx_geometry, geometry_var_names)),
            #
            (self._set_groom_geometry_build_, (groom_rsv_task, with_groom_geometry, with_groom_grow_geometry)),
            #
            (self._set_geometry_uv_map_build_by_usd_, (surface_rsv_task, with_surface_geometry_uv_map, geometry_var_names, uv_map_face_vertices_contrast)),
            (self._set_work_geometry_uv_map_build_by_usd_, (surface_rsv_task, with_work_surface_geometry_uv_map, geometry_var_names, uv_map_face_vertices_contrast)),
            #
            (self._set_look_build_by_ass_, (surface_rsv_task, with_surface_look)),
            (self._set_look_build_by_ass_, (surface_cfx_rsv_task, with_surface_cfx_look)),
            #
            (self._set_look_preview_build_by_yml_, (surface_occ_rsv_task, with_surface_look_preview)),
            (self._set_work_look_preview_build_by_yml_, (surface_occ_rsv_task, with_work_surface_look_preview)),
            #
            (self._set_model_act_geometry_dyn_connect_, (with_model_act_geometry_dyn_connect, )),
            #
            (self._set_camera_build_by_abc_, (camera_rsv_task, with_camera)),
            (self._set_light_build_by_ass_, (light_rsv_task, with_light)),
            #
            (self._set_render_, (render_resolution, )),
            #
            (self._set_scene_save_, (rsv_asset, save_scene)),
        ]
        if method_args:
            with utl_core.gui_progress(maximum=len(method_args)) as g_p:
                for i_method, i_args in method_args:
                    g_p.set_update()
                    #
                    i_method(*i_args)


if __name__ == '__main__':
    import lxmaya

    lxmaya.set_reload()

    import lxmaya.fnc.builders as mya_fnc_builders

    mya_fnc_builders.AssetBuilder(option=dict(project='cjd', asset='huayao')).set_run_with_window()
