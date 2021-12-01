# coding:utf-8
from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxgui import gui_configure

from lxgui.objects import gui_obj_abs

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil_gui.panel import utl_gui_pnl_abs_resolver


class RsvEntityActionSession(gui_obj_abs.AbsRsvEntitySession):
    def __init__(self, *args, **kwargs):
        super(RsvEntityActionSession, self).__init__(*args, **kwargs)


class RsvTaskActionSession(gui_obj_abs.AbsRsvTaskSession):
    def __init__(self, *args, **kwargs):
        super(RsvTaskActionSession, self).__init__(*args, **kwargs)


class RsvUnitActionSession(gui_obj_abs.AbsRsvUnitActionSession):
    def __init__(self, *args, **kwargs):
        super(RsvUnitActionSession, self).__init__(*args, **kwargs)


class RsvEntitiesPanel(utl_gui_pnl_abs_resolver.AbsEntitiesLoaderPanel):
    RSV_ENTITY_ACTION_SESSION_CLASS = RsvEntityActionSession
    RSV_TASK_ACTION_SESSION_CLASS = RsvTaskActionSession
    RSV_UNIT_ACTION_SESSION_CLASS = RsvUnitActionSession
    def __init__(self, *args, **kwargs):
        self._configure = kwargs['configure']
        #
        self.WINDOW_NAME = self._configure.get('option.gui.name')
        self.WINDOW_SIZE = self._configure.get('option.gui.size')
        # filter
        exact_filter = self._get_resolver_exact_filter_()
        if exact_filter:
            self.RESOLVER_FILTER = exact_filter
        else:
            self.RESOLVER_FILTER = self._configure.get('resolver.filter')
        #
        self.ITEM_FRAME_ICON_SIZE = self._configure.get('option.gui.item_frame_icon_size')
        self.ITEM_FRAME_IMAGE_SIZE = self._configure.get('option.gui.item_frame_image_size')
        self.ITEM_FRAME_NAME_SIZE = self._configure.get('option.gui.item_frame_name_size')
        super(RsvEntitiesPanel, self).__init__()
        #
        self._session_dict = {}

    def _get_resolver_exact_filter_(self):
        _ = self._configure.get('resolver.exact_filter') or {}
        for k, v in _.items():
            if bsc_core.SystemMtd.get_is_matched([k]):
                return v

    def get_rsv_task_unit_show_raw(self, rsv_task):
        lis = []
        keywords = self._configure.get('resolver.task_unit.keywords') or []
        enable = False
        for i_raw in keywords:
            if isinstance(i_raw, (str, unicode)):
                i_keyword = i_raw
                i_keyword = i_keyword.format(**rsv_task.properties.value)
                #
                i_rsv_unit = rsv_task.get_rsv_unit(
                    keyword=i_keyword
                )
                i_rsv_unit_file_path = i_rsv_unit.get_result(version='latest')
                if i_rsv_unit_file_path:
                    enable = True
                    #
                    lis.append(
                        (True, i_rsv_unit, i_rsv_unit_file_path)
                    )
                # else:
                #     i_rsv_unit_pattern = i_rsv_unit.pattern
                #     lis.append(
                #         (False, i_rsv_unit, i_rsv_unit_pattern)
                #     )
            elif isinstance(i_raw, dict):
                for j_keyword, j_raw in i_raw.items():
                    j_keyword = j_keyword.format(**rsv_task.properties.value)
                    system_keys = j_raw.get('systems') or []
                    if bsc_core.SystemMtd.get_is_matched(system_keys):
                        j_rsv_unit = rsv_task.get_rsv_unit(
                            keyword=j_keyword
                        )
                        j_rsv_unit_file_path = j_rsv_unit.get_result(version='latest')
                        if j_rsv_unit_file_path:
                            enable = True
                            #
                            lis.append(
                                (True, j_rsv_unit, j_rsv_unit_file_path)
                            )
        return enable, lis

    def get_rsv_entity_menu_content(self, rsv_entity):
        hook_keys = self._configure.get(
            'actions.asset.hooks'
        ) or []
        return self.__get_menu_content_by_hook_keys_(
            hook_keys, rsv_entity
        )

    def get_rsv_task_menu_content(self, rsv_task):
        hook_keys = self._configure.get(
            'actions.task.hooks'
        ) or []
        return self.__get_menu_content_by_hook_keys_(
            hook_keys, rsv_task
        )

    def get_rsv_task_unit_menu_content(self, rsv_task):
        hook_keys = self._configure.get(
            'actions.task_unit.hooks'
        ) or []
        #
        return self.__get_menu_content_by_hook_keys_(
            hook_keys, rsv_task
        )

    def __get_menu_content_by_hook_keys_(self, keys, *args, **kwargs):
        content = bsc_objects.Dict()
        for i_key in keys:
            i_args = self.__get_rsv_unit_action_hook_args_(
                i_key, *args, **kwargs
            )
            if i_args:
                i_session, i_execute_fnc = i_args
                if i_session.get_is_loadable() is True:
                    i_group_name = i_session.gui_group_name
                    if i_group_name:
                        content.set(
                            '{}.properties.type'.format(i_group_name), 'separator'
                        )
                        content.set(
                            '{}.properties.name'.format(i_group_name), i_group_name
                        )
                    #
                    i_action_name = i_session.gui_name
                    #
                    content.set(
                        '{}.properties.type'.format(i_action_name), 'action'
                    )
                    content.set(
                        '{}.properties.name'.format(i_action_name), i_action_name
                    )
                    content.set(
                        '{}.properties.icon_name'.format(i_action_name), i_session.gui_icon_name
                    )
                    content.set(
                        '{}.properties.executable_fnc'.format(i_action_name), i_session.get_is_executable
                    )
                    content.set(
                        '{}.properties.execute_fnc'.format(i_action_name), i_execute_fnc
                    )
        return content

    def __get_rsv_unit_action_hook_args_(self, key, *args, **kwargs):
        def execute_fnc():
            session._set_code_execute_(raw)
        #
        rsv_task = args[0]
        session_path = '{}/{}'.format(rsv_task.path, key)
        if session_path in self._session_dict:
            return self._session_dict[session_path]
        else:
            python_file_path = gui_configure.Hooks.get_python_file(key)
            python_file = utl_dcc_objects.OsPythonFile(python_file_path)
            yaml_file_path = '{}.yml'.format(python_file.path_base)
            yaml_file = utl_dcc_objects.OsFile(yaml_file_path)
            if python_file.get_is_exists() is True and yaml_file.get_is_exists() is True:
                configure = bsc_objects.Configure(value=yaml_file.path)
                type_name = configure.get('option.type')
                if type_name is not None:
                    kwargs['configure'] = configure
                    #
                    if type_name in ['asset', 'shot']:
                        session = self.RSV_ENTITY_ACTION_SESSION_CLASS(
                            *args, **kwargs
                        )
                    elif type_name in ['task']:
                        session = self.RSV_TASK_ACTION_SESSION_CLASS(
                            *args, **kwargs
                        )
                    elif type_name in ['unit']:
                        session = self.RSV_UNIT_ACTION_SESSION_CLASS(
                            *args, **kwargs
                        )
                    else:
                        raise TypeError()
                    #
                    raw = python_file.set_read()
                    self._session_dict[session_path] = session, execute_fnc
                    return session, execute_fnc


class RsvPanelSession(gui_obj_abs.AbsRsvPanelSession):
    RSV_PANEL_CLASS = RsvEntitiesPanel
    def __init__(self, *args, **kwargs):
        super(RsvPanelSession, self).__init__(*args, **kwargs)
