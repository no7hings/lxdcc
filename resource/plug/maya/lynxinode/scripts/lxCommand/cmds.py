# encoding=utf-8
import math
#
import json
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.api.OpenMaya as OpenMaya
#
import lxCommand.core as lxcore
#
PATHSEP = '|'
#
C2M_TYPE_NAME = 'curveToMesh'
C2M_MESH_GROUP_NAME = 'c2m_mesh_grp_0'
#
M2S_TYPE_NAME = 'meshToSurface'
M2S_SURFACE_GROUP_NAME = 'm2s_surface_grp_0'
#
X2C_TYPE_NAME = 'xgenToCurve'
X2C_CURVE_GROUP_NAME = 'x2c_curve_grp_0'
#
CURVE_TYPE_NAME = 'nurbsCurve'
MESH_TYPE_NAME = 'mesh'
SURFACE_TYPE_NAME = 'nurbsSurface'
#
S2M_TYPE_NAME = 'surfaceToMesh'
S2M_MESH_GROUP_NAME = 's2m_mesh_grp_0'


def _set_undo_mark(method):
    def sub_method(*args, **kwargs):
        cmds.undoInfo(openChunk=1, undoName='test')
        _method = method(*args, **kwargs)
        cmds.undoInfo(closeChunk=1, undoName='test')
        return _method
    return sub_method


@_set_undo_mark
def set_mesh_create_by_curve_cmd(curve_shapes=None):
    cmds.loadPlugin('lxConvertNode', quiet=1)
    #
    nodes = []
    mesh_shapes = []
    if curve_shapes is None:
        curve_shapes = cmds.ls(type=CURVE_TYPE_NAME, selection=1, dagObjects=1, noIntermediate=1, long=1) or []
    #
    for curve_shape in curve_shapes:
        ts = cmds.listRelatives(curve_shape, parent=1, fullPath=1)
        transform = ts[0]
        ctomAttr = transform + '.' + C2M_TYPE_NAME
        atrs = {}
        if cmds.objExists(ctomAttr):
            attrData = cmds.getAttr(ctomAttr)
            atrs = json.loads(attrData)
        node, mesh_shape = set_c2m_create_cmd(curve_shape)
        #
        if atrs:
            set_c2m_atrs(node, mesh_shape, atrs)
        #
        nodes.append(node)
        mesh_shapes.append(mesh_shape)
    #
    if len(mesh_shapes) > 1:
        group = cmds.group(empty=1, name=C2M_MESH_GROUP_NAME)
        set_shapes_parent_to(mesh_shapes, group)
        #
        set_outliner_color(group, 1, .5, .25)
    return nodes, mesh_shapes


@_set_undo_mark
def set_surface_create_by_mesh_cmd():
    cmds.loadPlugin('lxConvertNode', quiet=1)
    #
    nodes = []
    surface_shapes = []
    mesh_shapes = cmds.ls(type=MESH_TYPE_NAME, selection=1, dagObjects=1, noIntermediate=1, long=1)
    for mesh_shape in mesh_shapes:
        node, surface = set_m2s_create_cmd(mesh_shape)
        nodes.append(node)
        surface_shapes.append(surface)
    #
    if len(surface_shapes) > 1:
        group = cmds.group(empty=1, name=M2S_SURFACE_GROUP_NAME)
        set_shapes_parent_to(surface_shapes, group)
        #
        set_outliner_color(group, 1, .5, .25)
    return mesh_shapes, nodes, surface_shapes


@_set_undo_mark
def set_curve_create_by_xgen_guide_cmd():
    cmds.loadPlugin('lxConvertNode', quiet=1)
    #
    nodes = []
    curve_shapes = []
    xgen_guide_shapes = cmds.ls(type='xgmSplineGuide', selection=1, dagObjects=1, noIntermediate=1, long=1) or []
    for xgen_guide_shape in xgen_guide_shapes:
        node, curve_shape = set_x2c_create_cmd(xgen_guide_shape)
        nodes.append(node)
        curve_shapes.append(curve_shape)
    #
    if len(curve_shapes) > 1:
        group = cmds.group(empty=1, name=X2C_CURVE_GROUP_NAME)
        set_shapes_parent_to(curve_shapes, group)
        #
        set_outliner_color(group, 1, .5, .25)
    return xgen_guide_shapes, nodes, curve_shapes


