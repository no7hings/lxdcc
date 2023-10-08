# encoding=utf-8
from __future__ import division

import copy
import logging

import sys

import math
# noinspection PyUnresolvedReferences
import maya.mel as mel
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.api.OpenMaya as om
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.api.OpenMayaUI as omui
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.api.OpenMayaRender as omrd
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.OpenMayaRender as omrd1


# Use 2.0 API
maya_useNewAPI = True


def trace_error(text):
    sys.stderr.write(text)


def trace(text):
    sys.stdout.write(text)


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
    def _get_om_mesh_fnc_(cls, path):
        return om.MFnMesh(cls._get_om_dag_path_(path))
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
    @staticmethod
    def _get_curve_knots_(count, degree, form):
        if form == 1:
            if count == 2:
                return [0.0] * degree + [1.0]
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
                lis.append(float(seq+1) * knot_maximum/(add_count+1))
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
            add_count = count-N-1
            for seq in range(add_count):
                lis.append(float(seq+1) * knot_maximum/(add_count+1))
            #
            [lis.append(knot_maximum+i) for i in range(degree)]
            return lis
    @classmethod
    def _get_surface_knots_(cls, count, degree, form):
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
    def get_radian_by_coord(cls, x1, y1, x2, y2):
        radian = 0.0
        #
        r0 = 0.0
        r90 = math.pi / 2.0
        r180 = math.pi
        r270 = 3.0 * math.pi / 2.0
        #
        if x1 == x2:
            if y1 < y2:
                radian = r0
            elif y1 > y2:
                radian = r180
        elif y1 == y2:
            if x1 < x2:
                radian = r90
            elif x1 > x2:
                radian = r270
        elif x1 < x2 and y1 < y2:
            radian = math.atan2((-x1 + x2), (-y1 + y2))
        elif x1 < x2 and y1 > y2:
            radian = r90 + math.atan2((y1 - y2), (-x1 + x2))
        elif x1 > x2 and y1 > y2:
            radian = r180 + math.atan2((x1 - x2), (y1 - y2))
        elif x1 > x2 and y1 < y2:
            radian = r270 + math.atan2((-y1 + y2), (x1 - x2))
        #
        return radian


class NodeBasic(object):
    @classmethod
    def add_comp_atr(cls, long_name, short_name):
        cmp_atr = om.MFnCompoundAttribute()
        num_atr = om.MFnNumericAttribute()
        enm_atr = om.MFnEnumAttribute()
        #
        atr = cmp_atr.create(long_name, short_name)
        #
        position_atr = num_atr.create(
            long_name + '_Position', short_name + 'p',
            om.MFnNumericData.kFloat
        )
        #
        value_atr = num_atr.create(
            long_name + '_FloatValue', short_name + 'v',
            om.MFnNumericData.kFloat
        )
        #
        interp_atr = enm_atr.create(
            long_name + '_Interp', short_name + 'i'
        )
        enm_atr.addField('None', 0)
        enm_atr.addField('Linear', 1)
        enm_atr.addField('Smooth', 2)
        enm_atr.addField('Spline', 3)
        enm_atr.default = 3
        cmp_atr.addChild(position_atr)
        cmp_atr.addChild(value_atr)
        cmp_atr.addChild(interp_atr)
        #
        cmp_atr.storable = True
        cmp_atr.array = True
        cmp_atr.usesArrayDataBuilder = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_int_atr(cls, long_name, short_name, value, maximum=None, minimum=None, soft_maximum=None, soft_minimum=None, keyable=True):
        num_atr = om.MFnNumericAttribute()
        #
        atr = num_atr.create(long_name, short_name, om.MFnNumericData.kInt, int(value))
        num_atr.writable = True
        num_atr.keyable = keyable
        num_atr.storable = True
        num_atr.channelBox = True
        if maximum is not None:
            num_atr.setMax(int(maximum))
        if minimum is not None:
            num_atr.setMin(int(minimum))
        if soft_maximum is not None:
            num_atr.setSoftMax(soft_maximum)
        if soft_minimum is not None:
            num_atr.setSoftMin(soft_minimum)
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_float_atr(cls, long_name, short_name, value=None, maximum=None, minimum=None, soft_maximum=None, soft_minimum=None, keyable=True, array=False, hidden=False):
        num_atr = om.MFnNumericAttribute()
        #
        if value is not None:
            atr = num_atr.create(long_name, short_name, om.MFnNumericData.kFloat, float(value))
        else:
            atr = num_atr.create(long_name, short_name, om.MFnNumericData.kFloat)
        #
        num_atr.writable = True
        num_atr.keyable = keyable
        num_atr.storable = True
        num_atr.channelBox = True
        if hidden is True:
            num_atr.hidden = True
        #
        if array is True:
            num_atr.array = True
            num_atr.usesArrayDataBuilder = True
        #
        if maximum is not None:
            num_atr.setMax(float(maximum))
        if minimum is not None:
            num_atr.setMin(float(minimum))
        if soft_maximum is not None:
            num_atr.setSoftMax(float(soft_maximum))
        if soft_minimum is not None:
            num_atr.setSoftMin(float(soft_minimum))
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_bool_atr(cls, long_name, short_name, value, keyable=True):
        num_atr = om.MFnNumericAttribute()
        #
        atr = num_atr.create(
            long_name, short_name,
            om.MFnNumericData.kBoolean,
            value
        )
        num_atr.writable = True
        num_atr.keyable = keyable
        num_atr.storable = True
        num_atr.channelBox = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_enumerate_atr(cls, long_name, short_name, values, value=None, keyable=True):
        enm_atr = om.MFnEnumAttribute()
        #
        atr = enm_atr.create(long_name, short_name, 0)
        for seq, i in enumerate(values):
            enm_atr.addField(i, seq)

        if value is not None:
            enm_atr.default = value
        #
        enm_atr.writable = True
        enm_atr.keyable = keyable
        enm_atr.storable = True
        enm_atr.channelBox = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_point_atr(cls, long_name, short_name, value=None, keyable=True, array=False, array_builder=False):
        num_atr = om.MFnNumericAttribute()
        #
        atr = num_atr.createPoint(long_name, short_name)
        #
        num_atr.writable = True
        num_atr.keyable = keyable
        num_atr.storable = True
        num_atr.channelBox = True
        if value is not None:
            num_atr.default = value
        if array is True:
            num_atr.array = True
            if array_builder is True:
                num_atr.usesArrayDataBuilder = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_geometry_atr(cls, long_name, short_name, geometry_type, array=False):
        typ_atr = om.MFnTypedAttribute()
        atr = typ_atr.create(
            long_name, short_name,
            geometry_type
        )
        typ_atr.hidden = True
        typ_atr.writable = True
        typ_atr.storable = True
        if array is True:
            typ_atr.array = True
            # typ_atr.usesArrayDataBuilder = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_message_atr(cls, long_name, short_name):
        msg_atr = om.MFnMessageAttribute()
        atr = msg_atr.create(
            long_name, short_name
        )
        msg_atr.writable = True
        msg_atr.storable = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_string_atr(cls, long_name, short_name, value=None, array=False, writable=True):
        typ_atr = om.MFnTypedAttribute()
        if value is not None:
            s = om.MFnStringData()
            s_value = s.create(value)
            atr = typ_atr.create(
                long_name, short_name,
                om.MFnData.kString,
                s_value
            )
        else:
            atr = typ_atr.create(
                long_name, short_name,
                om.MFnData.kString
            )
        typ_atr.writable = writable
        typ_atr.storable = True
        if array is True:
            typ_atr.array = True
            # typ_atr.usesArrayDataBuilder = True
        # noinspection PyUnresolvedReferences
        cls.addAttribute(atr)
        return atr
    @classmethod
    def add_comp_curve_array_atr(cls, long_name, short_name):
        cmp_atr = om.MFnCompoundAttribute()
        typ_atr = om.MFnTypedAttribute()
        num_atr = om.MFnNumericAttribute()
        #
        atr = cmp_atr.create(long_name, short_name)
        #
        curve_atr = typ_atr.create(
            long_name + 'Curve', short_name + 'c',
            om.MFnData.kNurbsCurve
        )
        #
        position_atr = num_atr.create(
            long_name + 'Position', short_name + 'p',
            om.MFnNumericData.kFloat
        )
        cmp_atr.addChild(curve_atr)
        cmp_atr.addChild(position_atr)
        #
        cmp_atr.storable = True
        cmp_atr.array = True
        # cmp_atr.usesArrayDataBuilder = True
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


class CurveCreate(object):
    def __init__(self, om_create):
        self._om_create = om_create

    def update(self, degree, form, points):
        count = len(points)
        knots = MtdBasic._get_curve_knots_(count, degree, form)
        om_obj = om.MFnNurbsCurve()
        om_obj.create(
            points,
            knots, degree, form,
            False,
            True,
            parent=self._om_create
        )


class SurfaceCreate(object):
    def __init__(self, om_create):
        self._om_create = om_create

    def update(self, u_degree, v_degree, u_form, v_form, u_count, v_count, points):
        u_knots, v_knots = (
            MtdBasic._get_surface_knots_(u_count, u_degree, u_form),
            MtdBasic._get_surface_knots_(v_count, v_degree, v_form)
        )
        om_obj = om.MFnNurbsSurface()
        om_obj.create(
            points,
            u_knots, v_knots,
            u_degree, v_degree,
            u_form, v_form,
            True,
            parent=self._om_create
        )

    def update_as_closed(self, u_degree, v_degree, u_form, v_form, u_count, v_count, points):
        if v_degree > 1:
            u_knots, v_knots = (
                MtdBasic._get_surface_knots_(u_count, u_degree, u_form),
                MtdBasic._get_surface_knots_(v_count, v_degree, v_form)
            )
        else:
            u_knots, v_knots = (
                MtdBasic._get_surface_knots_(u_count, u_degree, u_form),
                MtdBasic._get_surface_knots_(v_count, v_degree, 1)
            )
        om_obj = om.MFnNurbsSurface()
        om_obj.create(
            points,
            u_knots, v_knots,
            u_degree, v_degree,
            u_form, v_form,
            True,
            parent=self._om_create
        )


class MeshCreate(object):
    def __init__(self, om_create):
        self._om_create = om_create
        self._om_fnc = None
    @classmethod
    def get_face_vertices(cls, u_count, v_count):
        counts = []
        indices = []
        s = [0, 1, 2 + u_count, 1 + u_count]
        for v in range(v_count):
            for u in range(u_count):
                counts.append(4)
                if u == 0:
                    i_s = [(i + v * (u_count + 1)) for i in s]
                else:
                    i_s = [(i + v * (u_count + 1) + u) for i in s]
                #
                indices.extend(i_s)
        return counts, indices

    def update(self, face_vertex_counts, face_vertex_indices, points):
        self._om_fnc = om.MFnMesh()
        #
        self._om_fnc.create(
            points,
            face_vertex_counts, face_vertex_indices,
            parent=self._om_create
        )

    def update_smoothing(self, edge_indices, boolean):
        if self._om_fnc is not None:
            self._om_fnc.setEdgeSmoothings(edge_indices, [boolean]*len(edge_indices))
            self._om_fnc.updateSurface()


class CurveCreateData(object):
    @staticmethod
    def _to_close_points_(points):
        ps = copy.copy(points)
        ps.append(ps[1])
        return ps


