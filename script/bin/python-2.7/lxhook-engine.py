# coding:utf-8
from __future__ import print_function

import sys

import os

import getopt


def main(argv):
    try:
        opts, args = getopt.getopt(
            argv[1:],
            'ho:',
            ['help', 'option=']
        )
        option = None
        for key, value in opts:
            if key in ('-h', '--help'):
                __set_help_print()
                #
                sys.exit()
            elif key in ('-o', '--option'):
                option = value
        #
        if option is not None:
            __set_run_by_option(option)
    #
    except getopt.GetoptError:
        print('argv error')


def __set_help_print():
    print (
        '***** lxhook-engine *****\n'
        '\n'
        'run command(s) by rez-env and application program\n'
        '\n'
        '-h or --help: show help\n'
        '-o or --option: set run option\n'
        '\n'
        'engines:\n'
        '    python,'
        '    maya, maya-python,\n'
        '    houdini, houdini-python,\n'
        '    katana, katana-python...\n'
        '\n'
        '***** lxhook-engine *****\n'
    )


def __set_run_by_option(option):
    from lxbasic import bsc_core
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    option_hook_key = option_opt.get('option_hook_key')
    if option_hook_key:
        __set_option_hook_run(hook_option=option)


def __set_option_hook_run(hook_option):
    """
    :param hook_option:
    :return:
    """
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    from lxsession import ssn_core
    #
    all_hook_engines = ssn_core.SsnHookEngineMtd.get_all()
    option_opt = bsc_core.ArgDictStringOpt(hook_option)
    #
    project = option_opt.get('project')
    hook_engine = option_opt.get('hook_engine')
    # check engine is in configure
    if hook_engine in all_hook_engines:
        rez_beta = option_opt.get('rez_beta') or False
        if rez_beta is True:
            bsc_core.EnvironMtd.set(
                'REZ_BETA', '1'
            )
        #
        kwargs = option_opt.value
        kwargs.update(
            dict(
                lxdcc_root=os.environ.get('REZ_LXDCC_BASE'),
                hook_option=hook_option,
            )
        )
        cmd_args = []
        # add extend packages
        extend_packages = option_opt.get('extend_packages', as_array=True)
        if extend_packages:
            cmd_args.append(' '.join(extend_packages))
        #
        cmd_args.append(
            ssn_core.SsnHookEngineMtd.get_command(
                **kwargs
            )
        )
        #
        application = hook_engine.split('-')[0]
        #
        use_thread = option_opt.get('use_thread') or False
        # add extend environs
        extend_environs = {}
        #
        _ = bsc_core.EnvironMtd.get('LYNXI_RESOURCES')
        if _:
            extend_environs['LYNXI_RESOURCES'] = _
        #
        if use_thread is True:
            utl_core.AppLauncher(
                project=project,
                application=application
            ).set_cmd_run_with_result_use_thread(
                ' '.join(cmd_args),
                extend_environs=extend_environs
            )
        else:
            utl_core.AppLauncher(
                project=project,
                application=application
            ).set_cmd_run_with_result(
                ' '.join(cmd_args),
                extend_environs=extend_environs
            )
    else:
        raise TypeError(
            utl_core.Log.set_module_error_trace(
                'hook-run',
                u'engine="{}" is not available'.format(hook_engine)
            )
        )


if __name__ == '__main__':
    main(sys.argv)
