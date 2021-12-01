# coding:utf-8
import collections

from LxGraphic import grhCfg

from LxMtx import mtxObjects

import lxutil.dcc.dcc_objects as utl_dcc_objects


def set_translate_data_create(file_path):
    query_raw_creator = mtxObjects.GRH_OBJ_QUERYRAW_CREATOR
    dic = collections.OrderedDict()
    type_paths = query_raw_creator.typepaths()
    for tgt_type_path in type_paths:
        tgtNodeQueryraw = query_raw_creator.nodeQueryraw(tgt_type_path)

        node_dict = collections.OrderedDict()
        if tgt_type_path == 'material':
            src_type_path = u'lynxi/material'
        elif tgt_type_path == 'mesh':
            src_type_path = u'lynxi/mesh'
        else:
            src_type_path = u'shader/{}'.format(tgt_type_path)

        dic[src_type_path] = node_dict
        node_dict[grhCfg.GrhUtility.DEF_grh__keyword_target_typepath] = tgt_type_path

        sourcePortDic = collections.OrderedDict()
        node_dict[grhCfg.GrhUtility.DEF_grh__keyword_port_converter] = sourcePortDic
        for tgtPortQueryrawObject in tgtNodeQueryraw.portQueryraws():
            tgtAssignStr = tgtPortQueryrawObject.port_assign
            portDic = collections.OrderedDict()
            tgtPortpathStr = tgtPortQueryrawObject.portpath

            if tgtAssignStr in [grhCfg.GrhUtility.DEF_grh__keyword__inport]:
                srcPortpathStr = 'inputs:{}'.format(tgtPortQueryrawObject.portpath)
            elif tgtAssignStr in [grhCfg.GrhUtility.DEF_grh__keyword__inport_channel]:
                srcPortpathStr = 'inputs:{}'.format(tgtPortQueryrawObject.portpath)
            elif tgtAssignStr in [grhCfg.GrhUtility.DEF_grh__keyword__otport]:
                srcPortpathStr = 'outputs:{}'.format(tgtPortQueryrawObject.portpath)
            elif tgtAssignStr in [grhCfg.GrhUtility.DEF_grh__keyword__otport_channel]:
                srcPortpathStr = 'outputs:{}'.format(tgtPortQueryrawObject.portpath)
            #
            elif tgtAssignStr in [grhCfg.GrhUtility.DEF_grh__keyword__property]:
                srcPortpathStr = 'inputs:{}'.format(tgtPortQueryrawObject.portpath)
            elif tgtAssignStr in [grhCfg.GrhUtility.DEF_grh__keyword__visibility]:
                srcPortpathStr = 'inputs:{}'.format(tgtPortQueryrawObject.portpath)
            else:
                srcPortpathStr = None
            if srcPortpathStr is not None:
                sourcePortDic[srcPortpathStr] = portDic
                portDic[grhCfg.GrhUtility.DEF_grh__keyword_target_portpath] = tgtPortpathStr
    utl_dcc_objects.OsJsonFile(
        file_path
    ).set_write(dic)


if __name__ == '__main__':
    set_translate_data_create('/data/f/materialx_test/ar2mtx_0.json')
