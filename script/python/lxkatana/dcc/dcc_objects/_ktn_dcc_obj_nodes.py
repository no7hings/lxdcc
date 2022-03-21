# coding:utf-8
import collections

import copy

import parse
# noinspection PyUnresolvedReferences
import NodegraphAPI

from lxutil import utl_core

from lxbasic import bsc_core

from lxkatana import ktn_configure, ktn_core

from lxkatana.dcc import ktn_dcc_obj_abs

from lxkatana.dcc.dcc_objects import _ktn_dcc_obj_node


class Materials(ktn_dcc_obj_abs.AbsKtnObjs):
    INCLUDE_DCC_TYPES = [
        'NetworkMaterial'
    ]
    DCC_OBJ_CLASS = _ktn_dcc_obj_node.Material
    def __init__(self, *args):
        super(Materials, self).__init__(*args)
    @classmethod
    def get_material_dict(cls):
        dic_0 = {}
        objs = cls.get_objs()
        for obj in objs:
            if obj.get_parent().ktn_obj.isBypassed() is True:
                continue
            key = obj.get_port('sceneGraphLocation').get()
            #
            dic_0.setdefault(
                key, []
            ).append(obj)
        #
        dic = {}
        #
        for k, v in dic_0.items():
            nme_objs = [i for i in v if i.get_parent().type == 'NetworkMaterialEdit']
            nmc_objs = [i for i in v if i.get_parent().type == 'NetworkMaterialCreate']
            #
            if nme_objs:
                dic[k] = nme_objs[0]
            else:
                # if len(nmc_objs) > 1:
                #     print nmc_objs
                dic[k] = nmc_objs[0]
        return dic
    @classmethod
    def get_nmc_material_dict(cls):
        dic_0 = {}
        objs = cls.get_objs()
        for obj in objs:
            if obj.get_parent().ktn_obj.isBypassed() is True:
                continue
            #
            key = obj.get_port('sceneGraphLocation').get()
            dic_0.setdefault(
                key, []
            ).append(obj)
        #
        dic = {}
        #
        for k, v in dic_0.items():
            nmc_objs = [i for i in v if i.get_parent().type == 'NetworkMaterialCreate']
            if nmc_objs:
                dic[k] = nmc_objs[0]
        return dic
    @classmethod
    def get_nme_material_dict(cls):
        dic_0 = {}
        objs = cls.get_objs()
        for obj in objs:
            if obj.get_parent().ktn_obj.isBypassed() is True:
                continue
            #
            key = obj.get_port('sceneGraphLocation').get()
            dic_0.setdefault(
                key, []
            ).append(obj)
        #
        dic = {}
        #
        for k, v in dic_0.items():
            nme_objs = [i for i in v if i.get_parent().type == 'NetworkMaterialEdit']
            if nme_objs:
                dic[k] = nme_objs[0]
        return dic
    @classmethod
    def _set_pre_run_(cls):
        _ = NodegraphAPI.GetAllNodesByType('NetworkMaterialEdit') or []
        if _:
            gp = utl_core.GuiProgressesRunner(maximum=len(_))
            #
            for i_ktn_obj in _:
                gp.set_update()
                # noinspection PyBroadException
                try:
                    ktn_core.NGNmeOpt(i_ktn_obj).set_contents_update()
                except:
                    bsc_core.ExceptionMtd.set_print()
                    #
                    utl_core.Log.set_error_trace(
                        'materials update "NetworkMaterialEdit" "{}" is failed'.format(i_ktn_obj.getName())
                    )
            #
            gp.set_stop()


class AndShaders(ktn_dcc_obj_abs.AbsKtnObjs):
    INCLUDE_DCC_TYPES = [
        'ArnoldShadingNode'
    ]
    DCC_OBJ_CLASS = _ktn_dcc_obj_node.AndShader
    def __init__(self, *args):
        super(AndShaders, self).__init__(*args)
    @classmethod
    def get_texture_references(cls, **kwargs):
        lis = []
        _ = cls.get_objs(**kwargs)
        for i in _:
            if i.get_port('nodeType').get() == 'image':
                lis.append(i)
        return lis
    @classmethod
    def get_standard_surfaces(cls, **kwargs):
        lis = []
        _ = cls.get_objs(**kwargs)
        for i in _:
            if i.get_port('nodeType').get() == 'standard_surface':
                lis.append(i)
        return lis
    @classmethod
    def _set_pre_run_(cls):
        _ = NodegraphAPI.GetAllNodesByType('NetworkMaterialEdit') or []
        if _:
            for i_ktn_obj in _:
                # noinspection PyBroadException
                try:
                    ktn_core.NGNmeOpt(i_ktn_obj).set_contents_update()
                except:
                    bsc_core.ExceptionMtd.set_print()
                    #
                    utl_core.Log.set_error_trace(
                        'shaders update "NetworkMaterialEdit" "{}" is failed'.format(i_ktn_obj.getName())
                    )


