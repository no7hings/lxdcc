# coding:utf-8
import os

import re
# noinspection PyUnresolvedReferences
import hou

import lxbasic.core as bsc_core

from lxutil import utl_core

from ... import hou_configure

from .. import hou_dcc_obj_abs

from ...dcc.dcc_objects import _hou_dcc_obj_os, _hou_dcc_obj_node


class AbsFileReferences(object):
    DCC_FILE_REFERENCE_NODE_CLS = None
    SCENE_CLS = None
    # file type
    INCLUDE_DCC_FILE_TYPES = []
    EXCLUDE_DCC_FILE_TYPES = []
    # file ext
    INCLUDE_FILE_TYPES = []
    def __init__(self, *args):
        pass
    @classmethod
    def get_houdini_absolutely_path_with_parm(cls, hou_parm, path):
        re_pattern = r'.*?(\$F.*?)[\.]'
        re_results = re.findall(re_pattern, path)
        if re_results:
            frame = 9527
            sequence_path = hou_parm.evalAsStringAtFrame(frame)
            _path = sequence_path.replace(str(frame), re_results[0])
            is_sequence = True
        else:
            _path = hou_parm.eval()
            is_sequence = False
        return _path, is_sequence

    def _get_type_is_available_(self, dcc_file_type):
        raise NotImplementedError()

    def _get_type_is_used(self, file_type):
        raise NotImplementedError()

    def get_objs(self):
        lis = []
        PORT_PATHSEP = hou_configure.Util.PORT_PATHSEP
        for hou_parm, hou_path in hou.fileReferences():
            if hou_parm is not None:
                if hou_path.startswith('op:'):
                    _reference_hou_node = hou_parm.evalAsNode()
                else:
                    plf_path, is_sequence = self.get_houdini_absolutely_path_with_parm(hou_parm, hou_path)
                    dcc_file_type = hou_parm.parmTemplate().fileType()
                    if self._get_type_is_available_(dcc_file_type) is True:
                        node_path = hou_parm.node().path()
                        node = self.DCC_FILE_REFERENCE_NODE_CLS(node_path)
                        # attribute name
                        attribute_path = hou_parm.path()
                        port_path = attribute_path.split(PORT_PATHSEP)[-1]
                        node.set_file_port_path(port_path)
                        # file path
                        reference_file_path = bsc_core.StgPathOpt(plf_path).__str__()
                        node.set_file_path(reference_file_path)
                        if self._get_type_is_used(node.get_file().type):
                            lis.append(node)
        return lis


class FileReferences_(AbsFileReferences):
    DCC_FILE_REFERENCE_NODE_CLS = _hou_dcc_obj_node.FileReference
    INCLUDE_DCC_FILE_TYPES = [
        hou.fileType.Any,
        hou.fileType.Geometry,
    ]
    def __init__(self, *args):
        super(FileReferences_, self).__init__(*args)

    def _get_type_is_available_(self, dcc_file_type):
        return dcc_file_type in self.INCLUDE_DCC_FILE_TYPES

    def _get_type_is_used(self, file_type):
        return True


class FileReferences(object):
    DCC_NODE_CLS_DICT = {
        'custom': _hou_dcc_obj_node.FileReference,
        'arnold::Driver/materialx': _hou_dcc_obj_node.AndMaterialx,
    }
    CUSTOM_SEARCH_KEYS = [
        'arnold::Driver/materialx.filename',
    ]
    def __init__(self, *args):
        self._node_raw = {}

    def _get_obj_cls_(self, obj_type_path):
        if obj_type_path in self.DCC_NODE_CLS_DICT:
            return self.DCC_NODE_CLS_DICT[obj_type_path]
        return self.DCC_NODE_CLS_DICT['custom']

    def __get_by_definition_(self):
        for hou_port, plf_path in hou.fileReferences():
            if hou_port is not None:
                if hou_port is not None:
                    port_path = hou_port.path()
                    hou_obj = hou_port.node()
                    dcc_path = hou_port.node().path()
                    obj_type_path = hou_obj.type().nameWithCategory()
                    try:
                        file_path = hou_port.unexpandedString()
                    except:
                        file_path = hou_port.eval()
                    #
                    if dcc_path in self._node_raw:
                        dcc_obj = self._node_raw[dcc_path]
                    else:
                        obj_class = self._get_obj_cls_(obj_type_path)
                        dcc_obj = obj_class(dcc_path)
                        self._node_raw[dcc_path] = dcc_obj
                    #
                    dcc_obj.set_file_port_raw_add(
                        port_path, file_path
                    )

    def __get_by_custom_(self):
        pass

    def get_objs(self):
        self._node_raw = {}
        self.__get_by_definition_()
        self.__get_by_custom_()
        return self._node_raw.values()


class TextureReferences(AbsFileReferences):
    DCC_FILE_REFERENCE_NODE_CLS = _hou_dcc_obj_node.ImageReference
    INCLUDE_DCC_FILE_TYPES = [
        hou.fileType.Image
    ]
    def __init__(self, *args):
        super(TextureReferences, self).__init__(*args)

    def _get_type_is_available_(self, dcc_file_type):
        return dcc_file_type in self.INCLUDE_DCC_FILE_TYPES

    def _get_type_is_used(self, file_type):
        return True


class References(object):
    OS_FILE_CLS = _hou_dcc_obj_os.OsFile
    def __init__(self, *args):
        pass

    @classmethod
    def get_houdini_absolutely_path_with_path(cls, path):
        path_ = path
        if '$' in path_:
            # noinspection RegExpRedundantEscape
            re_pattern = re.compile(r'[\$](.*?)[\/]', re.S)
            results = re.findall(re_pattern, path_)
            for environ_key in results:
                variant = '${}'.format(environ_key)
                if environ_key in os.environ:
                    environ_value = os.environ[environ_key]
                    path_ = path_.replace(variant, environ_value)
                else:
                    bsc_core.Log.trace_warning('Variant "{}" in "{}" is Not Available.'.format(variant, path_))
        return path_

    def get_file_plf_objs(self):
        lis = []
        for hou_parm, path in hou.fileReferences():
            if hou_parm is None:
                plf_path = self.get_houdini_absolutely_path_with_path(path)
                os_file = self.OS_FILE_CLS(plf_path)
                lis.append(os_file)
        return lis


# node stack ********************************************************************************************************* #
class Alembics(hou_dcc_obj_abs.AbsHouObjs):
    INCLUDE_DCC_TYPES = [
        'Sop/alembic',
    ]
    DCC_NODE_CLS = _hou_dcc_obj_node.Alembic
    FILE_REFERENCE_FILE_PORT_PATHS_DICT = {
        'Sop/alembic': ['fileName']
    }
    def __init__(self, *args):
        super(Alembics, self).__init__(*args)


class Materialxs(hou_dcc_obj_abs.AbsHouObjs):
    INCLUDE_DCC_TYPES = [
        'arnold::Driver/materialx',
    ]
    DCC_NODE_CLS = _hou_dcc_obj_node.AndMaterialx
    FILE_REFERENCE_FILE_PORT_PATHS_DICT = {
        'arnold::Driver/materialx': ['filename']
    }
    def __init__(self, *args):
        super(Materialxs, self).__init__(*args)
