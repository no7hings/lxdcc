# coding:utf-8
from __future__ import print_function

import sys

import getopt

argv = sys.argv


def main():
    try:
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
    import lxsession.commands as ssn_commands
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    hook_key = option_opt.get('hook_key')
    hook_args = ssn_commands.get_hook_args(hook_key)
    if hook_args:
        session, fnc = hook_args
        #
        # add extend packages
        extend_packages = session.get_rez_extend_packages()
        #
        if extend_packages:
            cmd = 'rez-env lxdcc {} -- lxhook-python -o "{}"'.format(' ' .join(extend_packages), option)
        else:
            cmd = 'rez-env lxdcc -- lxhook-python -o "{}"'.format(option)
        #
        extend_environs = {}
        _ = bsc_core.EnvironMtd.get('LYNXI_RESOURCES')
        if _:
            extend_environs['LYNXI_RESOURCES'] = _
        # run cmd by subprocess
        utl_core.SubProcessRunner.set_run_with_result_use_thread(
            cmd, extend_environs=extend_environs
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
