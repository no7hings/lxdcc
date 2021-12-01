# coding:utf-8
from __future__ import print_function

import sys

import getopt

import subprocess

import multiprocessing

import os

argv = sys.argv


def usage():
    print (
        u'***** lxdcc *****\n'
        u'\n'
        #
        u'-h or --help: show help-info\n'
        #
        u'-m or --method: method-name\n'
        u'  look-klf\n'
        u'      etc: "lxdcc -m look-klf -p project_name -a asset_name -s step_name -t task_name"\n'
        u'  scene_file_open\n'
        u'      etc: "lxdcc -m scene_file_open -p project_name -a asset_name -s step_name -t task_name"\n'
        u'  scene_builder_gui\n'
        u'      etc: "lxdcc -m scene_builder_gui -p project_name"\n'
        u'  katana\n'
        u'      etc: "lxdcc -m katana -p project_name"\n'
        #
        u'-p or --project: project-name\n'
        u'-a or --project: asset-name(s)\n'
        u'-s or --step: step-name\n'
        u'-t or --task: task-name\n'
        #
        u'-w or --workspace: workspace\n'
        #
        u'-o or --option: option(s)\n'
        u'\n'
        u'***** lxdcc *****\n'
    )


def main():
    try:
        opts, args = getopt.getopt(
            argv[1:], 'hm:p:a:s:t:w:o:',
            ['help', 'method=', 'project=', 'asset=', 'step=', 'task=', 'workspace=', 'option=']
        )
        method, project, asset, step, task, workspace, option = [None] * 7
        for key, value in opts:
            if key in ('-h', '--help'):
                usage()
                sys.exit()
            elif key in ('-m', '--method'):
                method = value
            elif key in ('-p', '--project'):
                project = value
            elif key in ('-a', '--asset'):
                if os.path.isfile(value):
                    with open(value) as f:
                        asset = [str(i).rstrip().lstrip() for i in f.readlines()]
                else:
                    asset = str(value).split(',')
            elif key in ('-s', '--step'):
                step = value
            elif key in ('-t', '--task'):
                task = value
            elif key in ('-w', '--workspace'):
                workspace = value
            elif key in ('-o', '--option'):
                option = str(value).split(',')
        #
        if method == 'look-klf':
            look_klf_method(method, project, asset, step, task, workspace, option)
        elif method == 'scene-builder-gui':
            scene_builder_gui(method, project)
        elif method == 'katana':
            katana(method, project)

    except getopt.GetoptError:
        print('argv error')


def look_klf_method(method, project, asset, step, task, workspace, option):
    from lxutil import utl_core, commands
    #
    e = commands.AssetTaskFileGain(project=project, asset=asset, step=step, task=task, workspace=workspace)
    rs = e.get_look_file_export_args()
    utl_core.Log.set_result_trace('method:"{}" is start.'.format(method))
    for k, v in rs.items():
        if v:
            file_args = v[-1]
            (geometry_file_path, hair_file_path, mtl_file_path), (look_file_path, source_katana_file_path) = file_args
            if option is not None:
                if 'ignore_exists' in option:
                    if os.path.isfile(look_file_path) is True:
                        utl_core.Log.set_result_trace('asset: "{}" is exists'.format(k))
                        continue
            utl_core.Log.set_result_trace('asset: "{}" is start.'.format(k))
            #
            cmd = 'rez-env lxdcc ktoa pgkatana katana -c "katana --script=$REZ_LXDCC_BASE/script/bin/look_klf_method.py {} {} {} {} {}"'.format(
                geometry_file_path, hair_file_path, mtl_file_path, look_file_path, source_katana_file_path
            )
            sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            #
            utl_core.Log.set_result_trace('asset: "{}" is complete.'.format(k))

    utl_core.Log.set_result_trace('method: "{}" is complete.'.format(method))


def scene_builder_gui(method, project):
    import sys
    #
    from PySide2 import QtWidgets
    #
    from lxutil_gui.panel import utl_pnl_widgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = utl_pnl_widgets.SceneBuildToolPanel()
    #
    w.set_window_show()
    sys.exit(app.exec_())


def katana(method, project):
    from lxutil import utl_core
    cmd = 'rez-env lxdcc ktoa pgkatana katana -c "katana"'.format()
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    [print(i) for i in p.stdout.readlines()]
    utl_core.Log.set_result_trace('method: "{}" is start.'.format(method))


if __name__ == '__main__':
    main()
