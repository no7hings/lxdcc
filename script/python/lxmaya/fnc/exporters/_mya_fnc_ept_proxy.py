# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

import lxbasic.core as bsc_core

from lxutil import utl_configure, utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxmaya import ma_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects

from lxutil.fnc import utl_fnc_obj_abs

from lxmaya.fnc.exporters import _mya_fnc_ept_look


class ProxyGpuExporter(utl_fnc_obj_abs.AbsFncOptionBase):
    # cmds.gpuCache(
    #     nodepathString,
    #     startTime=startFrame, endTime=endFrame,
    #     optimize=1, optimizationThreshold=40000,
    #     writeMaterials=withMaterial, dataFormat='ogawa',
    #     directory=path,
    #     fileName=fileName
    # )
    PLUG_NAME = 'gpuCache'
    OPTION = dict(
        file='',
        location='',
        frame=None,
    )
    def __init__(self, option=None):
        super(ProxyGpuExporter, self).__init__(option)
    @classmethod
    def _set_cmd_run_(cls, *args, **kwargs):
        """
        :param j: str
        :return: None
        """
        cmds.loadPlugin(cls.PLUG_NAME, quiet=1)
        return cmds.gpuCache(*args, **kwargs)

    def set_run(self):
        option = self.get_option()
        #
        file_path = option.get('file')
        location = option['location']
        location_dag_opt = bsc_core.PthNodeOpt(location)
        mya_location = location_dag_opt.translate_to('|').get_value()
        frame = option.get('frame')
        start_frame, end_frame = mya_dcc_objects.Scene.get_frame_range(frame)
        o = ma_core.CmdMeshesOpt(mya_location)
        #
        file_ = utl_dcc_objects.OsFile(file_path)
        #
        file_.create_directory()
        #
        args = []
        kwargs = dict(
            startTime=start_frame,
            endTime=end_frame,
            optimize=True,
            optimizationThreshold=o.get_evaluate()['face']*2,
            dataFormat='ogawa',
            directory=file_.directory.path,
            fileName=file_.name_base
        )
        args.append(mya_location)

        results = self._set_cmd_run_(*args, **kwargs)

        for i in results:
            bsc_core.Log.trace_method_result(
                'gpu-export',
                'file="{}"'.format(i)
            )


class ProxyAssExporter(utl_fnc_obj_abs.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        frame=None,
    )
    def __init__(self, option=None):
        super(ProxyAssExporter, self).__init__(option)

    def set_run(self):
        option = self.get_option()
        #
        file_path = option.get('file')
        location = option['location']
        location_dag_opt = bsc_core.PthNodeOpt(location)
        mya_location = location_dag_opt.translate_to('|').get_value()
        frame = option.get('frame')
        start_frame, end_frame = mya_dcc_objects.Scene.get_frame_range(frame)
        #
        _mya_fnc_ept_look.FncLookAssExporter(
            option=dict(
                file=file_path,
                location=location,
                texture_use_environ_map=True,
            ),
        ).execute()
    @classmethod
    def _set_color_correct_create_(cls):
        def set_user_data_rgb_over_create_fnc_(osl_color_correct_):
            _node = mya_dcc_objects.Shader('{}__user_data__rgb_over'.format(osl_color_correct_.path))
            _, _is_create = _node.get_dcc_instance('aiUserDataColor')
            if _is_create is True:
                _node.get_port('attribute').set('pg_rgb_over')
                _node.get_port('default').set([0, 0, 0])
                #
                osl_color_correct_.get_port('rgb_over').set_source(_node.get_port('outColor'))

        def set_user_data_hsv_offset_create_fnc_(osl_color_correct_):
            _node = mya_dcc_objects.Shader('{}__user_data__hsv_offset'.format(osl_color_correct_.path))
            _, _is_create = _node.get_dcc_instance('aiUserDataColor')
            if _is_create is True:
                _node.get_port('attribute').set('pg_hsv_offset')
                _node.get_port('default').set([.5, .5, .5])
                #
                osl_color_correct_.get_port('h_offset').set_source(_node.get_port('outColor.outColorR'))
                osl_color_correct_.get_port('s_offset').set_source(_node.get_port('outColor.outColorG'))
                osl_color_correct_.get_port('v_offset').set_source(_node.get_port('outColor.outColorB'))

        _ = mya_dcc_objects.Nodes(['aiStandardSurface'])
        for i in _.get_objs():
            i_color_port = i.get_port('base_color')
            i_source_obj = i_color_port.get_source_obj()
            if i_source_obj.type_name == 'osl_color_correct':
                print i
            else:
                i_source = i_color_port.get_source()
                i_osl_color_correct = mya_dcc_objects.Shader(
                    '{}__osl_color_correct'.format(i.path)
                )
                _, is_create = i_osl_color_correct.get_dcc_instance('osl_color_correct')
                if is_create is True:
                    i_osl_color_correct._update_path_()
                    i_input_port = i_osl_color_correct.get_port('input')
                    i_output_port = i_osl_color_correct.get_port('outColor')
                    i_input_port.set_source(i_source)
                    i_color_port.set_source_disconnect()
                    i_color_port.set_source(i_output_port)
                    #
                    set_user_data_rgb_over_create_fnc_(i_osl_color_correct)
                    set_user_data_hsv_offset_create_fnc_(i_osl_color_correct)


