# coding:utf-8


if __name__ == '__main__':
    import lxbasic.core as bsc_core

    import lxresource.core as rsc_core

    data = bsc_core.StgFileOpt(
        '/production/library/resource/all/3d_plant_proxy/tree_a001_rsc/v0001/look/json/tree_a001_rsc.preview.json'
    ).set_read()
    r = rsc_core.ResourceJinja.get_result(
        'usda/look/preview-material-diffuse',
        data
    )

    print r

    bsc_core.StgFileOpt(
        '/production/library/resource/all/3d_plant_proxy/tree_a001_rsc/v0001/look/usd/tree_a001_rsc.preview.usda'
    ).set_write(r)
