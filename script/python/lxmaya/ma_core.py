# coding:utf-8
import six
# noinspection PyUnresolvedReferences
from maya import cmds, OpenMayaUI
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.api.OpenMaya as om2

import fnmatch

import math

from lxbasic import bsc_core

from lxutil import utl_core

from . import ma_configure

from PySide2 import QtWidgets


def _ma__get_group_paths_():
    return [
        i
        for i in cmds.ls(exactType='transform', long=1) or []
        if i and cmds.listRelatives(i, children=1, shapes=1, noIntermediate=0) is None
    ]


def _ma__get_shape_paths_():
    return [
        i
        for i in cmds.ls(shapes=1, long=1, noIntermediate=1) or []
        if i and cmds.listRelatives(i, children=1, shapes=1, noIntermediate=0) is None
    ]


def _ma__get_namespace_paths_():
    lis = []
    except_list = ['UI', 'shared']
    _ = cmds.namespaceInfo(recurse=1, listOnlyNamespaces=1, fullName=1)
    if _:
        _.reverse()
        for namespace in _:
            if namespace not in except_list:
                lis.append(namespace)
    return lis


def _ma_node__get_history_paths_(obj_string):
    except_types = ['shadingEngine', 'groupId', 'set']
    lis = []
    for j in cmds.listHistory(obj_string, pruneDagObjects=1) or []:
        if cmds.nodeType(j) not in except_types:
            lis.append(j)
    return lis


def _ma_type__get_file_reference_dict_(node_type):
    dic = {}
    PORT_PATHSEP = ma_configure.Util.PORT_PATHSEP
    directory_paths = cmds.filePathEditor(query=True, listDirectories="") or []
    for directory_path in directory_paths:
        raw = cmds.filePathEditor(query=True, listFiles=directory_path, withAttribute=True, byType=node_type) or []
        for i in range(len(raw) / 2):
            file_name = raw[i * 2]
            attribute_path = raw[i * 2 + 1]
            _ = attribute_path.split(PORT_PATHSEP)
            file_path = '{}/{}'.format(directory_path, file_name)
            node_path = cmds.ls(_[0], long=1)[0]
            port_path = PORT_PATHSEP.join(_[1:])
            dic.setdefault(node_path, []).append((port_path, file_path))
    return dic


def _ma_get_override_node_paths_(reference=True):
    _ = [x for x in cmds.ls() if '|' in x]
    if reference is True:
        return _
    return [i for i in _ if not cmds.referenceQuery(i, isNodeReferenced=1)]


def _ma_obj_name__get_with_namespace_clear_(obj_name):
    namespace_pathsep = ma_configure.Util.NAMESPACE_PATHSEP
    return obj_name.split(namespace_pathsep)[-1]


def _ma_obj_path__get_with_namespace_clear_(obj_path):
    obj_pathsep = ma_configure.Util.OBJ_PATHSEP
    return obj_pathsep.join([_ma_obj_name__get_with_namespace_clear_(i) for i in obj_path.split(obj_pathsep)])


def get_is_ui_mode():
    return not cmds.about(batch=1)


class Om2Method(object):
    DEFAULT_MAP_NAME = 'map1'
    @classmethod
    def _get_om2_dag_path_(cls, path):
        return om2.MGlobal.getSelectionListByName(path).getDagPath(0)
    @classmethod
    def _get_om2_dag_obj_(cls, path):
        return om2.MFnDagNode(cls._get_om2_dag_path_(path)).object()
    @classmethod
    def _get_om2_transform_(cls, path=None):
        if path:
            return om2.MFnTransform(cls._get_om2_dag_path_(path))
        return om2.MFnTransform()
    @classmethod
    def _get_om2_mesh_fnc_(cls, path):
        return om2.MFnMesh(cls._get_om2_dag_path_(path))
    @classmethod
    def _get_om2_nurbs_curve_fnc_(cls, path):
        return om2.MFnNurbsCurve(cls._get_om2_dag_path_(path))
    @classmethod
    def _get_om2_nurbs_surface_fnc_(cls, path):
        return om2.MFnNurbsSurface(cls._get_om2_dag_path_(path))
    @classmethod
    def _get_om2_dag_node_fnc_(cls, path):
        return om2.MFnDagNode(cls._get_om2_dag_path_(path))
    @classmethod
    def _get_om2_obj_(cls, name):
        return om2.MFnDependencyNode(
            om2.MGlobal.getSelectionListByName(name).getDependNode(0)
        )
    #
    @classmethod
    def _get_om2_point_(cls, point):
        om2_point = om2.MPoint()
        om2_point.x, om2_point.y, om2_point.z = point
        return om2_point
    @classmethod
    def _get_om2_point_array_(cls, point_array):
        m2PointArray = om2.MPointArray()
        for point in point_array:
            om2_point = cls._get_om2_point_(point)
            m2PointArray.append(om2_point)
        return m2PointArray
    #
    @classmethod
    def _get_int_array_(cls, om2_int_array):
        return [int(i) for i in om2_int_array]
    @classmethod
    def _get_float_array_(cls, om2_float_array):
        """
        :param om2_float_array: instance(OpenMaya.MFloatArray)
        :return:
            list(
                float,
                ...
            )
        """
        return [float(i) for i in om2_float_array]
    @classmethod
    def _get_point_(cls, om2_point, round_count=None):
        x, y, z = om2_point.x, om2_point.y, om2_point.z
        if isinstance(round_count, int):
            return round(x, round_count), round(y, round_count), round(z, round_count)
        return x, y, z
    @classmethod
    def _get_point_array_(cls, om2_point_array, round_count=None):
        """
        :param om2_point_array: instance(OpenMaya.MPoint)
        :return:
            list(
                tuple(float(x), float(y), float(z)),
                ...
            )
        """
        return [cls._get_point_(i, round_count) for i in om2_point_array]
    @classmethod
    def _get_float_vector_(cls, om2_float_vector):
        """
        :param om2_float_vector: instance(OpenMaya.MFloatVector)
        :return:
            tuple(float(x), float(y), float(z))
        """
        return om2_float_vector.x, om2_float_vector.y, om2_float_vector.z
    @classmethod
    def _get_float_vector_array_(cls, om2_float_vector_array):
        """
        :param om2_float_vector_array: instance(OpenMaya.MFloatVectorArray)
        :return:
            list(
                tuple(float(x), float(y), float(z)),
                ...
            )
        """
        return [(i.x, i.y, i.z) for i in om2_float_vector_array]
    @classmethod
    def _get_rgba_array_(cls, om2_color_array):
        """
        :param om2_color_array: instance(OpenMaya.MColorArray)
        :return:
            list(
                tuple(float(r), float(g), float(b), float(a)),
                ...
            )
        """
        return [(i.r, i.g, i.b, i.a) for i in om2_color_array]
    @classmethod
    def _get_om2_vector_(cls, vector):
        return om2.MVector(*vector)
    @classmethod
    def _get_om2_int_array_(cls, int_array):
        return om2.MIntArray(int_array)
    @classmethod
    def _get_om2_matrix_(cls, matrix):
        om2_matrix = om2.MMatrix()
        for seq in range(4):
            for sub_seq in range(4):
                om2_matrix.setElement(seq, sub_seq, matrix[seq * 4 + sub_seq])
        return om2_matrix
    @classmethod
    def _get_om2_transformation_matrix_(cls, matrix):
        return om2.MTransformationMatrix(cls._get_om2_matrix_(matrix))
    #
    @staticmethod
    def _to_int_array_reduce(array):
        lis = []
        #
        maximum, minimum = max(array), min(array)
        #
        start, end = None, None
        count = len(array)
        index = 0
        #
        array.sort()
        for seq in array:
            if index > 0:
                pre = array[index - 1]
            else:
                pre = None
            #
            if index < (count - 1):
                nex = array[index + 1]
            else:
                nex = None
            #
            if pre is None and nex is not None:
                start = minimum
                if seq - nex != -1:
                    lis.append(start)
            elif pre is not None and nex is None:
                end = maximum
                if seq - pre == 1:
                    lis.append((start, end))
                else:
                    lis.append(end)
            elif pre is not None and nex is not None:
                if seq - pre != 1 and seq - nex != -1:
                    lis.append(seq)
                elif seq - pre == 1 and seq - nex != -1:
                    end = seq
                    lis.append((start, end))
                elif seq - pre != 1 and seq - nex == -1:
                    start = seq
            #
            index += 1
        #
        return lis
    @classmethod
    def _get_mesh_comp_names_(cls, indices, comp_key):
        lis = []
        if indices:
            reduce_ids = cls._to_int_array_reduce(indices)
            if len(reduce_ids) == 1:
                if isinstance(reduce_ids[0], tuple):
                    return ['{}[{}:{}]'.format(comp_key, *reduce_ids[0])]
            for i in reduce_ids:
                if isinstance(i, int):
                    lis.append('{}[{}]'.format(comp_key, i))
                elif isinstance(i, tuple):
                    lis.append('{}[{}:{}]'.format(comp_key, *i))
        #
        return lis
    @classmethod
    def _get_mesh_face_comp_names_(cls, indices):
        return cls._get_mesh_comp_names_(indices, 'f')
    @classmethod
    def _get_mesh_edge_comp_names_(cls, indices):
        return cls._get_mesh_comp_names_(indices, 'e')
    @classmethod
    def _get_mesh_vertex_comp_names_(cls, indices):
        return cls._get_mesh_comp_names_(indices, 'vtx')
    @classmethod
    def _get_curve_knots_(cls, count, degree):
        span = count-3
        M = span
        N = degree
        # c = M+2*N-1
        lis = []
        knot_minimum, knot_maximum = 0.0, float(M)
        #
        [lis.append(knot_minimum) for i in range(degree)]
        #
        add_count = count-N-1
        for seq in range(add_count):
            lis.append(float(seq + 1) * knot_maximum / (add_count + 1))
        #
        [lis.append(knot_maximum) for i in range(degree)]
        return lis
    @classmethod
    def _get_surface_knots_(cls, count, degree):
        lis = []
        minKnots, maxKnots = 0.0, 1.0
        #
        iPCount = count - 2
        [lis.append(minKnots) for _ in range(degree)]
        #
        for seq in range(iPCount):
            lis.append(float(seq + 1) * maxKnots / (iPCount + 1))
        #
        [lis.append(maxKnots) for _ in range(degree)]
        return lis
    @classmethod
    def _set_locator_create_by_points(cls, points):
        for seq, point in enumerate(points):
            cmds.spaceLocator(name='test_{}_loc'.format(seq), position=point)
    @classmethod
    def _get_center_point_(cls, point_0, point_1):
        x, y, z = (point_0.x + point_1.x) / 2, (point_0.y + point_1.y) / 2, (point_0.z + point_1.z) / 2
        return om2.MPoint(x, y, z)
    @staticmethod
    def _set_value_map_(range1, range2, value1):
        min1, max1 = range1
        min2, max2 = range2
        #
        percent = float(value1 - min1)/(max1 - min1)
        #
        value2 = (max2 - min2) * percent + min2
        return value2
    @classmethod
    def _set_om2_curve_create_(cls, points, knots, degree, form, parent):
        om2_curve = om2.MFnNurbsCurve()
        om2_curve.create(
            points,
            knots, degree, form,
            False,
            True,
            parent=parent
        )


