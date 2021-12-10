# coding:utf-8
from lxbasic import bsc_core

import lxbasic.objects as bsc_objects


class AbsDdlQuery(object):
    CONFIGURE_FILE_PATH = None
    @classmethod
    def _get_option_(cls, option_pattern, **option_kwargs):
        # type=method&name=database&configure=cjd&engine=houdini-python&script=set_geometry_unify_by_usd_file
        return option_pattern.format(
            **option_kwargs
        )
    @classmethod
    def get_script_option(cls, **kwargs):
        return bsc_core.KeywordArgumentsOpt._to_string_(
            **kwargs
        )
    #
    def __init__(self, key, extend_option_kwargs=None):
        self._configure = bsc_objects.Configure(
            value=self.CONFIGURE_FILE_PATH
        )
        #
        self._method_option_pattern = self._configure.get(
            'option.method-option-pattern'
        )
        #
        self._key = key
        self._extend_option_kwargs = dict(
            configure='default'
        )
        if extend_option_kwargs is not None:
            self._extend_option_kwargs.update(extend_option_kwargs)

    def get_method_option(self, **kwargs):
        option_kwargs = self._configure.get(self._key)
        option_kwargs.update(
            self._extend_option_kwargs
        )
        return self._get_option_(
            self._method_option_pattern,
            **option_kwargs
        )


class AbsDdlMethodQuery(AbsDdlQuery):
    def __init__(self, key, extend_option_kwargs=None):
        super(AbsDdlMethodQuery, self).__init__(key, extend_option_kwargs)


class AbsDdlRsvTaskQuery(AbsDdlQuery):
    @classmethod
    def _get_rsv_task_version_(cls, rsv_task_properties):
        if rsv_task_properties.get('shot'):
            return '{project}.{shot}.{step}.{task}.{version}'.format(**rsv_task_properties.value)
        elif rsv_task_properties.get('asset'):
            return '{project}.{asset}.{step}.{task}.{version}'.format(**rsv_task_properties.value)
        else:
            raise TypeError()

    def __init__(self, key, rsv_task_properties):
        super(AbsDdlRsvTaskQuery, self).__init__(
            key,
            extend_option_kwargs=dict(
                configure=rsv_task_properties.get('project'),
                name=self._get_rsv_task_version_(rsv_task_properties)
            )
        )
