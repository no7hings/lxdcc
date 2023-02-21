# coding:utf-8
from lxbasic import bsc_core

if bsc_core.EnvExtraMtd.get_scheme() == 'default':
    bsc_core.LogMtd.trace_method_result(
        'extra script imported',
        'scheme="default"'
    )
    from .default import *
elif bsc_core.EnvExtraMtd.get_scheme() == 'new':
    bsc_core.LogMtd.trace_method_result(
        'extra script imported',
        'scheme="new"'
    )
    from .new import *