class SurfaceCreateData(object):
    def __init__(self, points_map):
        self._points_map = points_map
    @classmethod
    def get_point_between(cls, point_0, point_1):
        x, y, z = (point_0.x + point_1.x) / 2, (point_0.y + point_1.y) / 2, (point_0.z + point_1.z) / 2
        return om.MPoint(x, y, z)

    def _get_center_u_points_at_(self, v_index):
        u_vertex_indices = self._points_map[v_index]
        u_count = len(u_vertex_indices)
        u_points = []
        for u_index in range(u_count):
            u_point = self._points_map[v_index][u_index]
            if u_index == 0:
                next_u_point = self._points_map[v_index][u_index+1]
                center_u_point = self.get_point_between(u_point, next_u_point)
                u_points.extend([u_point, center_u_point])
            elif u_index == u_count - 1:
                pre_u_point = self._points_map[v_index][u_index-1]
                center_u_point = self.get_point_between(pre_u_point, u_point)
                u_points.extend([center_u_point, u_point])
            else:
                u_points.append(u_point)
        return u_points
    #
    def _get_center_u_points_between_(self, v_index_0, v_index_1):
        u_vertex_indices_0 = self._points_map[v_index_0]
        u_points_0 = self._points_map[v_index_0]
        u_points_1 = self._points_map[v_index_1]
        u_count = len(u_points_0)
        u_points = []
        for u_index, u_vertex_index_0 in enumerate(u_vertex_indices_0):
            u_point_0 = u_points_0[u_index]
            u_point_1 = u_points_1[u_index]
            u_point = self.get_point_between(u_point_0, u_point_1)
            if u_index == 0:
                next_u_point_0 = u_points_0[u_index+1]
                next_u_point_1 = u_points_1[u_index+1]
                center_u_point_0 = self.get_point_between(u_point_0, next_u_point_0)
                center_u_point_1 = self.get_point_between(u_point_1, next_u_point_1)
                center_u_point = self.get_point_between(center_u_point_0, center_u_point_1)
                u_points.extend([u_point, center_u_point])
            elif u_index == u_count-1:
                pre_u_point_0 = u_points_0[u_index-1]
                pre_u_point_1 = u_points_1[u_index-1]
                center_u_point_0 = self.get_point_between(pre_u_point_0, u_point_0)
                center_u_point_1 = self.get_point_between(pre_u_point_1, u_point_1)
                center_u_point = self.get_point_between(center_u_point_0, center_u_point_1)
                u_points.extend([center_u_point, u_point])
            else:
                u_points.append(u_point)
        return u_points

    def _get_center_u_points_as_closed_at_(self, v_index):
        u_vertex_indices = self._points_map[v_index]
        u_count = len(u_vertex_indices)
        u_points = []
        for u_index in range(u_count):
            u_point = self._points_map[v_index][u_index]
            u_points.append(u_point)
        return u_points
    #
    def _get_center_u_points_as_closed_between_(self, v_index_0, v_index_1):
        u_vertex_indices_0 = self._points_map[v_index_0]
        u_points_0 = self._points_map[v_index_0]
        u_points_1 = self._points_map[v_index_1]
        u_points = []
        for u_index, u_vertex_index_0 in enumerate(u_vertex_indices_0):
            u_point_0 = u_points_0[u_index]
            u_point_1 = u_points_1[u_index]
            u_point = self.get_point_between(u_point_0, u_point_1)
            u_points.append(u_point)
        return u_points
    @staticmethod
    def _to_v_close_points_(u_count, v_count, points):
        ps = copy.copy(points)
        for i_u in range(u_count):
            i_start_index = i_u * v_count
            i_end_index = (i_u + 1) * v_count - 1
            ps.insert(i_end_index + i_u + 1, ps[i_start_index + i_u + 1])
        return ps

    def get(self):
        points = []
        # u is v and v is u it must be swap
        v_count = len(self._points_map)
        u_count = len(self._points_map[0])
        for i_v in range(v_count):
            u_points = self._get_center_u_points_at_(i_v)
            if i_v == 0:
                center_u_points = self._get_center_u_points_between_(
                    i_v, i_v+1
                )
                points.extend(u_points+center_u_points)
            elif i_v == v_count-1:
                center_u_points = self._get_center_u_points_between_(
                    i_v-1, i_v
                )
                points.extend(center_u_points+u_points)
            else:
                points.extend(u_points)
        # u-count, v-count,  cv-points
        return v_count+2, u_count+2, points

    def get_as_closed(self):
        points = []
        # u is v and v is u it must be swap
        v_count = len(self._points_map)
        u_count = len(self._points_map[0])
        for i_v in range(v_count):
            u_points = self._get_center_u_points_as_closed_at_(i_v)
            if i_v == 0:
                center_u_points = self._get_center_u_points_as_closed_between_(
                    i_v, i_v+1
                )
                points.extend(u_points+center_u_points)
            elif i_v == v_count-1:
                center_u_points = self._get_center_u_points_as_closed_between_(
                    i_v-1, i_v
                )
                points.extend(center_u_points+u_points)
            else:
                points.extend(u_points)
        # u-count, v-count,  cv-points
        return v_count+2, u_count, points


class MeshCreateData(object):
    def __init__(self, points_map):
        self._points_map = points_map
    @staticmethod
    def get_face_vertices(u_count, v_count):
        counts = om.MIntArray()
        indices = om.MIntArray()
        s = [0, 1, 2+u_count, 1+u_count]
        for v in range(v_count):
            for u in range(u_count):
                counts.append(4)
                if u == 0:
                    i_s = [(i + v * (u_count+1)) for i in s]
                else:
                    i_s = [(i + v * (u_count+1) + u) for i in s]
                #
                indices += i_s
        return counts, indices
    @staticmethod
    def get_v_edge_indices(u_count, v_count):
        id_start = 0
        list_ = []
        for i_u in range(u_count):
            for i_v in range(v_count):
                i_is_corner = i_u == 0 and i_v == 0
                i_is_u_border = i_v == 0
                i_is_v_border = i_u == 0
                if i_is_corner is True:
                    list_.extend([id_start, id_start + 2])
                    id_start += 4
                elif i_is_v_border is True:
                    list_.extend([id_start, id_start + 2])
                    id_start += 3
                elif i_is_u_border:
                    list_.append(id_start + 1)
                    id_start += 3
                else:
                    list_.append(id_start + 1)
                    id_start += 2
        return list_
    @staticmethod
    def get_u_edge_indices(u_count, v_count):
        id_start = 0
        list_ = []
        for i_u in range(u_count):
            for i_v in range(v_count):
                i_is_corner = i_u == 0 and i_v == 0
                i_is_u_border = i_v == 0
                i_is_v_border = i_u == 0
                if i_is_corner is True:
                    list_.extend([id_start + 1, id_start + 3])
                    id_start += 4
                elif i_is_v_border is True:
                    list_.extend([id_start + 1])
                    id_start += 3
                elif i_is_u_border:

                    list_.extend([id_start, id_start + 2])
                    id_start += 3
                else:
                    list_.append(id_start)
                    id_start += 2
        return list_

    def get(self, grow_mesh_om_fnc=None, attach=False):
        points_map = zip(*self._points_map)
        points = om.MPointArray()
        v_count = len(points_map)
        u_count = len(points_map[0])
        face_vertex_counts, face_vertex_indices = self.get_face_vertices(
            u_count-1, v_count-1
        )
        base_vertex_indices = []
        for i_v in range(v_count):
            for j_u in range(u_count):
                j_index = i_v*u_count+j_u
                if j_u == 0:
                    base_vertex_indices.append(j_index)
                j_point = points_map[i_v][j_u]
                points.append(j_point)
        #
        if attach is True:
            if grow_mesh_om_fnc is not None:
                for i in base_vertex_indices:
                    i_point = points[i]
                    i_p = grow_mesh_om_fnc.getClosestPoint(
                        i_point, space=om.MSpace.kWorld
                    )[0]
                    i_point.x, i_point.y, i_point.z = i_p.x, i_p.y, i_p.z
        return v_count, u_count, face_vertex_counts, face_vertex_indices, points


class InputUBaseCurvesData(object):
    ATR = 'inputUBaseCurves'
    WSP = om.MSpace.kObject
    def __init__(self, om_fnc):
        self._om_fnc = om_fnc

    def get_valid_om_fncs(self):
        om_fncs = []
        p = self._om_fnc.findPlug(self.ATR, 0)
        c = p.numElements()
        for i in range(c):
            i_e = p.elementByLogicalIndex(i)
            i_s = i_e.source()
            if i_s.isNull is False:
                i_node = om.MFnDagNode(i_s.node())
                om_fncs.append(
                    om.MFnNurbsCurve(i_node.getPath())
                )
        return om_fncs
    @classmethod
    def get_at(cls, om_fnc, index, percent, length, p_min, p_max, uniform_enable):
        if uniform_enable is True:
            length_ = MtdBasic._set_value_map_((0, 1), (0, length), percent)
            param = om_fnc.findParamFromLength(length_)
        else:
            param = MtdBasic._set_value_map_((0, 1), (p_min, p_max), percent)
        p = om_fnc.getPointAtParam(param, cls.WSP)
        return om.MPoint(p.x, index, p.z)

    def get(self, count, start_index, end_index, uniform_enable):
        points_map = []
        om_fncs = self.get_valid_om_fncs()
        if om_fncs:
            if len(om_fncs) == 1:
                om_fncs *= 4
            elif len(om_fncs) == 2:
                om_fncs = [om_fncs[0]]*3 + om_fncs[1:]
            elif len(om_fncs) == 3:
                om_fncs += [om_fncs[0]]*2 + om_fncs[2:]
            for i_v, i_om_fnc in enumerate(om_fncs):
                i_points = []
                i_length = i_om_fnc.length()
                i_p_range = i_om_fnc.knotDomain
                i_p_min, i_p_max = i_p_range
                for j_u in range(count+1):
                    if j_u == 0:
                        j_percent = start_index
                    elif j_u == count:
                        j_percent = end_index
                    else:
                        j_percent = MtdBasic._set_value_map_(
                            (0, count),
                            (start_index, end_index),
                            j_u
                        )
                    #
                    j_point = self.get_at(
                        i_om_fnc,
                        i_v, j_percent,
                        i_length, i_p_min, i_p_max,
                        uniform_enable
                    )
                    i_points.append(j_point)
                # reverse for normal invert
                i_points.reverse()
                points_map.append(i_points)
        return points_map


class InputVBaseCurveData(object):
    ATR = 'inputVBaseCurve'
    WSP = om.MSpace.kWorld
    def __init__(self, om_fnc):
        self._om_fnc = om_fnc

    def get_valid_om_fnc(self):
        p = self._om_fnc.findPlug(self.ATR, False)
        s = p.source()
        if s.isNull is False:
            node = om.MFnDagNode(s.node())
            return om.MFnNurbsCurve(node.getPath())
    @classmethod
    def get_at(cls, om_fnc, index, percent, length, p_min, p_max, uniform_enable):
        if uniform_enable is True:
            length_ = MtdBasic._set_value_map_((0, 1), (0, length), percent)
            param = om_fnc.findParamFromLength(length_)
        else:
            param = MtdBasic._set_value_map_((0, 1), (p_min, p_max), percent)
        return om_fnc.getPointAtParam(param, cls.WSP)

    def get(self, count, start_index, end_index, uniform_enable):
        points = []
        om_fnc = self.get_valid_om_fnc()
        if om_fnc:
            length = om_fnc.length()
            p_range = om_fnc.knotDomain
            p_min, p_max = p_range
            #
            for i_index in range(count + 1):
                if i_index == 0:
                    i_percent = start_index
                elif i_index == count:
                    i_percent = end_index
                else:
                    i_percent = MtdBasic._set_value_map_(
                        (0, count),
                        (start_index, end_index),
                        i_index
                    )
                #
                i_point = self.get_at(
                    om_fnc, i_index, i_percent,
                    length, p_min, p_max,
                    uniform_enable
                )
                points.append(i_point)
        return points


class InputVExtraPointsData(object):
    def __init__(self, om_fnc):
        self._om_fnc = om_fnc

    def get(self, atr, count):
        p = self._om_fnc.findPlug(atr, False)
        c = count
        points = om.MPointArray()
        for i in range(c):
            i_e = p.elementByLogicalIndex(i)
            i_c = i_e.numChildren()
            i_point = om.MPoint()
            for j in range(i_c):
                j_c = i_e.child(j)
                i_point[j] = j_c.asFloat()
            #
            i_point.x = i
            #
            points.append(i_point)
        return points


class InputGrowMeshData(object):
    def __init__(self, om_fnc):
        self._om_fnc = om_fnc

    def get_valid_om_fnc(self):
        p = self._om_fnc.findPlug('inputGrowMesh', 0)
        s = p.source()
        if s.isNull is False:
            node = om.MFnDagNode(s.node())
            return om.MFnMesh(node.getPath())

    def get_valid_world_matrix(self):
        om_fnc = self.get_valid_om_fnc()
        if om_fnc is not None:
            plug = om_fnc.findPlug('worldMatrix', 0)
            plug = plug.elementByLogicalIndex(0)
            plug_obj = plug.asMObject()
            matrix_data = om.MFnMatrixData(plug_obj)
            world_matrix = matrix_data.matrix()
            return world_matrix
    #
    def get_valid_world_axis(self):
        world_matrix = self.get_valid_world_matrix()
        if world_matrix:
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

    def get_world_axis(self):
        axis = self.get_valid_world_axis()
        if axis is not None:
            return axis
        v = om.MVector()
        return v.kXaxisVector, v.kYaxisVector, v.kZaxisVector


class OutputUBaseData(object):
    def __init__(self, om_create):
        self._om_create = om_create

    def get(self, u_count, v_count):
        points_map = []
        om_fnc = om.MFnNurbsSurface(self._om_create)
        # u and v is inverted
        u_p_range = om_fnc.knotDomainInV
        u_p_min, u_p_max = u_p_range
        v_p_range = om_fnc.knotDomainInU
        v_p_min, v_p_max = v_p_range
        for i_v in range(v_count + 1):
            i_points = om.MPointArray()
            i_v_percent = float(i_v)/v_count
            i_v_p = MtdBasic._set_value_map_((0, 1), (v_p_min, v_p_max), i_v_percent)
            for j_u in range(u_count + 1):
                j_u_percent = float(j_u)/u_count
                j_u_p = MtdBasic._set_value_map_((0, 1), (u_p_min, u_p_max), j_u_percent)
                j_point = om_fnc.getPointAtParam(i_v_p, j_u_p, om.MSpace.kObject)
                i_points.append(
                    om.MPoint(j_point.x, 0, j_point.z)
                )
            #
            points_map.append(i_points)
        return points_map


