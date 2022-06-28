# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

import os

import glob

import copy

import collections

from lxbasic import bsc_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxbasic.objects as bsc_objects

from lxutil import utl_core

from lxutil.fnc import utl_fnc_obj_abs

from lxmaya import ma_configure, ma_core

import lxmaya.modifiers as mya_modifiers

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxutil.fnc.exporters as utl_fnc_exporters


class SceneExporter(utl_fnc_obj_abs.AbsFncOptionMethod):
    WITH_XGEN = 'with_xgen_collection'
    OPTION = dict(
        file='',
        location='',
        with_xgen_collection=False,
        with_set=False,
        ext_extras=[]
    )
    def __init__(self, option=None):
        super(SceneExporter, self).__init__(option)

    def set_run(self):
        file_path = self.get('file')
        location = self.get('location')
        with_xgen_collection = self.get('with_xgen_collection')
        with_set = self.get('with_set')
        #
        ext_extras = self.get('ext_extras')
        #
        os_file = utl_dcc_objects.OsFile(file_path)
        os_file.set_directory_create()
        #
        option = dict(
            type=mya_dcc_objects.Scene._get_file_type_name_(file_path),
            options='v=0;',
            force=True,
            defaultExtensions=True,
            preserveReferences=False,
        )
        _selected_paths = []
        if location:
            root_dag_opt = bsc_core.DccPathDagOpt(location)
            root_mya_dag_opt = root_dag_opt.set_translate_to(
                ma_configure.Util.OBJ_PATHSEP
            )
            _selected_paths = cmds.ls(selection=1, long=1) or []
            if with_set is True:
                ss = mya_dcc_objects.Sets()
                for i in ss.get_paths():
                    i_set = mya_dcc_objects.Set(i)
                    if i_set.get_elements_match('|master|*'):
                        utl_core.Log.set_module_result_trace(
                            'maya scene export',
                            u'set="{}" is add to export'.format(i_set.path)
                        )
                        cmds.select(i_set.path, noExpand=True, add=True)
            #
            cmds.select(root_mya_dag_opt.path)
            option['exportSelected'] = True
        else:
            option['exportAll'] = True
        #
        _ = cmds.file(file_path, **option)
        if _:
            self._results = [file_path]
        #
        if with_xgen_collection is True:
            utl_fnc_exporters.DotMaExporter._set_xgen_collection_files_copy_(
                file_path_src=mya_dcc_objects.Scene.get_current_file_path(),
                file_path_tgt=file_path
            )
        #
        if ext_extras:
            file_src = utl_dcc_objects.OsFile(mya_dcc_objects.Scene.get_current_file_path())
            file_tgt = utl_dcc_objects.OsFile(file_path)
            for i_ext in ext_extras:
                i_src = '{}.{}'.format(file_src.path_base, i_ext)
                i_tgt = '{}.{}'.format(file_tgt.path_base, i_ext)
                utl_dcc_objects.OsFile(i_src).set_copy_to_file(i_tgt)
        #
        if self._results:
            for i in self._results:
                utl_core.Log.set_module_result_trace(
                    'maya scene export',
                    u'file="{}"'.format(i)
                )

        if 'exportSelected' in option:
            if _selected_paths:
                cmds.select(_selected_paths)
            else:
                cmds.select(clear=1)

        return self._results

    def get_outputs(self):
        return self._results