class Om2CurveCreator(object):
    def __init__(self, path):
        # if cmds.objExists(path) is False:
        #     cmds.createNode('transform', name=path)
        self._obj_path = path
        self._om2_obj_fnc = Om2Method._get_om2_dag_obj_(path)
    @classmethod
    def _get_om2_point_array_(cls, point_array):
        m2PointArray = om2.MPointArray()
        for point in point_array:
            om2_point = Om2Method._get_om2_point_(point)
            m2PointArray.append(om2_point)
        return m2PointArray
    @classmethod
    def _get_knots__(cls, count, degree, span):
        M = span
        N = degree
        # c = M+2*N-1
        lis = []
        knot_minimum, knot_maximum = 0.0, float(M)
        #
        [lis.append(knot_minimum) for i in range(degree)]
        #
        add_count = count-N-1
        for seq in range(add_count):
            lis.append(float(seq + 1) * knot_maximum / (add_count + 1))
        #
        [lis.append(knot_maximum) for i in range(degree)]
        return lis
    @classmethod
    def _set_points_reduce_(cls, points):
        lis = [points[0], cls._get_mid_point_(points[0], points[1])]
        for i in points[1:-1]:
            lis.append(i)
        lis.extend(
            [points[-1]]
        )
        return lis
    @classmethod
    def _get_mid_point_(cls, point_0, point_1):
        x_0, y_0, z_0 = point_0
        x_1, y_1, z_1 = point_1
        return (x_1 + x_0) / 2, (y_1 + y_0) / 2, (z_1 + z_0) / 2

    def set_create_by_points(self, points, degree=3):
        points_ = points
        form = 1
        count = len(points_)
        knots = Om2Method._get_curve_knots_(count, degree)
        om2_curve = om2.MFnNurbsCurve()
        om2_curve.create(
            self._get_om2_point_array_(points_),
            knots, degree, form,
            False,
            True,
            parent=Om2Method._get_om2_dag_obj_('|{}'.format(self._obj_path))
        )

    def set_create_by_raw(self, raw):
        points, knots, degree, form = raw
        om2_curve = om2.MFnNurbsCurve()
        om2_curve.create(
            self._get_om2_point_array_(points),
            knots, degree, form,
            False,
            True,
            parent=Om2Method._get_om2_dag_obj_(self._obj_path)
        )


class Om2CurveOpt(object):
    def __init__(self, path):
        self._om2_obj_fnc = Om2Method._get_om2_nurbs_curve_fnc_(path)
    @property
    def path(self):
        return self._om2_obj_fnc.fullPathName()

    def get_degree(self):
        return self._om2_obj_fnc.degree

    def get_form(self):
        return self._om2_obj_fnc.form

    def get_knots(self):
        return Om2Method._get_float_array_(self._om2_obj_fnc.knots())

    def set_knots(self, knots):
        self._om2_obj_fnc.setKnots(knots, 0, len(knots)-1)
        self._om2_obj_fnc.updateCurve()

    def get_points(self):
        return Om2Method._get_point_array_(self._om2_obj_fnc.cvPositions())

    def get_create_raw(self):
        points = Om2Method._get_point_array_(self._om2_obj_fnc.cvPositions())
        knots = Om2Method._get_float_array_(self._om2_obj_fnc.knots())
        degree = self._om2_obj_fnc.degree
        form = self._om2_obj_fnc.form
        return points, knots, degree, form

    def _test_(self):
        print self._om2_obj_fnc.cvs()
    @staticmethod
    def _get_curve_knots_(count, degree, form):
        if form == 1:
            if count == 2:
                return [0.0]*degree+[1.0]
            span = max(count - 3, 1)
            M = span
            N = degree
            lis = []
            knot_minimum, knot_maximum = 0.0, float(M)
            #
            [lis.append(knot_minimum) for _ in range(degree)]
            #
            add_count = count - N - 1
            for seq in range(add_count):
                lis.append(float(seq + 1) * knot_maximum / (add_count + 1))
            #
            [lis.append(knot_maximum) for _ in range(degree)]
            return lis
        elif form == 3:
            span = max(count - 3, 1)
            M = span
            N = degree
            lis = []
            knot_minimum, knot_maximum = 0.0, float(M) + 1
            #
            [lis.append(knot_minimum + i - degree + 1) for i in range(degree)]
            #
            add_count = count - N - 1
            for seq in range(add_count):
                lis.append(float(seq + 1) * knot_maximum / (add_count + 1))
            #
            [lis.append(knot_maximum + i) for i in range(degree)]
            return lis
    @classmethod
    def set_create(cls, name, degree, form, points):
        if form == 3:
            if degree > 1:
                points.append(points[1])
        #
        count = len(points)
        knots = cls._get_curve_knots_(count, degree, 1)
        # print knots
        # knots = [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        knots = [0.0, 0.2, 0.4, 0.6, 1.0]
        transform = cmds.createNode('transform', name=name)
        Om2Method._set_om2_curve_create_(
            Om2Method._get_om2_point_array_(points),
            knots, degree, form,
            parent=Om2Method._get_om2_dag_obj_(transform)
        )


class Om2MeshOpt(object):
    def __init__(self, path):
        self._om2_obj_fnc = Om2Method._get_om2_mesh_fnc_(path)
    @property
    def name(self):
        return self._om2_obj_fnc.name()
    @property
    def path(self):
        return self._om2_obj_fnc.fullPathName()

    def get_face_vertices(self):
        face_vertex_counts = []
        face_vertex_indices = []
        om2_obj = self._om2_obj_fnc
        for i_face_index in xrange(om2_obj.numPolygons):
            i_count = om2_obj.polygonVertexCount(i_face_index)
            face_vertex_counts.append(i_count)
            om2_indices = om2_obj.getPolygonVertices(i_face_index)
            indices = list(om2_indices)
            face_vertex_indices.extend(indices)
        return face_vertex_counts, face_vertex_indices

    def get_unused_vertices(self):
        lis = []
        om2_vertex_itr = om2.MItMeshVertex(self._om2_obj_fnc.object())
        vertex_count = self._om2_obj_fnc.numVertices
        for i_vertex_index in range(vertex_count):
            om2_vertex_itr.setIndex(i_vertex_index)
            if not om2_vertex_itr.numConnectedFaces():
                lis.append(i_vertex_index)
        return lis

    def set_unused_vertices_delete(self):
        c = self.get_unused_vertices()
        for i in Om2Method._get_mesh_vertex_comp_names_(c):
            p = '{}.{}'.format(self.path, i)
            cmds.delete(p)

    def set_vertex_delete(self, vertex_index):
        om2_obj = self._om2_obj_fnc
        om2_obj.deleteVertex(vertex_index)

    def get_face_count(self):
        om2_obj = self._om2_obj_fnc
        return om2_obj.numPolygons

    def get_points(self, round_count=None):
        return Om2Method._get_point_array_(
            self._om2_obj_fnc.getPoints(),
            round_count
        )

    def get_point_at(self, vertex_index):
        return Om2Method._get_point_(
            self._om2_obj_fnc.getPoint(vertex_index),
        )

    def _get_points_(self):
        return self._om2_obj_fnc.getPoints()

    def get_bounding_box(self):
        om2_world_matrix = self.get_world_matrix()
        om2_bounding_box = self._om2_obj_fnc.boundingBox
        om2_bounding_box.transformUsing(om2_world_matrix)
        return om2_bounding_box

    def get_center_point(self):
        return self.get_bounding_box().center

    def get_width(self):
        return self.get_bounding_box().width

    def get_height(self):
        return self.get_bounding_box().height

    def get_depth(self):
        return self.get_bounding_box().depth

    def get_world_matrix(self):
        plug = om2.MPlug(self._om2_obj_fnc.object(), self._om2_obj_fnc.attribute('worldMatrix'))
        plug = plug.elementByLogicalIndex(0)
        plug_obj = plug.asMObject()
        matrix_data = om2.MFnMatrixData(plug_obj)
        world_matrix = matrix_data.matrix()
        return world_matrix
    @classmethod
    def set_create(cls, name, face_vertices, points, uv_map_coords=None, normal_maps=None, color_maps=None):
        transform = cmds.createNode('transform', name=name)
        om2_obj = om2.MFnMesh()
        face_vertex_counts, face_vertex_indices = face_vertices
        om2_obj.create(
            Om2Method._get_om2_point_array_(points),
            face_vertex_counts, face_vertex_indices,
            parent=Om2Method._get_om2_dag_obj_(transform)
        )
        if uv_map_coords is not None:
            uv_map_name = 'map1'
            map_u_coords, map_v_coords = zip(*uv_map_coords)
            om2_obj.setUVs(map_u_coords, map_v_coords, uv_map_name)
            om2_obj.assignUVs(
                face_vertex_counts, face_vertex_indices,
                uv_map_name
            )
        #
        cmds.sets(om2_obj.fullPathName(), forceElement='initialShadingGroup')

    def get_uv_map_names(self):
        """
        :return:
            list(
                str(uv_map_name),
                ...
            )
        """
        return self._om2_obj_fnc.getUVSetNames()

    def get_uv_map_coords(self, uv_map_name):
        """
        :param uv_map_name: str(uv_map_name)
        :return:
            list(
                tuple(float(u), float(v)),
                ...
            )
        """
        u_coords, v_coords = self._om2_obj_fnc.getUVs(uv_map_name)
        coords = zip(u_coords, v_coords)
        return coords

    def get_uv_map_range(self, uv_map_name):
        u_coords, v_coords = self._om2_obj_fnc.getUVs(uv_map_name)
        return (min(u_coords), max(u_coords)), (min(v_coords), max(v_coords))

    def _set_morph_by_uv_map_0_(self, uv_map_name):
        scale = self.get_height() + self.get_width() + self.get_depth()
        #
        face_vertices = self._om2_obj_fnc.getAssignedUVs(uv_map_name)
        #
        (u_minimum, u_maximum), (v_minimum, v_maximum) = self.get_uv_map_range(uv_map_name)
        uv_map_coords = self.get_uv_map_coords(uv_map_name)
        points = []
        for i in uv_map_coords:
            x, z = i
            x, z = (
                Om2Method._set_value_map_((u_minimum, u_maximum), (0, 1), x),
                Om2Method._set_value_map_((v_minimum, v_maximum), (0, 1), z)
            )
            y = 0
            points.append((x*scale, y, -z*scale))
        #
        name = '{}_morph_mesh_0'.format(self.name)
        self.set_create(
            name, face_vertices, points
        )

    def _set_morph_by_uv_map_1_(self, uv_map_name):
        scale = self.get_height() + self.get_width() + self.get_depth()
        #
        om2_vertex_itr = om2.MItMeshVertex(self._om2_obj_fnc.object())
        face_vertices = self.get_face_vertices()
        #
        (u_minimum, u_maximum), (v_minimum, v_maximum) = self.get_uv_map_range(uv_map_name)
        #
        points = []
        vertex_count = self._om2_obj_fnc.numVertices
        for vertex_index in range(vertex_count):
            om2_vertex_itr.setIndex(vertex_index)
            x, z = om2_vertex_itr.getUV(uv_map_name)
            x, z = (
                Om2Method._set_value_map_((u_minimum, u_maximum), (0, 1), x),
                Om2Method._set_value_map_((v_minimum, v_maximum), (0, 1), z)
            )
            y = 0
            points.append((x*scale, y, -z*scale))
        #
        name = '{}_morph_mesh_0'.format(self.name)
        self.set_create(
            name, face_vertices, points
        )

    def set_morph_by_uv_map(self, keep_face_vertices, uv_map_name='map1'):
        if keep_face_vertices is True:
            self._set_morph_by_uv_map_1_(uv_map_name)
        else:
            self._set_morph_by_uv_map_0_(uv_map_name)

    def get_color_map_names(self):
        return self._om2_obj_fnc.getColorSetNames()

    def get_color_map(self, color_map_name):
        return self._om2_obj_fnc.getFaceVertexColors(color_map_name)

    def set_face_vertex_color(self, rgbs, alpha=1):
        color_map_name = 'test'
        color_map_names = self.get_color_map_names()
        if color_map_name not in color_map_names:
            self._om2_obj_fnc.createColorSet(
                color_map_name, True
            )
        self._om2_obj_fnc.setCurrentColorSetName(
            color_map_name
        )
        cmds.polyColorPerVertex(self.path, cdo=1)
        idx = 0
        colors = om2.MColorArray()
        face_indices = []
        for i_face_index in xrange(self._om2_obj_fnc.numPolygons):
            face_indices.append(i_face_index)
            i_count = self._om2_obj_fnc.polygonVertexCount(i_face_index)
            j_om2_color = om2.MColor()
            for j in range(i_count):
                j_om2_color = om2.MColor()
                j_r, j_g, j_b = rgbs[idx], rgbs[idx+1], rgbs[idx+2]
                j_om2_color.r, j_om2_color.g, j_om2_color.b, j_om2_color.a = (j_r, j_g, j_b, alpha)
                idx += 3
            colors.append(j_om2_color)

        self._om2_obj_fnc.setFaceColors(
            colors, face_indices
        )
        self._om2_obj_fnc.updateSurface()

    def _test_(self):
        vertex_index = 11144
        om2_vertex_itr = om2.MItMeshVertex(self._om2_obj_fnc.object())
        om2_vertex_itr.setIndex(vertex_index)
        print om2_vertex_itr.getConnectedFaces()

    def get_face_shell_ids(self):
        counts, indices = self.get_face_vertices()
        return bsc_core.MeshFaceShellMtd.get_shell_dict_from_face_vertices(
            counts, indices
        )


