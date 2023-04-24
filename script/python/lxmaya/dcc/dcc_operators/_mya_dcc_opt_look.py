# coding:utf-8
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.cmds as cmds

import collections

from lxbasic import bsc_core

from lxutil import utl_core

from lxarnold import and_configure

from lxmaya import ma_configure, ma_core

from lxmaya.dcc.dcc_operators import _mya_dcc_opt_geometry

import lxmaya.modifiers as mya_modifiers


class AbsLookOpt(object):
    def __init__(self, *args):
        self._obj = args[0]
    @property
    def obj(self):
        return self._obj

    def get_material_assign_is_default(self):
        return self.get_material_paths() == [u'initialShadingGroup']

    def get_material_paths(self):
        shape_path = self._obj.path
        return cmds.listConnections(
            shape_path, destination=1, source=0, type=ma_configure.Util.MATERIAL_TYPE
        ) or []

    def get_materials(self):
        return [self._obj.__class__(i) for i in self.get_material_paths()]

    def set_default_material_assign(self):
        shape_path = self._obj.path
        value = 'initialShadingGroup'
        cmds.sets(shape_path, forceElement=value)
        utl_core.Log.set_module_result_trace(
            'material-assign',
            u'assign="{}" >> "{}"'.format(shape_path, value)
        )

    def set_material_assigns(self, material_assigns, force=False):
        for key, value in material_assigns.items():
            if key == 'all':
                self.set_material(value)
            else:
                self.__set_comp_material_(
                    key, value
                )

    def set_material(self, material_path):
        shape_path = self._obj.path
        self._set_material_(shape_path, material_path)

    def __set_comp_material_(self, comp_name, material_path):
        shape_path = self._obj.path
        comp_path = '.'.join([shape_path, comp_name])
        self._set_material_(comp_path, material_path)
    @classmethod
    def _set_material_(cls, geometry_path, material_path):
        if cmds.objExists(material_path) is True:
            _ = cmds.sets(material_path, query=1) or []
            _ = [cmds.ls(i, long=1)[0] for i in _]
            if geometry_path not in _:
                # noinspection PyBroadException
                try:
                    cmds.sets(geometry_path, forceElement=material_path)
                    utl_core.Log.set_module_result_trace(
                        'material-assign',
                        u'assign="{}" >> "{}"'.format(geometry_path, material_path)
                    )
                except:
                    bsc_core.ExceptionMtd.set_print()
                    utl_core.Log.set_module_error_trace(
                        'material-assign',
                        u'assign="{}" >> "{}"'.format(geometry_path, material_path)
                    )
        else:
            utl_core.Log.set_module_warning_trace(
                'material-assign',
                'material-obj="{}" is non-exists'.format(material_path)
            )

    def set_properties(self, properties):
        for key, value in properties.items():
            self._obj.get_port(key).set(value)

    def set_visibilities(self, visibilities, renderer='arnold'):
        for key, value in visibilities.items():
            self._obj.get_port(key).set(value)
    @mya_modifiers.set_undo_mark_mdf
    def set_surface_shader(self, shader_path):
        shape_path = self._obj.path
        if cmds.objExists(shader_path) is True:
            material_path = '{}_SG'.format(shader_path)
            exists_material_paths = self.get_material_paths()
            if exists_material_paths:
                _ = exists_material_paths[-1]
                if _ != 'initialShadingGroup':
                    material_path = _
            #
            if cmds.objExists(material_path) is False:
                cmds.sets(renderable=1, noSurfaceShader=1, empty=1, n=material_path)
            #
            cmds.connectAttr(shader_path + '.outColor', material_path + '.surfaceShader')
            cmds.sets(shape_path, forceElement=material_path)

    def set_displacement_shader(self, shader_path):
        shape_path = self._obj.path
        if cmds.objExists(shader_path) is True:
            material_path = '{}_SG'.format(shader_path)
            exists_material_paths = self.get_material_paths()
            if exists_material_paths:
                _ = exists_material_paths[-1]
                if _ != 'initialShadingGroup':
                    material_path = _
            #
            if cmds.objExists(material_path) is False:
                cmds.sets(renderable=1, noSurfaceShader=1, empty=1, n=material_path)
            #
            cmds.connectAttr(shader_path + '.displacement', material_path + '.displacementShader')
            cmds.sets(shape_path, forceElement=material_path)


