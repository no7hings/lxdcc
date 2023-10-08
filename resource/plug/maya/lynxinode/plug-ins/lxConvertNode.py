# encoding=utf-8
import sys
#
import math
# noinspection PyUnresolvedReferences
import maya.mel as mel
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.api.OpenMaya as om
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.api.OpenMayaUI as omui


# Use 2.0 API
def maya_useNewAPI():
    pass


class MtdBasic(object):
    @classmethod
    def _get_om_dag_path_(cls, path):
        return om.MGlobal.getSelectionListByName(path).getDagPath(0)
    @classmethod
    def get_atr(cls, om_obj_fnc, port_name):
        p = om_obj_fnc.findPlug(port_name, 0)
        return p
    @classmethod
    def _get_om_point_(cls, point):
        m2Point = om.MPoint()
        m2Point.x, m2Point.y, m2Point.z = point
        return m2Point
    @classmethod
    def _get_om_point_array_(cls, point_array):
        m2PointArray = om.MPointArray()
        for point in point_array:
            m2Point = cls._get_om_point_(point)
            m2PointArray.append(m2Point)
        return m2PointArray
    @classmethod
    def _set_om_curve_create_(cls, points, knots, degree, form, parent):
        om_curve = om.MFnNurbsCurve()
        om_curve.create(
            points,
            knots, degree, form,
            False,
            True,
            parent=parent
        )
    @classmethod
    def _get_om_mesh_fnc_(cls, path):
        return om.MFnMesh(cls._get_om_dag_path_(path))
    @classmethod
    def _get_division_(cls, value, sample):
        _ = int(value * sample)
        division = max(_, 2)
        return division
    @classmethod
    def _get_point_(cls, om_point):
        return om_point.x, om_point.y, om_point.z
    @classmethod
    def _get_point_array_(cls, om_point_array):
        return [cls._get_point_(i) for i in om_point_array]
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