class Om2MeshChecker(object):
    def __init__(self, path):
        self._om2_mesh_opt = Om2MeshOpt(path)

    def get_unused_vertex_comp_names(self):
        lis = []
        om2_obj_fnc = self._om2_mesh_opt._om2_obj_fnc
        om2_vertex_itr = om2.MItMeshVertex(om2_obj_fnc.object())
        for i_vertex_index in range(om2_obj_fnc.numVertices):
            om2_vertex_itr.setIndex(i_vertex_index)
            if not om2_vertex_itr.numConnectedFaces():
                lis.append(i_vertex_index)
        return Om2Method._get_mesh_vertex_comp_names_(lis)

    def set_unused_vertices_delete(self):
        cs = self.get_unused_vertex_comp_names()
        for i_c in Om2Method._get_mesh_vertex_comp_names_(cs):
            p = '{}.{}'.format(self._om2_mesh_opt.path, i_c)
            cmds.delete(p)


class MeshToSurfaceConverter(object):
    def __init__(self, mesh_om2_fnc):
        self._mesh_om2_obj_fnc = mesh_om2_fnc
        #
        self._corner_index = 0
        self._rotation = 1
    @classmethod
    def _get_center_point_(cls, point_0, point_1):
        x, y, z = (point_0.x + point_1.x) / 2, (point_0.y + point_1.y) / 2, (point_0.z + point_1.z) / 2
        return om2.MPoint(x, y, z)
    @classmethod
    def _get_next_comp_index_(cls, comp_index, comp_indices, rotation, step):
        def move_fnc_(i_):
            if rotation > 0:
                if i_ == maximum_index:
                    _n_i = 0
                else:
                    _n_i = i_ + 1
            else:
                if i_ == 0:
                    _n_i = maximum_index
                else:
                    _n_i = i_ - 1
            return _n_i
        #
        comp_indices = list(comp_indices)
        maximum_index = len(comp_indices) - 1
        i = comp_indices.index(comp_index)
        for _ in range(step):
            i = move_fnc_(i)
        return comp_indices[i]
    @classmethod
    def _get_next_edge_vertex_index_(cls, edge_vertex_index, om2_edge_itr):
        edge_vertex_indices = [om2_edge_itr.vertexId(i) for i in range(2)]
        edge_vertex_indices.remove(edge_vertex_index)
        return edge_vertex_indices[0]
    @classmethod
    def _get_border_next_vertex_index_(cls, vertex_index, edge_index, om2_vertex_itr, om2_edge_itr, rotation, step):
        om2_vertex_itr.setIndex(vertex_index)
        om2_edge_itr.setIndex(edge_index)
        #
        next_vertex_index = cls._get_next_edge_vertex_index_(vertex_index, om2_edge_itr)
        #
        om2_vertex_itr.setIndex(next_vertex_index)
        next_edge_indices = om2_vertex_itr.getConnectedEdges()
        next_edge_index = cls._get_next_comp_index_(
            edge_index, next_edge_indices, rotation, step
        )
        return next_vertex_index, next_edge_index

    def _get_corner_vertex_indices_at_(self, vertex_index, include_vertex_indices, rotation):
        self._mesh_om2_vertex_itr.setIndex(vertex_index)
        #
        start_edge_indices = self._mesh_om2_vertex_itr.getConnectedEdges()
        if rotation == -1:
            start_edge_index = start_edge_indices[1]
        else:
            start_edge_index = start_edge_indices[0]
        self._mesh_om2_edge_itr.setIndex(start_edge_index)
        #
        return self._get_vertex_indices_at_(
            vertex_index, start_edge_index, include_vertex_indices, rotation, step=1
        )

    def _get_border_vertex_indices_at_(self, vertex_index, include_vertex_indices, rotation):
        self._mesh_om2_vertex_itr.setIndex(vertex_index)
        start_edge_indices = self._mesh_om2_vertex_itr.getConnectedEdges()
        # temp
        start_edge_index = start_edge_indices[1]
        self._mesh_om2_edge_itr.setIndex(start_edge_index)
        #
        return self._get_vertex_indices_at_(
            vertex_index, start_edge_index, include_vertex_indices, rotation, step=2
        )

    def _get_vertex_indices_at_(self, start_vertex_index, start_edge_index, include_vertex_indices, rotation, step):
        lis = [start_vertex_index]
        #
        depth = 0
        maximum_depth = 1000
        #
        current_vertex_index = start_vertex_index
        current_edge_index = start_edge_index
        #
        is_end = False
        while is_end is False:
            current_vertex_index, current_edge_index = self._get_border_next_vertex_index_(
                current_vertex_index, current_edge_index,
                self._mesh_om2_vertex_itr, self._mesh_om2_edge_itr,
                rotation, step
            )
            #
            lis.append(current_vertex_index)
            #
            if current_vertex_index in include_vertex_indices:
                is_end = True
            #
            if depth == maximum_depth:
                is_end = True
            #
            depth += 1
        return lis

    def _set_mesh_data_update_(self):
        self._mesh_om2_vertex_itr = om2.MItMeshVertex(self._mesh_om2_obj_fnc.object())
        self._mesh_om2_edge_itr = om2.MItMeshEdge(self._mesh_om2_obj_fnc.object())
        #
        self._mesh_points = self._mesh_om2_obj_fnc.getPoints(space=4)
        #
        self._set_border_vertex_indices_update_()

    def _set_border_vertex_indices_update_(self):
        self._corner_vertex_indices, self._border_vertex_indices = [], []
        om2_vertex_itr = om2.MItMeshVertex(self._mesh_om2_obj_fnc.object())
        vertex_indices = range(om2_vertex_itr.count())
        for vertex_index in vertex_indices:
            om2_vertex_itr.setIndex(vertex_index)
            if om2_vertex_itr.onBoundary() is True:
                if len(om2_vertex_itr.getConnectedFaces()) == 1:
                    self._corner_vertex_indices.append(vertex_index)
                else:
                    self._border_vertex_indices.append(vertex_index)

    def _set_surface_data_update_(self):
        self._set_surface_vertex_indices_update_()
        self._set_surface_points_update_()

    def _set_surface_vertex_indices_update_(self):
        self._surface_grid_vertex_indices_0 = []
        #
        vertex_index = self._corner_vertex_indices[self._corner_index]
        border_start_u_vertex_indices = self._get_corner_vertex_indices_at_(
            vertex_index, self._corner_vertex_indices,
            self._rotation
        )
        border_v_vertex_indices = self._get_corner_vertex_indices_at_(
            vertex_index, self._corner_vertex_indices,
            -self._rotation
        )
        border_end_u_vertex_indices = self._get_corner_vertex_indices_at_(
            border_v_vertex_indices[-1], self._corner_vertex_indices,
            -self._rotation
        )
        self._surface_u_count, self._surface_v_count = len(border_start_u_vertex_indices), len(border_v_vertex_indices)
        #
        for seq, border_v_index in enumerate(border_v_vertex_indices):
            if seq == 0:
                u_vertex_indices = border_start_u_vertex_indices
            elif seq == self._surface_v_count - 1:
                u_vertex_indices = border_end_u_vertex_indices
            else:
                u_vertex_indices = self._get_border_vertex_indices_at_(
                    border_v_index, self._border_vertex_indices,
                    self._rotation
                )
            self._surface_grid_vertex_indices_0.append(u_vertex_indices)

        self._surface_grid_vertex_indices_1 = zip(*self._surface_grid_vertex_indices_0)

    def _set_surface_points_update_(self):
        self._surface_points = []
        v_count = len(self._surface_grid_vertex_indices_1)
        for v_index, u_vertex_indices in enumerate(self._surface_grid_vertex_indices_1):
            u_points = self._get_center_u_points_at_(v_index)
            if v_index == 0:
                center_u_points = self._get_center_u_points_between_(
                    v_index, v_index+1
                )
                self._surface_points.extend(u_points+center_u_points)
            elif v_index == v_count-1:
                center_u_points = self._get_center_u_points_between_(
                    v_index-1, v_index
                )
                self._surface_points.extend(center_u_points+u_points)
            else:
                self._surface_points.extend(u_points)

    def _get_center_u_points_at_(self, v_index):
        u_vertex_indices = self._surface_grid_vertex_indices_1[v_index]
        u_count = len(u_vertex_indices)
        u_points = []
        for u_index in range(u_count):
            u_vertex_index = u_vertex_indices[u_index]
            u_point = self._mesh_points[u_vertex_index]
            if u_index == 0:
                next_u_point = self._mesh_points[u_vertex_indices[u_index + 1]]
                center_u_point = self._get_center_point_(u_point, next_u_point)
                u_points.extend([u_point, center_u_point])
            elif u_index == u_count - 1:
                pre_u_point = self._mesh_points[u_vertex_indices[u_index - 1]]
                center_u_point = self._get_center_point_(pre_u_point, u_point)
                u_points.extend([center_u_point, u_point])
            else:
                u_points.append(u_point)
        return u_points
    #
    def _get_center_u_points_between_(self, v_index_0, v_index_1):
        u_vertex_indices_0 = self._surface_grid_vertex_indices_1[v_index_0]
        u_vertex_indices_1 = self._surface_grid_vertex_indices_1[v_index_1]
        u_count = len(u_vertex_indices_0)
        u_points = []
        for u_index, u_vertex_index_0 in enumerate(u_vertex_indices_0):
            u_vertex_index_1 = u_vertex_indices_1[u_index]
            #
            u_point_0 = self._mesh_points[u_vertex_index_0]
            u_point_1 = self._mesh_points[u_vertex_index_1]
            u_point = self._get_center_point_(u_point_0, u_point_1)
            if u_index == 0:
                next_u_point_0 = self._mesh_points[u_vertex_indices_0[u_index+1]]
                next_u_point_1 = self._mesh_points[u_vertex_indices_1[u_index+1]]
                center_u_point_0 = self._get_center_point_(u_point_0, next_u_point_0)
                center_u_point_1 = self._get_center_point_(u_point_1, next_u_point_1)
                center_u_point = self._get_center_point_(center_u_point_0, center_u_point_1)
                u_points.extend([u_point, center_u_point])
            elif u_index == u_count-1:
                pre_u_point_0 = self._mesh_points[u_vertex_indices_0[u_index-1]]
                pre_u_point_1 = self._mesh_points[u_vertex_indices_1[u_index-1]]
                center_u_point_0 = self._get_center_point_(pre_u_point_0, u_point_0)
                center_u_point_1 = self._get_center_point_(pre_u_point_1, u_point_1)
                center_u_point = self._get_center_point_(center_u_point_0, center_u_point_1)
                u_points.extend([center_u_point, u_point])
            else:
                u_points.append(u_point)
        return u_points

    def set_run(self):
        self._set_mesh_data_update_()
        self._set_surface_data_update_()
        Om2SurfaceOpt.set_create(
            'test', self._surface_u_count, self._surface_v_count, self._surface_points
        )


