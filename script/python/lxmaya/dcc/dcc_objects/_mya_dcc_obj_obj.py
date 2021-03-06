# coding:utf-8
import fnmatch
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from lxmaya import ma_core

from lxmaya.dcc import mya_dcc_obj_abs

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_utility

from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects


class Port(mya_dcc_obj_abs.AbsMyaPort):
    def __init__(self, node, name, port_assign=None):
        super(Port, self).__init__(node, name, port_assign=port_assign)


class Node(mya_dcc_obj_abs.AbsMyaObj):
    PORT_CLASS = _mya_dcc_obj_utility.Port
    CONNECTION_CLASS = _mya_dcc_obj_utility.Connection
    def __init__(self, path):
        super(Node, self).__init__(path)
    # dag
    def get_child_paths(self):
        return cmds.listRelatives(self.path, children=1, fullPath=1) or []

    def get_children(self):
        return [self.__class__(i) for i in self.get_child_paths()]

    def get_descendant_paths(self, *args, **kwargs):
        def _rcs_fnc(lis_, path_):
            lis_.append(path_)
            _ = cmds.listRelatives(path_, children=1, fullPath=1) or []
            if _:
                for _i in _:
                    _rcs_fnc(lis_, _i)
        lis = []
        _rcs_fnc(lis, self.path)
        return lis

    def get_descendants(self, *args, **kwargs):
        # noinspection PyArgumentList
        return [self.__class__(i) for i in self.get_descendant_paths(*args, **kwargs)]


class DisplayLayer(mya_dcc_obj_abs.AbsMyaObj):
    PORT_CLASS = _mya_dcc_obj_utility.Port
    CONNECTION_CLASS = _mya_dcc_obj_utility.Connection
    DCC_OBJ_CLASS = Node
    def __init__(self, path):
        super(DisplayLayer, self).__init__(path)

    def get_objs(self):
        lis = []
        for path in self.get_node_paths():
            lis.append(self.DCC_OBJ_CLASS(path))
        return lis

    def get_node_paths(self):
        if cmds.objExists(self.path):
            return cmds.editDisplayLayerMembers(self.path, query=1, fullNames=1) or []
        return []


class Reference(mya_dcc_obj_abs.AbsMyaFileReferenceObj):
    PORT_CLASS = _mya_dcc_obj_utility.Port
    OS_FILE_CLASS = utl_dcc_objects.OsFile
    def __init__(self, path):
        super(Reference, self).__init__(self._get_full_path_(path))

    def get_is_loaded(self):
        # noinspection PyBroadException
        try:
            return cmds.referenceQuery(self.name, isLoaded=1)
        except:
            return False

    def set_replace(self, file_path):
        cmds.file(file_path, loadReference=self.name)
        utl_core.Log.set_module_result_trace(
            'reference replace',
            u'file="{}"'.format(file_path)
        )

    def set_reload(self):
        cmds.file(loadReference=self.name)

    def set_load(self):
        cmds.file(loadReference=self.name)

    def set_remove(self):
        if cmds.objExists(self.name):
            file_path = cmds.referenceQuery(self.name, filename=1)
            cmds.file(file_path, removeReference=1)

    def set_unload(self):
        cmds.file(unloadReference=self.name)

    def get_file_path(self, extend=True):
        _ = cmds.referenceQuery(self.name, filename=1)
        if extend is True:
            return cmds.referenceQuery(self.name, filename=1, withoutCopyNumber=1)
        return _

    def get_file(self):
        return utl_dcc_objects.OsFile(self.get_file_path())

    def get_namespace_path(self):
        return cmds.referenceQuery(self.name, namespace=1)

    def get_namespace(self):
        return cmds.referenceQuery(self.name, namespace=1, shortName=1)

    def set_namespace_path(self, namespace_path):
        if cmds.namespace(exists=namespace_path) is False:
            file_path = cmds.referenceQuery(self.name, filename=1)
            cmds.file(file_path, namespace=namespace_path, edit=1)

    def get_content_obj_paths(self):
        return [cmds.ls(i, long=1)[0] for i in cmds.referenceQuery(self.name, nodes=1, dagPath=1) or []]

    def set_load_from_file(self, file_path, namespace):
        if cmds.objExists(self.name) is False:
            result = _mya_dcc_obj_utility.SceneFile.set_reference_create(file_path, namespace)
            rn = cmds.referenceQuery(result, referenceNode=1)
            if rn != self.name:
                cmds.lockNode(rn, lock=0)
                r = cmds.rename(rn, self.name)
                cmds.lockNode(r, lock=1)

    def get_content_root_paths(self):
        paths = [cmds.ls(i, long=1)[0] for i in cmds.referenceQuery(self.name, nodes=1, dagPath=1) or []]
        return [path for path in paths if len(path.split(self.PATHSEP)) == 2]

    def _test(self):
        pass


class Material(mya_dcc_obj_abs.AbsMyaObj):
    PORT_CLASS = _mya_dcc_obj_utility.Port
    CONNECTION_CLASS = _mya_dcc_obj_utility.Connection
    #
    SHADING_NODE_TYPES = ['mesh', 'pgYetiMaya', 'nurbsHair']
    OBJ_TYPE = 'shadingEngine'
    def __init__(self, path):
        super(Material, self).__init__(path)

    def get_assign_dict(self):
        dic = {}
        _ = cmds.sets(self.path, query=1)
        if _:
            paths = [i for i in cmds.ls(_, leaf=1, noIntermediate=1, long=1)]
            for raw in paths:
                # Object Group
                show_type = cmds.ls(raw, showType=1)[1]
                if show_type in self.SHADING_NODE_TYPES:
                    dic.setdefault('obj', []).append(raw)
                # Component Object Group
                elif show_type == 'float3':
                    # check component is whole
                    obj_path, obj_cmp_name = raw.split('.')
                    face_count = cmds.polyEvaluate(obj_path, face=1)
                    whole_obj_cmp_name = 'f[0:{}]'.format(face_count-1)
                    if obj_cmp_name == whole_obj_cmp_name:
                        dic.setdefault('obj', []).append(raw)
                    else:
                        dic.setdefault('obj_cmp', []).append(raw)
        return dic

    def set_create(self, type_name):
        if self.get_is_exists() is False:
            ma_core.CmdObjOpt._set_material_create_(
                self.name, type_name
            )
            utl_core.Log.set_module_result_trace(
                'shader create',
                u'obj="{}"'.format(self.path)
            )