# command
class CurveToMeshData(object):
    def __init__(self, *args):
        (
            converter,
            input_curve, input_mesh,
            output_mesh,
            #
            v_uniform_enable, base_attach_to_mesh_enable,
            order,
            u_auto_division_enable, v_auto_division_enable,
            u_division, v_division,
            width, width_extra,
            spin, spin_extra,
            twist, taper,
            arch_attach_curve_enable, arch, arch_extra,
            v_start_index, v_end_index,
            u_sample, v_sample,
            u_texture_coord_tile_width, v_texture_coord_tile_width
        ) = args
        #
        self._converter_om_obj_fnc = om.MFnDependencyNode(converter)
        #
        self._input_curve = input_curve
        self._input_curve_om_obj_fnc = om.MFnNurbsCurve(input_curve)
        #
        self._input_mesh = input_mesh
        self._input_mesh_om_obj_fnc = self._get_input_mesh_om_obj_fnc_()
        #
        self._output_mesh_om_fnc = output_mesh
        #
        self._length = self._input_curve_om_obj_fnc.length()
        #
        self._v_count = v_division - 1
        self._u_count = u_division - 1
        #
        self._width = width
        self._width_extra = width_extra
        self._spin = spin
        self._spin_extra = spin_extra
        #
        self._twist = twist
        self._taper = taper
        #
        self._arch_attach_curve_enable = arch_attach_curve_enable
        self._arch = arch
        self._arch_extra = arch_extra
        #
        self._u_sample = u_sample
        self._v_sample = v_sample
        # Clamp in 0.1
        self._v_start_index = max(min(v_start_index, v_start_index - .1, 1.0 - .1), 0.0)
        self._v_end_index = max(v_end_index, min(v_start_index + .1, 1.0), .1)
        #
        self._v_uniform_enable = v_uniform_enable
        self._base_attach_to_mesh_enable = base_attach_to_mesh_enable
        self._order = order
        #
        self._u_texture_coord_tile_width = u_texture_coord_tile_width
        #
        curve_param = self._input_curve_om_obj_fnc.knotDomain
        #
        self._curve_param_minimum = curve_param[0]
        self._curve_param_maximum = curve_param[1]
        #
        self._v_search_count = int(self._v_count*self._v_sample)
        #
        self._update_output_curve_data_()
        self._set_value_reduce_update_()
        self._set_mesh_data_update_()
    #
    def _update_output_curve_data_at_(self, index, percent):
        if self._v_uniform_enable is True:
            length = MtdBasic._set_value_map_((0, 1), (0, self._length), percent)
            param = self._input_curve_om_obj_fnc.findParamFromLength(length)
        else:
            param = MtdBasic._set_value_map_((0, 1), (self._curve_param_minimum, self._curve_param_maximum), percent)
        #
        om_mesh_obj_fnc = self._input_mesh_om_obj_fnc
        #
        v = om.MVector()
        #
        x_axis, y_axis, z_axis = v.kXaxisVector, v.kYaxisVector, v.kZaxisVector
        #
        if self._base_attach_to_mesh_enable is True:
            if om_mesh_obj_fnc is not None:
                x_axis, y_axis, z_axis = self._get_input_mesh_axis_()
        # tangent = z-normal, space=world
        point, z_normal = self._input_curve_om_obj_fnc.getDerivativesAtParam(param, 4)
        z_normal = z_normal.normalize()
        #
        if index == 0:
            # ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']
            # xyz
            if self._order == 0:
                if z_normal.isParallel(y_axis):
                    axis = x_axis
                else:
                    axis = y_axis
            # yzx
            elif self._order == 1:
                if z_normal.isParallel(z_axis):
                    axis = y_axis
                else:
                    axis = z_axis
            # zxy
            elif self._order == 2:
                if z_normal.isParallel(x_axis):
                    axis = z_axis
                else:
                    axis = x_axis
            # xzy
            elif self._order == 3:
                if z_normal.isParallel(z_axis):
                    axis = x_axis
                else:
                    axis = z_axis*-1
            # yxz
            elif self._order == 4:
                if z_normal.isParallel(x_axis):
                    axis = y_axis
                else:
                    axis = x_axis*-1
            # zyx
            elif self._order == 5:
                if z_normal.isParallel(y_axis):
                    axis = z_axis
                else:
                    axis = y_axis*-1
            # xyz
            else:
                if z_normal.isParallel(y_axis):
                    axis = x_axis
                else:
                    axis = y_axis
            # Vector Multiplication Cross
            x_normal = z_normal.__rxor__(axis)
            y_normal = x_normal.__rxor__(z_normal)
        else:
            quaternion = self._output_curve_z_normal[index-1].rotateTo(z_normal)
            #
            x_normal = self._output_curve_v_normals_x[index-1]
            x_normal = x_normal.rotateBy(quaternion)
            #
            y_normal = self._output_curve_v_normals_y[index-1]
            y_normal = y_normal.rotateBy(quaternion)
        #
        self._output_curve_v_percents[index] = percent
        #
        self._output_curve_v_points[index] = point
        self._output_curve_z_normal[index] = z_normal
        #
        self._output_curve_v_normals_x[index] = x_normal.normalize()
        self._output_curve_v_normals_y[index] = y_normal.normalize()
    #
    def _update_output_curve_data_(self):
        c = self._v_search_count + 1
        self._output_curve_v_percents = [None]*c
        #
        self._output_curve_v_points = [None]*c
        self._output_curve_z_normal = [None]*c
        #
        self._output_curve_v_normals_x = [None]*c
        self._output_curve_v_normals_y = [None]*c
        #
        for i_index in range(c):
            if i_index == 0:
                i_percent = self._v_start_index
            elif i_index == self._v_search_count:
                i_percent = self._v_end_index
            else:
                i_percent = MtdBasic._set_value_map_(
                    (0, c),
                    (self._v_start_index, self._v_end_index),
                    i_index
                )
            #
            self._update_output_curve_data_at_(i_index, i_percent)
    #
    def _set_value_reduce_update_(self):
        def main_fnc_():
            for n in range(rangeCount):
                seq = n + 1
                #
                if seq % self._v_sample == 0:
                    self._filterSeqs.append(seq)
            #
            self._filterSeqs.insert(0, 0)
            self._filterSeqs.append(self._v_search_count)
            self._filterSeqs.sort()
        #
        self._filterSeqs = []
        #
        rangeCount = self._v_search_count - 2
        #
        main_fnc_()
    #
    def _get_input_mesh_om_obj_fnc_(self):
        p = self._converter_om_obj_fnc.findPlug('inputMesh', 0)
        s = p.source()
        if s.isNull is False:
            obj = om.MFnDagNode(s.node())
            obj_path = obj.fullPathName()
            if obj_path:
                return MtdBasic._get_om_mesh_fnc_(obj_path)
    #
    def _get_input_mesh_world_matrix_(self):
        om_mesh_obj_fnc = self._input_mesh_om_obj_fnc
        if om_mesh_obj_fnc is not None:
            plug = om_mesh_obj_fnc.findPlug('worldMatrix', 0)
            plug = plug.elementByLogicalIndex(0)
            plug_obj = plug.asMObject()
            matrix_data = om.MFnMatrixData(plug_obj)
            world_matrix = matrix_data.matrix()
            return world_matrix
    #
    def _get_input_mesh_axis_(self):
        world_matrix = self._get_input_mesh_world_matrix_()
        x_vector = om.MVector(
            [world_matrix.getElement(0, i) for i in range(3)]
        )
        y_vector = om.MVector(
            [world_matrix.getElement(1, i) for i in range(3)]
        )
        z_vector = om.MVector(
            [world_matrix.getElement(2, i) for i in range(3)]
        )
        return x_vector, y_vector, z_vector
    #
    def _set_mesh_data_update_(self):
        def set_face_vertex_update_fnc_():
            _l = [0, 1, 2 + u_count, 1 + u_count]
            for v in range(v_count):
                for u in range(u_count):
                    self._mesh_face_vertex_counts.append(4)
                    if u == 0:
                        __l = [(i + v*(u_count + 1)) for i in _l]
                    else:
                        __l = [(i + v*(u_count + 1) + u) for i in _l]
                    #
                    self._mesh_face_vertex_indices.extend(__l)
        #
        def set_point_update_fnc_():
            if (u_count + 1) % 2:
                m = int((u_count + 1) / 2)
            else:
                m = None
            #
            c = float(u_count) / 2.0
            for _v_index in range(v_count + 1):
                if _v_index == 0:
                    _v_index_ = 0
                elif _v_index == self._v_count:
                    _v_index_ = self._v_search_count
                else:
                    _v_index_ = self._filterSeqs[_v_index]
                #
                _v_point = self._output_curve_v_points[_v_index_]
                _v_tangent = self._output_curve_z_normal[_v_index_]
                _v_side = self._output_curve_v_normals_x[_v_index_]
                _v_mid = self._output_curve_v_normals_y[_v_index_]
                _v_percent = self._output_curve_v_percents[_v_index_]
                _v_width_extra = self._width_extra.getValueAtPosition(_v_percent)
                _v_spin = self._spin_extra.getValueAtPosition(_v_percent)
                _v_arch_extra = self._arch_extra.getValueAtPosition(_v_percent)
                for _u_index in range(u_count + 1):
                    _u_percent = float(abs(_u_index - c)) / float(c)
                    #
                    _u_width = width*_v_width_extra*2 + (taper - 1)*_v_percent*width
                    _u_width = max(_u_width, 0)
                    vector = _v_side*_u_width/2
                    #
                    p_ = om.MPoint()
                    if _u_index == 0 or _u_index == u_count:
                        v_ = vector
                    else:
                        if _u_index == m:
                            # noinspection PyArgumentList
                            v_ = om.MVector(0, 0, 0)
                        else:
                            v_ = _u_percent*vector
                    #
                    _u_arch = max(min(arch + (_v_arch_extra-.5)*2, 1), -1)
                    _u_arch_radians = math.radians(_u_percent*90*_u_arch)
                    if _u_index < c:
                        _u_arch_radians = -math.radians(_u_percent*90*_u_arch)
                        v_ /= -1
                    # arch
                    _u_arch_rotate = om.MQuaternion()
                    # noinspection PyArgumentList
                    _u_arch_rotate.setValue(
                        om.MVector(_v_tangent.x, _v_tangent.y, _v_tangent.z),
                        _u_arch_radians
                    )
                    v_ = v_.rotateBy(_u_arch_rotate)
                    #
                    if arch_attach_curve_enable is False:
                        _a = max(min(abs(_u_arch), 1.0), 0.0)
                        if _u_arch > 0:
                            _w_0 = _u_width/2/math.pi*_a
                        else:
                            _w_0 = -_u_width/2/math.pi*_a
                        v_ -= _v_mid*_w_0*2
                    # Spin + Spin Extra +  Twist
                    _u_spin_rotate = om.MQuaternion()
                    # noinspection PyArgumentList
                    _u_spin_rotate.setValue(
                        om.MVector(_v_tangent.x, _v_tangent.y, _v_tangent.z),
                        math.radians(spin) + math.radians(_v_spin*360) + math.radians(twist*_v_percent)
                    )
                    v_ = v_.rotateBy(_u_spin_rotate)
                    #
                    p_.x, p_.y, p_.z = _v_point.x + v_.x, _v_point.y + v_.y, _v_point.z + v_.z
                    #
                    self._mesh_points.append(p_)
                    #
                    u_coord = 0
                    if _u_index == 0:
                        u_coord = 0.5 + u_texture_coord_tile_width*abs(_u_index-c)
                    elif _u_index == u_count:
                        u_coord = 0.5 - u_texture_coord_tile_width*abs(_u_index-c)
                    else:
                        if _u_index == c:
                            u_coord = .5
                        elif c < _u_index:
                            u_coord = 0.5 - u_texture_coord_tile_width*abs(_u_index-c)
                        elif _u_index < c:
                            u_coord = 0.5 + u_texture_coord_tile_width*abs(_u_index-c)
                    #
                    v_coord = 1 - _v_percent

                    self._mesh_map_coords.append(
                        (u_coord, v_coord)
                    )
        #
        def set_base_point_attach_to_glow_mesh_fnc_():
            if self._base_attach_to_mesh_enable is True:
                om_mesh_obj_fnc = self._input_mesh_om_obj_fnc
                if om_mesh_obj_fnc is not None:
                    base_points = self._mesh_points[:u_count+1]
                    for seq, base_point in enumerate(base_points):
                        _o = om_mesh_obj_fnc.getClosestPoint(
                            base_point, space=4
                        )
                        self._mesh_points[seq] = _o[0]
        #
        self._mesh_face_vertex_counts, self._mesh_face_vertex_indices = [], []
        self._mesh_points = []
        self._mesh_map_coords = []
        #
        v_count = self._v_count
        u_count = self._u_count
        #
        width = self._width
        spin = self._spin
        #
        u_texture_coord_tile_width = self._u_texture_coord_tile_width
        #
        twist = self._twist
        taper = self._taper
        arch = self._arch
        arch_attach_curve_enable = self._arch_attach_curve_enable
        #
        set_face_vertex_update_fnc_()
        set_point_update_fnc_()
        set_base_point_attach_to_glow_mesh_fnc_()
    #
    def update(self):
        MeshMtd.set_create(
            self._output_mesh_om_fnc,
            (self._mesh_face_vertex_counts, self._mesh_face_vertex_indices),
            self._mesh_points,
            self._mesh_map_coords
        )


