# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

from lxdeadline import ddl_core

import lxdeadline.objects as ddl_objects

import lxresolver.commands as rsv_commands


class AbsJobSender(object):
    DEADLINE_COMMAND_PATTERN = None
    SHELL_COMMAND_PATTERN = None
    def __init__(self, option, job_dependencies):
        self._option = option
        self._option += '&user={}&time={}'.format(
            utl_core.System.get_user_name(),
            utl_core.System.get_time_tag(),
        )
        #
        self._job_key = self.__class__.__name__
        #
        self._deadline_command_pattern = None
        self._shell_command_pattern = None
        #
        self._deadline_command = None
        self._shell_command = None
        #
        self._job_dependencies = job_dependencies
        #
        self._ddl_job_sender = None
        #
        self._js_result = {}

    def get_job_key(self):
        return self._job_key
    job_key = property(get_job_key)

    def get_option(self):
        return self._option
    option = property(get_option)

    def get_option_opt(self):
        return bsc_core.KeywordArgumentsOpt(self.get_option())
    option_opt = property(get_option_opt)

    def get_ddl_job_sender(self):
        return self._ddl_job_sender

    def get_ddl_job_is_submit(self):
        _ = self.get_ddl_job_sender()
        if _:
            return _.get_is_submit()

    def get_ddl_job_group_name(self):
        _ = self.get_ddl_job_sender()
        if _:
            return _.get_group_name()

    def get_ddl_job_name(self):
        _ = self.get_ddl_job_sender()
        if _:
            return _.get_name()

    def get_ddl_job_id(self):
        _ = self.get_ddl_job_sender()
        if _:
            result = _.get_result()
            if isinstance(result, dict):
                if '_id' in result:
                    return result['_id']
                else:
                    utl_core.Log.set_module_warning_trace(
                        'deadline-job-method',
                        'deadline-job="{}" is false or not start'.format(self._job_key)
                    )
            else:
                raise RuntimeError(
                    result
                )
    ddl_job_id = property(get_ddl_job_id)

    def set_run(self, *args, **kwargs):
        self.set_run_with_deadline(*args, **kwargs)

    def set_run_with_deadline(self, *args, **kwargs):
        raise NotImplementedError()

    def set_run_with_shell(self, with_result=False):
        if self._shell_command is not None:
            from lxutil import utl_core
            if with_result is True:
                utl_core.SubProcessRunner.set_run_with_result(self._shell_command)
            else:
                utl_core.SubProcessRunner.set_run(self._shell_command)


