# coding:utf-8
from lxbasic import bsc_core


print bsc_core.StgFileMultiplyMtd.set_convert_to(
    '/l/temp/td/dongchangbao/tx_convert_1/nngongshifu_cloth_mask/nngongshifu_cloth_mask.1001.1012.exr',
    ['*.<udim>.####.{ext}', '*.####.{ext}']
)

print bsc_core.StgFileMultiplyMtd.set_convert_to(
    '/l/temp/td/dongchangbao/tx_convert_1/nngongshifu_cloth_mask/nngongshifu_cloth_mask.1001.exr',
    ['*.<udim>.####.{ext}', '*.####.{ext}']
)