class ShapeLookOpt(AbsLookOpt):
    def __init__(self, *args):
        super(ShapeLookOpt, self).__init__(*args)


class MeshLookOpt(AbsLookOpt):
    def __init__(self, *args):
        super(MeshLookOpt, self).__init__(*args)

    def get_material_assigns(self):
        material_assigns = collections.OrderedDict()
        transform_path = self._obj.transform.path
        shape_path = self._obj.path
        material_paths = self.get_material_paths()
        if material_paths:
            for material_path in material_paths:
                elements = cmds.sets(material_path, query=1)
                if elements:
                    element_paths = [i for i in cmds.ls(elements, leaf=1, noIntermediate=1, long=1)]
                    for element_path in element_paths:
                        shot_type = cmds.ls(element_path, showType=1)[1]
                        value = material_path
                        value = ma_core._ma_obj_path__get_with_namespace_clear_(value)
                        #
                        key = None
                        if shot_type in [ma_configure.Util.MESH_TYPE]:
                            if element_path == shape_path:
                                key = 'all'
                        elif shot_type == 'float3':
                            if element_path.startswith(transform_path):
                                comp_name = element_path.split('.')[-1]
                                mesh_obj_opt = _mya_dcc_opt_geometry.MeshOpt(self._obj)
                                if mesh_obj_opt.get_comp_name_is_whole(comp_name) is True:
                                    key = 'all'
                                else:
                                    key = comp_name
                        #
                        if key is not None:
                            material_assigns[key] = value
        return material_assigns

    def get_face_assign_comp_names(self):
        lis = []
        material_assigns = self.get_material_assigns()
        if material_assigns:
            for k, v in material_assigns.items():
                if k != 'all':
                    lis.append(k)
        return lis

    def get_properties(self, renderer='arnold'):
        properties = collections.OrderedDict()
        if renderer == 'arnold':
            for key in and_configure.MeshProperty.ALL:
                if key in and_configure.MeshProperty.MAYA_DICT:
                    dcc_port_path = and_configure.MeshProperty.MAYA_DICT[key]
                    port = self._obj.get_port(dcc_port_path)
                    if port.get_is_exists() is True:
                        value = port.get()
                        properties[key] = value
                    else:
                        utl_core.Log.set_warning_trace(
                            'port: "{}" is Non-exists'.format(port.path)
                        )
        return properties

    def set_properties(self, properties, renderer='arnold'):
        if renderer == 'arnold':
            for key, value in properties.items():
                if key in and_configure.MeshProperty.MAYA_DICT:
                    dcc_port_path = and_configure.MeshProperty.MAYA_DICT[key]
                    self._obj.get_port(dcc_port_path).set(value)

    def get_visibilities(self, renderer='arnold'):
        visibilities = collections.OrderedDict()
        if renderer == 'arnold':
            kwargs = {key: self._obj.get_port(v).get() for key, v in and_configure.Visibility.MAYA_VISIBILITY_DICT.items()}
            value = and_configure.Visibility.get_visibility(**kwargs)
            visibilities[and_configure.Visibility.VISIBILITY] = value
            #
            value = self._obj.get_port(and_configure.Visibility.MAYA_AUTOBUMP_VISIBILITY).get()
            visibilities[and_configure.Visibility.AUTOBUMP_VISIBILITY] = value
        return visibilities

    def set_visibilities(self, visibilities, renderer='arnold'):
        if renderer == 'arnold':
            kwargs = and_configure.Visibility.get_visibility_as_dict(visibilities[and_configure.Visibility.VISIBILITY])
            for key, value in kwargs.items():
                if key in and_configure.Visibility.MAYA_VISIBILITY_DICT:
                    dcc_port_path = and_configure.Visibility.MAYA_VISIBILITY_DICT[key]
                    self._obj.get_port(dcc_port_path).set(value)
            #
            port = self._obj.get_port(and_configure.Visibility.MAYA_AUTOBUMP_VISIBILITY)
            if port.get_is_exists() is True:
                port.set(visibilities[and_configure.Visibility.AUTOBUMP_VISIBILITY])


