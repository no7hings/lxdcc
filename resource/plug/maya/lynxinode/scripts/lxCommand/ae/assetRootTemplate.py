# encoding=utf-8
from contextlib import contextmanager
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel
#
from lxCommand.template import nodeTemplate


class ControlBase(object):
    @classmethod
    def get_gui_key(cls, atr_path):
        _ = atr_path.split('.')
        node, port_path = _
        node_type = cmds.nodeType(node)
        return 'GUI_{}__{}'.format(node_type, port_path)
    @classmethod
    def get_gui_replace_args(cls, atr_path):
        _ = atr_path.split('.')
        node, keys = _
        node_type = cmds.nodeType(node)
        list_ = []
        for i_index, i_key in enumerate(keys.split('&')):
            list_.append(
                (i_key, 'GUI_{}__{}'.format(node_type, i_key))
            )
        return node, list_
    @classmethod
    def get_gui_new_args(cls, atr_path, labels, icons):
        _ = atr_path.split('.')
        node, keys = _
        node_type = cmds.nodeType(node)
        list_ = []
        for i_index, i_key in enumerate(keys.split('&')):
            i_label = labels.split('&')[i_index]
            i_icon = icons.split('&')[i_index]
            list_.append(
                (i_key, 'GUI_{}__{}'.format(node_type, i_key), i_label, i_icon)
            )
        return node, list_
    @classmethod
    def gui_new_fnc(cls, *args, **kwargs):
        raise NotImplementedError()
    @classmethod
    def gui_replace_fnc(cls, *args, **kwargs):
        raise NotImplementedError()


