# coding:utf-8
from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxsession.objects import ssn_obj_abs

from lxgui.objects import gui_obj_abs

from lxsession import ssn_configure

import lxsession.objects as ssn_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil_gui.panel import utl_gui_pnl_abs_resolver


class ToolPanelSession(ssn_obj_abs.AbsToolPanelSession):
    def __init__(self, *args, **kwargs):
        super(ToolPanelSession, self).__init__(*args, **kwargs)


class RsvEntitiesPanel(utl_gui_pnl_abs_resolver.AbsEntitiesLoaderPanel):
    RSV_OBJ_ACTION_SESSION_CLASS = ssn_objects.RsvObjActionSession
    RSV_UNIT_ACTION_SESSION_CLASS = ssn_objects.RsvUnitActionSession
    def __init__(self, *args, **kwargs):
        self._configure = kwargs['configure']
        #
        self.WINDOW_NAME = self._configure.get('option.gui.name')
        self.WINDOW_SIZE = self._configure.get('option.gui.size')
        # filter
        application_filter = self._get_resolver_application_filter_()
        if application_filter:
            self.RESOLVER_FILTER = application_filter
        else:
            self.RESOLVER_FILTER = self._configure.get('resolver.filter')
        #
        self.ITEM_FRAME_SIZE = self._configure.get('option.gui.item_frame_size')
        #
        super(RsvEntitiesPanel, self).__init__()
        #
        self._session_dict = {}

    def _get_resolver_application_filter_(self):
        _ = self._configure.get('resolver.application_filter') or {}
        for k, v in _.items():
            if bsc_core.SystemMtd.get_is_matched(['*-{}'.format(k)]):
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
                    j_system_keys = j_raw.get('systems') or []
                    j_extend_variants = j_raw.get('extend_variants') or {}
                    if j_system_keys:
                        if bsc_core.SystemMtd.get_is_matched(j_system_keys):
                            j_rsv_unit = rsv_task.get_rsv_unit(
                                keyword=j_keyword
                            )
                            j_rsv_unit_file_path = j_rsv_unit.get_result(
                                version='latest',
                                extend_variants=j_extend_variants
                            )
                            if j_rsv_unit_file_path:
                                enable = True
                                #
                                lis.append(
                                    (True, j_rsv_unit, j_rsv_unit_file_path)
                                )
                    else:
                        j_rsv_unit = rsv_task.get_rsv_unit(
                            keyword=j_keyword
                        )
                        j_rsv_unit_file_path = j_rsv_unit.get_result(
                            version='latest',
                            extend_variants=j_extend_variants
                        )
                        if j_rsv_unit_file_path:
                            enable = True
                            #
                            lis.append(
                                (True, j_rsv_unit, j_rsv_unit_file_path)
                            )
        return enable, lis

    def get_rsv_assets_menu_content(self, rsv_entity):
        hook_keys = self._configure.get(
            'actions.assets.hooks'
        ) or []
        return self.__get_menu_content_by_hook_keys_(
            hook_keys, rsv_entity
        )

    def get_rsv_asset_menu_content(self, rsv_entity):
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
                if i_session.get_is_loadable() is True and i_session.get_is_visible() is True:
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
            session._set_file_execute_(python_file_path, dict(session=session))
        #
        rsv_task = args[0]
        session_path = '{}/{}'.format(rsv_task.path, key)
        if session_path in self._session_dict:
            return self._session_dict[session_path]
        else:
            python_file_path = ssn_configure.Hooks.get_python_file(key)
            yaml_file_path = ssn_configure.Hooks.get_yaml_file(key)
            if python_file_path and yaml_file_path:
                python_file = utl_dcc_objects.OsPythonFile(python_file_path)
                yaml_file = utl_dcc_objects.OsFile(yaml_file_path)
                if python_file.get_is_exists() is True and yaml_file.get_is_exists() is True:
                    configure = bsc_objects.Configure(value=yaml_file.path)
                    type_name = configure.get('option.type')
                    if type_name is not None:
                        kwargs['configure'] = configure
                        #
                        if type_name in ['asset', 'shot', 'step', 'task']:
                            session = self.RSV_OBJ_ACTION_SESSION_CLASS(
                                *args,
                                **kwargs
                            )
                        elif type_name in ['unit']:
                            session = self.RSV_UNIT_ACTION_SESSION_CLASS(
                                *args,
                                **kwargs
                            )
                        else:
                            raise TypeError()
                        #
                        self._session_dict[session_path] = session, execute_fnc
                        return session, execute_fnc


class RsvLoaderSession(gui_obj_abs.AbsRsvPanelSession):
    RSV_PANEL_CLASS = RsvEntitiesPanel
    def __init__(self, *args, **kwargs):
        super(RsvLoaderSession, self).__init__(*args, **kwargs)
