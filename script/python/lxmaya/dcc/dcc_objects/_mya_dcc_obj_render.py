# encoding=utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from lxmaya.dcc import mya_dcc_obj_abs

from lxmaya.dcc.dcc_objects import _ma_dcc_obj_obj


class RenderOption(object):
    PORT_DICT = {
        'renderer': 'defaultRenderGlobals.currentRenderer',
        'output_file_path': 'defaultRenderGlobals.imageFilePrefix',
        #
        'start_frame': 'defaultRenderGlobals.startFrame',
        'end_frame': 'defaultRenderGlobals.endFrame',
        #
        'animation': 'defaultRenderGlobals.animation',
        'imageFormat': 'defaultRenderGlobals.imfPluginKey',
        'periodInExt': 'defaultRenderGlobals.periodInExt',
        'putFrameBeforeExt': 'defaultRenderGlobals.putFrameBeforeExt',
        'extensionPadding': 'defaultRenderGlobals.extensionPadding',
        'renderVersion': 'defaultRenderGlobals.renderVersion',
        #
        'image_width': 'defaultResolution.width',
        'image_height': 'defaultResolution.height',
        #
        'preMel': 'defaultRenderGlobals.preMel'
    }
    RENDER_GLOBALS = 'defaultRenderGlobals'
    def __init__(self):
        self.render_globals = _ma_dcc_obj_obj.Node(self.RENDER_GLOBALS)
    @classmethod
    def set_animation_enable(cls, boolean):
        cmds.setAttr('defaultRenderGlobals.animation', boolean)
        cmds.setAttr('defaultRenderGlobals.putFrameBeforeExt', True)
        cmds.setAttr('defaultRenderGlobals.periodInExt', True)
        cmds.setAttr('defaultRenderGlobals.outFormatControl', False)
    @classmethod
    def get_animation_enable(cls):
        return cmds.getAttr(cls.PORT_DICT['animation'])
    @classmethod
    def get_frame_rage(cls):
        start_frame = cmds.getAttr(cls.PORT_DICT['start_frame'])
        end_frame = cmds.getAttr(cls.PORT_DICT['end_frame'])
        return start_frame, end_frame

    def set_frame_range(self, start_frame, end_frame):
        if start_frame is None:
            start_frame = int(cmds.playbackOptions(query=1, minTime=1))
        if end_frame is None:
            end_frame = int(cmds.playbackOptions(query=1, maxTime=1))
        #
        cmds.setAttr(self.PORT_DICT['start_frame'], start_frame)
        cmds.setAttr(self.PORT_DICT['end_frame'], end_frame)
        #
        self.render_globals.get_port('extensionPadding').set(4)
    @classmethod
    def get_image_size(cls):
        image_width = cmds.getAttr(cls.PORT_DICT['image_width'])
        image_height = cmds.getAttr(cls.PORT_DICT['image_height'])
        return image_width, image_height
    @classmethod
    def set_image_size(cls, image_width, image_height, dpi=72):
        cmds.setAttr(cls.PORT_DICT['image_width'], image_width)
        cmds.setAttr(cls.PORT_DICT['image_height'], image_height)
        #
        cmds.setAttr('defaultResolution.pixelAspect', 1)
        cmds.setAttr('defaultResolution.deviceAspectRatio', float(image_width / image_height))
        cmds.setAttr('defaultResolution.dpi', dpi)
    @classmethod
    def set_output_file_path(cls, file_path):
        cmds.setAttr(cls.PORT_DICT['output_file_path'], file_path, type='string')


class AndRenderOption(object):
    PORT_DICT = dict(
        image_format='defaultArnoldDriver.aiTranslator',
        color_space='defaultArnoldDriver.colorManagement'
    )
    AND_OPTIONS = 'defaultArnoldRenderOptions'
    AND_AOV_FILTER = 'defaultArnoldFilter'
    AND_AOV_DRIVER = 'defaultArnoldDriver'
    AND_DISPLAY_AOV_DRIVER = 'defaultArnoldDisplayDriver'
    AND_ALL = [
        AND_OPTIONS,
        AND_DISPLAY_AOV_DRIVER,
        AND_AOV_FILTER,
        AND_AOV_DRIVER
    ]
    def __init__(self):
        self._options_obj = _ma_dcc_obj_obj.Node(self.AND_OPTIONS)
    @classmethod
    def set_image_format(cls, image_format):
        cmds.setAttr(cls.PORT_DICT['image_format'], image_format, type='string')
    @classmethod
    def set_color_space(cls, color_space):
        cmds.setAttr(cls.PORT_DICT['color_space'], color_space)
    @classmethod
    def get(cls):
        for i in [cls.AND_OPTIONS]:
            obj = _ma_dcc_obj_obj.Node(i)
            obj_ports_opt = mya_dcc_obj_abs.ObjPortsOpt(obj.path)
            port_names = obj_ports_opt.get_port_names()
            for port_name in port_names:
                port = obj.get_port(port_name)
                print port, port.get(), port.get_default()

    def set_aa_sample(self, value):
        self._options_obj.get_port('AASamples').set(value)