class MeshToSurfaceConverter(object):
    def __init__(self, mesh_om_fnc, surface_om_obj):
        self._mesh_om_obj_fnc = mesh_om_fnc
        self._surface_om_obj = surface_om_obj
        #
        self._corner_index = 0
        self._rotation = 1
    @classmethod
    def _get_center_point_(cls, point_0, point_1):
        x, y, z = (point_0.x + point_1.x) / 2, (point_0.y + point_1.y) / 2, (point_0.z + point_1.z) / 2
        return om.MPoint(x, y, z)
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
    def _get_next_edge_vertex_index_(cls, edge_vertex_index, om_edge_itr):
        edge_vertex_indices = [om_edge_itr.vertexId(i) for i in range(2)]
        edge_vertex_indices.remove(edge_vertex_index)
        return edge_vertex_indices[0]
    @classmethod
    def _get_border_next_vertex_index_(cls, vertex_index, edge_index, om_vertex_itr, om_edge_itr, rotation, step):
        om_vertex_itr.setIndex(vertex_index)
        om_edge_itr.setIndex(edge_index)
        #
        next_vertex_index = cls._get_next_edge_vertex_index_(vertex_index, om_edge_itr)
        #
        om_vertex_itr.setIndex(next_vertex_index)
        next_edge_indices = om_vertex_itr.getConnectedEdges()
        next_edge_index = cls._get_next_comp_index_(
            edge_index, next_edge_indices, rotation, step
        )
        return next_vertex_index, next_edge_index

    def _get_corner_vertex_indices_at_(self, vertex_index, include_vertex_indices, rotation):
        self._mesh_om_vertex_itr.setIndex(vertex_index)
        #
        start_edge_indices = self._mesh_om_vertex_itr.getConnectedEdges()
        if rotation == -1:
            start_edge_index = start_edge_indices[1]
        else:
            start_edge_index = start_edge_indices[0]
        self._mesh_om_edge_itr.setIndex(start_edge_index)
        #
        return self._get_vertex_indices_at_(
            vertex_index, start_edge_index, include_vertex_indices, rotation, step=1
        )

    def _get_border_vertex_indices_at_(self, vertex_index, include_vertex_indices, rotation):
        self._mesh_om_vertex_itr.setIndex(vertex_index)
        start_edge_indices = self._mesh_om_vertex_itr.getConnectedEdges()
        # temp
        start_edge_index = start_edge_indices[1]
        self._mesh_om_edge_itr.setIndex(start_edge_index)
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
                self._mesh_om_vertex_itr, self._mesh_om_edge_itr,
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
        self._mesh_om_vertex_itr = om.MItMeshVertex(self._mesh_om_obj_fnc.object())
        self._mesh_om_edge_itr = om.MItMeshEdge(self._mesh_om_obj_fnc.object())
        #
        self._mesh_points = self._mesh_om_obj_fnc.getPoints(space=4)
        #
        self._set_border_vertex_indices_update_()

    def _set_border_vertex_indices_update_(self):
        self._corner_vertex_indices, self._border_vertex_indices = [], []
        om_vertex_itr = om.MItMeshVertex(self._mesh_om_obj_fnc.dagPath())
        vertex_indices = range(om_vertex_itr.count())
        for vertex_index in vertex_indices:
            om_vertex_itr.setIndex(vertex_index)
            if om_vertex_itr.onBoundary() is True:
                if len(om_vertex_itr.getConnectedFaces()) == 1:
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
        # swap to v
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
        SurfaceCreator(self._surface_om_obj).update(
            self._surface_u_count, self._surface_v_count, self._surface_points
        )


class MeshToSurfaceData(object):
    def __init__(self, *args):
        (
            converter,
            input_mesh,
            output_surface,
            direction
        ) = args
        self._converter_om_obj_fnc = om.MFnDependencyNode(converter)
        self._input_mesh = input_mesh
        self._input_mesh_om_obj_fnc = om.MFnMesh(input_mesh)
        self._output_surface_om_obj = output_surface
        #
        self._surface_direction = max(min(direction, 3), 0)

    def _get_input_mesh_om_obj_fnc_(self):
        p = self._converter_om_obj_fnc.findPlug('inputMesh', 0)
        s = p.source()
        if s.isNull is False:
            obj = om.MFnDagNode(s.node())
            obj_path = obj.fullPathName()
            if obj_path:
                return MtdBasic._get_om_mesh_fnc_(obj_path)

    def set_run(self):
        MeshToSurfaceConverter(
            self._get_input_mesh_om_obj_fnc_(), self._output_surface_om_obj
        ).set_run()


class XgenToCurveCmd(object):
    def __init__(self, *args):
        (
            converter,
            input_xgen_guide, input_mesh,
            output_curve
        ) = args
        #
        self._converter_om_obj_fnc = om.MFnDependencyNode(converter)
        #
        self._output_curve_create = output_curve

    def get_xgen_guide_control_points(self):
        path = self.get_xgen_guide_obj_path()
        lis = []
        if path:
            _ = mel.eval('xgmGuideGeom -guide {} -controlPoints'.format(path)) or []
            for seq, i in enumerate(_):
                if not seq % 3:
                    lis.append(tuple([_[seq+j] for j in range(3)]))
        return lis

    def get_xgen_guide_obj_path(self):
        p = self._converter_om_obj_fnc.findPlug('inputXgenGuide', 0)
        s = p.source()
        if s.isNull is False:
            obj = om.MFnDagNode(s.node())
            return obj.fullPathName()

    def update(self):
        control_points = self.get_xgen_guide_control_points()
        if control_points:
            points = MtdBasic._get_om_point_array_(control_points)
            CurveCreator(
                self._output_curve_create
            ).update(
                degree=2, form=1,
                points=points
            )


