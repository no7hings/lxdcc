# coding:utf-8
from lxutil import scripts

r = scripts.ShotReader('d10010')

fs = r.scene_file_paths
if fs:
    f = fs[-1]
    r.set_manifest_create(f)


