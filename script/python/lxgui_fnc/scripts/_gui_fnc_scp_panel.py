# coding:utf-8


def set_session_hook_run(key):
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
            # noinspection PyUnusedLocal
            session = gui_objects.RsvPanelSession(
                configure=configure
            )
            raw = python_file.set_read()
            session._set_code_execute_(raw)
