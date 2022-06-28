# coding:utf-8
import cProfile

import glob

import fnmatch

import os

import scandir


def test():
    return glob.glob(
        '/l/temp/td/dongchangbao/tx_convert_test/tx_22/jiguang_cloth_mask.[0-9][0-9][0-9][0-9].[0-9][0-9][0-9][0-9].exr'
    )


def test_1():
    f = '/l/temp/td/dongchangbao/tx_convert_test/tx_22/jiguang_cloth_mask.[0-9][0-9][0-9][0-9].[0-9][0-9][0-9][0-9].tx'
    return fnmatch.filter(
        [i.path for i in scandir.scandir(os.path.dirname(f))], f
    )


# cProfile.run("test()")
cProfile.run("test_1()")
