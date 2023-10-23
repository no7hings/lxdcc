# coding:utf-8
import lxlog.core as log_core

from lxbasic import bsc_core


def get_module(framework_scheme):
    return bsc_core.PyModule(
        'lxbasic.extra.methods.{}'.format(framework_scheme)
    ).get_module()


if bsc_core.EnvExtraMtd.get_scheme() == 'default':
    log_core.Log.trace_method_result(
        'extra script',
        'load scheme: "default"'
    )
    from .default import *
elif bsc_core.EnvExtraMtd.get_scheme() == 'new':
    log_core.Log.trace_method_result(
        'extra script',
        'load scheme: "new"'
    )
    from .new import *
else:
    log_core.Log.trace_method_result(
        'extra script',
        'load scheme: "new"'
    )
    from .default import *