class AbsJobSender2(object):
    DEADLINE_COMMAND_PATTERN = None
    SHELL_COMMAND_PATTERN = None
    def __init__(self, method_option, script_option, job_dependencies):
        self._method_option = method_option
        self._script_option = script_option
        #
        self._method_option_opt = bsc_core.KeywordArgumentsOpt(self._method_option)
        self._script_option_opt = bsc_core.KeywordArgumentsOpt(self._script_option)
        # update user + time_tag
        user, time_tag = self._script_option_opt.get('user') or utl_core.System.get_user_name(), self._script_option_opt.get('time_tag') or utl_core.System.get_time_tag()
        #
        self._method_option_opt.set('user', user), self._method_option_opt.set('time_tag', time_tag)
        self._method_option = self._method_option_opt.to_option()
        #
        self._script_option_opt.set('user', user), self._script_option_opt.set('time_tag', time_tag)
        self._script_option = self._script_option_opt.to_option()
        #
        self._mtd_kwargs = self._method_option_opt.value
        self._mtd_kwargs['script_option'] = self._script_option
        #
        self._deadline_command = self.DEADLINE_COMMAND_PATTERN.format(**self._mtd_kwargs)
        self._shell_command = self.SHELL_COMMAND_PATTERN.format(**self._mtd_kwargs)
        #
        self._job_dependencies = job_dependencies
        #
        self._ddl_job_sender = None
        #
        self._js_result = {}

    def get_method_option(self):
        return self._method_option
    method_option = property(get_method_option)

    def get_method_option_opt(self):
        return bsc_core.KeywordArgumentsOpt(self.get_method_option())
    method_option_opt = property(get_method_option_opt)

    def get_script_option(self):
        return self._script_option
    script_option = property(get_script_option)

    def get_script_option_opt(self):
        return bsc_core.KeywordArgumentsOpt(self.get_script_option())
    script_option_opt = property(get_script_option_opt)

    def get_ddl_job_sender(self):
        return self._ddl_job_sender

    def get_ddl_job_is_submit(self):
        _ = self.get_ddl_job_sender()
        if _:
            return _.get_job_is_submit()

    def get_ddl_job_group_name(self):
        _ = self.get_ddl_job_sender()
        if _:
            return _.get_job_group_name()

    def get_ddl_job_name(self):
        _ = self.get_ddl_job_sender()
        if _:
            return _.get_job_name()

    def get_ddl_job_id(self):
        _ = self.get_ddl_job_sender()
        if _:
            result = _.get_job_result()
            if isinstance(result, dict):
                if '_id' in result:
                    return result['_id']
                else:
                    utl_core.Log.set_module_warning_trace(
                        'deadline-job-method',
                        'deadline-job is false or not start'
                    )
            else:
                raise RuntimeError(
                    result
                )
    ddl_job_id = property(get_ddl_job_id)

    def set_run(self, *args, **kwargs):
        self.set_run_with_deadline(*args, **kwargs)

    def set_run_with_deadline(self, *args, **kwargs):
        raise NotImplementedError()

    def set_run_with_shell(self, with_result=False):
        if self._shell_command is not None:
            from lxutil import utl_core
            if with_result is True:
                utl_core.SubProcessRunner.set_run_with_result(self._shell_command)
            else:
                utl_core.SubProcessRunner.set_run(self._shell_command)


class AbsDdlMethodRunner(AbsJobSender2):
    DEADLINE_COMMAND_PATTERN = r'rez-env lxdcc -c \"lxscript -p {configure} -a {engine} -s {script} -o \\\"{script_option}&start_index=\<STARTFRAME\>&end_index=\<ENDFRAME\>\\\"\"'
    SHELL_COMMAND_PATTERN = r'rez-env lxdcc -c "lxscript -p {configure} -a {engine} -s {script} -o \"{script_option}&start_index=\<STARTFRAME\>&end_index=\<ENDFRAME\>\\\"\"'
    def __init__(self, method_option, script_option, job_dependencies):
        super(AbsDdlMethodRunner, self).__init__(method_option, script_option, job_dependencies)

    def set_run_with_deadline(self):
        script_option_opt = self.get_script_option_opt()
        file_path = script_option_opt.get('file')
        #
        self._ddl_job_sender = ddl_objects.DdlMethodJobSender(option=self._method_option)
        self._ddl_job_sender.set_method(**self._mtd_kwargs)
        self._ddl_job_sender.method.set('job.output_file', file_path)
        #
        self._ddl_job_sender.job_info.set(
            'Comment', self._script_option
        )
        self._ddl_job_sender.method.set(
            'job.command',
            self._deadline_command
        )
        #
        self._ddl_job_sender.method.set('job.group', self.get_method_option_opt().get('group'))
        self._ddl_job_sender.method.set('job.pool', self.get_method_option_opt().get('pool'))
        #
        if isinstance(self._job_dependencies, (tuple, list)):
            self._ddl_job_sender.job_info.set('JobDependencies', ','.join(self._job_dependencies))
            self._ddl_job_sender.job_info.set('ResumeOnCompleteDependencies', True)
        #
        td_enable = utl_core.Environ.get_td_enable()
        if td_enable is True:
            self._ddl_job_sender.job_info.set(
                'Pool', 'td'
            )
            self._ddl_job_sender.job_info.set(
                'Group', 'td'
            )
            self._ddl_job_sender.job_info.set(
                'Whitelist', 'centos-d-009'
            )
        #
        self._js_result = self._ddl_job_sender.set_job_submit()
        ddl_job_id = self.get_ddl_job_id()
        if ddl_job_id is not None:
            utl_core.Log.set_module_result_trace(
                'deadline-job-sender-result',
                u'group-name="{}";name="{}";id="{}"option="{}"'.format(
                    self._ddl_job_sender.method.get('job.group_name'),
                    self._ddl_job_sender.method.get('job.name'),
                    ddl_job_id,
                    self._script_option
                )
            )
            utl_core.Log.set_module_result_trace(
                'deadline-job-sender-result',
                u'command=`{}`'.format(self._deadline_command)
            )
            self._ddl_job_sender.get_cache_opt().set_update(self)
        return self._js_result