class SurfaceToMeshData(object):
    def __init__(self, *args):
        (
            converter,
            input_surface,
            output_curve, output_mesh,
            u_uniform_enable, v_uniform_enable,
            u_division, v_division
        ) = args
        #
        self._input_surface_om_obj_fnc = om.MFnNurbsSurface(input_surface)
        #
        self._output_curve_create = output_curve
        self._output_mesh_create = output_mesh
        #
        self._u_uniform_enable, self._v_uniform_enable = u_uniform_enable, v_uniform_enable
        #
        self._mesh_u_division, self._mesh_v_division = u_division, v_division

    def _set_surface_data_update_(self):
        u_count, v_count = self._mesh_u_division, self._mesh_v_division
        self._surface_points = []
        #
        u_p_max, u_p_min = self._input_surface_om_obj_fnc.knotDomainInU
        v_p_max, v_p_min = self._input_surface_om_obj_fnc.knotDomainInV
        for u_index in range(u_count):
            u_percent = float(u_index) / float(u_count - 1)
            u_param = MtdBasic._set_value_map_(
                (0, 1), (u_p_max, u_p_min), u_percent
            )
            for v_index in range(v_count):
                v_percent = float(v_index) / float(v_count - 1)
                v_param = MtdBasic._set_value_map_(
                    (0, 1), (v_p_max, v_p_min), v_percent
                )
                #
                point = self._input_surface_om_obj_fnc.getPointAtParam(
                    u_param, v_param,
                    space=4
                )
                self._surface_points.append(point)

    def _update_output_curve_data_(self):
        self._set_curve_data_update_step_0_()
        self._set_curve_date_update_step_1_()

    def _get_curve_uniform_v_points_at_(self, count, uniform):
        points = []
        curve_om_obj_fnc = om.MFnNurbsCurve(self._output_curve_create)
        curve_length = curve_om_obj_fnc.length()
        curve_param_minimum, curve_param_maximum = curve_om_obj_fnc.knotDomain
        for index in range(count):
            i_percent = float(index) / float(count - 1)
            if uniform is True:
                i_length = MtdBasic._set_value_map_((0, 1), (0, curve_length), i_percent)
                i_param = curve_om_obj_fnc.findParamFromLength(i_length)
            else:
                i_param = MtdBasic._set_value_map_((0, 1), (curve_param_minimum, curve_param_maximum), i_percent)
            i_point = curve_om_obj_fnc.getPointAtParam(i_param, space=4)
            points.append(i_point)
        return points

    def _set_curve_data_update_step_0_(self):
        u_count, v_count = self._mesh_v_division, self._mesh_u_division
        self._curve_uniform_v_grid_points = []
        #
        u_p_max, u_p_min = self._input_surface_om_obj_fnc.knotDomainInU
        v_p_max, v_p_min = self._input_surface_om_obj_fnc.knotDomainInV
        for u_index in range(u_count):
            v_points = []
            #
            u_percent = float(u_index) / float(u_count - 1)
            u_param = MtdBasic._set_value_map_(
                (0, 1), (u_p_max, u_p_min), u_percent
            )
            for v_index in range(v_count):
                v_percent = float(v_index) / float(v_count - 1)
                v_param = MtdBasic._set_value_map_(
                    (0, 1), (v_p_max, v_p_min), v_percent
                )
                #
                v_point = self._input_surface_om_obj_fnc.getPointAtParam(
                    u_param, v_param,
                    space=4
                )
                #
                v_points.append(v_point)
            #
            CurveCreator(
                self._output_curve_create
            ).update(
                degree=2, form=1,
                points=v_points
            )
            #
            curve_uniform_v_points = self._get_curve_uniform_v_points_at_(
                v_count, self._v_uniform_enable
            )
            self._curve_uniform_v_grid_points.append(curve_uniform_v_points)
        #
        self._curve_uniform_u_grid_points = zip(*self._curve_uniform_v_grid_points)
    #
    def _set_curve_date_update_step_1_(self):
        u_count, v_count = self._mesh_v_division, self._mesh_u_division
        self._surface_points = []
        for u_points in self._curve_uniform_u_grid_points:
            CurveCreator(
                self._output_curve_create
            ).update(
                degree=2, form=1,
                points=u_points
            )
            uniform_u_points = self._get_curve_uniform_v_points_at_(
                u_count, self._u_uniform_enable
            )
            uniform_u_points.reverse()
            for uniform_u_point in uniform_u_points:
                self._surface_points.append(uniform_u_point)

    def _set_mesh_data_update_(self):
        def set_face_vertices_update_fnc_():
            _v_face_count = mesh_v_face_count
            _u_face_count = mesh_u_face_count
            #
            _l = [0, 1, 2+_u_face_count, 1+_u_face_count]
            for _v_face_index in range(_v_face_count):
                for _u_face_index in range(_u_face_count):
                    self._mesh_face_vertex_counts.append(4)
                    if _u_face_index == 0:
                        __l = [(i+_v_face_index * (_u_face_count+1)) for i in _l]
                    else:
                        __l = [(i+_v_face_index * (_u_face_count+1)+_u_face_index) for i in _l]
                    #
                    self._mesh_face_vertex_indices.extend(__l)
        #
        def set_points_update_fnc_():
            _u_point_count = self._mesh_u_division
            _v_point_count = self._mesh_v_division
            #
            for _v_point_index in range(_v_point_count):
                _map_v_coord = float(_v_point_index) / float(_v_point_count - 1)
                for _u_point_index in range(_u_point_count):
                    _index = _u_point_index * _v_point_count+_v_point_index
                    #
                    self._mesh_points.append(self._surface_points[_index])
                    _map_u_coord = float(_u_point_index) / float(_u_point_count - 1)
                    self._mesh_map_coords.append(
                        (_map_u_coord, _map_v_coord)
                    )
        #
        mesh_u_face_count = self._mesh_u_division - 1
        mesh_v_face_count = self._mesh_v_division - 1
        #
        self._mesh_face_vertex_counts, self._mesh_face_vertex_indices = [], []
        self._mesh_points = []
        self._mesh_map_coords = []
        #
        set_face_vertices_update_fnc_()
        set_points_update_fnc_()

    def _set_output_mesh_create_(self):
        MeshMtd.set_create(
            self._output_mesh_create,
            (self._mesh_face_vertex_counts, self._mesh_face_vertex_indices),
            self._mesh_points,
            self._mesh_map_coords
        )

    def update(self):
        self._update_output_curve_data_()
        #
        # self._set_surface_data_update_()
        self._set_mesh_data_update_()
        #
        self._set_output_mesh_create_()


class CurveCreator(object):
    def __init__(self, om_obj):
        self._om_obj_fnc = om_obj

    def update(self, degree, form, points):
        count = len(points)
        knots = MtdBasic._get_curve_knots_(count, degree)
        MtdBasic._set_om_curve_create_(
            points, knots, degree, form, self._om_obj_fnc
        )