class Om2SurfaceOpt(object):
    def __init__(self, path):
        self._om2_obj_fnc = Om2Method._get_om2_nurbs_surface_fnc_(path)
    @property
    def path(self):
        return self._om2_obj_fnc.fullPathName()

    def get_points(self, round_count=None):
        return Om2Method._get_point_array_(
            self._om2_obj_fnc.cvPositions(),
            round_count
        )

    def get_count(self):
        return self._om2_obj_fnc.numCVsInU, self._om2_obj_fnc.numCVsInV

    def get_knots(self):
        return self._om2_obj_fnc.knotsInU(), self._om2_obj_fnc.knotsInV()

    def get_degree(self):
        return self._om2_obj_fnc.degreeInU, self._om2_obj_fnc.degreeInV

    def get_form(self):
        return self._om2_obj_fnc.formInU, self._om2_obj_fnc.formInV

    def get_points_(self, u_division, v_division):
        lis = []
        u_p_max, u_p_min = self._om2_obj_fnc.knotDomainInU
        v_p_max, v_p_min = self._om2_obj_fnc.knotDomainInV
        for u_index in range(u_division):
            u_percent = float(u_index)/float(u_division-1)
            u_p = Om2Method._set_value_map_(
                (0, 1), (u_p_max, u_p_min), u_percent
            )
            for v_index in range(v_division):
                v_percent = float(v_index) / float(v_division-1)
                v_p = Om2Method._set_value_map_(
                    (0, 1), (v_p_max, v_p_min), v_percent
                )
                lis.append(
                    Om2Method._get_point_(
                        self._om2_obj_fnc.getPointAtParam(u_p, v_p, 4)
                    )
                )
        return lis

    def get_v_points(self, sample):
        pass

    def set_convert_to_mesh(self):
        def set_face_vertices_update_fnc_():
            _v_face_count = mesh_v_face_count - 2
            _u_face_count = mesh_u_face_count - 2
            #
            _l = [0, 1, 2 + _u_face_count, 1 + _u_face_count]
            for _v_face_index in range(_v_face_count):
                for _u_face_index in range(_u_face_count):
                    mesh_face_vertex_counts.append(4)
                    if _u_face_index == 0:
                        __l = [(i + _v_face_index * (_u_face_count + 1)) for i in _l]
                    else:
                        __l = [(i + _v_face_index * (_u_face_count + 1) + _u_face_index) for i in _l]
                    #
                    mesh_face_vertex_indices.extend(__l)
        #
        def set_points_update_fnc_():
            # u = 5, v = 4
            # [0, 4, 8, 12, 16, 1, 5, 9, 13, 17, 2, 6, 10, 14, 18, 3, 7, 11, 15, 19]
            _v_point_count = surface_v_count
            _u_point_count = surface_u_count
            #
            _exclude_v_point_indices = [1, _v_point_count-2]
            _exclude_u_point_indices = [1, _u_point_count-2]
            for _v_point_index in range(_v_point_count):
                if _v_point_index in _exclude_v_point_indices:
                    continue
                #
                _map_v_coord = float(_v_point_index) / float(_v_point_count - 3)
                for _u_point_index in range(_u_point_count):
                    if _u_point_index in _exclude_u_point_indices:
                        continue
                    _index = _u_point_index*_v_point_count + _v_point_index
                    #
                    mesh_points.append(surface_points[_index])
                    #
                    _map_u_coord = float(_u_point_index) / float(_u_point_count-3)
                    mesh_map_coords.append(
                        (_map_u_coord, _map_v_coord)
                    )
        #
        surface_v_count = self._om2_obj_fnc.numCVsInV
        surface_u_count = self._om2_obj_fnc.numCVsInU
        surface_points = self.get_points()
        #
        mesh_v_face_count = surface_v_count-1
        mesh_u_face_count = surface_u_count-1
        #
        mesh_face_vertex_counts, mesh_face_vertex_indices = [], []
        mesh_points = []
        mesh_map_coords = []
        #
        set_face_vertices_update_fnc_()
        set_points_update_fnc_()
        #
        Om2MeshOpt.set_create(
            'test',
            (mesh_face_vertex_counts, mesh_face_vertex_indices),
            mesh_points,
            mesh_map_coords
        )

    def set_convert_to_mesh_(self, u_division, v_division):
        def set_face_vertices_update_fnc_():
            _v_face_count = mesh_v_face_count
            _u_face_count = mesh_u_face_count
            #
            _l = [0, 1, 2 + _u_face_count, 1 + _u_face_count]
            for _v_face_index in range(_v_face_count):
                for _u_face_index in range(_u_face_count):
                    mesh_face_vertex_counts.append(4)
                    if _u_face_index == 0:
                        __l = [(i + _v_face_index * (_u_face_count + 1)) for i in _l]
                    else:
                        __l = [(i + _v_face_index * (_u_face_count + 1) + _u_face_index) for i in _l]
                    #
                    mesh_face_vertex_indices.extend(__l)
        #
        def set_points_update_fnc_():
            # u = 5, v = 4
            # [0, 4, 8, 12, 16, 1, 5, 9, 13, 17, 2, 6, 10, 14, 18, 3, 7, 11, 15, 19]
            _v_point_count = surface_v_count
            _u_point_count = surface_u_count
            #
            _exclude_v_point_indices = [1, _v_point_count-2]
            _exclude_u_point_indices = [1, _u_point_count-2]
            for _v_point_index in range(_v_point_count):
                _map_v_coord = float(_v_point_index)/float(_v_point_count-1)
                for _u_point_index in range(_u_point_count):
                    _index = _u_point_index*_v_point_count + _v_point_index
                    #
                    mesh_points.append(
                        surface_points[_index]
                    )
                    _map_u_coord = float(_u_point_index)/float(_u_point_count-1)
                    mesh_map_coords.append(
                        (_map_u_coord, _map_v_coord)
                    )
        #
        surface_v_count = u_division
        surface_u_count = v_division
        surface_points = self.get_points_(
            surface_u_count,
            surface_v_count
        )
        #
        mesh_v_face_count = surface_v_count-1
        mesh_u_face_count = surface_u_count-1
        #
        mesh_face_vertex_counts, mesh_face_vertex_indices = [], []
        mesh_points = []
        mesh_map_coords = []
        #
        set_face_vertices_update_fnc_()
        set_points_update_fnc_()
        #
        Om2MeshOpt.set_create(
            'test',
            (mesh_face_vertex_counts, mesh_face_vertex_indices),
            mesh_points,
            mesh_map_coords
        )
    @staticmethod
    def _get_surface_knots_(count, degree, form):
        if form == 1:
            lis = []
            span = max(count - 3, 1)
            M = span
            N = degree
            knot_minimum, knot_maximum = 0.0, 1.0
            #
            add_count = count - N - 1
            [lis.append(knot_minimum) for _ in range(degree)]
            #
            for seq in range(add_count):
                lis.append(float(seq + 1) * knot_maximum / (add_count + 1))
            #
            [lis.append(knot_maximum) for _ in range(degree)]
            return lis
        elif form == 3:
            span = max(count - 3, 1)
            M = span
            N = degree
            lis = []
            knot_minimum, knot_maximum = 0.0, float(M)+1
            #
            [lis.append(knot_minimum + i - degree + 1) for i in range(degree)]
            #
            add_count = count - N - 1
            for seq in range(add_count):
                lis.append(float(seq + 1) * knot_maximum / (add_count + 1))
            #
            [lis.append(knot_maximum + i) for i in range(degree)]
            return lis
    @classmethod
    def set_create(cls, name, u_count, v_count, points, u_form=1, v_form=3):
        u_degree, v_degree = 3, 2
        u_form, v_form = u_form, v_form

        u_knots, v_knots = (
            cls._get_surface_knots_(u_count, u_degree, u_form),
            cls._get_surface_knots_(v_count, v_degree, v_form)
        )
        transform = cmds.createNode('transform', name=name)
        om2_obj = om2.MFnNurbsSurface()
        om2_obj.create(
            points,
            u_knots, v_knots,
            u_degree, v_degree,
            u_form, v_form,
            True,
            parent=Om2Method._get_om2_dag_obj_(transform)
        )


