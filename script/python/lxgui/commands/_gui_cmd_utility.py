# coding:utf-8


def get_hook_args(key):
    def execute_fnc():
        session._set_file_execute_(python_file_path, dict(session=session))
    #
    import lxbasic.objects as bsc_objects
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    from lxgui import gui_configure
    #
    import lxgui.objects as gui_objects
    #
    python_file_path = gui_configure.Hooks.get_python_file(key)
    yaml_file_path = gui_configure.Hooks.get_yaml_file(key)
    if python_file_path and yaml_file_path:
        python_file = utl_dcc_objects.OsPythonFile(python_file_path)
        yaml_file = utl_dcc_objects.OsFile(yaml_file_path)
        if python_file.get_is_exists() is True and yaml_file.get_is_exists() is True:
            configure = bsc_objects.Configure(value=yaml_file.path)
            type_name = configure.get('option.type')
            session = None
            if type_name == 'tool-panel':
                session = gui_objects.ToolPanelSession(
                    configure=configure
                )
            elif type_name == 'kit-panel':
                session = gui_objects.RsvLoaderSession(
                    configure=configure
                )
            elif type_name == 'rsv-loader':
                session = gui_objects.RsvLoaderSession(
                    configure=configure
                )
            #
            if session is not None:
                session.set_hook_python_file(python_file_path)
                session.set_hook_yaml_file(yaml_file_path)
                return session, execute_fnc


def set_hook_run(key):
    hook_args = get_hook_args(key)
    if hook_args is not None:
        session, execute_fnc = hook_args
        execute_fnc()
