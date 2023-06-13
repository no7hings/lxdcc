# coding:utf-8
from lxbasic import bsc_core
# noinspection PyUnresolvedReferences
import lxbasic.objects as bsc_objects


def get_module(framework_scheme):
    return bsc_objects.PyModule(
        'lxutil.extra.methods.{}'.format(framework_scheme)
    ).get_module()


if bsc_core.EnvExtraMtd.get_scheme() == 'default':
    bsc_core.LogMtd.trace_method_result(
        'extra script',
        'load scheme: "default"'
    )
    from .default import *
elif bsc_core.EnvExtraMtd.get_scheme() == 'new':
    bsc_core.LogMtd.trace_method_result(
        'extra script',
        'load scheme: "new"'
    )
    from .new import *
else:
    bsc_core.LogMtd.trace_method_result(
        'extra script',
        'load scheme: "default"'
    )
    from .default import *