class Shader(mya_dcc_obj_abs.AbsMyaObj):
    PORT_CLASS = _mya_dcc_obj_utility.Port
    CONNECTION_CLASS = _mya_dcc_obj_utility.Connection
    #
    CATEGORY_DICT = {}
    for _category in ['shader', 'texture', 'light', 'utility']:
        _ = cmds.listNodeTypes(_category) or []
        for _i in _:
            CATEGORY_DICT[_i] = _category
    #
    def __init__(self, path):
        super(Shader, self).__init__(path)

    def set_create(self, obj_type):
        if self.get_is_exists() is False:
            name = self.name
            utl_core.Log.set_module_result_trace(
                'shader-obj-create',
                u'obj="{}"'.format(self.path)
            )
            category = self.CATEGORY_DICT.get(obj_type, 'utility')
            kwargs = dict(
                name=name,
                skipSelect=1
            )
            if category == 'shader':
                kwargs['asShader'] = 1
            elif category == 'texture':
                kwargs['asTexture'] = 1
            elif category == 'light':
                kwargs['asLight'] = 1
            elif category == 'utility':
                kwargs['asUtility'] = 1
            #
            result = cmds.shadingNode(
                obj_type, **kwargs
            )
            return result


class AndShader(Shader):
    CATEGORY_DICT = {}
    for _category in ['shader', 'texture', 'light', 'utility']:
        _ = cmds.listNodeTypes('rendernode/arnold/' + _category) or []
        for _i in _:
            CATEGORY_DICT[_i] = _category
    #
    def __init__(self, path):
        super(AndShader, self).__init__(path)

    def set_create(self, obj_type):
        if self.get_is_exists() is False:
            name = self.name
            utl_core.Log.set_module_result_trace(
                'shader-obj-create',
                u'obj="{}"'.format(self.path)
            )
            category = self.CATEGORY_DICT.get(obj_type, 'utility')
            kwargs = dict(
                name=name,
                skipSelect=1
            )
            if category == 'shader':
                kwargs['asShader'] = 1
            elif category == 'texture':
                kwargs['asTexture'] = 1
            elif category == 'light':
                kwargs['asLight'] = 1
            elif category == 'utility':
                kwargs['asUtility'] = 1
            # noinspection PyArgumentList
            result = cmds.shadingNode(
                obj_type, **kwargs
            )
            return result


class FileReference(mya_dcc_obj_abs.AbsMyaFileReferenceObj):
    PORT_CLASS = _mya_dcc_obj_utility.Port
    OS_FILE_CLASS = utl_dcc_objects.OsFile
    def __init__(self, path, file_path=None):
        super(FileReference, self).__init__(self._get_full_path_(path))
        self._set_file_reference_def_init_(file_path)


class TextureReference(mya_dcc_obj_abs.AbsMyaFileReferenceObj):
    PORT_CLASS = _mya_dcc_obj_utility.Port
    OS_FILE_CLASS = utl_dcc_objects.OsTexture
    def __init__(self, path, file_path=None):
        super(TextureReference, self).__init__(self._get_full_path_(path), file_path)

    def get_color_space(self):
        return self.get_port('colorSpace').get()

    def set_color_space(self, color_space):
        if self.get_color_space() != color_space:
            self.get_port('ignoreColorSpaceFileRules').set(True)
            self.get_port('colorSpace').set(color_space)
            utl_core.Log.set_module_result_trace(
                'color-space switch',
                'obj="{}", color-space="{}"'.format(self.path, color_space)
            )


class Alembic(mya_dcc_obj_abs.AbsMyaFileReferenceObj):
    PORT_CLASS = _mya_dcc_obj_utility.Port
    OS_FILE_CLASS = utl_dcc_objects.OsFile
    def __init__(self, path):
        super(Alembic, self).__init__(path)


class Set(mya_dcc_obj_abs.AbsMyaObj):
    PORT_CLASS = _mya_dcc_obj_utility.Port
    CONNECTION_CLASS = _mya_dcc_obj_utility.Connection
    def __init__(self, path):
        super(Set, self).__init__(path)

    def set_create(self, *args, **kwargs):
        if self.get_is_exists() is False:
            cmds.sets(name=self.path, empty=1)

    def set_element_add(self, path):
        cmds.sets(path, addElement=self.path, edit=1)
        utl_core.Log.set_module_result_trace(
            'set-element-add',
            'connection="{}" >> "{}"'.format(path, self.path)
        )

    def get_element_exists(self, path):
        pass

    def get_elements(self):
        return cmds.sets(self.path, query=1) or []

    def set_element_remove(self, path):
        cmds.sets(path, remove=self.path, edit=1)
        utl_core.Log.set_module_result_trace(
            'set-element-remove',
            'connection="{}" >> "{}"'.format(path, self.path)
        )

    def set_elements_clear(self):
        _ = self.get_elements()
        [self.set_element_remove(i) for i in _]

    def get_elements_match(self, pattern):
        return fnmatch.filter(
            [cmds.ls(i, long=1)[0] for i in self.get_elements()], pattern
        )