class SurfaceCreator(object):
    def __init__(self, om_obj):
        self._om_obj_fnc = om_obj

    def update(self, u_count, v_count, points):
        u_degree, v_degree = 3, 3
        u_form, v_form = 1, 1
        u_knots, v_knots = (
            MtdBasic._get_surface_knots_(u_count, u_degree),
            MtdBasic._get_surface_knots_(v_count, v_degree)
        )
        om_obj = om.MFnNurbsSurface()
        om_obj.create(
            points,
            u_knots, v_knots,
            u_degree, v_degree,
            u_form, v_form,
            True,
            parent=self._om_obj_fnc
        )


class MeshMtd(MtdBasic):
    @classmethod
    def set_create(cls, om_obj, face_vertices, points, map_coords):
        om_mesh = om.MFnMesh()
        #
        face_vertex_counts, face_vertex_indices = face_vertices
        om_mesh.create(
            points,
            face_vertex_counts, face_vertex_indices,
            parent=om_obj
        )
        #
        uv_map_name = 'map1'
        map_u_coords, map_v_coords = zip(*map_coords)
        om_mesh.setUVs(
            map_u_coords, map_v_coords,
            uv_map_name
        )
        om_mesh.assignUVs(
            face_vertex_counts, face_vertex_indices,
            uv_map_name
        )


class NodeBasic(object):
    @classmethod
    def add_comp_atr(cls, long_name, short_name):
        compAttr = om.MFnCompoundAttribute()
        numAttr = om.MFnNumericAttribute()
        enumAttr = om.MFnEnumAttribute()
        #
        atr = compAttr.create(long_name, short_name)
        #
        positionAttr = numAttr.create(
            long_name + '_Position', short_name + 'p',
            om.MFnNumericData.kFloat
        )
        #
        valueAttr = numAttr.create(
            long_name + '_FloatValue', short_name + 'v',
            om.MFnNumericData.kFloat
        )
        #
        interpAttr = enumAttr.create(
            long_name + '_Interp', short_name + 'i'
        )
        enumAttr.addField('None', 0)
        enumAttr.addField('Linear', 1)
        enumAttr.addField('Smooth', 2)
        enumAttr.addField('Spline', 3)
        enumAttr.default = 3
        compAttr.addChild(positionAttr)
        compAttr.addChild(valueAttr)
        compAttr.addChild(interpAttr)
        #
        compAttr.storable = True
        compAttr.array = True
        compAttr.usesArrayDataBuilder = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_int_atr(cls, long_name, short_name, value, maximum=None, minimum=None, soft_maximum=None, soft_minimum=None, keyable=True):
        numAttr = om.MFnNumericAttribute()
        #
        atr = numAttr.create(long_name, short_name, om.MFnNumericData.kInt, int(value))
        numAttr.writable = True
        numAttr.keyable = keyable
        numAttr.storable = True
        numAttr.channelBox = True
        if maximum is not None:
            numAttr.setMax(int(maximum))
        if minimum is not None:
            numAttr.setMin(int(minimum))
        if soft_maximum is not None:
            numAttr.setSoftMax(soft_maximum)
        if soft_minimum is not None:
            numAttr.setSoftMin(soft_minimum)
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_float_atr(cls, long_name, short_name, value, maximum=None, minimum=None, soft_maximum=None, soft_minimum=None, keyable=True):
        numAttr = om.MFnNumericAttribute()
        #
        atr = numAttr.create(long_name, short_name, om.MFnNumericData.kFloat, float(value))
        numAttr.writable = True
        numAttr.keyable = keyable
        numAttr.storable = True
        numAttr.channelBox = True
        if maximum is not None:
            numAttr.setMax(float(maximum))
        if minimum is not None:
            numAttr.setMin(float(minimum))
        if soft_maximum is not None:
            numAttr.setSoftMax(float(soft_maximum))
        if soft_minimum is not None:
            numAttr.setSoftMin(float(soft_minimum))
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_bool_atr(cls, long_name, short_name, value, keyable=True):
        numAttr = om.MFnNumericAttribute()
        #
        atr = numAttr.create(long_name, short_name, om.MFnNumericData.kBoolean, value)
        numAttr.writable = True
        numAttr.keyable = keyable
        numAttr.storable = True
        numAttr.channelBox = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_enumerate_atr(cls, long_name, short_name, value, keyable=True):
        _atr = om.MFnEnumAttribute()
        #
        atr = _atr.create(long_name, short_name, 0)
        for seq, i in enumerate(value):
            _atr.addField(i, seq)
        #
        _atr.writable = True
        _atr.keyable = keyable
        _atr.storable = True
        _atr.channelBox = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_point_atr(cls, long_name, short_name, value):
        numAttr = om.MFnNumericAttribute()
        #
        atr = numAttr.createPoint(long_name, short_name)
        numAttr.default = value
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def get_mesh_atr(cls, long_name, short_name):
        typed_atr = om.MFnTypedAttribute()
        atr = typed_atr.create(
            long_name, short_name,
            om.MFnData.kMesh
        )
        typed_atr.hidden = True
        typed_atr.writable = True
        typed_atr.storable = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def get_curve_atr(cls, long_name, short_name):
        typed_atr = om.MFnTypedAttribute()
        atr = typed_atr.create(
            long_name, short_name,
            om.MFnData.kNurbsCurve
        )
        typed_atr.hidden = True
        typed_atr.writable = True
        typed_atr.storable = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def get_surface_atr(cls, long_name, short_name):
        typed_atr = om.MFnTypedAttribute()
        atr = typed_atr.create(
            long_name, short_name,
            om.MFnData.kNurbsSurface
        )
        typed_atr.hidden = True
        typed_atr.writable = True
        typed_atr.storable = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_geometry_atr(cls, long_name, short_name, geometry_type):
        typed_atr = om.MFnTypedAttribute()
        atr = typed_atr.create(
            long_name, short_name,
            geometry_type
        )
        typed_atr.hidden = True
        typed_atr.writable = True
        typed_atr.storable = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def set_atrs_connect(cls, ss, ts):
        for s in ss:
            for t in ts:
                # noinspection PyUnresolvedReferences
                cls.attributeAffects(
                    s, t,
                )


