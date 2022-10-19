# coding:utf-8
import locale
import os

from lxbasic import bsc_core

from lxutil import utl_core

import lxresolver.commands as rsv_commands


class AbsHookExecutor(object):
    SHELL_CMD_PATTERN = 'rez-env lxdcc -c \"lxhook-engine -o \\\"{option}\\\"\"'
    DEADLINE_RUN_PATTERN = 'rez-env lxdcc -- lxhook-engine -o "{option}&start_index=<STARTFRAME>&end_index=<ENDFRAME>"'
    SUBMITTER_CLASS = None
    def __init__(self, session):
        self._session = session

    def get_session(self):
        return self._session
    session = property(get_session)

    def set_run_with_deadline(self):
        session = self.get_session()

        name = session.get_type()
        return self._set_deadline_submit_(
            session, name, dict(platform=bsc_core.SystemMtd.get_platform())
        )

    def _set_deadline_submit_(self, session, name, option_extra_dict):
        hook_option_opt = session.get_option_opt()
        hook_option = session.get_option()
        option_hook_key = hook_option_opt.get('option_hook_key')
        #
        ddl_configure = session.get_ddl_configure()
        #
        self._ddl_submiter = self.SUBMITTER_CLASS()
        self._ddl_submiter.set_option(
            type=session.get_type(),
            name=name,
            group=session.get_group(),
            engine=session.get_engine(),
            hook=session.get_hook(),
            #
            user=hook_option_opt.get('user'),
            time_tag=hook_option_opt.get('time_tag'),
        )
        # update task properties
        self._ddl_submiter.set_option_extra(
            **option_extra_dict
        )
        #
        self._ddl_submiter.option.set('deadline.group', ddl_configure.get('group'))
        self._ddl_submiter.option.set('deadline.pool', ddl_configure.get('pool'))
        #
        error_limit = ddl_configure.get('error_limit')
        if error_limit is not None:
            self._ddl_submiter.job_info.set(
                'FailureDetectionTaskErrors', error_limit
            )
        #
        batch_key = hook_option_opt.get('batch_key')
        if batch_key:
            batch_list = hook_option_opt.get(batch_key, as_array=True) or []
            self._ddl_submiter.job_info.set(
                'Frames', ','.join(map(str, range(len(batch_list))))
            )
        #
        renderer = hook_option_opt.get('renderer')
        if renderer:
            render_output_directory_path = hook_option_opt.get('render_output_directory')
            if render_output_directory_path:
                self._ddl_submiter.option.set('deadline.output_file', render_output_directory_path)
            #
            render_frames = hook_option_opt.get('render_frames', as_array=True)
            if render_frames:
                self._ddl_submiter.job_info.set(
                    'Frames', ','.join(render_frames)
                )
        else:
            file_path = hook_option_opt.get('file')
            if file_path:
                self._ddl_submiter.option.set('deadline.output_file', file_path)
        # Priority
        deadline_priority = hook_option_opt.get('deadline_priority')
        if deadline_priority is not None:
            self._ddl_submiter.job_info.set('Priority', int(deadline_priority))
        #
        option_hook_key_extend = hook_option_opt.get('option_hook_key_extend', as_array=True)
        if option_hook_key_extend:
            keys = [option_hook_key]
            keys.extend(option_hook_key_extend)
            option_hook_key = '/'.join(keys)
            self._ddl_submiter.option.set('hook', option_hook_key)
        #
        self._ddl_submiter.job_info.set(
            'Comment', hook_option
        )
        ddl_command = self.get_deadline_command()
        if bsc_core.TextOpt(ddl_command).get_is_contain_chinese():
            ddl_command = ddl_command.encode(locale.getdefaultlocale()[1])
        #
        self._ddl_submiter.option.set(
            'deadline.command',
            ddl_command
        )
        #
        hook_dependent_ddl_job_ids = session.set_ddl_dependent_job_ids_find(hook_option)
        if isinstance(hook_dependent_ddl_job_ids, (tuple, list)):
            self._ddl_submiter.job_info.set('JobDependencies', ','.join(hook_dependent_ddl_job_ids))
            self._ddl_submiter.job_info.set('ResumeOnCompleteDependencies', True)
        #
        dependent_ddl_job_id_extend = hook_option_opt.get('dependent_ddl_job_id_extend', as_array=True)
        if dependent_ddl_job_id_extend:
            dependent_ddl_job_ids_string_old = self._ddl_submiter.job_info.get('JobDependencies')
            dependent_ddl_job_id_extend_string = ','.join(dependent_ddl_job_id_extend)
            if dependent_ddl_job_ids_string_old:
                self._ddl_submiter.job_info.set('JobDependencies', ','.join(
                    [dependent_ddl_job_ids_string_old, dependent_ddl_job_id_extend_string]))
                self._ddl_submiter.job_info.set('ResumeOnCompleteDependencies', True)
            else:
                dependent_ddl_job_ids_string_new = '{},{}'.format(dependent_ddl_job_ids_string_old,
                                                                  dependent_ddl_job_id_extend_string)
                self._ddl_submiter.job_info.set('JobDependencies', dependent_ddl_job_ids_string_new)
                self._ddl_submiter.job_info.set('ResumeOnCompleteDependencies', True)
        #
        td_enable = hook_option_opt.get('td_enable') or False
        if td_enable is True:
            self._ddl_submiter.job_info.set(
                'Pool', 'td'
            )
            self._ddl_submiter.job_info.set(
                'Group', 'td'
            )
            self._ddl_submiter.job_info.set(
                'Whitelist', bsc_core.SystemMtd.get_host()
            )
        #
        localhost_enable = hook_option_opt.get('localhost_enable') or False
        if localhost_enable is True:
            self._ddl_submiter.job_info.set(
                'Pool', 'artist'
            )
            self._ddl_submiter.job_info.set(
                'Group', 'artist'
            )
            self._ddl_submiter.job_info.set(
                'Whitelist', bsc_core.SystemMtd.get_host()
            )
        #
        exists_ddl_job_id = session.set_ddl_job_id_find(hook_option)
        if exists_ddl_job_id:
            session._ddl_job_id = exists_ddl_job_id
            utl_core.Log.set_module_warning_trace(
                'option-hook execute by deadline', 'option-hook="{}", job-id="{}" is exists'.format(
                    option_hook_key, exists_ddl_job_id
                )
            )
        else:
            ddl_job_id = self._ddl_submiter.set_job_submit()
            if ddl_job_id is not None:
                session._ddl_job_id = ddl_job_id
                #
                session.set_ddl_result_update(
                    hook_option, ddl_job_id
                )
                utl_core.Log.set_module_result_trace(
                    'option-hook execute by deadline', 'option-hook="{}", job-id="{}"'.format(
                        option_hook_key, ddl_job_id
                    )
                )
        return self._ddl_submiter.get_job_result()

    def set_run_with_shell(self, block=False):
        #
        extend_environs = {}
        #
        _ = bsc_core.EnvironMtd.get('LYNXI_RESOURCES')
        if _:
            extend_environs['LYNXI_RESOURCES'] = _
        #
        cmd = self.get_shell_command()
        #
        if block is True:
            utl_core.SubProcessRunner.set_run_with_result(
                cmd, extend_environs=extend_environs
            )
        else:
            utl_core.SubProcessRunner.set_run_with_result_use_thread(
                cmd, extend_environs=extend_environs
            )

    def set_run(self):
        return self.set_run_with_deadline()

    def get_shell_command(self):
        return self.SHELL_CMD_PATTERN.format(
            **dict(option=self.get_session().get_option())
        )

    def get_deadline_command(self):
        return self.DEADLINE_RUN_PATTERN.format(
            **dict(option=self.get_session().get_option())
        ).replace(
            '<', '\\<'
        ).replace(
            '>', '\\>'
        )


class AbsRsvTaskMethodHookExecutor(AbsHookExecutor):
    def __init__(self, *args, **kwargs):
        super(AbsRsvTaskMethodHookExecutor, self).__init__(*args, **kwargs)

    def set_run_with_deadline(self):
        session = self.get_session()
        #
        hook_option_opt = session.get_option_opt()
        #
        scene_file_path = hook_option_opt.get('file')
        resolver = rsv_commands.get_resolver()
        #
        rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(
            file_path=scene_file_path
        )
        if rsv_task_properties:
            name = session._get_rsv_task_version_(rsv_task_properties)
            return self._set_deadline_submit_(
                session, name, rsv_task_properties.value
            )

    def set_run(self):
        return self.set_run_with_deadline()
