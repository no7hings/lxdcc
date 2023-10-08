# coding:utf-8
from collections import OrderedDict


if __name__ == '__main__':
    from lxbasic import bsc_core

    from lxutil import utl_core

    data = bsc_core.StgFileOpt(
        '/production/library/resource/all/3d_plant_proxy/tree_a001_rsc/v0001/look/json/tree_a001_rsc.preview.json'
    ).set_read()
    r = utl_core.Jinja.get_result(
        'usda/look/preview-material-diffuse',
        data
    )

    print r

    bsc_core.StgFileOpt(
        '/production/library/resource/all/3d_plant_proxy/tree_a001_rsc/v0001/look/usd/tree_a001_rsc.preview.usda'
    ).set_write(r)