# node
class CurveToMeshNode(
    omui.MPxLocatorNode,
    NodeBasic
):
    obj_type_name = 'curveToMesh'
    # noinspection PyArgumentList
    obj_type_id = om.MTypeId(0x8700A)
    obj_type_category = 'lynxi/geometry'
    #
    input_curve_atr = om.MObject()
    input_mesh_atr = om.MObject()
    output_mesh_atr = om.MObject()
    #
    v_uniform_enable_atr = om.MObject()
    base_attach_to_mesh_enable_atr = om.MObject()
    order_atr = om.MObject()
    #
    u_auto_division_enable_atr = om.MObject()
    v_auto_division_enable_atr = om.MObject()
    #
    u_division_atr = om.MObject()
    v_division_atr = om.MObject()
    #
    u_sample_atr = om.MObject()
    v_sample_atr = om.MObject()
    #
    width_atr = om.MObject()
    width_extra_atr = om.MObject()
    #
    spin_atr = om.MObject()
    spin_extra_atr = om.MObject()
    #
    twist_atr = om.MObject()
    taper_atr = om.MObject()
    arch_atr = om.MObject()
    arch_attach_curve_enable_atr = om.MObject()
    arch_extra_atr = om.MObject()
    #
    start_index_atr = om.MObject()
    v_end_index_atr = om.MObject()
    #
    u_texture_coord_tile_width_atr = om.MObject()
    v_texture_coord_tile_width_atr = om.MObject()
    def __init__(self):
        super(CurveToMeshNode, self).__init__()
    @staticmethod
    def _update_fnc_(*args):
        if not args[0].isNull():
            cmd = CurveToMeshData(*args)
            cmd.update()
    @classmethod
    def initializer(cls):
        cls.input_curve_atr = cls.add_geometry_atr(
            'inputCurve', 'iptcrv',
            om.MFnData.kNurbsCurve
        )
        cls.input_mesh_atr = cls.add_geometry_atr(
            'inputMesh', 'iptmsh',
            om.MFnData.kMesh
        )
        #
        cls.output_mesh_atr = cls.add_geometry_atr(
            'outputMesh', 'optmsh',
            om.MFnData.kMesh
        )
        #
        cls.v_uniform_enable_atr = cls.add_bool_atr(
            'uniformEnable', 'ufmEn',
            value=1
        )
        cls.base_attach_to_mesh_enable_atr = cls.add_bool_atr(
            'baseAttachToMeshEnable', 'batme',
            value=1
        )
        cls.order_atr = cls.add_enumerate_atr(
            'order', 'o',
            value=['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']
        )
        cls.u_auto_division_enable_atr = cls.add_bool_atr(
            'autoUDivisionEnable', 'aude',
            value=1
        )
        cls.v_auto_division_enable_atr = cls.add_bool_atr(
            'autoVDivisionEnable', 'avde',
            value=1
        )
        # Custom
        cls.v_division_atr = cls.add_int_atr(
            'vDivision', 'vd',
            value=32,
            minimum=2
        )
        cls.u_division_atr = cls.add_int_atr(
            'uDivision', 'ud',
            value=2,
            minimum=2
        )
        #
        cls.u_sample_atr = cls.add_int_atr(
            'uSample', 'usp',
            value=4,
            minimum=1, maximum=64
        )
        cls.v_sample_atr = cls.add_int_atr(
            'vSample', 'vsp',
            value=4,
            minimum=1, maximum=64
        )
        # Modify
        cls.width_atr = cls.add_float_atr(
            'width', 'w',
            value=1,
            minimum=0
        )
        cls.width_extra_atr = cls.add_comp_atr(
            'widthExtra', 'we'
        )
        #
        cls.spin_atr = cls.add_float_atr(
            'spin', 's',
            value=0
        )
        cls.spin_extra_atr = cls.add_comp_atr(
            'spinExtra', 'se'
        )
        #
        cls.twist_atr = cls.add_float_atr(
            'twist', 'tw',
            value=0
        )
        cls.taper_atr = cls.add_float_atr(
            'taper', 'tp',
            value=1,
            minimum=0
        )
        cls.arch_attach_curve_enable_atr = cls.add_bool_atr(
            'archAttachCurveEnable', 'aace',
            value=1
        )
        cls.arch_atr = cls.add_float_atr(
            'arch', 'a',
            value=0,
            minimum=-1, maximum=1
        )
        cls.arch_extra_atr = cls.add_comp_atr(
            'archExtra', 'ae'
        )
        #
        cls.v_start_index_atr = cls.add_float_atr(
            'startIndex', 'si',
            value=0,
            minimum=0, maximum=1
        )
        cls.v_end_index_atr = cls.add_float_atr(
            'endIndex', 'ei',
            value=1,
            minimum=0, maximum=1
        )
        #
        cls.u_texture_coord_tile_width_atr = cls.add_float_atr(
            'uTextureCoordTileWidth', 'utctw',
            value=0.01,
            minimum=0
        )
        cls.v_texture_coord_tile_width_atr = cls.add_float_atr(
            'vTextureCoordTileWidth', 'vtctw',
            value=0.01,
            minimum=0
        )
        #
        ss = [
            cls.input_curve_atr,
            cls.input_mesh_atr,
            cls.v_uniform_enable_atr,
            cls.base_attach_to_mesh_enable_atr,
            cls.order_atr,
            cls.u_auto_division_enable_atr,
            cls.v_auto_division_enable_atr,
            cls.u_division_atr,
            cls.v_division_atr,
            cls.u_sample_atr,
            cls.v_sample_atr,
            cls.width_atr,
            cls.width_extra_atr,
            cls.spin_atr,
            cls.spin_extra_atr,
            cls.twist_atr,
            cls.taper_atr,
            cls.arch_attach_curve_enable_atr,
            cls.arch_atr,
            cls.arch_extra_atr,
            cls.v_start_index_atr,
            cls.v_end_index_atr,
            #
            cls.u_texture_coord_tile_width_atr,
            cls.v_texture_coord_tile_width_atr,
        ]
        ts = [
            cls.output_mesh_atr
        ]
        #
        cls.set_atrs_connect(ss, ts)
    @classmethod
    def create(cls):
        node = CurveToMeshNode()
        return node
    # noinspection PyMethodOverriding
    def compute(self, plug, data_block):
        if (
                plug == CurveToMeshNode.output_mesh_atr
                ):
            #
            input_curve = data_block.inputValue(CurveToMeshNode.input_curve_atr)
            input_curve_value = input_curve.asNurbsCurve()
            #
            if input_curve_value.isNull() is False:
                input_mesh = data_block.inputValue(CurveToMeshNode.input_mesh_atr)
                input_mesh_value = input_mesh.asMesh()
                #
                width = data_block.inputValue(CurveToMeshNode.width_atr)
                width_value = width.asFloat()
                height_value = om.MFnNurbsCurve(input_curve_value).length()
                #
                u_auto_division_enable = data_block.inputValue(CurveToMeshNode.u_auto_division_enable_atr)
                u_auto_division_enable_value = u_auto_division_enable.asBool()
                v_auto_division_enable = data_block.inputValue(CurveToMeshNode.v_auto_division_enable_atr)
                v_auto_division_enable_value = v_auto_division_enable.asBool()
                #
                u_sample = data_block.inputValue(CurveToMeshNode.u_sample_atr)
                u_sample_value = u_sample.asInt()
                v_sample = data_block.inputValue(CurveToMeshNode.v_sample_atr)
                v_sample_value = v_sample.asInt()
                #
                v_division = data_block.inputValue(CurveToMeshNode.v_division_atr)
                u_division = data_block.inputValue(CurveToMeshNode.u_division_atr)
                if u_auto_division_enable_value is True:
                    u_division.setInt(MtdBasic._get_division_(width_value, u_sample_value))
                if v_auto_division_enable_value is True:
                    v_division.setInt(MtdBasic._get_division_(height_value, v_sample_value))
                #
                u_division_value = u_division.asInt()
                v_division_value = v_division.asInt()
                #
                v_uniform_enable = data_block.inputValue(CurveToMeshNode.v_uniform_enable_atr)
                v_uniform_enable_value = v_uniform_enable.asBool()
                #
                base_attach_to_mesh_enable = data_block.inputValue(CurveToMeshNode.base_attach_to_mesh_enable_atr)
                base_attach_to_mesh_enable_value = base_attach_to_mesh_enable.asBool()
                order = data_block.inputValue(CurveToMeshNode.order_atr)
                order_value = order.asShort()
                # noinspection PyArgumentList
                width_extra_value = om.MRampAttribute(self.thisMObject(), CurveToMeshNode.width_extra_atr)
                #
                spin = data_block.inputValue(CurveToMeshNode.spin_atr)
                spin_value = spin.asFloat()
                # noinspection PyArgumentList
                spin_extra_value = om.MRampAttribute(self.thisMObject(), CurveToMeshNode.spin_extra_atr)
                #
                twist = data_block.inputValue(CurveToMeshNode.twist_atr)
                twist_value = twist.asFloat()
                taper = data_block.inputValue(CurveToMeshNode.taper_atr)
                taper_value = taper.asFloat()
                #
                arch_attach_curve_enable = data_block.inputValue(CurveToMeshNode.arch_attach_curve_enable_atr)
                arch_attach_curve_enable_value = arch_attach_curve_enable.asBool()
                arch = data_block.inputValue(CurveToMeshNode.arch_atr)
                arch_value = arch.asFloat()
                arch_extra_value = om.MRampAttribute(self.thisMObject(), CurveToMeshNode.arch_extra_atr)
                #
                v_start_index = data_block.inputValue(CurveToMeshNode.v_start_index_atr)
                v_start_index_value = v_start_index.asFloat()
                v_end_index = data_block.inputValue(CurveToMeshNode.v_end_index_atr)
                v_end_index_value = v_end_index.asFloat()
                #
                u_texture_coord_tile_width = data_block.inputValue(CurveToMeshNode.u_texture_coord_tile_width_atr)
                u_texture_coord_tile_width_value = u_texture_coord_tile_width.asFloat()
                v_texture_coord_tile_width = data_block.inputValue(CurveToMeshNode.v_texture_coord_tile_width_atr)
                v_texture_coord_tile_width_value = v_texture_coord_tile_width.asFloat()
                #
                output_mesh = data_block.outputValue(CurveToMeshNode.output_mesh_atr)
                output_mesh_value = om.MFnMeshData()
                output_mesh_create = output_mesh_value.create()
                #
                self._update_fnc_(
                    self.thisMObject(),
                    input_curve_value, input_mesh_value,
                    output_mesh_create,
                    v_uniform_enable_value,
                    base_attach_to_mesh_enable_value,
                    order_value,
                    u_auto_division_enable_value, v_auto_division_enable_value,
                    u_division_value, v_division_value,
                    width_value, width_extra_value,
                    spin_value, spin_extra_value,
                    twist_value, taper_value,
                    arch_attach_curve_enable_value, arch_value, arch_extra_value,
                    v_start_index_value, v_end_index_value,
                    u_sample_value, v_sample_value,
                    u_texture_coord_tile_width_value, v_texture_coord_tile_width_value,
                )
                #
                output_mesh.setMObject(output_mesh_create)
                data_block.setClean(plug)
        else:
            return None


