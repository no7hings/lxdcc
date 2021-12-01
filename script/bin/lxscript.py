# coding:utf-8
from __future__ import print_function

import sys

import getopt

import os

import collections

argv = sys.argv


def usage():
    print (
        '***** lxscript *****\n'
        '\n'
        #
        '-h or --help: show help\n'
        #
        '-p or --project: <project-name>\n'
        '-a or --application: <application-name>\n'
        '-s or --script: <script-name>\n'
        '-o or --option: <option>\n'
        'etc\n'
        'lxscript -p cjd -a maya -s set_scene_export_by_any_scene_file -o "file=/l/prod/cjd/publish/assets/chr/td_test/srf/surfacing/td_test.srf.surfacing.v014/scene/td_test.ma&with_scene=True"',
        'lxscript -p cjd -a katana -s set_scene_export_by_any_scene_file -o "file=/l/prod/cjd/publish/assets/chr/td_test/srf/surfacing/td_test.srf.surfacing.v014/scene/td_test.katana&with_scene=True"'
        'lxscript -p cjd -a houdini -s set_geometry_uv_map_unify -o "file=/home/dongchangbao/.lynxi/temporary/2021_0903/test.usd"'
    )


def main():
    try:
        opts, args = getopt.getopt(
            argv[1:],
            'hp:a:s:o:',
            ['help', 'project=', 'application=', 'script=', 'option=']
        )
        project, engine, script, option = [None] * 4
        for key, value in opts:
            if key in ('-h', '--help'):
                usage()
                sys.exit()
            elif key in ('-p', '--project'):
                project = value
            elif key in ('-a', '--application'):
                engine = value
            elif key in ('-s', '--script'):
                script = value
            elif key in ('-o', '--option'):
                option = value
        #
        set_script_run(project, engine, script, option)
    #
    except getopt.GetoptError:
        print('argv error')


def set_script_run(project, engine, script, option):
    from lxutil import utl_core
    # use maya python
    if engine == 'python':
        cmd_args = [
            r'-c "mayapy {}/script/bin/scp_utility_run.py \"{}\" \"{}\""'.format(
                os.environ.get('REZ_LXDCC_BASE'),
                script,
                option
            )
        ]
    # use maya batch
    elif engine == 'maya':
        cmd_args = [
            r'-- maya -batch -command "python(\"import lxmaya_fnc.scripts as mya_fnc_scripts;mya_fnc_scripts.{}(option=\\\"{}\\\")\")"'.format(
                script,
                option
            )
        ]
    # use maya python
    elif engine == 'maya-python':
        cmd_args = [
            r'-c "mayapy {}/script/bin/scp_maya_run.py \"{}\" \"{}\""'.format(
                os.environ.get('REZ_LXDCC_BASE'),
                script,
                option
            )
        ]
    # use maya render
    elif engine == 'maya-render':
        cmd_args = utl_core.MayaArnoldRenderCommand(option).get()
    # use houdini python
    elif engine == 'houdini':
        cmd_args = [
            r'-c "hython {}/script/bin/scp_houdini_run.py \"{}\" \"{}\""'.format(
                os.environ.get('REZ_LXDCC_BASE'),
                script,
                option
            )
        ]
    # use houdini python
    elif engine == 'houdini-python':
        cmd_args = [
            r'-c "hython {}/script/bin/scp_houdini_run.py \"{}\" \"{}\""'.format(
                os.environ.get('REZ_LXDCC_BASE'),
                script,
                option
            )
        ]
    #
    elif engine == 'katana':
        cmd_args = [
            r'-c "katana --script={}/script/bin/scp_katana_run.py \"{}\" \"{}\""'.format(
                os.environ.get('REZ_LXDCC_BASE'),
                script,
                option
            )
        ]
    elif engine == 'katana-python':
        cmd_args = [
            r'-c "katana --script={}/script/bin/scp_katana_run.py \"{}\" \"{}\""'.format(
                os.environ.get('REZ_LXDCC_BASE'),
                script,
                option
            )
        ]
    #
    elif engine == 'katana-render':
        cmd_args = get_katana_render_cmd_args(option)
    #
    elif engine == 'usd':
        cmd_args = [
            r'-- maya -batch -command "python(\"import lxusd_fnc.scripts as usd_fnc_scripts;usd_fnc_scripts.{}(option=\\\"{}\\\")\")"'.format(
                script,
                option
            )
        ]
    elif engine == 'shotgun':
        cmd_args = [
            r'-c "mayapy {}/script/bin/scp_shotgun_run.py \"{}\" \"{}\""'.format(
                os.environ.get('REZ_LXDCC_BASE'),
                script,
                option
            )
        ]
        # cmd_args = [
        #     r'-- maya -batch -command "python(\"import lxshotgun_fnc.scripts as stg_fnc_scripts;stg_fnc_scripts.{}(option=\\\"{}\\\")\")"'.format(
        #         script,
        #         option
        #     )
        # ]
    else:
        raise TypeError()
    #
    application = engine.split('-')[0]
    utl_core.AppLauncher(
        project=project, application=application
    ).set_cmd_run_with_result(
        ' '.join(cmd_args)
    )


def get_katana_render_cmd_args(option):
    from lxbasic import bsc_core
    #
    option_opt = bsc_core.KeywordArgumentsOpt(option)
    #
    cmd_args = [
        r'-c "katana --batch --katana-file=\"{render_file}\" -t {start_index}-{end_index} --render-node=\"{renderer}\""'.format(
            **option_opt.value
        )
    ]
    return cmd_args


if __name__ == '__main__':
    main()
