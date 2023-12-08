# coding:utf-8
import collections

import copy

import os.path

import parse

from lxkatana.core.wrap import *

import lxbasic.core as bsc_core

import lxkatana.core as ktn_core

from lxkatana.dcc import ktn_dcc_obj_abs

from lxkatana.dcc.dcc_objects import _ktn_dcc_obj_node


class Materials(ktn_dcc_obj_abs.AbsKtnObjs):
    INCLUDE_DCC_TYPES = [
        'NetworkMaterial'
    ]
    DCC_NODE_CLS = _ktn_dcc_obj_node.Material

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
    def pre_run_fnc(cls):
        _ = NodegraphAPI.GetAllNodesByType('NetworkMaterialEdit') or []
        if _:
            gp = bsc_core.LogProcessContext(maximum=len(_))
            #
            for i_ktn_obj in _:
                gp.do_update()
                # noinspection PyBroadException
                try:
                    ktn_core.NGNmeOpt(i_ktn_obj).set_contents_update()
                except Exception:
                    bsc_core.ExceptionMtd.set_print()
                    #
                    bsc_core.Log.trace_error(
                        'materials update "NetworkMaterialEdit" "{}" is failed'.format(i_ktn_obj.getName())
                    )
            #
            gp.set_stop()


class AndShaders(ktn_dcc_obj_abs.AbsKtnObjs):
    INCLUDE_DCC_TYPES = [
        'ArnoldShadingNode'
    ]
    DCC_NODE_CLS = _ktn_dcc_obj_node.AndShader

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
    def pre_run_fnc(cls):
        _ = NodegraphAPI.GetAllNodesByType('NetworkMaterialEdit') or []
        if _:
            for i_ktn_obj in _:
                # noinspection PyBroadException
                try:
                    ktn_core.NGNmeOpt(i_ktn_obj).set_contents_update()
                except Exception:
                    bsc_core.ExceptionMtd.set_print()
                    #
                    bsc_core.Log.trace_error(
                        'shaders update "NetworkMaterialEdit" "{}" is failed'.format(i_ktn_obj.getName())
                    )


