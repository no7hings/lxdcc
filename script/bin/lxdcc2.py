# coding:utf-8
from __future__ import print_function

import sys

import getopt

import os

import collections

argv = sys.argv


def usage():
    print (
        '***** lxdcc2 *****\n'
        '\n'
        #
        '-h or --help: show help\n'
        #
        '-s or --script: script\n'
        '-o or --option: option\n'
        '\n'
        'lxdcc2 -s maya-scene-export -o "file=`pwd`/{asset}.ma"\n'
        'lxdcc2 -s maya-geometry-export -o "file=`pwd`/{asset}.ma&with_geometry_usd=True"\n'
        'lxdcc2 -s shotgun-export -o "file=`pwd`/{asset}.ma&with_version=True"\n'
        '\n'
        'lxdcc2 -s maya-scene-info-export -o "file=`pwd`/{file}.ma&root=/master/hi"\n'
        '***** lxdcc2 *****\n'
    )


def main():
    try:
        opts, args = getopt.getopt(
            argv[1:], 'hs:o:c:',
            ['help', 'script=', 'option=', 'command=']
        )
        script, option, command = [None] * 3
        for key, value in opts:
            if key in ('-h', '--help'):
                usage()
                sys.exit()
            elif key in ('-s', '--script'):
                script = value
            elif key in ('-o', '--option'):
                option = value
            elif key in ('-c', '--command'):
                command = value
        #
        if script == 'maya-scene-export':
            set_maya_scene_export_run(option)
        elif script == 'katana-scene-export':
            set_katana_scene_export_run(option)
        elif script == 'maya-geometry-export':
            set_maya_geometry_export_run(option)
        elif script == 'katana-geometry-export':
            set_katana_geometry_export_run(option)
        elif script == 'maya-look-export':
            set_maya_look_export_run(option)
        elif script == 'katana-look-export':
            set_katana_look_export_run(option)
        elif script == 'usd-export':
            set_usd_export_run(option)
        elif script == 'shotgun-export':
            set_shotgun_export_run(option)
        elif script == 'maya-scene-info-export':
            set_maya_scene_info_export(option)
        #
        elif script == 'maya-geometry-import':
            set_maya_geometry_import_run(option)
        #
        elif script == 'hook':
            set_hook_run(option)
        #
        elif script == 'asset-loader':
            set_asset_loader_panel_show()
        elif script == 'asset-batcher':
            set_asset_batcher_panel_show()
        elif script == 'shot-loader':
            set_shot_loader_panel_show()
    #
    except getopt.GetoptError:
        print('argv error')


def set_dcc_script_run(project, application, fnc, option):
    from lxutil import utl_core
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    utl_core.Log.set_module_result_trace(
        key,
        'option="{}"'.format(option)
    )
    if application == 'maya':
        cmd_args = [r'-- maya -batch -command "python(\"print \\\"abc\\\"\")"']
    elif application == 'houdini':
        cmd_args = [r'-c "hython " ']
    elif application == 'katana':
        cmd_args = [
            r'-c "katana --script={}/script/bin/scp_katana_run.py \"{}\" \"{}\""'.format(
                os.environ.get('REZ_LXDCC_BASE'), fnc, option
            )
        ]
    else:
        raise TypeError()
    #
    utl_core.AppLauncher(
        project=project, application=application
    ).set_cmd_run_with_result(
        ' '.join(cmd_args)
    )


def set_maya_scene_export_run(option):
    from lxutil import utl_core
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    utl_core.Log.set_module_result_trace(
        key,
        'option="{}"'.format(option)
    )
    py_cmd = r'import lxmaya_fnc.scripts as mya_fnc_scripts;mya_fnc_scripts.set_scene_export_by_any_scene_file(option=\\\"{}\\\")'.format(
        option
    )
    cmd = r'rez-env lxdcc pg_production_lib mtoa pgmaya usd maya -- maya -batch -command "python(\"{}\")"'.format(
        py_cmd
    )
    utl_core.SubProcessRunner.set_run_with_result(cmd)


def set_katana_scene_export_run(option):
    from lxutil import utl_core
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    utl_core.Log.set_module_result_trace(
        key,
        'option="{}"'.format(option)
    )
    #
    cmd = r'rez-env lxdcc ktoa pgkatana usd katana -c "katana --script={}/script/bin/scp_katana_run.py \"set_scene_export_by_any_scene_file\" \"{}\""'.format(
        os.environ.get('REZ_LXDCC_BASE'), option
    )
    utl_core.SubProcessRunner.set_run_with_result(cmd)


def set_maya_geometry_export_run(option):
    from lxutil import utl_core
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name

    utl_core.Log.set_module_result_trace(
        key,
        'option="{}"'.format(option)
    )
    py_cmd = r'import lxmaya_fnc.scripts as mya_fnc_scripts;mya_fnc_scripts.set_geometry_export_by_any_scene_file(option=\\\"{}\\\")'.format(
        option
    )
    cmd = r'rez-env lxdcc pg_production_lib mtoa pgmaya usd maya -- maya -batch -command "python(\"{}\")"'.format(
        py_cmd
    )
    utl_core.SubProcessRunner.set_run_with_result(cmd)


