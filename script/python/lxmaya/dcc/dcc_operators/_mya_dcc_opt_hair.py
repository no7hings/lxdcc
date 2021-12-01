# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from lxbasic import bsc_core

from lxobj import obj_configure

from lxutil import utl_core

from lxmaya import ma_core


class XgenDescriptionOpt(object):
    def __init__(self, *args):
        self._obj = args[0]

    def get_path(self, lstrip=None):
        # remove namespace, use transform path
        raw = ma_core._ma_obj_path__get_with_namespace_clear_(self._obj.transform.path)
        # replace pathsep
        raw = raw.replace(self._obj.PATHSEP, obj_configure.Obj.PATHSEP)
        # strip path
        if lstrip is not None:
            if raw.startswith(lstrip):
                raw = raw[len(lstrip):]
        return raw

    def get_path_as_uuid(self, lstrip=None):
        return bsc_core.HashMtd.get_hash_value(self.get_path(lstrip), as_unique_id=True)

    def get_name(self):
        # use transform name
        raw = self._obj.transform.name
        raw = ma_core._ma_obj_name__get_with_namespace_clear_(raw)
        return raw

    def get_name_as_uuid(self):
        return bsc_core.HashMtd.get_hash_value(self.get_name(), as_unique_id=True)
