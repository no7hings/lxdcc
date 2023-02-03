# coding:utf-8
from __future__ import print_function

import sys

import getopt

from flask import Flask

argv = sys.argv

app = Flask(__name__)


def usage():
    print (
        '***** lxhook-python *****\n'
        '\n'
        #
        '-h or --help: show help\n'
    )


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
                usage()
                sys.exit()
            elif key in ('-o', '--option'):
                option = value
        #
        if option is not None:
            set_run_by_option(option)
    #
    except getopt.GetoptError:
        print('argv error')


def set_run_by_option(option):
    from lxbasic import bsc_core
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    start_server = option_opt.get('start_server') or False
    if start_server:
        set_server_start()


def set_server_start():
    from lxutil import utl_configure
    #
    app.run(
        host="0.0.0.0",
        debug=1,
        port=utl_configure.Hook.PORT
    )


@app.route("/cmd-run")
def set_cmd_run():
    import functools

    import threading

    from flask import request
    #
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    kwargs = request.args
    #
    unique_id = kwargs.get('uuid')
    if unique_id:
        hook_yml_file_path = bsc_core.SystemMtd.get_hook_file_path(unique_id=unique_id)
        hook_yml_file = bsc_core.StgFileOpt(hook_yml_file_path)
        if hook_yml_file.get_is_exists() is True:
            raw = hook_yml_file.set_read()
            if raw:
                cmd = raw.get('cmd')
                if cmd:
                    utl_core.Log.set_module_result_trace(
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
            utl_core.Log.set_module_warning_trace(
                'hook run',
                'key="{}" is non-exists'.format(hook_yml_file_path)
            )
    return ''


# if __name__ == '__main__':
#     app.run(host="0.0.0.0", debug=1, port=9527)

if __name__ == '__main__':
    main()
