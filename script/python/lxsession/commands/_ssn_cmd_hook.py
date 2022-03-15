# coding:utf-8


def get_hook_args(key):
    def execute_fnc():
        session._set_file_execute_(
            python_file_path, dict(session=session)
        )
    #
    import lxbasic.objects as bsc_objects
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    from lxsession import ssn_configure
    #
    import lxsession.objects as ssn_objects
    #
    import lxgui.objects as gui_objects
    #
    yaml_file_path = ssn_configure.Hooks.get_yaml_file(key)
    if yaml_file_path:
        python_file_path = ssn_configure.Hooks.get_python_file(key)
        python_file = utl_dcc_objects.OsPythonFile(python_file_path)
        yaml_file = utl_dcc_objects.OsFile(yaml_file_path)
        if python_file.get_is_exists() is True and yaml_file.get_is_exists() is True:
            configure = bsc_objects.Configure(value=yaml_file.path)
            type_name = configure.get('option.type')
            session = None
            if type_name == 'application':
                session = ssn_objects.ApplicationSession(
                    type=type_name,
                    hook=key,
                    configure=configure
                )
            elif type_name == 'tool-panel':
                session = gui_objects.ToolPanelSession(
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
            elif type_name == 'rsv-loader':
                session = gui_objects.RsvLoaderSession(
                    type=type_name,
                    hook=key,
                    configure=configure
                )
            else:
                raise TypeError()
            #
            if session is not None:
                session.set_hook_python_file(python_file_path)
                session.set_hook_yaml_file(yaml_file_path)
                return session, execute_fnc


def set_hook_execute(key):
    hook_args = get_hook_args(key)
    if hook_args is not None:
        session, execute_fnc = hook_args
        execute_fnc()


def set_hook_execute_by_shell(key):
    hook_args = get_hook_args(key)
    if hook_args is not None:
        session, execute_fnc = hook_args
        #
        # session.set_execute_by_shell()


def get_option_hook_script_inherit_keys(key):
    import lxbasic.objects as bsc_objects

    from lxsession import ssn_configure

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    yaml_file_path = ssn_configure.Hooks.get_yaml_file(key)
    if yaml_file_path:
        yaml_file = utl_dcc_objects.OsFile(yaml_file_path)
        if yaml_file.get_is_exists() is True:
            configure = bsc_objects.Configure(value=yaml_file.path)
            return configure.get('hook_option.script.inherit_keys') or []
    return []


def get_option_hook_args(option):
    def execute_fnc():
        session._set_file_execute_(python_file_path, dict(session=session))
    #
    from lxbasic import bsc_core
    #
    import lxbasic.objects as bsc_objects
    #
    from lxutil import utl_core
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    from lxsession import ssn_configure
    #
    import lxsession.objects as ssn_objects
    #
    option_opt = bsc_core.KeywordArgumentsOpt(option)
    #
    hook_key = option_opt.get('option_hook_key')
    #
    yaml_file_path = ssn_configure.OptionHooks.get_yaml_file(hook_key)
    if yaml_file_path:
        python_file_path = ssn_configure.OptionHooks.get_python_file(hook_key)
        python_file = utl_dcc_objects.OsPythonFile(python_file_path)
        yaml_file = utl_dcc_objects.OsFile(yaml_file_path)
        if python_file.get_is_exists() is True and yaml_file.get_is_exists() is True:
            configure = bsc_objects.Configure(value=yaml_file.path)
            type_name = configure.get('option.type')
            #
            session = None
            if type_name == 'method':
                session = ssn_objects.OptionMethodSession(
                    type=type_name,
                    hook=hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'rsv-task-method':
                session = ssn_objects.RsvOptionHookMethodSession(
                    type=type_name,
                    hook=hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'rsv-task-batcher':
                session = ssn_objects.RsvOptionHookMethodSession(
                    type=type_name,
                    hook=hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'kit-panel':
                session = ssn_objects.GuiSession(
                    type=type_name,
                    hook=hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            else:
                raise TypeError()
            #
            session.set_hook_python_file(python_file_path)
            session.set_hook_yaml_file(yaml_file_path)
            return session, execute_fnc
    else:
        utl_core.Log.set_module_error_trace(
            'option-hook gain',
            'key="{}" configue (.yml) is not found'.format(hook_key)
        )


def set_option_hook_execute(option):
    hook_args = get_option_hook_args(option)
    if hook_args is not None:
        session, execute_fnc = hook_args
        execute_fnc()


def set_option_hook_execute_by_shell(option):
    hook_args = get_option_hook_args(option)
    if hook_args is not None:
        session, execute_fnc = hook_args
        #
        session.set_execute_by_shell()


def set_option_hook_execute_by_deadline(option):
    hook_args = get_option_hook_args(option)
    if hook_args is not None:
        session, execute_fnc = hook_args
        #
        session.set_execute_by_deadline()


if __name__ == '__main__':
    pass