def set_katana_geometry_export_run(option):
    from lxutil import utl_core
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    utl_core.Log.set_module_result_trace(
        key,
        'option="{}"'.format(option)
    )
    #
    cmd = r'rez-env lxdcc ktoa pgkatana usd katana -c "katana --script={}/script/bin/scp_katana_run.py \"set_geometry_export_by_any_scene_file\" \"{}\""'.format(
        os.environ.get('REZ_LXDCC_BASE'), option
    )
    utl_core.SubProcessRunner.set_run_with_result(cmd)


def set_maya_look_export_run(option):
    from lxutil import utl_core
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    utl_core.Log.set_module_result_trace(
        key,
        'option="{}"'.format(option)
    )
    py_cmd = r'import lxmaya_fnc.scripts as mya_fnc_scripts;mya_fnc_scripts.set_look_export_by_any_scene_file(option=\\\"{}\\\")'.format(
        option
    )
    cmd = r'rez-env lxdcc pg_production_lib mtoa pgmaya usd maya -- maya -batch -command "python(\"{}\")"'.format(
        py_cmd
    )
    utl_core.SubProcessRunner.set_run_with_result(cmd)


def set_katana_look_export_run(option):
    from lxutil import utl_core
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    utl_core.Log.set_module_result_trace(
        key,
        'option="{}"'.format(option)
    )
    #
    cmd = r'rez-env lxdcc ktoa pgkatana usd katana -c "katana --script={}/script/bin/scp_katana_run.py \"set_look_export_by_any_scene_file\" \"{}\""'.format(
        os.environ.get('REZ_LXDCC_BASE'), option
    )
    utl_core.SubProcessRunner.set_run_with_result(cmd)


def set_maya_scene_info_export(option):
    from lxbasic import bsc_core

    from lxutil import utl_core

    import lxutil.fnc.exporters as utl_fnc_exporters
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name

    utl_core.Log.set_module_result_trace(
        key,
        'option="{}"'.format(option)
    )

    option_opt = bsc_core.KeywordArgumentsOpt(option)

    file_path = option_opt.get('file')
    root = option_opt.get('root')

    utl_fnc_exporters.DotMaSceneInfoExporter(
        option=dict(
            file_path=file_path,
            root=root
        )
    ).set_run()


def set_maya_geometry_import_run(option):
    from lxutil import utl_core
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    utl_core.Log.set_module_result_trace(
        key,
        'option="{}"'.format(option)
    )
    py_cmd = r'import lxmaya_fnc.scripts as mya_fnc_scripts;mya_fnc_scripts.set_geometry_import_by_any_scene_file(option=\\\"{}\\\")'.format(
        option
    )
    cmd = r'rez-env lxdcc pg_production_lib mtoa pgmaya usd maya -- maya -batch -command "python(\"{}\")"'.format(
        py_cmd
    )
    utl_core.SubProcessRunner.set_run_with_result(cmd)


def set_usd_export_run(option):
    from lxutil import utl_core
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    utl_core.Log.set_module_result_trace(
        key,
        'option="{}"'.format(option)
    )
    py_cmd = r'import lxusd_fnc.scripts as usd_fnc_scripts;usd_fnc_scripts.set_usd_export_by_any_scene_file(option=\\\"{}\\\")'.format(
        option
    )
    cmd = r'rez-env lxdcc pg_production_lib mtoa pgmaya usd maya -- maya -batch -command "python(\"{}\")"'.format(
        py_cmd
    )
    utl_core.SubProcessRunner.set_run_with_result(cmd)


def set_shotgun_export_run(option):
    from lxutil import utl_core
    # noinspection PyUnresolvedReferences
    key = sys._getframe().f_code.co_name
    #
    utl_core.Log.set_module_result_trace(
        key,
        'option="{}"'.format(option)
    )
    py_cmd = r'import lxshotgun_fnc.scripts as stg_fnc_scripts;stg_fnc_scripts.set_shotgun_export_by_any_scene_file(option=\\\"{}\\\")'.format(
        option
    )
    cmd = r'rez-env lxdcc pg_production_lib mtoa pgmaya usd maya -- maya -batch -command "python(\"{}\")"'.format(
        py_cmd
    )
    utl_core.SubProcessRunner.set_run_with_result(cmd)


def set_test_window_show():
    import lxutil_gui.proxy.widgets as utl_prx_widgets

    class TestWindow(utl_prx_widgets.PrxToolWindow):
        def __init__(self, *args, **kwargs):
            super(TestWindow, self).__init__(*args, **kwargs)
            self._test_()

        def _test_(self):
            n = utl_prx_widgets.PrxNode()
            self.set_widget_add(n)
            p = n.set_port_add(utl_prx_widgets.PrxEnumeratePort_('test_0', 'Test-0'))
            p.set(['a', 'b', 'c'])

            p = n.set_port_add(utl_prx_widgets.PrxPortForString('test_1', 'Test-1'))
            p.set('a')

            p.set_use_as_storage(True)
    #
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    #
    w.set_window_show()
    #
    sys.exit(app.exec_())


def set_hook_run(key):
    import lxsession.commands as ssn_commands; ssn_commands.set_hook_execute(key)


def set_asset_loader_panel_show():
    set_hook_run('rsv-panels/asset-loader')


def set_asset_batcher_panel_show():
    set_hook_run('rsv-panels/asset-batcher')


def set_shot_loader_panel_show():
    set_hook_run('rsv-panels/shot-loader')


if __name__ == '__main__':
    main()
