# coding:utf-8
from lxbasic import bsc_core

raw = bsc_core.StgFileOpt(
    '/job/CFG/SHOW-CFG/NSA_DEV/presets/global.storage.json'
).set_read()

bsc_core.StgFileOpt(
    '/data/f/json-temp/global.storage.yml'
).set_write(raw)