class FileControl(ControlBase):
    @classmethod
    def gui_update_value(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        value = cmds.getAttr(atr_path) or ''
        cmds.textFieldGrp(
            gui_key,
            edit=True,
            text=value,
            annotation='attribute="{}"'.format(atr_path)
        )
    @classmethod
    def gui_update_edit_callback(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        cmds.textFieldGrp(
            gui_key,
            edit=1,
            changeCommand=lambda x: cls.dcc_update_value(atr_path),
        )
        cmds.symbolButton(
            gui_key+'__button',
            edit=1,
            command=lambda x: cls.dcc_update_value_by_button(atr_path)
        )
    #
    @classmethod
    def dcc_update_value(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        value = cmds.getAttr(atr_path) or ''
        value_new = cmds.textFieldGrp(
            gui_key,
            query=1,
            text=1
        ) or ''
        if value_new != value:
            cmds.setAttr(atr_path, value_new, type="string")
    @classmethod
    def dcc_update_value_by_button(cls, atr_path):
        import os

        gui_key = cls.get_gui_key(atr_path)
        value = cmds.getAttr(atr_path) or ''
        #
        results = cmds.fileDialog2(
            fileFilter='All Files (*.*)',
            cap='Load File',
            okc='Load',
            fm=4,
            dir=os.path.dirname(value)
        ) or []
        if results:
            value_new = results[0]
            if value_new != value:
                cmds.setAttr(atr_path, value_new, type="string")
                cmds.textFieldGrp(
                    gui_key,
                    edit=1,
                    text=value_new
                )
    @classmethod
    def dcc_update_attribute_change_callback(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        cmds.scriptJob(
            parent=gui_key,
            replacePrevious=True,
            attributeChange=[
                atr_path,
                lambda: cls.gui_update_value(atr_path)
            ]
        )
    #
    @classmethod
    def gui_new_fnc(cls, atr_path, label):
        gui_key = cls.get_gui_key(atr_path)
        #
        cmds.rowLayout(
            nc=2,
            cw2=(360, 30),
            cl2=('left', 'left'),
            adjustableColumn=1,
            columnAttach=[(1, 'left', -2), (2, 'left', 0)]
        )
        cmds.textFieldGrp(
            gui_key,
            label=label
        )
        cmds.symbolButton(
            gui_key+'__button',
            image='folder-closed.png'
        )
        cls.gui_update_edit_callback(atr_path)
        cls.gui_update_value(atr_path)
        cls.dcc_update_attribute_change_callback(atr_path)
    @classmethod
    def gui_replace_fnc(cls, atr_path):
        cls.gui_update_edit_callback(atr_path)
        cls.gui_update_value(atr_path)
        cls.dcc_update_attribute_change_callback(atr_path)


class EnumerateControl(ControlBase):
    @classmethod
    def get_dcc_values(cls, enumerate_option):
        return enumerate_option.split('|')
    @classmethod
    def get_gui_values(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        return [cmds.menuItem(i, query=1, label=1) for i in cmds.optionMenuGrp(gui_key, query=1, itemListLong=1) or []]
    @classmethod
    def gui_build_and_update_value(cls, atr_path, enumerate_option):
        gui_key = cls.get_gui_key(atr_path)
        #
        gui_values = cls.get_gui_values(atr_path)
        values = cls.get_dcc_values(enumerate_option)
        if values != gui_values:
            [cmds.deleteUI(i) for i in cmds.optionMenuGrp(gui_key, query=1, itemListLong=1) or []]
            for i_index, i_version in enumerate(values):
                cmds.menuItem(
                    label=i_version, data=i_index,
                    parent=gui_key+'|OptionMenu'
                )
        #
        cls.gui_update_value(atr_path)
    @classmethod
    def gui_update_value(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        #
        values = cls.get_gui_values(atr_path)
        value_current = cmds.getAttr(atr_path)
        if value_current in values:
            index = values.index(value_current)
            cmds.optionMenuGrp(
                gui_key,
                edit=1,
                select=index+1,
                annotation='attribute="{}"'.format(atr_path)
            )
        else:
            cmds.optionMenuGrp(
                gui_key,
                edit=1,
                select=1,
                annotation='attribute="{}"'.format(atr_path)
            )
    @classmethod
    def gui_update_edit_callback(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        cmds.optionMenuGrp(
            gui_key,
            edit=1,
            changeCommand=lambda x: cls.dcc_update_value(atr_path)
        )
    #
    @classmethod
    def dcc_update_value(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        items = cmds.optionMenuGrp(gui_key, query=1, itemListLong=1)
        index = cmds.optionMenuGrp(gui_key, query=1, select=1)
        value_current = cmds.getAttr(atr_path)
        value_current_new = cmds.menuItem(items[index-1], query=1, label=1)
        if value_current_new != value_current:
            cmds.setAttr(
                atr_path, value_current_new, type='string'
            )
    @classmethod
    def dcc_update_attribute_change_callback(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        #
        cmds.scriptJob(
            parent=gui_key,
            replacePrevious=True,
            attributeChange=[
                atr_path,
                lambda: cls.gui_update_value(atr_path)
            ]
        )
    #
    @classmethod
    def gui_new_fnc(cls, atr_path, label, enumerate_option):
        gui_key = cls.get_gui_key(atr_path)
        cmds.optionMenuGrp(
            gui_key,
            label=label
        )
        cls.gui_build_and_update_value(atr_path, enumerate_option)
        cls.gui_update_edit_callback()
        cls.dcc_update_attribute_change_callback(atr_path)
    @classmethod
    def gui_replace_fnc(cls, atr_path, enumerate_option):
        cls.gui_build_and_update_value(atr_path, enumerate_option)
        cls.gui_update_edit_callback()
        cls.dcc_update_attribute_change_callback(atr_path)


class IconButtonControls(ControlBase):
    @classmethod
    def execute_fnc(cls, *args, **kwargs):
        print args, kwargs
    @classmethod
    def gui_new_fnc(cls, atr_path, labels, icons, data_port_path):
        node_, gui_args = cls.get_gui_new_args(atr_path, labels, icons)
        cmds.columnLayout(
            adjustableColumn=2,
            rowSpacing=4,
            # backgroundColor=(.15, .15, .15)
        )
        cmds.rowLayout(
            numberOfColumns=4,
            adjustableColumn=1,
            columnWidth4=[120] * 4,
            columnAttach4=['both'] * 4,
            columnAlign4=['center'] * 4,
            columnOffset4=[2] * 4
        )
        cmds.text(label='')
        for i_key, i_gui_key, i_label, i_icon in gui_args:
            cmds.nodeIconButton(
                i_gui_key,
                style='iconAndTextHorizontal',
                image1=i_icon,
                label=i_label,
                command=lambda key=i_key, node=node_: cls.execute_fnc(key=key, node=node)
            )
    @classmethod
    def gui_replace_fnc(cls, atr_path, data_port_path):
        node_, gui_args = cls.get_gui_replace_args(atr_path)
        for i_key, i_gui_key in gui_args:
            cmds.nodeIconButton(
                i_gui_key,
                edit=1,
                command=lambda key=i_key, node=node_: cls.execute_fnc(key=key, node=node)
            )


class TextControl(ControlBase):
    @classmethod
    def gui_update_value(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        value = cmds.getAttr(atr_path) or ''
        cmds.textFieldGrp(
            gui_key,
            edit=True,
            text=value,
            annotation='attribute="{}"'.format(atr_path)
        )
    @classmethod
    def gui_update_edit_callback(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        cmds.textFieldGrp(
            gui_key,
            edit=1,
            changeCommand=lambda x: cls.dcc_update_value(atr_path)
        )
    #
    @classmethod
    def dcc_update_value(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        value = cmds.getAttr(atr_path) or ''
        value_new = cmds.textFieldGrp(
            gui_key,
            query=1,
            text=1
        ) or ''
        if value_new != value:
            cmds.setAttr(atr_path, value_new, type="string")
    @classmethod
    def dcc_update_attribute_change_callback(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        cmds.scriptJob(
            parent=gui_key,
            replacePrevious=True,
            attributeChange=[
                atr_path,
                lambda: cls.gui_update_value(atr_path)
            ]
        )
    #
    @classmethod
    def gui_new_fnc(cls, atr_path, label, lock=False):
        gui_key = cls.get_gui_key(atr_path)
        #
        cmds.textFieldGrp(
            gui_key,
            label=label,
            editable=not lock,
        )
        cls.gui_update_edit_callback(atr_path)
        cls.gui_update_value(atr_path)
        cls.dcc_update_attribute_change_callback(atr_path)
    @classmethod
    def gui_replace_fnc(cls, atr_path):
        cls.gui_update_edit_callback(atr_path)
        cls.gui_update_value(atr_path)
        cls.dcc_update_attribute_change_callback(atr_path)


class DataControls(ControlBase):
    @classmethod
    def get_dcc_value_data(cls, atr_path):
        raw = cmds.getAttr(
            atr_path
        )
        try:
            _ = eval(raw)
            if isinstance(_, dict):
                return _
        except SyntaxError as e:
            pass
        return {}
    @classmethod
    def get_gui_key_data(cls, atr_path, build_port_path, build_key):
        _ = atr_path.split('.')
        node, port_path = _
        data_atr_path = '{}.{}'.format(node, build_port_path)
        raw = cmds.getAttr(
            data_atr_path
        )
        try:
            _ = eval(raw)
            if isinstance(_, dict):
                if port_path in _:
                    data = _[port_path]
                    return data.get(build_key) or []
        except SyntaxError as e:
            pass
        return []
    #
    @classmethod
    def gui_update_value(cls, atr_path, key_data):
        data = cls.get_dcc_value_data(atr_path)
        gui_key = cls.get_gui_key(atr_path)
        for i_key, i_label in key_data:
            i_gui_key = gui_key + '__' + i_key
            if i_key in data:
                i_value = data[i_key]
            else:
                i_value = ''
            #
            cmds.textFieldGrp(
                i_gui_key,
                edit=1,
                text=i_value,
                annotation='attribute="{}"\nkey="{}"'.format(atr_path, i_key)
            )
    @classmethod
    def dcc_update_attribute_change_callback(cls, atr_path, key_data):
        gui_key = cls.get_gui_key(atr_path)
        cmds.scriptJob(
            parent=gui_key,
            replacePrevious=True,
            attributeChange=[
                atr_path,
                lambda: cls.gui_update_value(atr_path, key_data)
            ]
        )
    #
    @classmethod
    def gui_new_fnc(cls, atr_path, build_port_path, build_key):
        key_data = cls.get_gui_key_data(atr_path, build_port_path, build_key)
        gui_key = cls.get_gui_key(atr_path)
        cmds.columnLayout(
            gui_key,
            adjustableColumn=1,
            # backgroundColor=(.275, .275, .275)
        )
        for i_key, i_label in key_data:
            i_gui_key = gui_key+'__'+i_key
            cmds.textFieldGrp(
                i_gui_key,
                label=i_label,
                editable=False
            )
        cls.gui_update_value(atr_path, key_data)
        cls.dcc_update_attribute_change_callback(atr_path, key_data)
    @classmethod
    def gui_replace_fnc(cls, atr_path, build_port_path, build_key):
        key_data = cls.get_gui_key_data(atr_path, build_port_path, build_key)
        #
        cls.gui_update_value(atr_path, key_data)
        cls.dcc_update_attribute_change_callback(atr_path, key_data)


class VariantControl(ControlBase):
    @classmethod
    def get_dcc_values(cls, atr_path, data_port_path):
        _ = atr_path.split('.')
        node, port_path = _
        data_atr_path = '{}.{}'.format(node, data_port_path)
        raw = cmds.getAttr(
            data_atr_path
        )
        try:
            _ = eval(raw)
            if isinstance(_, dict):
                if port_path in _:
                    data = _[port_path]
                    return data['all'], data['default']
        except SyntaxError as e:
            pass
        return ['None'], 'None'
    @classmethod
    def get_gui_values(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        return [cmds.menuItem(i, query=1, label=1) for i in cmds.optionMenuGrp(gui_key, query=1, itemListLong=1) or []]
    #
    @classmethod
    def gui_build_and_update_value(cls, atr_path, data_port_path):
        gui_key = cls.get_gui_key(atr_path)
        #
        gui_values = cls.get_gui_values(atr_path)
        values, value_default = cls.get_dcc_values(atr_path, data_port_path)
        if values != gui_values:
            [cmds.deleteUI(i) for i in cmds.optionMenuGrp(gui_key, query=1, itemListLong=1) or []]
            for i_index, i_version in enumerate(values):
                cmds.menuItem(
                    label=i_version, data=i_index,
                    parent=gui_key+'|OptionMenu'
                )
        #
        cls.gui_update_value(atr_path, data_port_path)
    @classmethod
    def gui_update_value(cls, atr_path, data_port_path):
        gui_key = cls.get_gui_key(atr_path)
        #
        values = cls.get_gui_values(atr_path)
        value_current = cmds.getAttr(atr_path)
        if value_current in values:
            index = values.index(value_current)
            cmds.optionMenuGrp(
                gui_key,
                edit=1,
                select=index+1,
                annotation='attribute="{}"'.format(atr_path)
            )
        else:
            cmds.optionMenuGrp(
                gui_key,
                edit=1,
                select=1,
                annotation='attribute="{}"'.format(atr_path)
            )
        #
        cls.gui_check_value(atr_path, data_port_path)
    @classmethod
    def gui_update_edit_callback(cls, atr_path, data_port_path):
        gui_key = cls.get_gui_key(atr_path)
        cmds.optionMenuGrp(
            gui_key,
            edit=1,
            changeCommand=lambda x: cls.dcc_update_value(atr_path, data_port_path)
        )
    #
    @classmethod
    def dcc_update_value(cls, atr_path, data_port_path):
        gui_key = cls.get_gui_key(atr_path)
        items = cmds.optionMenuGrp(gui_key, query=1, itemListLong=1)
        index = cmds.optionMenuGrp(gui_key, query=1, select=1)
        value_current = cmds.getAttr(atr_path)
        value_current_new = cmds.menuItem(items[index-1], query=1, label=1)
        if value_current_new != value_current:
            cmds.setAttr(
                atr_path, value_current_new, type='string'
            )
        cls.gui_check_value(atr_path, data_port_path)
    @classmethod
    def dcc_update_attribute_change_callback(cls, atr_path, data_port_path):
        gui_key = cls.get_gui_key(atr_path)
        #
        cmds.scriptJob(
            parent=gui_key,
            replacePrevious=True,
            attributeChange=[
                atr_path,
                lambda: cls.gui_update_value(atr_path, data_port_path)
            ]
        )
    #
    @classmethod
    def gui_update_value_by_data(cls, atr_path, data_port_path):
        gui_key = cls.get_gui_key(atr_path)
        #
        gui_values = cls.get_gui_values(atr_path)
        values, value_default = cls.get_dcc_values(atr_path, data_port_path)
        if values != gui_values:
            [cmds.deleteUI(i) for i in cmds.optionMenuGrp(gui_key, query=1, itemListLong=1) or []]
            for i_index, i_version in enumerate(values):
                cmds.menuItem(
                    label=i_version, data=i_index,
                    parent=gui_key+'|OptionMenu'
                )
        cls.gui_update_value(atr_path, data_port_path)
    @classmethod
    def dcc_update_data_change_callback(cls, atr_path, data_port_path):
        _ = atr_path.split('.')
        node, port_path = _

        gui_key = cls.get_gui_key(atr_path)

        data_atr_path = '{}.{}'.format(node, data_port_path)
        cmds.scriptJob(
            parent=gui_key,
            replacePrevious=True,
            attributeChange=[
                data_atr_path,
                lambda: cls.gui_update_value_by_data(atr_path, data_port_path)
            ]
        )
    #
    @classmethod
    def gui_check_value(cls, atr_path, data_port_path):
        values, value_default = cls.get_dcc_values(atr_path, data_port_path)
        gui_key = cls.get_gui_key(atr_path)
        value_current = cmds.getAttr(atr_path)
        if value_current != 'None':
            if value_current == value_default:
                cmds.optionMenu(gui_key+'|OptionMenu', edit=1, backgroundColor=(.125, 0.75, 0.5))
            else:
                cmds.optionMenu(gui_key+'|OptionMenu', edit=1, backgroundColor=(.75, 0.75, 0.125))
        else:
            cmds.optionMenu(gui_key + '|OptionMenu', edit=1, backgroundColor=(.375, 0.375, 0.375))
    #
    @classmethod
    def gui_new_fnc(cls, atr_path, label, data_port_path):
        gui_key = cls.get_gui_key(atr_path)
        cmds.optionMenuGrp(
            gui_key,
            label=label
        )
        cls.gui_build_and_update_value(atr_path, data_port_path)
        cls.gui_update_edit_callback(atr_path, data_port_path)
        cls.dcc_update_attribute_change_callback(atr_path, data_port_path)
        cls.dcc_update_data_change_callback(atr_path, data_port_path)
    @classmethod
    def gui_replace_fnc(cls, atr_path, data_port_path):
        cls.gui_build_and_update_value(atr_path, data_port_path)
        cls.gui_update_edit_callback(atr_path, data_port_path)
        cls.dcc_update_attribute_change_callback(atr_path, data_port_path)
        cls.dcc_update_data_change_callback(atr_path, data_port_path)


class AEassetRootTemplate(nodeTemplate.attributeTemplate):
    @contextmanager
    def scroll_layout(self):
        # noinspection PyArgumentList
        self.beginScrollLayout()
        yield
        # noinspection PyArgumentList
        self.endScrollLayout()
    @contextmanager
    def layout(self, label, **kwargs):
        # noinspection PyArgumentList
        cmds.editorTemplate(beginLayout=label, **kwargs)
        yield
        # noinspection PyArgumentList
        cmds.editorTemplate(endLayout=True)

    def _add_text_control_(self, port_path, label, lock=False):
        self.addCustom(
            port_path,
            lambda atr_path: TextControl.gui_new_fnc(atr_path, label, lock),
            lambda atr_path: TextControl.gui_replace_fnc(atr_path)
        )

    def _add_file_control_(self, port_path, label):
        self.addCustom(
            port_path,
            lambda atr_path: FileControl.gui_new_fnc(atr_path, label),
            lambda atr_path: FileControl.gui_replace_fnc(atr_path)
        )

    def _add_enumerate_control_(self, port_path, label, enumerate_option):
        self.addCustom(
            port_path,
            lambda atr_path: EnumerateControl.gui_new_fnc(atr_path, label, enumerate_option),
            lambda atr_path: EnumerateControl.gui_replace_fnc(atr_path)
        )

    def _add_variant_control_(self, port_path, label, data_port_path):
        self.addCustom(
            port_path,
            lambda atr_path: VariantControl.gui_new_fnc(atr_path, label, data_port_path),
            lambda atr_path: VariantControl.gui_replace_fnc(atr_path, data_port_path)
        )

    def _add_data_controls_(self, port_path, build_port_path, build_key):
        self.addCustom(
            port_path,
            lambda atr_path: DataControls.gui_new_fnc(atr_path, build_port_path, build_key),
            lambda atr_path: DataControls.gui_replace_fnc(atr_path, build_port_path, build_key)
        )

    def _add_button_controls_(self, keys, labels, icons, data_port_path):
        self.addCustom(
            keys,
            lambda atr_path: IconButtonControls.gui_new_fnc(atr_path, labels, icons, data_port_path),
            lambda atr_path: IconButtonControls.gui_replace_fnc(atr_path, data_port_path)
        )
    #
    def setup(self):
        with self.scroll_layout():
            # task
            with self.layout('Task', collapse=True):
                self.addControl('rsv_task', 'resolver task')
                with self.layout('Task Properties', collapse=True):
                    for i, j in [
                        ('project', 'project'),
                        ('asset', 'asset'),
                        ('task', 'task'),
                        ('version', 'version'),
                        ('version_extra', 'version extra'),
                        ('user', 'user'),
                    ]:
                        self._add_text_control_(
                            i, j, lock=True
                        )
                #
                with self.layout('Task ID', collapse=True):
                    for i, j in [
                        ('project_id', 'project'),
                        ('asset_id', 'asset'),
                        ('task_id', 'task'),
                        ('version_id', 'version'),
                        ('user_id', 'user'),
                    ]:
                        self._add_text_control_(
                            i, j, lock=True
                        )
                self._add_button_controls_(
                    'asset_task_refresh', 'refresh task', 'QR_refresh.png',
                    data_port_path='button_script_data'
                )
            # dcc
            with self.layout('DCC', collapse=True):
                with self.layout('Asset Properties', collapse=True):
                    self._add_data_controls_(
                        'asset_dcc_data',
                        build_port_path='ae_build_data',
                        build_key='main',
                    )
                with self.layout('Shot Asset Properties', collapse=True):
                    self._add_data_controls_(
                        'shot_asset_dcc_data',
                        build_port_path='ae_build_data',
                        build_key='main',
                    )
                #
                self._add_button_controls_(
                    'asset_dcc_refresh', 'refresh', 'QR_refresh.png',
                    data_port_path='button_script_data'
                )
            # dcc hash
            with self.layout('DCC Hash', collapse=True):
                with self.layout('Geometry UUID', collapse=True):
                    self._add_data_controls_(
                        'asset_dcc_hash_data',
                        build_port_path='ae_build_data',
                        build_key='geometry',
                    )
            # cache
            with self.layout('Cache', collapse=True):
                # self.addControl('asset_cache_file', 'file')
                self._add_file_control_(
                    'asset_cache_file', 'file'
                )
                self.addControl('asset_cache_location', 'location')
                self.addControl('asset_cache_root', 'root')
                #
                self._add_button_controls_(
                    'asset_usd_create&asset_usd_reload', 'create file&reload file', 'QR_add.png&QR_refresh.png',
                    data_port_path='button_script_data'
                )
            #
            with self.layout('Cache Variant', collapse=True):
                # variant
                for i, j in [
                    ('asset_shot', 'shot'),
                    ('asset_namespace', 'namespace'),
                ]:
                    self._add_variant_control_(i, j, data_port_path='asset_cache_variant_data')
                #   version
                #       asset version
                with self.layout('Asset Version', collapse=True):
                    for i, j in [
                        ('asset_model_version', 'model'),
                        ('asset_groom_version', 'groom'),
                        ('asset_effect_version', 'effect'),
                        ('asset_rig_version', 'rig'),
                        ('asset_surface_version', 'surface'),
                        ('asset_light_version', 'light'),
                        ('asset_camera_version', 'camera')
                    ]:
                        self._add_variant_control_(i, j, data_port_path='asset_cache_variant_data')
                    self._add_button_controls_(
                        'asset_usd_version_reset', 'reset to default', 'QR_refresh.png',
                        data_port_path='button_script_data'
                    )
                #       asset version override
                with self.layout('Asset Version Override', collapse=True):
                    for i, j in [
                        ('asset_model_version_override', 'model'),
                        ('asset_groom_version_override', 'groom'),
                        ('asset_effect_version_override', 'effect'),
                        ('asset_rig_version_override', 'rig'),
                        ('asset_surface_version_override', 'surface'),
                        ('asset_light_version_override', 'light'),
                        ('asset_camera_version_override', 'camera')
                    ]:
                        self._add_variant_control_(i, j, data_port_path='asset_cache_variant_data')
                    self._add_button_controls_(
                        'asset_usd_version_override_reset', 'reset to default', 'QR_refresh.png',
                        data_port_path='button_script_data'
                    )
                #       shot version
                with self.layout('Shot Version', collapse=True):
                    for i, j in [
                        ('shot_animation_version', 'animation'),
                        ('shot_character_effect_version', 'character effect'),
                        ('shot_effect_version', 'effect'),
                        ('shot_light_version', 'light'),
                        ('shot_camera_version', 'camera'),
                    ]:
                        self._add_variant_control_(i, j, data_port_path='asset_cache_variant_data')
                    self._add_button_controls_(
                        'shot_usd_version_reset', 'reset to default', 'QR_refresh.png',
                        data_port_path='button_script_data'
                    )
                #       shot version override
                with self.layout('Shot Version Override', collapse=True):
                    for i, j in [
                        ('shot_animation_version_override', 'animation'),
                        ('shot_character_effect_version_override', 'character effect'),
                        ('shot_effect_version_override', 'effect'),
                        ('shot_light_version_override', 'light'),
                        ('shot_camera_version_override', 'camera'),
                    ]:
                        self._add_variant_control_(i, j, data_port_path='asset_cache_variant_data')
                    self._add_button_controls_(
                        'shot_usd_version_override_reset', 'reset to default', 'QR_refresh.png',
                        data_port_path='button_script_data'
                    )
            #
            with self.layout('Cache Variant Record', collapse=True):
                self._add_data_controls_(
                    'asset_cache_variant_record_data',
                    build_port_path='ae_build_data',
                    build_key='main',
                )
                with self.layout('Asset Version', collapse=True):
                    self._add_data_controls_(
                        'asset_cache_variant_record_data',
                        build_port_path='ae_build_data',
                        build_key='asset_version',
                    )
                #
                with self.layout('Asset Version Override', collapse=True):
                    self._add_data_controls_(
                        'asset_cache_variant_record_data',
                        build_port_path='ae_build_data',
                        build_key='asset_version_override',
                    )
                #
                with self.layout('Shot Version', collapse=True):
                    self._add_data_controls_(
                        'asset_cache_variant_record_data',
                        build_port_path='ae_build_data',
                        build_key='shot_version',
                    )
                #
                with self.layout('Shot Version Override', collapse=True):
                    self._add_data_controls_(
                        'asset_cache_variant_record_data',
                        build_port_path='ae_build_data',
                        build_key='shot_version_override',
                    )
            # cache hash
            with self.layout('Cache Hash', collapse=True):
                with self.layout('Geometry UUID', collapse=True):
                    self._add_data_controls_(
                        'asset_cache_hash_data',
                        build_port_path='ae_build_data',
                        build_key='geometry',
                    )
            #
            self.beginLayout('Option')
            self.addControl('start_frame', 'start frame')
            self.addControl('end_frame', 'end frame')
            self.addControl('frame_offset', 'frame offset')
            self.addControl('frame_loop_enable', 'frame loop enable')
            self.addSeparator()
            self.addControl('frame_override_enable', 'frame override enable')
            self.addControl('start_frame_override', 'start frame override')
            self.addControl('end_frame_override', 'end frame override')
            self.endLayout()
            #
            self.beginLayout('Extra')
            self.addControl('label', 'label')
            self.addControl('description', 'description')
            self.addControl('tag', 'tag')
            self.addControl('metadata', 'metadata')
            self.endLayout()
            self.beginLayout('Data')
            for i, j in [
                ('ae_build_data', 'AE build data'),
                ('button_script_data', 'button script data'),
                ('asset_cache_variant_data', 'asset cache variant data'),
            ]:
                self._add_text_control_(
                    i, j, lock=True
                )
            self.endLayout()
            #
            mel.eval('AEtransformMain ' + self.nodeName)
            mel.eval('AEtransformNoScroll ' + self.nodeName)
            mel.eval('AEtransformSkinCluster ' + self.nodeName)
            #
            mel.eval('AEdependNodeTemplate ' + self.nodeName)
            #
            self.addExtraControls()
