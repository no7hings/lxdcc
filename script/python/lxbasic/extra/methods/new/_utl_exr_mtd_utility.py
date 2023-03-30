# coding:utf-8
from lxbasic import bsc_core

import lxbasic.extra.abstracts as bsc_etr_abstracts


class EtrBase(bsc_etr_abstracts.AbsEtrBase):
    @classmethod
    def get_base_packages_extend(cls):
        return ['lxdcc', 'lxdcc_lib', 'lxdcc_gui', 'lxdcc_rsc']
    @classmethod
    def get_base_command(cls, args_execute=None, packages_extend=None):
        import lxbasic.objects as bsc_objects
        #
        return bsc_objects.PackageContextNew(
            None
        ).get_command(
            args_execute=args_execute, packages_extend=packages_extend
        )
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
            project='nsa_dev',
            resource='td_test',
            task='surface'
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