class AbsTextureReferences(object):
    OBJ_CLS_DICT = {
        'image': _ktn_dcc_obj_node.TextureReference,
        'osl_file_path': _ktn_dcc_obj_node.TextureReference,
        'osl_window_box': _ktn_dcc_obj_node.TextureReference,
        'osl_window_box_s': _ktn_dcc_obj_node.TextureReference,
        'jiWindowBox_Arnold': _ktn_dcc_obj_node.TextureReference,
        #
        'custom': _ktn_dcc_obj_node.FileReference,
    }
    PORT_PATHSEP = ktn_core.KtnUtil.PORT_PATHSEP
    OPTION = dict(
        with_reference=True
    )
    PORT_QUERY_DICT = {
        'image': [
            'parameters.filename'
        ],
        'osl_file_path': [
            'parameters.filename'
        ],
        'osl_window_box': [
            'parameters.filename'
        ],
        'osl_window_box_s': [
            'parameters.filename'
        ],
        'jiWindowBox_Arnold': [
            'parameters.filename'
        ]
    }
    EXPRESSION_PATTERNS_SRC = [
        # etc. "/temp/tx/texture_name.<udim>.%04d.tx'%(frame)"
        "'{base}'%{argument}",
        # etc. "extra.texture_directory+'/tx'+'/texture_name.<udim>.%04d.tx'%(frame)"
        "{extra}'{base}'%{argument}"
    ]
    EXPRESSION_PATTERN_TGT = '\'{file}\'%{argument}'

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

    def _get_obj_type_is_available_(self, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def _get_real_file_path_(cls, port):
        ktn_port = port.ktn_port
        if ktn_port.isExpression() is True:
            e = ktn_port.getExpression()
            for i_pattern in cls.EXPRESSION_PATTERNS_SRC:
                i_p = parse.parse(
                    i_pattern, e
                )
                if i_p:
                    i_file_path_old = ktn_port.getValue(0)
                    i_base = i_p['base']
                    i_file_name = i_base.split('/')[-1]
                    i_file_path_new = '{}/{}'.format(
                        os.path.dirname(i_file_path_old), i_file_name
                    )
                    return i_file_path_new
        return ktn_port.getValue(0)

    @classmethod
    def _set_real_file_path_(cls, port, file_path, remove_expression=False):
        file_path = str(file_path)
        ktn_port = port.ktn_port
        if ktn_port.isExpression() is True:
            e = ktn_port.getExpression()
            for i_pattern in cls.EXPRESSION_PATTERNS_SRC:
                i_p = parse.parse(
                    i_pattern, e
                )
                if i_p:
                    i_kwargs = dict(
                        file=file_path,
                        argument=i_p['argument']
                    )
                    i_e_new = cls.EXPRESSION_PATTERN_TGT.format(**i_kwargs)
                    if not e == i_e_new:
                        ktn_port.setExpression(i_e_new)
                        bsc_core.Log.trace_method_result(
                            'file repath',
                            u'attribute="{}", expression="{}"'.format(port.path, i_e_new)
                        )
                        return True
            #
            if remove_expression is True:
                ktn_port.setExpressionFlag(False)
                ktn_port.setValue(file_path, 0)
                bsc_core.Log.trace_method_result(
                    'file repath',
                    u'attribute="{}", file="{}"'.format(port.path, file_path)
                )
                return True
        else:
            v = ktn_port.getValue(0)
            if not v == file_path:
                ktn_port.setValue(file_path, 0)
                bsc_core.Log.trace_method_result(
                    'file repath',
                    u'attribute="{}", file="{}"'.format(port.path, file_path)
                )
                return True
        return False

    @classmethod
    def _get_expression_(cls, port):
        ktn_port = port.ktn_port
        if ktn_port.isExpression() is True:
            e = ktn_port.getExpression()
            if e:
                return e

    @classmethod
    def _set_real_file_path_by_atr_path_(cls, atr_path, file_path):
        atr_path_opt = bsc_core.DccAttrPathOpt(atr_path)
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
    def _get_obj_cls_(cls, shader_type_name):
        if shader_type_name in cls.OBJ_CLS_DICT:
            return cls.OBJ_CLS_DICT[shader_type_name]
        return cls.OBJ_CLS_DICT['custom']

    def _set_customize_update_(self, exclude_paths=None, include_paths=None):
        objs = AndShaders.get_objs()
        for i_obj in objs:
            i_obj_path = i_obj.path
            i_obj_type_name = i_obj.get_port('nodeType').get()
            # filter by include type
            if self._get_obj_type_is_available_(i_obj_type_name) is False:
                continue
            #
            if isinstance(exclude_paths, (tuple, list)):
                if i_obj_path in exclude_paths:
                    continue
            # filter by include
            if isinstance(include_paths, (tuple, list)):
                if i_obj_path not in include_paths:
                    continue
            #
            i_ktn_obj = i_obj.ktn_obj
            # filter by bypassed
            if i_ktn_obj.isBypassed() is True:
                continue
            #
            if i_obj_type_name in self.PORT_QUERY_DICT:
                i_port_paths = self.PORT_QUERY_DICT[i_obj_type_name]
                for j_port_path in i_port_paths:
                    j_enable = i_obj.get_port('{}.enable'.format(j_port_path)).get()
                    if j_enable:
                        if i_obj_path in self._raw:
                            j_file_reference_obj = self._raw[i_obj_path]
                        else:
                            j_obj_cls = self._get_obj_cls_(i_obj_type_name)
                            j_file_reference_obj = j_obj_cls(i_obj_path)
                            self._raw[i_obj_path] = j_file_reference_obj
                        #
                        j_value_port_path = '{}.value'.format(j_port_path)
                        #
                        j_value_port = j_file_reference_obj.get_port(j_value_port_path)
                        j_value = self._get_real_file_path_(j_value_port)
                        j_file_reference_obj.set_file_port_raw_add(
                            j_value_port_path, j_value
                        )

    def get_objs(self, exclude_paths=None, include_paths=None):
        self._set_customize_update_(exclude_paths=exclude_paths, include_paths=include_paths)
        return self._raw.values()

    @classmethod
    def repath_fnc(cls, obj, port_path, file_path_new, remove_expression=False):
        cls._set_real_file_path_(
            obj.get_port(port_path), file_path_new, remove_expression
        )


class TextureReferences(AbsTextureReferences):
    INCLUDE_TYPES = [
        'image',
        'osl_file_path',
        'osl_window_box',
        'osl_window_box_s',
        'jiWindowBox_Arnold'
    ]

    def __init__(self, *args, **kwargs):
        super(TextureReferences, self).__init__(*args, **kwargs)

    def _get_obj_type_is_available_(self, obj_type_name):
        return obj_type_name in self.INCLUDE_TYPES

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
                #
                obj.set_file_port_raw_add(
                    i_port_path, i_value
                )
