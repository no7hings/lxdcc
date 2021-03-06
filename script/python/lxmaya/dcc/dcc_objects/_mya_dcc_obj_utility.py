# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from lxmaya import ma_configure

from lxutil import utl_core

from .. import mya_dcc_obj_abs


class Port(mya_dcc_obj_abs.AbsMyaPort):
    def __init__(self, node, name, port_assign=None):
        super(Port, self).__init__(node, name, port_assign=port_assign)


class Connection(mya_dcc_obj_abs.AbsMyaObjConnection):
    PORT_PATHSEP = ma_configure.Util.PORT_PATHSEP
    def __init__(self, source, target):
        super(Connection, self).__init__(source, target)


class SceneFile(object):
    FILE_TYPE_ASCII = 'mayaAscii'
    FILE_TYPE_BINARY = 'mayaBinary'
    FILE_TYPE_ALEMBIC = 'Alembic'
    FILE_TYPE_DICT = {
        '.ma': FILE_TYPE_ASCII,
        '.mb': FILE_TYPE_BINARY,
        '.abc': FILE_TYPE_ALEMBIC
    }
    def __init__(self, file_path=None):
        self._file_path = file_path
    @classmethod
    def get_type(cls, file_path=None):
        """
        :param file_path: str(path)
        :return: str(type)
        """
        ext = os.path.splitext(file_path)[-1]
        return cls.FILE_TYPE_DICT.get(ext, cls.FILE_TYPE_ASCII)
    @classmethod
    def get_current_file_path(cls):
        """
        :return: str(path)
        """
        _ = cmds.file(query=1, expandName=1)
        if isinstance(_, (str, unicode)):
            return _.replace('\\', '/')
    @classmethod
    def get_current_directory_path(cls):
        file_path = cls.get_current_file_path()
        return os.path.dirname(file_path)
    @classmethod
    def set_open(cls, file_path=None):
        cmds.file(
            file_path,
            open=1,
            options='v=0',
            force=1,
            type=cls.get_type(file_path)
        )
        utl_core.Log.set_result_trace(
            u'open file: {}'.format(file_path)
        )
    @classmethod
    def set_reference_create(cls, file_path, namespace=':'):
        return cmds.file(
            file_path,
            ignoreVersion=1,
            reference=1,
            mergeNamespacesOnClash=0,
            namespace=namespace,
            options='v=0;p=17;f=0',
            type=cls.get_type(file_path)
        )


class Selection(object):
    def __init__(self, *args):
        self._paths = args[0]

    def set_all_select(self):
        exist_paths = [i for i in self._paths if cmds.objExists(i)]
        cmds.select(exist_paths)
    @classmethod
    def set_clear(cls):
        cmds.select(clear=1)
    @classmethod
    def get_current(cls):
        _ = cmds.ls(selection=1, long=1)
        if _:
            return _[0]
    @classmethod
    def get_selected_paths(cls, include=None):
        if include is not None:
            return cmds.ls(selection=1, type=include, long=1, dag=1, noIntermediate=1)
        return cmds.ls(selection=1, long=1, dag=1, noIntermediate=1)


class Workspace(object):
    pass


class ConfirmDialog(object):
    def __init__(self, title, message):
        self._title = title
        self._message = message

    def show(self):
        cmds.confirmDialog(
            title=self._title,
            message=self._message
        )
    @classmethod
    def show_warning(cls, message):
        cmds.confirmDialog(
            title='Warning',
            message=message
        )
    @classmethod
    def show_result(cls, message):
        cmds.confirmDialog(
            title='Result',
            message=message
        )
    @classmethod
    def show_error(cls, message):
        cmds.confirmDialog(
            title='Error',
            message=message
        )
