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
        #
        look_pass_node=None,
        look_pass=None,
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
        self.__set_export_(
            file_path=self._file_path,
            frame=frame, 
            root='/master',
        )
    @classmethod
    def _get_katana_is_ui_mode_(cls):
        return Configuration.get('KATANA_UI_MODE')

    def __set_file_export_(self, source_port, file_path, frame, camera_location):
        file_obj = utl_dcc_objects.OsFile(file_path)
        #
        file_obj.set_directory_create()
        #
        path_base = file_obj.path_base
        ext = file_obj.ext
        #
        camera_node = ktn_dcc_objects.Node('/rootNode/look_ass_export__camera')
        merge_node = ktn_dcc_objects.Node('/rootNode/look_ass_export__merge')
        render_settings_node = ktn_dcc_objects.Node('/rootNode/look_ass_export__render_settings')
        arnold_render_settings_node = ktn_dcc_objects.Node('/rootNode/look_ass_export__arnold_render_settings')
        #
        merge_node.get_dcc_instance('Merge')
        camera_node.get_dcc_instance('CameraCreate')
        camera_node.get_port('name').set(camera_location)
        #
        render_settings_node.get_dcc_instance('RenderSettings')
        render_settings_node.set('args.renderSettings.sceneTraversal.cache.cacheSoftLimit.enable', True)
        render_settings_node.set('args.renderSettings.sceneTraversal.cache.cacheSoftLimit.value', 51200)
        render_settings_node.set('args.renderSettings.sceneTraversal.useCachePrepopulation.enable', True)
        render_settings_node.set('args.renderSettings.sceneTraversal.useCachePrepopulation.value', 0)
        #
        arnold_render_settings_node.get_dcc_instance('ArnoldGlobalSettings')
        arnold_render_settings_node.set('args.arnoldGlobalStatements.assFileContents.enable', True)
        arnold_render_settings_node.set('args.arnoldGlobalStatements.assFileContents.value', 'geometry and materials')
        arnold_render_settings_node.set('args.arnoldGlobalStatements.assFile.enable', True)
        source_port.set_target(
            merge_node.get_input_port('output'),
            force=True
        )
        camera_node.get_output_port('out').set_target(
            merge_node.get_input_port('camera'),
            force=True
        )
        merge_node.get_output_port('out').set_target(
            render_settings_node.get_input_port('input')
        )
        render_settings_node.get_output_port('out').set_target(
            arnold_render_settings_node.get_input_port('input')
        )
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
        if frame[0] != frame[1]:
            for i_current_frame in range(frame[0], frame[1] + 1):
                i_output_file_path = u'{}.{}{}'.format(path_base, str(i_current_frame).zfill(4), ext)
                arnold_render_settings_node.set('args.arnoldGlobalStatements.assFile.value', i_output_file_path)
                #
                NodegraphAPI.GetRootNode().getParameter("currentTime").setValue(i_current_frame, 0)
                ktn_dcc_objects.Scene.set_current_frame(i_current_frame)
                render_set.frame = i_current_frame
                RenderManager.StartRender(
                    self.RENDER_MODE,
                    node=arnold_render_settings_node.ktn_obj,
                    views=[camera_location],
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
            arnold_render_settings_node.set('args.arnoldGlobalStatements.assFile.value', output_file_path)
            render_set.frame = frame[0]
            RenderManager.StartRender(
                self.RENDER_MODE,
                node=arnold_render_settings_node.ktn_obj,
                views=[camera_location],
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
        merge_node.set_delete()
        camera_node.set_delete()
        arnold_render_settings_node.set_delete()

    def __set_export_(self, file_path, frame, root):
        camera_location = '/root/world/cam/camera'
        #
        look_pass_node = self._option.get('look_pass_node')
        look_pass_name = self._option.get('look_pass')
        utl_core.Log.set_module_result_trace(
            'ass export',
            'obj="{}", look_pass="{}"'.format(
                look_pass_node,
                look_pass_name
            )
        )
        if isinstance(look_pass_node, (str, unicode)):
            look_pass_node = ktn_dcc_objects.Node(look_pass_node)
        #
        if look_pass_node.get_is_exists() is True:
            input_port = look_pass_node.get_input_port(look_pass_name)
            if input_port:
                source_port = input_port.get_source()
                if source_port is not None:
                    self.__set_file_export_(
                        source_port, file_path, frame, camera_location
                    )


class LookKlfExtraExporter(utl_fnc_obj_abs.AbsDccExporter):
    def __init__(self, file_path, root=None, option=None):
        super(LookKlfExtraExporter, self).__init__(file_path, root, option)

    def set_run(self):
        import parse

        texture_references = ktn_dcc_objects.TextureReferences()
        objs = texture_references.get_objs()
        dic = {}
        if objs:
            for obj in objs:
                for port_path, file_path in obj.reference_raw.items():
                    port = obj.get_port(port_path)
                    expression = texture_references._get_expression_(port)
                    if expression is not None:
                        parse_pattern = '\'{file}\'%{argument}'
                        p = parse.parse(parse_pattern, expression)
                        if p:
                            key = u'{}.{}'.format(obj.name, port_path)
                            dic[key] = expression
        #
        if dic:
            utl_dcc_objects.OsJsonFile(
                self._file_path
            ).set_write(dic)
