# coding:utf-8
import platform

import lxlog.core as log_core

from lxresource.core import _rsc_cor_base

import lxcontent.objects as ctt_objects


class RscTool(_rsc_cor_base.Resource):
    CACHE = {}
    ENVIRON_KEY = 'PAPER_EXTEND_TOOLS'

    @classmethod
    def get_yaml(cls, key):
        return cls.get('{}.yml'.format(key))

    @classmethod
    def get_python(cls, key):
        return cls.get(
            '{}.py'.format(key)
        )

    @classmethod
    def get_shell(cls, key):
        if platform.system() == 'Linux':
            return cls.get(
                '{}.sh'.format(key)
            )
        elif platform.system() == 'Windows':
            return cls.get(
                '{}.bat'.format(key)
            )


class RscDesktopTool(object):
    BRANCH = 'desktop'

    @classmethod
    def get_yaml(cls, key):
        return RscTool.get_yaml('{}/{}'.format(cls.BRANCH, key))

    @classmethod
    def get_python(cls, key):
        return RscTool.get_python('{}/{}'.format(cls.BRANCH, key))

    @classmethod
    def get_shell(cls, key):
        return RscTool.get_shell('{}/{}'.format(cls.BRANCH, key))

    @classmethod
    def find_all_keys_at(cls, group_name):
        return RscTool.find_all_file_keys_at(
            cls.BRANCH, group_name, ext_includes={'.yml'}
        )

    @classmethod
    def find_all_group_keys_at(cls, group_name):
        return RscTool.find_all_directory_keys_at(
            cls.BRANCH, group_name
        )

    @classmethod
    def get_args(cls, key):
        yaml_file_path = cls.get_yaml(key)
        if yaml_file_path:
            configure = ctt_objects.Configure(value=yaml_file_path)
            type_ = configure.get('option.type')
            if type_:
                python_file_path = cls.get_python(key)
                shell_file_path = cls.get_shell(key)
                return type_, key, configure, yaml_file_path, python_file_path, shell_file_path

            log_core.Log.trace_warning(
                'hook file is not valid: "{}"'.format(yaml_file_path)
            )
            return None
        log_core.Log.trace_error(
            'hook file is found: "{}"'.format(key)
        )
        return None


class RscDccTool(RscDesktopTool):
    BRANCH = 'dcc'


if __name__ == '__main__':
    pass
    # print RscTool.get_yaml('desktop/Share/quixel_python')
    # print RscDesktopTool.get_yaml('Share/quixel_python')
    print RscDesktopTool.find_all_keys_at('Studio')
    print RscDesktopTool.find_all_group_keys_at('User')
    # print RscDesktopTool.get_args('Share/quixel_python')
