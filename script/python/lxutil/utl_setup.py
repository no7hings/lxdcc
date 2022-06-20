# coding:utf-8
import os

import lxbasic.objects as bsc_objects

from lxutil import utl_configure

from lxutil import utl_abstract


class HoudiniXml(object):
    XML_HEAD = 'subMenu'
    INDENT_COUNT = 4
    def __init__(self):
        self._indent = 0

    def get_head(self):
        return self.XML_HEAD

    def get_indent_count(self):
        return self._indent

    def set_indent_count(self, count):
        self._indent = count

    def get_xml_attributes(self):
        raise NotImplementedError()

    def get_xml_elements(self):
        raise NotImplementedError()

    def get_xml(self):
        lis = [
            (self.get_indent_count(), '<{}'.format(self.get_head()), '')
        ]
        ports = self.get_xml_attributes()
        elements = self.get_xml_elements()
        if ports:
            for i in ports:
                k, v = i
                lis.append(
                    (0, ' {}="{}"'.format(k, v), '')
                )
            if elements:
                lis.append(
                    (0, '>', os.linesep)
                )
        if elements:
            for i in elements:
                if isinstance(i, HoudiniXml):
                    lis.extend(i.get_xml())
                else:
                    k, v = i
                    lis.append(
                        (self.get_indent_count() + 1, '<{}>{}</{}>'.format(k, v, k), os.linesep)
                    )
            lis.append(
                (self.get_indent_count(), '</{}>'.format(self.get_head()), os.linesep)
            )
        else:
            lis.append(
                (0, ' />'.format(self.get_head()), os.linesep)
            )
        return lis


class HoudiniXmlAction(HoudiniXml):
    XML_HEAD = 'scriptItem', 'separatorItem'
    def __init__(self, key=None):
        super(HoudiniXmlAction, self).__init__()
        self._key = key
        self._name = None
        self._is_separator = False
        self._python_command = None

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, text):
        self._name = text
    @property
    def python_command(self):
        return self._python_command
    @python_command.setter
    def python_command(self, text):
        self._python_command = text

    def get_head(self):
        if self._is_separator is True:
            return self.XML_HEAD[1]
        return self.XML_HEAD[0]

    def set_is_separator(self, boolean):
        self._is_separator = boolean

    def get_is_separator(self):
        return self._is_separator

    def get_xml_attributes(self):
        if self.get_is_separator() is True:
            return []
        return [
            ('id', self._key)
        ]

    def get_xml_elements(self):
        if self.get_is_separator() is True:
            return []
        lis = [
            ('label', self.name)
        ]
        if self.python_command is not None:
            lis.append(
                ('scriptCode', '<![CDATA[{}]]>'.format(self._python_command))
            )
        return lis


class HoudiniXmlMenu(HoudiniXml):
    ACTION_CLASS = HoudiniXmlAction
    XML_HEAD = 'subMenu'
    def __init__(self, key, sub=False):
        super(HoudiniXmlMenu, self).__init__()
        self._key = key
        self._name = None
        self._sub = sub
        self._children = []
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, text):
        self._name = text

    def set_action_add(self, key):
        action = self.ACTION_CLASS(key)
        self._children.append(action)
        return action

    def set_menu_add(self, key):
        menu = self.__class__(key, True)
        self._children.append(menu)
        return menu

    def get_actions(self):
        return self._children

    def set_separator_add(self):
        action = self.ACTION_CLASS()
        action.set_is_separator(True)
        self._children.append(action)
        return action

    def get_xml_attributes(self):
        return [
            ('id', self._key)
        ]

    def get_xml_elements(self):
        if self._sub is True:
            lis = [
                ('label', self.name)
            ]
        else:
            lis = [
                ('label', self.name),
                ('insertBefore', 'help_menu')
            ]
        for i in self.get_actions():
            i.set_indent_count(self.get_indent_count() + 1)
            lis.append(i)
        return lis


class HoudiniXmlMainMenuBar(HoudiniXml):
    MENU_CLASS = HoudiniXmlMenu
    XML_HEAD = 'menuBar'
    def __init__(self):
        super(HoudiniXmlMainMenuBar, self).__init__()
        self._menus = []

    @property
    def menus(self):
        return self._menus

    def set_menu_add(self, name):
        menu = self.MENU_CLASS(name)
        self._menus.append(menu)
        return menu

    def get_menus(self):
        return self._menus

    def get_xml_attributes(self):
        return []

    def get_xml_elements(self):
        lis = []
        return lis

    def set_convert_to_xml(self):
        lis = [
            (0, '<?xml version="1.0" encoding="UTF-8"?>', os.linesep),
            (0, '<mainMenu>', os.linesep),
            (1, '<menuBar>', os.linesep)
        ]
        for i in self.get_menus():
            i.set_indent_count(2)
            lis.extend(i.get_xml())
        lis.extend(
            [
                (1, '</menuBar>', os.linesep),
                (0, '</mainMenu>', '')
            ]
        )
        return ''.join(['{}{}{}'.format(c*' '*self.INDENT_COUNT, i, l) for c, i, l in lis])

    def __str__(self):
        return self.set_convert_to_xml()


class HoudiniSetupCreator(object):
    def __init__(self, file_path):
        self._file_path = file_path

    def set_main_menu_xml_create(self):
        def set_menu_add_fnc_(tool_config_, seq):
            _menu = self._menu_bar.set_menu_add('tool_menu_{}'.format(seq))
            _menu.name = tool_config_.get('menu.name')
            _tools = tool_config_.get('menu.tools')
            for _i_key in _tools:
                if _i_key == 'separator':
                    _menu.set_separator_add()
                else:
                    _i_name = tool_config_.get('tool.{}.name'.format(_i_key))
                    _i_children = tool_config_.get('tool.{}.items'.format(_i_key))
                    if _i_children:
                        _i_menu = _menu.set_menu_add(_i_key)
                        _i_menu.name = _i_name
                        for _j_key in _i_children:
                            if _j_key == 'separator':
                                _i_menu.set_separator_add()
                            else:
                                _j_name = tool_config_.get('tool.{}.name'.format(_j_key))
                                _j_command = tool_config_.get('tool.{}.command'.format(_j_key))
                                #
                                _j_action = _i_menu.set_action_add(_j_key)
                                _j_action.name = _j_name
                                _j_action.python_command = _j_command
                    else:
                        _i_command = tool_config_.get('tool.{}.command'.format(_i_key))
                        #
                        _i_action = _menu.set_action_add(_i_key)
                        _i_action.name = _i_name
                        _i_action.python_command = _i_command
        #
        self._menu_bar = HoudiniXmlMainMenuBar()
        #
        configure_file_path = utl_configure.MainData.get_configure_file('houdini/menu/main')
        configure = bsc_objects.Configure(value=configure_file_path)
        set_menu_add_fnc_(configure, 0)
        #
        main_menu_xml_file = '{}/MainMenuCommon.xml'.format(self._file_path)
        self.set_file_write(main_menu_xml_file, self._menu_bar.__str__())
        return main_menu_xml_file

    @classmethod
    def set_file_write(cls, file_path, raw):
        with open(file_path, 'w') as f:
            f.write(raw)


class OcioSetup(utl_abstract.AbsSetup):
    def __init__(self, root):
        super(OcioSetup, self).__init__(root)

    def set_run(self):
        self._set_environ_(
            'OCIO', '{}/config.ocio'.format(self._root)
        )
