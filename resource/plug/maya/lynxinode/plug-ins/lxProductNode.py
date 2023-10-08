# encoding=utf-8
"""
use python api 1.0
api 2.0 dont support "MPxTransform"
"""
from __future__ import division

import sys
# noinspection PyUnresolvedReferences
import maya.mel as mel
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.OpenMaya as om
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.OpenMayaMPx as ompx


def trace_error(text):
    sys.stderr.write(text)


def trace(text):
    sys.stdout.write(text)


class OmBasic(object):
    @classmethod
    def add_comp_atr(cls, long_name, short_name):
        cmp_atr = om.MFnCompoundAttribute()
        num_atr = om.MFnNumericAttribute()
        enm_atr = om.MFnEnumAttribute()
        #
        atr = cmp_atr.create(long_name, short_name)
        #
        position_atr = num_atr.create(
            long_name + '_Position', short_name + 'p',
            om.MFnNumericData.kFloat
        )
        #
        value_atr = num_atr.create(
            long_name + '_FloatValue', short_name + 'v',
            om.MFnNumericData.kFloat
        )
        #
        interp_atr = enm_atr.create(
            long_name + '_Interp', short_name + 'i'
        )
        enm_atr.addField('None', 0)
        enm_atr.addField('Linear', 1)
        enm_atr.addField('Smooth', 2)
        enm_atr.addField('Spline', 3)
        enm_atr.setDefault(3)
        cmp_atr.addChild(position_atr)
        cmp_atr.addChild(value_atr)
        cmp_atr.addChild(interp_atr)
        #
        cmp_atr.setStorable(True)
        cmp_atr.setArray(True)
        cmp_atr.usesArrayDataBuilder = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_int_atr(cls, long_name, short_name, value, maximum=None, minimum=None, soft_maximum=None, soft_minimum=None, keyable=True):
        num_atr = om.MFnNumericAttribute()
        #
        atr = num_atr.create(long_name, short_name, om.MFnNumericData.kInt, int(value))
        num_atr.setWritable(True)
        num_atr.setKeyable(keyable)
        num_atr.setStorable(True)
        num_atr.setChannelBox(True)
        if maximum is not None:
            num_atr.setMax(int(maximum))
        if minimum is not None:
            num_atr.setMin(int(minimum))
        if soft_maximum is not None:
            num_atr.setSoftMax(soft_maximum)
        if soft_minimum is not None:
            num_atr.setSoftMin(soft_minimum)
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_float_atr(cls, long_name, short_name, value=None, maximum=None, minimum=None, soft_maximum=None, soft_minimum=None, keyable=True, array=False, hidden=False):
        num_atr = om.MFnNumericAttribute()
        #
        if value is not None:
            atr = num_atr.create(long_name, short_name, om.MFnNumericData.kFloat, float(value))
        else:
            atr = num_atr.create(long_name, short_name, om.MFnNumericData.kFloat)
        #
        num_atr.setWritable(True)
        num_atr.setKeyable(keyable)
        num_atr.setStorable(True)
        num_atr.setChannelBox(True)
        if hidden is True:
            num_atr.setHidden(True)
        #
        if array is True:
            num_atr.setArray(True)
            num_atr.usesArrayDataBuilder = True
        #
        if maximum is not None:
            num_atr.setMax(float(maximum))
        if minimum is not None:
            num_atr.setMin(float(minimum))
        if soft_maximum is not None:
            num_atr.setSoftMax(float(soft_maximum))
        if soft_minimum is not None:
            num_atr.setSoftMin(float(soft_minimum))
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_bool_atr(cls, long_name, short_name, value=None, keyable=True):
        num_atr = om.MFnNumericAttribute()
        #
        if value is not None:
            atr = num_atr.create(
                long_name, short_name,
                om.MFnNumericData.kBoolean,
                value
            )
        else:
            atr = num_atr.create(
                long_name, short_name,
                om.MFnNumericData.kBoolean,
            )
        num_atr.setWritable(True)
        num_atr.setKeyable(keyable)
        num_atr.setStorable(True)
        num_atr.setChannelBox(True)
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_enumerate_atr(cls, long_name, short_name, values, value=None, keyable=True):
        enm_atr = om.MFnEnumAttribute()
        #
        atr = enm_atr.create(long_name, short_name, 0)
        for seq, i in enumerate(values):
            enm_atr.addField(i, seq)

        if value is not None:
            enm_atr.setDefault(value)
        #
        enm_atr.setWritable(True)
        enm_atr.setKeyable(keyable)
        enm_atr.setStorable(True)
        enm_atr.setChannelBox(True)
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_point_atr(cls, long_name, short_name, value=None, keyable=True, array=False, array_builder=False):
        num_atr = om.MFnNumericAttribute()
        #
        atr = num_atr.createPoint(long_name, short_name)
        #
        num_atr.setWritable(True)
        num_atr.setKeyable(keyable)
        num_atr.setStorable(True)
        num_atr.setChannelBox(True)
        if value is not None:
            num_atr.setDefault(value)
        if array is True:
            num_atr.setArray(True)
            if array_builder is True:
                num_atr.usesArrayDataBuilder = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_geometry_atr(cls, long_name, short_name, geometry_type, array=False):
        typ_atr = om.MFnTypedAttribute()
        atr = typ_atr.create(
            long_name, short_name,
            geometry_type
        )
        typ_atr.setHidden(True)
        typ_atr.setWritable(True)
        typ_atr.setStorable(True)
        if array is True:
            typ_atr.setArray(True)
            # typ_atr.usesArrayDataBuilder = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_message_atr(cls, long_name, short_name):
        msg_atr = om.MFnMessageAttribute()
        atr = msg_atr.create(
            long_name, short_name
        )
        msg_atr.setWritable(True)
        msg_atr.setStorable(True)
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_string_atr(cls, long_name, short_name, value=None, array=False, writable=True, channel_box=False, use_as_file=False):
        typ_atr = om.MFnTypedAttribute()
        if value is not None:
            s = om.MFnStringData()
            s_value = s.create(value)
            atr = typ_atr.create(
                long_name, short_name,
                om.MFnData.kString,
                s_value
            )
        else:
            atr = typ_atr.create(
                long_name, short_name,
                om.MFnData.kString
            )
        typ_atr.writable = writable
        typ_atr.setStorable(True)
        if array is True:
            typ_atr.setArray(True)
            # typ_atr.usesArrayDataBuilder = True
        if channel_box is True:
            typ_atr.setChannelBox(True)
        if use_as_file is True:
            typ_atr.setUsedAsFilename(True)
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_comp_curve_array_atr(cls, long_name, short_name):
        cmp_atr = om.MFnCompoundAttribute()
        typ_atr = om.MFnTypedAttribute()
        num_atr = om.MFnNumericAttribute()
        #
        atr = cmp_atr.create(long_name, short_name)
        #
        curve_atr = typ_atr.create(
            long_name + 'Curve', short_name + 'c',
            om.MFnData.kNurbsCurve
        )
        #
        position_atr = num_atr.create(
            long_name + 'Position', short_name + 'p',
            om.MFnNumericData.kFloat
        )
        cmp_atr.addChild(curve_atr)
        cmp_atr.addChild(position_atr)
        #
        cmp_atr.setStorable(True)
        cmp_atr.setArray(True)
        # cmp_atr.usesArrayDataBuilder = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def set_atrs_connect(cls, ss, ts):
        for s in ss:
            for t in ts:
                # noinspection PyUnresolvedReferences
                cls.attributeAffects(
                    s, t,
                )