class PreviewExporter(utl_fnc_obj_abs.AbsDccExporter):
    OPTION = dict(
        convert_to_dot_mov=True,
        use_render=False,
        frame=(0, 0),
        color_space='Linear'
    )
    def __init__(self, file_path, root=None, option=None):
        super(PreviewExporter, self).__init__(file_path, root, option)
    @classmethod
    def _set_playblast_(cls, file_path, root, use_default_material=False, frame=(0, 0), size=(1024, 1024), persp_view=True, default_material_color=None):
        output_file = utl_dcc_objects.OsFile(file_path)
        output_file_path_base = output_file.path_base
        ext = output_file.ext
        compression = ext[1:]
        #
        preview_window = 'preview_export'
        mya_dcc_objects.Scene.set_window_delete(preview_window)
        cmds.window(preview_window, title='preview_export')
        image_width, image_height = size
        layout = cmds.paneLayout(width=image_width, height=image_height)
        camera, camera_shape = CameraYamlExporter._set_camera_create_(root, persp_view)
        preview_export_viewport = cmds.modelPanel(
            label='snapShotPanel',
            parent=layout,
            menuBarVisible=1,
            modelEditor=1,
            camera=camera
        )
        #
        if not use_default_material:
            mya_dcc_objects.Scene.set_display_mode(6)
        else:
            mya_dcc_objects.Scene.set_display_mode(5)
        #
        cmds.displayRGBColor('background', .25, .25, .25)
        cmds.displayRGBColor('backgroundTop', .25, .25, .25)
        cmds.displayRGBColor('backgroundBottom', .25, .25, .25)
        cmds.showWindow(preview_window)
        # Set ModelPanel ( Viewport 2.0 )
        mya_dcc_objects.Scene._set_preview_viewport_setup_(preview_export_viewport, mode=1)
        #
        cmds.modelEditor(
            preview_export_viewport,
            edit=1,
            activeView=1,
            useDefaultMaterial=use_default_material,
            wireframeOnShaded=0,
            fogging=0,
            dl='default',
            twoSidedLighting=1,
            allObjects=0,
            manipulators=0,
            grid=0,
            hud=1,
            sel=0
        )
        #
        cmds.modelEditor(
            preview_export_viewport,
            edit=1,
            activeView=1,
            polymeshes=1,
            subdivSurfaces=1,
            fluids=1,
            strokes=1,
            nCloths=1,
            nParticles=1,
            pluginShapes=1,
            pluginObjects=['gpuCacheDisplayFilter', 1],
            displayAppearance='smoothShaded'
        )
        #
        if default_material_color is not None:
            r, g, b = default_material_color
            cmds.setAttr('lambert1.color', r, g, b)
        else:
            cmds.setAttr('lambert1.color', 0, .75, .75)
        #
        start_frame, end_frame = frame
        cmds.playblast(
            startTime=start_frame,
            endTime=end_frame,
            format='iff',
            filename=output_file_path_base,
            sequenceTime=0,
            clearCache=1,
            viewer=0,
            showOrnaments=0,
            offScreen=0,
            framePadding=4,
            percent=100,
            compression=compression,
            quality=100,
            widthHeight=size
        )
        #
        cmds.isolateSelect(preview_export_viewport, state=0)
        mya_dcc_objects.Scene.set_window_delete(preview_window)
        mya_dcc_objects.Scene.set_display_mode(5)
        #
        cmds.setAttr('lambert1.color', .5, .5, .5)
        cmds.delete(camera)
    @classmethod
    def _set_render_(cls, file_path, root, persp_view=True, size=(1024, 1024), frame=(0, 0)):
        output_file = utl_dcc_objects.OsFile(file_path)
        output_file_path_base = output_file.path_base
        ext = output_file.ext
        compression = ext[1:]
        image_width, image_height = size
        camera, camera_shape = CameraYamlExporter._set_camera_create_(root, persp_view)
        #
        render_option = mya_dcc_objects.RenderOption()
        start_frame, end_frame = frame
        render_option.set_animation_enable(True)
        render_option.set_frame_range(start_frame, end_frame)
        render_option.set_image_size(image_width, image_height)
        render_option.set_output_file_path(output_file_path_base)
        #
        light = cls._set_arnold_light_create_()
        cls._set_arnold_options_create_()
        cls._set_arnold_options_update_()
        cls._set_arnold_render_run_(camera, image_width, image_height)
        cmds.delete(light)
        cmds.delete(camera)
    @classmethod
    def _set_arnold_light_create_(cls):
        light = mya_dcc_objects.Shape('light')
        if light.get_is_exists() is False:
            light = light.set_create('aiStandIn')
        #
        atr_raw = dict(
            dso=utl_core.Path.set_map_to_platform(
                '/l/resource/td/asset/ass/default-light.ass'
            )
        )
        [light.get_port(k).set(v) for k, v in atr_raw.items()]
        return light.transform.path
    @classmethod
    def _set_arnold_options_create_(cls):
        # noinspection PyBroadException
        try:
            # noinspection PyUnresolvedReferences
            import mtoa.core as core
            core.createOptions()
        except:
            pass
    @classmethod
    def _set_arnold_options_update_(cls):
        arnold_render_option = mya_dcc_objects.AndRenderOption()
        arnold_render_option.set_image_format('exr')
        arnold_render_option.set_aa_sample(6)
    @classmethod
    def _set_arnold_render_run_(cls, camera, image_width, image_height, frame=None):
        cls._set_arnold_options_create_()
        #
        cmds.arnoldRender(
            seq='', cam=camera, w=image_width, h=image_height, srv=False
        )
        return True

    def set_run(self):
        use_render = self._option.get('use_render')
        self._mya_root_dag_path = self._root_dat_opt.set_translate_to(
            ma_configure.Util.OBJ_PATHSEP
        )
        root_mya_obj = mya_dcc_objects.Group(self._mya_root_dag_path.path)
        mya_dcc_objects.Scene.set_render_resolution(1024, 1024)
        if root_mya_obj.get_is_exists() is True:
            if use_render is True:
                self._set_render_run_()
                utl_core.Log.set_module_result_trace(
                    'maya-render-preview-export',
                    u'file="{}"'.format(self._file_path)
                )
            else:
                self._set_snapshot_run_()
                utl_core.Log.set_module_result_trace(
                    'maya-snapshot-preview-export',
                    u'file="{}"'.format(self._file_path)
                )
        else:
            utl_core.Log.set_module_warning_trace(
                'maya-preview-export',
                u'obj="{}" is non-exists'.format(self._root)
            )

    def _set_snapshot_run_(self):
        import lxshotgun.operators as stg_operators
        #
        self._file_obj = utl_dcc_objects.OsFile(self._file_path)
        file_path_base = self._file_obj.path_base
        #
        jpg_file_path = '{}.snapshot/image{}'.format(file_path_base, '.jpg')
        jpg_seq_file_path = '{}.snapshot/image.%04d{}'.format(file_path_base, '.jpg')
        mov_file_path = '{}{}'.format(file_path_base, '.mov')
        frame = self._option.get('frame')
        self._set_playblast_(
            jpg_file_path,
            self._root,
            frame=frame
        )
        jpg_seq_file = utl_dcc_objects.OsFile(jpg_seq_file_path)
        if self._option.get('convert_to_dot_mov') is True:
            if jpg_seq_file.get_exists_files_():
                bsc_core.VedioOpt(
                    mov_file_path
                ).set_create_from(
                    jpg_seq_file_path
                )
                # stg_operators.ImageOpt(
                #     jpg_seq_file
                # ).set_convert_to(mov_file_path)
        else:
            jpg_seq_file = utl_dcc_objects.OsFile(jpg_seq_file_path)
            exist_files = jpg_seq_file.get_exists_files_()
            if exist_files:
                jpg_seq_file.get_exists_files_()[0].set_copy_to_file(
                    self._file_path
                )
        #
        self._results = [mov_file_path]

    def _set_render_run_(self):
        self._file_obj = utl_dcc_objects.OsFile(self._file_path)
        file_path_base = self._file_obj.path_base
        #
        jpg_file_path = '{}.render/image{}'.format(file_path_base, '.exr')
        jpg_seq_file_path = '{}.render/image.%04d{}'.format(file_path_base, '.exr')
        mov_file_path = '{}{}'.format(file_path_base, '.mov')

        self._set_render_(
            jpg_file_path,
            self._mya_root_dag_path.path
        )
        jpg_seq_file = utl_dcc_objects.OsFile(jpg_seq_file_path)
        if self._option.get('convert_to_dot_mov') is True:
            if jpg_seq_file.get_exists_files_():
                bsc_core.VedioOpt(
                    mov_file_path
                ).set_create_from(
                    jpg_seq_file_path
                )
                # stg_operators.ImageOpt(
                #     utl_dcc_objects.OsFile(jpg_seq_file_path)
                # ).set_convert_to(mov_file_path)

        self._results = [mov_file_path]


