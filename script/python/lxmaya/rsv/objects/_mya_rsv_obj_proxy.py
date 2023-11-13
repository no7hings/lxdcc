# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccProxyHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccProxyHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_proxy_xarc_export(self):
        from lxbasic import bsc_core
        #
        import lxutil.fnc.exporters as utl_fnc_exporters
        #
        from lxutil import utl_core
        #
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        #
        import lxmaya.fnc.exporters as mya_fnc_exporters
        #
        asset = self._rsv_scene_properties.get('asset')
        version = self._rsv_scene_properties.get('version')
        model_location = self._rsv_scene_properties.get('dcc.renderable.model.high')
        dcc_model_location = bsc_core.DccPathDagOpt(model_location).translate_to('|').get_value()
        dcc_model_group = mya_dcc_objects.Group(dcc_model_location)
        if dcc_model_group.get_is_exists() is True:
            act = 'static'
            for i_look_pass in ['default']:
                i_name = '{}.{}.{}'.format(asset, i_look_pass, act)
                i_color = bsc_core.RawTextOpt(i_name).to_rgb(maximum=1)
                i_xarc_option = dict(
                    name=i_name,
                    color=i_color,
                )
                i_gpu_files = []
                i_ass_files = []
                #
                i_proxy_jpg_sub_file = self._rsv_task.get_rsv_unit(
                    keyword='asset-proxy-jpg-sub-file',
                )
                i_proxy_jpg_sub_file_path = i_proxy_jpg_sub_file.get_result(
                    version=version,
                    variants_extend=dict(
                        look_pass=i_look_pass
                    )
                )
                #
                i_xarc_option['jpg_file'] = i_proxy_jpg_sub_file_path
                #
                i_proxy_gpu_act_file = self._rsv_task.get_rsv_unit(
                    keyword='asset-proxy-gpu-sub-act-file'
                )
                i_proxy_gpu_act_file_path = i_proxy_gpu_act_file.get_result(
                    version=version,
                    variants_extend=dict(
                        look_pass=i_look_pass,
                        act=act
                    )
                )
                mya_fnc_exporters.ProxyGpuExporter(
                    option=dict(
                        file=i_proxy_gpu_act_file_path,
                        location=model_location
                    )
                ).set_run()
                #
                i_gpu_files.append(i_proxy_gpu_act_file_path)
                #
                i_proxy_ass_var_file = self._rsv_task.get_rsv_unit(
                    keyword='asset-proxy-ass-sub-act-file'
                )
                i_proxy_ass_var_file_path = i_proxy_ass_var_file.get_result(
                    version=version,
                    variants_extend=dict(
                        look_pass=i_look_pass,
                        act=act
                    )
                )
                mya_fnc_exporters.ProxyAssExporter(
                    option=dict(
                        file=i_proxy_ass_var_file_path,
                        location=model_location
                    )
                ).set_run()
                #
                i_ass_files.append(i_proxy_ass_var_file_path)
                #
                for j_lod in range(2):
                    j_proxy_gpu_act_lod_file = self._rsv_task.get_rsv_unit(
                        keyword='asset-proxy-gpu-sub-act-lod-file'
                    )
                    j_proxy_gpu_act_lod_file_path = j_proxy_gpu_act_lod_file.get_result(
                        version=version,
                        variants_extend=dict(
                            look_pass=i_look_pass,
                            act=act,
                            lod=str(j_lod + 1).zfill(2)
                        )
                    )
                    #
                    i_gpu_files.append(j_proxy_gpu_act_lod_file_path)
                    #
                    # ma_core.CmdMeshesOpt(dcc_model_location).set_reduce_by(.5)
                    #
                    mya_fnc_exporters.ProxyGpuExporter(
                        option=dict(
                            file=j_proxy_gpu_act_lod_file_path,
                            location=model_location
                        )
                    ).set_run()
                    #
                    j_proxy_ass_var_lod_file = self._rsv_task.get_rsv_unit(
                        keyword='asset-proxy-ass-sub-act-lod-file'
                    )
                    j_proxy_ass_var_lod_file_path = j_proxy_ass_var_lod_file.get_result(
                        version=version,
                        variants_extend=dict(
                            look_pass=i_look_pass,
                            act=act,
                            lod=str(j_lod + 1).zfill(2)
                        )
                    )
                    mya_fnc_exporters.ProxyAssExporter(
                        option=dict(
                            file=j_proxy_ass_var_lod_file_path,
                            location=model_location
                        )
                    ).set_run()
                    #
                    i_ass_files.append(j_proxy_ass_var_lod_file_path)
                #
                i_proxy_xarc_sub_act_file = self._rsv_task.get_rsv_unit(
                    keyword='asset-proxy-xarc-sub-act-file',
                )
                i_xarc_option['gpu_files'] = i_gpu_files
                i_xarc_option['ass_files'] = i_ass_files
                #
                i_proxy_xarc_sub_act_file_path = i_proxy_xarc_sub_act_file.get_result(
                    version=version,
                    variants_extend=dict(
                        act=act,
                        look_pass=i_look_pass
                    )
                )
                i_xarc_option['file'] = i_proxy_xarc_sub_act_file_path
                #
                utl_fnc_exporters.DotXarcExporter(
                    option=i_xarc_option
                ).set_run()
        else:
            bsc_core.Log.trace_method_error(
                'proxy-xarc export',
                'obj="{}" is non-exists'.format(dcc_model_group.path)
            )
