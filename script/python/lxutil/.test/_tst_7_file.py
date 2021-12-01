# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects

f = utl_dcc_objects.OsMultiplyFile(
    '/l/prod/cg7/publish/shots/z88/z88030/efx/efx/z88030.efx.efx.v006/cache/fire/bgeo_sc/fire.$F.bgeo.sc'
)

print f.get_has_elements()
