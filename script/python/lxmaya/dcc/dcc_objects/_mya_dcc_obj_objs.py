# coding:utf-8
import re

import copy

import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxmaya import ma_configure

from lxmaya.dcc import mya_dcc_obj_abs

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_obj, _mya_dcc_obj_dag, _mya_dcc_obj_xgen, _mya_dcc_obj_arnold


class Nodes(object):
    DCC_OBJ_CLASS = _mya_dcc_obj_obj.Node
    def __init__(self, type_names):
        self._type_names = type_names

    def get_obj_paths(self):
        return cmds.ls(type=self._type_names, long=1) or []

    def get_objs(self):
        return [self.DCC_OBJ_CLASS(i) for i in self.get_obj_paths()]


class Sets(mya_dcc_obj_abs.AbsMyaObjs):
    INCLUDE_DCC_TYPES = ['objectSet']
    EXCLUDE_DCC_PATHS = ['defaultLightSet', 'defaultObjectSet']
    DCC_OBJ_CLASS = _mya_dcc_obj_dag.Shape
    def __init__(self, *args):
        super(Sets, self).__init__(*args)


class Cameras(mya_dcc_obj_abs.AbsMyaObjs):
    INCLUDE_DCC_TYPES = ['camera']
    EXCLUDE_DCC_PATHS = ['|persp|perspShape', '|top|topShape', '|front|frontShape', '|side|sideShape']
    DCC_OBJ_CLASS = _mya_dcc_obj_dag.Shape
    def __init__(self, *args):
        super(Cameras, self).__init__(*args)


class AnimationLayers(mya_dcc_obj_abs.AbsMyaObjs):
    INCLUDE_DCC_TYPES = ['animLayer']
    EXCLUDE_DCC_PATHS = ['BaseAnimation']
    DCC_OBJ_CLASS = _mya_dcc_obj_obj.Node
    def __init__(self, *args):
        super(AnimationLayers, self).__init__(*args)


class DisplayLayers(mya_dcc_obj_abs.AbsMyaObjs):
    INCLUDE_DCC_TYPES = ['displayLayer']
    EXCLUDE_DCC_PATHS = ['defaultLayer']
    DCC_OBJ_CLASS = _mya_dcc_obj_obj.DisplayLayer
    def __init__(self, *args):
        super(DisplayLayers, self).__init__(*args)


class Constrains(mya_dcc_obj_abs.AbsMyaObjs):
    INCLUDE_DCC_TYPES = [
        'parentConstraint',
        'pointConstraint',
        'orientConstraint',
        'scaleConstraint'
    ]
    EXCLUDE_DCC_PATHS = []
    DCC_OBJ_CLASS = _mya_dcc_obj_obj.Node
    def __init__(self, *args):
        super(Constrains, self).__init__(*args)


class UnknownNodes(mya_dcc_obj_abs.AbsMyaObjs):
    INCLUDE_DCC_TYPES = ['unknown']
    EXCLUDE_DCC_PATHS = []
    DCC_OBJ_CLASS = _mya_dcc_obj_obj.Node
    def __init__(self, *args):
        super(UnknownNodes, self).__init__(*args)


class References(mya_dcc_obj_abs.AbsMyaObjs):
    INCLUDE_DCC_TYPES = ['reference']
    EXCLUDE_DCC_PATHS = ['_UNKNOWN_REF_NODE_', 'sharedReferenceNode']
    DCC_OBJ_CLASS = _mya_dcc_obj_obj.Reference
    def __init__(self, *args):
        super(References, self).__init__(*args)

    def get_reference_raw(self):
        lis = []
        for i in self.get_custom_nodes():
            file_path = i.get_file_path()
            namespace = i.get_namespace()
            lis.append((file_path, namespace))
        return lis


class Materials(mya_dcc_obj_abs.AbsMyaObjs):
    INCLUDE_DCC_TYPES = ['shadingEngine']
    EXCLUDE_DCC_PATHS = [
        'initialShadingGroup',
        'initialParticleSE',
        'defaultLightSet',
        'defaultObjectSet'
    ]
    DCC_OBJ_CLASS = _mya_dcc_obj_obj.Material
    def __init__(self, *args):
        super(Materials, self).__init__(*args)

    def get_reference_raw(self):
        lis = []
        for i in self.get_custom_nodes():
            file_path = i.get_file_path()
            namespace = i.get_namespace()
            lis.append((file_path, namespace))
        return lis


class TemporaryNodes(mya_dcc_obj_abs.AbsMyaObjs):
    INCLUDE_DCC_TYPES = ['mesh', 'nurbsCurve', 'nurbsSurface', 'brush', 'nParticle']
    EXCLUDE_DCC_PATHS = []
    DCC_OBJ_CLASS = _mya_dcc_obj_obj.Node
    def __init__(self, *args):
        super(TemporaryNodes, self).__init__(*args)


