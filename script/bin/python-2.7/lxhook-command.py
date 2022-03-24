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
        '***** lxhook-command *****\n'
        '\n'
        #
        '-h or --help: show help\n'
    )


def __set_run_by_option(option):
    import functools
    #
    import threading
    #
    from lxbasic import bsc_core
    #
    option_opt = bsc_core.KeywordArgumentsOpt(option)
    option_hook_key = option_opt.get('option_hook_key')
    if option_hook_key:
        __set_option_hook_run(option)
    else:
        hook_key = option_opt.get('hook_key')
        if hook_key:
            # t = threading.Thread(
            #     target=functools.partial(__set_hook_run, option=option)
            # )
            # t.start()
            __set_hook_run(option)


# hook
def __set_hook_run(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxsession.commands as ssn_commands
    #
    option_opt = bsc_core.KeywordArgumentsOpt(option)
    #
    hook_key = option_opt.get('hook_key')
    hook_args = ssn_commands.get_hook_args(hook_key)
    if hook_args:
        session, fnc = hook_args
        #
        packages = session.get_rez_extend_packages()
        #
        if packages:
            cmd = 'rez-env lxdcc {} -- lxhook-python -o "{}"'.format('' .join(packages), option)
        else:
            cmd = 'rez-env lxdcc -- lxhook-python -o "{}"'.format(option)
        # run cmd by subprocess
        utl_core.SubProcessRunner.set_run_with_result_use_thread(
            cmd
        )


# option hook
def __set_option_hook_run(option):
    import lxsession.commands as ssn_commands
    #
    hook_args = ssn_commands.get_option_hook_args(option)
    if hook_args:
        session, fnc = hook_args
        #
        session.set_execute_by_shell()


if __name__ == '__main__':
    main()
