# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects

f = '/data/f/texture-collection/copy/tx/nn4_nail.diff_clr.1001.tx'

utl_dcc_objects.OsTexture(
    f
).copy_unit_as_base_link_with_src(
    '/data/f/texture-collection/base_copy/base',
    '/data/f/texture-collection/base_copy/v001'
)


f = '/data/f/texture-collection/copy_01/nn4_body_dark.close.sss_clr.1001.tx'

utl_dcc_objects.OsTexture(
    f
).copy_unit_as_base_link_with_src(
    '/data/f/texture-collection/base_copy/base',
    '/data/f/texture-collection/base_copy/v001'
)
