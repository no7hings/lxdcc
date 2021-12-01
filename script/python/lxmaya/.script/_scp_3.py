# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import os

import fnmatch


class shaderConvert(object):
    MAP_0_DICT = [
        ('BiChu', 'baseColor'),
        ('BaseColor', 'baseColor'),
        ('BiChuNormal', 'normalCamera'),
    ]
    MAP_1_DICT = [
        ('BuLiaoDiSe', 'baseColor'),
    ]
    # map3
    MAP_2_DICT = [
        ('BuLiaoTex', 'baseColor'),
        ('BuLiaoNormal', 'normalCamera'),
    ]
    MAP_3_DICT = [
        ('HuaWenAbledo', 'baseColor'),
        ('HuaWenNormal', 'normalCamera'),
    ]
    MAPS = [
        (4, 'map1', MAP_0_DICT, 26),
        (3, 'map2', MAP_1_DICT, 26),
        (2, 'map3', MAP_2_DICT, 26),
        (1, 'map4', MAP_3_DICT, 26),
    ]
    VALUE_MAP_DICT = {
        '_Metallic': 'metalness',
        '_Smoothness': 'specularRoughness',
        '_SpecularColor': 'specularColor',
    }
    #
    CLR_TEX_PATTERN = '*_D.*'
    NRM_TEX_PATTERN = '*_N.*'
    MTL_TEX_PATTERN = '*_M.*'
    #
    TEX_PATTERN_DICT = {
        CLR_TEX_PATTERN: 'clr',
        NRM_TEX_PATTERN: 'nrm'
    }
    def __init__(self):
        pass
    @classmethod
    def _get_tex_type_(cls, tex):
        basename = os.path.basename(tex)
        for k, v in cls.TEX_PATTERN_DICT.items():
            if fnmatch.filter([basename], k):
                return v
    @classmethod
    def _get_tex_ext_(cls, tex):
        return os.path.splitext(tex)[-1]

    def _set_convert_by_layer_rgba_(self):
        self._convert_dict = {}
        objs = cmds.ls(type='shadingEngine')
        for mtl in objs:
            if not cmds.connectionInfo('{}.surfaceShader'.format(mtl), isExactDestination=1):
                continue
            sdr_out = cmds.connectionInfo('{}.surfaceShader'.format(mtl), sourceFromDestination=1)
            sdr = sdr_out.split('.')[0]
            if cmds.nodeType(sdr) != 'cgfxShader':
                continue
            #
            mst_sdr = '{}__mst'.format(sdr)
            if cmds.objExists(mst_sdr) is False:
                cmds.shadingNode('aiStandardSurface', name=mst_sdr, asShader=1)
            cmds.connectAttr('{}.outColor'.format(mst_sdr), '{}.aiSurfaceShader'.format(mtl), force=1)
            #
            count = len(self.MAPS)
            for i in self.MAPS:
                index, uv_set, maps, operation = i
                for src_atr_name, tgt_atr_name in maps:
                    src_attr = '{}.{}'.format(sdr, src_atr_name)
                    if not cmds.connectionInfo(src_attr, isExactDestination=1):
                        continue
                    #
                    src_img_out = cmds.connectionInfo(src_attr, sourceFromDestination=1)
                    src_img = src_img_out.split('.')[0]
                    tex = cmds.getAttr('{}.fileTextureName'.format(src_img))
                    tex_type = self._get_tex_type_(tex)
                    ext = self._get_tex_ext_(tex)
                    if tex_type is not None and tgt_atr_name is not None:
                        bsc_img = '{}__{}'.format(sdr, tex_type)
                        if cmds.objExists(bsc_img) is False:
                            cmds.shadingNode('aiLayerRgba', name=bsc_img, asShader=1)
                            cmds.setAttr('{}.enable1'.format(bsc_img), 0)
                        #
                        cmds.setAttr('{}.enable{}'.format(bsc_img, index), 1)
                        cmds.setAttr('{}.name{}'.format(bsc_img, index), src_atr_name, type='string')
                        # alpha
                        if ext.lower() == '.tga':
                            alp_rvs = '{}__alp_rvs'.format(sdr)
                            if cmds.objExists(alp_rvs) is False:
                                cmds.shadingNode('aiComplement', name=alp_rvs, asShader=1)
                                cmds.setAttr('{}.input'.format(alp_rvs), 0, 0, 0)
                            cmds.connectAttr('{}.outColor.outColorR'.format(alp_rvs), '{}.transmission'.format(mst_sdr), force=1)

                            bsc_alp = '{}__alp'.format(sdr)
                            if cmds.objExists(bsc_alp) is False:
                                cmds.shadingNode('aiLayerFloat', name=bsc_alp, asShader=1)
                                cmds.setAttr('{}.enable1'.format(bsc_alp), 0)
                                #
                            cmds.connectAttr('{}.outValue'.format(bsc_alp), '{}.input.inputR'.format(alp_rvs), force=1)
                        else:
                            bsc_alp = None
                        #
                        sub_img = '{}__{}'.format(bsc_img, index)
                        if cmds.objExists(sub_img) is False:
                            cmds.shadingNode('aiImage', name=sub_img, asShader=1)
                        cmds.setAttr('{}.filename'.format(sub_img), tex, type='string')
                        cmds.setAttr('{}.uvset'.format(sub_img), uv_set, type='string')
                        cmds.connectAttr('{}.outColor'.format(sub_img), '{}.input{}'.format(bsc_img, index), force=1)
                        if ext.lower() == '.tga':
                            cmds.setAttr('{}.operation{}'.format(bsc_img, index), 26)
                            cmds.connectAttr('{}.outAlpha'.format(sub_img), '{}.mix{}'.format(bsc_img, index), force=1)
                        # else:
                        #     if tex_type == 'clr':
                        #         cmds.setAttr('{}.operation{}'.format(bsc_img, index), operation)
                        if tex_type == 'clr':
                            cmds.connectAttr('{}.outColor'.format(bsc_img), '{}.{}'.format(mst_sdr, tgt_atr_name), force=1)
                            # alpha
                            if bsc_alp is not None:
                                cmds.setAttr('{}.enable{}'.format(bsc_alp, index), 1)
                                cmds.setAttr('{}.mix{}'.format(bsc_alp, index), 1)
                                cmds.connectAttr('{}.outAlpha'.format(sub_img), '{}.input{}'.format(bsc_alp, index), force=1)

                        elif tex_type == 'nrm':
                            tgt_nrm = '{}__nrm_inp'.format(sdr)
                            if cmds.objExists(tgt_nrm) is False:
                                cmds.shadingNode('aiNormalMap', name=tgt_nrm, asShader=1)
                            #
                            clr_img = '{}__{}__{}'.format(sdr, 'clr', index)
                            if cmds.objExists(clr_img) is True:
                                clr_txr = cmds.getAttr('{}.filename'.format(clr_img))
                                ext = self._get_tex_ext_(clr_txr)
                                if ext.lower() == '.tga':
                                    cmds.connectAttr('{}.outAlpha'.format(clr_img), '{}.mix{}'.format(bsc_img, index), force=1)
                            #
                            cmds.connectAttr('{}.outValue'.format(tgt_nrm), '{}.{}'.format(mst_sdr, tgt_atr_name), force=1)
                            cmds.connectAttr('{}.outColor'.format(bsc_img), '{}.input'.format(tgt_nrm), force=1)
            #
            # for src_atr_name, tgt_atr_name in self.VALUE_MAP_DICT.items():
            #     src_attr = '{}.{}'.format(sdr, src_atr_name)
            #     v = cmds.getAttr(src_attr)
            #     if isinstance(v, list):
            #         v = v[0]
            #     if isinstance(v, tuple):
            #         cmds.setAttr('{}.{}'.format(mst_sdr, tgt_atr_name), *v)
            #     else:
            #         cmds.setAttr('{}.{}'.format(mst_sdr, tgt_atr_name), v)
    
    def run(self):
        self._set_convert_by_layer_rgba_()


if __name__ == '__main__':
    shaderConvert().run()
    cmds.setAttr('C_01__nrm__1.uvset', 'map3', type='string')
    cmds.setAttr('C_01__clr__1.uvset', 'map3', type='string')

    cmds.setAttr('D_15__nrm__1.uvset', 'map3', type='string')
    cmds.setAttr('D_15__clr__1.uvset', 'map3', type='string')