@_set_undo_mark
def set_mesh_create_by_xgen_guide_cmd_01():
    xgen_guide_shapes, x2c_nodes, curve_shapes = set_curve_create_by_xgen_guide_cmd()
    [set_hide_by_shape(i) for i in curve_shapes]
    c2m_nodes, mesh_shapes = set_mesh_create_by_curve_cmd(curve_shapes)
    for seq, c2m_node in enumerate(c2m_nodes):
        xgen_guide_shape = xgen_guide_shapes[seq]
        width = cmds.getAttr(xgen_guide_shape + '.width')
        cmds.setAttr(c2m_node + '.width', width*2)
        input_mesh_shape = get_xgen_guide_input_mesh_shape(xgen_guide_shape)
        if input_mesh_shape is not None:
            if not cmds.connectionInfo(c2m_node + '.inputMesh', isExactDestination=1):
                cmds.connectAttr(
                    input_mesh_shape + '.worldMesh[0]', c2m_node + '.inputMesh'
                )


@_set_undo_mark
def set_mesh_create_by_surface_cmd(surface_shapes=None):
    cmds.loadPlugin('lxConvertNode', quiet=1)
    #
    mesh_shapes = []
    if surface_shapes is None:
        surface_shapes = cmds.ls(type=SURFACE_TYPE_NAME, selection=1, dagObjects=1, noIntermediate=1, long=1)
    for surface in surface_shapes:
        node, mesh_shape = set_s2m_create_cmd(surface)
        mesh_shapes.append(mesh_shape)
    #
    if len(mesh_shapes) > 1:
        group = cmds.group(empty=1, name=S2M_MESH_GROUP_NAME)
        set_shapes_parent_to(mesh_shapes, group)
    return mesh_shapes


@_set_undo_mark
def set_mesh_create_by_xgen_guide_cmd_02():
    xgen_guide_shapes, x2c_nodes, curve_shapes = set_curve_create_by_xgen_guide_cmd()
    [set_hide_by_shape(i) for i in curve_shapes]
    if curve_shapes:
        input_name = get_transform_name_by_shape(curve_shapes[0])
        #
        name = '{}_{}_0'.format(input_name, SURFACE_TYPE_NAME)
        surface_transform, _ = cmds.loft(*curve_shapes, name=name, constructionHistory=True, range=True, autoReverse=True)
        set_transform_hide(surface_transform)
        set_mesh_create_by_surface_cmd([get_shape_name_by_transform(surface_transform)])


@_set_undo_mark
def set_mesh_create_by_mesh_cmd():
    mesh_shapes, m2s_nodes, surface_shapes = set_surface_create_by_mesh_cmd()
    [set_hide_by_shape(i) for i in surface_shapes]
    if surface_shapes:
        set_mesh_create_by_surface_cmd(surface_shapes)


@_set_undo_mark
def set_mesh_morph_by_uv_map_cmd_01():
    mesh_shapes = cmds.ls(type=MESH_TYPE_NAME, selection=1, dagObjects=1, noIntermediate=1, long=1)
    for mesh_shape in mesh_shapes:
        lxcore.MeshOpt(mesh_shape).set_morph_by_uv_map(
            keep_face_vertices=True
        )


@_set_undo_mark
def set_mesh_morph_by_uv_map_cmd_02():
    mesh_shapes = cmds.ls(type=MESH_TYPE_NAME, selection=1, dagObjects=1, noIntermediate=1, long=1)
    for mesh_shape in mesh_shapes:
        lxcore.MeshOpt(mesh_shape).set_morph_by_uv_map(
            keep_face_vertices=False
        )


def get_xgen_guide_input_mesh_shape(xgen_guide_shape):
    _0s = cmds.listConnections(
        xgen_guide_shape + '.toMakeGuide',
        destination=0, source=1, shapes=1
    )
    if _0s:
        _0 = _0s[0]
        _1s = cmds.listConnections(
            _0 + '.geomHitIn',
            destination=0, source=1, shapes=1
        )
        if _1s:
            _1 = _1s[0]
            _2s = cmds.listConnections(
                _1 + '.geometry',
                destination=0, source=1, shapes=1
            )
            if _2s:
                return _2s[0]


def set_outliner_color(path, r, g, b):
    cmds.setAttr(path + '.useOutlinerColor', 1)
    cmds.setAttr(path + '.outlinerColor', r, g, b)


def get_real_angle(angle):
    r = angle % 180
    if r > 0:
        if r > 90:
            angle_ = r - 180
        else:
            angle_ = r
    else:
        angle_ = r
    return angle_