#
class meshToSurface(
    omui.MPxLocatorNode,
    NodeBasic
):
    obj_type_name = 'meshToSurface'
    # noinspection PyArgumentList
    obj_type_id = om.MTypeId(0x8700C)
    obj_type_category = 'lynxi/geometry'
    #
    input_mesh_atr = om.MObject()
    output_surface_atr = om.MObject()
    #
    direction_atr = om.MObject()
    def __init__(self):
        super(meshToSurface, self).__init__()
    @classmethod
    def initializer(cls):
        cls.input_mesh_atr = cls.add_geometry_atr(
            'inputMesh', 'inmsh',
            om.MFnData.kMesh
        )
        #
        cls.output_surface_atr = cls.add_geometry_atr(
            'outputSurface', 'otsfc',
            om.MFnData.kNurbsSurface
        )
        #
        cls.direction_atr = cls.add_int_atr(
            'direction', 'dir',
            value=0,
            minimum=0, maximum=3,
            soft_minimum=0, soft_maximum=3
        )
        #
        ss = [
            cls.input_mesh_atr,
        ]
        ts = [
            cls.output_surface_atr
        ]
        cls.set_atrs_connect(ss, ts)
    @classmethod
    def create(cls):
        node = meshToSurface()
        return node
    @staticmethod
    def _update_fnc_(*args):
        if not args[0].isNull():
            MeshToSurfaceData(*args).set_run()
    # noinspection PyMethodOverriding
    def compute(self, plug, data_block):
        if (
                plug in [meshToSurface.output_surface_atr]
                ):
            input_mesh = data_block.inputValue(meshToSurface.input_mesh_atr)
            input_mesh_value = input_mesh.asMesh()
            #
            direction = data_block.inputValue(meshToSurface.direction_atr)
            direction_value = direction.asInt()
            #
            output_surface = data_block.outputValue(meshToSurface.output_surface_atr)
            output_surface_value = om.MFnNurbsSurfaceData()
            output_surface_create = output_surface_value.create()
            #
            self._update_fnc_(
                self.thisMObject(),
                input_mesh_value,
                output_surface_create,
                direction_value
            )
            #
            output_surface.setMObject(output_surface_create)
            data_block.setClean(plug)
        else:
            return None


