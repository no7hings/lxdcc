# coding:utf-8
from __future__ import print_function

import sys

import os

import getopt


def main(argv):
    try:
        sys.stdout.write('execute lxhook-engine from: "{}"\n'.format(__file__))
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


def __execute_with_option(option):
    from lxbasic import bsc_core
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    option_hook_key = option_opt.get('option_hook_key')
    if option_hook_key:
        __execute_option_hook(hook_option=option)


def __execute_option_hook(hook_option):
    """
    :param hook_option:
    :return:
    """
    from lxbasic import bsc_core
    #
    import lxresolver.commands as rsv_commands
    #
    from lxutil import utl_core
    #
    from lxsession import ssn_core
    #
    resolver = rsv_commands.get_resolver()
    #
    all_hook_engines = ssn_core.SsnHookEngineMtd.get_all()
    option_opt = bsc_core.ArgDictStringOpt(hook_option)
    #
    project = option_opt.get('project')
    rsv_project = resolver.get_rsv_project(project=project)
    if rsv_project is None:
        raise RuntimeError()
    #
    hook_engine = option_opt.get('hook_engine')
    # check engine is in configure
    if hook_engine not in all_hook_engines:
        raise RuntimeError(
            utl_core.Log.set_module_error_trace(
                'hook-run',
                u'engine="{}" is not available'.format(hook_engine)
            )
        )
    #
    rez_beta = option_opt.get('rez_beta') or False
    if rez_beta is True:
        bsc_core.EnvironMtd.set(
            'REZ_BETA', '1'
        )
    #
    kwargs = option_opt.value
    kwargs.update(
        dict(
            lxdcc_root=os.environ.get('LXDCC_BASE'),
            hook_option=hook_option,
        )
    )
    engine_args_execute = []
    engine_packages_extend = []
    # add extend packages
    hook_package_extend = option_opt.get('extend_packages', as_array=True)
    if hook_package_extend:
        engine_packages_extend.extend(
            hook_package_extend
        )
    #
    engine_args_execute.append(
        ssn_core.SsnHookEngineMtd.get_command(
            **kwargs
        )
    )
    #
    application = hook_engine.split('-')[0]
    #
    rsv_app = rsv_project.get_rsv_app(
        application=application
    )
    if rsv_app is None:
        raise RuntimeError()
    #
    use_thread = option_opt.get('use_thread') or False
    # add extend environs
    environs_extend = {}
    #
    _ = bsc_core.EnvironMtd.get('LYNXI_RESOURCES')
    if _:
        environs_extend['LYNXI_RESOURCES'] = _
    #
    frame_scheme = rsv_project.get_frame_scheme()
    if frame_scheme == 'new':
        engine_packages_extend.extend(
            ['lxdcc', 'lxdcc_lib', 'lxdcc_gui', 'lxdcc_rsc']
        )
    #
    command = rsv_app.get_command(
        args_execute=engine_args_execute,
        packages_extend=engine_packages_extend
    )
    #
    if use_thread is True:
        rsv_app.execute_with_result_use_thread(
            command, extend_environs=environs_extend
        )
    else:
        rsv_app.execute_with_result(
            command, extend_environs=environs_extend
        )


if __name__ == '__main__':
    main(sys.argv)
