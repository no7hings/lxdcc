# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

from lxbasic import bsc_core

from lxutil import utl_configure, utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxmaya import ma_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects

from lxutil.fnc import utl_fnc_obj_abs

from lxmaya.fnc.exporters import _mya_fnc_ept_look


class ProxyGpuExporter(utl_fnc_obj_abs.AbsFncOptionMethod):
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
        location_dag_opt = bsc_core.DccPathDagOpt(location)
        mya_location = location_dag_opt.set_translate_to('|').get_value()
        frame = option.get('frame')
        start_frame, end_frame = mya_dcc_objects.Scene.get_frame_range(frame)
        o = ma_core.CmdMeshesOpt(mya_location)
        #
        file_ = utl_dcc_objects.OsFile(file_path)
        #
        file_.set_directory_create()
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
            utl_core.Log.set_module_result_trace(
                'gpu-export',
                'file="{}"'.format(i)
            )


class ProxyAssExporter(utl_fnc_obj_abs.AbsFncOptionMethod):
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
        location_dag_opt = bsc_core.DccPathDagOpt(location)
        mya_location = location_dag_opt.set_translate_to('|').get_value()
        frame = option.get('frame')
        start_frame, end_frame = mya_dcc_objects.Scene.get_frame_range(frame)
        #
        _mya_fnc_ept_look.LookAssExporter(
            file_path=file_path,
            root=location
        ).set_run()