class CmdXgenSplineGuideOpt(object):
    def __init__(self, path):
        self._om2_obj_fnc = Om2Method._get_om2_dag_node_fnc_(path)
        self._obj_path = self._om2_obj_fnc.fullPathName()
    @property
    def path(self):
        return self._obj_path

    def get_control_points(self):
        lis = []
        # xgmGuideGeom [-guide STRING] [-numVertices] [-basePoint | -controlPoints] [-lockBasePt BOOL] [-guideNormal] [-uvLocation] [-isCached]
        _ = cmds.xgmGuideGeom(guide=self._obj_path, controlPoints=1)
        for seq, i in enumerate(_):
            if not seq % 3:
                lis.append(tuple([_[seq + j] for j in range(3)]))
        return lis

    def get_vertex_points(self):
        lis = []
        _ = cmds.xgmGuideGeom(guide=self._obj_path, numVertices=True) or []
        if _:
            c = _[0]
            for i in range(int(c)):
                lis.append(cmds.getAttr('xgGuide1Shape.vtx[{}]'.format(i))[0])
        return lis

    def _test_(self):
        cmd = 'curve -d '
        cmd += '1'
        _ = cmds.xgmGuideGeom(guide=self._obj_path, numVertices=True) or []
        if _:
            c = _[0]
            for i in range(int(c)):
                cmd += ' -p '
                cmd += ' '.join([str(i) for i in cmds.getAttr('xgGuide1Shape.vtx[{}]'.format(i))[0]])
        print cmd


class ObjOpt(object):
    def __init__(self, path):
        self._om2_obj_fnc = Om2Method._get_om2_obj_(path)
        self._obj_path = self._om2_obj_fnc.name()

    def _test_(self):
        p = self._om2_obj_fnc.findPlug('inputXgenGuide', 0)
        s = p.source()
        if s.isNull is False:
            obj = om2.MFnDagNode(s.node())
            print obj.fullPathName()

    def get_port(self, port_path):
        p = self._om2_obj_fnc.findPlug(port_path, 0)
        return p


class ScriptJobMtd(object):
    # dbTraceChanged
    # resourceLimitStateChange
    # linearUnitChanged
    # timeUnitChanged
    # angularUnitChanged
    # Undo
    # undoSupressed
    # Redo
    # customEvaluatorChanged
    # serialExecutorFallback
    # timeChanged
    # currentContainerChange
    # quitApplication
    # idleHigh
    # idle
    # idleVeryLow
    # RecentCommandChanged
    # ToolChanged
    # PostToolChanged
    # ToolDirtyChanged
    # ToolSettingsChanged
    # DisplayRGBColorChanged
    # animLayerRebuild
    # animLayerRefresh
    # animLayerAnimationChanged
    # animLayerLockChanged
    # animLayerBaseLockChanged
    # animLayerGhostChanged
    # cteEventKeyingTargetForClipChanged
    # cteEventKeyingTargetForLayerChanged
    # cteEventKeyingTargetForInvalidChanged
    # teClipAdded
    # teClipModified
    # teClipRemoved
    # teCompositionAdded
    # teCompositionRemoved
    # teCompositionActiveChanged
    # teCompositionNameChanged
    # teMuteChanged
    # cameraChange
    # cameraDisplayAttributesChange
    # SelectionChanged
    # PreSelectionChangedTriggered
    # LiveListChanged
    # ActiveViewChanged
    # SelectModeChanged
    # SelectTypeChanged
    # SelectPreferenceChanged
    # DisplayPreferenceChanged
    # DagObjectCreated
    # transformLockChange
    # renderLayerManagerChange
    # renderLayerChange
    # displayLayerManagerChange
    # displayLayerAdded
    # displayLayerDeleted
    # displayLayerVisibilityChanged
    # displayLayerChange
    # renderPassChange
    # renderPassSetChange
    # renderPassSetMembershipChange
    # passContributionMapChange
    # DisplayColorChanged
    # lightLinkingChanged
    # lightLinkingChangedNonSG
    # UvTileProxyDirtyChangeTrigger
    # preferredRendererChanged
    # polyTopoSymmetryValidChanged
    # SceneSegmentChanged
    # PostSceneSegmentChanged
    # SequencerActiveShotChanged
    # ColorIndexChanged
    # deleteAll
    # NameChanged
    # symmetricModellingOptionsChanged
    # softSelectOptionsChanged
    # SetModified
    # xformConstraintOptionsChanged
    # metadataVisualStatusChanged
    # undoXformCmd
    # redoXformCmd
    # freezeOptionsChanged
    # linearToleranceChanged
    # angularToleranceChanged
    # nurbsToPolygonsPrefsChanged
    # nurbsCurveRebuildPrefsChanged
    # constructionHistoryChanged
    # threadCountChanged
    # SceneSaved
    # NewSceneOpened
    # SceneOpened
    # SceneImported
    # PreFileNewOrOpened
    # PreFileNew
    # PreFileOpened
    # PostSceneRead
    # renderSetupAutoSave
    # workspaceChanged
    # PolyUVSetChanged
    # PolyUVSetDeleted
    # selectionConstraintsChanged
    # nurbsToSubdivPrefsChanged
    # startColorPerVertexTool
    # stopColorPerVertexTool
    # start3dPaintTool
    # stop3dPaintTool
    # DragRelease
    # ModelPanelSetFocus
    # modelEditorChanged
    # MenuModeChanged
    # gridDisplayChanged
    # interactionStyleChanged
    # axisAtOriginChanged
    # CurveRGBColorChanged
    # SelectPriorityChanged
    # snapModeChanged
    # texWindowEditorImageBaseColorChanged
    # texWindowEditorCheckerDensityChanged
    # texWindowEditorCheckerDisplayChanged
    # texWindowEditorDisplaySolidMapChanged
    # texWindowEditorShowup
    # texWindowEditorClose
    # profilerSelectionChanged
    # activeHandleChanged
    # ChannelBoxLabelSelected
    # colorMgtOCIORulesEnabledChanged
    # colorMgtUserPrefsChanged
    # RenderSetupSelectionChanged
    # colorMgtEnabledChanged
    # colorMgtConfigFileEnableChanged
    # colorMgtConfigFilePathChanged
    # colorMgtConfigChanged
    # colorMgtWorkingSpaceChanged
    # colorMgtPrefsViewTransformChanged
    # colorMgtPrefsReloaded
    # colorMgtOutputChanged
    # colorMgtPlayblastOutputChanged
    # colorMgtRefreshed
    # selectionPipelineChanged
    # currentSoundNodeChanged
    # graphEditorChanged
    # graphEditorParamCurveSelected
    # graphEditorOutlinerHighlightChanged
    # graphEditorOutlinerListChanged
    # glFrameTrigger
    # EditModeChanged
    # playbackRangeAboutToChange
    # playbackSpeedChanged
    # playbackModeChanged
    # playbackRangeSliderChanged
    # playbackByChanged
    # playbackRangeChanged
    # RenderViewCameraChanged
    # texScaleContextOptionsChanged
    # texRotateContextOptionsChanged
    # texMoveContextOptionsChanged
    # polyCutUVSteadyStrokeChanged
    # polyCutUVEventTexEditorCheckerDisplayChanged
    # polyCutUVShowTextureBordersChanged
    # polyCutUVShowUVShellColoringChanged
    # shapeEditorTreeviewSelectionChanged
    # poseEditorTreeviewSelectionChanged
    # sculptMeshCacheBlendShapeListChanged
    # sculptMeshCacheCloneSourceChanged
    # RebuildUIValues
    # cacheDestroyed
    # cachingPreferencesChanged
    # cachingSafeModeChanged
    # cachingEvaluationModeChanged
    # teTrackAdded
    # teTrackRemoved
    # teTrackNameChanged
    # teTrackModified
    # cteEventClipEditModeChanged
    # teEditorPrefsChanged
    @classmethod
    def get_all(cls):
        return cmds.scriptJob(listJobs=1) or []
    @classmethod
    def set_delete(cls, pattern):
        _ = fnmatch.filter(cls.get_all(), pattern)
        if _:
            for i in _:
                index = i.split(': ')[0]
                cmds.scriptJob(kill=int(index), force=1)
                utl_core.Log.set_module_result_trace(
                    'job-script kill',
                    'job-script="{}"'.format(i.lstrip().rstrip())
                )


