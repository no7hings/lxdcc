# coding:utf-8
import lxbasic.core as bsc_core


def get_module(framework_scheme):
    return bsc_core.PyModule(
        'lxutil.extra.methods.{}'.format(framework_scheme)
    ).get_module()


if bsc_core.EnvExtraMtd.get_scheme() == 'default':
    bsc_core.Log.trace_method_result(
        'extra script',
        'load scheme: "default"'
    )
    from .default import *
elif bsc_core.EnvExtraMtd.get_scheme() == 'new':
    bsc_core.Log.trace_method_result(
        'extra script',
        'load scheme: "new"'
    )
    from .new import *
else:
    bsc_core.Log.trace_method_result(
        'extra script',
        'load scheme: "new"'
    )
    from .default import *

