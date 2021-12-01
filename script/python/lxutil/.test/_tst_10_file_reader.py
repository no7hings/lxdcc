# coding:utf-8
from lxutil import objects


f = objects.DotMtlxFileReader(
    file_path='/l/prod/shl/publish/assets/chr/nn_gongshifu/srf/surfacing/nn_gongshifu.srf.surfacing.v004/look/mtlx/nn_gongshifu.mtlx'
)


print f.get_geometries_properties()