class OutputVBaseData(object):
    WSP = om.MSpace.kWorld
    def __init__(self, om_create):
        self._om_create = om_create

    def update_at(self, om_fnc, index, percent, length, p_min, p_max, x_axis, y_axis, z_axis, uniform_enable, order):
        if uniform_enable is True:
            length = MtdBasic._set_value_map_((0, 1), (0, length), percent)
            param = om_fnc.findParamFromLength(length)
        else:
            param = MtdBasic._set_value_map_((0, 1), (p_min, p_max), percent)
        # tangent = z-normal, space=world
        point, normal_z = om_fnc.getDerivativesAtParam(param, self.WSP)
        normal_z = normal_z.normalize()
        #
        if index == 0:
            # ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']
            # xyz
            if order == 0:
                if normal_z.isParallel(y_axis):
                    axis = x_axis
                else:
                    axis = y_axis
            # yzx
            elif order == 1:
                if normal_z.isParallel(z_axis):
                    axis = y_axis
                else:
                    axis = z_axis
            # zxy
            elif order == 2:
                if normal_z.isParallel(x_axis):
                    axis = z_axis
                else:
                    axis = x_axis
            # xzy
            elif order == 3:
                if normal_z.isParallel(z_axis):
                    axis = x_axis
                else:
                    axis = z_axis * -1
            # yxz
            elif order == 4:
                if normal_z.isParallel(x_axis):
                    axis = y_axis
                else:
                    axis = x_axis * -1
            # zyx
            elif order == 5:
                if normal_z.isParallel(y_axis):
                    axis = z_axis
                else:
                    axis = y_axis * -1
            # xyz
            else:
                if normal_z.isParallel(y_axis):
                    axis = x_axis
                else:
                    axis = y_axis
            # Vector Multiplication Cross
            normal_x = normal_z.__rxor__(axis)
            normal_y = normal_x.__rxor__(normal_z)
        else:
            pre_normal_z = self._output_v_base_curve_normals_z[index-1]
            quaternion = pre_normal_z.rotateTo(normal_z)
            #
            pre_normal_x = self._output_v_base_curve_normals_x[index-1]
            normal_x = pre_normal_x.rotateBy(quaternion)
            #
            pre_normal_y = self._output_v_base_curve_normals_y[index-1]
            normal_y = pre_normal_y.rotateBy(quaternion)
        #
        self._output_v_base_curve_percents.append(percent)
        self._output_v_base_curve_points.append(point)
        self._output_v_base_curve_normals_x.append(normal_x.normalize())
        self._output_v_base_curve_normals_y.append(normal_y.normalize())
        self._output_v_base_curve_normals_z.append(normal_z)

    def get(self, count, order, axis, uniform_enable):
        om_fnc = om.MFnNurbsCurve(self._om_create)
        #
        self._output_v_base_curve_percents = om.MFloatArray()
        self._output_v_base_curve_points = om.MPointArray()
        self._output_v_base_curve_normals_x = om.MVectorArray()
        self._output_v_base_curve_normals_y = om.MVectorArray()
        self._output_v_base_curve_normals_z = om.MVectorArray()
        #
        length = om_fnc.length()
        p_range = om_fnc.knotDomain
        p_min, p_max = p_range
        #
        x_axis, y_axis, z_axis = axis
        #
        for i_index in range(count + 1):
            i_percent = float(i_index)/count
            #
            self.update_at(
                om_fnc, i_index, i_percent,
                length, p_min, p_max, x_axis, y_axis, z_axis,
                uniform_enable, order
            )
        return (
            self._output_v_base_curve_percents,
            self._output_v_base_curve_points,
            self._output_v_base_curve_normals_x,
            self._output_v_base_curve_normals_y,
            self._output_v_base_curve_normals_z
        )


class OutputVExtraData(object):
    WSP = om.MSpace.kObject
    def __init__(self, om_create):
        self._om_create = om_create
    @classmethod
    def get_at(cls, om_fnc, index, percent, length, p_min, p_max, uniform_enable):
        if uniform_enable is True:
            length_ = MtdBasic._set_value_map_((0, 1), (0, length), percent)
            param = om_fnc.findParamFromLength(length_)
        else:
            param = MtdBasic._set_value_map_((0, 1), (p_min, p_max), percent)
        return om_fnc.getPointAtParam(param, cls.WSP)

    def get(self, count, uniform_enable):
        points = []
        om_fnc = om.MFnNurbsCurve(self._om_create)
        length = om_fnc.length()
        p_range = om_fnc.knotDomain
        p_min, p_max = p_range
        for i_index in range(count+1):
            i_percent = float(i_index)/count
            i_point = self.get_at(
                om_fnc, i_index, i_percent,
                length, p_min, p_max,
                uniform_enable
            )
            points.append(i_point)
        return points


class CurveToMeshExtraData(object):
    DIVISION_SCALE = 5
    def __init__(self, *args):
        (
            node,
            test_fnc,
            input_u_base_curve, input_v_base_curve,
            #
            base_attach_to_grow_mesh_enable,
            order, form,
            radius,
            u_sample, v_sample,
            u_base_degree, v_base_degree,
            u_degree, v_degree,
            #
            u_uniform_enable, v_uniform_enable,
            u_smoothing_enable, v_smoothing_enable,
            #
            v_translate_uniform_enable, v_rotate_uniform_enable, v_scale_uniform_enable,
            v_translate_extra_smooth, v_rotate_extra_smooth, v_scale_extra_smooth,
            u_auto_division_enable, v_auto_division_enable,
            u_division, v_division,
            #
            u_start_index, u_end_index,
            v_start_index, v_end_index,
            #
            spin, twist, taper,
            # output
            output_u_base_curve_create, output_u_base_surface_create, output_v_base_curve_create,
            output_v_translate_extra_curve_create, output_v_rotate_extra_curve_create, output_v_scale_extra_curve_create,
            #
            output_surface, output_mesh,
        ) = args
        #
        self._node_om_fnc = om.MFnDependencyNode(node)
        #
        self._base_attach_to_grow_mesh_enable = base_attach_to_grow_mesh_enable
        self._order = order
        self._form = form
        #
        self._radius = radius
        #
        self._u_uniform_enable, self._v_uniform_enable = u_uniform_enable, v_uniform_enable
        self._u_smoothing_enable, self._v_smoothing_enable = u_smoothing_enable, v_smoothing_enable
        #
        self._v_translate_uniform_enable, self._v_rotate_uniform_enable, self._v_scale_uniform_enable = (
            v_translate_uniform_enable, v_rotate_uniform_enable, v_scale_uniform_enable
        )
        self._v_translate_extra_degree, self._v_rotate_extra_degree, self._v_scale_extra_degree = (
            v_translate_extra_smooth, v_rotate_extra_smooth, v_scale_extra_smooth
        )
        #
        self._u_sample, self._v_sample = u_sample, v_sample
        self._u_base_degree, self._v_base_degree = u_base_degree, v_base_degree
        self._u_degree, self._v_degree = u_degree, v_degree
        #
        self._output_u_count, self._output_v_count = u_division, v_division
        # Clamp in 0.1
        self._u_start_index, self._u_end_index = u_start_index, u_end_index
        self._v_start_index, self._v_end_index = v_start_index, v_end_index
        #
        self._spin = spin
        self._twist = twist
        self._taper = taper
        #
        self._output_u_base_curve_om_create = output_u_base_curve_create
        self._output_u_base_surface_om_create = output_u_base_surface_create
        self._output_v_base_curve_om_create = output_v_base_curve_create
        self._output_v_translate_extra_curve_om_create = output_v_translate_extra_curve_create
        self._output_v_rotate_extra_curve_om_create = output_v_rotate_extra_curve_create
        self._output_v_scale_extra_curve_om_create = output_v_scale_extra_curve_create
        #
        self._output_surface_om_create = output_surface
        self._output_mesh_om_create = output_mesh
    # u data
    def update_input_u_base_data(self):
        self._input_u_base_points_map = InputUBaseCurvesData(
            self._node_om_fnc
        ).get(
            count=self._output_u_count,
            start_index=self._u_start_index,
            end_index=self._u_end_index,
            uniform_enable=self._u_uniform_enable
        )
        if self._input_u_base_points_map:
            return True
        return False

    def create_output_u_base_curve(self):
        # draw a close curve
        CurveCreate(
            self._output_u_base_curve_om_create
        ).update(
            degree=2, form=1,
            points=self._input_u_base_points_map[0]
        )
        if self._form == 1:
            # noinspection PyBroadException
            try:
                points = CurveCreateData._to_close_points_(
                    self._input_u_base_points_map[0]
                )
                # noinspection PyBroadException
                CurveCreate(
                    self._output_u_base_curve_om_create
                ).update(
                    degree=2, form=3,
                    points=points
                )
            except:
                om.MGlobal.displayWarning('build output u curve failed')
                pass

    def create_output_u_base_surface(self):
        u_degree, v_degree = self._v_degree, self._u_base_degree
        u_count, v_count, points = SurfaceCreateData(
            self._input_u_base_points_map
        ).get()
        SurfaceCreate(
            self._output_u_base_surface_om_create
        ).update(
            u_degree=u_degree, v_degree=v_degree,
            u_form=1, v_form=1,
            u_count=u_count, v_count=v_count, points=points,
        )
        if self._form == 1:
            u_count, v_count, points = SurfaceCreateData(
                self._input_u_base_points_map
            ).get_as_closed()
            #
            if v_degree > 1:
                points = SurfaceCreateData._to_v_close_points_(
                    u_count, v_count, points
                )
                v_count += 1
            # noinspection PyBroadException
            try:
                SurfaceCreate(
                    self._output_u_base_surface_om_create
                ).update_as_closed(
                    u_degree=u_degree, v_degree=v_degree,
                    u_form=1, v_form=3,
                    u_count=u_count, v_count=v_count, points=points,
                )
            except:
                om.MGlobal.displayWarning('build output u surface failed')
                pass

    def update_output_u_base_data(self):
        self._output_u_base_point_map = OutputUBaseData(
            self._output_u_base_surface_om_create
        ).get(
            self._output_u_count, self._output_v_count
        )

    def update_u_base(self):
        # step 1 gain data from "input-u-curves"
        if self.update_input_u_base_data() is False:
            return False
        # step 2 create "output-u-surface" by input data
        self.create_output_u_base_curve()
        self.create_output_u_base_surface()
        # step 3 gain data from "output-u-surface"
        self.update_output_u_base_data()
    # v data
    # v base data
    def update_input_v_base_data(self):
        self._input_v_base_points = InputVBaseCurveData(
            self._node_om_fnc
        ).get(
            count=self._output_v_count,
            start_index=self._v_start_index,
            end_index=self._v_end_index,
            uniform_enable=self._v_uniform_enable
        )

    def create_output_v_base_curve(self):
        CurveCreate(
            self._output_v_base_curve_om_create
        ).update(
            degree=2, form=1,
            points=self._input_v_base_points
        )

    def update_output_v_base_data(self):
        (
            self._output_v_base_curve_percents,
            self._output_v_base_curve_points,
            self._output_v_base_curve_normals_x,
            self._output_v_base_curve_normals_y,
            self._output_v_base_curve_normals_z
        ) = OutputVBaseData(
            self._output_v_base_curve_om_create
        ).get(
            count=self._output_v_count,
            order=self._order,
            axis=InputGrowMeshData(self._node_om_fnc).get_world_axis(),
            uniform_enable=self._v_uniform_enable
        )

    def update_v_base(self):
        self.update_input_v_base_data()
        self.create_output_v_base_curve()
        self.update_output_v_base_data()

    def update_input_v_extra_transformations(self):
        control_c = len(self._input_u_base_points_map)
        # print control_c, 'AA'
        c = (control_c-1)*2+1
        self._v_translate_extra_points = InputVExtraPointsData(
            self._node_om_fnc
        ).get(
            'vTranslateExtraPoints', c
        )
        #
        self._v_rotate_extra_points = InputVExtraPointsData(
            self._node_om_fnc
        ).get(
            'vRotateExtraPoints', c
        )
        #
        self._v_scale_extra_points = InputVExtraPointsData(
            self._node_om_fnc
        ).get(
            'vScaleExtraPoints', c
        )

    def create_output_v_extra_curves(self):
        CurveCreate(
            self._output_v_translate_extra_curve_om_create
        ).update(
            degree=self._v_translate_extra_degree, form=1,
            points=self._v_translate_extra_points
        )
        CurveCreate(
            self._output_v_rotate_extra_curve_om_create
        ).update(
            degree=self._v_rotate_extra_degree, form=1,
            points=self._v_rotate_extra_points
        )
        CurveCreate(
            self._output_v_scale_extra_curve_om_create
        ).update(
            degree=self._v_scale_extra_degree, form=1,
            points=self._v_scale_extra_points
        )
    # v extra data
    def update_output_v_extra_data(self):
        self.update_input_v_extra_transformations()
        self.create_output_v_extra_curves()
        #
        self._output_v_translate_points = OutputVExtraData(
            self._output_v_translate_extra_curve_om_create
        ).get(
            count=self._output_v_count,
            uniform_enable=self._v_translate_uniform_enable,
        )
        self._output_v_rotate_points = OutputVExtraData(
            self._output_v_rotate_extra_curve_om_create
        ).get(
            count=self._output_v_count,
            uniform_enable=self._v_rotate_uniform_enable,
        )
        self._output_v_scale_points = OutputVExtraData(
            self._output_v_scale_extra_curve_om_create
        ).get(
            count=self._output_v_count,
            uniform_enable=self._v_scale_uniform_enable,
        )

    def update_v_extra(self):
        self.update_output_v_extra_data()
    # output
    def update_output_data_map(self):
        u_c = self._output_u_count
        v_c = self._output_v_count

        u_radius = self._radius
        u_spin = self._spin
        u_twist = self._twist
        u_taper = self._taper

        u_point_center = om.MPoint(0, 0, 0)
        self._output_surface_points_map_0 = []
        for i_v in range(v_c+1):
            i_v_percent = self._output_v_base_curve_percents[i_v]
            i_v_point = self._output_v_base_curve_points[i_v]
            i_v_normal_x = self._output_v_base_curve_normals_x[i_v]
            i_v_normal_z = self._output_v_base_curve_normals_z[i_v]
            #
            i_v_points = self._output_u_base_point_map[i_v]
            i_u_points = []
            #
            i_v_translate_point = self._output_v_translate_points[i_v]
            i_v_rotate_point = self._output_v_rotate_points[i_v]
            i_v_scale_point = self._output_v_scale_points[i_v]
            #
            i_v_radius_scale_by_taper = 1+(u_taper-1)*i_v_percent
            i_v_radius_scale_by_extra = max(i_v_scale_point.y, 0)
            #
            i_v_radian_by_spin = math.radians(u_spin)
            i_v_radian_by_twist = math.radians(u_twist*i_v_percent)
            i_v_radian_by_extra = math.radians(i_v_rotate_point.y)
            for j_u in range(u_c+1):
                j_u_percent = float(j_u)/u_c
                #
                j_u_point_ = i_v_points[j_u]
                #
                j_u_radius_base = j_u_point_.distanceTo(u_point_center)
                j_u_radius = u_radius*j_u_radius_base*i_v_radius_scale_by_taper*i_v_radius_scale_by_extra
                j_u_vector_offset = i_v_normal_x*j_u_radius
                #
                j_u_radian_base = MtdBasic.get_radian_by_coord(
                    j_u_point_.x, j_u_point_.z, u_point_center.x, u_point_center.z
                )
                j_u_radian = j_u_radian_base+i_v_radian_by_spin+i_v_radian_by_twist+i_v_radian_by_extra
                #
                j_u_rotate_z = om.MQuaternion()
                j_u_rotate_z.setValue(
                    om.MVector(i_v_normal_z.x, i_v_normal_z.y, i_v_normal_z.z),
                    j_u_radian
                )
                j_u_vector_offset = j_u_vector_offset.rotateBy(j_u_rotate_z)

                j_u_point = om.MPoint()
                j_u_point.x, j_u_point.y, j_u_point.z = (
                    i_v_point.x+j_u_vector_offset.x,
                    i_v_point.y+j_u_vector_offset.y,
                    i_v_point.z+j_u_vector_offset.z
                )
                i_u_points.append(j_u_point)
            #
            self._output_surface_points_map_0.append(i_u_points)

    def create_output_surface(self):
        u_degree, v_degree = self._v_degree, self._u_base_degree
        u_count, v_count, points = SurfaceCreateData(
            self._output_surface_points_map_0
        ).get()
        SurfaceCreate(
            self._output_surface_om_create
        ).update(
            u_degree=u_degree, v_degree=v_degree,
            u_form=1, v_form=1,
            u_count=u_count, v_count=v_count, points=points,
        )

    def update_output(self):
        self.update_output_data_map()
        self.create_output_surface()
        self.create_output_mesh()

    def create_output_mesh(self):
        u_count, v_count, face_vertex_counts, face_vertex_indices, points = MeshCreateData(
            self._output_surface_points_map_0
        ).get(
            InputGrowMeshData(self._node_om_fnc).get_valid_om_fnc(),
            self._base_attach_to_grow_mesh_enable
        )
        #
        mesh_create = MeshCreate(
            self._output_mesh_om_create
        )
        mesh_create.update(
            face_vertex_counts, face_vertex_indices, points
        )
        if self._u_smoothing_enable is False:
            mesh_create.update_smoothing(
                MeshCreateData.get_u_edge_indices(u_count-1, v_count-1), False
            )
        if self._v_smoothing_enable is False or self._u_base_degree == 1:
            mesh_create.update_smoothing(
                MeshCreateData.get_v_edge_indices(u_count-1, v_count-1), False
            )

    def update(self):
        if self.update_u_base() is False:
            return False
        self.update_v_base()
        self.update_v_extra()
        #
        self.update_output()
    # methods
    @classmethod
    def _get_division_(cls, length, sample, percent, minimum, scale=1.0):
        _ = int(length*sample*percent*cls.DIVISION_SCALE*scale)
        return max(_, minimum)
    @classmethod
    def _get_range_(cls, start_index, end_index, minimum):
        start_index_ = max(min(start_index, start_index-minimum, 1.0-minimum), 0.0)
        end_index_ = max(end_index, min(start_index + minimum, 1.0), minimum)
        return start_index_, end_index_


