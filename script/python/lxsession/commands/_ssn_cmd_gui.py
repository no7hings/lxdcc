# coding:utf-8


def get_menu_content_by_hook_options(hook_options, content=None):
    from lxsession.commands import _ssn_cmd_hook

    import lxbasic.objects as bsc_objects

    content = bsc_objects.Dict()
    for i_hook_option in hook_options:
        i_args = _ssn_cmd_hook.get_option_hook_args(i_hook_option)
        if i_args:
            i_session, i_execute_fnc = i_args
            if i_session.get_is_loadable() is True:
                i_hook_option_opt = i_session.option_opt
                i_gui_group_name = i_session.gui_group_name
                if i_gui_group_name:
                    i_gui_group_name_override = i_hook_option_opt.get(
                        'gui_group_name'
                    )
                    if i_gui_group_name_override:
                        i_gui_group_name = i_gui_group_name_override
                    #
                    content.set(
                        '{}.properties.type'.format(i_gui_group_name), 'separator'
                    )
                    content.set(
                        '{}.properties.name'.format(i_gui_group_name), i_gui_group_name
                    )
                #
                i_gui_name = i_session.gui_name
                i_gui_name_override = i_hook_option_opt.get('gui_name')
                if i_gui_name_override:
                    i_gui_name = i_gui_name_override
                #
                content.set(
                    '{}.properties.type'.format(i_gui_name), 'action'
                )
                content.set(
                    '{}.properties.name'.format(i_gui_name), i_gui_name
                )
                content.set(
                    '{}.properties.icon_name'.format(i_gui_name), i_session.gui_icon_name
                )
                content.set(
                    '{}.properties.executable_fnc'.format(i_gui_name), i_session.get_is_executable
                )
                content.set(
                    '{}.properties.execute_fnc'.format(i_gui_name), i_execute_fnc
                )
    return content
