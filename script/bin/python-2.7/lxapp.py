# coding:utf-8
from __future__ import print_function

import sys

import os

import getopt

KEY = 'lxapp'


def main(argv):
    try:
        opt_kwargs_0, opt_args_0 = getopt.getopt(
            argv[1:],
            'h',
            ['help']
        )
        option = None
        args_execute = None
        args_extend = None
        environs_extend = None
        if opt_kwargs_0:
            for i_key, i_value in opt_kwargs_0:
                if i_key in ('-h', '--help'):
                    __print_help()
                    #
                    sys.exit()
        # etc. nsa_dev.maya
        else:
            if opt_args_0:
                _ = __get_app_args(
                    opt_args_0
                )
                if _ is not None:
                    option, args_execute, args_extend, environs_extend = _
        #
        if option is not None:
            __execute_with_option(option, args_execute, args_extend, environs_extend)
    #
    except getopt.GetoptError:
        # import traceback
        # sys.stderr.write(traceback.print_exc())
        sys.stderr.write('argv error\n')


def __get_app_args(args):
    from lxbasic import bsc_core
    #
    bsc_core.LogMtd.trace_method_result(
        KEY,
        'execute from: {}'.format(__file__)
    )
    # etc. nsa_dev.maya
    launcher_arg = args[0]
    if '.' not in launcher_arg:
        raise SyntaxError(
            sys.stderr.write('argv error\n')
        )
    #
    _ = launcher_arg.split('.')
    if len(_) < 2:
        raise SyntaxError(
            sys.stderr.write('argv error\n')
        )
    #
    project = _[0]
    app_arg = '.'.join(_[1:])
    #
    import lxbasic.extra.methods as bsc_etr_methods
    #
    import lxresolver.commands as rsv_commands
    # find resolver project
    resolver = rsv_commands.get_resolver()
    rsv_project = resolver.get_rsv_project(project=project)
    if not rsv_project:
        return

    framework_scheme = rsv_project.get_framework_scheme()
    m = bsc_etr_methods.get_module(framework_scheme)
    #
    app_execute_mapper = m.EtrBase.get_app_execute_mapper(rsv_project)
    #
    if app_arg in app_execute_mapper:
        cfg = app_execute_mapper[app_arg]
        application = cfg['application']
        args_execute = cfg['args_execute']
    else:
        application = app_arg
        args_execute = ['-- {}'.format(application)]
    #
    args_extend = args[1:]
    args_task = None
    if len(args) == 2:
        arg_sub = args[1]
        # when arg_sub is file path, ignore
        if os.path.exists(arg_sub) is False:
            task_arg = arg_sub
            if '.' in task_arg:
                arg_sub = task_arg.split('.')
                if len(arg_sub) == 2:
                    resource, task = arg_sub
                    args_task = [project, resource, task]
                    args_extend = []
            # project task
            else:
                task = args[1]
                args_task = [project, project, task]
                args_extend = []
    #
    option = 'project={}&application={}'.format(project, application)
    return option, args_execute, args_extend, args_task


def __print_help():
    sys.stdout.write(
        '***** lxapp *****\n'
        'etc.\n'
        '# open app\n'
        'lxapp cgm.katana\n'
        'lxapp -a cgm.katana -- katana\n'
        'lxapp -a cgm.katana -c "katana"\n'
        '# execute script\n'
        'lxapp -a cgm.katana -- katana --script=script.py\n'
        'lxapp -a cgm.katana -c "katana --script=script.py"\n'
    )


def __execute_with_option(option, args_execute=None, args_extend=None, args_task=None):
    from lxbasic import bsc_core
    #
    import lxbasic.extra.methods as bsc_etr_methods
    #
    import lxresolver.commands as rsv_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    # find project
    project = option_opt.get('project')
    if not project:
        return
    # find resolver project
    resolver = rsv_commands.get_resolver()
    rsv_project = resolver.get_rsv_project(project=project)
    if not rsv_project:
        return
    #
    application = option_opt.get('application')
    if not application:
        return
    #
    opt_packages_extend = []
    #
    framework_scheme = rsv_project.get_framework_scheme()
    m = bsc_etr_methods.get_module(framework_scheme)
    framework_packages_extend = m.EtrBase.get_base_packages_extend()
    if framework_packages_extend:
        opt_packages_extend.extend(framework_packages_extend)
    #
    rsv_app = rsv_project.get_rsv_app(application=application)
    #
    command = rsv_app.get_command(
        args_execute=args_execute,
        args_extend=args_extend,
        packages_extend=opt_packages_extend
    )
    if command:
        sys.stdout.write(
            (
                '\033[34m'
                'resolved full command:\n'
                '\033[32m'
                '{}'
                '\033[0m\n'
            ).format(command)
        )
    #
    if args_task is not None:
        environs_extend = m.EtrBase.get_task_environs_extend(*args_task)
    else:
        environs_extend = m.EtrBase.get_project_environs_extend(project)
    #
    if environs_extend:
        sys.stdout.write(
            (
                '\033[34m'
                'resolved environments:\n'
                '\033[32m'
                '{}'
                '\033[0m\n'
            ).format('\n'.join(['{}={}'.format(k.rjust(20), v) for k, v in environs_extend.items()]))
        )
    if args_execute:
        rsv_app.execute_command(
            args_execute=args_execute,
            args_extend=args_extend,
            packages_extend=opt_packages_extend,
            #
            environs_extend=environs_extend,
            # clear_environ='auto'
        )


if __name__ == '__main__':
    main(sys.argv)
