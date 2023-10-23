# coding:utf-8
from lxbasic import bsc_core

import lxcontent.objects as ctt_objects

from lxutil import utl_core


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
        return bsc_core.ArgDictStringMtd.to_string(
            **kwargs
        )

    #
    def __init__(self, key, extend_option_kwargs=None):
        self._configure = ctt_objects.Configure(
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


class AbsDdlSubmiter(object):
    CON = None
    CONFIGURE_FILE_PATH = None

    def __init__(self):
        self._configure = ctt_objects.Configure(value=self.CONFIGURE_FILE_PATH)
        #
        self._option = self._configure.get_content('option')
        #
        self._job_info = self._configure.get_content('output.info')
        self._job_plug = self._configure.get_content('output.plug')
        #
        self._result = None
        self._job_id = None

    def get_option(self):
        return self._option

    option = property(get_option)

    def set_option(self, **kwargs):
        for k in self._configure.get('option'):
            if k in kwargs:
                self._configure.set(
                    'option.{}'.format(k),
                    kwargs[k]
                )

    def set_option_extra(self, **kwargs):
        for k in self._configure.get('option.extra'):
            if k in kwargs:
                self._configure.set(
                    'option.extra.{}'.format(k),
                    kwargs[k]
                )

    #
    def get_job_info(self):
        return self._job_info

    job_info = property(get_job_info)

    def get_job_plug(self):
        return self._job_plug

    job_plug = property(get_job_plug)

    def set_job_info_extra(self, raw):
        if isinstance(raw, dict):
            content = ctt_objects.Content(value=raw)
            for seq, k in enumerate(content._get_leaf_keys_()):
                self.job_info.set(
                    'ExtraInfoKeyValue{}'.format(seq),
                    '{}={}'.format(k, content.get(k))
                )

    def set_job_submit(self):
        self._configure.set_flatten()
        info = self.job_info.value
        plug = self.job_plug.value
        return self.__set_job_submit_(info, plug)

    def __set_job_submit_(self, info, plug):
        bsc_core.Log.trace_method_result(
            'deadline-job submit', 'is started'
        )
        self._result = self.CON.Jobs.SubmitJob(info, plug)
        if isinstance(self._result, dict):
            if '_id' in self._result:
                self._job_id = self._result['_id']
                bsc_core.Log.trace_method_result(
                    'deadline-job submit', 'is completed, jon-id="{}"'.format(self._job_id)
                )
                return self._job_id
        #
        bsc_core.Log.trace_method_error(
            'deadline-job submit', 'is failed, {}'.format(self._result)
        )
        return None

    def get_job_is_submit(self):
        return self.get_job_id() is not None

    def get_job_group_name(self):
        return self.job_info.get('BatchName')

    def get_job_name(self):
        return self.job_info.get('Name')

    def get_job_result(self):
        return self._result

    def get_job_id(self):
        _ = self.get_job_result()
        if isinstance(_, dict):
            if '_id' in _:
                return _['_id']

    def __str__(self):
        return self._configure.get_str_as_yaml_style()