class AbsFileReferences(object):
    DCC_NODE_CLASS_DICT = {
        'custom': _mya_dcc_obj_obj.FileReference,
        'file': _mya_dcc_obj_obj.TextureReference,
        # it's right name
        'aiImage': _mya_dcc_obj_obj.TextureReference,
        'reference': _mya_dcc_obj_obj.Reference,
        #
        'xgmPalette': _mya_dcc_obj_xgen.XgnPalette,
        'xgmDescription': _mya_dcc_obj_xgen.XgnDescription,
        #
        'aiMaterialx': _mya_dcc_obj_arnold.AndMaterialx,
        #
        'osl_file_path': _mya_dcc_obj_obj.TextureReference,
    }
    #
    CUSTOM_SEARCH_KEYS = [
        'gpuCache.cacheFileName',
        'AlembicNode.abc_File',
        'aiVolume.filename',
        'aiMaterialx.filename'
    ]
    PORT_QUERY_DICT = {
        'file': ['fileTextureName'],
        'aiImage': ['filename'],
        #
        'gpuCache': ['cacheFileName'],
        'AlembicNode': ['abc_File'],
        #
        'aiVolume': ['filename'],
        'aiMaterialx': ['filename'],
        #
        'osl_file_path': ['filename']
    }
    PORT_PATHSEP = ma_configure.Util.PORT_PATHSEP
    #
    OPTION = dict(
        with_reference=True,
        includes=[]
    )

    def __init__(self, *args, **kwargs):
        self._raw = {}
        #
        self._option = copy.deepcopy(self.OPTION)
        if 'option' in kwargs:
            option = kwargs['option']
            if isinstance(option, dict):
                for k, v in option.items():
                    if k in self.OPTION:
                        self._option[k] = v
    # convert for file
    @classmethod
    def _set_file_gain_value_convert_(cls, obj, file_path):
        if obj.type == 'file':
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            re_pattern = re.compile(r'.*?(<udim>).*?', re.IGNORECASE)
            results = re.findall(re_pattern, file_name)
            if results:
                return file_path
            #
            mode = obj.get_port('uvTilingMode').get()
            if mode == 3:
                results = re.findall(r'[0-9][0-9][0-9][0-9]', file_name)
                if results:
                    return file_path.replace(results[-1], '<UDIM>')
            return file_path
        else:
            return file_path
    @classmethod
    def _get_real_file_path_(cls, port):
        pass
    @classmethod
    def _set_real_file_path_(cls, port, new_value):
        port.set(new_value)
        obj = port.obj
        #
        cls._set_file_value_repair_(obj)
    @classmethod
    @utl_core._debug_
    def _set_file_value_repair_(cls, obj):
        port = obj.get_port('fileTextureName')
        file_path = port.get()
        file_ = utl_dcc_objects.OsFile(file_path)
        if file_.get_is_udim():
            if obj.get_port('uvTilingMode').get() == 3:
                exists_file_paths = file_.get_exists_file_paths()
                port.set(exists_file_paths[0])
        # crash error for close
        # mel.eval('generateUvTilePreview {}'.format(obj.path))
    @classmethod
    def set_files_value_repair(cls):
        fs = cmds.ls(type='file')
        for i_f in fs:
            cls._set_file_value_repair_(
                _mya_dcc_obj_obj.Node(i_f)
            )
    @classmethod
    def _get_obj_cls_(cls, obj_type_name):
        if obj_type_name in cls.DCC_NODE_CLASS_DICT:
            return cls.DCC_NODE_CLASS_DICT[obj_type_name]
        return cls.DCC_NODE_CLASS_DICT['custom']
    @classmethod
    def _get_type_is_available_(cls, *args):
        return True

    def __get_by_definition_(self, with_reference):
        cmds.filePathEditor(refresh=1)
        directory_paths = cmds.filePathEditor(query=1, listDirectories="") or []
        for directory_path in directory_paths:
            raw = cmds.filePathEditor(query=1, listFiles=directory_path, withAttribute=1) or []
            for i in range(len(raw) / 2):
                i_file_name = raw[i * 2]
                i_atr_path = raw[i * 2 + 1]
                search_key = cmds.filePathEditor(i_atr_path, query=1, attributeType=1)
                #
                search_key_s = search_key.split(self.PORT_PATHSEP)
                obj_type_name = search_key_s[0]
                if self._get_type_is_available_(obj_type_name) is False:
                    continue
                #
                i_file_path = u'{}/{}'.format(directory_path, i_file_name)
                #
                atr_path_s = i_atr_path.split(self.PORT_PATHSEP)
                #
                obj_path = atr_path_s[0]
                port_path = self.PORT_PATHSEP.join(atr_path_s[1:])
                #
                if obj_path in self._raw:
                    obj = self._raw[obj_path]
                else:
                    obj_cls = self._get_obj_cls_(obj_type_name)
                    obj = obj_cls(obj_path)
                    self._raw[obj_path] = obj
                #
                if with_reference is False:
                    is_reference = obj.get_is_reference()
                    if is_reference is True:
                        continue
                #
                obj.set_file_port_raw_add(
                    port_path, self._set_file_gain_value_convert_(obj, i_file_path)
                )

    def __get_by_custom_(self, with_reference):
        all_obj_type_names = cmds.allNodeTypes()
        #
        for i_obj_type_name, i_port_paths in self.PORT_QUERY_DICT.items():
            if self._get_type_is_available_(i_obj_type_name) is False:
                continue
            #
            if i_obj_type_name not in all_obj_type_names:
                utl_core.Log.set_warning_trace(
                    'obj-type="{}" is "unknown" / "unload"'.format(i_obj_type_name)
                )
                continue
            #
            for j_port_path in i_port_paths:
                obj_paths = cmds.ls(type=i_obj_type_name, long=1) or []
                for j_obj_path in obj_paths:
                    j_atr_path = self.PORT_PATHSEP.join([j_obj_path, j_port_path])
                    j_file_path = cmds.getAttr(j_atr_path)
                    if not j_file_path:
                        utl_core.Log.set_warning_trace(
                            'port="{}" is "empty"'.format(j_atr_path)
                        )
                        continue
                    if j_obj_path in self._raw:
                        obj = self._raw[j_obj_path]
                    else:
                        obj_cls = self._get_obj_cls_(i_obj_type_name)
                        obj = obj_cls(j_obj_path)
                        self._raw[j_obj_path] = obj
                    #
                    if with_reference is False:
                        is_reference = obj.get_is_reference()
                        if is_reference is True:
                            continue
                    #
                    obj.set_file_port_raw_add(
                        j_port_path, self._set_file_gain_value_convert_(obj, j_file_path)
                    )

    def get_objs(self):
        with_reference = self._option['with_reference']
        #
        self._raw = {}
        self.__get_by_definition_(with_reference)
        self.__get_by_custom_(with_reference)
        return self._raw.values()

    def get_types(self):
        pass

    def get_exists_file_paths(self):
        lis = []
        path_dict = {}
        for n in self.get_objs():
            for f in n.get_file_plf_objs():
                sub_files = f.get_exists_files()
                for sf in sub_files:
                    normcase_file_path = sf.normcase_path
                    if normcase_file_path in path_dict:
                        file_path = path_dict[normcase_file_path]
                    else:
                        file_path = sf.path
                        path_dict[normcase_file_path] = file_path
                    #
                    lis.append(file_path)
        return lis

    def get_file_paths(self):
        lis = []
        path_dict = {}
        for n in self.get_objs():
            for f in n.get_file_plf_objs():
                normcase_file_path = f.normcase_path
                if normcase_file_path in path_dict:
                    file_path = path_dict[normcase_file_path]
                else:
                    file_path = f.path
                    path_dict[normcase_file_path] = file_path
                #
                lis.append(file_path)
        return lis