def set_c2m_atrs(node, mesh_shape, atrs):
    ribbonMesh = atrs['ribbonMesh']
    orientationAttr = ribbonMesh + '.' + 'orientation'
    orientation = cmds.getAttr(orientationAttr)
    cmds.setAttr(orientationAttr, 1)
    differAngle = getDifferAngle(ribbonMesh, mesh_shape)
    cmds.setAttr(orientationAttr, orientation)
    for k, v in atrs.items():
        attr = node + '.' + k
        if cmds.objExists(attr):
            # Fix Spin
            if k == 'spin':
                r = (v + differAngle) % 180
                if r > 0:
                    if r > 90:
                        v_ = r - 180
                    else:
                        v_ = r
                else:
                    v_ = r
                #
                v = v_
            #
            cmds.setAttr(attr, v)


def set_s2m_create_cmd(surface_shape):
    node = set_s2m_node_create(surface_shape)
    mesh_shape = set_s2m_mesh_create(node, surface_shape)
    return node, mesh_shape


def set_s2m_node_create(surface_shape):
    _ = cmds.listConnections(surface_shape, destination=1, source=0, type=S2M_TYPE_NAME, shapes=1)
    if _:
        return _[0]
    #
    node = cmds.createNode(S2M_TYPE_NAME, skipSelect=1)
    set_m2s_node_init(node)
    cmds.connectAttr(surface_shape + '.worldSpace[0]', node + '.inputSurface')
    return node


def set_s2m_mesh_create(node, surface_shape):
    _ = cmds.listConnections(node, destination=1, source=0, type=MESH_TYPE_NAME, shapes=1)
    if not _:
        input_name = get_transform_name_by_shape(surface_shape)
        #
        name = '{}_{}_0'.format(input_name, MESH_TYPE_NAME)
        #
        mesh_shape = set_geometry_create(MESH_TYPE_NAME, name)
        cmds.connectAttr(node + '.outputMesh', mesh_shape + '.inMesh')
    else:
        mesh_shape = _[0]
    #
    add_to_model_panel(mesh_shape)
    return mesh_shape


def set_m2s_create_cmd(mesh_shape):
    node = set_m2s_node_create(mesh_shape)
    surface = set_m2s_surface_create(node, mesh_shape)
    return node, surface


def set_m2s_node_create(mesh_shape):
    _ = cmds.listConnections(mesh_shape, destination=1, source=0, type=M2S_TYPE_NAME, shapes=1)
    if _:
        return _[0]
    #
    node = cmds.createNode(M2S_TYPE_NAME, skipSelect=1)
    set_m2s_node_init(node)
    cmds.connectAttr(mesh_shape + '.worldMesh[0]', node + '.inputMesh')
    return node


def set_m2s_surface_create(node, mesh_shape):
    _ = cmds.listConnections(node, destination=1, source=0, type=SURFACE_TYPE_NAME, shapes=1)
    if not _:
        input_name = get_transform_name_by_shape(mesh_shape)
        #
        name = '{}_{}_0'.format(input_name, SURFACE_TYPE_NAME)
        #
        surface_shape = set_geometry_create(SURFACE_TYPE_NAME, name)
        cmds.connectAttr(node + '.outputSurface', surface_shape + '.create')
        #
        set_outliner_color(surface_shape, .25, 1, .5)
    else:
        surface_shape = _[0]
    #
    add_to_model_panel(surface_shape)
    return surface_shape


def set_x2c_create_cmd(xgen_guide_shape):
    node = set_x2c_node_create(xgen_guide_shape)
    curve_shape = set_x2c_curve_create(node, xgen_guide_shape)
    return node, curve_shape


def set_x2c_node_create(xgen_guide_shape):
    _ = cmds.listConnections(xgen_guide_shape, destination=1, source=0, type=X2C_TYPE_NAME, shapes=1)
    if _:
        return _[0]
    #
    input_name = get_transform_name_by_shape(xgen_guide_shape)
    #
    name = '{}_{}_0'.format(input_name, X2C_TYPE_NAME)
    #
    node = cmds.createNode(X2C_TYPE_NAME, name=name, skipSelect=1)
    set_x2c_node_init(node)
    cmds.connectAttr(xgen_guide_shape + '.worldMesh[0]', node + '.inputXgenGuide')
    return node


def set_x2c_curve_create(node, xgen_guide_shape):
    _ = cmds.listConnections(node, destination=1, source=0, type=CURVE_TYPE_NAME, shapes=1)
    if _:
        curve_shape = _[0]
    else:
        input_name = get_transform_name_by_shape(xgen_guide_shape)
        #
        name = '{}_{}_0'.format(input_name, CURVE_TYPE_NAME)
        #
        curve_shape = set_geometry_create(CURVE_TYPE_NAME, name)
        cmds.connectAttr(node + '.outputCurve', curve_shape + '.create')
        #
        set_outliner_color(curve_shape, .25, 1, .5)
    return curve_shape


