# coding:utf-8
import six

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

import lxbasic.extra.abstracts as bsc_etr_abstracts


class EtrUtility(bsc_etr_abstracts.AbsEtrUtility):
    @classmethod
    def get_base_packages_extend(cls):
        return ['lxdcc', 'lxdcc_lib', 'lxdcc_gui', 'lxdcc_rsc']
    @classmethod
    def get_base_command(cls, args_execute=None, packages_extend=None):
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


class EtrIde(bsc_etr_abstracts.AbsEtrIde):
    @classmethod
    def open_file(cls, file_path):
        cmd = 'rez-env sublime_text -- sublime_text "{}"'.format(
            file_path
        )
        bsc_core.SubProcessMtd.set_run(cmd)


class EtrRv(bsc_etr_abstracts.AbsEtrRv):
    @classmethod
    def open_file(cls, file_path):
        bsc_core.SubProcessMtd.set_run_with_result_use_thread(
            'rez-env pgrv -- rv "{}"'.format(file_path)
        )
    @classmethod
    def convert_to_mov(cls, **kwargs):
        default_kwargs = dict(
            input='',
            output='',
            quality=1.0,
            width=2048,
            lut_directory='/l/packages/pg/third_party/ocio/aces/1.0.3/baked/maya/sRGB_for_ACEScg_Maya.csp',
            comment='test',
            start_frame=1001,
        )
        cmd_args = [
            'rez-env pgrv',
            '--',
            '/opt/rv/bin/rvio',
            '{input}',
            '-vv',
            # '-overlay frameburn .4 1.0 30.0',
            # '-dlut "{lut_directory}"',
            '-o "{output}"',
            '-outparams comment="{comment}"',
            '-quality {quality}',
            '-copyright "©2013-2022 Papergames. All rights reserved."'
        ]
        if 'input' in kwargs:
            input_ = kwargs['input']
            if input_:
                _ = []
                if isinstance(input_, (tuple, list)):
                    if input_[0].endswith('.exr'):
                        cmd_args.extend(
                            [
                                '-dlut "{lut_directory}"',
                            ]
                        )
                    #
                    if '####' in input_[0]:
                        cmd_args.extend(
                            [
                                '-overlay frameburn .4 1.0 30.0',
                            ]
                        )
                    #
                    default_kwargs['input'] = ' '.join(map(lambda x: '"{}"'.format(x), input_))
                elif isinstance(input_, six.string_types):
                    if input_.endswith('.exr'):
                        cmd_args.extend(
                            ['-dlut "{lut_directory}"']
                        )
                    #
                    default_kwargs['input'] = '"{}"'.format(input_)

        default_kwargs['output'] = kwargs['output']
        bsc_core.SubProcessMtd.set_run_with_result(
            ' '.join(cmd_args).format(**default_kwargs)
        )


class EtrUsd(bsc_etr_abstracts.AbsEtrUsd):
    @classmethod
    def registry_set(cls, file_path):
        pass
