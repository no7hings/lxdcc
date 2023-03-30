# coding:utf-8
import six

from lxbasic import bsc_core

import lxbasic.extra.abstracts as bsc_etr_abstracts


class EtrBase(bsc_etr_abstracts.AbsEtrBase):
    @classmethod
    def get_base_packages_extend(cls):
        return ['lxdcc']
    @classmethod
    def get_base_command(cls, args_execute=None, packages_extend=None):
        args = [
            'rez-env',
            ' '.join(packages_extend or []),
            ' '.join(args_execute or [])
        ]
        return ' '.join(args)
    @classmethod
    def get_project_environs_extend(cls, project):
        return dict(
            PG_SHOW=project.upper(),
        )
    @classmethod
    def get_task_environs_extend(cls, project, resource, task):
        return dict(
            PG_SHOW=project.upper(),
        )
    @classmethod
    def get_shotgun_step_name(cls, task):
        return task
    @classmethod
    def set_project(cls, project):
        bsc_core.EnvExtraMtd.set(
            'PG_SHOW', project.upper()
        )
    @classmethod
    def get_project(cls):
        return (bsc_core.EnvExtraMtd.get(
            'PG_SHOW'
        ) or '').lower()
    @classmethod
    def open_ide(cls, file_path):
        cmd = 'rez-env sublime_text -- sublime_text "{}"'.format(
            file_path
        )
        bsc_core.SubProcessMtd.set_run(cmd)

