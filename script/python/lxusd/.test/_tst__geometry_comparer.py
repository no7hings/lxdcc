# coding:utf-8
from lxutil import utl_configure

import lxusd.fnc.comparers as usd_fnc_comparers

print usd_fnc_comparers.FncGeometryComparer(
    option=dict(
        file_src='/l/prod/cgm/publish/assets/flg/xiangzhang_tree_g/mod/modeling/xiangzhang_tree_g.mod.modeling.v003/cache/usd/geo/hi.usd',
        file_tgt='/l/prod/cgm/publish/assets/flg/xiangzhang_tree_g/mod/mod_dynamic/xiangzhang_tree_g.mod.mod_dynamic.v001/cache/usd/geo/hi.usd',
        location='/master/hi'
    )
).get_results(
    check_status_includes=[
        utl_configure.DccMeshCheckStatus.ADDITION,
        utl_configure.DccMeshCheckStatus.DELETION,
        #
        utl_configure.DccMeshCheckStatus.PATH_CHANGED,
        utl_configure.DccMeshCheckStatus.PATH_EXCHANGED,
        #
        utl_configure.DccMeshCheckStatus.FACE_VERTICES_CHANGED
    ]
)
