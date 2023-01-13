# coding:utf-8


def get_menu_content_by_hooks(hooks):
    from lxbasic import bsc_core

    import lxbasic.objects as bsc_objects

    from lxsession.commands import _ssn_cmd_hook

    content = bsc_objects.Dict()
    for i_hook in hooks:
        if isinstance(i_hook, (str, unicode)):
            i_hook_key = i_hook
            i_extra_kwargs = None
        elif isinstance(i_hook, dict):
            i_hook_key = i_hook.keys()[0]
            i_extra_kwargs = i_hook.values()[0]
        else:
            raise RuntimeError()
        #
        i_hook_args = _ssn_cmd_hook.get_hook_args(i_hook_key)
        if i_hook_args:
            i_session, i_execute_fnc = i_hook_args
            if i_session.get_is_loadable() is True:
                i_gui_configure = i_session.gui_configure
                #
                i_gui_parent_path = '/'
                #
                i_gui_name = i_gui_configure.get('name')
                if i_extra_kwargs:
                    if 'gui_parent' in i_extra_kwargs:
                        i_gui_parent_path = i_extra_kwargs['gui_parent']
                #
                i_gui_parent_path_opt = bsc_core.DccPathDagOpt(i_gui_parent_path)
                #
                if i_gui_parent_path_opt.get_is_root():
                    i_gui_path = '/{}'.format(i_gui_name)
                else:
                    i_gui_path = '{}/{}'.format(i_gui_parent_path, i_gui_name)
                #
                i_gui_separator_name = i_gui_configure.get('group_name')
                if i_gui_separator_name:
                    if i_gui_parent_path_opt.get_is_root():
                        i_gui_separator_path = '/{}'.format(i_gui_separator_name)
                    else:
                        i_gui_separator_path = '{}/{}'.format(i_gui_parent_path, i_gui_separator_name)
                    #
                    content.set(
                        '{}.properties.type'.format(i_gui_separator_path), 'separator'
                    )
                    content.set(
                        '{}.properties.name'.format(i_gui_separator_path), i_gui_configure.get('group_name')
                    )
                #
                content.set(
                    '{}.properties.type'.format(i_gui_path), 'action'
                )
                content.set(
                    '{}.properties.group_name'.format(i_gui_path), i_gui_configure.get('group_name')
                )
                content.set(
                    '{}.properties.name'.format(i_gui_path), i_gui_configure.get('name')
                )
                content.set(
                    '{}.properties.icon_name'.format(i_gui_path), i_gui_configure.get('icon_name')
                )
                if i_extra_kwargs:
                    if 'gui_icon_name' in i_extra_kwargs:
                        content.set(
                            '{}.properties.icon_name'.format(i_gui_path), i_extra_kwargs.get('gui_icon_name')
                        )
                #
                content.set(
                    '{}.properties.executable_fnc'.format(i_gui_path), i_session.get_is_executable
                )
                content.set(
                    '{}.properties.execute_fnc'.format(i_gui_path), i_execute_fnc
                )
    return content


def get_menu_content_by_hook_options(hook_options):
    from lxbasic import bsc_core

    from lxsession.commands import _ssn_cmd_hook

    import lxbasic.objects as bsc_objects

    content = bsc_objects.Dict()
    for i_hook_option in hook_options:
        i_hook_args = _ssn_cmd_hook.get_option_hook_args(i_hook_option)
        if i_hook_args:
            i_session, i_execute_fnc = i_hook_args
            if i_session.get_is_loadable() is True:
                i_hook_option_opt = i_session.option_opt
                i_gui_configure = i_session.gui_configure
                i_gui_parent_path = '/'
                #
                i_gui_name = i_gui_configure.get('name')
                if i_hook_option_opt.get_key_is_exists('gui_name'):
                    i_gui_name = i_hook_option_opt.get('gui_name')
                #
                i_gui_group_name = i_gui_configure.get('group_name')
                if i_hook_option_opt.get_key_is_exists('gui_group_name'):
                    i_gui_group_name = i_hook_option_opt.get('gui_group_name')
                #
                if i_hook_option_opt.get_value():
                    if i_hook_option_opt.get_key_is_exists('gui_parent'):
                        i_gui_parent_path = i_hook_option_opt.get('gui_parent')
                #
                i_gui_parent_path_opt = bsc_core.DccPathDagOpt(i_gui_parent_path)
                #
                if i_gui_parent_path_opt.get_is_root():
                    i_gui_path = '/{}'.format(i_gui_name)
                else:
                    i_gui_path = '{}/{}'.format(i_gui_parent_path, i_gui_name)
                #
                if i_gui_group_name:
                    if i_gui_parent_path_opt.get_is_root():
                        i_gui_separator_path = '/{}'.format(i_gui_group_name)
                    else:
                        i_gui_separator_path = '{}/{}'.format(i_gui_parent_path, i_gui_group_name)
                    #
                    content.set(
                        '{}.properties.type'.format(i_gui_separator_path), 'separator'
                    )
                    content.set(
                        '{}.properties.name'.format(i_gui_separator_path), i_gui_configure.get('group_name')
                    )
                #
                content.set(
                    '{}.properties.type'.format(i_gui_path), 'action'
                )
                content.set(
                    '{}.properties.group_name'.format(i_gui_path), i_gui_group_name
                )
                content.set(
                    '{}.properties.name'.format(i_gui_path), i_gui_name
                )
                content.set(
                    '{}.properties.icon_name'.format(i_gui_path), i_gui_configure.get('icon_name')
                )
                if i_hook_option_opt.get_value():
                    if i_hook_option_opt.get_key_is_exists('gui_icon_name'):
                        content.set(
                            '{}.properties.icon_name'.format(i_gui_path), i_hook_option_opt.get('gui_icon_name')
                        )
                #
                content.set(
                    '{}.properties.executable_fnc'.format(i_gui_path), i_session.get_is_executable
                )
                content.set(
                    '{}.properties.execute_fnc'.format(i_gui_path), i_execute_fnc
                )
    return content


