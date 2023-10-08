# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.api.OpenMaya as om2


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
    def _get_om2_curve_fnc_(cls, path):
        return om2.MFnNurbsCurve(cls._get_om2_dag_path_(path))
    @classmethod
    def _get_om2_surface_fnc_(cls, path):
        return om2.MFnNurbsSurface(cls._get_om2_dag_path_(path))
    @classmethod
    def _get_om2_dag_(cls, path):
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
    def _to_om2_point_array_(cls, point_array):
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
        span = count - 3
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


class MeshOpt(object):
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
        for face_index in xrange(om2_obj.numPolygons):
            count = om2_obj.polygonVertexCount(face_index)
            face_vertex_counts.append(count)
            om2_indices = om2_obj.getPolygonVertices(face_index)
            indices = list(om2_indices)
            face_vertex_indices.extend(indices)

        return face_vertex_counts, face_vertex_indices

    def get_points(self, round_count=None):
        return Om2Method._get_point_array_(
            self._om2_obj_fnc.getPoints(),
            round_count
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
            Om2Method._to_om2_point_array_(points),
            face_vertex_counts, face_vertex_indices,
            parent=Om2Method._get_om2_dag_obj_(transform)
        )
        if uv_map_coords is not None:
            uv_map_name = 'map1'
            map_u_coords, map_v_coords = zip(*uv_map_coords)
            om2_obj.setUVs(map_u_coords, map_v_coords, uv_map_name)
            om2_obj.assignUVs(face_vertex_counts, face_vertex_indices, uv_map_name)
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