class AbsDdlRsvTaskMethodRunner(AbsDdlMethodRunner):
    def __init__(self, method_option, script_option, job_dependencies):
        super(AbsDdlRsvTaskMethodRunner, self).__init__(method_option, script_option, job_dependencies)

    def set_run_with_deadline(self):
        script_option_opt = self.get_script_option_opt()
        scene_file_path = script_option_opt.get('file')
        resolver = rsv_commands.get_resolver()
        #
        rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_file_path)
        if rsv_task_properties:
            self._ddl_job_sender = ddl_objects.DdlRsvTaskMethodJobSender(option=self._method_option)
            self._ddl_job_sender.set_method(**self._mtd_kwargs)
            self._ddl_job_sender.set_method_extra(**rsv_task_properties.value)
            #
            if self._ddl_job_sender.method.get('extra.shot'):
                entity = self._ddl_job_sender.method.get('extra.shot')
            elif self._ddl_job_sender.method.get('extra.asset'):
                entity = self._ddl_job_sender.method.get('extra.asset')
            else:
                raise TypeError()
            #
            self._ddl_job_sender.method.set('extra.entity', entity)
            #
            self._ddl_job_sender.method.set('job.output_file', scene_file_path)
            #
            self._ddl_job_sender.method.set('job.group', self.get_method_option_opt().get('group'))
            self._ddl_job_sender.method.set('job.pool', self.get_method_option_opt().get('pool'))
            #
            self._ddl_job_sender.job_info.set(
                'Comment', self._script_option
            )
            self._ddl_job_sender.method.set(
                'job.command',
                self._deadline_command
            )
            if isinstance(self._job_dependencies, (tuple, list)):
                self._ddl_job_sender.job_info.set('JobDependencies', ','.join(self._job_dependencies))
                self._ddl_job_sender.job_info.set('ResumeOnCompleteDependencies', True)
            #
            o_td_enable = script_option_opt.get('td_enable') or False
            td_enable = utl_core.Environ.get_td_enable()
            if td_enable is True or o_td_enable is True:
                self._ddl_job_sender.job_info.set(
                    'Pool', 'td'
                )
                self._ddl_job_sender.job_info.set(
                    'Group', 'td'
                )
                self._ddl_job_sender.job_info.set(
                    'Whitelist', 'centos-d-009'
                )
            #
            self._js_result = self._ddl_job_sender.set_job_submit()
            ddl_job_id = self.get_ddl_job_id()
            if ddl_job_id is not None:
                utl_core.Log.set_module_result_trace(
                    'deadline-job-sender-result',
                    u'group-name="{}";name="{}";id="{}"option="{}"'.format(
                        self._ddl_job_sender.method.get('job.group_name'),
                        self._ddl_job_sender.method.get('job.name'),
                        ddl_job_id,
                        self._script_option
                    )
                )
                utl_core.Log.set_module_result_trace(
                    'deadline-job-sender-result',
                    u'command=`{}`'.format(self._deadline_command)
                )
                self._ddl_job_sender.get_cache_opt().set_update(self)
            return self._js_result


