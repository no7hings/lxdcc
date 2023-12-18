# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.extra.abstracts as bsc_etr_abstracts


class EtrBase(bsc_etr_abstracts.AbsEtrBase):
    @classmethod
    def get_base_packages_extend(cls):
        return ['lxdcc']

    @classmethod
    def get_builtin_packages_extend(cls):
        return ['lxdcc', 'lxdcc_gui', 'lxdcc_lib', 'lxdcc_rsc']

    @classmethod
    def get_base_command(cls, args_execute=None, packages_extend=None):
        args_execute = bsc_core.PkgContextNew.convert_args_execute(
            args_execute
        )

        args = [
            bsc_core.PkgContextNew.get_bin_source(),
            ' '.join(packages_extend or []),
            ' '.join(args_execute or [])
        ]
        return ' '.join(args)

    @classmethod
    def packages_completed_to(cls, packages):
        return bsc_core.PkgContextNew()._completed_packages_to(packages)

    @classmethod
    def get_project_environs_extend(cls, project):
        return dict(
            PAPER_SHOW_NAME=project.upper(),
            PAPER_DB_NAME='production'
        )

    @classmethod
    def get_task_environs_extend(cls, project, resource, task):
        import lxwrap.shotgun.core as wrp_stg_core

        c = wrp_stg_core.StgConnector()
        task_id = c.find_task_id(
            project=project,
            resource=resource,
            task=task
        )
        if task_id is not None:
            return dict(
                PAPER_SHOW_NAME=project.upper(),
                PAPER_DB_NAME='production',
                PAPER_TASK_ID=str(task_id)
            )
        return dict(
            PAPER_SHOW_NAME=project.upper(),
            PAPER_DB_NAME='production'
        )

    @classmethod
    def get_task_environs_extend_(cls, **kwargs):
        if 'project' in kwargs:
            import lxwrap.shotgun.core as wrp_stg_core
            c = wrp_stg_core.StgConnector()
            stg_task = c.find_stg_task(**kwargs)
            if stg_task:
                task_id = stg_task['id']
                return dict(
                    PAPER_SHOW_NAME=kwargs['project'].upper(),
                    PAPER_DB_NAME='production',
                    PAPER_TASK_ID=str(task_id)
                )
            return dict(
                PAPER_SHOW_NAME=kwargs['project'].upper(),
                PAPER_DB_NAME='production'
            )
        return dict(
            PAPER_DB_NAME='production'
        )

    @classmethod
    def get_shotgun_step_name(cls, task):
        return str(task).upper()

    @classmethod
    def set_project(cls, project):
        bsc_core.EnvExtraMtd.set(
            'PAPER_SHOW_NAME', project.upper()
        )
        bsc_core.EnvExtraMtd.set(
            'PAPER_DB_NAME', 'production'
        )

    @classmethod
    def get_project(cls):
        return (bsc_core.EnvExtraMtd.get(
            'PAPER_SHOW_NAME'
        ) or '').lower()

    @classmethod
    def open_ide(cls, file_path):
        cmd = 'rez-env sublime_text -- sublime_text "{}"'.format(
            file_path
        )
        bsc_core.PrcBaseMtd.set_run(cmd)

    @classmethod
    def get_app_execute_mapper(cls, rsv_project):
        dict_ = {}
        platform = bsc_core.SysBaseMtd.get_platform()
        package_data = rsv_project.get_package_data()
        cfg_file_path = package_data['application-configure-file'][platform]
        cfg_file_path = bsc_core.PtnParseMtd.update_variants(cfg_file_path, project=rsv_project.get_name())
        data = bsc_core.StgFileOpt(cfg_file_path).set_read()
        if data:
            for i_app, i_data in data.items():
                i_e_main = i_data.get('cmd')
                if i_e_main is not None:
                    dict_[i_app] = dict(
                        application=i_app,
                        args_execute=['-- {}'.format(i_e_main)]
                    )
                #
                i_executes_extend = i_data.get('executes')
                if i_executes_extend:
                    for j_e_k_extend, j_e_s_extend in i_executes_extend.items():
                        dict_[j_e_k_extend] = dict(
                            application=i_app,
                            args_execute=['-- {}'.format(j_e_s_extend)]
                        )
        return dict_

    @classmethod
    def get_application_configure_file(cls, rsv_project):
        platform = bsc_core.SysBaseMtd.get_platform()
        package_data = rsv_project.get_package_data()
        cfg_file_path = package_data['application-configure-file'][platform]
        return bsc_core.PtnParseMtd.update_variants(cfg_file_path, project=rsv_project.get_name())

    @classmethod
    def get_deadline_configure_file(cls, rsv_project):
        platform = bsc_core.SysBaseMtd.get_platform()
        package_data = rsv_project.get_package_data()
        cfg_file_path = package_data['deadline-configure-file'][platform]
        return bsc_core.PtnParseMtd.update_variants(cfg_file_path, project=rsv_project.get_name())

    @classmethod
    def send_mail(cls, *args, **kwargs):
        import pkgutil

        if pkgutil.find_loader('cosmos'):
            # noinspection PyUnresolvedReferences
            from cosmos.message import imsg

            return imsg.send_email(
                receivers=kwargs['receivers'],
                title=kwargs['subject'],
                message=kwargs.get('content') or '',
            )
        else:
            return bsc_core.MsgBaseMtd.send_mail_(
                addresses=kwargs['addresses'],
                subject=kwargs['subject'],
                content=kwargs.get('content') or '',
            )

    @classmethod
    def send_feishu(cls, *args, **kwargs):
        import pkgutil

        if pkgutil.find_loader('cosmos'):
            # noinspection PyUnresolvedReferences
            from cosmos.message import imsg

            return imsg.send_message(
                receivers=kwargs['receivers'],
                title=kwargs['subject'],
                style='normal',
                message=kwargs.get('content') or '',
            )
        else:
            return bsc_core.MsgBaseMtd.send_feishu_(
                receivers=kwargs['receivers'],
                subject=kwargs['subject'],
                content=kwargs.get('content') or '',
            )

    @classmethod
    def send_chat(cls, *args, **kwargs):
        import pkgutil

        if pkgutil.find_loader('cosmos'):
            # noinspection PyUnresolvedReferences
            from cosmos.message import ichat

            return ichat.send_message(
                sender_name='sg_new_version',
                receivers=kwargs['receivers'],
                title=kwargs['subject'],
                message=kwargs.get('content') or '',
            )
        bsc_log.Log.trace_method_warning(
            'send messages failed', 'module "cosmos" is not found'
        )
        return False

    @classmethod
    def register_version_file_dependency(cls, *args, **kwargs):
        import pkgutil

        if pkgutil.find_loader('cosmos'):
            # noinspection PyUnresolvedReferences
            from cosmos.pipeline import dependency

            return dependency.create_version_depends(
                version_id=kwargs['version_id'],
                file_type=kwargs['keyword'],
                depend_file_paths=[kwargs['result']],
            )
        bsc_log.Log.trace_method_warning(
            'register dependency failed', 'module "cosmos" is not found'
        )
        return False


if __name__ == '__main__':
    print EtrBase.packages_completed_to(
        ['lxdcc', 'arnold']
    )
    print EtrBase.get_base_command(
        ['-- lxhook-command']
    )