def set_c2m_create_cmd(curve_shape):
    node = set_c2m_node_create(curve_shape)
    mesh_shape = set_c2m_mesh_create(node, curve_shape)
    return node, mesh_shape


def set_c2m_node_create(curve_shape):
    _ = cmds.listConnections(curve_shape, destination=1, source=0, type=C2M_TYPE_NAME, shapes=1)
    if _:
        return _[0]
    #
    input_name = get_transform_name_by_shape(curve_shape)
    #
    name = '{}_{}_0'.format(input_name, C2M_TYPE_NAME)
    #
    node = cmds.createNode(C2M_TYPE_NAME, name=name, skipSelect=1)
    set_c2m_node_init(node)
    cmds.connectAttr(curve_shape + '.worldSpace[0]', node + '.inputCurve')
    return node


def set_c2m_mesh_create(node, curve_shape):
    _ = cmds.listConnections(node, destination=1, source=0, type=MESH_TYPE_NAME, shapes=1)
    if _:
        mesh_shape = _[0]
    else:
        input_name = get_transform_name_by_shape(curve_shape)
        #
        name = '{}_{}_0'.format(input_name, MESH_TYPE_NAME)
        #
        mesh_shape = set_geometry_create(MESH_TYPE_NAME, name)
        cmds.connectAttr(node + '.outputMesh', mesh_shape + '.inMesh')
        #
        set_outliner_color(mesh_shape, .25, 1, .5)
    #
    add_to_model_panel(mesh_shape)
    return mesh_shape


def get_c2m_curve(node):
    existsCurves = cmds.listConnections(node, destination=0, source=1, type=CURVE_TYPE_NAME, shapes=1)
    if existsCurves:
        return existsCurves[0]


def get_m2s_mesh(node):
    exists_meshes = cmds.listConnections(node, destination=0, source=1, type=MESH_TYPE_NAME, shapes=1)
    if exists_meshes:
        return exists_meshes[0]


def set_hide_by_shape(path):
    ts = cmds.listRelatives(path, parent=1, fullPath=1)
    transform = ts[0]
    cmds.setAttr(transform + '.visibility', 0)


def get_shape_name_by_transform(path):
    if cmds.objExists(path):
        if cmds.nodeType(path) == 'transform':
            shape_names = cmds.listRelatives(path, children=1, shapes=1, noIntermediate=1, fullPath=0)
            if shape_names:
                return shape_names[0]
        return path


def get_transform(path):
    _ = cmds.listRelatives(
        path, parent=1, fullPath=1
    )
    if _:
        return _[0]


def get_transform_name_by_shape(path):
    _ = cmds.listRelatives(
        path, parent=1, fullPath=1
    )
    if _:
        return _[0].split(PATHSEP)[-1]


def get_transform_path_by_shape(path):
    _ = cmds.listRelatives(
        path, parent=1, fullPath=1
    )
    if _:
        return _[0]


def set_shapes_parent_to(shapes, group):
    cmds.parent(
        [get_transform_path_by_shape(i) for i in shapes], group
    )


def set_transform_hide(path):
    cmds.setAttr(path + '.visibility', 0)


def set_c2m_modify_reset(node):
    resetDic = {
        'spin': 0,
        'twist': 0,
        'taper': 1,
        'arch': 0,
        'startIndex': 0,
        'endIndex': 1
    }
    for k, v in resetDic.items():
        attr = node + '.' + k
        cmds.setAttr(attr, v)


def add_to_model_panel(path):
    cmds.isolateSelect('modelPanel4', addDagObject=path)


def set_c2m_node_init(node):
    cmds.setAttr(node + '.widthExtra[0].widthExtra_Position', 0)
    cmds.setAttr(node + '.widthExtra[0].widthExtra_FloatValue', 0.5)
    cmds.setAttr(node + '.widthExtra[1].widthExtra_Position', 1)
    cmds.setAttr(node + '.widthExtra[1].widthExtra_FloatValue', 0.5)
    #
    cmds.setAttr(node + '.spinExtra[0].spinExtra_Position', 0)
    cmds.setAttr(node + '.spinExtra[0].spinExtra_FloatValue', .5)
    cmds.setAttr(node + '.spinExtra[1].spinExtra_Position', 1)
    cmds.setAttr(node + '.spinExtra[1].spinExtra_FloatValue', .5)
    #
    cmds.setAttr(node + '.archExtra[0].archExtra_Position', 0)
    cmds.setAttr(node + '.archExtra[0].archExtra_FloatValue', .5)
    cmds.setAttr(node + '.archExtra[1].archExtra_Position', 1)
    cmds.setAttr(node + '.archExtra[1].archExtra_FloatValue', .5)


