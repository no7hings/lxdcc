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
    @classmethod
    def get_app_execute_mapper(cls, *args, **kwargs):
        return {}


class EtrStorage(bsc_etr_abstracts.AbsEtrStorage):
    @classmethod
    def create_directory(cls, directory_path):
        bsc_core.StgExtraMtd.create_directory(directory_path)
    @classmethod
    def copy_to_file(cls, file_path_src, file_path_tgt, replace=False):
        bsc_core.StgFileOpt(file_path_src).set_copy_to_file(
            file_path_tgt, replace=replace
        )
    @classmethod
    def change_owner(cls, path, user='artist', group='artists'):
        pass
