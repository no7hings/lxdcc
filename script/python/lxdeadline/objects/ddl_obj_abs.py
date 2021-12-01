# coding:utf-8
from lxbasic import bsc_core

import lxbasic.objects as bsc_objects


class AbsDdlRsvTaskQuery(object):
    CONFIGURE_FILE_PATH = None
    @classmethod
    def _get_(cls, method_pattern, **kwargs):
        # type=method&name=database&configure=cjd&engine=houdini-python&script=set_geometry_unify_by_usd_file
        return method_pattern.format(
            **kwargs
        )
    @classmethod
    def _get_rsv_task_version_(cls, rsv_task_properties):
        if rsv_task_properties.get('shot'):
            return '{project}.{shot}.{step}.{task}.{version}'.format(**rsv_task_properties.value)
        elif rsv_task_properties.get('asset'):
            return '{project}.{asset}.{step}.{task}.{version}'.format(**rsv_task_properties.value)
        else:
            raise TypeError()

    def __init__(self, key, rsv_task_properties):
        self._key = key
        self._project = rsv_task_properties.get('project')
        self._name = self._get_rsv_task_version_(rsv_task_properties)
        #
        self._configure = bsc_objects.Configure(
            value=self.CONFIGURE_FILE_PATH
        )
        #
        self._method_option_pattern = self._configure.get(
            'option.method-option-pattern'
        )

    def get_method_option(self, **kwargs):
        kwargs_ = self._configure.get(self._key)
        return self._get_(
            self._method_option_pattern,
            name=self._name,
            configure=self._project,
            **kwargs_
        )
    @classmethod
    def get_script_option(cls, **kwargs):
        return bsc_core.KeywordArgumentsOpt._to_string_(
            **kwargs
        )
