# coding:utf-8
import cProfile

import lxutil.dcc.dcc_objects as utl_dcc_objects


def test():
    print len(utl_dcc_objects.OsFile._get_exists_file_paths_('/l/temp/td/dongchangbao/tx_convert_test/exr/jiguang_cloth_mask.<udim>.####.exr'))


def test_1():
    print len(utl_dcc_objects.OsFile._get_exists_file_paths__('/l/temp/td/dongchangbao/tx_convert_test/exr/jiguang_cloth_mask.<udim>.####.exr'))


def test_2():
    print len(utl_dcc_objects.OsFile.get_exists_unit_paths_fnc('/l/temp/td/dongchangbao/tx_convert_test/exr/jiguang_cloth_mask.<udim>.####.exr'))


# cProfile.run("test()")
# cProfile.run("test_1()")
cProfile.run("test_2()")