def get_menu_content_by_hook_options_(hook_options):
    from lxbasic import bsc_core

    from lxsession.commands import _ssn_cmd_hook

    import lxbasic.objects as bsc_objects

    content = bsc_objects.Dict()
    for i_key in hook_options:
        if isinstance(i_key, (str, unicode)):
            i_hook_option = i_key
            i_extra_kwargs = None
        elif isinstance(i_key, dict):
            i_hook_option = i_key.keys()[0]
            i_extra_kwargs = i_key.values()[0]
        else:
            raise RuntimeError()
        #
        i_hook_args = _ssn_cmd_hook.get_option_hook_args(i_hook_option)
        if i_hook_args:
            i_session, i_execute_fnc = i_hook_args
            if i_session.get_is_loadable() is True:
                i_hook_option_opt = i_session.option_opt
                i_hook_option_opt.set_update(i_extra_kwargs)
                i_gui_configure = i_session.gui_configure
                i_gui_parent_path = '/'
                #
                i_gui_name = i_gui_configure.get('name')
                if i_hook_option_opt.get_key_is_exists('gui_name'):
                    i_gui_name = i_hook_option_opt.get('gui_name')
                #
                i_gui_group_name = i_gui_configure.get('group_name')
                if i_hook_option_opt.get_key_is_exists('gui_group_name'):
                    i_gui_group_name = i_hook_option_opt.get('gui_group_name')
                #
                if i_hook_option_opt.get_value():
                    if i_hook_option_opt.get_key_is_exists('gui_parent'):
                        i_gui_parent_path = i_hook_option_opt.get('gui_parent')
                #
                i_gui_parent_path_opt = bsc_core.DccPathDagOpt(i_gui_parent_path)
                #
                if i_gui_parent_path_opt.get_is_root():
                    i_gui_path = '/{}'.format(i_gui_name)
                else:
                    i_gui_path = '{}/{}'.format(i_gui_parent_path, i_gui_name)
                #
                if i_gui_group_name:
                    if i_gui_parent_path_opt.get_is_root():
                        i_gui_separator_path = '/{}'.format(i_gui_group_name)
                    else:
                        i_gui_separator_path = '{}/{}'.format(i_gui_parent_path, i_gui_group_name)
                    #
                    content.set(
                        '{}.properties.type'.format(i_gui_separator_path), 'separator'
                    )
                    content.set(
                        '{}.properties.name'.format(i_gui_separator_path), i_gui_configure.get('group_name')
                    )
                #
                content.set(
                    '{}.properties.type'.format(i_gui_path), 'action'
                )
                content.set(
                    '{}.properties.group_name'.format(i_gui_path), i_gui_group_name
                )
                content.set(
                    '{}.properties.name'.format(i_gui_path), i_gui_name
                )
                content.set(
                    '{}.properties.icon_name'.format(i_gui_path), i_gui_configure.get('icon_name')
                )
                if i_hook_option_opt.get_value():
                    if i_hook_option_opt.get_key_is_exists('gui_icon_name'):
                        content.set(
                            '{}.properties.icon_name'.format(i_gui_path), i_hook_option_opt.get('gui_icon_name')
                        )
                #
                content.set(
                    '{}.properties.executable_fnc'.format(i_gui_path), i_session.get_is_executable
                )
                content.set(
                    '{}.properties.execute_fnc'.format(i_gui_path), i_execute_fnc
                )
    return content


if __name__ == '__main__':
    c = get_menu_content_by_hook_options_(
        [
            {
                'option_hook_key=dtb-panels/asset-look-library&category=texture': {'gui_parent': '/Asset', 'gui_icon_name': 'window/loader'}
            }
        ]
    )

    print c.get_value()

