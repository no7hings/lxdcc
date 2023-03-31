# coding:utf-8


class AbsEtrBase(object):
    @classmethod
    def get_base_packages_extend(cls):
        raise NotImplementedError()
    @classmethod
    def get_base_command(cls, args_execute=None, packages_extend=None):
        raise NotImplementedError()
    @classmethod
    def get_project_environs_extend(cls, project):
        raise NotImplementedError()
    @classmethod
    def get_task_environs_extend(cls, project, resource, task):
        raise NotImplementedError()
    @classmethod
    def get_shotgun_step_name(cls, task):
        raise NotImplementedError()
    @classmethod
    def set_project(cls, project):
        raise NotImplementedError()
    @classmethod
    def get_project(cls):
        raise NotImplementedError()
    @classmethod
    def open_ide(cls, file_path):
        raise NotImplementedError()
    @classmethod
    def get_app_execute_mapper(cls, *args, **kwargs):
        raise NotImplementedError()


class AbsEtrIde(object):
    @classmethod
    def open_file(cls, file_path):
        raise NotImplementedError()


class AbsEtrRv(object):
    @classmethod
    def open_file(cls, file_path):
        raise NotImplementedError()
    @classmethod
    def convert_to_mov(cls, **kwargs):
        raise NotImplementedError()


class AbsEtrUsd(object):
    @classmethod
    def registry_set(cls, file_path):
        raise NotImplementedError()