def set_m2s_node_init(node):
    pass


def set_x2c_node_init(node):
    pass


def set_mesh_create_by_bonus_curve():
    group = setCopyBonusCurve()
    if group:
        cmds.select(group)
        set_mesh_create_by_curve_cmd()


def set_geometry_create(geometry_type, transform_name):
    t = cmds.createNode('transform', name=transform_name, skipSelect=1)
    s = cmds.createNode(geometry_type, parent=t, name=t + 'Shape', skipSelect=1)
    if geometry_type in [MESH_TYPE_NAME, SURFACE_TYPE_NAME]:
        cmds.sets(s, forceElement='initialShadingGroup')
    return s


#
def getDifferAngle(mesh1, mesh2):
    def toM2Vector(mesh_shape, vertexId1, vertexId2):
        mMeshPath = OpenMaya.MGlobal.getSelectionListByName(mesh_shape).getDagPath(0)
        mMesh = OpenMaya.MFnMesh(mMeshPath)
        #
        p1, p2 = mMesh.getPoint(vertexId1, space=4), mMesh.getPoint(vertexId2, space=4)
        mVector = OpenMaya.MVector()
        mVector.x, mVector.y, mVector.z = (p2.x - p1.x), (p2.y - p1.y), (p2.z - p1.z)
        return mVector
    #
    iVector1 = toM2Vector(mesh1, 0, 1)
    iVector2 = toM2Vector(mesh2, 0, 1)
    #
    axisAngle = iVector2.rotateTo(iVector1).asAxisAngle()
    x = iVector2.x
    a = math.degrees(axisAngle[1])
    if x < 0:
        return -a
    elif x >= 0:
        return a


#
def getBonusCurveDic():
    attrNames = [
        'width',
        'orientation',
        'taper',
        'twist',
        'lengthDivisions'
    ]
    #
    dic = {}
    ribbonMeshes = []
    selCurves = cmds.ls(type=CURVE_TYPE_NAME, selection=1, dagObjects=1)
    if selCurves:
        for c in selCurves:
            t = cmds.listRelatives(c, parent=1, fullPath=1)
            css = cmds.listConnections(t, destination=1, source=0, type='orientConstraint', shapes=1)
            if css:
                for cs in css:
                    ms = cmds.listConnections(cs, destination=1, source=0, type='transform', shapes=1)
                    if ms:
                        ribbonMesh = ms[0]
                        attrDatas = []
                        for a in attrNames:
                            attr = ribbonMesh + '.' + a
                            attrData = cmds.getAttr(attr)
                            attrDatas.append(attrData)
                        #
                        attrDatas.append(ribbonMesh)
                        #
                        if not ribbonMesh in ribbonMeshes:
                            dic.setdefault(c, []).append(attrDatas)
                        #
                        ribbonMeshes.append(ribbonMesh)
    #
    return dic


#
def setCopyBonusCurve():
    attrNames = [
        'width',
        'spin',
        'taper',
        'twist',
        'vDivision',
        'ribbonMesh'
    ]
    #
    dic = getBonusCurveDic()
    copyCurves = []
    if dic:
        for k, v in dic.items():
            for seq, i in enumerate(v):
                ts = cmds.listRelatives(k, parent=1, fullPath=1)
                transform = ts[0]
                copyPath = PATHSEP.join(transform.split(PATHSEP)[:-1])
                copyCurveName = transform.split(PATHSEP)[-1] + '_copy_%s' % seq
                copyCurvePath = copyPath + PATHSEP + copyCurveName
                if not cmds.objExists(copyCurveName):
                    cmds.duplicate(transform, name=copyCurveName, returnRootsOnly=1)
                    #
                    cmds.addAttr(copyCurvePath, longName=C2M_TYPE_NAME, dataType='string')
                    #
                    atrs = {}
                    for subSeq, j in enumerate(i):
                        atrs[attrNames[subSeq]] = j
                    #
                    cmds.setAttr(copyCurvePath + '.' + C2M_TYPE_NAME, json.dumps(atrs), type='string')
                #
                copyCurves.append(copyCurvePath)
    #
    if copyCurves:
        group = cmds.group(empty=1, name='ctom_curve_copy_grp_0')
        cmds.parent(copyCurves, group)
        return group
