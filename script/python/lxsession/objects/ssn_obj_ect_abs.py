# coding:utf-8
from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxutil import utl_core

import lxresolver.commands as rsv_commands

import lxdeadline.objects as ddl_objects


class AbsHookExecutor(object):
    SHELL_CMD_PATTERN = 'rez-env lxdcc -c \"lxhook-engine -o \\\"{option}\\\"\"'
    DEADLINE_RUN_PATTERN = 'rez-env lxdcc -- lxhook-engine -o "{option}&start_index=<STARTFRAME>&end_index=<ENDFRAME>"'
    def __init__(self, session):
        self._session = session

    def get_session(self):
        return self._session
    session = property(get_session)

    def set_run_with_deadline(self):
        pass

    def set_run_with_shell(self):
        cmd = self.get_shell_command()
        #
        utl_core.SubProcessRunner.set_run_with_result_use_thread(
            cmd
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


class AbsRsvTaskHookExecutor(AbsHookExecutor):
    def __init__(self, *args, **kwargs):
        super(AbsRsvTaskHookExecutor, self).__init__(*args, **kwargs)

    def set_run_with_deadline(self):
        session = self.get_session()
        #
        hook_option_opt = session.get_option_opt()
        hook_option = session.get_option()
        #
        scene_file_path = hook_option_opt.get('file')
        engine = hook_option_opt.get('engine')
        resolver = rsv_commands.get_resolver()
        #
        ddl_configure = session.get_ddl_configure()
        #
        rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(
            file_path=scene_file_path
        )
        if rsv_task_properties:
            name = session._get_rsv_task_version_(rsv_task_properties)
            self._ddl_submiter = ddl_objects.DdlSubmiter()
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
                **rsv_task_properties.value
            )
            #
            render_file_path = hook_option_opt.get('render_file')
            if render_file_path:
                self._ddl_submiter.option.set('deadline.output_file', render_file_path)
            else:
                self._ddl_submiter.option.set('deadline.output_file', scene_file_path)
            #
            self._ddl_submiter.option.set('deadline.group', ddl_configure.get('group'))
            self._ddl_submiter.option.set('deadline.pool', ddl_configure.get('pool'))
            #
            batch_key = hook_option_opt.get('batch_key')
            if batch_key:
                batch_list = hook_option_opt.get(batch_key, as_array=True) or []
                self._ddl_submiter.job_info.set(
                    'Frames', ','.join(map(str, range(len(batch_list))))
                )
            else:
                render_frames = hook_option_opt.get('render_frames', as_array=True)
                if render_frames:
                    self._ddl_submiter.job_info.set(
                        'Frames', ','.join(render_frames)
                    )
            #
            renderer = hook_option_opt.get('renderer')
            if renderer:
                job_name = self._ddl_submiter.option.get('deadline.job_name')
                job_name_ = '{}[{}]'.format(job_name, renderer)
                self._ddl_submiter.option.set('deadline.job_name', job_name_)
            #
            self._ddl_submiter.job_info.set(
                'Comment', hook_option
            )
            ddl_command = self.get_deadline_command()
            #
            self._ddl_submiter.option.set(
                'deadline.command',
                ddl_command
            )
            dependent_ddl_job_ids = session.get_ddl_dependencies(hook_option)
            if isinstance(dependent_ddl_job_ids, (tuple, list)):
                self._ddl_submiter.job_info.set('JobDependencies', ','.join(dependent_ddl_job_ids))
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
            self._js_result = self._ddl_submiter.set_job_submit()
            #
            ddl_job_id = self._ddl_submiter.get_job_id()
            if ddl_job_id is not None:
                #
                session.set_ddl_result_update(
                    hook_option, ddl_job_id
                )
                #
                utl_core.Log.set_module_result_trace(
                    'deadline-job submit',
                    u'batch-name="{}";job-name="{}";job-id="{}"option="{}"'.format(
                        self._ddl_submiter.option.get('deadline.batch_name'),
                        self._ddl_submiter.option.get('deadline.job_name'),
                        ddl_job_id,
                        hook_option
                    )
                )
                utl_core.Log.set_module_result_trace(
                    'deadline-job submit',
                    u'command=`{}`'.format(ddl_command)
                )
            return self._ddl_submiter.get_job_result()

    def set_run(self):
        return self.set_run_with_deadline()

