# coding:utf-8
import glob

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

d_ = '/depts/lookdev/ld_qiuhua/texture/megascans/surfaces/concrete/Concrete_Castinsitu_vdxicg2_4K_surface_ms'

p_ = '{key}_{size}_{tag}.{ext}'
key_ = 'vdxicg2'


def get_files(d, key):
    p = bsc_core.ParsePatternOpt(
        '{}/{}'.format(d, p_)
    )
    p.set_update(**dict(key=key))
    for i in p.get_matches():
        print i['result']


if __name__ == '__main__':
    get_files(d_, key_)


a = [ 'normal', 'bump', 'gloss', 'displacement', 'ao', 'roughness', 'cavity', 'specular', 'albedo' ]

a.sort()

print a