class AssetRootNodeTransformMatrix(ompx.MPxTransformationMatrix):
    ID = om.MTypeId(0x8709F)
    @classmethod
    def _create_fnc_(cls):
        return ompx.asMPxPtr(cls())


# node for asset
class AssetRootNode(
    ompx.MPxTransform,
    OmBasic,
):
    NAME = 'assetRoot'
    ID = om.MTypeId(0x8709E)
    # asset
    rsv_task = om.MObject()
    project = om.MObject()
    project_id = om.MObject()
    asset = om.MObject()
    asset_id = om.MObject()
    task = om.MObject()
    task_id = om.MObject()
    version = om.MObject()
    version_id = om.MObject()
    user = om.MObject()
    update = om.MObject()
    #
    version_extra = om.MObject()
    # cache
    asset_cache_file = om.MObject()
    asset_cache_location = om.MObject()
    asset_cache_root = om.MObject()
    #
    asset_shot = om.MObject()
    asset_namespace = om.MObject()
    # asset version
    asset_model_version = om.MObject()
    asset_groom_version = om.MObject()
    asset_effect_version = om.MObject()
    asset_rig_version = om.MObject()
    asset_surface_version = om.MObject()
    asset_light_version = om.MObject()
    asset_camera_version = om.MObject()
    #   asset version override
    asset_model_version_override = om.MObject()
    asset_groom_version_override = om.MObject()
    asset_effect_version_override = om.MObject()
    asset_rig_version_override = om.MObject()
    asset_surface_version_override = om.MObject()
    asset_light_version_override = om.MObject()
    # shot version
    shot_animation_version = om.MObject()
    shot_character_effect_version = om.MObject()
    shot_effect_version = om.MObject()
    shot_light_version = om.MObject()
    shot_camera_version = om.MObject()
    #   shot version override
    shot_animation_version_override = om.MObject()
    shot_character_effect_version_override = om.MObject()
    shot_effect_version_override = om.MObject()
    shot_light_version_override = om.MObject()
    shot_camera_version_override = om.MObject()
    # asset dcc
    asset_dcc_data = om.MObject()
    shot_asset_dcc_data = om.MObject()
    #
    shot_asst_dcc_file = om.MObject()
    # options
    #   time sample override
    start_frame = om.MObject()
    end_frame = om.MObject()
    frame_offset = om.MObject()
    frame_loop_enable = om.MObject()
    #
    frame_override_enable = om.MObject()
    start_frame_override = om.MObject()
    end_frame_override = om.MObject()
    #
    label = om.MObject()
    description = om.MObject()
    tag = om.MObject()
    metadata = om.MObject()
    #
    ae_build_data = om.MObject()
    button_script_data = om.MObject()
    #
    asset_cache_variant_data = om.MObject()
    asset_cache_variant_record_data = om.MObject()
    asset_dcc_hash_data = om.MObject()
    asset_cache_hash_data = om.MObject()
    @classmethod
    def _initializer_fnc_(cls):
        cls.rsv_task = cls.add_string_atr(
            'rsv_task', 'rsv_tsk_',
        )
        cls.project = cls.add_string_atr(
            'project', 'prj_',
        )
        cls.project_id = cls.add_string_atr(
            'project_id', 'prj_id_',
        )
        #
        cls.asset = cls.add_string_atr(
            'asset', 'ast_',
        )
        cls.asset_id = cls.add_string_atr(
            'asset_id', 'ast_id_',
        )
        #
        cls.task = cls.add_string_atr(
            'task', 'tsk_',
        )
        cls.task_id = cls.add_string_atr(
            'task_id', 'tsk_id_',
        )
        #
        cls.version = cls.add_string_atr(
            'version', 'vsn_',
        )
        cls.version_id = cls.add_string_atr(
            'version_id', 'vsn_id_',
        )
        #
        cls.version_extra = cls.add_string_atr(
            'version_extra', 'vsn_etr_',
        )
        cls.user = cls.add_string_atr(
            'user', 'usr_',
        )
        cls.user_id = cls.add_string_atr(
            'user_id', 'usr_id_',
        )
        cls.update = cls.add_string_atr(
            'update', 'upt_',
        )
        # dcc
        cls.asset_dcc_data = cls.add_string_atr(
            'asset_dcc_data', 'ast_dcc_dta',
            value='{}'
        )
        cls.shot_asset_dcc_data = cls.add_string_atr(
            'shot_asset_dcc_data', 'ast_dcc_sot_dta',
            value='{}'
        )
        # usd
        cls.asset_cache_file = cls.add_string_atr(
            'asset_cache_file', 'ast_cch_fle'
        )
        cls.asset_cache_location = cls.add_string_atr(
            'asset_cache_location', 'ast_cch_lcn',
        )
        cls.asset_cache_root = cls.add_string_atr(
            'asset_cache_root', 'ast_cch_rot',
        )
        cls.asset_shot = cls.add_string_atr(
            'asset_shot', 'ast_sot',
            value='None'
        )
        cls.asset_namespace = cls.add_string_atr(
            'asset_namespace', 'ast_sot_ast',
            value='None'
        )
        #   asset version
        cls.asset_model_version = cls.add_string_atr(
            'asset_model_version', 'ast_mdl_vsn',
            value='None'
        )
        cls.asset_groom_version = cls.add_string_atr(
            'asset_groom_version', 'ast_grm_vsn',
            value='None'
        )
        cls.asset_effect_version = cls.add_string_atr(
            'asset_effect_version', 'ast_efx_vsn',
            value='None'
        )
        cls.asset_rig_version = cls.add_string_atr(
            'asset_rig_version', 'ast_rig_vsn',
            value='None'
        )
        cls.asset_surface_version = cls.add_string_atr(
            'asset_surface_version', 'ast_srf_vsn',
            value='None'
        )
        cls.asset_light_version = cls.add_string_atr(
            'asset_light_version', 'ast_lgt_vsn',
            value='None'
        )
        cls.asset_camera_version = cls.add_string_atr(
            'asset_camera_version', 'ast_cmr_vsn',
            value='None'
        )
        #   asset version override
        cls.asset_model_version_override = cls.add_string_atr(
            'asset_model_version_override', 'ast_mdl_vsn_ovr',
            value='None'
        )
        cls.asset_groom_version_override = cls.add_string_atr(
            'asset_groom_version_override', 'ast_grm_vsn_ovr',
            value='None'
        )
        cls.asset_effect_version_override = cls.add_string_atr(
            'asset_effect_version_override', 'ast_efx_vsn_ovr',
            value='None'
        )
        cls.asset_rig_version_override = cls.add_string_atr(
            'asset_rig_version_override', 'ast_rig_vsn_ovr',
            value='None'
        )
        cls.asset_surface_version_override = cls.add_string_atr(
            'asset_surface_version_override', 'ast_srf_vsn_ovr',
            value='None'
        )
        cls.asset_light_version_override = cls.add_string_atr(
            'asset_light_version_override', 'ast_lgt_vsn_ovr',
            value='None'
        )
        cls.asset_camera_version_override = cls.add_string_atr(
            'asset_camera_version_override', 'ast_cmr_vsn_ovr',
            value='None'
        )
        #   shot version
        cls.shot_animation_version = cls.add_string_atr(
            'shot_animation_version', 'sot_anm_vsn',
            value='None'
        )
        cls.shot_character_effect_version = cls.add_string_atr(
            'shot_character_effect_version', 'sot_cfx_vsn',
            value='None'
        )
        cls.shot_effect_version = cls.add_string_atr(
            'shot_effect_version', 'sot_efx_vsn',
            value='None'
        )
        cls.shot_light_version = cls.add_string_atr(
            'shot_light_version', 'sot_lgt_vsn',
            value='None'
        )
        cls.shot_camera_version = cls.add_string_atr(
            'shot_camera_version', 'sot_cmr_vsn',
            value='None'
        )
        #   shot version override
        cls.shot_animation_version_override = cls.add_string_atr(
            'shot_animation_version_override', 'sot_anm_vsn_ovr',
            value='None'
        )
        cls.shot_character_effect_version_override = cls.add_string_atr(
            'shot_character_effect_version_override', 'sot_cfx_vsn_ovr',
            value='None'
        )
        cls.shot_effect_version_override = cls.add_string_atr(
            'shot_effect_version_override', 'sot_efx_vsn_ovr',
            value='None'
        )
        cls.shot_light_version_override = cls.add_string_atr(
            'shot_light_version_override', 'sot_lgt_vsn_ovr',
            value='None'
        )
        cls.shot_camera_version_override = cls.add_string_atr(
            'shot_camera_version_override', 'sot_cmr_vsn_ovr',
            value='None'
        )
        # options
        #   frame
        cls.start_frame = cls.add_float_atr(
            'start_frame', 'str_frm'
        )
        cls.end_frame = cls.add_float_atr(
            'end_frame', 'end_frm'
        )
        cls.frame_offset = cls.add_float_atr(
            'frame_offset', 'frm_ofs'
        )
        cls.frame_loop_enable = cls.add_bool_atr(
            'frame_loop_enable', 'frm_lop_enb'
        )
        #   override frame
        cls.frame_override_enable = cls.add_bool_atr(
            'frame_override_enable', 'frm_ovr_enb'
        )
        cls.start_frame_override = cls.add_float_atr(
            'start_frame_override', 'str_frm_ovr'
        )
        cls.end_frame_override = cls.add_float_atr(
            'end_frame_override', 'end_frm_ovr'
        )
        # extra
        cls.label = cls.add_string_atr(
            'label', 'lbl_'
        )
        cls.description = cls.add_string_atr(
            'description', 'dsp_'
        )
        cls.tag = cls.add_string_atr(
            'tag', 'tag_'
        )
        cls.metadata = cls.add_string_atr(
            'metadata', 'mtd_'
        )
        #
        cls.ae_build_data = cls.add_string_atr(
            'ae_build_data', 'ae_bld_scp',
            value='{}'
        )
        cls.button_script_data = cls.add_string_atr(
            'button_script_data', 'btn_scp_dta',
            value='{}'
        )
        cls.asset_dcc_hash_data = cls.add_string_atr(
            'asset_dcc_hash_data', 'dcc_hsh_dta',
            value='{}'
        )
        cls.asset_cache_hash_data = cls.add_string_atr(
            'asset_cache_hash_data', 'cch_hsh_dta',
            value='{}'
        )
        cls.asset_cache_variant_data = cls.add_string_atr(
            'asset_cache_variant_data', 'vrn_dta',
            value='{}'
        )
        cls.asset_cache_variant_record_data = cls.add_string_atr(
            'asset_cache_variant_record_data', 'ast_dcc_vsn_dta',
            value='{}'
        )
    @classmethod
    def _create_fnc_(cls):
        return ompx.asMPxPtr(cls())


# initialize
def initializePlugin(obj):
    om_plug = ompx.MFnPlugin(obj, 'paper game', '1.0.0', 'Any')
    #
    node_args = [
        (
            AssetRootNode.NAME,
            AssetRootNode.ID,
            AssetRootNode._create_fnc_,
            AssetRootNode._initializer_fnc_,
            #
            AssetRootNodeTransformMatrix._create_fnc_,
            AssetRootNodeTransformMatrix.ID,
        ),
    ]
    for i_node_args in node_args:
        try:
            # resister transform
            om_plug.registerTransform(*i_node_args)
        except:
            trace_error('failed to register node: "{}"'.format(i_node_args[0]))
            raise


# uninitialize
def uninitializePlugin(obj):
    om_plug = ompx.MFnPlugin(obj)
    #
    node_args = [
        (
            AssetRootNode.NAME,
            AssetRootNode.ID,
        ),
    ]
    for i_node_args in node_args:
        # Deregister Node
        try:
            om_plug.deregisterNode(
                i_node_args[1]
            )
        except:
            trace_error('failed to deregister node: "{}"'.format(i_node_args[0]))
            raise