#
class xgenToCurve(
    omui.MPxLocatorNode,
    NodeBasic
):
    obj_type_name = 'xgenToCurve'
    # noinspection PyArgumentList
    obj_type_id = om.MTypeId(0x8700E)
    obj_type_category = 'lynxi/geometry'
    #
    input_xgen_guide_atr = om.MObject()
    input_mesh_atr = om.MObject()
    output_curve_atr = om.MObject()
    def __init__(self):
        super(xgenToCurve, self).__init__()
    @staticmethod
    def _update_fnc_(*args):
        if not args[0].isNull():
            cmd = XgenToCurveCmd(*args)
            cmd.update()
    @classmethod
    def initializer(cls):
        cls.input_xgen_guide_atr = cls.add_geometry_atr(
            'inputXgenGuide', 'iptxgngud',
            om.MFnData.kPluginGeometry
        )
        cls.input_mesh_atr = cls.add_geometry_atr(
            'inputMesh', 'iptmsh',
            om.MFnData.kMesh
        )
        #
        cls.output_curve_atr = cls.add_geometry_atr(
            'outputCurve', 'otcrv',
            om.MFnData.kNurbsCurve
        )
        # ============================================================================================================ #
        ss = [
                cls.input_xgen_guide_atr,
                cls.input_mesh_atr,
            ]
        ts = [
                cls.output_curve_atr
            ]
        cls.set_atrs_connect(ss, ts)
    @classmethod
    def create(cls):
        return xgenToCurve()
    # noinspection PyMethodOverriding
    def compute(self, plug, data_block):
        if (
                plug in [xgenToCurve.output_curve_atr]
                ):
            #
            input_xgen_guide = data_block.inputValue(xgenToCurve.input_xgen_guide_atr)
            input_xgen_guide_value = input_xgen_guide.asPluginData()
            #
            input_mesh = data_block.inputValue(xgenToCurve.input_mesh_atr)
            input_mesh_value = input_mesh.asMesh()
            #
            output_curve = data_block.outputValue(xgenToCurve.output_curve_atr)
            output_curve_data = om.MFnNurbsCurveData()
            output_curve_create = output_curve_data.create()
            #
            self._update_fnc_(
                self.thisMObject(),
                input_xgen_guide_value, input_mesh_value,
                output_curve_create
            )
            #
            output_curve.setMObject(output_curve_create)
            data_block.setClean(plug)
        else:
            return None


class surfaceToMesh(
    omui.MPxLocatorNode,
    NodeBasic
):
    obj_type_name = 'surfaceToMesh'
    # noinspection PyArgumentList
    obj_type_id = om.MTypeId(0x8700F)
    obj_type_category = 'lynxi/geometry'
    #
    input_surface_atr = om.MObject()
    output_curve_atr = om.MObject()
    output_mesh_atr = om.MObject()
    #
    u_uniform_enable_atr = om.MObject()
    v_uniform_enable_atr = om.MObject()
    #
    u_division_atr = om.MObject()
    v_division_atr = om.MObject()
    def __init__(self):
        super(surfaceToMesh, self).__init__()
    @classmethod
    def initializer(cls):
        cls.input_surface_atr = cls.add_geometry_atr(
            'inputSurface', 'insfc',
            om.MFnData.kNurbsSurface
        )
        #
        cls.output_curve_atr = cls.add_geometry_atr(
            'outputCurve', 'otcrv',
            om.MFnData.kNurbsCurve
        )
        cls.output_mesh_atr = cls.add_geometry_atr(
            'outputMesh', 'otmsh',
            om.MFnData.kMesh
        )
        cls.u_uniform_enable_atr = cls.add_bool_atr(
            'uUniformEnable', 'uue',
            value=1
        )
        cls.v_uniform_enable_atr = cls.add_bool_atr(
            'vUniformEnable', 'vue',
            value=1
        )
        #
        cls.u_division_atr = cls.add_int_atr(
            'uDivision', 'ud',
            value=8,
            minimum=2
        )
        cls.v_division_atr = cls.add_int_atr(
            'vDivision', 'vd',
            value=8,
            minimum=2
        )
        #
        ss = [
            cls.input_surface_atr,
            #
            cls.u_uniform_enable_atr, cls.v_uniform_enable_atr,
            #
            cls.u_division_atr, cls.v_division_atr,
        ]
        ts = [
            cls.output_curve_atr, cls.output_mesh_atr
        ]
        cls.set_atrs_connect(ss, ts)
    @staticmethod
    def _update_fnc_(*args):
        if not args[0].isNull():
            SurfaceToMeshData(*args).update()
    @classmethod
    def create(cls):
        return surfaceToMesh()
    # noinspection PyMethodOverriding
    def compute(self, plug, data_block):
        if (
            plug in [surfaceToMesh.output_curve_atr, surfaceToMesh.output_mesh_atr]
        ):
            #
            input_surface = data_block.inputValue(surfaceToMesh.input_surface_atr)
            input_surface_value = input_surface.asNurbsSurface()
            #
            output_curve = data_block.outputValue(surfaceToMesh.output_curve_atr)
            output_curve_value = om.MFnNurbsCurveData()
            output_curve_create = output_curve_value.create()
            #
            output_mesh = data_block.outputValue(surfaceToMesh.output_mesh_atr)
            output_mesh_value = om.MFnMeshData()
            output_mesh_create = output_mesh_value.create()
            #
            u_uniform_enable = data_block.inputValue(surfaceToMesh.u_uniform_enable_atr)
            u_uniform_enable_value = u_uniform_enable.asBool()
            v_uniform_enable = data_block.inputValue(surfaceToMesh.v_uniform_enable_atr)
            v_uniform_enable_value = v_uniform_enable.asBool()
            #
            u_division = data_block.inputValue(surfaceToMesh.u_division_atr)
            u_division_value = u_division.asInt()
            v_division = data_block.inputValue(surfaceToMesh.v_division_atr)
            v_division_value = v_division.asInt()
            #
            self._update_fnc_(
                self.thisMObject(),
                input_surface_value,
                output_curve_create, output_mesh_create,
                u_uniform_enable_value, v_uniform_enable_value,
                u_division_value, v_division_value
            )
            #
            output_curve.setMObject(output_curve_create)
            #
            output_mesh.setMObject(output_mesh_create)
            #
            data_block.setClean(plug)
        else:
            return None


# initialize
def initializePlugin(obj):
    plug = om.MFnPlugin(obj, 'ChangBao.Dong', '1.0.0', 'Any')
    all_args = [
        (CurveToMeshNode.obj_type_name, CurveToMeshNode.obj_type_id, CurveToMeshNode.create, CurveToMeshNode.initializer),
        (meshToSurface.obj_type_name, meshToSurface.obj_type_id, meshToSurface.create, meshToSurface.initializer),
        (xgenToCurve.obj_type_name, xgenToCurve.obj_type_id, xgenToCurve.create, xgenToCurve.initializer),
        (surfaceToMesh.obj_type_name, surfaceToMesh.obj_type_id, surfaceToMesh.create, surfaceToMesh.initializer)
    ]
    for i_args in all_args:
        try:
            plug.registerNode(*i_args)
        except:
            sys.stderr.write('Failed to Register Node: "{}"'.format(i_args[0]))
            raise


# uninitialize
def uninitializePlugin(obj):
    plug = om.MFnPlugin(obj)
    all_args = [
        (CurveToMeshNode.obj_type_name, CurveToMeshNode.obj_type_id, CurveToMeshNode.create, CurveToMeshNode.initializer),
        (meshToSurface.obj_type_name, meshToSurface.obj_type_id, meshToSurface.create, meshToSurface.initializer),
        (xgenToCurve.obj_type_name, xgenToCurve.obj_type_id, xgenToCurve.create, xgenToCurve.initializer),
        (surfaceToMesh.obj_type_name, surfaceToMesh.obj_type_id, surfaceToMesh.create, surfaceToMesh.initializer)
    ]
    for i_args in all_args:
        # Deregister Node
        try:
            plug.deregisterNode(
                i_args[1]
            )
        except:
            sys.stderr.write('Failed to Deregister Node: "{}"'.format(i_args[0]))
            raise
