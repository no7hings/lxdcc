# coding:utf-8
from __future__ import print_function

import sys

import getopt

argv = sys.argv


def main():
    try:
        sys.stdout.write('execute lxhook-command from: "{}"\n'.format(__file__))
        opts, args = getopt.getopt(
            argv[1:],
            'ho:',
            ['help', 'option=']
        )
        option = None
        for key, value in opts:
            if key in ('-h', '--help'):
                __print_help()
                #
                sys.exit()
            elif key in ('-o', '--option'):
                option = value
        #
        if option is not None:
            __execute_with_option(option)
    #
    except getopt.GetoptError:
        sys.stdout.write('argv error\n')


def __print_help():
    sys.stdout.write(
        '***** lxhook-command *****\n'
        '\n'
        #
        '-h or --help: show help\n'
    )


def __execute_with_option(option):
    from lxbasic import bsc_core
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    option_hook_key = option_opt.get('option_hook_key')
    if option_hook_key:
        __execute_option_hook(option)
    else:
        hook_key = option_opt.get('hook_key')
        if hook_key:
            __execute_hook(option)


# hook
def __execute_hook(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxbasic.extra.methods as utl_etr_methods
    #
    import lxsession.commands as ssn_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    hook_key = option_opt.get('hook_key')
    hook_args = ssn_commands.get_hook_args(hook_key)
    if hook_args:
        session, fnc = hook_args
        #
        packages_extend = utl_etr_methods.EtrUtility.get_base_packages_extend()
        # add extend packages
        opt_packages_extend = session.get_packages_extend()
        if opt_packages_extend:
            packages_extend.extend(opt_packages_extend)
        #
        cmd = utl_etr_methods.EtrUtility.get_base_command(
                args_execute=['-- lxhook-python -o "{}"'.format(option)],
                packages_extend=packages_extend
            )
        #
        environs_extend = {}
        _ = bsc_core.EnvironMtd.get('LYNXI_RESOURCES')
        if _:
            environs_extend['LYNXI_RESOURCES'] = (_, 'prepend')
        # run cmd by subprocess
        utl_core.SubProcessRunner.set_run_with_result_use_thread(
            cmd, environs_extend=environs_extend
        )


# option hook
def __execute_option_hook(option):
    from lxbasic import bsc_core

    import lxsession.commands as ssn_commands

    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    hook_args = ssn_commands.get_option_hook_args(option)
    if hook_args:
        session, fnc = hook_args

        deadline_enable = option_opt.get_as_boolean('deadline_enable')
        if deadline_enable is True:
            session.set_execute_by_deadline()
        else:
            session.set_execute_by_shell()


if __name__ == '__main__':
    main()
