# encoding=utf-8
import math
#
import json

from itertools import product

import sys
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.api.OpenMaya as om2

import lxCommand.cmds as lxcmds


def trace_error(text):
    sys.stderr.write(text+'\n')


def trace(text):
    sys.stdout.write(text+'\n')


def set_undo_mark(method):
    def sub_method(*args, **kwargs):
        cmds.undoInfo(openChunk=1, undoName='test')
        _method = method(*args, **kwargs)
        cmds.undoInfo(closeChunk=1, undoName='test')
        return _method
    return sub_method


class MtdBase(object):
    SELECTION_WINDOW_NAME = 'c2me_for_selection'
    CONTROL_WINDOW_NAME = 'c2me_window'
    CONTROL_WINDOW_SIZE = 500, 720
    CAMERA_NAME = 'c2me_camera'
    #
    PLUGIN_NAME = 'lxConvertNodeExtra'
    #
    C2ME_TYPE_NAME = 'curveToMeshExtra'
    C2ME_NODE_GROUP_NAME = 'c2me_node_grp_0'
    C2ME_CONTAINER_GROUP_NAME = 'c2me_container_grp_0'
    C2ME_CURVE_GROUP_NAME = 'c2me_curve_grp_0'
    C2ME_MESH_GROUP_NAME = 'c2me_mesh_grp_0'
    #
    CURVE_TYPE_NAME = 'nurbsCurve'
    MESH_TYPE_NAME = 'mesh'
    SURFACE_TYPE_NAME = 'nurbsSurface'
    #
    PATHSEP = '|'
    #
    INPUT_U_BASE_CURVE_POINTS = [
        (1.0, 0.0, 0.0),
        (0.0, 0.0, -1.0),
        (-1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0),
        (1.0, 0.0, 0.0),
        (0.0, 0.0, -1.0)
    ]
    INPUT_U_BASE_CURVE_FORM = 3
    INPUT_U_BASE_CURVE_DEGREE = 2
    INPUT_U_BASE_CURVE_KNOTS = [-1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    @classmethod
    def get_om2_dag_path(cls, path):
        return om2.MGlobal.getSelectionListByName(path).getDagPath(0)
    @classmethod
    def get_om2_dag_obj(cls, path):
        return om2.MFnDagNode(cls.get_om2_dag_path(path)).object()
    @classmethod
    def _get_shape_transform_path_(cls, path):
        _ = cmds.listRelatives(
            path, parent=1, fullPath=1
        )
        if _:
            return _[0]
    @classmethod
    def _get_shape_transform_name_(cls, path):
        _ = cmds.listRelatives(
            path, parent=1, fullPath=1
        )
        if _:
            return _[0].split(cls.PATHSEP)[-1]
    @classmethod
    def _get_name_(cls, path):
        return path.split(cls.PATHSEP)[-1]
    @classmethod
    def _parent_shapes_parent_to_(cls, shapes, group):
        cmds.parent(
            [cls._get_shape_transform_path_(i) for i in shapes], group
        )
    @classmethod
    def _parent_transform_to_(cls, transforms, group):
        cmds.parent(
            transforms, group
        )
    @classmethod
    def _add_to_model_panel_(cls, path):
        cmds.isolateSelect('modelPanel4', addDagObject=path)
    @classmethod
    def _set_outliner_color_(cls, path, r, g, b):
        cmds.setAttr(path + '.useOutlinerColor', 1)
        cmds.setAttr(path + '.outlinerColor', r, g, b)
    @classmethod
    def _create_shape_(cls, type_name, transform_name):
        t = cmds.createNode('transform', name=transform_name, skipSelect=1)
        s = cmds.createNode(type_name, parent=t, name=t + 'Shape', skipSelect=1)
        if type_name in [cls.MESH_TYPE_NAME, cls.SURFACE_TYPE_NAME]:
            cmds.sets(s, forceElement='initialShadingGroup')
        return t, s
    @classmethod
    def _create_curve_(cls, transform_name):
        t = cmds.createNode('transform', name=transform_name, skipSelect=1)
        om2_curve = om2.MFnNurbsCurve()
        om2_curve.create(
            cls.INPUT_U_BASE_CURVE_POINTS,
            cls.INPUT_U_BASE_CURVE_KNOTS, cls.INPUT_U_BASE_CURVE_DEGREE, cls.INPUT_U_BASE_CURVE_FORM,
            False,
            True,
            parent=cls.get_om2_dag_obj(t)
        )
        om2_curve.setName(t+'Shape')
        return t, t+'Shape'
    @classmethod
    def _append_annotation_(cls, shape_path):
        t_p = cls._get_shape_transform_path_(shape_path)
        t = cls._get_shape_transform_name_(shape_path)
        s = cmds.createNode('annotationShape', parent=t_p, name=t + 'annotationShape', skipSelect=1)
        return s
    @classmethod
    def _append_annotation__(cls, transform_path):
        name = cls._get_name_(transform_path)
        s = cmds.createNode('annotationShape', parent=transform_path, name=name + 'annotationShape', skipSelect=1)
        return s
    @classmethod
    def _lock_transformations_(cls, path):
        [cmds.setAttr(path+i+j, lock=True) for i, j in product(['.translate', '.rotate', '.scale'], ['X', 'Y', 'Z'])]
        cmds.setAttr(path + '.visibility', lock=0)
    @classmethod
    def _set_attributes_(cls, path, attributes):
        for i_args in attributes:
            i_k, i_v = i_args[:2]
            i_atr = '{}.{}'.format(path, i_k)
            if len(i_args) == 2:
                i_kwargs = {}
            elif len(i_args) == 3:
                i_kwargs = i_args[2]
            else:
                raise RuntimeError()
            #
            is_locked = cmds.getAttr(i_atr, lock=1)
            if is_locked is True:
                cmds.setAttr(i_atr, lock=0)
            cmds.setAttr(i_atr, i_v, **i_kwargs)
            if is_locked is True:
                cmds.setAttr(i_atr, lock=1)
    @classmethod
    def _hide_by_shape_(cls, path):
        ts = cmds.listRelatives(path, parent=1, fullPath=1)
        transform = ts[0]
        cmds.setAttr(transform + '.visibility', 0)
        cls._set_attributes_(
            transform, [('hiddenInOutliner', 1), ('visibility', 0)]
        )


class C2meNode(MtdBase):
    CONTROL_SPACING = 4
    def __init__(self, node_shape):
        self._node_shape = node_shape
    @classmethod
    @set_undo_mark
    def create(cls, input_v_base_curve_shape, control_count=2, radius=.1):
        if not cls.get_exists_node(input_v_base_curve_shape):
            n = cls.create_node(input_v_base_curve_shape, radius=radius)
            n.create_control_container()
            n.create_controls(control_count)
            output_mesh_shape = n.create_output_mesh()
            return n._node_shape, output_mesh_shape
    @classmethod
    def get_exists_node(cls, input_v_base_curve_shape):
        _ = cmds.listConnections('{}.worldSpace[0]'.format(input_v_base_curve_shape), destination=1, source=0) or []
        if _:
            return _[0]
    @classmethod
    def create_node(cls, input_v_base_curve_shape, radius=.1):
        _ = cmds.listConnections(input_v_base_curve_shape, destination=1, source=0, type=cls.C2ME_TYPE_NAME, shapes=1)
        if _:
            return _[0]
        #
        input_name = cls._get_shape_transform_name_(input_v_base_curve_shape)
        #
        transform_name = '{}_c2me_0'.format(input_name)
        node_transform, node_shape = cls._create_shape_(cls.C2ME_TYPE_NAME, transform_name)
        cls._lock_transformations_(node_transform)
        cls._set_attributes_(node_shape, [('radius', radius), ('lynxiScale', .5)])
        cls._set_outliner_color_(node_transform, 1, .5, 1)
        cls._set_outliner_color_(node_shape, 1, .5, 1)
        #
        cmds.connectAttr(input_v_base_curve_shape + '.worldSpace[0]', node_shape + '.inputVBaseCurve')
        cls._add_to_model_panel_(node_shape)
        return cls(node_shape)

    def add_to_container(self, nodes):
        c_c = self.get_exists_control_container()
        if c_c:
            self._parent_transform_to_(nodes, c_c)

    def get_exists_control_container(self):
        _ = cmds.listConnections('{}.inputControlContainer'.format(self._node_shape), destination=0, source=1) or []
        if _:
            return _[0]

    def get_exists_control_transforms(self):
        return cmds.listConnections('{}.inputUBaseCurves'.format(self._node_shape), destination=0, source=1) or []

    def get_exists_control_shapes(self):
        return cmds.listConnections('{}.inputUBaseCurves'.format(self._node_shape), destination=0, source=1, shapes=1) or []

    def create_control_container(self):
        _ = cmds.listConnections('{}.inputControlContainer'.format(self._node_shape), destination=0, source=1) or []
        if _:
            return _[0]
        #
        input_name = self._get_shape_transform_name_(self._node_shape)
        #
        transform_name = '{}_input_container_0'.format(input_name)
        #
        n = cmds.createNode('transform', name=transform_name, skipSelect=1)
        cmds.connectAttr(n + '.message', self._node_shape + '.inputControlContainer')
        self._set_attributes_(
            n, [('translateX', 100000), ('translateY', 100000), ('translateZ', 100000), ('blackBox', 1), ('hiddenInOutliner', 1)]
        )
        self._lock_transformations_(n)
        self._parent_transform_to_(n, self._get_shape_transform_path_(self._node_shape))
        return n

    def create_controls(self, count=1):
        c_c = self.get_exists_control_container()
        if c_c:
            _ = cmds.listConnections('{}.inputUBaseCurves'.format(self._node_shape), destination=0, source=1) or []
            if _:
                return _[0]
            #
            for i in range(count):
                self.create_control_at(i)

    def create_control_at(self, index):
        c_c = self.get_exists_control_container()
        direction = cmds.getAttr(
            '{}.lynxiControlDirection'.format(self._node_shape)
        )
        if c_c:
            name = self._get_shape_transform_name_(self._node_shape)
            curve_transform, curve_shape = self._create_curve_('{}_input_u_base_curve_{}'.format(name, str(index)))
            self.create_control_info(curve_transform, index)
            self.layout_control(curve_transform, index, direction)
            self.setup_control(curve_transform, curve_shape)
            cmds.connectAttr(curve_shape + '.worldSpace[0]'.format(index), self._node_shape + '.inputUBaseCurves[{}]'.format(index))
            #
            self.add_to_container(
                [
                    curve_transform,
                ]
            )

    def append_one_control(self):
        for i in range(10):
            i_atr = '{}.inputUBaseCurves[{}]'.format(self._node_shape, i)
            _ = cmds.listConnections(i_atr, destination=0, source=1, shapes=1) or []
            if not _:
                self.create_control_at(i)
                break

    def layout_all_controls(self, direction):
        cs = self.get_exists_control_transforms()
        self._set_attributes_(
            self._node_shape, [('lynxiControlDirection', direction)]
        )
        for i_index, i in enumerate(cs):
            self.layout_control(i, i_index, direction)

    def layout_control(self, transform_path, index, direction=None):
        if direction is None:
            direction = cmds.getAttr(
                '{}.lynxiControlDirection'.format(self._node_shape)
            )
        if direction == 0:
            self._set_attributes_(
                transform_path, [('translateX', 0), ('translateX', index * self.CONTROL_SPACING), ('translateZ', 0)]
            )
        elif direction == 1:
            self._set_attributes_(
                transform_path, [('translateX', 0), ('translateX', 0), ('translateZ', -index * self.CONTROL_SPACING)]
            )

        self.set_control_info(transform_path, index)

    def create_output_mesh(self):
        _ = cmds.listConnections('{}.outputMesh'.format(self._node_shape), destination=0, source=1) or []
        if _:
            return _[0]
        #
        input_name = self._get_shape_transform_name_(self._node_shape)
        #
        transform_name = '{}_output_mesh_0'.format(input_name)
        #
        mesh_transform, mesh_shape = self._create_shape_(self.MESH_TYPE_NAME, transform_name)
        cmds.connectAttr(self._node_shape + '.outputMesh', mesh_shape + '.inMesh')
        #
        # self._set_outliner_color_(mesh_shape, .25, 1, .5)
        self._add_to_model_panel_(mesh_shape)
        return mesh_shape

    def switch_all_controls(self, mode=None):
        if mode is None:
            mode = cmds.getAttr(
                '{}.lynxiControlMode'.format(self._node_shape)
            )
        else:
            self._set_attributes_(
                self._node_shape, [('lynxiControlMode', mode)]
            )
        #
        cs = self.get_exists_control_shapes()
        if mode == 0:
            [mel.eval('doMenuNURBComponentSelection("{}", "controlVertex");'.format(i)) for i in cs]
        elif mode == 1:
            [mel.eval('doMenuNURBComponentSelection("{}", "curveParameterPoint");'.format(i)) for i in cs]
        elif mode == 2:
            [mel.eval('maintainActiveChangeSelectMode {} 1;'.format(i)) for i in cs]
    @classmethod
    def get_control_connection_args(cls, shape_path):
        _ = cmds.listConnections('{}.worldSpace[0]'.format(shape_path), destination=1, source=0, connections=1, plugs=1) or []
        if _:
            atr_src, atr_tgt = _[:2]
            node_shape, atr_tgt_name = atr_tgt.split('.')
            if cmds.nodeType(node_shape) == cls.C2ME_TYPE_NAME:
                if atr_tgt_name.startswith('inputUBaseCurves['):
                    index = int(atr_tgt_name.split('inputUBaseCurves[')[-1][:-1])
                    return atr_src, atr_tgt, node_shape, index
    @classmethod
    def connect_control_to(cls, transform_path, atr):
        _ = cmds.listRelatives(transform_path, children=1, type='nurbsCurve', fullPath=1) or []
        if _:
            shape_path = _[0]
            cmds.connectAttr('{}.worldSpace[0]'.format(shape_path), atr)
    @classmethod
    def setup_control(cls, transform_path, shape_path=None):
        if shape_path is None:
            _ = cmds.listRelatives(transform_path, children=1, type='nurbsCurve', fullPath=1) or []
            if _:
                shape_path = _[0]
        #
        if shape_path is None:
            return
        #
        cls._set_attributes_(
            transform_path, [('displayLocalAxis', 1)]
        )
        cls._lock_transformations_(transform_path)
        cls._set_attributes_(
            shape_path, [('dispCV', 1), ('dispHull', 1), ('dispGeometry', 1)]
        )
    @classmethod
    def set_control_info(cls, transform_path, index):
        _ = cmds.listRelatives(transform_path, children=1, type='annotationShape', fullPath=1) or []
        if _:
            shape_path = _[0]
            cls._set_attributes_(
                shape_path, [('text', '    {}'.format(str(index)), dict(type='string'))]
            )
        else:
            cls.create_control_info(transform_path, index)
    @classmethod
    def create_control_info(cls, transform_path, index):
        i = cls._append_annotation__(transform_path)
        cls._set_attributes_(
            i, [('displayArrow', 0), ('text', '    {}'.format(str(index)), dict(type='string'))]
        )


class C2meWindow(MtdBase):
    BUTTON_WIDTH = 120
    def __init__(self):
        self._copy_from_shape = None

    def reset(self):
        pass
    @set_undo_mark
    def setup(self):
        self.create_camera()
        self.reset_camera()
        mel.eval('source dagMenuProc;')
        #
        self.reset_window()
        #
        w, h = self.CONTROL_WINDOW_SIZE
        cmds.window(self.CONTROL_WINDOW_NAME, title=self.CONTROL_WINDOW_NAME, width=w, height=h, closeCommand=self.__close_fnc)
        cmds.window(self.CONTROL_WINDOW_NAME, edit=1, width=w, height=h)
        layout = cmds.paneLayout(width=w, height=h)
        self._tool = cmds.curveToMeshExtraContext()
        self._panel = cmds.modelPanel(
            label=self.CONTROL_WINDOW_NAME + '_model_panel',
            parent=layout,
            modelEditor=1,
            camera=self.get_camera()
        )
        #
        self.__setup_panel(self._panel)
        # cmds.frameLayout(label='Tool', collapse=False, height=80)
        c_l = cmds.columnLayout(
            adjustableColumn=True, rowSpacing=2
        )
        #
        self.__setup_switch_tool(c_l)
        self.__setup_control_point_tool(c_l)
        self.__setup_control_tool(c_l)
        self.__setup_layout_control_toll(c_l)
        #
        cmds.separator(
            parent=c_l,
            height=4,
            style='shelf'
        )
        #
        r_l = cmds.rowLayout(
            numberOfColumns=2,
            parent=c_l
        )
        cmds.button(
            self.CONTROL_WINDOW_NAME + '_set_to_tool_button', label='Set to Tool',
            # backgroundColor=(.25, 1, .5),
            width=self.BUTTON_WIDTH,
            command=self.__set_to_tool_fnc,
            parent=r_l
        )
        cmds.button(
            self.CONTROL_WINDOW_NAME + '_select_node_button', label='Select Node',
            # backgroundColor=(.25, 1, .5),
            width=self.BUTTON_WIDTH,
            command=self.__select_node_fnc,
            parent=r_l
        )
        cmds.showWindow(self.CONTROL_WINDOW_NAME)
        self.__selection_changed_fnc()
        self.create_selection_script_jobs()

    def __setup_panel(self, panel):
        cmds.modelEditor(
            panel,
            edit=1,
            activeView=1,
            wireframeOnShaded=0,
            fogging=0,
            dl='default',
            twoSidedLighting=1,
            allObjects=0,
            grid=0,
            # hud=0,
            sel=1,
            nurbsCurves=1,
            controlVertices=1,
            locators=1,
            hulls=1,
            manipulators=1,
            handles=1,
            #
            dimensions=1,
            #
            headsUpDisplay=0,
        )

    def __setup_switch_tool(self, layout):
        r_l = cmds.rowLayout(
            numberOfColumns=4,
            parent=layout,
        )
        cmds.text(
            label='Switch All to',
            width=self.BUTTON_WIDTH,
            align='right'
        )
        cmds.nodeIconButton(
            self.CONTROL_WINDOW_NAME + '_switch_all_to_control_vertex_button', label='Control Vertex',
            image1='curveEP.png',
            style='iconAndTextHorizontal',
            width=self.BUTTON_WIDTH,
            # height=24,
            command=self.__switch_all_to_control_vertex,
            parent=r_l
        )
        cmds.nodeIconButton(
            self.CONTROL_WINDOW_NAME + '_switch_all_to_curve_point_button', label='Curve Point',
            image1='pencil.png',
            style='iconAndTextHorizontal',
            width=self.BUTTON_WIDTH,
            command=self.__switch_all_to_curve_point,
            parent=r_l
        )
        cmds.nodeIconButton(
            self.CONTROL_WINDOW_NAME + '_switch_all_to_object_mode_button', label='Object Mode',
            image1='circle.png',
            style='iconAndTextHorizontal',
            width=self.BUTTON_WIDTH,
            command=self.__switch_all_to_object_mode,
            parent=r_l
        )

    def __setup_control_point_tool(self, layout):
        r_l = cmds.rowLayout(
            numberOfColumns=3,
            parent=layout,
        )
        cmds.text(
            label='Control Point',
            width=self.BUTTON_WIDTH,
            align='right'
        )
        cmds.nodeIconButton(
            self.CONTROL_WINDOW_NAME + '_insert_control_point_button', label='Insert',
            image1='insertKnot.png',
            style='iconAndTextHorizontal',
            width=self.BUTTON_WIDTH,
            command=self.__insert_control_point_fnc,
            parent=r_l
        )
        cmds.nodeIconButton(
            self.CONTROL_WINDOW_NAME + '_rebuild_control_point_button', label='Rebuild',
            image1='rebuildCurve.png',
            style='iconAndTextHorizontal',
            width=self.BUTTON_WIDTH,
            command=self.__rebuild_control_point_fnc,
            parent=r_l
        )

    def __setup_control_tool(self, layout):
        r_l = cmds.rowLayout(
            numberOfColumns=4,
            parent=layout,
        )
        cmds.text(
            label='Control',
            width=self.BUTTON_WIDTH,
            align='right'
        )
        cmds.nodeIconButton(
            self.CONTROL_WINDOW_NAME + '_append_one_new_control_button', label='Append One New',
            image1='polyCreateUVSet.png',
            style='iconAndTextHorizontal',
            width=self.BUTTON_WIDTH,
            command=self.__append_one_new_control,
            parent=r_l
        )
        cmds.nodeIconButton(
            self.CONTROL_WINDOW_NAME + '_copy_from_current_control_button', label='Copy from Current',
            image1='polyCopyUV.png',
            style='iconAndTextHorizontal',
            width=self.BUTTON_WIDTH,
            command=self.__copy_from_current_control,
            parent=r_l
        )
        cmds.nodeIconButton(
            self.CONTROL_WINDOW_NAME + '_paste_to_current_control_button', label='Past to Current',
            image1='polyPasteUV.png',
            style='iconAndTextHorizontal',
            width=self.BUTTON_WIDTH,
            command=self.__paste_to_current_control,
            parent=r_l
        )

    def __setup_layout_control_toll(self, layout):
        r_l = cmds.rowLayout(
            numberOfColumns=3,
            parent=layout,
        )
        cmds.text(
            label='Layout Control as',
            width=self.BUTTON_WIDTH,
            align='right'
        )
        cmds.nodeIconButton(
            self.CONTROL_WINDOW_NAME + '_layout_all_control_as_horizontal_button', label='Horizontal',
            image1='defaultTwoSideBySideLayout.png',
            style='iconAndTextHorizontal',
            width=self.BUTTON_WIDTH,
            command=self.__layout_all_control_as_horizontal,
            parent=r_l
        )
        cmds.nodeIconButton(
            self.CONTROL_WINDOW_NAME + '_layout_all_control_as_vertical_button', label='Vertical',
            image1='defaultTwoStackedLayout.png',
            style='iconAndTextHorizontal',
            width=self.BUTTON_WIDTH,
            command=self.__layout_all_control_as_vertical,
            parent=r_l
        )
    @staticmethod
    def _node_get_control_transforms_(node_shape):
        return cmds.listConnections('{}.inputUBaseCurves'.format(node_shape), destination=0, source=1) or []

    def __set_to_tool_fnc(self, *args, **kwargs):
        if self._tool is not None:
            cmds.setToolTo(self._tool)

    def __switch_all_to_control_vertex(self, *args, **kwargs):
        if self._node_shape is not None:
            if cmds.objExists(self._node_shape):
                C2meNode(self._node_shape).switch_all_controls(0)

    def __switch_all_to_curve_point(self, *args, **kwargs):
        if self._node_shape is not None:
            if cmds.objExists(self._node_shape):
                C2meNode(self._node_shape).switch_all_controls(1)

    def __switch_all_to_object_mode(self, *args, **kwargs):
        if self._node_shape is not None:
            if cmds.objExists(self._node_shape):
                C2meNode(self._node_shape).switch_all_controls(2)

    def __select_node_fnc(self, *args, **kwargs):
        if self._node_shape is not None:
            if cmds.objExists(self._node_shape):
                cmds.select(self._node_shape)
    @staticmethod
    def __insert_control_point_fnc(*args, **kwargs):
        mel.eval(
            'InsertKnot;'
        )

    @set_undo_mark
    def __append_one_new_control(self, *args, **kwargs):
        if self._node_shape is not None:
            if cmds.objExists(self._node_shape):
                C2meNode(self._node_shape).append_one_control()
                self.view_to_select_node(self._node_shape)
    @set_undo_mark
    def __copy_from_current_control(self, *args, **kwargs):
        _ = cmds.ls(selection=1, long=1, type='nurbsCurve', dagObjects=1, noIntermediate=1, objectsOnly=1) or []
        if _:
            self._copy_from_shape = _[0]
            trace('copy from "{}"'.format(self._copy_from_shape))
    @set_undo_mark
    def __paste_to_current_control(self, *args, **kwargs):
        if self._copy_from_shape:
            from_shape_path = self._copy_from_shape
            _ = cmds.ls(selection=1, long=1, type='nurbsCurve', dagObjects=1, noIntermediate=1, objectsOnly=1) or []
            if _:
                to_shape_path = _[0]
                if from_shape_path != to_shape_path:
                    name = self._get_shape_transform_name_(from_shape_path)
                    _ = C2meNode.get_control_connection_args(to_shape_path)
                    if not _:
                        return
                    atr_tgt, atr_tgt, node_shape, index = _
                    results = cmds.duplicate(from_shape_path, name='{}_copy'.format(name))
                    if results:
                        n = C2meNode(node_shape)
                        c_c = n.get_exists_control_container()
                        if c_c is None:
                            return
                        c_c_path = cmds.ls(c_c, long=1)[0]
                        to_transform_path = self._get_shape_transform_path_(to_shape_path)

                        result = results[0]
                        new_transform_path = cmds.ls(result, long=1)[0]
                        if not new_transform_path.startswith(c_c_path):
                            _results = cmds.parent(new_transform_path, c_c_path)
                            _result = _results[0]
                            new_transform_path = cmds.ls(_result, long=1)[0]
                        #
                        cmds.delete(to_transform_path)
                        n.connect_control_to(new_transform_path, atr_tgt)
                        n.setup_control(new_transform_path)
                        n.layout_control(new_transform_path, index)
                        panel = self.get_panel()
                        if panel:
                            self._add_to_view_set_(panel, [new_transform_path])
    @set_undo_mark
    def __layout_all_control_as_horizontal(self, *args, **kwargs):
        if self._node_shape is not None:
            if cmds.objExists(self._node_shape):
                C2meNode(self._node_shape).layout_all_controls(0)
    @set_undo_mark
    def __layout_all_control_as_vertical(self, *args, **kwargs):
        if self._node_shape is not None:
            if cmds.objExists(self._node_shape):
                C2meNode(self._node_shape).layout_all_controls(1)
    @staticmethod
    def __rebuild_control_point_fnc(*args, **kwargs):
        mel.eval(
            'RebuildCurveOptions;'
        )

    def __selection_changed_fnc(self):
        _ = cmds.ls(selection=1, long=1, type='curveToMeshExtra', dagObjects=1, noIntermediate=1, objectsOnly=1) or []
        node_shape = None
        if _:
            node_shape = _[0]
        #
        if node_shape is not None:
            # self.load_tool()
            self._node_shape = node_shape
            self.view_to_select_node(node_shape)
            self.view_to_select_control(node_shape)
            self.create_script_job_for_node(node_shape)
            trace('view node for "{}"'.format(node_shape))

    def __close_fnc(self):
        cmds.isolateSelect(self._panel, state=0)
    @staticmethod
    def load_tool():
        ctx = cmds.curveToMeshExtraContext(nop=1)
        cmds.setToolTo(ctx)

    def create_selection_script_jobs(self):
        if cmds.window(self.SELECTION_WINDOW_NAME, query=1, exists=1) is False:
            cmds.window(self.SELECTION_WINDOW_NAME, title=self.SELECTION_WINDOW_NAME)
        #
        cmds.scriptJob(
            parent=self._panel,
            replacePrevious=True,
            event=['SelectionChanged', self.__selection_changed_fnc]
        )
    @classmethod
    def create_view_set(cls, panel):
        ss = cmds.ls(selection=1, long=1)
        cmds.isolateSelect(panel, state=1)
        [cmds.isolateSelect(panel, removeDagObject=i) for i in ss]
        return cmds.isolateSelect(panel, query=1, viewObjects=1)
    @classmethod
    def get_view_set(cls, panel):
        _ = cmds.isolateSelect(panel, query=1, viewObjects=1) or None
        if _ is not None:
            return _
        ss = cmds.ls(selection=1, long=1)
        cmds.isolateSelect(panel, state=1)
        [cmds.isolateSelect(panel, removeDagObject=i) for i in ss]
        return cmds.isolateSelect(panel, query=1, viewObjects=1)
    @classmethod
    def _clear_view_set_(cls, panel, view_set):
        ccs = cmds.sets(view_set, query=1) or []
        [cmds.isolateSelect(panel, removeDagObject=i) for i in ccs]
    @classmethod
    def _add_to_view_set_(cls, panel, nodes):
        [cmds.isolateSelect(panel, addDagObject=i) for i in nodes]
    @set_undo_mark
    def view_to_select_node(self, node_shape):
        if cmds.objExists(node_shape):
            panel = self.get_panel()
            view_set = self.get_view_set(panel)
            n = C2meNode(node_shape)
            if view_set is not None:
                if cmds.objExists(view_set):
                    ccs = cmds.sets(view_set, query=1) or []
                    [cmds.isolateSelect(panel, removeDagObject=i) for i in ccs]
                    self._clear_view_set_(panel, view_set)
                    control_transforms = n.get_exists_control_transforms()
                    self._add_to_view_set_(panel, control_transforms)
            #
            n.switch_all_controls()
    @set_undo_mark
    def view_to_select_control(self, node_shape):
        if cmds.objExists(node_shape):
            atr = '{}.vExtraIndex'.format(node_shape)
            n = C2meNode(node_shape)
            control_transforms = n.get_exists_control_transforms()
            control_query = {i_seq*2: i for i_seq, i in enumerate(control_transforms)}
            if control_transforms:
                panel = self.get_panel()
                camera = self.get_camera()
                if panel is not None and camera is not None:
                    index = cmds.getAttr(atr)
                    if index in control_query:
                        control_transform = control_query[index]
                        cmds.viewFit(
                            camera,
                            [control_transform],
                            fitFactor=1.0,
                            animate=0
                        )
                        trace('view control for "{}" at {}'.format(node_shape, index))

    def create_script_job_for_node(self, node_shape):
        def fnc_(*args, **kwargs):
            self.view_to_select_control(node_shape)
        #
        atr = '{}.vExtraIndex'.format(node_shape)
        if cmds.window(self.CONTROL_WINDOW_NAME, query=1, exists=1) is True:
            cmds.scriptJob(
                parent=self.CONTROL_WINDOW_NAME,
                replacePrevious=True,
                attributeChange=[atr, fnc_]
            )

    def reset_window(self):
        if cmds.window(self.CONTROL_WINDOW_NAME, query=1, exists=1) is True:
            cmds.deleteUI(self.CONTROL_WINDOW_NAME, window=1)
    @classmethod
    def create_camera(cls):
        camera_shape_name = cls.CAMERA_NAME + 'Shape'
        if cmds.objExists(cls.CAMERA_NAME) is False:
            camera = cmds.createNode('camera', name=camera_shape_name, skipSelect=1)
            cmds.camera(
                camera,
                edit=1,
                displayFilmGate=0,
                displaySafeAction=0,
                displaySafeTitle=0,
                displayFieldChart=0,
                displayResolution=0,
                displayGateMask=0,
                filmFit=1,
                focalLength=35.000,
                overscan=1.0,
                nearClipPlane=0.1,
                farClipPlane=1000000.0
            )
            #
            cmds.camera(
                camera,
                edit=1,
                position=(0, 0, 0),
                rotation=(90, 0, 0)
            )
            cmds.setAttr(camera+'.renderable', 0)
            cmds.setAttr(camera+'.orthographic', 1)
    @classmethod
    def get_camera(cls):
        _ = cmds.ls('*{}'.format(cls.CAMERA_NAME), long=1)
        if _:
            return _[0]

    def reset_camera(self):
        camera = self.get_camera()
        if camera:
            cmds.camera(
                camera,
                edit=1,
                position=(-100000, -100000, -100000),
                rotation=(90, 0, 0)
            )
    #
    def get_panel(self):
        if cmds.modelPanel(
            self._panel, query=1, exists=1
        ) is True:
            return self._panel


class C2meCommand(MtdBase):
    def __init__(self):
        self._panel = None
        self._node_shape = None
        self._tool = None
    @classmethod
    def create_node_by_curves(cls, input_v_base_curve_shapes=None, control_count=2, radius=.1):
        cmds.loadPlugin(cls.PLUGIN_NAME, quiet=1)
        #
        node_shapes = []
        mesh_shapes = []
        if input_v_base_curve_shapes is None:
            input_v_base_curve_shapes = cmds.ls(type=cls.CURVE_TYPE_NAME, selection=1, dagObjects=1, noIntermediate=1, long=1) or []
        #
        for i_input_v_base_curve_shape in input_v_base_curve_shapes:
            ts = cmds.listRelatives(i_input_v_base_curve_shape, parent=1, fullPath=1)
            r = C2meNode.create(i_input_v_base_curve_shape, control_count=control_count, radius=radius)
            if r:
                i_node_shape, i_output_mesh_shape = r
                #
                node_shapes.append(i_node_shape)
                mesh_shapes.append(i_output_mesh_shape)
        #
        if len(node_shapes) > 1:
            group = cmds.createNode('transform', name=cls.C2ME_NODE_GROUP_NAME, skipSelect=1)
            cls._parent_shapes_parent_to_(node_shapes, group)
            cls._set_outliner_color_(group, 1, .5, .25)
        #
        if len(mesh_shapes) > 1:
            group = cmds.createNode('transform', name=cls.C2ME_MESH_GROUP_NAME, skipSelect=1)
            cls._parent_shapes_parent_to_(mesh_shapes, group)
            cls._set_outliner_color_(group, 1, .5, .25)
        return node_shapes, mesh_shapes
    @classmethod
    def create_node_by_guides(cls, input_v_base_guide_shapes=None, control_count=2, radius=.1):
        cmds.loadPlugin('lxConvertNode', quiet=1)
        #
        nodes = []
        curve_shapes = []
        node_shapes = []
        mesh_shapes = []
        if input_v_base_guide_shapes is None:
            input_v_base_guide_shapes = cmds.ls(type='xgmSplineGuide', selection=1, dagObjects=1, noIntermediate=1, long=1) or []
        #
        for i_guide_shape in input_v_base_guide_shapes:
            i_guide_transform = cls._get_shape_transform_path_(i_guide_shape)
            i_node, i_curve_shape = lxcmds.set_x2c_create_cmd(i_guide_shape)
            # cls._hide_by_shape_(i_curve_shape)
            i_curve_transform = cls._get_shape_transform_path_(i_curve_shape)
            cls._parent_transform_to_(i_curve_transform, i_guide_transform)
            nodes.append(i_node)
            # curve_shapes.append(i_curve_shape)
            r = C2meNode.create(i_curve_shape, control_count=control_count, radius=radius)
            if r:
                i_node_shape, i_output_mesh_shape = r
                #
                node_shapes.append(i_node_shape)
                mesh_shapes.append(i_output_mesh_shape)
                #
                i_input_mesh_shape = lxcmds.get_xgen_guide_input_mesh_shape(i_guide_shape)
                if i_input_mesh_shape is not None:
                    if not cmds.connectionInfo(i_node_shape + '.inputGrowMesh', isExactDestination=1):
                        cmds.connectAttr(
                            i_input_mesh_shape + '.worldMesh[0]', i_node_shape + '.inputGrowMesh'
                        )
        #
        if len(node_shapes) > 1:
            group = cmds.createNode('transform', name=cls.C2ME_NODE_GROUP_NAME, skipSelect=1)
            cls._parent_shapes_parent_to_(node_shapes, group)
            cls._set_outliner_color_(group, 1, .5, 1)
        #
        if len(mesh_shapes) > 1:
            group = cmds.createNode('transform', name=cls.C2ME_MESH_GROUP_NAME, skipSelect=1)
            cls._parent_shapes_parent_to_(mesh_shapes, group)
            cls._set_outliner_color_(group, 1, 1, .25)
    @staticmethod
    def setup():
        C2meWindow.create_camera()
    @staticmethod
    def show_control_window():
        C2meWindow().setup()