class FileReferences(AbsFileReferences):
    def __init__(self, *args, **kwargs):
        super(FileReferences, self).__init__(*args, **kwargs)


class TextureReferences(AbsFileReferences):
    INCLUDE_DCC_FILE_TYPES = [
        'file',
        'aiImage.filename',
    ]
    INCLUDE_TYPES = [
        'file',
        'aiImage',
        'osl_file_path'
    ]
    def __init__(self, *args, **kwargs):
        super(TextureReferences, self).__init__(*args, **kwargs)

    def _get_type_is_available_(self, file_type):
        return file_type in self.INCLUDE_TYPES
    @classmethod
    def _get_objs_(cls, obj_paths):
        lis = []
        for obj_path in obj_paths:
            i_obj_type_name = cmds.nodeType(obj_path)
            if i_obj_type_name in cls.PORT_QUERY_DICT:
                obj_cls = cls._get_obj_cls_(i_obj_type_name)
                obj = obj_cls(obj_path)
                cls._set_obj_reference_update_(obj)
                lis.append(obj)
        return lis
    @classmethod
    def _set_obj_reference_update_(cls, obj):
        obj_type_name = obj.type_name
        obj_path = obj.path
        if obj_type_name in cls.PORT_QUERY_DICT:
            port_paths = cls.PORT_QUERY_DICT[obj_type_name]
            obj.set_reference_raw_clear()
            for i_port_path in port_paths:
                atr_path = cls.PORT_PATHSEP.join([obj_path, i_port_path])
                value = cmds.getAttr(atr_path)
                obj.set_file_port_raw_add(
                    i_port_path, cls._set_file_gain_value_convert_(obj, value)
                )


class XgenPalettes(mya_dcc_obj_abs.AbsMyaObjs):
    INCLUDE_DCC_TYPES = ['xgmPalette']
    EXCLUDE_DCC_PATHS = []
    DCC_OBJ_CLASS = _mya_dcc_obj_xgen.XgnPalette
    def __init__(self):
        super(XgenPalettes, self).__init__(XgenPalettes)


class XgenDescriptions(mya_dcc_obj_abs.AbsMyaObjs):
    INCLUDE_DCC_TYPES = ['xgmDescription']
    EXCLUDE_DCC_PATHS = []
    DCC_OBJ_CLASS = _mya_dcc_obj_xgen.XgnDescription
    def __init__(self):
        super(XgenDescriptions, self).__init__(XgenPalettes)
