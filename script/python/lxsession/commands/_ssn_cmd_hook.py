# coding:utf-8
import functools

import types


def get_hook_args(key, search_paths=None):
    from lxbasic import bsc_core
    #
    from lxsession import ssn_core
    #
    import lxsession.objects as ssn_objects

    import lxcontent.objects as ctt_objects
    #
    yaml_file_path = ssn_core.SsnHookFileMtd.get_yaml(key, search_paths)
    if yaml_file_path:
        yaml_file_opt = bsc_core.StgFileOpt(yaml_file_path)
        configure = ctt_objects.Configure(value=yaml_file_opt.path)
        type_name = configure.get('option.type')
        if type_name == 'application':
            session = ssn_objects.ApplicationSession(
                type=type_name,
                hook=key,
                configure=configure
            )
        elif type_name == 'kit-panel':
            session = ssn_objects.GuiSession(
                type=type_name,
                hook=key,
                configure=configure
            )
        elif type_name in {
            'tool',
            'dcc-tool',
        }:
            session = ssn_objects.ToolSession(
                type=type_name,
                hook=key,
                configure=configure
            )
        elif type_name in {
            'tool-panel', 'kit-panel',
            'dcc-tool-panel', 'dcc-menu',
            'rsv-tool-panel', 'rsv-loader', 'rsv-publisher'
        }:
            session = ssn_objects.GuiSession(
                type=type_name,
                hook=key,
                configure=configure
            )
        elif type_name in {
            'python-command', 'shell-command'
        }:
            session = ssn_objects.CommandSession(
                type=type_name,
                hook=key,
                configure=configure
            )
        else:
            raise TypeError()
        session.set_configure_yaml_file(yaml_file_path)
        python_file_path = ssn_core.SsnHookFileMtd.get_python(key, search_paths)
        if python_file_path is not None:
            session.set_python_script_file(python_file_path)
        shell_file_path = ssn_core.SsnHookFileMtd.get_shell(key, search_paths)
        if shell_file_path:
            session.set_shell_script_file(shell_file_path)
        #
        execute_fnc = functools.partial(session.execute)
        return session, execute_fnc


def set_hook_execute(key):
    from lxbasic import bsc_core
    #
    hook_args = get_hook_args(key)
    if hook_args is not None:
        session, execute_fnc = hook_args
        execute_fnc()
        return session
    else:
        bsc_core.LogMtd.trace_method_warning(
            'hook execute',
            'hook_key="{}" is not found'.format(key)
        )


def get_option_hook_args(option, search_paths=None):
    def execute_fnc():
        session.execute_python_file(
            python_file_path, session=session
        )

    from lxbasic import bsc_core

    import lxcontent.objects as ctt_objects

    from lxsession import ssn_core

    import lxsession.objects as ssn_objects

    option_opt = bsc_core.ArgDictStringOpt(option)

    option_hook_key = option_opt.get('option_hook_key')

    yaml_file_path = ssn_core.SsnOptionHookFileMtd.get_yaml(option_hook_key, search_paths)
    if yaml_file_path:
        python_file_path = ssn_core.SsnOptionHookFileMtd.get_python(option_hook_key, search_paths)
        python_file_opt = bsc_core.StgFileOpt(python_file_path)
        yaml_file_opt = bsc_core.StgFileOpt(yaml_file_path)
        if python_file_opt.get_is_exists() is True and yaml_file_opt.get_is_exists() is True:
            configure = ctt_objects.Configure(value=yaml_file_opt.path)
            type_name = configure.get('option.type')
            #
            session = None
            if type_name == 'action':
                session = ssn_objects.OptionActionSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'dtb-action':
                session = ssn_objects.DatabaseOptionActionSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'launcher':
                session = ssn_objects.OptionLauncherSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'tool-panel':
                session = ssn_objects.OptionToolPanelSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'rsv-tool-panel':
                session = ssn_objects.RsvOptionToolPanelSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'method':
                session = ssn_objects.SsnOptionMethod(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name in {'rsv-project-batcher', 'rsv-project-method'}:
                session = ssn_objects.RsvProjectMethodSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name in {'rsv-task-batcher', 'rsv-task-method'}:
                session = ssn_objects.RsvTaskMethodSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'kit-panel':
                session = ssn_objects.OptionGuiSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            else:
                raise TypeError()
            #
            session.set_python_script_file(python_file_path)
            session.set_configure_yaml_file(yaml_file_path)
            return session, execute_fnc
    else:
        raise RuntimeError(
            bsc_core.LogMtd.trace_method_error(
                'option-hook gain',
                'option-hook key="{}" configue (.yml) is not found'.format(option_hook_key)
            )
        )


def get_option_hook_configure(option):
    from lxbasic import bsc_core
    #
    import lxcontent.objects as ctt_objects
    #
    from lxsession import ssn_core
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    option_hook_key = option_opt.get('option_hook_key')
    #
    yaml_file_path = ssn_core.SsnOptionHookFileMtd.get_yaml(option_hook_key)
    if yaml_file_path:
        yaml_file_opt = bsc_core.StgFileOpt(yaml_file_path)
        if yaml_file_opt.get_is_exists() is True:
            return ctt_objects.Configure(value=yaml_file_opt.path)


def set_option_hook_execute(option):
    hook_args = get_option_hook_args(option)
    if hook_args is not None:
        session, execute_fnc = hook_args
        execute_fnc()
        return session


def get_option_hook_session(option):
    hook_args = get_option_hook_args(option)
    if hook_args is not None:
        session, execute_fnc = hook_args
        return session


def get_option_hook_shell_script_command(option):
    hook_args = get_option_hook_args(option)
    if hook_args is not None:
        session, execute_fnc = hook_args
        return session, session.get_shell_script_command()


def set_option_hook_execute_by_shell(option, block=False):
    hook_args = get_option_hook_args(option)
    if hook_args is not None:
        session, execute_fnc = hook_args
        #
        session.set_execute_by_shell(block)
        return session


def set_option_hook_execute_by_deadline(option):
    hook_args = get_option_hook_args(option)
    if hook_args is not None:
        session, execute_fnc = hook_args
        #
        session.set_execute_by_deadline()
        return session


if __name__ == '__main__':
    pass
