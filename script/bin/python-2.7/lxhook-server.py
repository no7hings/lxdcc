# coding:utf-8
from __future__ import print_function

import sys

import getopt

from flask import Flask

argv = sys.argv

app = Flask(__name__)


def main():
    try:
        opts, args = getopt.getopt(
            argv[1:],
            'ho:',
            ['help', 'option=']
        )
        option = [None] * 1
        for key, value in opts:
            if key in ('-h', '--help'):
                __print_help()
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
        '***** lxhook-server *****\n'
        '\n'
        #
        '-h or --help: show help\n'
    )


def __execute_with_option(option):
    import lxbasic.core as bsc_core
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    if option_opt.get('start_server') or False is True:
        __start_server()


def __start_server():
    import lxsession.configure as ssn_configure
    #
    app.run(
        host="0.0.0.0",
        debug=1,
        port=ssn_configure.Hook.PORT
    )


@app.route("/cmd-run")
def set_cmd_run():
    import functools

    import threading

    from flask import request

    import lxlog.core as log_core

    import lxbasic.core as bsc_core

    import lxsession.core as ssn_core

    kwargs = request.args

    unique_id = kwargs.get('uuid')
    if unique_id:
        hook_yml_file_path = ssn_core.SsnHookServerMtd.get_file_path(unique_id=unique_id)
        hook_yml_file = bsc_core.StgFileOpt(hook_yml_file_path)
        if hook_yml_file.get_is_exists() is True:
            raw = hook_yml_file.set_read()
            if raw:
                cmd = raw.get('cmd')
                if cmd:
                    log_core.Log.trace_method_result(
                        'hook run',
                        'key="{}"'.format(unique_id)
                    )
                    t = threading.Thread(
                        target=functools.partial(
                            bsc_core.SubProcessMtd.set_run, cmd=cmd
                        )
                    )
                    #
                    t.start()
        else:
            log_core.Log.trace_method_warning(
                'hook run',
                'key="{}" is non-exists'.format(hook_yml_file_path)
            )
    return ''


# if __name__ == '__main__':
#     app.run(host="0.0.0.0", debug=1, port=9527)

if __name__ == '__main__':
    main()