class XgenDescriptionLookOpt(AbsLookOpt):
    def __init__(self, *args):
        super(XgenDescriptionLookOpt, self).__init__(*args)

    def get_material_assigns(self):
        material_assigns = collections.OrderedDict()
        shape_path = self._obj.path
        material_paths = self.get_material_paths()
        if material_paths:
            for material_path in material_paths:
                elements = cmds.sets(material_path, query=1)
                if elements:
                    element_paths = [i for i in cmds.ls(elements, leaf=1, noIntermediate=1, long=1)]
                    for element_path in element_paths:
                        if element_path == shape_path:
                            value = material_path
                            value = ma_core._ma_obj_path__get_with_namespace_clear_(value)
                            key = 'all'
                            material_assigns[key] = value
        return material_assigns

    def get_properties(self, renderer='arnold'):
        properties = collections.OrderedDict()
        if renderer == 'arnold':
            for key in and_configure.HairProperty.ALL:
                if key in and_configure.HairProperty.MAYA_XGEN_DESCRIPTION_DICT:
                    value = and_configure.HairProperty.MAYA_XGEN_DESCRIPTION_DICT[key]
                    port = self._obj.get_port(value)
                    if port.get_is_exists() is True:
                        value = port.get()
                        properties[key] = value
                    else:
                        utl_core.Log.set_warning_trace(
                            'port: "{}" is Non-exists'.format(port.path)
                        )
        return properties

    def set_properties(self, properties, renderer='arnold'):
        if renderer == 'arnold':
            for key, value in properties.items():
                if key in and_configure.HairProperty.MAYA_XGEN_DESCRIPTION_DICT:
                    dcc_port_path = and_configure.HairProperty.MAYA_XGEN_DESCRIPTION_DICT[key]
                    port = self._obj.get_port(dcc_port_path)
                    if port.get_is_exists() is True:
                        port.set(value)

    def get_visibilities(self, renderer='arnold'):
        visibilities = collections.OrderedDict()
        if renderer == 'arnold':
            kwargs = {k: self._obj.get_port(v).get() for k, v in and_configure.Visibility.MAYA_VISIBILITY_DICT.items()}
            value = and_configure.Visibility.get_visibility(**kwargs)
            visibilities[and_configure.Visibility.VISIBILITY] = value
        return visibilities

    def set_visibilities(self, visibilities, renderer='arnold'):
        if renderer == 'arnold':
            kwargs = and_configure.Visibility.get_visibility_as_dict(visibilities[and_configure.Visibility.VISIBILITY])
            for key, value in kwargs.items():
                if key in and_configure.Visibility.MAYA_VISIBILITY_DICT:
                    dcc_port_path = and_configure.Visibility.MAYA_VISIBILITY_DICT[key]
                    self._obj.get_port(dcc_port_path).set(value)


class ObjsLookOpt(object):
    SHAPE_TYPE_NAMES = [
        'mesh',
        'xgmDescription'
    ]
    TEXTURE_REFERENCE_TYPE_NAMES = [
        'file',
        'aiImage',
        'osl_window_box',
        'osl_window_box_s'
    ]
    def __init__(self, objs):
        self._objs = objs

    def get_material_paths(self):
        set_ = set([])
        for i_obj in self._objs:
            if i_obj.type in self.SHAPE_TYPE_NAMES:
                i_shape_look_opt = ShapeLookOpt(i_obj)
                i_material_paths = i_shape_look_opt.get_material_paths()
                for j_path in i_material_paths:
                    set_.add(j_path)
        return list(set_)

    def get_texture_reference_paths(self):
        def rcs_fnc_(obj_path_):
            _ = cmds.listConnections(obj_path_, destination=0, source=1) or []
            for _i in _:
                _obj_type_name = cmds.nodeType(_i)
                if _obj_type_name in self.TEXTURE_REFERENCE_TYPE_NAMES:
                    lis.append(_i)
                if not _i in keys:
                    keys.append(_i)
                    rcs_fnc_(_i)
        #
        keys = []
        lis = []
        #
        material_paths = self.get_material_paths()
        for i_path in material_paths:
            rcs_fnc_(i_path)

        return lis