class CurveToMeshExtraNode(
    omui.MPxLocatorNode,
    NodeBasic,
):
    NAME = 'curveToMeshExtra'
    ID = om.MTypeId(0x8701A)
    #
    DRAW_TYPE = 'drawdb/geometry/{}_draw'.format(NAME)
    DRAW_ID = '{}_draw'.format(NAME)
    #
    input_u_base_curves_atr = om.MObject()
    input_v_base_curve_atr = om.MObject()
    #
    input_grow_mesh_atr = om.MObject()
    #
    lynxi_type_atr = om.MObject()
    lynxi_scale_atr = om.MObject()
    lynxi_control_mode_atr = om.MObject()
    lynxi_control_direction_atr = om.MObject()
    #
    base_attach_to_grow_mesh_enable_atr = om.MObject()
    order_atr = om.MObject()
    form_atr = om.MObject()
    #
    radius_atr = om.MObject()
    #
    u_sample_atr = om.MObject()
    v_sample_atr = om.MObject()
    #
    u_degree_atr = om.MObject()
    v_degree_atr = om.MObject()
    #
    u_uniform_enable_atr = om.MObject()
    v_uniform_enable_atr = om.MObject()
    #
    u_smoothing_enable_atr = om.MObject()
    v_smoothing_enable_atr = om.MObject()
    #
    v_translate_uniform_enable_atr = om.MObject()
    v_rotate_uniform_enable_atr = om.MObject()
    v_scale_uniform_enable_atr = om.MObject()
    #
    v_translate_extra_points_atr = om.MObject()
    v_rotate_extra_points_atr = om.MObject()
    v_scale_extra_points_atr = om.MObject()
    #
    v_translate_extra_smooth_atr = om.MObject()
    v_rotate_extra_smooth_atr = om.MObject()
    v_scale_extra_smooth_atr = om.MObject()
    #
    v_extra_index_atr = om.MObject()
    #
    u_auto_division_enable_atr = om.MObject()
    v_auto_division_enable_atr = om.MObject()
    #
    u_start_index_atr = om.MObject()
    u_end_index_atr = om.MObject()
    v_start_index_atr = om.MObject()
    v_end_index_atr = om.MObject()
    #
    u_division_atr = om.MObject()
    v_division_atr = om.MObject()
    #
    spin_atr = om.MObject()
    twist_atr = om.MObject()
    taper_atr = om.MObject()
    #
    input_control_container_atr = om.MObject()
    #
    output_u_base_curve_atr = om.MObject()
    output_u_base_surface_atr = om.MObject()
    output_v_base_curve_atr = om.MObject()
    output_v_translate_extra_curve_atr = om.MObject()
    output_v_rotate_extra_curve_atr = om.MObject()
    output_v_scale_extra_curve_atr = om.MObject()
    #
    output_surface_atr = om.MObject()
    output_mesh_atr = om.MObject()
    #
    def __init__(self):
        super(CurveToMeshExtraNode, self).__init__()
    @classmethod
    def _initializer_fnc_(cls):
        cls.input_u_base_curves_atr = cls.add_geometry_atr(
            'inputUBaseCurves', 'iubcs',
            om.MFnData.kNurbsCurve,
            array=True
        )
        cls.input_v_base_curve_atr = cls.add_geometry_atr(
            'inputVBaseCurve', 'ivbc',
            om.MFnData.kNurbsCurve
        )
        cls.input_grow_mesh_atr = cls.add_geometry_atr(
            'inputGrowMesh', 'igm',
            om.MFnData.kMesh
        )
        # parameter
        cls.lynxi_type_atr = cls.add_string_atr(
            'lynxiType', 'lt',
            value=cls.NAME,
            writable=False
        )
        cls.lynxi_scale_atr = cls.add_float_atr(
            'lynxiScale', 'ls',
            value=1.0,
            minimum=0.01, maximum=100.0
        )
        cls.lynxi_control_mode_atr = cls.add_int_atr(
            'lynxiControlMode', 'lxcm',
            value=0,
            minimum=0, maximum=2
        )
        cls.lynxi_control_direction_atr = cls.add_int_atr(
            'lynxiControlDirection', 'lxcd',
            value=0,
            minimum=0, maximum=1
        )
        cls.base_attach_to_grow_mesh_enable_atr = cls.add_bool_atr(
            'baseAttachToGrowMeshEnable', 'batgme',
            value=1
        )
        cls.order_atr = cls.add_enumerate_atr(
            'order', 'o',
            values=['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']
        )
        cls.form_atr = cls.add_enumerate_atr(
            'form', 'f',
            values=['open', 'close'],
            # value=1
        )
        #
        cls.radius_atr = cls.add_float_atr(
            'radius', 'r',
            value=1,
            minimum=0
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
        cls.u_degree_atr = cls.add_int_atr(
            'uDegree', 'udg',
            value=2,
            minimum=1, maximum=2
        )
        cls.v_degree_atr = cls.add_int_atr(
            'vDegree', 'vdg',
            value=2,
            minimum=1, maximum=2
        )
        cls.u_uniform_enable_atr = cls.add_bool_atr(
            'uUniformEnable', 'uue',
            value=1
        )
        cls.v_uniform_enable_atr = cls.add_bool_atr(
            'vUniformEnable', 'vue',
            value=1
        )
        cls.u_smoothing_enable_atr = cls.add_bool_atr(
            'uSmoothingEnable', 'use',
            value=1
        )
        cls.v_smoothing_enable_atr = cls.add_bool_atr(
            'vSmoothingEnable', 'vse',
            value=1
        )
        #
        cls.v_extra_index_atr = cls.add_int_atr(
            'vExtraIndex', 'vei',
            value=0,
            minimum=0, maximum=19
        )
        cls.v_translate_uniform_enable_atr = cls.add_bool_atr(
            'vTranslateUniformEnable', 'vtue',
            value=0
        )
        cls.v_rotate_uniform_enable_atr = cls.add_bool_atr(
            'vRotateUniformEnable', 'vrue',
            value=0
        )
        cls.v_scale_uniform_enable_atr = cls.add_bool_atr(
            'vScaleUniformEnable', 'vsue',
            value=0
        )
        #
        cls.v_translate_extra_points_atr = cls.add_point_atr(
            'vTranslateExtraPoints', 'vteps',
            array=True, array_builder=True
        )
        cls.v_rotate_extra_points_atr = cls.add_point_atr(
            'vRotateExtraPoints', 'vreps',
            array=True, array_builder=True
        )
        cls.v_scale_extra_points_atr = cls.add_point_atr(
            'vScaleExtraPoints', 'vseps',
            array=True, array_builder=True
        )
        #
        cls.v_translate_extra_smooth_atr = cls.add_int_atr(
            'vTranslateExtraSmooth', 'vtes',
            value=2,
            minimum=1, maximum=4
        )
        cls.v_rotate_extra_smooth_atr = cls.add_int_atr(
            'vRotateExtraSmooth', 'vres',
            value=2,
            minimum=1, maximum=4
        )
        cls.v_scale_extra_smooth_atr = cls.add_int_atr(
            'vScaleExtraSmooth', 'vses',
            value=2,
            minimum=1, maximum=4
        )
        #
        cls.u_auto_division_enable_atr = cls.add_bool_atr(
            'uAutoDivisionEnable', 'uade',
            value=1
        )
        cls.v_auto_division_enable_atr = cls.add_bool_atr(
            'vAutoDivisionEnable', 'vade',
            value=1
        )
        #
        cls.u_start_index_atr = cls.add_float_atr(
            'uStartIndex', 'usidx',
            value=0,
            minimum=0, maximum=1
        )
        cls.u_end_index_atr = cls.add_float_atr(
            'uEndIndex', 'ueidx',
            value=1,
            minimum=0, maximum=1
        )
        cls.v_start_index_atr = cls.add_float_atr(
            'vStartIndex', 'vsidx',
            value=0,
            minimum=0, maximum=1
        )
        cls.v_end_index_atr = cls.add_float_atr(
            'vEndIndex', 'veidx',
            value=1,
            minimum=0, maximum=1
        )
        #
        cls.u_division_atr = cls.add_int_atr(
            'uDivision', 'ud',
            value=2,
            minimum=2
        )
        cls.v_division_atr = cls.add_int_atr(
            'vDivision', 'vd',
            value=32,
            minimum=2
        )
        #
        cls.spin_atr = cls.add_float_atr(
            'spin', 'spn',
            value=0
        )
        cls.twist_atr = cls.add_float_atr(
            'twist', 'tst',
            value=0
        )
        cls.taper_atr = cls.add_float_atr(
            'taper', 'tpr',
            value=1,
            minimum=0
        )
        cls.input_control_container_atr = cls.add_message_atr(
            'inputControlContainer', 'lxicc'
        )
        # output
        cls.output_u_base_curve_atr = cls.add_geometry_atr(
            'outputUBaseCurve', 'oubc',
            om.MFnData.kNurbsCurve
        )
        cls.output_u_base_surface_atr = cls.add_geometry_atr(
            'outputUBaseSurface', 'oubs',
            om.MFnData.kNurbsSurface
        )
        cls.output_v_base_curve_atr = cls.add_geometry_atr(
            'outputVBaseCurve', 'ovbc',
            om.MFnData.kNurbsCurve
        )
        cls.output_v_translate_extra_curve_atr = cls.add_geometry_atr(
            'outputVTranslateExtraCurve', 'ovte',
            om.MFnData.kNurbsCurve
        )
        cls.output_v_rotate_extra_curve_atr = cls.add_geometry_atr(
            'outputVRotateExtraCurve', 'ovre',
            om.MFnData.kNurbsCurve
        )
        cls.output_v_scale_extra_curve_atr = cls.add_geometry_atr(
            'outputVScaleExtraCurve', 'ovse',
            om.MFnData.kNurbsCurve
        )
        #
        cls.output_surface_atr = cls.add_geometry_atr(
            'outputSurface', 'optsrf',
            om.MFnData.kNurbsSurface
        )
        cls.output_mesh_atr = cls.add_geometry_atr(
            'outputMesh', 'optmsh',
            om.MFnData.kMesh
        )
        #
        ss = [
            cls.input_u_base_curves_atr, cls.input_v_base_curve_atr,
            cls.input_grow_mesh_atr,
            #
            cls.lynxi_type_atr, cls.lynxi_scale_atr,
            #
            cls.base_attach_to_grow_mesh_enable_atr,
            cls.order_atr, cls.form_atr,
            cls.radius_atr,
            cls.u_sample_atr, cls.v_sample_atr,
            cls.u_degree_atr, cls.v_degree_atr,
            #
            cls.u_uniform_enable_atr, cls.v_uniform_enable_atr,
            cls.u_smoothing_enable_atr, cls.v_smoothing_enable_atr,
            cls.v_translate_uniform_enable_atr, cls.v_rotate_uniform_enable_atr, cls.v_scale_uniform_enable_atr,
            cls.v_translate_extra_points_atr, cls.v_rotate_extra_points_atr, cls.v_scale_extra_points_atr,
            cls.v_translate_extra_smooth_atr, cls.v_rotate_extra_smooth_atr, cls.v_scale_extra_smooth_atr,
            cls.v_extra_index_atr,
            cls.u_auto_division_enable_atr, cls.v_auto_division_enable_atr,
            cls.u_division_atr, cls.v_division_atr,
            cls.u_start_index_atr, cls.u_end_index_atr,
            cls.v_start_index_atr, cls.v_end_index_atr,
            #
            cls.spin_atr, cls.twist_atr, cls.taper_atr,
        ]
        ts = [
            cls.output_u_base_curve_atr, cls.output_u_base_surface_atr, cls.output_v_base_curve_atr,
            cls.output_v_translate_extra_curve_atr, cls.output_v_rotate_extra_curve_atr, cls.output_v_scale_extra_curve_atr,
            #
            cls.output_surface_atr, cls.output_mesh_atr
        ]
        cls.set_atrs_connect(ss, ts)
    @staticmethod
    def _update_fnc_(*args):
        if not args[0].isNull():
            cmd = CurveToMeshExtraData(*args)
            cmd.update()
    @classmethod
    def _create_fnc_(cls):
        return cls()

    def _transformation_compute_fnc_(self, data_block):
        count = 20
        v_translate_extra = data_block.outputArrayValue(self.v_translate_extra_points_atr)
        v_translate_extra_builder = v_translate_extra.builder()
        o_c = len(v_translate_extra_builder)
        if o_c < count:
            builder = om.MArrayDataBuilder(v_translate_extra_builder)
            for vtx in range(count-o_c):
                child = builder.addLast()
                child.set3Float(0.0001, 0.0001, 0.0001)
            #
            v_translate_extra.set(builder)

        v_rotate_extra = data_block.outputArrayValue(self.v_rotate_extra_points_atr)
        v_rotate_extra_builder = v_rotate_extra.builder()
        o_c = len(v_rotate_extra_builder)
        if o_c < count:
            builder = om.MArrayDataBuilder(v_rotate_extra_builder)
            for vtx in range(count-o_c):
                child = builder.addLast()
                child.set3Float(0.0001, 0.0001, 0.0001)
            #
            v_rotate_extra.set(builder)

        v_scale_extra = data_block.outputArrayValue(self.v_scale_extra_points_atr)
        v_scale_extra_builder = v_scale_extra.builder()
        o_c = len(v_scale_extra_builder)
        if o_c < count:
            builder = om.MArrayDataBuilder(v_scale_extra_builder)
            for vtx in range(count-o_c):
                child = builder.addLast()
                child.set3Float(1, 1, 1)
            #
            v_scale_extra.set(builder)

    def compute(self, plug, data_block):
        if (
            plug in [
                # u and v node
                self.output_u_base_curve_atr, self.output_u_base_surface_atr, self.output_v_base_curve_atr,
                self.output_v_translate_extra_curve_atr, self.output_v_rotate_extra_curve_atr, self.output_v_scale_extra_curve_atr,
                #
                self.output_surface_atr, self.output_mesh_atr
            ]
        ):
            input_u_base_curves = data_block.inputArrayValue(self.input_u_base_curves_atr)
            #
            input_v_base_curve = data_block.inputValue(self.input_v_base_curve_atr)
            input_v_base_curve_value = input_v_base_curve.asNurbsCurve()
            if (
                input_u_base_curves.isDone() is False
                and input_v_base_curve_value.isNull() is False
            ):
                input_u_base_curve = input_u_base_curves.inputValue()
                input_u_base_curve_value = input_u_base_curve.asNurbsCurve()
                #
                self._transformation_compute_fnc_(data_block)
                #
                lynxi_scale = data_block.inputValue(self.lynxi_scale_atr)
                lynxi_scale_value = lynxi_scale.asFloat()
                # parameter
                base_attach_to_grow_mesh_enable = data_block.inputValue(self.base_attach_to_grow_mesh_enable_atr)
                base_attach_to_grow_mesh_enable_value = base_attach_to_grow_mesh_enable.asBool()
                #
                order = data_block.inputValue(self.order_atr)
                order_value = order.asShort()
                #
                form = data_block.inputValue(self.form_atr)
                form_value = form.asShort()
                #
                radius = data_block.inputValue(self.radius_atr)
                radius_value = radius.asFloat()
                #
                v_translate_extra_points = data_block.inputArrayValue(self.v_translate_extra_points_atr)
                v_rotate_extra_points = data_block.inputArrayValue(self.v_rotate_extra_points_atr)
                v_scale_extra_points = data_block.inputArrayValue(self.v_scale_extra_points_atr)
                v_scale = v_scale_extra_points.inputValue()
                v_scale_value = v_scale.asFloat3()
                u_scale_value = v_scale_value[1]
                #
                u_base_curve_om_fnc = om.MFnNurbsCurve(input_u_base_curve_value)
                u_base_length_value = u_base_curve_om_fnc.length()
                u_base_degree_value = u_base_curve_om_fnc.degree
                v_base_curve_om_fnc = om.MFnNurbsCurve(input_v_base_curve_value)
                v_base_length_value = v_base_curve_om_fnc.length()
                v_base_degree_value = v_base_curve_om_fnc.degree
                #
                u_sample = data_block.inputValue(self.u_sample_atr)
                u_sample_value = u_sample.asInt()
                v_sample = data_block.inputValue(self.v_sample_atr)
                v_sample_value = v_sample.asInt()
                #
                u_degree = data_block.inputValue(self.u_degree_atr)
                u_degree_value = u_degree.asInt()
                v_degree = data_block.inputValue(self.v_degree_atr)
                v_degree_value = v_degree.asInt()
                #
                u_uniform_enable = data_block.inputValue(self.u_uniform_enable_atr)
                u_uniform_enable_value = u_uniform_enable.asBool()
                v_uniform_enable = data_block.inputValue(self.v_uniform_enable_atr)
                v_uniform_enable_value = v_uniform_enable.asBool()
                #
                u_smoothing_enable = data_block.inputValue(self.u_smoothing_enable_atr)
                u_smoothing_enable_value = u_smoothing_enable.asBool()
                v_smoothing_enable = data_block.inputValue(self.v_smoothing_enable_atr)
                v_smoothing_enable_value = v_smoothing_enable.asBool()
                #
                v_translate_uniform_enable = data_block.inputValue(self.v_translate_uniform_enable_atr)
                v_translate_uniform_enable_value = v_translate_uniform_enable.asBool()
                v_rotate_uniform_enable = data_block.inputValue(self.v_rotate_uniform_enable_atr)
                v_rotate_uniform_enable_value = v_rotate_uniform_enable.asBool()
                v_scale_uniform_enable = data_block.inputValue(self.v_scale_uniform_enable_atr)
                v_scale_uniform_enable_value = v_scale_uniform_enable.asBool()
                #
                v_translate_extra_smooth = data_block.inputValue(self.v_translate_extra_smooth_atr)
                v_translate_extra_smooth_value = v_translate_extra_smooth.asInt()
                v_rotate_extra_smooth = data_block.inputValue(self.v_rotate_extra_smooth_atr)
                v_rotate_extra_smooth_value = v_rotate_extra_smooth.asInt()
                v_scale_extra_smooth = data_block.inputValue(self.v_scale_extra_smooth_atr)
                v_scale_extra_smooth_value = v_scale_extra_smooth.asInt()
                #
                u_auto_division_enable = data_block.inputValue(self.u_auto_division_enable_atr)
                u_auto_division_enable_value = u_auto_division_enable.asBool()
                v_auto_division_enable = data_block.inputValue(self.v_auto_division_enable_atr)
                v_auto_division_enable_value = v_auto_division_enable.asBool()
                #
                u_start_index = data_block.inputValue(self.u_start_index_atr)
                u_start_index_value = u_start_index.asFloat()
                u_end_index = data_block.inputValue(self.u_end_index_atr)
                u_end_index_value = u_end_index.asFloat()
                u_start_index_value_, u_end_index_value_ = CurveToMeshExtraData._get_range_(
                    start_index=u_start_index_value,
                    end_index=u_end_index_value,
                    minimum=.01
                )
                #
                v_start_index = data_block.inputValue(self.v_start_index_atr)
                v_start_index_value = v_start_index.asFloat()
                v_end_index = data_block.inputValue(self.v_end_index_atr)
                v_end_index_value = v_end_index.asFloat()
                v_start_index_value_, v_end_index_value_ = CurveToMeshExtraData._get_range_(
                    start_index=v_start_index_value,
                    end_index=v_end_index_value,
                    minimum=.01
                )
                #
                v_division = data_block.inputValue(self.v_division_atr)
                u_division = data_block.inputValue(self.u_division_atr)
                if u_auto_division_enable_value is True:
                    u_percent = (u_end_index_value_-u_start_index_value_)/1.0
                    u_division.setInt(
                        CurveToMeshExtraData._get_division_(
                            length=u_base_length_value,
                            sample=u_sample_value,
                            percent=u_percent,
                            minimum=3,
                            scale=lynxi_scale_value*radius_value*u_scale_value
                        )
                    )
                if v_auto_division_enable_value is True:
                    v_percent = (v_end_index_value_-v_start_index_value_)/1.0
                    v_division.setInt(
                        CurveToMeshExtraData._get_division_(
                            length=v_base_length_value,
                            sample=v_sample_value,
                            percent=v_percent,
                            minimum=3,
                            scale=lynxi_scale_value
                        )
                    )
                #
                u_division_value = u_division.asInt()
                v_division_value = v_division.asInt()
                #
                spin = data_block.inputValue(self.spin_atr)
                spin_value = spin.asFloat()
                twist = data_block.inputValue(self.twist_atr)
                twist_value = twist.asFloat()
                taper = data_block.inputValue(self.taper_atr)
                taper_value = taper.asFloat()
                # output
                output_u_base_curve = data_block.outputValue(self.output_u_base_curve_atr)
                output_u_base_curve_value = om.MFnNurbsCurveData()
                output_u_base_curve_create = output_u_base_curve_value.create()

                output_u_base_surface = data_block.outputValue(self.output_u_base_surface_atr)
                output_u_base_surface_value = om.MFnNurbsSurfaceData()
                output_u_base_surface_create = output_u_base_surface_value.create()
                #
                output_v_base_curve = data_block.outputValue(self.output_v_base_curve_atr)
                output_v_base_curve_value = om.MFnNurbsCurveData()
                output_v_base_curve_create = output_v_base_curve_value.create()
                #
                output_v_translate_extra_curve = data_block.outputValue(self.output_v_translate_extra_curve_atr)
                output_v_translate_extra_curve_value = om.MFnNurbsCurveData()
                output_v_translate_extra_curve_create = output_v_translate_extra_curve_value.create()
                output_v_rotate_extra_curve = data_block.outputValue(self.output_v_rotate_extra_curve_atr)
                output_v_rotate_extra_curve_value = om.MFnNurbsCurveData()
                output_v_rotate_extra_curve_create = output_v_rotate_extra_curve_value.create()
                output_v_scale_extra_curve = data_block.outputValue(self.output_v_scale_extra_curve_atr)
                output_v_scale_extra_curve_value = om.MFnNurbsCurveData()
                output_v_scale_extra_curve_create = output_v_scale_extra_curve_value.create()
                #
                output_surface = data_block.outputValue(self.output_surface_atr)
                output_surface_value = om.MFnNurbsSurfaceData()
                output_surface_create = output_surface_value.create()
                #
                output_mesh = data_block.outputValue(self.output_mesh_atr)
                output_mesh_value = om.MFnMeshData()
                output_mesh_create = output_mesh_value.create()
                #
                self._update_fnc_(
                    self.thisMObject(),
                    #
                    None,
                    # input
                    input_u_base_curve_value, input_v_base_curve_value,
                    # parameter
                    base_attach_to_grow_mesh_enable_value,
                    order_value, form_value,
                    radius_value,
                    u_sample_value, v_sample_value,
                    u_base_degree_value, v_base_degree_value,
                    u_degree_value, v_degree_value,
                    #
                    u_uniform_enable_value, v_uniform_enable_value,
                    u_smoothing_enable_value, v_smoothing_enable_value,
                    v_translate_uniform_enable_value, v_rotate_uniform_enable_value, v_scale_uniform_enable_value,
                    v_translate_extra_smooth_value, v_rotate_extra_smooth_value, v_scale_extra_smooth_value,
                    # v_rotate_extra,
                    u_auto_division_enable_value, v_auto_division_enable_value,
                    u_division_value, v_division_value,
                    #
                    u_start_index_value_, u_end_index_value_,
                    v_start_index_value_, v_end_index_value_,
                    #
                    spin_value, twist_value, taper_value,
                    # output
                    output_u_base_curve_create, output_u_base_surface_create, output_v_base_curve_create,
                    output_v_translate_extra_curve_create, output_v_rotate_extra_curve_create, output_v_scale_extra_curve_create,
                    output_surface_create, output_mesh_create,
                )
                # update to output
                output_u_base_curve.setMObject(output_u_base_curve_create)
                output_u_base_surface.setMObject(output_u_base_surface_create)
                output_v_base_curve.setMObject(output_v_base_curve_create)
                output_v_translate_extra_curve.setMObject(output_v_translate_extra_curve_create)
                output_v_rotate_extra_curve.setMObject(output_v_rotate_extra_curve_create)
                output_v_scale_extra_curve.setMObject(output_v_scale_extra_curve_create)
                #
                output_surface.setMObject(output_surface_create)
                output_mesh.setMObject(output_mesh_create)
                #
                data_block.setClean(plug)
        else:
            return None

    def isBounded(self):
        return True

    def boundingBox(self):
        corner1 = om.MPoint(-10, -10, -10)
        corner2 = om.MPoint(10, 10, 10)

        bbox = om.MBoundingBox(corner1, corner2)
        return bbox


class AbsDrawData(object):
    def __init__(self):
        self._status = omrd.MGeometryUtilities.kNoStatus
        self._draw_data = []
        self._point_size = 1.0

    def draw(self, draw_manager):
        for i in self._draw_data:
            for j_fnc_name, j_args in i.items():
                draw_manager.__getattribute__(j_fnc_name)(*j_args)


class UCurvesDrawData(AbsDrawData):
    def __init__(self, surface, curve):
        super(UCurvesDrawData, self).__init__()
        self._surface = surface
        self._curve = curve

        self._status = omrd.MGeometryUtilities.kNoStatus
        #
        self._u_count = 0
        self._v_count = 0
        #
        self._draw_data = []
        self._point_size = 1.0

    def set_node(self, surface, curve):
        self._surface = surface
        self._curve = curve

    def set_status(self, status):
        self._status = status

    def update_v_count(self, node):
        om_fnc = om.MFnNurbsSurface(node)
        self._v_maximum = om_fnc.numCVsInU-3
        self._v_count = (self._v_maximum*2)+1
        self._u_count = 2

    def update(self):
        self._draw_data = []
        if self._surface is not None:
            surface_om_fnc = om.MFnNurbsSurface(self._surface)
            v_c = self._v_count
            # u and v is inverted
            u_p_range = surface_om_fnc.knotDomainInV
            u_p_min, u_p_max = u_p_range
            v_p_range = surface_om_fnc.knotDomainInU
            v_p_min, v_p_max = v_p_range
            #
            curve_om_fnc = om.MFnNurbsCurve(self._curve)
            v_curve_p_range = curve_om_fnc.knotDomain
            v_curve_p_min, v_curve_p_max = v_curve_p_range
            for i_v in range(v_c):
                i_points = om.MPointArray()
                i_colors = om.MColorArray()
                i_v_percent = float(i_v)/(v_c-1)
                i_v_surface_p = MtdBasic._set_value_map_((0, 1), (v_p_min, v_p_max), i_v_percent)
                i_v_center_p = MtdBasic._set_value_map_((0, 1), (v_curve_p_min, v_curve_p_max), i_v_percent)
                i_v_start_p = MtdBasic._set_value_map_((0, 1), (v_p_min, v_p_max), 0)
                i_start_point = surface_om_fnc.getPointAtParam(i_v_surface_p, i_v_start_p, om.MSpace.kWorld)
                i_v_end_p = MtdBasic._set_value_map_((0, 1), (v_p_min, v_p_max), .5)
                i_end_point = surface_om_fnc.getPointAtParam(i_v_surface_p, i_v_end_p, om.MSpace.kWorld)
                #
                i_center_point = curve_om_fnc.getPointAtParam(i_v_center_p, om.MSpace.kWorld)
                i_points += [i_start_point, i_center_point, i_end_point]
                if self._status == omrd.MGeometryUtilities.kLead:
                    i_color = om.MColor((.25, 1, .5, 1))
                elif self._status == omrd.MGeometryUtilities.kActiveTemplate:
                    i_color = om.MColor((.25, .25, .25, 1))
                else:
                    i_color = om.MColor((1 - i_v_percent, .5, i_v_percent, 1))
                i_colors += [i_color, i_color, i_color]
                #
                if i_v % 2:
                    self._draw_data.extend(
                        [
                            {
                                'point': (i_center_point,)
                            },
                        ]
                    )
                else:
                    self._draw_data.extend(
                        [
                            {
                                'point': (i_center_point,)
                            },
                            {
                                'mesh': (omrd.MUIDrawManager.kLineStrip, i_points, None, i_colors)
                            },
                        ]
                    )
            self._point_size = 10.0


class VCurveDrawData(AbsDrawData):
    def __init__(self, curve):
        super(VCurveDrawData, self).__init__()
        self._curve = curve

        self._status = omrd.MGeometryUtilities.kNoStatus

        self._draw_data = []
        self._point_size = 1.0

    def set_node(self, curve):
        self._curve = curve

    def set_status(self, status):
        self._status = status

    def update(self):
        self._draw_data = []
        if self._curve is not None:
            curve_om_fnc = om.MFnNurbsCurve(self._curve)
            points = curve_om_fnc.cvPositions()
            colors = om.MColorArray()
            c = len(points)
            if c > 0:
                # selected
                for i_index in range(c):
                    i_percent = float(i_index)/c
                    if self._status == omrd.MGeometryUtilities.kLead:
                        i_color = om.MColor((.25, 1, .5, 1))
                    elif self._status == omrd.MGeometryUtilities.kActiveTemplate:
                        i_color = om.MColor((.25, .25, .25, 1))
                    else:
                        i_color = om.MColor((1-i_percent, .5, i_percent, 1))
                    colors.append(i_color)
                #
                self._draw_data.append(
                    {
                        'mesh': (omrd.MUIDrawManager.kLineStrip, points, None, colors)
                    }
                )
            self._point_size = 10.0


class CurveToMeshExtraDrawData(om.MUserData):
    def __init__(self):
        super(CurveToMeshExtraDrawData, self).__init__(False)
        #
        self._u_curves_draw_data = UCurvesDrawData(None, None)
        self._v_curve_draw_data = VCurveDrawData(None)

    def update(self, node_path):
        node = node_path.node()
        om_fnc = om.MFnDependencyNode(node)
        #
        status = omrd.MGeometryUtilities.displayStatus(node_path)
        #
        output_u_base_surface_p = om_fnc.findPlug('outputUBaseSurface', False)
        output_v_base_curve_p = om_fnc.findPlug('outputVBaseCurve', False)
        output_surface_p = om_fnc.findPlug('outputSurface', False)
        u_division_p, v_division_p = om_fnc.findPlug('uDivision', False), om_fnc.findPlug('vDivision', False)
        # noinspection PyBroadException
        try:
            output_u_base_surface = output_u_base_surface_p.asMObject()
            output_v_base_curve = output_v_base_curve_p.asMObject()
            output_surface = output_surface_p.asMObject()
            self._u_curves_draw_data.set_node(output_surface, output_v_base_curve)
            self._u_curves_draw_data.update_v_count(output_u_base_surface)
            self._u_curves_draw_data.set_status(status)
            self._u_curves_draw_data.update()
            #
            self._v_curve_draw_data.set_node(output_v_base_curve)
            self._v_curve_draw_data.set_status(status)
            self._v_curve_draw_data.update()
            #
        except:
            self._u_curves_draw_data.set_node(None, None)
            self._u_curves_draw_data.update()
            #
            self._v_curve_draw_data.set_node(None)
            self._v_curve_draw_data.update()
            om.MGlobal.displayWarning('failed to read data')


class CurveToMeshExtraDrawOverride(
    omrd.MPxDrawOverride
):
    """
    displayStatus
    ####################################################################################################################
    0 kActive               Object is active (selected).
    1 kLive                 Object is live (construction surface).
    2 kDormant              Object is dormant.
    3 kInvisible            Object is invisible (not drawn).
    4 kHilite               Object is hilited (has selectable components).
    5 kTemplate             Object is templated (Not renderable).
    6 kActiveTemplate       Object is active and templated.
    7 kActiveComponent      Object has active components.
    8 kLead                 Last selected object.
    9 kIntermediateObject   Construction object (not drawn).
    10 kActiveAffected       Affected by active object(s).
    11 kNoStatus             Object does not have a valid display status.
    """
    def __init__(self, node):
        super(CurveToMeshExtraDrawOverride, self).__init__(node, None, False)
    @classmethod
    def _create_fnc_(cls, node):
        return cls(node)

    def isBounded(self, node_path, camera_path):
        return True

    def supportedDrawAPIs(self):
        return omrd.MRenderer.kOpenGL | omrd.MRenderer.kDirectX11 | omrd.MRenderer.kOpenGLCoreProfile

    def hasUIDrawables(self):
        return True

    def prepareForDraw(self, node_path, camera_path, frame_context, old_data):
        data = old_data
        if not isinstance(old_data, CurveToMeshExtraDrawData):
            data = CurveToMeshExtraDrawData()
        #
        data.update(node_path)
        return data

    def addUIDrawables(self, node_path, draw_manager, frame_context, data):
        old_data = data
        if not isinstance(old_data, CurveToMeshExtraDrawData):
            return
        # start draw
        draw_manager.beginDrawable()
        # draw u curve
        draw_manager.setLineWidth(4)
        draw_manager.setPointSize(data._u_curves_draw_data._point_size)
        draw_manager.setLineStyle(omrd.MUIDrawManager.kSolid)
        data._u_curves_draw_data.draw(draw_manager)
        # draw v curve
        draw_manager.setPointSize(data._v_curve_draw_data._point_size)
        draw_manager.setLineStyle(omrd.MUIDrawManager.kSolid)
        data._v_curve_draw_data.draw(draw_manager)
        #
        draw_manager.endDrawable()


class ControlPlane(object):
    def __init__(self):
        self._n_x = 0.0
        self._n_y = 0.0
        self._n_z = 0.0
        self._w = 0.0

    def update(self, point, normal):
        n = om.MVector(normal)
        n.normalize()
        #
        self._n_x = n.x
        self._n_y = n.y
        self._n_z = n.z
        self._w = -(self._n_x*point.x+self._n_y*point.y+self._n_z*point.z)

    def get_intersect_args(self, ray):
        point = om.MPoint()
        p, n = ray
        #
        denominator = self._n_x*n.x+self._n_y*n.y+self._n_z*n.z
        if denominator < .00001:
            return False, point
        #
        t = -(self._w+self._n_x*p.x+self._n_y*p.y+self._n_z*p.z)/denominator
        return True, p+t*n


class LineMath(object):
    """
    This utility class represents a mathematical line and returns the closest point
    on the line to a given point.
    """

    def __init__(self):
        """
        Initialze the member variables of the class.
        """
        self.point = om.MPoint()
        self.direction = om.MVector()

    def set_line(self, line_point, line_direction):
        """
        Define the line by supplying a point on the line and the line's direction.
        """
        self.point = om.MPoint(line_point)
        self.direction = om.MVector(line_direction)
        self.direction.normalize()

    def closest_point(self, to_point):
        t = self.direction * (to_point - self.point)
        return self.point + (self.direction * t)


class AbsHandle(object):
    HANDLE_SPAN = 10
    HANDLE_SIZE = .2
    HANDLE_LINE_SIZE = 5
    HANDLE_ROTATE_MULTIPLY = 1000
    HANDLE_SCALE_MULTIPLY = 100
    def __init__(self, handle_index):
        self._handle_index = handle_index
        self._data_index = 0
        #
        self._point_size = 1.0
        self._color = om.MColor((1, 1, 1, 1))
        self._line_width = 1.0
        self._line_style = omrd.MUIDrawManager.kSolid
        self._draw_data = {}
        self._press_draw_data = {}
        #
        self._center_point = om.MPoint(0, 0, 0)
        self._center_normal_z = om.MVector(0, 0, 0)
        #
        self._control_point = om.MPoint(0, 0, 0)
        self._control_point_start = om.MPoint(0, 0, 0)
        self._control_normal = om.MVector(0, 0, 0)
        #
        self._information_point = om.MPoint(0, 0, 0)
        self._atr = None
        self._atr_key = ''
        self._atr_value = None
        self._atr_value_index = 0
        self._atr_value_offset_multiply = 1.0
        self._atr_value_start = 0
        self._atr_value_offset = 0
        self._atr_control_point_index = 0

        self._point_start = om.MPoint(0, 0, 0)
        self._point_cur = om.MPoint(0, 0, 0)
        #
        self._press_point = om.MPoint(0, 0, 0)

        self._press_normal_to_plane = om.MVector(0, 0, 0)
        self._press_point_to_plane = om.MPoint(0, 0, 0)

        self._press_frame_points = om.MPointArray(
            [om.MPoint(1, 1, 0), om.MPoint(0, 0, 0), om.MPoint(0, 0, 0), om.MPoint(0, 0, 0)]
        )

    def draw(self, draw_manager):
        for k_fnc_name, k_args in self._draw_data.items():
            draw_manager.__getattribute__(k_fnc_name)(*k_args)

    def draw_information(self, draw_manager):
        draw_manager.setColor(om.MColor((0, 0, 0, 1)))
        draw_manager.text(
            self._information_point, '    {}[{}] = {} {} {}'.format(
                self._atr_key,
                self._data_index,
                self._atr_value_start,
                ['+', '-'][self._atr_value_offset < 0],
                abs(self._atr_value_offset)
            )
        )

    def draw_state_line(self, draw_manager):
        draw_manager.setLineWidth(2)
        draw_manager.setLineStyle(omrd.MUIDrawManager.kDashed)
        draw_manager.setColor(om.MColor((.25, .25, .25, 1)))
        # draw_manager.line(self._control_point, self._press_point)
        # press normal
        p = self._center_point
        draw_manager.line(
            p,
            om.MPoint(p.x+self._press_normal_to_plane.x, p.y+self._press_normal_to_plane.y, p.z+self._press_normal_to_plane.z)
        )
        draw_manager.line(self._control_point, self._press_point_to_plane)
        draw_manager.mesh(
            omrd.MUIDrawManager.kClosedLine, self._press_frame_points
        )

    def set_data(self, key, value):
        pass

    def update_control_point(self, point):
        pass

    def update_by_press(self, ray, control_plane, manipulator):
        normal = ray[1]
        normal.normalize()
        x, y, z = normal.z, normal.y, normal.z
        #
        if z > 0:
            press_normal = om.MVector(0, 0, 1)
        else:
            press_normal = om.MVector(0, 0, -1)
        #
        (
            self._control_point_start.x,
            self._control_point_start.y,
            self._control_point_start.z
        ) = (
            self._control_point.x,
            self._control_point.y,
            self._control_point.z,
        )
        #
        press_normal.normalize()
        (
            self._press_point_to_plane.x,
            self._press_point_to_plane.y,
            self._press_point_to_plane.z
        ) = (
            self._control_point.x,
            self._control_point.y,
            self._control_point.z,
        )
        (
            self._press_normal_to_plane.x,
            self._press_normal_to_plane.y,
            self._press_normal_to_plane.z
        ) = (
            press_normal.x,
            0,
            press_normal.z
        )
        control_plane.update(
            self._press_point_to_plane, self._press_normal_to_plane
        )

        value_index = manipulator._get_value_index_(self._handle_index)
        if value_index is not None:
            self._atr_value_start = manipulator.getDoubleValue(value_index, False)

    def update_by_release(self):
        (
            self._control_point.x,
            self._control_point.y,
            self._control_point.z
        ) = (
            self._control_point_start.x,
            self._control_point_start.y,
            self._control_point_start.z,
        )

    def update_by_drag(self, ray, control_plane, manipulator):
        enable, point = control_plane.get_intersect_args(ray)
        (
            self._press_point.x, self._press_point.y, self._press_point.z
        ) = (
            point.x, point.y, point.z
        )
        self._control_point[self._atr_control_point_index] = point[self._atr_control_point_index]
        #

        value_index = manipulator._get_value_index_(self._handle_index)
        if value_index is not None:
            v_s = self._control_point_start[self._atr_control_point_index]
            v = self._control_point[self._atr_control_point_index]
            self._atr_value_offset = (v - v_s)*self._atr_value_offset_multiply
            self._atr_value = self._atr_value_start + self._atr_value_offset
            manipulator.setDoubleValue(value_index, self._atr_value)
    @classmethod
    def _get_handle_group_index_(cls, data_index):
        return cls.HANDLE_SPAN*data_index
    @classmethod
    def _get_handle_group_args_(cls, data_index):
        handle_index = cls._get_handle_group_index_(data_index)
        index_minimum = handle_index
        index_maximum = cls.HANDLE_SPAN*(data_index+1)
        return handle_index, index_minimum, index_maximum
    @classmethod
    def _get_handle_index_(cls, data_index, index):
        return data_index*cls.HANDLE_SPAN+index


class ControlPoints(om.MPointArray):
    def __init__(self):
        pass


class HandleRoot(AbsHandle):
    WSP = om.MSpace.kWorld
    def __init__(self, u_base_surface_node, v_base_curve_node, surface_node):
        super(HandleRoot, self).__init__(0)
        #
        self._lynxi_scale = 1.0
        #
        self._u_base_surface_node = u_base_surface_node
        self._v_base_curve_node = v_base_curve_node
        self._surface_node = surface_node
        #
        self._handle_groups = []
        #
        self._handle_group_query = {}
        self._handle_query = {}

    def set_lynxi_scale(self, value):
        self._lynxi_scale = value

    def setup(self):
        if (
            self._u_base_surface_node is not None
            and self._v_base_curve_node is not None
            and self._surface_node is not None
        ):
            u_base_surface_om_fnc = om.MFnNurbsSurface(self._u_base_surface_node)
            v_base_curve_om_fnc = om.MFnNurbsCurve(self._v_base_curve_node)
            v_curve_p_range = v_base_curve_om_fnc.knotDomain
            v_curve_p_min, v_curve_p_max = v_curve_p_range
            self._v_index_maximum = u_base_surface_om_fnc.numCVsInU-3
            surface_om_fnc = om.MFnNurbsSurface(self._surface_node)
            v_c = (self._v_index_maximum*2)+1
            points = om.MPointArray()
            normals_x = om.MVectorArray()
            normals_z = om.MVectorArray()
            #
            rotate_multiply = self.HANDLE_ROTATE_MULTIPLY*self._lynxi_scale
            scale_multiply = self.HANDLE_SCALE_MULTIPLY*self._lynxi_scale
            p_pre = 0
            i_handle_length = 1.0
            for i_v in range(v_c):
                i_v_percent = float(i_v) / (v_c-1)
                #
                i_v_p = MtdBasic._set_value_map_((0, 1), (v_curve_p_min, v_curve_p_max), i_v_percent)
                i_center_point = v_base_curve_om_fnc.getPointAtParam(i_v_p, om.MSpace.kWorld)
                i_normal_x = om.MVector(1, 0, 0)
                i_normal_y = om.MVector(0, 1, 0)
                i_normal_z = om.MVector(0, 0, 1)
                i_first_point = surface_om_fnc.getPointAtParam(i_v_percent, 0, 4)
                if i_v == 0:
                    i_handle_length = i_center_point.distanceTo(i_first_point)*1.25
                    i_handle_length = max(i_handle_length, 1)
                #
                if i_v > 0:
                    i_point_sub = v_base_curve_om_fnc.getPointAtParam(p_pre+(i_v_p-p_pre)/2, om.MSpace.kWorld)
                    points.append(i_point_sub)
                #
                p_pre = i_v_p
                #
                points.append(i_center_point)
                #
                normals_x.append(i_normal_x)
                normals_z.append(i_normal_z)
                #
                i_normal_x.normalize()
                i_normal_z.normalize()
                #
                i_control_normal_x_0 = i_normal_x*-i_handle_length
                i_control_point_x_0 = om.MPoint(
                    (i_center_point.x+i_control_normal_x_0.x), (i_center_point.y+i_control_normal_x_0.y), (i_center_point.z+i_control_normal_x_0.z)
                )
                i_control_normal_y_0 = i_normal_y*-i_handle_length
                i_control_point_y_0 = om.MPoint(
                    (i_center_point.x+i_control_normal_y_0.x), (i_center_point.y+i_control_normal_y_0.y), (i_center_point.z+i_control_normal_y_0.z)
                )
                #
                i_control_normal_x_1 = i_normal_x*i_handle_length
                i_control_point_x_1 = om.MPoint(
                    (i_center_point.x+i_control_normal_x_1.x), (i_center_point.y+i_control_normal_x_1.y), (i_center_point.z+i_control_normal_x_1.z)
                )
                i_control_normal_y_1 = i_normal_y*i_handle_length
                i_control_point_y_1 = om.MPoint(
                    (i_center_point.x+i_control_normal_y_1.x), (i_center_point.y+i_control_normal_y_1.y), (i_center_point.z+i_control_normal_y_1.z)
                )
                i_data_index = i_v
                #
                i_handle_group = self.create_handle_group(i_data_index)
                if i_v % 2:
                    i_handle_group._color = om.MColor((0, 1, .125, 1))
                    i_handle_group._point_size = 10.0
                else:
                    i_handle_group._color = om.MColor((.125, 1, 0, 1))
                    i_handle_group._point_size = 12.0
                i_handle_group._draw_data = {
                    'point': (i_center_point, ),
                }
                frame_points = om.MPointArray()
                frame_points += [
                    i_control_point_x_0,
                    i_control_point_y_0,
                    i_control_point_x_1,
                    i_control_point_y_1,
                ]
                # rotate
                i_sub_handle_0 = i_handle_group.create_handle(1)
                i_sub_handle_0._color = om.MColor((1, 0, .125, 1))
                i_sub_handle_0._point_size = 14.0
                i_sub_handle_0._draw_data = {
                    'line': (i_center_point, i_control_point_x_0),
                    # 'sphere': (i_control_point_x_0, handle_size, True),
                    'point': (i_control_point_x_0, ),
                }
                i_sub_handle_0._center_point = i_center_point
                i_sub_handle_0._control_point = i_control_point_x_0
                i_sub_handle_0._control_normal = i_normal_x
                i_sub_handle_0._information_point = i_center_point
                i_sub_handle_0._atr_key = 'rotate'
                i_sub_handle_0._press_frame_points = frame_points
                i_sub_handle_0._data_index = i_data_index
                i_sub_handle_0._atr_value_offset_multiply = rotate_multiply
                i_sub_handle_0._atr_control_point_index = 0
                #
                i_sub_handle_1 = i_handle_group.create_handle(2)
                i_sub_handle_1._point_size = 14.0
                i_sub_handle_1._color = om.MColor((.125, 0, 1, 1))
                i_sub_handle_1._draw_data = {
                    'line': (i_center_point, i_control_point_y_1),
                    'point': (i_control_point_y_1,),
                }
                i_sub_handle_1._center_point = i_center_point
                i_sub_handle_1._control_point = i_control_point_y_1
                i_sub_handle_1._control_normal = i_normal_x
                i_sub_handle_1._information_point = i_center_point
                i_sub_handle_1._atr_key = 'scale'
                i_sub_handle_1._press_frame_points = frame_points
                i_sub_handle_1._data_index = i_data_index
                i_sub_handle_1._atr_value_offset_multiply = scale_multiply
                i_sub_handle_1._atr_control_point_index = 1
            #
            self._color = om.MColor((0, 0, 0, 1))
            self._line_style = omrd.MUIDrawManager.kDashed
            self._draw_data = {
                'lineStrip': (points, False)
            }

    def create_handle_group(self, data_index):
        handle_index, index_minimum, index_maximum = self._get_handle_group_args_(data_index)
        handle_group = HandleGroup(self, handle_index, index_minimum, index_maximum)
        handle_group._data_index = data_index
        self._handle_groups.append(handle_group)
        self.register_handle_group(handle_group)
        return handle_group

    def register_handle_group(self, handle_group):
        self._handle_group_query[handle_group._handle_group_index] = handle_group

    def has_handle_group(self, data_index):
        return data_index in self._handle_group_query

    def get_handle_group(self, data_index):
        return self._handle_group_query[data_index]

    def register_handle(self, handle):
        self._handle_query[handle._handle_index] = handle

    def has_handle(self, handle_index):
        return handle_index in self._handle_query

    def get_handle(self, handle_index):
        return self._handle_query[handle_index]


class HandleGroup(AbsHandle):
    def __init__(self, handle_root, data_index, handle_group_index_minimum, handle_group_index_maximum):
        super(HandleGroup, self).__init__(data_index)
        self._handle_root = handle_root
        #
        self._handle_group_index = data_index
        self._handle_group_index_minimum = handle_group_index_minimum
        self._handle_group_index_maximum = handle_group_index_maximum
        #
        self._handles = []

    def create_handle(self, index):
        handle_index = self._get_handle_index_(self._data_index, index)
        handle = Handle(self, handle_index)
        self._handles.append(handle)
        self._handle_root.register_handle(handle)
        return handle

    def is_contain_handle(self, handle_index):
        return self._handle_group_index_minimum <= handle_index < self._handle_group_index_maximum


class Handle(AbsHandle):
    def __init__(self, handle_root, handle_index):
        super(Handle, self).__init__(handle_index)
        self._handle_root = handle_root


class CurveToMeshExtraManipulatorNode(
    omui.MPxManipulatorNode,
    NodeBasic,
):
    NAME = 'curveToMeshExtraManipulator'
    ID = om.MTypeId(0x8701B)
    PRE_ID = None
    def __init__(self):
        super(CurveToMeshExtraManipulatorNode, self).__init__()
        #
        self._control_index = -1
        #
        self._control_plane = ControlPlane()
        self._control_plane.update(om.MPoint(0, 1, 0), om.MVector(0, 0, 1))

        self._handle_root = HandleRoot(None, None, None)

        self._value_index_map = {}

    def postConstructor(self):
        self._control_index = self.addDoubleValue('twist', 0.0)

    def connectToDependNode(self, node):
        om_fnc = om.MFnDagNode(node)
        self._value_index_map = {}
        if om_fnc.hasAttribute('vExtraIndex'):
            v_extra_index_plug = om_fnc.findPlug('vExtraIndex', True)
            self.connectPlugToValue(v_extra_index_plug, 0)
            self.addDoubleValue('vExtraIndex', 0)
            #
            value_index = 1
            #
            v_rotate_extra_plug = om_fnc.findPlug('vRotateExtraPoints', True)
            c = v_rotate_extra_plug.numElements()
            for i_data_index in range(c):
                i_e = v_rotate_extra_plug.elementByLogicalIndex(i_data_index)
                i_p = i_e.child(1)
                i_name = i_p.name()
                i_handle_index = AbsHandle._get_handle_index_(i_data_index, 1)
                self.connectPlugToValue(i_p, value_index)
                self.addDoubleValue(i_name, 0.0)
                self._value_index_map[i_handle_index] = value_index
                value_index += 1
            #
            v_scale_extra_plug = om_fnc.findPlug('vScaleExtraPoints', True)
            c = v_scale_extra_plug.numElements()
            for i_data_index in range(c):
                i_e = v_scale_extra_plug.elementByLogicalIndex(i_data_index)
                i_p = i_e.child(1)
                i_name = i_p.name()
                i_handle_index = AbsHandle._get_handle_index_(i_data_index, 2)
                self.connectPlugToValue(i_p, value_index)
                self.addDoubleValue(i_name, 1.0)
                self._value_index_map[i_handle_index] = value_index
                value_index += 1
        else:
            trace_error("could not find attribute")
            return

        self.finishAddingManips()
        return omui.MPxManipulatorNode.connectToDependNode(self, node)

    def preDrawUI(self, view):
        """
        Cache the viewport for use in VP 2.0 drawing.
        """
        # for i_handle_group in self._data._handle_groups:
        #     for j_handle in i_handle_group._handles:
        #         print j_handle
        pass

    def drawUI(self, draw_manager, frame_context):
        if self._handle_root._handle_groups:
            handle_index_cur = self.glActiveName()
            data_index_cur = int(self.getDoubleValue(0, False))
            handle_group_index_cur = self._handle_root._get_handle_group_index_(data_index_cur)
            handle_group_index_cur = handle_group_index_cur
            #
            handle_index = self._handle_root._handle_index
            draw_manager.beginDrawable(omrd.MUIDrawManager.kNonSelectable, handle_index)
            self.setHandleColor(draw_manager, handle_index, self.mainColor())
            draw_manager.setLineWidth(self._handle_root._line_width)
            draw_manager.setLineStyle(self._handle_root._line_style)
            #
            draw_manager.setColor(self._handle_root._color)
            self._handle_root.draw(draw_manager)
            #
            for i_handle_group in self._handle_root._handle_groups:
                i_handle_index = i_handle_group._handle_index
                #
                draw_manager.beginDrawable(omrd.MUIDrawManager.kSelectable, i_handle_index)
                self.setHandleColor(draw_manager, i_handle_index, self.mainColor())
                draw_manager.setLineWidth(i_handle_group._line_width)
                draw_manager.setLineStyle(i_handle_group._line_style)
                if self.shouldDrawHandleAsSelected(i_handle_index):
                    pass
                else:
                    draw_manager.setColor(i_handle_group._color)
                draw_manager.setPointSize(i_handle_group._point_size)
                i_handle_group.draw(draw_manager)

                if i_handle_group.is_contain_handle(handle_group_index_cur):
                    i_sub_handles = i_handle_group._handles
                    for j_handle in i_sub_handles:
                        j_handle_index = j_handle._handle_index
                        draw_manager.beginDrawable(omrd.MUIDrawManager.kSelectable, j_handle_index)
                        self.setHandleColor(draw_manager, j_handle_index, self.mainColor())
                        draw_manager.setLineWidth(j_handle._line_width)
                        draw_manager.setLineStyle(j_handle._line_style)
                        if self.shouldDrawHandleAsSelected(j_handle_index):
                            pass
                        else:
                            draw_manager.setColor(j_handle._color)
                        draw_manager.setPointSize(j_handle._point_size)
                        j_handle.draw(draw_manager)
                        if handle_index_cur == j_handle_index:
                            j_handle.draw_state_line(draw_manager)
                            j_handle.draw_information(draw_manager)
            #
            draw_manager.endDrawable()

    def doPress(self, view):
        handle_index_cur = self.glActiveName()
        if self._handle_root.has_handle_group(handle_index_cur):
            handle_group = self._handle_root.get_handle_group(handle_index_cur)
            # print handle_group._data_index
            self.setDoubleValue(0, handle_group._data_index)
        if self._handle_root.has_handle(handle_index_cur):
            handle = self._handle_root.get_handle(handle_index_cur)
            ray = self.mouseRay()
            handle.update_by_press(ray, self._control_plane, self)
            # self.setDoubleValue(0, handle._data_index)
        self.__class__.PRE_ID = self.glActiveName()

    def doDrag(self, view):
        self._local_mouse = self.mouseRay()
        handle_index_cur = self.glActiveName()
        if self._handle_root.has_handle(handle_index_cur):
            handle = self._handle_root.get_handle(handle_index_cur)
            ray = self.mouseRay()
            handle.update_by_drag(ray, self._control_plane, self)

    def doRelease(self, view):
        self._local_mouse = self.mouseRay()
        handle_index_cur = self.glActiveName()
        if self._handle_root.has_handle(handle_index_cur):
            handle = self._handle_root.get_handle(handle_index_cur)
            handle.update_by_release()
        # self.__class__.PRE_ID = self.glActiveName()

    def _get_value_index_(self, handle_index):
        if handle_index in self._value_index_map:
            return self._value_index_map[handle_index]
    @classmethod
    def _create_fnc_(cls):
        return cls()
    @classmethod
    def _initializer_fnc_(cls):
        pass


class CurveToMeshExtraContextCommand(omui.MPxContextCommand):
    NAME = "curveToMeshExtraContext"

    kNopFlag = "-nop"
    kNopLongFlag = "-noOperation"

    def __init__(self):
        omui.MPxContextCommand.__init__(self)
    @staticmethod
    def _create_fnc_():
        return CurveToMeshExtraContextCommand()

    def doQueryFlags(self):
        theParser = self.parser()
        if theParser.isFlagSet(CurveToMeshExtraContextCommand.kNopFlag):
            print("doing absolutely nothing")
        return

    def makeObj(self):
        return CurveToMeshExtraSelectionContext()

    def appendSyntax(self):
        theSyntax = self.syntax()
        theSyntax.addFlag(
            CurveToMeshExtraContextCommand.kNopFlag,
            CurveToMeshExtraContextCommand.kNopLongFlag
        )


class CurveToMeshExtraSelectionContext(omui.MPxSelectionContext):
    NAME = 'CurveToMeshExtraSelectionContext'
    @classmethod
    def _create_fnc_(cls):
        return cls()

    def __init__(self):
        """
        Initialize the members of the CurveToMeshExtraSelectionContext class.
        """
        omui.MPxSelectionContext.__init__(self)
        self.setTitleString('Plug-in manipulator: ' + CurveToMeshExtraSelectionContext.NAME)
        self._manipulator_instance = None
        self._first_shape = None
        self.active_list_modified_msg_id = -1
    # virtual
    def toolOnSetup(self, event):
        self.setHelpString('Move the object using the manipulator')

        CurveToMeshExtraSelectionContext._update_fnc_(self)
        try:
            self.active_list_modified_msg_id = om.MModelMessage.addCallback(
                om.MModelMessage.kActiveListModified,
                CurveToMeshExtraSelectionContext._update_fnc_,
                self
            )
        except:
            trace_error('{}add callback failed'.format(self.NAME))

    def toolOffCleanup(self):
        """
        Unregister the selection list callback.
        """
        try:
            om.MModelMessage.removeCallback(self.active_list_modified_msg_id)
            self.active_list_modified_msg_id = -1
        except:
            trace_error("{}: remove callback failed".format(self.NAME))

        omui.MPxSelectionContext.toolOffCleanup(self)

    def namesOfAttributes(self, attribute_names):
        """
        Return the names of the attributes of the selected objects this context will be modifying.
        """
        attribute_names.append('translateX')

    def setInitialState(self):
        node_om_fnc = om.MFnDagNode(self._first_shape)
        #
        lynxi_scale = node_om_fnc.findPlug('lynxiScale', False)
        output_u_base_surface_p = node_om_fnc.findPlug('outputUBaseSurface', False)
        output_v_base_curve_p = node_om_fnc.findPlug('outputVBaseCurve', False)
        output_surface_p = node_om_fnc.findPlug('outputSurface', False)
        # noinspection PyBroadException
        try:
            u_base_surface_node = output_u_base_surface_p.asMObject()
            v_base_curve_node = output_v_base_curve_p.asMObject()
            surface_node = output_surface_p.asMObject()
            lynxi_scale_value = lynxi_scale.asFloat()
            if (
                u_base_surface_node.isNull() is False
                and v_base_curve_node.isNull() is False
                and surface_node.isNull() is False
            ):
                handle_root = HandleRoot(
                    u_base_surface_node, v_base_curve_node, surface_node
                )
                handle_root.set_lynxi_scale(lynxi_scale_value)
                handle_root.setup()
                self._manipulator_instance._handle_root = handle_root
        except:
            om.MGlobal.displayWarning('failed to read data')
    @staticmethod
    def _validation_fnc_():
        # noinspection PyBroadException
        try:
            s_list = om.MGlobal.getActiveSelectionList()
            s_iter = om.MItSelectionList(s_list)
        except:
            trace_error('could not get active selection')
            return False

        if not s_list or s_list.length() == 0:
            return False

        while not s_iter.isDone():
            node = s_iter.getDependNode()
            if node.isNull() is False:
                if node.hasFn(om.MFn.kTransform):
                    transform_om_fnc = om.MFnDagNode(node)
                    if transform_om_fnc.childCount():
                        shape = transform_om_fnc.child(0)
                        shape_om_fnc = om.MFnDagNode(shape)
                        # noinspection PyBroadException
                        if shape_om_fnc.hasAttribute('lynxiType'):
                            return True
                else:
                    shape = node
                    shape_om_fnc = om.MFnDagNode(shape)
                    # noinspection PyBroadException
                    if shape_om_fnc.hasAttribute('lynxiType'):
                        return True
            #
            next(s_iter)
        #
        # om.MGlobal.displayWarning('node in selection list is not right type of node')
        return False
    @staticmethod
    def _update_fnc_(context):
        # clear first
        # noinspection PyBroadException
        try:
            context.deleteManipulators()
        except:
            om.MGlobal.displayWarning('no manipulators to delete')
        #
        # noinspection PyBroadException
        try:
            if not context._validation_fnc_() is True:
                return
            #
            context._manipulator_instance = None
            context._first_shape = om.MObject.kNullObj
            #
            manipulator_instance, manipulator_node = CurveToMeshExtraManipulatorNode.newManipulator('curveToMeshExtraManipulator')
            if manipulator_instance:
                # save state
                context._manipulator_instance = manipulator_instance
                # add the manipulator
                context.addManipulator(manipulator_node)
                s_list = om.MGlobal.getActiveSelectionList()
                s_iter = om.MItSelectionList(s_list)
                while not s_iter.isDone():
                    node = s_iter.getDependNode()
                    if node.isNull() is False:
                        if node.hasFn(om.MFn.kTransform):
                            transform_om_fnc = om.MFnDagNode(node)
                            if transform_om_fnc.childCount():
                                shape = transform_om_fnc.child(0)
                                shape_om_fnc = om.MFnDagNode(shape)
                                # noinspection PyBroadException
                                if shape_om_fnc.hasAttribute('lynxiType'):
                                    if not manipulator_instance.connectToDependNode(shape):
                                        om.MGlobal.displayWarning(
                                            'error connecting manipulator to node {}'.format(shape.name())
                                        )
                                        next(s_iter)
                                        continue
                                    #
                                    if context._first_shape == om.MObject.kNullObj:
                                        context._first_shape = shape
                        else:
                            shape = node
                            shape_om_fnc = om.MFnDagNode(shape)
                            if shape_om_fnc.hasAttribute('lynxiType'):
                                if not manipulator_instance.connectToDependNode(shape):
                                    om.MGlobal.displayWarning(
                                        'error connecting manipulator to node {}'.format(shape.name())
                                    )
                                    next(s_iter)
                                    continue
                                #
                                if context._first_shape == om.MObject.kNullObj:
                                    context._first_shape = shape
                    #
                    next(s_iter)
                # Allow the manipulator to set initial state
                context.setInitialState()
        except:
            om.MGlobal.displayWarning('failed to create new manipulator')
            return


# initialize
def initializePlugin(obj):
    om_plug = om.MFnPlugin(obj, 'ChangBao.Dong', '1.0.0', 'Any')
    #
    node_args = [
        (
            CurveToMeshExtraNode.NAME,
            CurveToMeshExtraNode.ID,
            CurveToMeshExtraNode._create_fnc_,
            CurveToMeshExtraNode._initializer_fnc_,
            om.MPxNode.kLocatorNode,
            CurveToMeshExtraNode.DRAW_TYPE
        ),
        (
            CurveToMeshExtraManipulatorNode.NAME,
            CurveToMeshExtraManipulatorNode.ID,
            CurveToMeshExtraManipulatorNode._create_fnc_,
            CurveToMeshExtraManipulatorNode._initializer_fnc_,
            om.MPxNode.kManipulatorNode,
        ),
    ]
    for i_node_args in node_args:
        try:
            om_plug.registerNode(*i_node_args)
        except:
            trace_error('failed to register node: "{}"'.format(i_node_args[0]))
            raise
    #
    draw_args = [
        (
            CurveToMeshExtraNode.DRAW_TYPE,
            CurveToMeshExtraNode.DRAW_ID,
            CurveToMeshExtraDrawOverride._create_fnc_
        )
    ]
    for i_draw_args in draw_args:
        try:
            omrd.MDrawRegistry.registerDrawOverrideCreator(
                *i_draw_args
            )
        except:
            trace_error('failed to register draw override: "{}"'.format(i_draw_args[0]))
            raise
    #
    context_command_args = [
        (
            CurveToMeshExtraContextCommand.NAME,
            CurveToMeshExtraContextCommand._create_fnc_
        )
    ]
    for i_context_command_args in context_command_args:
        try:
            om_plug.registerContextCommand(
                *i_context_command_args
            )
        except:
            trace_error('failed to register context command: "{}"'.format(i_context_command_args[0]))
            raise


# uninitialize
def uninitializePlugin(obj):
    om_plug = om.MFnPlugin(obj)
    #
    node_args = [
        (
            CurveToMeshExtraNode.NAME,
            CurveToMeshExtraNode.ID,
        ),
        (
            CurveToMeshExtraManipulatorNode.NAME,
            CurveToMeshExtraManipulatorNode.ID
        ),
    ]
    for i_node_args in node_args:
        # Deregister Node
        try:
            om_plug.deregisterNode(
                i_node_args[1]
            )
        except:
            trace_error('failed to deregister node: "{}"'.format(i_node_args[0]))
            raise
    #
    draw_args = [
        (
            CurveToMeshExtraNode.DRAW_TYPE,
            CurveToMeshExtraNode.DRAW_ID,
        ),
    ]
    for i_draw_args in draw_args:
        try:
            omrd.MDrawRegistry.deregisterDrawOverrideCreator(
                *i_draw_args
            )
        except:
            trace_error('failed to deregister draw: "{}"'.format(i_draw_args[0]))
            raise
    #
    context_command_args = [
        (
            CurveToMeshExtraContextCommand.NAME,
        )
    ]
    for i_context_command_args in context_command_args:
        try:
            om_plug.deregisterContextCommand(
                *i_context_command_args
            )
        except:
            trace_error('failed to deregister context command: "{}"'.format(i_context_command_args[0]))
            raise
