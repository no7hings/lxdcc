# coding:utf-8
from lxbasic import bsc_core

import lxbasic.extra.abstracts as bsc_etr_abstracts


class EtrBase(bsc_etr_abstracts.AbsEtrBase):
    @classmethod
    def get_base_packages_extend(cls):
        return ['lxdcc']
    @classmethod
    def get_base_command(cls, args_execute=None, packages_extend=None):
        import lxbasic.objects as bsc_objects

        args_execute = bsc_objects.PackageContextNew.convert_args_execute(
            args_execute
        )

        args = [
            '/job/PLE/support/wrappers/paper-bin',
            ' '.join(packages_extend or []),
            ' '.join(args_execute or [])
        ]
        return ' '.join(args)
    @classmethod
    def get_project_environs_extend(cls, project):
        return dict(
            PAPER_SHOW_NAME=project.upper(),
            PAPER_DB_NAME='production'
        )
    @classmethod
    def get_task_environs_extend(cls, project, resource, task):
        import lxshotgun.objects as stg_objects
        #
        c = stg_objects.StgConnector()
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
        bsc_core.SubProcessMtd.set_run(cmd)
    @classmethod
    def get_app_execute_mapper(cls, rsv_project):
        dict_ = {}
        platform = bsc_core.SystemMtd.get_platform()
        package_data = rsv_project.get_package_data()
        cfg_file_path = package_data['configure-files'][platform]
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
