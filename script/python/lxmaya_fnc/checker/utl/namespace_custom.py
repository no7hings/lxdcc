# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

from lxutil import utl_core

from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_scene


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # empty
    def _check_method_0(self, *args):
        obj, check_index = args
        #
        is_error = not obj.get_objs()
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs
    # noinspection PyMethodMayBeStatic
    def _repair_method_0(self, obj):
        def get_parent_path_fnc_(path_):
            parent = cmds.listRelatives(path_, parent=1, fullPath=1)
            if parent:
                return parent[0]

        def get_namespaces_fnc_():
            lis = []
            except_namespace = ['UI', 'shared']
            _ = cmds.namespaceInfo(recurse=1, listOnlyNamespaces=1)
            if _:
                _.reverse()
                for _namespace in _:
                    if not _namespace in except_namespace:
                        _is_assembly = False
                        _paths = cmds.namespaceInfo(_namespace, listOnlyDependencyNodes=1, dagPath=1)
                        if _paths:
                            for _path in _paths:
                                _parent_path = get_parent_path_fnc_(_path)
                                if _parent_path:
                                    if cmds.nodeType(_parent_path) == 'assemblyReference':
                                        _is_assembly = True
                                        break
                        #
                        if not _is_assembly:
                            lis.append(_namespace)
            return lis

        #
        namespaces = get_namespaces_fnc_()
        if namespaces:
            for namespace in namespaces:
                cmds.namespace(setNamespace=namespace)
                child_namespaces = cmds.namespaceInfo(recurse=1, listOnlyNamespaces=1)
                nodes = cmds.namespaceInfo(listOnlyDependencyNodes=1, dagPath=1)
                #
                parent_namespace = cmds.namespaceInfo(parent=1)
                cmds.namespace(setNamespace=':')
                if not child_namespaces:
                    if not nodes:
                        cmds.namespace(removeNamespace=namespace)
                    else:
                        is_clear = False
                        #
                        for node in nodes:
                            if cmds.referenceQuery(node, isNodeReferenced=1):
                                is_clear = True
                                break
                        #
                        if not is_clear:
                            cmds.namespace(force=1, moveNamespace=(namespace, parent_namespace))
                            cmds.namespace(removeNamespace=namespace)
    # not from reference
    def _check_method_1(self, *args):
        obj, check_index = args
        #
        is_error = obj.get_is_reference() is False
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs
    # noinspection PyMethodMayBeStatic
    def _repair_method_1(self, *args):
        self._repair_method_0(*args)

    def set_check_run(self):
        self.set_restore()
        namespaces = _mya_dcc_obj_scene.Scene().get_namespaces()
        self._set_objs_check_(namespaces)
