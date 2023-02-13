# coding:utf-8
from __future__ import print_function

import sys

import os

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
            __set_run(option)
    #
    except getopt.GetoptError:
        print('argv error')


def __set_help_print():
    print (
        '***** lxhook-python *****\n'
        '\n'
        #
        '-h or --help: show help\n'
    )


def __set_run(option):
    from lxbasic import bsc_core
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    bsc_core.EnvironMtd.set(
        'hook_start_m', str(bsc_core.TimeMtd.get_minute())
    )
    bsc_core.EnvironMtd.set(
        'hook_start_s', str(bsc_core.TimeMtd.get_second())
    )
    # do not use thread, there will be run with subprocess use thread by lxhook-command
    option_hook_key = option_opt.get('option_hook_key')
    if option_hook_key:
        deadline_enable = option_opt.get_as_boolean('deadline_enable')
        if deadline_enable is True:
            __set_option_hook_execute_by_deadline(hook_option=option)
        else:
            __set_option_hook_execute(hook_option=option)
    else:
        hook_key = option_opt.get('hook_key')
        if hook_key:
            __set_hook_execute(hook_key)


def __set_hook_execute(hook_key):
    import lxsession.commands as ssn_commands; ssn_commands.set_hook_execute(hook_key)


def __set_option_hook_execute(hook_option):
    import lxsession.commands as ssn_commands; ssn_commands.set_option_hook_execute(hook_option)


def __set_option_hook_execute_by_deadline(hook_option):
    import lxsession.commands as ssn_commands; ssn_commands.set_option_hook_execute_by_deadline(hook_option)


if __name__ == '__main__':
    main()
