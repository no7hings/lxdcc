# coding:utf-8
from __future__ import print_function

import sys

import os

import getopt


def main(argv):
    try:
        args_opt, args_execute = __get_opt_args(argv[1:])
        opt_kwargs, opt_args = getopt.getopt(
            args_opt,
            'ha:o:',
            ['help', 'app=', 'option=']
        )
        packages_extend = None
        option = None
        if opt_kwargs:
            for i_key, i_value in opt_kwargs:
                if i_key in ('-h', '--help'):
                    __print_help()
                    #
                    sys.exit()
                elif i_key in ('-a', '--app'):
                    launcher = i_value
                    if '.' not in launcher:
                        raise SyntaxError()
                    _ = launcher.split('.')
                    if len(_) != 2:
                        raise SyntaxError()
                    i_project, i_application = _
                    option = 'project={}&application={}'.format(i_project, i_application)
                elif i_key in ('-o', '--option'):
                    option = i_value
            #
            if opt_args:
                packages_extend = opt_args
                args_execute = args_execute
        else:
            if opt_args:
                launcher = opt_args[0]
                if '.' not in launcher:
                    raise SyntaxError()
                _ = launcher.split('.')
                if len(_) != 2:
                    raise SyntaxError()
                #
                project, application = _
                #
                packages_extend = opt_args[1:]
                #
                option = 'project={}&application={}'.format(project, application)
                args_execute = ['-- {}'.format(application)]
        #
        if option is not None:
            __execute_with_option(option, args_execute, packages_extend)
    #
    except getopt.GetoptError:
        # import traceback
        # sys.stderr.write(traceback.print_exc())
        sys.stderr.write('argv error\n')


def __get_opt_args(args):
    if '-c' in args:
        idx = args.index('-c')
        args_opt = args[:idx]
        args_e = args[idx+1:]
        args_execute = '-c "{}"'.format(' '.join(map(lambda x: x.replace('"', '\\\"'), args_e)))
        return args_opt, [args_execute]
    elif '--' in args:
        idx = args.index('--')
        args_opt = args[:idx]
        args_e = args[idx+1:]
        args_execute = '-- {}'.format(' '.join(args_e))
        return args_opt, [args_execute]
    return args, None


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


def __execute_with_option(option, args_execute, package_extend):
    from lxbasic import bsc_core
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
    rsv_launcher = rsv_project.get_rsv_app(application=application)
    sys.stdout.write(
        (
            '\033[34m'
            'resolved command:\n'
            '\033[32m'
            '{}'
            '\033[0m\n'
        ).format(rsv_launcher.get_command(args_execute, package_extend))
    )
    if args_execute:
        rsv_launcher.execute_command(args_execute, package_extend)


if __name__ == '__main__':
    main(sys.argv)