class AbsTextureReferences(object):
    OBJ_CLASS_DICT = {
        'image': _ktn_dcc_obj_node.TextureReference,
        'custom': _ktn_dcc_obj_node.FileReference,
    }
    CUSTOM_SEARCH_KEYS = [
        'image.parameters.filename'
    ]
    #
    PORT_PATHSEP = ktn_configure.Util.PORT_PATHSEP
    OPTION = dict(
        with_reference=True
    )
    PORT_QUERY_DICT = {
        'image': [
            'parameters.filename'
        ]
    }
    def __init__(self, *args, **kwargs):
        self._raw = collections.OrderedDict()
        #
        self._option = copy.deepcopy(self.OPTION)
        if 'option' in kwargs:
            option = kwargs['option']
            if isinstance(option, dict):
                for k, v in option.items():
                    if k in self.OPTION:
                        self._option[k] = v

    def _get_obj_type_is_available_(self, search_key):
        raise NotImplementedError()
    @classmethod
    def _get_real_file_path_(cls, port):
        parse_pattern = '\'{file}\'%{argument}'
        ktn_port = port.ktn_port
        e = ktn_port.getExpression()
        if e:
            p = parse.parse(parse_pattern, e)
            if p:
                return p.named.get('file')
            return ktn_port.getValue(0)
        return ktn_port.getValue(0)
    @classmethod
    def _get_expression_(cls, port):
        ktn_port = port.ktn_port
        e = ktn_port.getExpression()
        if e:
            return e
    @classmethod
    def _set_real_file_path_by_atr_path_(cls, atr_path, file_path):
        atr_path_opt = bsc_core.AtrPathOpt(atr_path)
        obj_path, port_path = atr_path_opt.obj_path, atr_path_opt.port_path
        obj_path_opt = bsc_core.DccPathDagOpt(obj_path)
        obj_name = obj_path_opt.name
        ktn_obj_opt = ktn_core.NGObjOpt(obj_name)
        shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
        obj_cls = cls._get_obj_cls_(shader_type_name)
        obj = obj_cls(obj_path)
        port = obj.get_port(port_path)
        #
        cls._set_real_file_path_(port, file_path)
    @classmethod
    def _set_real_file_path_(cls, port, file_path):
        file_path = str(file_path)
        parse_pattern = '\'{file}\'%{argument}'
        ktn_port = port.ktn_port
        e = ktn_port.getExpression()
        if e:
            p = parse.parse(parse_pattern, e)
            if p:
                new_expression = parse_pattern.format(
                    **dict(file=file_path, argument=p.named.get('argument'))
                )
                if not e == new_expression:
                    ktn_port.setExpression(new_expression)
                    utl_core.Log.set_module_result_trace(
                        'texture repath',
                        'port="{}"'.format(port.path)
                    )
                    utl_core.Log.set_module_result_trace(
                        'texture repath',
                        'expression="{}"'.format(new_expression)
                    )
        else:
            v = ktn_port.getValue(0)
            if not v == file_path:
                ktn_port.setValue(file_path, 0)
                #
                utl_core.Log.set_module_result_trace(
                    'texture repath',
                    'port="{}"'.format(port.path)
                )
                utl_core.Log.set_module_result_trace(
                    'texture repath',
                    'file="{}"'.format(file_path)
                )
    @classmethod
    def _get_obj_cls_(cls, shader_type_name):
        if shader_type_name in cls.OBJ_CLASS_DICT:
            return cls.OBJ_CLASS_DICT[shader_type_name]
        return cls.OBJ_CLASS_DICT['custom']

    def _set_customize_update_(self, exclude_paths):
        for search_key in self.CUSTOM_SEARCH_KEYS:
            if self._get_obj_type_is_available_(search_key) is False:
                continue
            #
            _ = search_key.split(self.PORT_PATHSEP)
            shader_type_name = _[0]
            port_key = self.PORT_PATHSEP.join(_[1:])
            #
            _ = AndShaders.get_objs()
            for obj in _:
                obj_path = obj.path
                if isinstance(exclude_paths, (tuple, list)):
                    if obj_path in exclude_paths:
                        continue
                #
                ktn_obj = obj.ktn_obj
                if ktn_obj.isBypassed() is True:
                    continue
                #
                if obj.get_port('nodeType').get() == shader_type_name:
                    # if not enable ignore
                    # if use "NetworkMaterialEdit" enable is 0 if value is not override
                    enable = obj.get_port('{}.enable'.format(port_key)).get()
                    if enable:
                        if obj_path in self._raw:
                            file_reference_obj = self._raw[obj_path]
                        else:
                            obj_cls = self._get_obj_cls_(shader_type_name)
                            file_reference_obj = obj_cls(obj_path)
                            self._raw[obj_path] = file_reference_obj
                        #
                        port_path = '{}.value'.format(port_key)
                        #
                        port = file_reference_obj.get_port(port_path)
                        value = self._get_real_file_path_(port)
                        file_reference_obj.set_file_port_raw_add(
                            port_path, value
                        )

    def get_objs(self, exclude_paths=None):
        self._set_customize_update_(exclude_paths=exclude_paths)
        return self._raw.values()


class TextureReferences(AbsTextureReferences):
    INCLUDE_SEARCH_KEYS = [
        'image.parameters.filename'
    ]
    def __init__(self, *args, **kwargs):
        super(TextureReferences, self).__init__(*args, **kwargs)

    def _get_obj_type_is_available_(self, search_key):
        return search_key in self.INCLUDE_SEARCH_KEYS
    @classmethod
    def _set_obj_reference_update_(cls, obj):
        ktn_obj_opt = ktn_core.NGObjOpt(bsc_core.DccPathDagOpt(obj.path).name)
        shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
        if shader_type_name in cls.PORT_QUERY_DICT:
            port_keys = cls.PORT_QUERY_DICT[shader_type_name]
            obj.set_reference_raw_clear()
            for i_port_key in port_keys:
                i_port_path = '{}.value'.format(i_port_key)
                #
                i_port = obj.get_port(i_port_path)
                i_value = cls._get_real_file_path_(i_port)
                obj.set_file_port_raw_add(
                    i_port_path, i_value
                )


class MaterialAssigns(ktn_dcc_obj_abs.AbsKtnObjs):
    INCLUDE_DCC_TYPES = [
        'MaterialAssign'
    ]
    DCC_OBJ_CLASS = _ktn_dcc_obj_node.MaterialAssign
    def __init__(self, *args):
        super(MaterialAssigns, self).__init__(*args)
