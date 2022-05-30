# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects

import cProfile


def test():
    t = utl_dcc_objects.OsTexture(
        '/data/f/tx_create_debug/test_1/jiguang_cloth_mask.<udim>.%04d.tx'
        # '/data/f/tx_create_debug/test_1//jiguang_cloth_mask.1001.1001.tx'
    )
    print t.get_tx_is_exists()


test()

# cProfile.run(test())