class CmdAtrQueryOpt(object):
    PORT_PATHSEP = ma_configure.Util.PORT_PATHSEP
    def __init__(self, atr_path):
        self._atr_path = atr_path
        _ = atr_path.split(self.PORT_PATHSEP)
        self._obj_path, self._port_path = _[0], self._get_port_path_(self.PORT_PATHSEP.join(_[1:]))
    @classmethod
    def _get_port_path_(cls, port_path):
        _ = port_path.split('.')[-1]
        if _.endswith(']'):
            return _.split('[')[0]
        return _
    #
    @property
    def atr_path(self):
        return self._atr_path
    @property
    def obj_path(self):
        return self._obj_path
    @property
    def port_path(self):
        return self._port_path

    def get_type(self):
        return cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            attributeType=1
        )
    type = property(get_type)
    #
    def get_is_exists(self):
        return cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            exists=1
        )

    def get_parent_path(self):
        _ = cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            listParent=1
        )
        if _ is not None:
            return _[0]

    def get_channel_names(self, alpha=True):
        _ = cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            numberOfChildren=1
        )
        if _ is not None:
            names = cmds.attributeQuery(
                self.port_path,
                node=self.obj_path,
                listChildren=1
            ) or []
            if alpha is True:
                if self.port_path == 'outColor':
                    alpha_port_path = 'outAlpha'
                else:
                    alpha_port_path = '{}A'.format(self.port_path)
                if cmds.attributeQuery(
                    alpha_port_path,
                    node=self.obj_path,
                    exists=1
                ) is True:
                    names.append(alpha_port_path)
            return names
        return []

    def get_is_channel(self):
        return cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            listParent=1
        ) is not None

    def get_alpha_channel_name(self):
        if self.port_path == 'outColor':
            alpha_port_path = 'outAlpha'
        else:
            alpha_port_path = '{}A'.format(self.port_path)
        if cmds.attributeQuery(
                self._get_port_path_(alpha_port_path),
                node=self.obj_path,
                exists=1
        ) is True:
            return alpha_port_path

    def get_element_indices(self):
        _ = cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            multi=1
        )
        if _ is True:
            return [int(i) for i in cmds.getAttr(self.atr_path, multiIndices=1, silent=1) or []]

    def get_is_enumerate(self):
        return cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            enum=1
        )

    def get_enumerate_strings(self):
        _ = cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            listEnum=1
        )
        if _:
            return _[0].split(':')
        return []

    def get_default(self):
        _ = cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            listDefault=1
        )
        if _:
            if self.get_channel_names():
                return tuple(_)
            return _[0]

    def set(self):
        pass


class CmdPortQueryOpt(object):
    PATHSEP = '.'
    def __init__(self, obj_type_name, port_query_path):
        self._obj_type_name = obj_type_name
        self._port_query_path = port_query_path

    def get_obj_type_name(self):
        return self._obj_type_name

    def get_port_query_path(self):
        return self._port_query_path
    
    def __get_query_key_(self):
        _ = self._port_query_path.split(self.PATHSEP)[-1]
        if _.endswith(u']'):
            return _.split(u'[')[0]
        return _

    def __get_query_kwargs_(self, obj_path, **kwargs):
        if obj_path is not None:
            kwargs['node'] = obj_path
        else:
            kwargs['type'] = self.get_obj_type_name()
        return kwargs

    def get_type_name(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, attributeType=True)
        )

    def get_has_channels(self, obj_path=None):
        return (cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, listChildren=True)
        ) or []) != []

    def get_channel_names(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, listChildren=True)
        ) or []

    def get_child_names(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, listChildren=True)
        ) or []

    def get_parent_name(self, obj_path=None):
        _ = cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, listParent=True)
        )
        if _:
            return _[0]

    def get_has_parent(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, listParent=True)
        ) is not None
    
    def get_is_array(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, multi=True)
        ) or False

    def get_is_writable(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, writable=True)
        ) or False

    def get_is_readable(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, readable=True)
        ) or False

    def get_is_message(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, readable=True)
        ) or False

    def get_is_enumerate(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, enum=True)
        ) or False
    #
    def get_enumerate_strings(self, obj_path=None):
        _ = cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, listEnum=True)
        )
        if _:
            return _[0].split(':')
        return []

    def get_short_name(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, shortName=True)
        )

    def get_ui_name(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, niceName=True)
        )

    def get_default(self, obj_path=None):
        _ = cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, listDefault=True)
        )
        if _:
            if self.get_has_channels() is True:
                return tuple(_)
            return _[0]

    def __str__(self):
        return '{}(path="{}.{}")'.format(
            self.get_type_name(), self.get_obj_type_name(), self.get_port_query_path()
        )


class CmdCustomizePortQueryOpt(object):
    pass


class CmdObjQueryOpt(object):
    def __init__(self, obj_type_name):
        self._obj_type_name = obj_type_name
    #
    def get_type_name(self):
        return self._obj_type_name
    @classmethod
    def _set_cleanup_to_(cls, lis):
        lis_ = list(filter(None, set(lis)))
        lis_.sort(key=lis.index)
        return lis_

    def get_port_query_is_exists(self, port_query_path):
        return cmds.attributeQuery(
            port_query_path,
            type=self.get_type_name(),
            exists=1
        )

    def get_port_query(self, port_query_path):
        return CmdPortQueryOpt(
            self.get_type_name(),
            port_query_path
        )

    def get_port_query_paths(self):
        def rcs_fnc_(port_query_path_):
            _child_names = self.get_port_query(
                port_query_path_
            ).get_channel_names()
            if _child_names:
                for _i in _child_names:
                    _i_port_query_path = u'{}.{}'.format(port_query_path_, _i)
                    lis.append(_i_port_query_path)
                    rcs_fnc_(_i_port_query_path)
        #
        lis = []
        #
        _ = self._set_cleanup_to_(
            cmds.attributeInfo(
                allAttributes=True,
                type=self.get_type_name()
            ) or []
        )
        if _:
            for port_query_path in _:
                if self.get_port_query(port_query_path).get_has_parent() is False:
                    lis.append(port_query_path)
                    rcs_fnc_(port_query_path)
        return lis

    def get_port_queries(self):
        return [
            self.get_port_query(i) for i in self.get_port_query_paths()
        ]


