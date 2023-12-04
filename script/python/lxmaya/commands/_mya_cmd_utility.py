# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

import lxbasic.core as bsc_core

from lxutil import utl_core


def get_shape_path(path):
    if cmds.objExists(path):
        if cmds.nodeType(path) == 'transform':
            shape_paths = cmds.listRelatives(path, children=1, shapes=1, noIntermediate=1, fullPath=1)
            if shape_paths:
                return shape_paths[0]
        return path


def get_selected_paths(shape=0):
    lis = []
    data = cmds.ls(selection=1, long=1)
    if data:
        if shape:
            lis = [get_shape_path(i) for i in data]
        else:
            lis = data
    return lis


def set_node_move(path, x, y, z):
    cmds.move(x, y, z, path, relative=1)


def set_selected_to_origin(mode=0):
    paths = cmds.ls(selection=1, long=1)
    if paths:
        bbox = cmds.polyEvaluate(paths, boundingBox=1)
        (x, _x), (y, _y), (z, _z) = bbox
        cx = (x + _x) / 2
        cy = (y + _y) / 2
        cz = (z + _z) / 2
        for i in paths:
            if mode == 0:
                set_node_move(i, -cx, -cy, -cz)
            elif mode == 1:
                set_node_move(i, -cx, -y, -cz)


def set_unknown_nodes_clear():
    for unknown_node in cmds.ls(type='unknown') or []:
        if cmds.objExists(unknown_node) is True:
            cmds.lockNode(unknown_node, lock=0)
            cmds.delete(unknown_node)
            bsc_core.Log.trace_method_result(
                'scene-clear',
                u'unknown-node: "{}"'.format(unknown_node)
            )


def set_unknown_plug_ins_clear():
    for unknown_plug_in in cmds.unknownPlugin(query=1, list=1) or []:
        cmds.unknownPlugin(unknown_plug_in, remove=1)
        bsc_core.Log.trace_method_result(
            'scene-clear',
            u'unknown-plug: "{}"'.format(unknown_plug_in)
        )


def set_unused_namespaces_clear():
    def get_obj_parent_path_fnc_(path_):
        parent = cmds.listRelatives(path_, parent=1, fullPath=1)
        if parent:
            return parent[0]
    #
    def get_namespaces_fnc_():
        lis = []
        _exclude_namespace = ['UI', 'shared']
        _ = cmds.namespaceInfo(recurse=1, listOnlyNamespaces=1)
        if _:
            _.reverse()
            for _namespace in _:
                if not _namespace in _exclude_namespace:
                    _obj_paths = cmds.namespaceInfo(_namespace, listOnlyDependencyNodes=1, dagPath=1)
                    _is_assembly_reference = False
                    if _obj_paths:
                        for _obj_path in _obj_paths:
                            _obj_parent_path = get_obj_parent_path_fnc_(_obj_path)
                            if _obj_parent_path is not None:
                                if cmds.nodeType(_obj_parent_path) == 'assemblyReference':
                                    _is_assembly_reference = True
                                    break
                    #
                    if _is_assembly_reference is False:
                        lis.append(_namespace)
        return lis
    #
    def set_remove_fnc(namespace_):
        cmds.namespace(removeNamespace=namespace_)
        bsc_core.Log.trace_method_result(
            'scene-clear',
            u'unused-namespace: "{}"'.format(namespace_)
        )

    def fnc_1_():
        _namespaces = get_namespaces_fnc_()
        if _namespaces:
            for _namespace in _namespaces:
                cmds.namespace(setNamespace=_namespace)
                child_namespaces = cmds.namespaceInfo(recurse=1, listOnlyNamespaces=1)
                _obj_paths = cmds.namespaceInfo(listOnlyDependencyNodes=1, dagPath=1)
                #
                _namespace_parent = cmds.namespaceInfo(parent=1)
                cmds.namespace(setNamespace=':')
                if not child_namespaces:
                    if not _obj_paths:
                        set_remove_fnc(_namespace)
                    else:
                        _is_reference = False
                        #
                        for _obj_path in _obj_paths:
                            if cmds.referenceQuery(_obj_path, isNodeReferenced=1):
                                _is_reference = True
                                break
                        #
                        if _is_reference is False:
                            cmds.namespace(force=1, moveNamespace=(_namespace, _namespace_parent))
                            set_remove_fnc(_namespace)

    fnc_1_()


def set_unused_windows_clear():
    for panel in cmds.getPanel(visiblePanels=1) or []:
        if panel != 'modelPanel4':
            if cmds.panel(panel, query=1, exists=1):
                window = panel + 'Window'
                if cmds.window(window, query=1, exists=1):
                    cmds.deleteUI(window, window=1)
                    bsc_core.Log.trace_method_result(
                        'scene-clear',
                        u'unused-window: "{}"'.format(window)
                    )


def set_unload_references_clear():
    for reference_node in cmds.ls(type='reference'):
        # noinspection PyBroadException
        try:
            is_loaded = cmds.referenceQuery(reference_node, isLoaded=1)
        except:
            is_loaded = False

        if is_loaded is False:
            cmds.lockNode(reference_node, lock=0)
            cmds.delete(reference_node)
            bsc_core.Log.trace_method_result(
                'scene-clear',
                u'unload-reference-node: "{}"'.format(reference_node)
            )
