# coding:utf-8
import sys
# noinspection PyUnresolvedReferences
from Katana import Configuration, RenderManager, ScenegraphManager, KatanaFile, FarmAPI, CacheManager, Nodes3DAPI, NodegraphAPI
# noinspection PyUnresolvedReferences
from UI4 import Manifest

from lxutil import utl_core

import lxutil.scripts as utl_scripts

from lxutil.fnc import utl_fnc_obj_abs

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


class LookAssExporter(utl_fnc_obj_abs.AbsDccExporter):
    RENDER_MODE = 'previewRender'
    #
    OPTION = dict(
        geometry_root='/root/world/geo',
        output_obj=None,
    )
    def __init__(self, file_path, root=None, option=None):
        super(LookAssExporter, self).__init__(file_path, root, option)

    def set_run(self):
        # utl_core.Log.set_module_result_trace(
        #     'python-run',
        #     '{}.{}(file_path="{}", root="{}").{}()'.format(
        #         self.__module__,
        #         self.__class__.__name__,
        #         self._file_path,
        #         self._root,
        #         sys._getframe().f_code.co_name
        #     )
        # )
        frame = ktn_dcc_objects.Scene.get_frame_range(frame=self._option.get('frame'))
        self._set_dot_ass_export_(
            file_path=self._file_path,
            frame=frame, 
            root='/master',
        )
    @classmethod
    def _get_katana_is_ui_mode_(cls):
        return Configuration.get('KATANA_UI_MODE')

    def _set_dot_ass_export_(self, file_path, frame, root):
        camera = '/root/world/cam/camera'
        file_obj = utl_dcc_objects.OsFile(file_path)
        #
        file_obj.set_directory_create()
        #
        path_base = file_obj.path_base
        ext = file_obj.ext
        geometry_root = self._option.get('geometry_root')
        location = geometry_root + root
        #
        output_obj_path = self._option.get('output_obj')
        utl_core.Log.set_module_result_trace(
            'katana-ass-sequence-export',
            'obj="{}"'.format(output_obj_path)
        )
        output_obj = ktn_dcc_objects.Node(output_obj_path)
        if output_obj.get_is_exists() is True:
            camera_obj = ktn_dcc_objects.Node('/rootNode/look_ass_export__camera')
            merge_obj = ktn_dcc_objects.Node('/rootNode/look_ass_export__merge')
            render_obj = ktn_dcc_objects.Node('/rootNode/look_ass_export__render')
            merge_ktn_obj, is_create = merge_obj.get_dcc_instance('Merge')
            camera_ktn_obj, is_create = camera_obj.get_dcc_instance('CameraCreate')
            render_ktn_obj, is_create = render_obj.get_dcc_instance('ArnoldGlobalSettings')
            output_obj.get_output_port('out').set_target(
                merge_obj.get_input_port('output'),
                force=True
            )
            camera_obj.get_output_port('out').set_target(
                merge_obj.get_input_port('camera'),
                force=True
            )
            merge_obj.get_output_port('out').set_target(
                render_obj.get_input_port('input')
            )
            #
            camera_obj.get_port('name').set(camera)
            #
            render_obj.get_port('args.arnoldGlobalStatements.assFileContents.enable').set(True)
            render_obj.get_port('args.arnoldGlobalStatements.assFileContents.value').set('geometry and materials')
            #
            render_set = RenderManager.RenderingSettings()
            render_set.ignoreROI = True
            render_set.asynch = False
            render_set.interactiveOutputs = True
            render_set.interactiveMode = True
            #
            if not self._get_katana_is_ui_mode_():
                Manifest.Nodes2DAPI.CreateExternalRenderListener(15900)
            #
            render_obj.get_port('args.arnoldGlobalStatements.assFile.enable').set(True)
            if frame[0] != frame[1]:
                for i_current_frame in range(frame[0], frame[1] + 1):
                    i_output_file_path = u'{}.{}{}'.format(path_base, str(i_current_frame).zfill(4), ext)
                    render_obj.get_port('args.arnoldGlobalStatements.assFile.value').set(i_output_file_path)
                    NodegraphAPI.GetRootNode().getParameter("currentTime").setValue(i_current_frame, 0)
                    ktn_dcc_objects.Scene.set_current_frame(i_current_frame)
                    render_set.frame = i_current_frame
                    RenderManager.StartRender(
                        self.RENDER_MODE,
                        node=render_obj.ktn_obj,
                        views=[camera],
                        settings=render_set
                    )
                    #
                    fr = utl_scripts.DotAssFileReader(i_output_file_path)
                    fr._set_file_paths_convert_()
                    #
                    utl_core.Log.set_module_result_trace(
                        'katana-ass-sequence-export',
                        u'file="{}"'.format(file_path)
                    )
            else:
                output_file_path = u'{}{}'.format(path_base, ext)
                render_obj.get_port('args.arnoldGlobalStatements.assFile.value').set(output_file_path)
                render_set.frame = frame[0]
                RenderManager.StartRender(
                    self.RENDER_MODE,
                    node=render_obj.ktn_obj,
                    views=[camera],
                    settings=render_set
                )
                #
                output_file = utl_dcc_objects.OsFile(output_file_path)
                if output_file.get_is_exists() is True:
                    #
                    fr = utl_scripts.DotAssFileReader(output_file_path)
                    fr._set_file_paths_convert_()
                    #
                    utl_core.Log.set_module_result_trace(
                        'katana-ass-export',
                        u'file="{}"'.format(file_path)
                    )
            #
            merge_obj.set_delete()
            camera_obj.set_delete()
            render_obj.set_delete()


class LookKlfExtraExporter(utl_fnc_obj_abs.AbsDccExporter):
    def __init__(self, file_path, root=None, option=None):
        super(LookKlfExtraExporter, self).__init__(file_path, root, option)

    def set_run(self):
        texture_references = ktn_dcc_objects.TextureReferences()
        objs = texture_references.get_objs()
        dic = {}
        if objs:
            for obj in objs:
                for port_path, file_path in obj.reference_raw.items():
                    port = obj.get_port(port_path)
                    expression = texture_references._get_expression_(port)
                    if expression is not None:
                        key = u'{}.{}'.format(obj.name, port_path)
                        dic[key] = expression
        #
        if dic:
            utl_dcc_objects.OsJsonFile(
                self._file_path
            ).set_write(dic)