class CameraYamlExporter(utl_fnc_obj_abs.AbsFncOptionMethod):
    OPTION = dict(
        file='',
        root=''
    )
    def __init__(self, option):
        super(CameraYamlExporter, self).__init__(option)
        #
        self._raw = bsc_objects.Content(
            value=collections.OrderedDict()
        )
    @classmethod
    def _set_camera_create_(cls, root, persp_view):
        dcc_root_dag_path = bsc_core.DccPathDagOpt(root)
        mya_root_dag_path = dcc_root_dag_path.set_translate_to(
            pathsep='|'
        )
        mya_camera = mya_dcc_objects.Shape('|persp_view')
        mya_camera = mya_camera.set_create('camera')
        camera_transform = mya_camera.transform.path
        camera_shape = mya_camera.path
        #
        cmds.camera(
            camera_shape,
            edit=1,
            displayFilmGate=0,
            displaySafeAction=0,
            displaySafeTitle=0,
            displayFieldChart=0,
            displayResolution=1,
            displayGateMask=1,
            filmFit=1,
            focalLength=35.000,
            overscan=1.0,
            nearClipPlane=0.1,
            farClipPlane=1000000.0
        )
        #
        if persp_view is True:
            cmds.camera(
                camera_shape,
                edit=1,
                position=(28.0, 21.0, 28.0),
                rotation=(-27.9383527296, 45, 0)
            )
        #
        cmds.setAttr(camera_shape + '.displayGateMaskOpacity', 1)
        cmds.setAttr(camera_shape + '.displayGateMaskColor', 0, 0, 0, type='double3')
        #
        cmds.viewFit(
            camera_shape,
            [mya_root_dag_path.value],
            fitFactor=1.0,
            animate=0
        )
        cmds.camera(
            camera_shape,
            edit=1,
            focalLength=67.177,
        )
        return camera_transform, camera_shape
    @mya_modifiers.set_undo_mark_mdf
    def set_run(self):
        file_path = self._option['file']
        root = self._option['root']
        camera_transform, camera_shape = self._set_camera_create_(root, persp_view=True)
        #
        for p in ma_core.CmdObjOpt(camera_transform).get_ports(includes=['translate', 'rotate', 'scale']):
            self._raw.set(
                'persp.transform.{}'.format(p.get_port_path()), p.get()
            )
        #
        for p in ma_core.CmdObjOpt(camera_shape).get_ports(includes=['focalLength', 'farClipPlane', 'nearClipPlane']):
            self._raw.set(
                'persp.shape.{}'.format(p.get_port_path()), p.get()
            )
        #
        self._raw.set_save_to(file_path)
        utl_core.Log.set_module_result_trace(
            'camera-yml-export',
            'file="{}"'.format(file_path)
        )
        cmds.delete(camera_transform)