class CmdPortOpt(object):
    PATHSEP = '.'
    def __init__(self, obj_path, port_path):
        self._obj_path = obj_path
        self._port_path = port_path
        _ = '.'.join(
            [self._obj_path, port_path]
        )
        self._atr_path = self._get_atr_path_(
            self._obj_path, self._port_path
        )
        if cmds.objExists(self._atr_path) is True:
            self._port_type = cmds.getAttr(self._atr_path, type=1)
            self._port_query = CmdPortQueryOpt(
                CmdObjOpt(obj_path).get_type_name(),
                self._port_path
            )
            self._atr_query = CmdAtrQueryOpt(self._atr_path)
        else:
            raise RuntimeError()
    @classmethod
    def _set_create_(cls, obj_path, port_path, type_name, enumerate_strings=None):
        if cls._get_is_exists_(obj_path, port_path) is False:
            if type_name == 'string':
                cmds.addAttr(
                    obj_path,
                    longName=port_path,
                    dataType=type_name
                )
            elif type_name == 'enum':
                if isinstance(enumerate_strings, (tuple, list)):
                    cmds.addAttr(
                        obj_path,
                        longName=port_path,
                        attributeType=type_name,
                        enumName=':'.join(enumerate_strings)
                    )
                else:
                    cmds.addAttr(
                        obj_path,
                        longName=port_path,
                        attributeType=type_name
                    )
            else:
                cmds.addAttr(
                    obj_path,
                    longName=port_path,
                    attributeType=type_name
                )
    @classmethod
    def _get_is_exists_(cls, obj_path, port_path):
        atr_path = cls._get_atr_path_(obj_path, port_path)
        return cmds.objExists(atr_path)
    @classmethod
    def _get_atr_path_(cls, obj_path, port_path):
        return cls.PATHSEP.join(
            [obj_path, port_path]
        )
    @classmethod
    def _set_connection_create_(cls, atr_path_src, atr_path_tgt):
        if cmds.isConnected(atr_path_src, atr_path_tgt) is False:
            if cmds.getAttr(atr_path_tgt, lock=1) is False:
                cmds.connectAttr(atr_path_src, atr_path_tgt, force=1)

    def get_port_query(self):
        return self._port_query

    def get_obj_path(self):
        return self._obj_path
    obj_path = property(get_obj_path)

    def get_type_name(self):
        return self._port_type
    type_name = property(get_type_name)

    def get_path(self):
        return self._atr_path
    path = property(get_path)

    def get_atr_path(self):
        return self._atr_path
    atr_path = property(get_atr_path)

    def get_port_path(self):
        return self._port_path
    port_path = property(get_port_path)

    def get_array_indices(self):
        if self.get_port_query().get_is_array(self.get_obj_path()) is True:
            return cmds.getAttr(
                '.'.join([self.get_obj_path(), self.get_port_path()]),
                multiIndices=1,
                silent=1
            ) or []
        return []

    def get(self, as_string=False):
        if self.get_type_name() == 'message':
            return None
        elif self.get_type_name() == 'TdataCompound':
            return None
        if as_string is True:
            return cmds.getAttr(self.path, asString=True) or ''
        #
        _ = cmds.getAttr(self.get_path())
        if self.get_port_query().get_has_channels(self.get_obj_path()):
            return _[0]
        return _

    def set(self, value, enumerate_strings=None):
        if self.get_has_source() is False:
            # unlock first
            is_lock = cmds.getAttr(self.get_path(), lock=1)
            if is_lock:
                cmds.setAttr(self.get_path(), lock=0)
            #
            if self.get_port_query().get_is_writable(self.get_obj_path()) is True:
                if self.get_type_name() == 'string':
                    cmds.setAttr(self.get_path(), value, type=self.get_type_name())
                elif self.get_type_name() == 'enum':
                    if enumerate_strings is not None:
                        cmds.addAttr(
                            self.get_path(),
                            enumName=':'.join(enumerate_strings),
                            edit=1
                        )
                    #
                    if isinstance(value, six.string_types):
                        enumerate_strings = self.get_port_query().get_enumerate_strings(self.get_obj_path())
                        index = enumerate_strings.index(value)
                        cmds.setAttr(self.get_path(), index)
                    else:
                        cmds.setAttr(self.get_path(), value)
                else:
                    if isinstance(value, (tuple, list)):
                        cmds.setAttr(self.get_path(), *value, clamp=1)
                    else:
                        # Debug ( Clamp Maximum or Minimum Value )
                        cmds.setAttr(self.get_path(), value, clamp=1)
    
    def get_default(self):
        if self.get_type_name() == 'message':
            return None
        elif self.get_type_name() == 'TdataCompound':
            return None
        #
        _ = self.get_port_query().get_default()
        if self.get_type_name() == 'bool':
            return bool(int(_))
        elif self.get_type_name() == 'matrix':
            return [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        return _

    def get_is_changed(self):
        return self.get() != self.get_default()

    def get_is_enumerate(self):
        return self.get_port_query().get_is_enumerate(self.get_obj_path())

    def get_enumerate_strings(self):
        return self.get_port_query().get_enumerate_strings(
            self.get_obj_path()
        )

    def set_enumerate_strings(self, strings):
        cmds.addAttr(
            self._atr_path,
            edit=1, enumName=':'.join(strings)
        )

    def get_has_source(self):
        _ = cmds.connectionInfo(
            self.get_path(), isExactDestination=True
        )
        if self.get_port_query().get_has_channels(self.get_obj_path()) is True:
            return cmds.connectionInfo(
                self.get_path(), isDestination=True
            )
        elif self.get_port_query().get_has_parent(self.get_obj_path()) is True:
            return cmds.connectionInfo(
                self.get_path(), isDestination=True
            )
        return _

    def get_has_source_(self, exact=False):
        if exact is True:
            return cmds.connectionInfo(
                self.get_path(), isExactDestination=True
            )
        return cmds.connectionInfo(
            self.get_path(), isDestination=True
        )

    def get_source(self):
        _ = cmds.connectionInfo(
            self.get_path(),
            sourceFromDestination=1
        )
        if _:
            a = bsc_core.DccAttrPathOpt(_)
            obj_path = a.obj_path
            port_path = a.port_path
            return self.PATHSEP.join(
                [CmdObjOpt(obj_path).get_path(), port_path]
            )

    def set_disconnect(self):
        source = self.get_source()
        if source:
            cmds.disconnectAttr(source, self.get_path())

    def set_default(self):
        default_value = self.get_default()
        if default_value is not None:
            self.set(default_value)

    def get_is_naming_match(self, pattern):
        return fnmatch.filter(
            [self.get_port_path()], pattern
        ) != []
    def get_is_naming_matches(self, patterns):
        for i in patterns:
            if self.get_is_naming_match(i) is True:
                return True
        return False
    def __str__(self):
        return '{}(path="{}")'.format(
            self.get_type_name(), self.get_path()
        )

    def __repr__(self):
        return self.__str__()


class CmdAtrOpt(object):
    PATHSEP = '.'
    def __init__(self, atr_path):
        pass


class CmdObjOpt(object):
    PORT_PATHSEP = '.'
    #
    OBJ_NAME_0 = 'renderPartition'
    OBJ_NAME_1 = 'lightLinker1'
    OBJ_NAME_2 = 'defaultLightSet'
    #
    SHADER_CATEGORY_DICT = {}
    for _category in ['shader', 'texture', 'light', 'utility']:
        _ = cmds.listNodeTypes(_category) or []
        for _i in _:
            SHADER_CATEGORY_DICT[_i] = _category
    #
    def __init__(self, obj_path):
        _ = cmds.ls(obj_path, long=1)
        if _:
            self._obj_path = _[0]
            self._obj_type = cmds.nodeType(self._obj_path)
            self._obj_query_opt = CmdObjQueryOpt(self._obj_type)
        else:
            raise RuntimeError()
    @classmethod
    def _get_is_exists_(cls, obj_path):
        return cmds.objExists(obj_path)
    @classmethod
    def _set_create_(cls, obj_path, type_name):
        if type_name == ma_configure.Util.MATERIAL_TYPE:
            cls._set_material_create_(obj_path, type_name)
        elif type_name in cls.SHADER_CATEGORY_DICT:
            cls._ser_shader_create_(obj_path, type_name)
        else:
            _ = cmds.createNode(type_name, name=obj_path, skipSelect=1)
    @classmethod
    def _ser_shader_create_(cls, obj_name, type_name):
        if cls._get_is_exists_(obj_name) is False:
            category = cls.SHADER_CATEGORY_DICT.get(type_name, 'utility')
            kwargs = dict(
                name=obj_name,
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
            _ = cmds.shadingNode(type_name, **kwargs)
    @classmethod
    def _set_material_create_(cls, obj_name, type_name):
        if cls._get_is_exists_(obj_name) is False:
            result = cmds.shadingNode(
                type_name,
                name=obj_name,
                asUtility=1,
                skipSelect=1
            )
            cls._set_material_light_link_create_(result)
    @classmethod
    def _set_material_light_link_create_(cls, shadingEngine):
        def get_connection_index_():
            for i in range(5000):
                if get_is_partition_connected_at_(i) \
                        and get_is_obj_link_connected_at_(i) \
                        and get_is_obj_shadow_link_connected_at_(i) \
                        and get_is_light_link_connected_at_(i) \
                        and get_is_light_shadow_link_connected_at_(i):
                    return i

        #
        def get_is_connected_(connection):
            boolean = False
            if cmds.objExists(connection):
                if not cmds.connectionInfo(connection, isDestination=1):
                    boolean = True
            return boolean

        #
        def get_is_partition_connected_at_(index):
            connection = cls.OBJ_NAME_0 + '.sets[%s]' % index
            return get_is_connected_(connection)

        #
        def get_is_obj_link_connected_at_(index):
            connection = cls.OBJ_NAME_1 + '.link[%s].object' % index
            return get_is_connected_(connection)

        #
        def get_is_obj_shadow_link_connected_at_(index):
            connection = cls.OBJ_NAME_1 + '.shadowLink[%s].shadowObject' % index
            return get_is_connected_(connection)

        #
        def get_is_light_link_connected_at_(index):
            connection = cls.OBJ_NAME_1 + '.link[%s].light' % index
            return get_is_connected_(connection)

        #
        def get_is_light_shadow_link_connected_at_(index):
            connection = cls.OBJ_NAME_1 + '.shadowLink[%s].shadowLight' % index
            return get_is_connected_(connection)

        #
        def main_fnc_():
            index = get_connection_index_()
            if index:
                # Debug ( Repeat )
                if not cmds.connectionInfo(shadingEngine + '.partition', isSource=1):
                    cmds.connectAttr(shadingEngine + '.partition', cls.OBJ_NAME_0 + '.sets[%s]' % index)
                    cmds.connectAttr(
                        shadingEngine + '.message',
                        cls.OBJ_NAME_1 + '.link[%s].object' % index
                    )
                    cmds.connectAttr(
                        shadingEngine + '.message',
                        cls.OBJ_NAME_1 + '.shadowLink[%s].shadowObject' % index
                    )
                    cmds.connectAttr(
                        cls.OBJ_NAME_2 + '.message',
                        cls.OBJ_NAME_1 + '.link[%s].light' % index
                    )
                    cmds.connectAttr(
                        cls.OBJ_NAME_2 + '.message',
                        cls.OBJ_NAME_1 + '.shadowLink[%s].shadowLight' % index
                    )

        #
        main_fnc_()

    def set_array_ports_clear(self):
        ports = self.get_ports()
        for port in ports:
            if port.get_port_query().get_is_array(self.get_path()) is True:
                array_indices = port.get_array_indices()
                for array_index in array_indices:
                    cmds.removeMultiInstance('{}[{}]'.format(port.get_path(), array_index), b=True)

    def get_obj_query(self):
        return self._obj_query_opt

    def get_type_name(self):
        return self._obj_type
    type_name = property(get_type_name)

    def get_path(self):
        return self._obj_path
    path = property(get_path)

    def __get_port_paths_(self, port_paths):
        def rcs_fnc_(port_path_):
            _port_query = self.get_obj_query().get_port_query(
                port_path_
            )
            _condition = _port_query.get_is_array(obj_path), _port_query.get_has_channels(obj_path)
            if _condition == (True, True):
                _array_indices = CmdPortOpt(self.get_path(), port_path_).get_array_indices()
                _child_port_names = _port_query.get_channel_names()
                for _i_array_index in _array_indices:
                    for _i_child_port_name in _child_port_names:
                        _i_port_path = '{}[{}].{}'.format(port_path_, _i_array_index, _i_child_port_name)
                        lis.append(_i_port_path)
                        rcs_fnc_(_i_port_path)
            elif _condition == (True, False):
                _array_indices = CmdPortOpt(self.get_path(), port_path_).get_array_indices()
                for _i_array_index in _array_indices:
                    _i_port_path = '{}[{}]'.format(port_path_, _i_array_index)
                    lis.append(_i_port_path)
                    rcs_fnc_(_i_port_path)
            elif _condition == (False, True):
                _child_port_names = _port_query.get_channel_names()
                for _i_child_port_name in _child_port_names:
                    _i_port_path = '{}.{}'.format(port_path_, _i_child_port_name)
                    lis.append(_i_port_path)
                    rcs_fnc_(_i_port_path)
            elif _condition == (False, False):
                pass
        #
        lis = []
        obj_path = self.get_path()
        for port_path in port_paths:
            port_query = self.get_obj_query().get_port_query(
                port_path
            )
            if CmdPortOpt._get_is_exists_(obj_path, port_path) is True:
                if port_query.get_has_parent(obj_path) is False:
                    lis.append(port_path)
                    rcs_fnc_(port_path)
        return lis

    def get_port_paths(self):
        return self.__get_port_paths_(
            cmds.attributeInfo(
                allAttributes=True,
                type=self.get_type_name()
            ) or []
        )

    def get_ports(self, includes=None):
        _ = self.get_port_paths()
        if isinstance(includes, (tuple, list)):
            _ = includes
        return [
            self.get_port(i) for i in _
        ]

    def get_customize_port_paths(self):
        return self.__get_port_paths_(
            cmds.listAttr(self.get_path(), userDefined=1) or []
        )

    def get_customize_ports(self, includes=None):
        _ = self.get_customize_port_paths()
        if isinstance(includes, (tuple, list)):
            _ = includes
        return [
            self.get_port(i) for i in _ if CmdPortOpt._get_is_exists_(
                self.get_path(), i
            )
        ]

    def set_customize_attributes_create(self, attributes):
        # 'message',
        # 'bool',
        # 'byte',
        # 'enum',
        # 'typed',
        # 'short',
        # 'float',
        # 'float3',
        # 'compound',
        # 'double',
        # 'time',
        # 'generic',
        # 'doubleLinear',
        # 'doubleAngle',
        # 'matrix',
        # 'long',
        # 'double3',
        # 'lightData',
        # 'addr',
        # 'float2',
        # 'double2',
        # 'double4',
        # 'fltMatrix',
        # 'char',
        # 'floatAngle',
        # 'floatLinear',
        # 'long3',
        # 'short2',
        # 'polyFaces',
        # 'long2'
        obj_path = self.get_path()
        for i_port_path, i_value in attributes.items():
            if isinstance(i_value, six.string_types):
                type_name = 'string'
            elif isinstance(i_value, bool):
                type_name = 'bool'
            elif isinstance(i_value, int):
                type_name = 'long'
            elif isinstance(i_value, float):
                type_name = 'double'
            else:
                raise RuntimeError()
            #
            CmdPortOpt._set_create_(
                obj_path=obj_path,
                port_path=i_port_path,
                type_name=type_name
            )
            #
            port = CmdPortOpt(obj_path, i_port_path)
            if i_value is not None:
                port.set(i_value)

    def set_customize_attribute_create(self, port_path, value):
        if value is not None:
            obj_path = self.get_path()
            if isinstance(value, six.string_types):
                type_name = 'string'
            elif isinstance(value, bool):
                type_name = 'bool'
            elif isinstance(value, int):
                type_name = 'long'
            elif isinstance(value, float):
                type_name = 'double'
            else:
                raise RuntimeError()
            #
            CmdPortOpt._set_create_(
                obj_path=obj_path,
                port_path=port_path,
                type_name=type_name
            )
            #
            port = CmdPortOpt(obj_path, port_path)
            port.set(value)

    def get_port(self, port_path):
        return CmdPortOpt(self._obj_path, port_path)

    def get_port_opt(self, port_path):
        return CmdPortOpt(self._obj_path, port_path)

    def set_file_new(self):
        for i_port in self.get_ports():
            i_port.set_disconnect()
        #
        for i_port in self.get_ports():
            # noinspection PyBroadException
            try:
                i_port.set_default()
            except:
                bsc_core.ExceptionMtd.set_print()
                utl_core.Log.set_module_error_trace(
                    'attribute-set',
                    'obj="{}", port="{}"'.format(
                        i_port.get_obj_path(), i_port.get_port_path()
                    )
                )

    def set(self, key, value):
        self.get_port(key).set(value)

    def __str__(self):
        return '{}(path="{}")'.format(
            self.get_type_name(), self.get_path()
        )

    def __repr__(self):
        return self.__str__()


class CmdMeshesOpt(object):
    EVALUATE_A = {
        'shell': 1,
        'triangle': 768,
        'area': 2.3317136764526367,
        'geometry': 1,
        'vertex': 386,
        'face': 384,
        'world-area': 2.3317136764526367,
        'uv-map': 441,
        'edge': 768,
        #
        'clip-x': -0.4245877265930176,
        'clip-y': -0.4245877265930176,
        'clip-z': -0.4245877265930176,
        #
        'width': 0.8491754531860352,
        'height': 0.8491754531860352,
        'depth': 0.8491754531860352,
        #
        'center-x': 0.0,
        'center-y': 0.0,
        'center-z': 0.0,
    }
    def __init__(self, root):
        self._root = root
        self._mesh_paths = cmds.ls(
            self._root,
            type='mesh',
            noIntermediate=1,
            dagObjects=1,
            long=1
        ) or []

    def get_evaluate(self):
        kwargs = dict(
            vertex='vertex'
        )
        dic = {}
        if self._mesh_paths:
            keys = [
                'vertex',
                'edge',
                'face',
                'triangle',
                'uvcoord',
                'area',
                'worldArea',
                'shell',
                'boundingBox'
            ]
            dic_0 = {}
            for i in keys:
                v = cmds.polyEvaluate(
                    self._mesh_paths, **{i: True}
                )
                dic_0[i] = v
            #
            count = len(self._mesh_paths)
            b_box = dic_0['boundingBox']
            #
            dic['geometry'] = count
            dic['vertex'] = dic_0['vertex']
            dic['edge'] = dic_0['edge']
            dic['face'] = dic_0['face']
            dic['triangle'] = dic_0['triangle']
            dic['uv-map'] = dic_0['uvcoord']
            dic['area'] = dic_0['area']
            dic['world-area'] = dic_0['worldArea']
            dic['shell'] = dic_0['shell']
            dic['center-x'] = b_box[0][0]+b_box[0][1]
            dic['center-y'] = b_box[1][0]+b_box[1][1]
            dic['center-z'] = b_box[2][0]+b_box[2][1]
            dic['clip-x'] = b_box[0][0]
            dic['clip-y'] = b_box[1][0]
            dic['clip-z'] = b_box[2][0]
            dic['width'] = b_box[0][1]-b_box[0][0]
            dic['height'] = b_box[1][1]-b_box[1][0]
            dic['depth'] = b_box[2][1]-b_box[2][0]
        #
        return dic

    def get_radar_chart_data(self):
        evaluate = self.get_evaluate()
        radar_chart_data = []
        if evaluate:
            tgt_keys = [
                'face',
                'edge',
                'vertex',
            ]
            for key in [
                'geometry',
                'shell',
                'area',
                'face',
                'edge',
                'vertex',
            ]:
                if key in tgt_keys:
                    a_0 = self.EVALUATE_A['area']
                    a_1 = evaluate['area']
                    v_0 = self.EVALUATE_A[key]
                    src_value = (a_1/a_0)*v_0
                else:
                    src_value = evaluate[key]
                #
                tgt_value = evaluate[key]
                radar_chart_data.append(
                    (key, src_value, tgt_value)
                )
        return radar_chart_data

    def set_reduce_by(self, percent):
        for i_mesh_path in self._mesh_paths:
            self._set_mesh_reduce_(i_mesh_path, percent)
    @classmethod
    def _set_mesh_reduce_(cls, mesh_path, percent):
        cmds.polyReduce(
            mesh_path,
            version=1,
            termination=0,
            percentage=percent*100,
            symmetryPlaneX=0,
            symmetryPlaneY=1,
            symmetryPlaneZ=0,
            symmetryPlaneW=0,
            keepQuadsWeight=0,
            vertexCount=0,
            triangleCount=0,
            sharpness=0,
            keepColorBorder=0,
            keepFaceGroupBorder=0,
            keepHardEdge=1,
            keepCreaseEdge=1,
            keepBorderWeight=0.5,
            keepMapBorderWeight=1,
            keepColorBorderWeight=0.5,
            keepFaceGroupBorderWeight=0.5,
            keepHardEdgeWeight=0.5,
            keepCreaseEdgeWeight=0.5,
            useVirtualSymmetry=0,
            symmetryTolerance=0.01,
            vertexMapName='',
            replaceOriginal=1,
            cachingReduce=1,
            constructionHistory=0
        )
        cmds.polyTriangulate(mesh_path, constructionHistory=0)
        cmds.delete(mesh_path, constructionHistory=1)

    def get_bounding_box(self):
        return cmds.polyEvaluate(self._mesh_paths, boundingBox=1)

    def get_geometry_args(self):
        b_box = self.get_bounding_box()
        x_0, y_0, z_0 = b_box[0][0], b_box[1][0], b_box[2][0]
        x_1, y_1, z_1 = b_box[0][1], b_box[1][1], b_box[2][1]
        c_x, c_y, c_z = x_0+(x_1-x_0)/2, y_0+(y_1-y_0)/2, z_0+(z_1-z_0)/2
        w, h, d = x_1-x_0, y_1-y_0, z_1-z_0
        return (x_0, y_0, z_0), (c_x, c_y, c_z), (w, h, d)


class CmdCameraOpt(CmdObjOpt):
    def __init__(self, obj_path):
        super(CmdCameraOpt, self).__init__(obj_path)
    @classmethod
    def get_front_frame_args(cls, geometry_args, angle):
        _, (c_x, c_y, c_z), (w, h, d) = geometry_args
        z_1 = h / math.tan(math.radians(angle))
        return (c_x, c_y, z_1 - c_z), (0, 0, 0)


class CmdUndoStack(object):
    def __init__(self, key=None):
        if key is None:
            key = bsc_core.UuidMtd.get_new()
        #
        self._key = key

    def __enter__(self):
        cmds.undoInfo(openChunk=1, undoName=self._key)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        cmds.undoInfo(closeChunk=1, undoName=self._key)


class QtControlOpt(object):
    def __init__(self, name):
        self._name = name

    def get_is_exists(self):
        return cmds.workspaceControl(self._name, exists=True)

    def set_visible(self, boolean):
        if self.get_is_exists():
            cmds.workspaceControl(
                self._name,
                edit=True,
                visible=boolean,
            )

    def set_restore(self):
        cmds.workspaceControl(
            self._name,
            edit=True,
            restore=True,
        )

    def set_delete(self):
        if cmds.workspaceControl(self._name, exists=True):
            cmds.workspaceControl(
                self._name,
                edit=True,
                close=True
            )
            #
            cmds.deleteUI(self._name)

    def set_script(self, script):
        cmds.workspaceControl(
            self._name,
            edit=True,
            uiScript=script
        )

    def set_create(self, width, height):
        if self.get_is_exists():
            self.set_restore()
            # self.set_visible(True)
        else:
            cmds.workspaceControl(
                self._name,
                label=bsc_core.RawStringUnderlineOpt(self._name).to_prettify(capitalize=False),
                dockToMainWindow=['right', False],
                initialWidth=width, initialHeight=height,
                widthProperty='free', heightProperty='free'
            )
    @classmethod
    def _to_qt_instance_(cls, ptr, base):
        from shiboken2 import wrapInstance
        return wrapInstance(long(ptr), base)

    def to_qt_widget(self):
        ptr = OpenMayaUI.MQtUtil.findControl(self._name)
        if ptr is not None:
            return self._to_qt_instance_(
                ptr, base=QtWidgets.QWidget
            )

    def get_qt_layout(self):
        widget = self.to_qt_widget()
        if widget is not None:
            return widget.layout()


def undo_stack(key=None):
    return CmdUndoStack(key)


def set_stack_trace_enable(boolean=False):
    cmds.stackTrace(state=boolean)