class AbsDdlRsvTaskRender(AbsDdlMethodRunner):
    def __init__(self, method_option, script_option, job_dependencies):
        super(AbsDdlRsvTaskRender, self).__init__(method_option, script_option, job_dependencies)

    def set_run_with_deadline(self):
        script_option_opt = self.get_script_option_opt()
        any_scene_file_path = script_option_opt.get('file')
        render_scene_file_path = script_option_opt.get('render_file')
        resolver = rsv_commands.get_resolver()
        #
        rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
        if rsv_task_properties:
            self._ddl_job_sender = ddl_objects.DdlRsvTaskRenderJobSender(option=self._method_option)
            self._ddl_job_sender.set_method(**self._mtd_kwargs)
            self._ddl_job_sender.set_method_extra(**rsv_task_properties.value)
            #
            if self._ddl_job_sender.method.get('extra.shot'):
                entity = self._ddl_job_sender.method.get('extra.shot')
            elif self._ddl_job_sender.method.get('extra.asset'):
                entity = self._ddl_job_sender.method.get('extra.asset')
            else:
                raise TypeError()
            #
            frame = script_option_opt.get('frame', as_array=True)
            #
            self._ddl_job_sender.method.set('extra.entity', entity)
            #
            start_frame, end_frame = frame[0], frame[-1]
            width, height = script_option_opt.get('width'), script_option_opt.get('height')
            renderer = script_option_opt.get('renderer')
            quality = script_option_opt.get('quality')
            if start_frame is not None:
                self._ddl_job_sender.method.set('render.start_frame', start_frame)
            if end_frame is not None:
                self._ddl_job_sender.method.set('render.end_frame', end_frame)
            if width is not None:
                self._ddl_job_sender.method.set('render.width', width)
            if height is not None:
                self._ddl_job_sender.method.set('render.height', height)
            if renderer is not None:
                self._ddl_job_sender.method.set('render.renderer', renderer)
            if quality is not None:
                self._ddl_job_sender.method.set('render.quality', quality)
            #
            self._ddl_job_sender.method.set('job.output_file', render_scene_file_path)
            #
            self._ddl_job_sender.method.set('job.group', self.get_method_option_opt().get('group'))
            self._ddl_job_sender.method.set('job.pool', self.get_method_option_opt().get('pool'))
            #
            self._ddl_job_sender.job_info.set(
                'Frames', ','.join(frame)
            )
            #
            self._ddl_job_sender.job_info.set(
                'Comment', self._script_option
            )
            self._ddl_job_sender.method.set(
                'job.command',
                self._deadline_command
            )
            if isinstance(self._job_dependencies, (tuple, list)):
                self._ddl_job_sender.job_info.set('JobDependencies', ','.join(self._job_dependencies))
                self._ddl_job_sender.job_info.set('ResumeOnCompleteDependencies', True)
            #
            o_td_enable = script_option_opt.get('td_enable') or False
            td_enable = utl_core.Environ.get_td_enable()
            if td_enable is True or o_td_enable is True:
                self._ddl_job_sender.job_info.set(
                    'Pool', 'td'
                )
                self._ddl_job_sender.job_info.set(
                    'Group', 'td'
                )
                self._ddl_job_sender.job_info.set(
                    'Whitelist', 'centos-d-009'
                )
            #
            self._js_result = self._ddl_job_sender.set_job_submit()
            ddl_job_id = self.get_ddl_job_id()
            if ddl_job_id is not None:
                utl_core.Log.set_module_result_trace(
                    'deadline-job-sender-result',
                    u'group-name="{}";name="{}";id="{}"option="{}"'.format(
                        self._ddl_job_sender.method.get('job.group_name'),
                        self._ddl_job_sender.method.get('job.name'),
                        ddl_job_id,
                        self._script_option
                    )
                )
                utl_core.Log.set_module_result_trace(
                    'deadline-job-sender-result',
                    u'command=`{}`'.format(self._deadline_command)
                )
                self._ddl_job_sender.get_cache_opt().set_update(self)
            return self._js_result
